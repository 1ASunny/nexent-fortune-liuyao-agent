"""Thin, deterministic adapter around the bundled Fortune Liuyao Skill.

The adapter intentionally delegates chart calculation, safety routing, rendering,
prompt assembly, and fact verification to the bundled Skill. It adds only run
isolation and a stable MCP-facing response contract.
"""

from __future__ import annotations

import importlib
import json
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = Path(
    os.environ.get("FORTUNE_LIUYAO_SKILL_ROOT", REPOSITORY_ROOT / "skill" / "fortune-liuyao")
).resolve()
RUN_ID_PATTERN = re.compile(r"^[0-9a-f]{32}$")


def _skill_module(name: str):
    scripts = SKILL_ROOT / "scripts"
    vendor = SKILL_ROOT / "vendor"
    for path in (scripts, vendor):
        value = str(path)
        if value not in sys.path:
            sys.path.insert(0, value)
    return importlib.import_module(name)


def _output_root(explicit: Path | None = None) -> Path:
    root = explicit or Path(os.environ.get("FORTUNE_LIUYAO_OUTPUT_DIR", "outputs"))
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


def _run_dir(run_id: str, output_root: Path | None = None) -> Path:
    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise ValueError("run_id must be the 32-character identifier returned by run_liuyao")
    root = _output_root(output_root)
    candidate = (root / run_id).resolve()
    if candidate.parent != root:
        raise ValueError("run_id resolved outside the configured output directory")
    return candidate


def check_runtime() -> dict[str, Any]:
    """Return the Skill's own Python, calendar, engine, and renderer self-check."""
    return _skill_module("run_liuyao").selfcheck()


def cast_line(position: int) -> dict[str, Any]:
    """Generate exactly one cryptographically random line for positions 1 through 6."""
    if position not in range(1, 7):
        raise ValueError("position must be between 1 (bottom) and 6 (top)")
    return _skill_module("cast_one_line").cast_one(position)


def run_reading(
    question: str,
    category: str = "general",
    method: str = "auto",
    lines: str = "",
    coins: str = "",
    perspective: str = "unspecified",
    timezone_name: str = "Asia/Shanghai",
    *,
    output_root: Path | None = None,
    public_base_url: str | None = None,
) -> dict[str, Any]:
    """Run the Skill's unified entry and expose only Nexent-relevant artifacts."""
    if not question.strip():
        raise ValueError("question is required")
    run_id = uuid.uuid4().hex
    run_dir = _output_root(output_root) / run_id
    module = _skill_module("run_liuyao")
    response = module.run(
        question.strip(),
        category,
        method,
        timezone_name,
        lines or None,
        coins or None,
        None if perspective == "unspecified" else perspective,
        artifact_dir=run_dir,
        artifact_stem="chart",
    )
    if response.get("blocked"):
        return {
            "schemaVersion": "nexent-fortune-liuyao-run.v1",
            "ok": False,
            "blocked": True,
            "safety": response.get("safety"),
        }

    run_dir.mkdir(parents=True, exist_ok=True)
    session_path = run_dir / "session.json"
    session_path.write_text(json.dumps(response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    base = public_base_url
    if base is None:
        base = os.environ.get("FORTUNE_LIUYAO_PUBLIC_BASE_URL", "")
    chart_url = f"{base.rstrip('/')}/{run_id}/chart.html" if base else None
    return {
        "schemaVersion": "nexent-fortune-liuyao-run.v1",
        "ok": True,
        "blocked": False,
        "run_id": run_id,
        "result": response["result"],
        "prompt": response["prompt"],
        "artifacts": {"html": chart_url},
        "notice": "HTML is optional; the complete interpretation must still be returned in chat.",
    }


def verify_reading(
    run_id: str,
    report: str,
    *,
    output_root: Path | None = None,
) -> dict[str, Any]:
    """Audit explicit chart claims in an Agent draft without grading divination."""
    if not report.strip():
        raise ValueError("report is required")
    session_path = _run_dir(run_id, output_root) / "session.json"
    if not session_path.is_file():
        raise FileNotFoundError("unknown or expired run_id")
    session = json.loads(session_path.read_text(encoding="utf-8"))
    return _skill_module("verify_facts").verify_report(report, session["result"])
