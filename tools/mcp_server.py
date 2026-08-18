"""FastMCP service exposing the deterministic Fortune Liuyao workflow to Nexent."""

from __future__ import annotations

import os

from fastmcp import FastMCP

from tools.fortune_runtime import cast_line, check_runtime, run_reading, verify_reading


mcp = FastMCP("Fortune Liuyao")


@mcp.tool(
    name="check_liuyao_runtime",
    description="Run the bundled Fortune Liuyao Skill self-check before the first chart in a deployment.",
)
def check_liuyao_runtime() -> dict:
    return check_runtime()


@mcp.tool(
    name="cast_liuyao_line",
    description=(
        "Generate one Liuyao line using python_secrets. Position 1 is the bottom line and 6 is the top. "
        "Call each position at most once in a staged six-line interaction."
    ),
)
def cast_liuyao_line(position: int) -> dict:
    return cast_line(position)


@mcp.tool(
    name="run_liuyao",
    description=(
        "Run sensitive-topic routing, casting, deterministic Wenwang Najia charting, rule facts, "
        "interpretation-prompt assembly, and HTML rendering through the bundled Fortune Liuyao Skill."
    ),
)
def run_liuyao(
    question: str,
    category: str = "general",
    method: str = "auto",
    lines: str = "",
    coins: str = "",
    perspective: str = "unspecified",
    timezone_name: str = "Asia/Shanghai",
) -> dict:
    return run_reading(question, category, method, lines, coins, perspective, timezone_name)


@mcp.tool(
    name="verify_liuyao_facts",
    description=(
        "Audit explicit original/changed hexagram, Shi/Ying, line-position, and Six-Relative claims "
        "in a completed draft. It does not grade auspiciousness or timing inferences."
    ),
)
def verify_liuyao_facts(run_id: str, report: str) -> dict:
    return verify_reading(run_id, report)


def main() -> None:
    mcp.run(transport="sse", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))


if __name__ == "__main__":
    main()
