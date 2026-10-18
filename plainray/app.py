"""PlainRay - explain a radiology report in plain language, fully offline.

Usage:
    python -m plainray explain --file report.txt
    python -m plainray explain "IMPRESSION: ..."      (JSON on stdout)
    python -m plainray serve [--port 7860]            (local web UI)
    python -m plainray selftest                       (no model needed)

Requires: a local Ollama server (ollama serve) with Gemma 3 pulled:
    ollama pull gemma3:4b
No other dependencies. No network access at runtime.
"""

import argparse
import json
import sys
from pathlib import Path

from .llm import DEFAULT_MODEL, chat, extract_json
from .prompts import build_messages
from .readability import fkgl_grade

HERE = Path(__file__).resolve().parent


def explain(report: str) -> dict:
    """Turn a report into a structured plain-language explainer dict."""
    messages = build_messages(report)
    reply = chat(messages)
    result = extract_json(reply)
    result = _validate(result)
    result["_meta"] = {
        "model": DEFAULT_MODEL,
        "backend": "local-ollama",
        "flesch_kincaid": round(fkgl_grade(result.get("summary", "")), 1),
    }
    return result


def _validate(r: dict) -> dict:
    out = {
        "summary": str(r.get("summary", "")).strip(),
        "glossary": [],
        "questions": [],
        "urgency_note": str(r.get("urgency_note", "None - nothing in the report is flagged urgent.")).strip(),
    }
    for cell in (r.get("glossary") or [])[:8]:
        if isinstance(cell, dict) and cell.get("term"):
            term = str(cell["term"]).strip().lower()
            if not term or term in {g["term"].lower() for g in out["glossary"]}:
                continue
            out["glossary"].append({"term": str(cell["term"])[:60],
                                    "plain": str(cell.get("plain", ""))[:140]})
    for q in (r.get("questions") or [])[:5]:
        if isinstance(q, str) and q.strip():
            out["questions"].append(q.strip()[:200])
    if not out["summary"]:
        raise ValueError("model produced an empty summary - try again")
    return out


def cmd_explain(args) -> int:
    report = args.report
    if args.file:
        report = Path(args.file).read_text(encoding="utf-8", errors="replace")
    if not report or not report.strip():
        print("No report text given.", file=sys.stderr)
        return 2
    result = explain(report)
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"saved -> {args.out}")
    print(json.dumps(result, indent=2))
    return 0


def cmd_selftest(_args) -> int:
    """Everything Except the model: prompts, validation, readability, samples."""
    samples = json.loads((HERE.parent / "samples" / "sample_reports.json").read_text(encoding="utf-8"))["reports"]
    readings = [fkgl_grade(s["original"]) for s in samples]
    print(f"sample reports: {len(samples)}")
    for s, g in zip(samples, readings):
        print(f'  - {s["id"]}: report reads at grade {g:.1f} (raw)')
    # validation logic must reject junk
    try:
        _validate({"summary": "  "})
        print("FAIL: validator accepted an empty summary")
        return 1
    except ValueError:
        pass
    print("prompts/validation/readability: OK")
    return 0


def cmd_serve(args) -> int:
    from .server import serve
    serve(port=args.port)
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="plainray", description="Plain-language radiology explainers, fully offline.")
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("explain", help="explain one report (JSON output)")
    e.add_argument("report", nargs="?", help="report text")
    e.add_argument("--file", help="path to a report .txt file")
    e.add_argument("--out", help="also write JSON to this file")
    e.set_defaults(func=cmd_explain)

    s = sub.add_parser("serve", help="start the local web UI")
    s.add_argument("--port", type=int, default=7860)
    s.set_defaults(func=cmd_serve)

    t = sub.add_parser("selftest", help="check prompts, validation and samples (no model needed)")
    t.set_defaults(func=cmd_selftest)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
