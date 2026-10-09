"""Fetch and shape GitHub contribution stats for the profile cards."""
import json
import os
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
    nodes { languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
  }
  contributionsCollection { totalCommitContributions contributionCalendar { totalContributions } }
} }"""

NON_CODE = {"CSS", "SCSS", "HTML", "PLpgSQL", "Shell", "Dockerfile", "Makefile",
            "Markdown", "Batchfile", "PowerShell", "INI", "TSQL"}
# ponytail: 自研仓与社区活动仓不算第三方上游，逐个点名；以后有新类别再加规则
EXCLUDE_REPOS = {"ggbdpq/cursor-loc", "nice-people-frontend-community/nice-21day"}


def merged_rows(repo_counts):
    """Third-party upstream repos only, display name + merged count, most first."""
    return [(name.split("/")[-1], count) for name, count in repo_counts.most_common()
            if name not in EXCLUDE_REPOS]


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
    return {
        "contributions": calendar["contributionCalendar"]["totalContributions"],
        "commits": calendar["totalCommitContributions"],
        "merged_prs": user["pullRequests"]["totalCount"],
        "merged_by_repo": merged_rows(repo_counts),
        "repositories": user["repositories"]["totalCount"],
        "followers": user["followers"]["totalCount"],
        "languages": languages,
    }
