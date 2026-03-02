import os
import argparse
import asyncio
from dotenv import load_dotenv

from src.graph import compiled_graph
from src.state import AgentState
load_dotenv()


async def main():

    tracing_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    if tracing_enabled:
        print("🔎 LangSmith tracing is enabled.")



    print("Which repo do you want to audit?")
    print("1. Self (your own repo)")
    print("2. Peer (your assigned peer's repo)")
    choice = input("Enter 1 for self or 2 for peer [1/2]: ").strip()
    if choice == '2':
        target = 'peer'
    else:
        target = 'self'

    print(f"[main] Target set to: {target}")

    if target == 'peer':
        repo_url = os.getenv("PEER_REPO_URL")
        pdf_path = os.getenv("PEER_PDF_PATH")
    else:
        repo_url = os.getenv("REPO_URL")
        pdf_path = os.getenv("PDF_PATH")
    
    # Load rubric from file if exists
    rubric_dimensions = []
    rubric_path = os.getenv("RUBRIC_PATH", "rubric/week2_rubric.json")
    rubric_data = {}
    if os.path.exists(rubric_path):
        import json
        with open(rubric_path) as f:
            rubric_data = json.load(f)
            rubric_dimensions = rubric_data.get("dimensions", [])

    print(f"[env] TARGET: {target}")
    print(f"[env] REPO_URL: {repo_url}")
    print(f"[env] PDF_PATH: {pdf_path}")

    if not repo_url:
        raise ValueError("❌ REPO_URL (or PEER_REPO_URL) must be provided in .env")

    # Construct state
    initial_state = {
        "repo_url": repo_url,
        "pdf_path": pdf_path,
        "rubric_dimensions": rubric_dimensions,
        "evidences": {},
        "opinions": [],
        "final_report": None,
    }

    print("\n🚀 Launching Digital Courtroom...\n")

    # Execute graph
    result = await compiled_graph.ainvoke(initial_state)
    
    # Handle Pydantic model serialization for display
    final_state = result

    print("\n==============================")
    print("🏛 FINAL AUDIT REPORT")
    print("==============================")


    report = final_state.get("final_report")
    if report:
        # Handle both dict and Pydantic object
        if hasattr(report, 'executive_summary'):
            # Pydantic object
            print(f"\nExecutive Summary: {report.executive_summary}")
            print(f"Overall Score: {report.overall_score:.2f}/5.0")

            print(f"\n--- Criteria Breakdown ---")
            for criterion in getattr(report, 'criteria', []):
                print(f"\n📋 {getattr(criterion, 'dimension_name', '')}")
                print(f"   Final Score: {getattr(criterion, 'final_score', 0)}/5")
                print(f"   Judicial Opinions:")
                for op in getattr(criterion, 'judge_opinions', []):
                    print(f"     • {getattr(op, 'judge', '')}: {getattr(op, 'score', 0)}/5 - {getattr(op, 'argument', '')[:80]}...")
                if getattr(criterion, 'dissent_summary', None):
                    print(f"   ⚠️  Dissent: {getattr(criterion, 'dissent_summary')}")
                print(f"   🔧 Remediation: {getattr(criterion, 'remediation', '')[:100]}...")

            print(f"\n--- Full Remediation Plan ---")
            print(getattr(report, 'remediation_plan', ''))
        else:
            # dict
            print(f"\nExecutive Summary: {report.get('executive_summary','')}")
            print(f"Overall Score: {report.get('overall_score',0):.2f}/5.0")

            print(f"\n--- Criteria Breakdown ---")
            for criterion in report.get('criteria', []):
                print(f"\n📋 {criterion.get('dimension_name','')}")
                print(f"   Final Score: {criterion.get('final_score',0)}/5")
                print(f"   Judicial Opinions:")
                for op in criterion.get('judge_opinions', []):
                    print(f"     • {op.get('judge','')}: {op.get('score',0)}/5 - {op.get('argument','')[:80]}...")
                if criterion.get('dissent_summary'):
                    print(f"   ⚠️  Dissent: {criterion.get('dissent_summary')}")
                print(f"   🔧 Remediation: {criterion.get('remediation','')[:100]}...")

            print(f"\n--- Full Remediation Plan ---")
            print(report.get('remediation_plan',''))
    else:
        print("❌ No final report generated. Check logs for errors.")

    print("\n✅ Court session completed.")


if __name__ == "__main__":
    asyncio.run(main())