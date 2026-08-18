# Test plan

## 本仓库自动化校验

- Progressive Skill frontmatter、引用资源和关键运行文件完整性。
- Skill ZIP 内容可复现且不包含 `__pycache__` / `.pyc`。
- MCP 适配器拒绝路径穿越式 `run_id`。
- 单爻工具保持初爻到上爻位置和 `python_secrets` 随机源契约。
- 原 Skill 自检覆盖 Python 版本、内置历法、金标盘和 HTML/Markdown 渲染。
- Agent 配置包含完整工具顺序、安全分流、聊天完整解读与事实审计要求。

## 暂不执行的 Nexent 实例校验

- 真实 Nexent v2.4.0 租户中的 Skill 上传与读取。
- MCP SSE 注册、工具 schema 展示和并发调用。
- 三种起卦方式的完整会话轨迹。
- 模型基于 `prompt` 的解读质量与二次事实审计。
- HTML 链接从独立用户客户端访问。
- 官方 Agent 导出后导入干净租户。
- 生产存储认证、过期、删除、审计与租户隔离。

在这些步骤真正执行前，不得在 README、截图或发布说明中将其标记为已通过。
