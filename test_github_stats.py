"""Check merged_rows keeps third-party upstream repos only, sorted by count. Run: python3 test_github_stats.py"""
from collections import Counter

from github_stats import merged_rows

counts = Counter({"apache/maka": 33, "CherryHQ/cherry-studio": 8, "ggbdpq/cursor-loc": 3,
                  "farion1231/cc-switch": 3, "router-for-me/CLIProxyAPI": 2,
                  "nice-people-frontend-community/nice-21day": 1,
                  "stablyai/orca": 1, "multica-ai/multica": 1, "yetone/magpie": 1})
rows = merged_rows(counts)
assert rows == [("maka", 33), ("cherry-studio", 8), ("cc-switch", 3), ("CLIProxyAPI", 2),
                ("orca", 1), ("multica", 1), ("magpie", 1)], rows
assert sum(c for _, c in rows) == 49, rows
print("test_github_stats: ok")
