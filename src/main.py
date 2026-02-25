import os
from dotenv import load_dotenv
from src.graph import graph
import asyncio

async def main():
    """
    Execution entry point for the Automaton Auditor.
    """
    # Load environment variables
    load_dotenv()

    # Check for LangSmith tracing
    tracing_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    if tracing_enabled:
        print("LangSmith tracing is enabled.")

    # Input data
    repo_url = os.getenv("REPO_URL", "")
    pdf_path = os.getenv("PDF_PATH", "")

    if not repo_url or not pdf_path:
        print("Error: REPO_URL and PDF_PATH must be provided.")
        return

    # Initial state
    initial_state = {
        "repo_url": repo_url,
        "pdf_path": pdf_path,
    }

    # Execute the graph
    final_state = await graph.execute(initial_state)
    print("Final State:", final_state)

if __name__ == "__main__":
    asyncio.run(main())