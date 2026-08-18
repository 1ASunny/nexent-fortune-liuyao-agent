# Validation report

Status: local design validation passed on 2026-08-18 (Asia/Shanghai).

## Observed evidence

- Python unit and contract checks: 6 passed with Python 3.12.
- Python syntax compilation: passed for the MCP adapter, runtime adapter, packager, and tests.
- Bundled Fortune Liuyao `--selfcheck`: `READY`; Python runtime, timezone support, vendored
  `lunar_python`, calendar conversion, deterministic golden chart, and renderers all passed.
- Progressive Skill archive: reproducibly packaged with 64 files; validation passed.
- `dist/fortune-liuyao-skill.zip`: 426,768 bytes; SHA-256
  `846C5A9C8450BD6BA53EA930A685B2037E972C9B94FA06D06E8595D8BD64F95F`.
- Adapter contract: invalid path-like run IDs are rejected; single-line casting retains position,
  6/7/8/9 values, and the `python_secrets` source marker.

## Explicitly unexecuted

- Nexent instance/E2E execution.
- MCP registration against a live tenant.
- Official Nexent Agent export/import.
- Production storage and retention validation.

This report records only observed local checks. It does not convert local fixtures, source assets,
or documentation into evidence of a Nexent instance run.
