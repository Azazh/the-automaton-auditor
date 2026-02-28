import os
from typing import List, Dict
import base64
from src.utils.llm_provider import LLMProvider
from PyPDF2 import PdfReader
from PIL import Image
import io

def extract_images_from_pdf(pdf_path: str) -> List[Image.Image]:
    """
    Extract images from a PDF file as PIL Images.
    """
    print(f"[vision_tools] Extracting images from PDF: {pdf_path}")
    if not os.path.exists(pdf_path):
        print("[vision_tools][ERROR] PDF not found.")
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    reader = PdfReader(pdf_path)
    images = []
    for page in reader.pages:
        if '/XObject' in page['/Resources']:
            xObject = page['/Resources']['/XObject'].get_object()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    data = xObject[obj]._data
                    img = Image.open(io.BytesIO(data))
                    images.append(img)
    print(f"[vision_tools] Extracted {len(images)} images.")
    return images

def classify_diagram(images: List[Image.Image], llm_vision_fn) -> List[Dict[str, str]]:
    """
    Use a multimodal LLM to classify each diagram image.
    llm_vision_fn should accept an image and return a dict with 'type' and 'flow_description'.
    """
    print(f"[vision_tools] Classifying {len(images)} images with LLM.")
    results = []
    for img in images:
        result = llm_vision_fn(img)
        results.append(result)
    print(f"[vision_tools] Classification complete.")
    return results

# --- LLM Vision Function for Layer 1 ---
def vision_llm_openrouter(img) -> Dict[str, str]:
    """
    Calls OpenRouter LLM with a base64-encoded image and a diagram classification prompt.
    Returns a dict with 'type' and 'flow_description'.
    """
    llm = LLMProvider()
    # Convert image to base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    prompt = (
        "You are a software architecture diagram classifier. "
        "Given a PNG image (base64 below), classify it as one of: "
        "'LangGraph State Machine', 'Sequence Diagram', 'Generic Flowchart', or 'Other'. "
        "Then, describe the flow in 1-2 sentences. "
        "Return a JSON object with keys 'type' and 'flow_description'.\n"
        f"Base64 PNG: {img_b64}"
    )
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    try:
        response = llm.chat(messages, temperature=0.2, max_tokens=512)
        import json as _json
        # Try to extract JSON from response
        if '{' in response:
            start = response.index('{')
            end = response.rindex('}') + 1
            json_str = response[start:end]
            return _json.loads(json_str)
        else:
            return {"type": "Unknown", "flow_description": response.strip()}
    except Exception as e:
        print(f"[vision_tools][ERROR] LLM vision call failed: {e}")
        return {"type": "Error", "flow_description": str(e)}
