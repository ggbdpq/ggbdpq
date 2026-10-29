"""Fetch and shape GitHub contribution stats for the profile cards."""
import json
import os
import time
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date, timedelta

USERNAME = "ggbdpq"

QUERY = """query($login: String!) { user(login: $login) {
  followers { totalCount }
  pullRequests(states: MERGED, first: 100) {
    totalCount
    nodes {
      repository {
        nameWithOwner
        isPrivate
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
  }
  issues(first: 1) { totalCount }
  repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
    totalCount
    nodes { stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
  }
  contributionsCollection {
    totalCommitContributions
    contributionCalendar { totalContributions }
    commitContributionsByRepository(maxRepositories: 100) {
      contributions { totalCount }
      repository {
        nameWithOwner
        isPrivate
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
  }
  repositoriesContributedTo(first: 1) { totalCount }
} }"""

NON_CODE = {"CSS", "SCSS", "HTML", "PLpgSQL", "Shell", "Dockerfile", "Makefile",
            "Markdown", "Batchfile", "PowerShell", "INI", "TSQL"}
# ponytail: 自研仓与社区活动仓不算第三方上游，逐个点名；以后有新类别再加规则
EXCLUDE_REPOS = {"ggbdpq/cursor-loc", "nice-people-frontend-community/nice-21day",
                 "ggbdpq/qoder-proxy-api"}
# ponytail: extension map, not linguist; add a language when a new one shows up
EXT_LANG = {
    "go": "Go", "ts": "TypeScript", "tsx": "TypeScript", "js": "JavaScript",
    "jsx": "JavaScript", "mjs": "JavaScript", "cjs": "JavaScript",
    "py": "Python", "rs": "Rust", "cs": "C#", "java": "Java",
    "kt": "Kotlin", "kts": "Kotlin", "swift": "Swift", "c": "C", "h": "C",
    "cc": "C++", "cpp": "C++", "hpp": "C++", "vue": "Vue",
}


def file_language(path):
    """Language of a changed file from its extension; unknown files are Other."""
    name = path.rsplit("/", 1)[-1]
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    return EXT_LANG.get(ext, "Other")


def top_languages(sizes, limit=7, floor=0.005):
    """Top languages by size, with everything under `floor` rolled into Other."""
    total = sum(sizes.values()) or 1
    top = [(name, size) for name, size in sizes.most_common()
           if name != "Other" and size / total >= floor][:limit]
    rows = [(name, round(size / total * 100, 1)) for name, size in top]
    other = total - sum(size for _, size in top)
    if other / total >= floor:
        rows.append(("Other", round(other / total * 100, 1)))
    return rows


def merged_rows(repo_counts, patches=None):
    """Third-party upstream repos only, display name + merged count, biggest total
    (merged + upstream patches) first."""
    patches = patches or {}
    rows = [(name, count) for name, count in repo_counts.most_common()
            if name not in EXCLUDE_REPOS]
    rows.sort(key=lambda nc: (-(nc[1] + patches.get(nc[0], 0)), -nc[1], nc[0]))
    return [(name.split("/")[-1], count) for name, count in rows]


def count_patches(commits, pr_shas):
    """Commits landed outside GitHub's merge flow and outside the author's own merged
    PRs — a maintainer can push a PR head verbatim (committer stays the author), which
    is a PR landing, not a patch."""
    return sum(1 for c in commits
               if c["commit"]["committer"]["email"] != "noreply@github.com"
               and c["sha"] not in pr_shas)


def count_coauthored(commits, username, pr_numbers=(), pr_shas=()):
    """Commits by OTHERS crediting `username` via a Co-authored-by trailer — the
    maintainer's own landing of the author's patch. Commits referencing one of the
    author's merged PR numbers are squashes of those PRs (already in the PR row)."""
    n = 0
    for c in commits:
        if username.lower() in c["commit"]["author"]["email"].lower():
            continue
        if c["sha"] in pr_shas:
            continue
        msg = c["commit"]["message"]
        if not any(l.lower().startswith("co-authored-by:") and username.lower() in l.lower()
                   for l in msg.splitlines()):
            continue
        if any(f"#{num}" in msg for num in pr_numbers):
            continue
        n += 1
    return n


