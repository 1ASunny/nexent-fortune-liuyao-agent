"""Build a reproducible Nexent Progressive Skill archive."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


DEFAULT_SOURCE = Path("skill/fortune-liuyao")
DEFAULT_OUTPUT = Path("dist/fortune-liuyao-skill.zip")
LINK_PATTERN = re.compile(r"\]\((references/[^)#]+)(?:#[^)]+)?\)")
REQUIRED_PATHS = (
    "SKILL.md",
    "references/domain-routing.md",
    "references/interpretation-modes.md",
    "references/manual-coin-casting.md",
    "references/runtime-contract.md",
    "references/safety-boundaries.md",
    "references/frontend-contract.md",
    "scripts/run_liuyao.py",
    "scripts/cast_one_line.py",
    "scripts/verify_facts.py",
    "assets/liuyao-viewer.html",
    "vendor/lunar_python/__init__.py",
    "vendor/lunar_python-LICENSE",
)


def validate(source: Path) -> None:
    skill = source / "SKILL.md"
    if not skill.is_file():
        raise SystemExit(f"SKILL.md not found under {source}")
    content = skill.read_text(encoding="utf-8")
    if not content.startswith("---\n") or content.count("---") < 2:
        raise SystemExit("SKILL.md requires closed YAML frontmatter")
    if not re.search(r"(?m)^name:\s*fortune-liuyao\s*$", content):
        raise SystemExit("Skill name must be fortune-liuyao")
    for relative in REQUIRED_PATHS:
        if not (source / relative).is_file():
            raise SystemExit(f"Required Skill resource is missing: {relative}")
    for relative in LINK_PATTERN.findall(content):
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            raise SystemExit(f"Unsafe Skill resource path: {relative}")
        if not (source / path).is_file():
            raise SystemExit(f"Referenced resource is missing: {relative}")


def _archive_files(source: Path):
    for path in sorted(item for item in source.rglob("*") if item.is_file()):
        relative = path.relative_to(source)
        if "__pycache__" in relative.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        if relative.as_posix() == ".gitignore":
            continue
        yield path


def build(source: Path, output: Path) -> None:
    validate(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for path in _archive_files(source):
            info = ZipInfo(path.relative_to(source).as_posix(), (1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    validate(args.source) if args.validate_only else build(args.source, args.output)
    print(args.source if args.validate_only else args.output)


if __name__ == "__main__":
    main()
