# Security

不要提交 Nexent `.env`、模型凭据、API key、内部存储 URL、用户占问内容、排盘 session、
审计草稿或包含个人信息的 HTML 产物。

Demo MCP 会把问题和排盘结果写入运行目录，以便同一 run ID 做事实审计。生产环境必须增加
Nexent/租户身份认证、每租户隔离、短期 run ID、静态文件授权、加密、最短保留期、自动删除、
访问日志脱敏、速率限制和并发控制。`FORTUNE_LIUYAO_PUBLIC_BASE_URL` 应指向受控 HTTPS
地址；示例 `localhost` 仅用于本机 Demo。

高风险医疗、生死、母婴、失踪和重大财务/法律问题由 Skill 在排盘前分流。不要移除该边界，
也不要让模型在工具之外自行排盘绕过分流。
