# Nexent Fortune Liuyao Agent

> **Demo design:** this repository provides a reproducible Nexent Progressive Skill package,
> deterministic MCP adapter, Agent configuration, tests, and integration documentation. It does
> not claim that a Nexent instance/E2E run or official Agent export has been completed.

Fortune Liuyao is designed for Nexent v2.4.0. It routes a user's question by meaning, supports
automatic casting, staged line casting, or six manually supplied coin/line results, then delegates
Wenwang Najia chart calculation to the bundled
[`fortune-liuyao`](skill/fortune-liuyao/README.md) Skill. The Nexent Agent writes the complete
interpretation in chat and sends its draft through a deterministic fact audit before answering.

## Why this design

The project keeps the workflow native to Nexent instead of building a second chat UI:

1. Nexent owns conversation, model access, tool traces, and Markdown output.
2. The Progressive Skill owns semantic routing, casting discipline, interpretation method, and safety.
3. The MCP adapter runs the Skill's deterministic engine and publishes an optional HTML chart.
4. The current Agent interprets the returned prompt; no second model or user API key is required.
5. The fact audit catches explicit chart contradictions without mechanically grading divination.

```mermaid
flowchart LR
  U["User question"] --> N["Nexent Agent"]
  N --> S["read_skill_md"]
  S --> C["Choose casting method"]
  C --> R["run_liuyao MCP tool"]
  R --> P["Deterministic chart + prompt + optional HTML"]
  P --> I["Complete interpretation draft"]
  I --> V["verify_liuyao_facts"]
  V --> O["Chat report + optional chart link"]
```

## Repository layout

```text
skill/fortune-liuyao/       bundled Fortune Liuyao Progressive Skill
tools/fortune_runtime.py    isolated deterministic adapter and run store
tools/mcp_server.py         FastMCP adapter for Nexent
nexent/agent-config.md      Agent fields, prompts, and dependency contract
docs/NEXENT_SETUP.md        proposed integration steps
docs/MANUAL_DEMO_RUNBOOK.md acceptance-oriented, currently unexecuted runbook
docs/TEST_PLAN.md           local gates and deferred Nexent instance gates
artifacts/validation/       observed local verification record
```

## Build the Skill and run local checks

```bash
python -m unittest discover -s tests -v
python skill/fortune-liuyao/scripts/run_liuyao.py --selfcheck
python scripts/package_skill.py
python scripts/package_skill.py --validate-only
```

Optional Demo MCP service:

```bash
python -m pip install .
fortune-liuyao-mcp
```

For a Docker-based Nexent deployment, register `http://host.docker.internal:8000/sse`. See the
[setup guide](docs/NEXENT_SETUP.md) and [Agent configuration](nexent/agent-config.md).

## Required tool chain

```text
read_skill_md("fortune-liuyao")
→ check_liuyao_runtime (first run in a deployment)
→ run_liuyao (or six one-time cast_liuyao_line calls, then run_liuyao)
→ complete interpretation draft from returned prompt
→ verify_liuyao_facts
→ complete chat interpretation + optional HTML chart
```

## Current verification status

- Progressive Skill archive: locally validated and reproducibly packaged.
- MCP adapter, runtime self-check, and packaging contract: local checks passed.
- Nexent instance/E2E conversation: **not executed**.
- Live MCP registration and user-side HTML download: **not executed**.
- Official Nexent Agent export: **not created**.

See the [validation report](artifacts/validation/validation-report.md).

## Safety and responsible use

- Medical diagnosis, life/death, pregnancy and fetal sex, missing-person location, and similarly
  high-risk questions are redirected before chart generation.
- Divination output is cultural interpretation, not professional medical, legal, financial, or
  major-life-decision advice.
- Production deployment needs authenticated storage, tenant isolation, expiry, deletion,
  observability, rate limits, and privacy review beyond this Demo.
- The complete interpretation must remain in chat. An HTML chart is optional and never a substitute.

## License

This integration and the bundled Fortune Liuyao Skill are distributed under Apache License 2.0.
The vendored `lunar_python` license and upstream attributions are preserved in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
