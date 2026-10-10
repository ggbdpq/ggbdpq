"""Check merged_rows filtering and the opensource card's PR+patch composition. Run: python3 test_github_stats.py"""
from collections import Counter

from github_stats import merged_rows
from svg_cards import THEMES, opensource

counts = Counter({"apache/maka": 33, "CherryHQ/cherry-studio": 8, "ggbdpq/cursor-loc": 3,
                  "farion1231/cc-switch": 3, "router-for-me/CLIProxyAPI": 2,
                  "nice-people-frontend-community/nice-21day": 1,
                  "stablyai/orca": 1, "multica-ai/multica": 1, "yetone/magpie": 1})
rows = merged_rows(counts)
assert rows == [("maka", 33), ("cherry-studio", 8), ("cc-switch", 3), ("CLIProxyAPI", 2),
                ("orca", 1), ("multica", 1), ("magpie", 1)], rows
assert sum(c for _, c in rows) == 49, rows

svg_patch = opensource(THEMES["light"], {"merged_by_repo": rows,
                                         "patches_by_repo": [["magpie", 2]]})
assert 'fill-opacity="0.4"' in svg_patch, svg_patch          # patch segment rendered faded
assert "second segment = upstream patch commits: magpie 2" in svg_patch, svg_patch
assert ">3<" in svg_patch, svg_patch                          # magpie row shows 1 PR + 2 patches
svg_plain = opensource(THEMES["light"], {"merged_by_repo": rows})
assert "fill-opacity" not in svg_plain and "patch commits" not in svg_plain, svg_plain
print("test_github_stats: ok")

from github_stats import count_patches

def _c(sha, committer):
    return {"sha": sha, "commit": {"committer": {"email": committer}}}

# CPA real case: maintainer pushed the PR head verbatim (committer stays the author) —
# that commit is a merged PR, not a patch; yetone-style git am patches count; noreply squash doesn't.
cpa = [_c("b467a83", "ggbdpq@gmail.com"), _c("bcd13ca", "noreply@github.com")]
assert count_patches(cpa, {"b467a83"}) == 0, count_patches(cpa, {"b467a83"})
magpie = [_c("172f45a", "noreply@github.com")] + [_c(s, "yetoneful@gmail.com") for s in
          ("e9ed294", "65dcc57", "74c48ac", "55ac9ec", "d81706f", "8714abd")]
assert count_patches(magpie, {"172f45a"}) == 6, count_patches(magpie, {"172f45a"})
assert count_patches([], set()) == 0

from svg_cards import stats

data = {"contributions": 968, "commits": 372, "merged_prs": 66,
        "patches_by_repo": [["magpie", 6]], "repositories": 9, "followers": 6,
        "stars": 7, "contributed_to": 11}
s = stats(THEMES["light"], data)
assert "GITHUB STATS" in s
assert "Total Stars Earned" in s and ">7<" in s, s
assert "Total Contributions (last year)" in s and ">968<" in s, s
assert "Merged Pull Requests" in s and ">66<" in s, s
assert "Upstream Patch Commits" in s, s
assert "Contributed to (last year)" in s and ">11<" in s, s
assert "stroke-dasharray" in s and ">A<" in s, s   # rank donut: 66+6=72 -> A
s2 = stats(THEMES["light"], {k: v for k, v in data.items() if k != "patches_by_repo"})
assert "Upstream Patch" not in s2, s2
