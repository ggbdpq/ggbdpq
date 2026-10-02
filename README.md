# 你好，我是小七 (ggbdpq) 👋

**高级前端工程师 · 8 年前端，重度 AI 工具实践者。**

- 📍 深圳 · 正在看机会：**AI 前端工程师**（高级前端 / 前端 AI 应用方向）
- 📮 `ggbdpq@gmail.com`（求职邮箱）
- 二次元 · 技术宅 · 我的幸运数字是 7

![PRs merged](https://img.shields.io/badge/PRs%20merged%20to%20upstream-35-brightgreen) ![PRs in review](https://img.shields.io/badge/PRs%20in%20review-46-blue) ![Issues filed](https://img.shields.io/badge/Issues%20filed-16-orange)

## 🌱 开源贡献

数字来自 GitHub API（截至 2026-10-02），只统计被维护者合并的 PR 和仍在审核中的 PR——每一条都能点开看。

| 项目 | Stars | PR 已合并 | PR 在途 | Issue |
|---|---:|---:|---:|---:|
| [apache/maka](https://github.com/apache/maka) | 5.7k | **27** | 12 | 7 |
| [router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI) | 53.8k | 2 | 9 | – |
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | 139.5k | – | 4 | – |
| [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) | 52.3k | **5** | 2 | – |
| [stablyai/orca](https://github.com/stablyai/orca) | 83.5k | – | 6 | – |
| [multica-ai/multica](https://github.com/multica-ai/multica) | 51.8k | – | 6 | – |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | 211.4k | – | 3 | – |
| [jlcodes99/cockpit-tools](https://github.com/jlcodes99/cockpit-tools) | 18.6k | – | 4 | – |

另外向 [microsoft/vscode](https://github.com/microsoft/vscode)、[Tencent/tdesign-vue](https://github.com/Tencent/tdesign-vue)、[sheinsight/shineout](https://github.com/sheinsight/shineout)、[chengazhen/cursor-auto-free](https://github.com/chengazhen/cursor-auto-free) 提交过 9 个 issue。

- **Apache Maka**（孵化中，本地优先的 AI agent workspace）：39 个 PR（27 已合并、12 在审）覆盖 runtime、TUI、cli、文档审计等模块，另报 7 个 issue——这是我投入最多的社区，也是我理解 agent 架构的主战场。
- **Cherry Studio**（52k★ AI 桌面客户端）：5 个 PR 已合并——知识库选择记忆（会话保存时记住上次使用的库）、tooltip 悬停反馈死循环修复、apiGateway 思考 token 细分上报等。

## 🛠 我的项目

### 核心

| 项目 | 说明 |
|---|---|
| [qoder-proxy-api](https://github.com/ggbdpq/qoder-proxy-api) | **AI Protocol Layer**（v0.3.0 冻结）：本地三链路协议网关——默认适配 Qoder 客户端 Gateway 私有协议（PAT→jobToken→签名 SSE），保留 Cloud Agents 官方 API 与本地 qodercli 子进程链路；Canonical Request/Event 契约隔离上游与协议演进，对外暴露 OpenAI Chat / Responses / Anthropic Messages（流式）。89 项零凭证离线测试 + 四级验证矩阵，非 Qoder 官方项目 |
| [agent-hub](https://github.com/ggbdpq/agent-hub) | **AI Application Layer**（v0.1.1 冻结）：花语智能体——流式 Agent Event Pipeline（跨 chunk 安全的 SSE 解码）、A2UI 结构化渲染（AI 输出白名单契约）、Evidence 证据溯源、异步任务恢复（刷新按 taskId 续追到终态）四主线；契约 → API → 浏览器端到端三层 CI，演示视频见 Release |
| [coding-agent](https://github.com/ggbdpq/coding-agent) | **Agent Runtime Layer**（v0.6.0 Conformance Edition）：one spec, five runtimes——七篇行为规范（Agent Loop / Plan Mode / apply_patch / 权限闸门…）的 TypeScript / Python / Go / Rust / C# 五实现，可执行一致性套件以 4 场景 × 5 runtime 在 CI 跨版验证等价（fail closed + 红操演练） |

### 更多

| 项目 | 说明 |
|---|---|
| [cursor-loc](https://github.com/ggbdpq/cursor-loc) | 为 **Cursor IDE 专有界面**提供简体中文汉化：覆盖 Settings、Agent、Composer、Review 等 Microsoft 官方语言包无法触及的区域 |
| [agent-skills](https://github.com/ggbdpq/agent-skills) | 个人沉淀的 agent skills 公开合集：多端前端开发、技术写作、构建验证等可安装技能（陆续上架中） |
| language (lang-go) 🔒 | 自创的确定性、类型化编程语言：源码可转译到 Go 与 JS 执行，具备规范化静态/动态语义与独立第二实现验证，151 个跨实现 Conformance Case（私有仓，面试可演示） |
| syntax-party 🔒 | 中英双语的五后端语言对照学习站，灵感来自 component-party.dev：同一主题多种语言并排对照（私有仓） |

## ⚙️ 技术栈

![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white) ![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black) ![Taro](https://img.shields.io/badge/Taro-2B6CB0?logo=taro&logoColor=white) ![Node.js](https://img.shields.io/badge/Node.js-339933?logo=node.js&logoColor=white) ![Zustand](https://img.shields.io/badge/Zustand-000000?logo=react&logoColor=white)

8 年多端一线经验：H5、小程序、App 内嵌 WebView，从业务交付到模块级工程化（构建、规范、性能）都趟过。现在把 AI coding agent 编进日常工作流——贡献 agent 项目、写 agent skills、拆 agent 源码，用 AI 交付 AI 相关的需求。

---

⭐️ 感谢所有上游项目的维护者，review 使人进步。
