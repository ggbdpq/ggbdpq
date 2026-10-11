"""Check merged_rows/count_patches and the merged GitHub-stats dashboard card. Run: python3 test_github_stats.py"""
from collections import Counter

from github_stats import merged_rows, count_patches
from svg_cards import THEMES, stats

counts = Counter({"apache/maka": 33, "CherryHQ/cherry-studio": 8, "ggbdpq/cursor-loc": 3,
                  "farion1231/cc-switch": 3, "router-for-me/CLIProxyAPI": 2,
                  "nice-people-frontend-community/nice-21day": 1,
                  "stablyai/orca": 1, "multica-ai/multica": 1, "yetone/magpie": 1})
rows = merged_rows(counts)
assert rows == [("maka", 33), ("cherry-studio", 8), ("cc-switch", 3), ("CLIProxyAPI", 2),
                ("orca", 1), ("multica", 1), ("magpie", 1)], rows
assert sum(c for _, c in rows) == 49, rows


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

data = {"contributions": 969, "commits": 373, "merged_prs": 66,
        "patches_by_repo": [["magpie", 6]],
        "merged_by_repo": [("maka", 42), ("cherry-studio", 8), ("cc-switch", 7),
                            ("CLIProxyAPI", 2), ("orca", 1), ("multica", 1), ("magpie", 1)],
        "stars": 8, "contributed_to": 12, "repositories": 9, "followers": 6,
        "languages": [["TypeScript", 36.0]]}
s = stats(THEMES["light"], data)
assert "GITHUB STATS" in s and "GGBDPQ'S" not in s, s
for label in ("Total Stars Earned", "Total Contributions (last year)", "Total Commits (last year)",
              "Merged Pull Requests", "Upstream Patch Commits", "Contributed to (last year)"):
    assert label in s, label
assert "Followers" not in s, s                                 # dropped: unrelated to merged PRs / patches
assert ">8<" in s and ">969<" in s and ">373<" in s and ">66<" in s and ">12<" in s, s
assert "stroke-dasharray" in s and "rank A · 72 pts" in s, s   # 66 PRs + 6 patches -> A
assert ">maka<" in s and ">42<" in s, s                        # per-repo bars
assert 'fill-opacity="0.4"' in s, s                            # faded patch segment
assert "62 merged in 7 third-party repos" in s, s
assert "upstream patch commits" in s and "external PRs closed there" in s, s
assert "<image" not in s                                       # no photo without img arg
s_img = stats(THEMES["light"], data, img="B64PAYLOAD")
assert "data:image/png;base64,B64PAYLOAD" in s_img, s_img
s_no_patch = stats(THEMES["light"], {k: v for k, v in data.items() if k != "patches_by_repo"})
assert "Upstream Patch" not in s_no_patch and "fill-opacity" not in s_no_patch, s_no_patch
assert "rank A · 66 pts" in s_no_patch, s_no_patch
print("test_github_stats: ok")

from github_stats import count_coauthored

def _co(sha, author_email, msg):
    return {"sha": sha, "commit": {"author": {"email": author_email}, "message": msg}}

# magpie real case: maintainer lands the patch, credits ggbdpq via Co-authored-by trailer.
co = [_co("c606da5", "yetoneful@gmail.com",
          "mcpauth: signed in (#1490, ggbdpq)\n\nPatch by ggbdpq in #1490, taken as is.\n\nCo-authored-by: ggbdpq <ggbdpq@gmail.com>"),
      _co("91581fc", "yetoneful@gmail.com",
          "library: WSL agent (#1488, ggbdpq)\n\nPatch by ggbdpq in #1488; resync added on top.\n\nCo-authored-by: ggbdpq <ggbdpq@gmail.com>")]
assert count_coauthored(co, "ggbdpq", {1339}) == 2, count_coauthored(co, "ggbdpq", {1339})
# a squash of the author's own merged PR carries the PR number -> already in the PR row, not a patch
squash = [_co("deadbee", "maintainer@example.com",
              "fix: thing (#8045)\n\nCo-authored-by: ggbdpq <ggbdpq@gmail.com>")]
assert count_coauthored(squash, "ggbdpq", {8045}) == 0
# self co-author trailer on own commit, or no trailer -> not counted
assert count_coauthored([_co("a1b2c3d", "ggbdpq@gmail.com", "x\n\nCo-authored-by: ggbdpq <ggbdpq@gmail.com>")], "ggbdpq", set()) == 0
assert count_coauthored([_co("b2c3d4e", "yetoneful@gmail.com", "no trailer here")], "ggbdpq", set()) == 0
