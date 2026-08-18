# Nexent 接入（建议 Demo 配置）

本文是接入方案，不是已经执行过的部署记录。

## 1. 构建并安装 Progressive Skill

```bash
python scripts/package_skill.py
```

在 Nexent Skill repository 中上传 `dist/fortune-liuyao-skill.zip`。

## 2. 启动 Demo MCP 服务

```bash
docker compose -f docker-compose.demo.yml up --build
```

当 Nexent 运行在 Docker 中时，可将 `http://host.docker.internal:8000/sse` 注册为 MCP 服务。
服务暴露四个工具：运行时自检、逐爻生成、统一排盘和事实审计。示例 Nginx 只负责公开 HTML
卦盘；生产环境必须改用带认证、过期、删除与租户隔离的对象存储。

## 3. 创建 Agent

按 `nexent/agent-config.md` 填写 Agent 字段、Duty prompt、Constraint prompt 和对话开场白，
绑定 `fortune-liuyao` Skill、`read_skill_md` 以及四个 MCP 工具。

## 4. 实例验证与官方导出（本版本未执行）

在全新会话中验证可见顺序：

```text
read_skill_md
→ check_liuyao_runtime（部署首次）
→ run_liuyao（或六次 cast_liuyao_line 后再 run_liuyao）
→ Agent 形成完整解读草稿
→ verify_liuyao_facts
→ 聊天完整解读 + 可选 HTML 卦盘
```

确认敏感问题不排盘、手动输入顺序无误、事实审计通过、聊天正文不依赖 HTML 后，再通过
Nexent 官方功能导出 Agent。不要手工制作并声称某个 ZIP 是官方 Agent 导出包。
