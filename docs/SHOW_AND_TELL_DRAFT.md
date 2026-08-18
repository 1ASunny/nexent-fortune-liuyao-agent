# Fortune Liuyao on Nexent — Show & Tell 草稿

## 一句话

把“模型自由猜盘”拆成可审计链路：Skill 负责确定性排盘，Nexent Agent 负责语义理解与综合
解读，最后再由程序核对明确盘面事实。

## 演示主线

1. 用户提出一个清晰的事业问题并选择自动起卦。
2. Agent 加载 Progressive Skill，不在提示词中复制整套规则。
3. MCP 运行内置历法和文王纳甲引擎，返回卦盘、规则事实、解读上下文与 HTML。
4. Agent 在聊天中写完整解读，而非只给附件或一句摘要。
5. Fact audit 只检查本卦、变卦、世应、爻位和六亲，不机械裁决吉凶与应期。

## 诚实边界

当前仓库提供代码、Skill 包、配置、文档和本地校验；尚未执行 Nexent 实例/E2E，也未生成
官方 Agent 导出包。演示前必须按 Manual runbook 补齐真实工具轨迹与用户侧 HTML 访问证据。
