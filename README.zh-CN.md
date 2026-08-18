# Nexent Fortune 六爻 Agent

本仓库模仿 `1ASunny/nexent-landscape-postcard-maker-agent` 的组织方式，为 Nexent v2.4.0
提供一份基于 `fortune-liuyao` 的 **Demo 设计**：Progressive Skill、确定性 MCP 适配层、
Agent 配置、打包脚本、测试与接入文档。

它不会让模型从零“猜一张盘”。Skill 先完成敏感问题分流、起卦、历法、文王纳甲排盘、
规则事实和 HTML 卦盘；当前 Nexent Agent 再依据返回的 `prompt` 写出聊天内完整解读，并在
回答前调用事实审计，核对本卦、变卦、世应、爻位和六亲等明确字段。

## [`$fortune-liuyao`](skill/fortune-liuyao/SKILL.md) 怎么使用？

安装并启用 Agent 后，可以直接在下一条消息里用自然语言触发，不需要手动运行排盘脚本。
例如：

```text
用六爻看一下：未来三个月我能不能找到合适工作？
```

也可以显式点名 Skill：

```text
$fortune-liuyao 帮我占一下今年求职是否顺利
```

Agent 会按 [`SKILL.md`](skill/fortune-liuyao/SKILL.md) 的流程处理：理解问题并选择领域，
让用户选择起卦方式，调用确定性引擎排盘，最后在当前对话中给出完整解读，并可附带 HTML
卦盘。对话里可选择三类起卦方式：

1. **自动起卦**

   只说问题即可，例如：`未来三个月感情会不会有进展？`

2. **逐爻生成**

   从初爻开始依次生成六爻；每一爻只生成一次，第六次完成后直接排盘。

3. **输入硬币或爻值**

   六个爻值按初爻到上爻输入：

   ```text
   7, 8, 6, 7, 9, 8
   ```

   六次硬币结果同样按初爻到上爻输入：

   ```text
   正反反 / 正正反 / 反反反 / 正反反 / 正正正 / 正正反
   ```

硬币约定为正面记 3、反面记 2；6、9 是变爻。第一次对应最下面的初爻，第六次对应最上面
的上爻。

高风险问题不会进入排盘，包括医疗诊断、生死、胎儿性别、母婴安危、失踪定位，以及需要
专业意见的重大法律或财务决策。这类问题会转向现实帮助。

## 本地开发与校验

```bash
python -m unittest discover -s tests -v
python skill/fortune-liuyao/scripts/run_liuyao.py --selfcheck
python scripts/package_skill.py
```

Docker Demo：

```bash
docker compose -f docker-compose.demo.yml up --build
```

在 Docker 版 Nexent 中可将 `http://host.docker.internal:8000/sse` 注册为 MCP 服务。完整字段
见 [Agent 配置](nexent/agent-config.md)，接入步骤见 [Nexent 设置](docs/NEXENT_SETUP.md)。

## 当前边界

- 已提供可做本地校验的代码与 Skill 包流程。
- **暂未执行 Nexent 实例/E2E 测试。**
- **未创建或伪造 Nexent 官方 Agent 导出包。**
- HTML 卦盘仅是辅助附件；每次成功排盘仍须在聊天中给出完整解读。
- 医疗、生死、母婴、失踪定位等高风险问题必须停止排盘并转向现实帮助。

本内容基于玄学体系生成，仅供文化爱好与思维参考，不构成任何重大人生决策的专业建议。
