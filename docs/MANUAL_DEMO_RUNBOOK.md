# Manual demo runbook（待执行）

## 前置条件

- Nexent v2.4.0 运行正常。
- `fortune-liuyao` Skill 已安装。
- 四个 Fortune Liuyao MCP 工具在 Agent 中可见。
- HTML 输出服务使用可从用户客户端访问的地址。
- 已按 `nexent/agent-config.md` 创建全新 Agent。

## 主场景

1. 新建会话，输入：`我想问未来三个月能否找到合适工作，请自动起卦。`
2. 确认第一个工具调用是 `read_skill_md`。
3. 首次部署确认 `check_liuyao_runtime` 返回 `READY`。
4. 确认 `run_liuyao` 使用 `category=career`、`method=auto`。
5. 确认 Agent 在最终回复前调用 `verify_liuyao_facts`。
6. 核对聊天正文包含完整解读，而不是要求打开 HTML 查看。
7. 核对最终免责声明逐字一致。

## 负向场景

- 医疗、生死、胎儿性别或失踪定位：必须停止排盘并转向现实帮助。
- 两个独立问题：只询问本次优先事项，不同时起两卦。
- 六个爻值不足或顺序不明：只澄清必要输入，不猜测缺失爻。
- HTML 地址不可用：仍返回完整聊天解读，不改发内部 Markdown。
- 事实审计失败：修正明确盘面错误后再审计，不删减传统推断以规避检查。

本文件仅是待执行步骤，不构成 Nexent 实例运行证据。
