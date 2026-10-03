# 你好，我是小七 (ggbdpq) 👋

**高级前端工程师 · 2018 年起从事 Web 开发，实践 AI 应用与 Agent 工程。**

- 📍 深圳 · 正在看机会：**AI 应用 / Agent 工程（Web + Node）**，也关注高级前端岗位
- 📮 `ggbdpq@gmail.com`（求职邮箱）
- 二次元 · 技术宅 · 我的幸运数字是 7

## 🌱 开源贡献

截至 2026-10-03，以下 5 个公开上游仓库中：**36 个 PR 已合并、41 个 PR 开放、16 个 PR 关闭未合并**。

| 项目 | PR 已合并 | PR 开放 | PR 关闭未合并 | Issue |
|---|---:|---:|---:|---:|
| [apache/maka](https://github.com/apache/maka) | 27 | 12 | 6 | 7 |
| [router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI) | 2 | 8 | 9 | 0 |
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | 1 | 9 | 0 | 0 |
| [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) | 5 | 3 | 0 | 0 |
| [stablyai/orca](https://github.com/stablyai/orca) | 1 | 9 | 1 | 0 |

复核方式：[已合并](https://github.com/search?q=is%3Apr+author%3Aggbdpq+is%3Amerged&type=pullrequests)、[开放](https://github.com/search?q=is%3Apr+author%3Aggbdpq+is%3Aopen&type=pullrequests)、[关闭未合并](https://github.com/search?q=is%3Apr+author%3Aggbdpq+is%3Aclosed+is%3Aunmerged&type=pullrequests)、[issue](https://github.com/search?q=is%3Aissue+author%3Aggbdpq&type=issues)，各查询再按表中仓库筛选；不把全站检索总数当作本表统计。

- **[Apache Maka（孵化中）](https://incubator.apache.org/projects/maka.html)**：投入最多的社区，27 个已合并 PR 覆盖 runtime、runtime-host、desktop、cli 的缺陷修复、测试预算钉界与 flaky 基线定性，以及 10 篇文档组对照实现的审计。代表工作：[#4815](https://github.com/apache/maka/pull/4815) 让 structured-only Messages 被准入并保持模型可见，配合 [#5118](https://github.com/apache/maka/pull/5118) 修好结构化历史在编辑重发 / rewind 场景被误拒的问题。
- **CLIProxyAPI**（聚合多家模型供应商的本地代理网关，Go）：2 个已合并 PR——translator 层把 tool-result 的 cache_control 上移到块（[#5432](https://github.com/router-for-me/CLIProxyAPI/pull/5432)）、xAI grok 客户端钉定版本升至 1.0.44（[#6252](https://github.com/router-for-me/CLIProxyAPI/pull/6252)）。上游迭代很快，先后有 4 单交付后被同题实现吸收取代而关闭。
- **cc-switch**（Rust 的 AI 供应商切换工具）：已合并 [#7741](https://github.com/farion1231/cc-switch/pull/7741)——DeepSeek 系上游把思考内容以内联 `<think>/<thinking>` 标签混进正文，为其 Claude 流式路径实现跨 chunk 安全的流首剥离状态机。
- **Cherry Studio**（52k★ AI 桌面客户端）：5 个已合并 PR——保存会话到知识库时记住上次选用的库（[#21193](https://github.com/CherryHQ/cherry-studio/pull/21193)）、tooltip 悬停反馈死循环修复（[#21214](https://github.com/CherryHQ/cherry-studio/pull/21214)）、DeepSeek harness 就绪探测接受相对 Location（[#21271](https://github.com/CherryHQ/cherry-studio/pull/21271)）、apiGateway 兼容适配器上报 reasoning / 用量 token 细分（[#21275](https://github.com/CherryHQ/cherry-studio/pull/21275)、[#21276](https://github.com/CherryHQ/cherry-studio/pull/21276)）。[作者 PR](https://github.com/CherryHQ/cherry-studio/pulls?q=is%3Apr+author%3Aggbdpq+is%3Amerged)可逐条查阅。
- **orca**（AI IDE）：已合并 [#24164](https://github.com/stablyai/orca/pull/24164)——`.rake`、`Guardfile`、`Podfile` 等 Ruby 生态文件没有语法高亮，为编辑器语言识别补齐扩展名 / 文件名映射；修法落在手维护的语言探测层而不是生成器产物，避免被覆盖。

## 🛠 我的项目

| 项目 | 公开实现与验证边界 |
|---|---|
| [qoder-proxy-api](https://github.com/ggbdpq/qoder-proxy-api) | **协议适配层**：[v0.3.0](https://github.com/ggbdpq/qoder-proxy-api/releases/tag/v0.3.0)。三类上游通过 Canonical Request/Event 接入 Chat、Responses、Messages 的文本接口；包含 89 项无凭证离线测试，可用 `node --test` 复现。Gateway 保持实验性，当前不宣称完整工具循环或多模态兼容 |
| [agent-hub](https://github.com/ggbdpq/agent-hub) | **AI 应用工程演示**：[v0.1.1](https://github.com/ggbdpq/agent-hub/releases/tag/v0.1.1)。花卉选购场景，跨 chunk SSE、固定 schema 卡片、fixture 依据展示、页面刷新后按 taskId 续追；[公开三层 CI](https://github.com/ggbdpq/agent-hub/actions/runs/36803101833)。演示不等于推荐质量、可信度算法或后端重启续跑 |
| [coding-agent](https://github.com/ggbdpq/coding-agent) | **Agent Runtime 实验**：[v0.6.0](https://github.com/ggbdpq/coding-agent/releases/tag/v0.6.0)。七主题行为规范、五语言实现、四个离线一致性场景，对选定观测使用统一期望判定；不宣称全行为等价、系统沙箱或补丁 I/O 事务原子性 |

这三个项目各自研究协议、应用和 Runtime，尚未证明它们组成一条集成产品链路。公开仓的代码、测试与 Release 是可查看的证据；历史公开 CI 与本轮局部验证分别说明范围。

### 更多

- [cursor-loc](https://github.com/ggbdpq/cursor-loc)：Cursor 界面汉化项目。
- [agent-skills](https://github.com/ggbdpq/agent-skills)：个人 agent skills 公开合集。

## ⚙️ 技术栈

![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white) ![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black) ![Taro](https://img.shields.io/badge/Taro-2B6CB0?logo=taro&logoColor=white) ![Node.js](https://img.shields.io/badge/Node.js-339933?logo=node.js&logoColor=white) ![Zustand](https://img.shields.io/badge/Zustand-000000?logo=zustand&logoColor=white)

React / Vue / TypeScript、Taro、Node.js、HTTP / SSE、状态管理与契约测试。从多端业务交付延伸到 AI 应用工程，关注模型输出进入产品后的数据、状态、失败路径和验证。

⭐️ 感谢上游维护者的评审与反馈。
