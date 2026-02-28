
"""
VisionInspector Tool: Diagram Classification & Flow Extraction
Uses LLMProvider to analyze extracted images/diagrams for rubric compliance.
"""
from typing import List, Dict, Any
from src.utils.llm_provider import LLMProvider
from PyPDF2 import PdfReader
from PIL import Image
import io
import os
from typing import List, Dict
import base64       
from src.utils.llm_provider import LLMProvider
import io

class VisionInspector:
    """
    Analyzes diagrams/images (e.g., from PDF) to classify type and extract flow structure.
    Uses LLMProvider for reasoning about the diagram content.
    """
    def __init__(self, provider: str = None, model: str = None):
        self.llm = LLMProvider(provider=provider, model=model)

    def classify_diagram(self, diagram_description: str) -> Dict[str, Any]:
        """
        Classifies a diagram based on its textual description (from OCR or alt text).
        Returns dict with 'type' and 'flow_structure'.
        """
        system_prompt = (
            "You are VisionInspector, a forensic diagram analyst. "
            "Given a diagram description, classify it as one of: 'LangGraph State Machine', 'Sequence Diagram', 'Generic Flowchart', or 'Other'. "
            "Then, describe the flow structure, focusing on whether it shows: "
            "(a) Parallel fan-out/fan-in for Detectives and Judges, "
            "(b) Linear pipeline, or "
            "(c) Something else. "
            "Be objective and concise."
        )
        user_prompt = f"""
Diagram Description:
{diagram_description}

Instructions:
- Classify the diagram type.
- Describe the flow structure, especially parallelism and synchronization points.
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response = self.llm.chat(messages, temperature=0.0, max_tokens=256)
        # Simple parsing: expect LLM to return a short JSON or structured text
        # Try to extract type and flow_structure
        result = {"type": None, "flow_structure": None, "raw": response}
        import re
        type_match = re.search(r"type\s*[:=]\s*([\w\- ]+)", response, re.I)
        flow_match = re.search(r"flow[_ ]structure\s*[:=]\s*([\w\- ,]+)", response, re.I)
        if type_match:
            result["type"] = type_match.group(1).strip()
        if flow_match:
            result["flow_structure"] = flow_match.group(1).strip()
        return result

    def analyze_images(self, diagram_descriptions: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze a list of diagram descriptions, returning classification and flow for each.
        """
        results = []
        for desc in diagram_descriptions:
            results.append(self.classify_diagram(desc))
        return results

def extract_images_from_pdf(pdf_path: str) -> List[Image.Image]:
    """
    Extract images from a PDF file as PIL Images.
    Note: pdf_path must be a local file path, not a URL. If a URL is passed, this will fail with FileNotFoundError.
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