def search_pr_total(token, username, extra=""):
    """Merged-PR total from the search index. The index lags fresh merges but its
    old rows never vanish, unlike GraphQL replica snapshots — an independent floor."""
    query = urllib.parse.quote(f"is:pr is:merged author:{username} {extra}".strip())
    request = urllib.request.Request(
        f"https://api.github.com/search/issues?q={query}",
        headers={"Authorization": f"Bearer {token}", "User-Agent": f"{username}-profile"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["total_count"]


def merged_recent_count(token, username, days=30):
    """Merged PRs across GitHub in the last `days` days — recent momentum."""
    since = (date.today() - timedelta(days=days)).isoformat()
    return search_pr_total(token, username, f"merged:>={since}")


def merged_pr_refs(token, username, repo):
    """Numbers and commit SHAs of the author's merged PRs in `repo`."""
    query = urllib.parse.quote(f"is:pr is:merged author:{username} repo:{repo}")
    request = urllib.request.Request(
        f"https://api.github.com/search/issues?q={query}",
        headers={"Authorization": f"Bearer {token}", "User-Agent": f"{username}-profile"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        numbers = [item["number"] for item in json.load(response)["items"]]
    shas = set()
    for number in numbers:
        request = urllib.request.Request(
            f"https://api.github.com/repos/{repo}/pulls/{number}/commits?per_page=100",
            headers={"Authorization": f"Bearer {token}", "User-Agent": f"{username}-profile"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            shas.update(c["sha"] for c in json.load(response))
    return numbers, shas


def repo_language_map(user):
    """name -> [(language, size)] for public repos the user committed or PR'd to."""
    out = {}
    for row in user["contributionsCollection"]["commitContributionsByRepository"]:
        repo = row["repository"]
        if repo and not repo["isPrivate"]:
            out[repo["nameWithOwner"]] = [(e["node"]["name"], e["size"])
                                          for e in repo["languages"]["edges"]]
    for node in user["pullRequests"]["nodes"]:
        repo = node["repository"]
        if repo and not repo["isPrivate"]:
            out.setdefault(repo["nameWithOwner"], [(e["node"]["name"], e["size"])
                                                   for e in repo["languages"]["edges"]])
    return out


def _api_get(token, username, url):
    request = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {token}", "User-Agent": f"{username}-profile"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def authored_commit_mix(token, username, repo, max_commits=200):
    """Language mix of this user's authored commits on the default branch. The
    commit detail API caps `files` at 300, so a huge commit is counted partially."""
    commits = _get_commits(token, username, repo, f"author={username}")
    mix = Counter()
    for commit in commits[:max_commits]:
        try:
            detail = _api_get(token, username,
                              f"https://api.github.com/repos/{repo}/commits/{commit['sha']}")
        except Exception:
            continue
        for changed in detail.get("files", []):
            mix[file_language(changed.get("filename", ""))] += changed.get("additions", 0)
    return mix


def _get_commits(token, username, repo, query, max_pages=20):
    """All commits matching `query`, following Link pagination up to max_pages."""
    import re
    out, url = [], f"https://api.github.com/repos/{repo}/commits?{query}&per_page=100"
    for _ in range(max_pages):
        request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "User-Agent": f"{username}-profile"})
        with urllib.request.urlopen(request, timeout=30) as response:
            page = json.load(response)
            link = response.headers.get("Link", "")
        out.extend(page)
        m = re.search(r'<([^>]+)>; rel="next"', link)
        if not m or len(page) < 100:
            return out
        url = m.group(1)
    return out


def fetch_patches(token, username, repos):
    """Upstream-applied patch commits per third-party repo. The scan below only
    decides which repos qualify (commits of mine that landed outside my merged
    PRs); the reported number is GitHub's own contributors-stats total — the same
    one the repo's Insights graph shows. Hand-rolled attribution kept drifting
    from that cached number (aligned three times now), so it gates but no longer
    counts."""
    counts = {}
    for repo in repos:
        authored = _get_commits(token, username, repo, f"author={username}")
        all_commits = _get_commits(token, username, repo, "since=2026-10-01T00:00:00Z")
        # ponytail: 资格扫描只回看一个月；高频仓一个月的量也用不满
        has_direct = any(c["commit"]["committer"]["email"] != "noreply@github.com" for c in authored)
        credited = count_coauthored(all_commits, username)
        if not has_direct and not credited:
            continue
        numbers, shas = merged_pr_refs(token, username, repo)
        n = count_patches(authored, shas) + count_coauthored(all_commits, username, set(numbers), shas)
        if n:
            try:
                counts[repo] = contributors_total(token, username, repo)
            except RuntimeError:
                counts[repo] = n  # ponytail: stats still recomputing, keep the card buildable
    return counts


def stats_total(stats, username):
    """`username`'s commit total from a /stats/contributors payload (author is None
    for deleted accounts)."""
    return sum(s["total"] for s in stats
               if s.get("author") and s["author"]["login"].lower() == username.lower())


def contributors_activity(token, username, repo, attempts=8):
    """(commits, additions, deletions) GitHub's contributors stats attribute to
    `username` in `repo`, or None while the stats are still recomputing (202)."""
    for _ in range(attempts):
        request = urllib.request.Request(
            f"https://api.github.com/repos/{repo}/stats/contributors",
            headers={"Authorization": f"Bearer {token}", "User-Agent": f"{username}-profile"},
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                stats = json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code != 202:
                raise
            time.sleep(3)
            continue
        rows = [s for s in stats
                if s.get("author") and s["author"]["login"].lower() == username.lower()]
        if rows:
            return (stats_total(rows, username),
                    sum(w["a"] for row in rows for w in row["weeks"]),
                    sum(w["d"] for row in rows for w in row["weeks"]))
        time.sleep(3)
    return None


def contributors_total(token, username, repo, reads=3, gap=15):
    """Commit count the Insights contributors graph shows for `username`. The endpoint
    serves divergent cached snapshots around pushes (magpie: 84 -> 86 -> 84 -> 87 within
    an hour), and rewritten-away commits stay counted (orca: 14 stats vs 1 reachable),
    so the aggregate only grows — the largest of a few spaced reads is the settled
    number the graph lands on."""
    best, prev = 0, None
    for i in range(reads):
        activity = contributors_activity(token, username, repo)
        if activity:
            best = max(best, activity[0])
            if activity[0] == prev:
                break  # 连续两次一致,缓存已稳定
            prev = activity[0]
        if i + 1 < reads:
            time.sleep(gap)
    if best:
        return best
    raise RuntimeError(f"{repo}: contributors stats never became ready")


def fetch_upstream_contributions(token, username, repo_langs):
    """Language mix of this user's work in third-party repos. The language split
    comes from the files in their landed commits; the repo weight is GitHub's
    contributor-stats additions (the Insights number), falling back to the
    commit files or the repo's own language mix when those are unavailable."""
    weighted = Counter()
    for repo, langs in repo_langs.items():
        if repo.split("/")[0].lower() == username.lower() or repo in EXCLUDE_REPOS:
            continue
        try:
            mix = authored_commit_mix(token, username, repo)
        except Exception:
            mix = Counter()
        try:
            activity = contributors_activity(token, username, repo)
        except Exception:
            activity = None
        weight = (activity[1] if activity and activity[1]
                  else sum(mix.values()))
        if not weight:
            continue
        mix_total = sum(mix.values())
        if mix_total:
            shares = {lang: size / mix_total for lang, size in mix.items()}
        else:
            size_total = sum(size for _, size in langs) or 1
            shares = {lang: size / size_total for lang, size in langs}
        for lang, share in shares.items():
            weighted[lang] += weight * share
    return {
        "upstream_languages": top_languages(weighted),
    }


def fetch_user(token, username, reads=3, gap=15):
    """User payload with the merged-PR total settled across reads. GraphQL serves
    divergent replica snapshots: CI twice saw 82 while ground truth was 83, and the
    counter can also disagree with its own node list. Merges are irreversible, so
    keep the payload of the read with the largest max(len(nodes), totalCount)."""
    best, best_n, prev = None, 0, None
    for i in range(reads):
        request = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": QUERY, "variables": {"login": username}}).encode(),
            headers={"Authorization": f"Bearer {token}", "User-Agent": f"{username}-profile"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            user = json.load(response)["data"]["user"]
        n = max(len(user["pullRequests"]["nodes"]), user["pullRequests"]["totalCount"])
        if n > best_n:
            best, best_n = user, n
        if n == prev:
            break  # 连续两次一致,缓存已稳定
        prev = n
        if i + 1 < reads:
            time.sleep(gap)
    return best, best_n


def fetch_data(token, username=USERNAME):
    # 多读取仍在:副本滞后时(实测 CI 见到 82、真值 83)取最全的那份 payload
    user, _ = fetch_user(token, username)

    sizes = Counter()
    for repo in user["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            sizes["Other" if name in NON_CODE else name] += edge["size"]
    languages = top_languages(sizes)

    calendar = user["contributionsCollection"]
    repo_counts = Counter(node["repository"]["nameWithOwner"]
                          for node in user["pullRequests"]["nodes"] if node["repository"])
    patch_counts = fetch_patches(token, username,
                                 [name for name in repo_counts if name not in EXCLUDE_REPOS])
    patches_by_repo = sorted(((name.split("/")[-1], count) for name, count in patch_counts.items() if count),
                             key=lambda item: (-item[1], item[0]))
    upstream = fetch_upstream_contributions(token, username, repo_language_map(user))
    try:
        merged_recent = merged_recent_count(token, username)
    except Exception:
        merged_recent = None  # ponytail: rate-limited search keeps the cached row out
    return {
        "merged_recent": merged_recent,
        "contributions": calendar["contributionCalendar"]["totalContributions"],
        "commits": calendar["totalCommitContributions"],
        # 只数公开仓:CI 的 bot 令牌天然看不见私有仓,本人令牌能看见,不过滤则两边视角
        # 会轮流改写这个数字(nice-21day 转私有后实测 86/87 来回)。first:100 一页在可见的
        # 量级下用不满,超了再补分页
        "merged_prs": sum(1 for node in user["pullRequests"]["nodes"]
                          if not node["repository"]["isPrivate"]),
        "issues": user["issues"]["totalCount"],
        "merged_by_repo": merged_rows(repo_counts, patch_counts),
        "patches_by_repo": patches_by_repo,
        "repositories": user["repositories"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in user["repositories"]["nodes"]),
        "contributed_to": user["repositoriesContributedTo"]["totalCount"],
        "followers": user["followers"]["totalCount"],
        "languages": languages,
        **upstream,
    }
