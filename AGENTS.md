# AGENTS.md — profile 统计卡仓库协作约定

GitHub 个人主页仓(ggbdpq/ggbdpq)。刷新入口 `PROFILE_TOKEN=$(gh auth token) python3 scripts/build.py`,产物 `assets/*.svg` + `scripts/data.json`;README 的 `?v=` 缓存戳按 refresh.yml 同款正则跳版后一起提交推送。CI 每天 01:00 UTC 自动刷新(实际常拖到 ~05:30 UTC 甚至下午),push 触碰 `scripts/*.py` 或 `scripts/data.json` 会再触发一轮;测试:`python3 scripts/test_github_stats.py`。

## 卡片各值取数口径

| 值 | 来源 | 口径说明 |
|---|---|---|
| Merged Pull Requests | GraphQL `pullRequests(MERGED)` 节点 | **只数非私有仓**(`fetch_user` 过滤 `isPrivate`,多读取取最全 payload);总数含公开自研仓,条形明细不含 |
| Merged PRs (30 days) | search API `is:pr is:merged merged:>=今天-30天` | 搜索索引,老行不丢、对新合并滞后数小时 |
| Upstream Patch Commits | 各 patch 仓 `/stats/contributors` 总数之和 | GitHub Insights 口径:**含被 squash/改写掉的幽灵提交,聚合只增不减**;`contributors_total` 间隔读至多 3 次取最大值、连续两次一致提前收敛 |
| patch 仓发现 | 有合并 PR 的第三方仓,经资格扫描(直签提交或 Co-authored-by 署名)确认 | 只扫这些仓;纯补丁无 PR 的仓不在列(现无此类) |
| Total Contributions / Commits | GraphQL `contributionsCollection` | 近一年日历 |
| Contributed to / Issues / Stars / Repositories / Followers | GraphQL 计数 | 直读 |
| merged_by_repo 条形 | 每仓合并 PR 数 + 淡色 patch 段 | 条形值 = PR+patch 合计,footer 分解行才是 patch 数;EXCLUDE_REPOS(自研/社区)与私有仓不入明细 |
| LANGUAGES | 本人公开仓代码体量(linguist) | 反映仓内容,不反映修复活动 |
| UPSTREAM CONTRIBUTIONS | 第三方仓可达落盘提交按扩展名计行,仓权重 = 可达行数 | contributors stats 增行只在混合取不到时兜底(幽灵提交会把历史乱的仓灌水);语言事实:magpie=Go,maka/cherry/multica/cc-switch=TS |

## 已知坑(改数前必读)

- stats/contributors 与 GraphQL PR 清单都会跨副本吐矛盾快照:**聚合只增,多读取取最大**;单次读可能拿到 0 或少 1 的旧值(2026-10-31 实测:单读 0、二读 117)。
- magpie(yetone/magpie)有"积压批量落盘"形态:维护者把积压 patch 整批 rebase 推上主干,作者日期保留旧日期;重落不重复计数,按新 SHA 对账;幽灵落盘(推送后被改写)使 stats 增量 > 可达条数,报告时给区间(可达数为下限)。
- nice-21day 已转私有:公开口径下整体不入卡。
- "今天"按 UTC+8 零点切;patch 基线取昨日收官值。
- CI cron 拖延:CI 跑完之后落地的增量要等下一天。当天新增要立即上卡 → 本地 build+push,或 `gh workflow run refresh.yml -R ggbdpq/ggbdpq` 后 `gh run watch <id> --exit-status`。
- 推送被拒:`git reset --soft origin/main` 后重提(先比对两边 data.json 新旧,本地新才覆盖)。

## 查今天增量的固定动作

1. `git fetch origin` 读线上 data.json 作基线,通常无需重刷;
2. GraphQL 拉 MERGED PR 明细按 `mergedAt`(本地零点起)过滤,私有仓跳过;
3. magpie/orca stats 双读取最大,对比昨日收官;
4. 可达提交(`author=ggbdpq&since=本地零点`)与 Co-authored-by 代落清单佐证(stats 增量应可闭合对账);
5. 有增量才 build+推送,无增量只报告。
