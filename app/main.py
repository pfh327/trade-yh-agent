from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from app.agents.orchestrator import TradeCareOrchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the TradeCare multi-agent customer support workflow.")
    parser.add_argument("--query", required=True, help="Customer inquiry text.")
    parser.add_argument(
        "--knowledge-dir",
        default=str(Path(__file__).resolve().parents[1] / "data" / "knowledge_base"),
        help="Path to markdown knowledge base directory.",
    )
    parser.add_argument("--json", action="store_true", help="Print full JSON trace.")
    parser.add_argument("--use-llm", action="store_true", help="Use paid LLM/API mode when OPENAI_API_KEY is set.")
    parser.add_argument("--model", default=None, help="Model name for paid LLM/API mode.")
    return parser


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = build_parser().parse_args()
    orchestrator = TradeCareOrchestrator(Path(args.knowledge_dir), use_llm=args.use_llm, model=args.model)
    result = orchestrator.run(args.query)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["final_answer"])


if __name__ == "__main__":
    main()
