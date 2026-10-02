# 你好，我是小七 (ggbdpq) 👋

**高级前端工程师 · 2018 年起从事 Web 开发，实践 AI 应用与 Agent 工程。**

- 📍 深圳 · 正在看机会：**AI 应用 / Agent 工程（Web + Node）**，也关注高级前端岗位
- 📮 `ggbdpq@gmail.com`（求职邮箱）
- 二次元 · 技术宅 · 我的幸运数字是 7

## 🌱 开源贡献

截至 2026-10-02，以下 12 个公开上游仓库中：**34 个 PR 已合并、50 个 PR 开放、15 个 PR 关闭未合并、16 个 issue**。仅统计作者 `ggbdpq`，不包含个人仓或其他仓库；开放状态不等于已获审核。GitHub 状态会继续变化，这是指定时点快照。

| 项目 | PR 已合并 | PR 开放 | PR 关闭未合并 | Issue |
|---|---:|---:|---:|---:|
| [apache/maka](https://github.com/apache/maka) | 27 | 12 | 6 | 7 |
| [router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI) | 2 | 10 | 7 | 0 |
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | 0 | 6 | 0 | 0 |
| [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) | 5 | 2 | 0 | 0 |
| [stablyai/orca](https://github.com/stablyai/orca) | 0 | 7 | 1 | 0 |
| [multica-ai/multica](https://github.com/multica-ai/multica) | 0 | 6 | 0 | 0 |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | 0 | 3 | 1 | 0 |
| [jlcodes99/cockpit-tools](https://github.com/jlcodes99/cockpit-tools) | 0 | 4 | 0 | 0 |
| [microsoft/vscode](https://github.com/microsoft/vscode) | 0 | 0 | 0 | 1 |
| [Tencent/tdesign-vue](https://github.com/Tencent/tdesign-vue) | 0 | 0 | 0 | 4 |
| [sheinsight/shineout](https://github.com/sheinsight/shineout) | 0 | 0 | 0 | 3 |
| [chengazhen/cursor-auto-free](https://github.com/chengazhen/cursor-auto-free) | 0 | 0 | 0 | 1 |

复核方式：[已合并](https://github.com/search?q=is%3Apr+author%3Aggbdpq+is%3Amerged&type=pullrequests)、[开放](https://github.com/search?q=is%3Apr+author%3Aggbdpq+is%3Aopen&type=pullrequests)、[关闭未合并](https://github.com/search?q=is%3Apr+author%3Aggbdpq+is%3Aclosed+is%3Aunmerged&type=pullrequests)、[issue](https://github.com/search?q=is%3Aissue+author%3Aggbdpq&type=issues)，各查询再按表中仓库筛选；不把全站检索总数当作本表统计。

- **[Apache Maka（孵化中）](https://incubator.apache.org/projects/maka.html)**：参与具体问题修复、测试和文档审计。已合并的 [#4815](https://github.com/apache/maka/pull/4815) 涉及结构化消息准入与重放可见性；我是模块贡献者，不是整体架构负责人。
- **Cherry Studio**：贡献已合并的交互与使用量相关修复。[作者 PR](https://github.com/CherryHQ/cherry-studio/pulls?q=is%3Apr+author%3Aggbdpq+is%3Amerged)可逐条查阅。

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
