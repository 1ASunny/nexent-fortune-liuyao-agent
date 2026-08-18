from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "fortune-liuyao" / "SKILL.md"
AGENT_CONFIG = ROOT / "nexent" / "agent-config.md"


class SkillContractTests(unittest.TestCase):
    def test_skill_keeps_unified_entry_and_fact_audit(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("scripts/run_liuyao.py", text)
        self.assertIn("scripts/verify_facts.py", text)
        self.assertIn("本内容基于玄学体系生成", text)

    def test_agent_config_keeps_required_tool_order_and_safety(self) -> None:
        text = AGENT_CONFIG.read_text(encoding="utf-8")
        for tool in (
            "read_skill_md",
            "check_liuyao_runtime",
            "run_liuyao",
            "verify_liuyao_facts",
        ):
            self.assertIn(tool, text)
        self.assertIn("不排盘", text)
        self.assertIn("完整解读", text)


if __name__ == "__main__":
    unittest.main()
