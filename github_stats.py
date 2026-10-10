"""Fetch and shape GitHub contribution stats for the profile cards."""
import json
import os
import urllib.parse
import urllib.request
from collections import Counter

USERNAME = "ggbdpq"

QUERY = """query($login: String!) { user(login: $login) {
  followers { totalCount }
  pullRequests(states: MERGED, first: 100) {
    totalCount
    nodes { repository { nameWithOwner } }
  }
  repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
    totalCount
    nodes { stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
  }
  contributionsCollection { totalCommitContributions contributionCalendar { totalContributions } }
  repositoriesContributedTo(first: 1) { totalCount }
} }"""

NON_CODE = {"CSS", "SCSS", "HTML", "PLpgSQL", "Shell", "Dockerfile", "Makefile",
            "Markdown", "Batchfile", "PowerShell", "INI", "TSQL"}
# ponytail: 自研仓与社区活动仓不算第三方上游，逐个点名；以后有新类别再加规则
EXCLUDE_REPOS = {"ggbdpq/cursor-loc", "nice-people-frontend-community/nice-21day"}


def merged_rows(repo_counts):
    """Third-party upstream repos only, display name + merged count, most first."""
    return [(name.split("/")[-1], count) for name, count in repo_counts.most_common()
            if name not in EXCLUDE_REPOS]


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


def _get_commits(token, username, repo, query):
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/commits?{query}&per_page=100",
        headers={"Authorization": f"Bearer {token}", "User-Agent": f"{username}-profile"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_patches(token, username, repos):
    """Upstream-applied patch commits per third-party repo: default-branch commits
    authored by `username` (applied by hand, outside merge flow and own PRs) plus
    commits by others crediting them via Co-authored-by. Returns {nameWithOwner: count}."""
    counts = {}
    for repo in repos:
        authored = _get_commits(token, username, repo, f"author={username}")
        all_commits = _get_commits(token, username, repo, "since=2026-10-01T00:00:00Z")
        # ponytail: 只取首页 100 条；author 提交超百条或全仓月提交超百条时补丁数会少算，出现再翻页
        has_direct = any(c["commit"]["committer"]["email"] != "noreply@github.com" for c in authored)
        credited = count_coauthored(all_commits, username)
        if not has_direct and not credited:
            continue
        numbers, shas = merged_pr_refs(token, username, repo)
        n = count_patches(authored, shas) + count_coauthored(all_commits, username, set(numbers), shas)
        if n:
            counts[repo] = n
    return counts


def fetch_data(token, username=USERNAME):
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": username}}).encode(),
        headers={"Authorization": f"Bearer {token}", "User-Agent": f"{username}-profile"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        user = json.load(response)["data"]["user"]

    sizes = Counter()
    for repo in user["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            sizes["Other" if name in NON_CODE else name] += edge["size"]
    total = sum(sizes.values()) or 1
    top = [(name, size) for name, size in sizes.most_common()
           if name != "Other" and size / total >= 0.005][:7]
    other = total - sum(size for _, size in top)
    languages = [(name, round(size / total * 100, 1)) for name, size in top]
    languages.append(("Other", round(other / total * 100, 1)))

    calendar = user["contributionsCollection"]
    repo_counts = Counter(node["repository"]["nameWithOwner"]
                          for node in user["pullRequests"]["nodes"] if node["repository"])
    patch_counts = fetch_patches(token, username,
                                 [name for name in repo_counts if name not in EXCLUDE_REPOS])
    patches_by_repo = sorted(((name.split("/")[-1], count) for name, count in patch_counts.items() if count),
                             key=lambda item: (-item[1], item[0]))
    return {
        "contributions": calendar["contributionCalendar"]["totalContributions"],
        "commits": calendar["totalCommitContributions"],
        "merged_prs": user["pullRequests"]["totalCount"],
        "merged_by_repo": merged_rows(repo_counts),
        "patches_by_repo": patches_by_repo,
        "repositories": user["repositories"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in user["repositories"]["nodes"]),
        "contributed_to": user["repositoriesContributedTo"]["totalCount"],
        "followers": user["followers"]["totalCount"],
        "languages": languages,
    }
