"""Build the profile SVG assets: fetch GitHub stats (cache fallback), write themed cards."""
import base64
import json
import os
import subprocess
from pathlib import Path

from github_stats import USERNAME, fetch_data
from svg_cards import THEMES, hero, skills, stats

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets"
DATA_CACHE = Path(__file__).parent / "data.json"
CHAN = ASSETS / "deepseek-chan.png"


def carry_over_patches(fresh, prev):
    """patch 仓的 stats 撞上 202 重算窗口时,fallback 手工计数对 squash 流仓库会算 0,
    该仓整行掉卡。补丁数只增不减,用上一次提交里的值垫底;本轮成功取到的新值照常覆盖。"""
    fresh_map = dict(fresh.get("patches_by_repo", []))
    for name, count in (prev or {}).get("patches_by_repo", []):
        fresh_map.setdefault(name, count)
    fresh["patches_by_repo"] = sorted(fresh_map.items(), key=lambda kv: (-kv[1], kv[0]))
    return fresh


def load_data():
    token = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN")
    data = None
    if token:
        try:
            data = fetch_data(token)
        except Exception as exc:  # keep the last good numbers if the API fails
            print(f"using cached data: {exc}")
    if data is None:
        data = json.loads(DATA_CACHE.read_text())
    try:
        prev = json.loads(subprocess.run(
            ["git", "show", "HEAD:scripts/data.json"],
            capture_output=True, text=True, check=True).stdout)
        data = carry_over_patches(data, prev)
    except Exception:
        pass  # ponytail: 垫底拿不到(如 CI 首跑)就按原样出卡
    DATA_CACHE.write_text(json.dumps(data, indent=2) + "\n")
    return data


def main():
    data = load_data()
    img = base64.b64encode(CHAN.read_bytes()).decode() if CHAN.exists() else None
    ASSETS.mkdir(exist_ok=True)
    for stale in [*ASSETS.glob("hero-*.svg"), *ASSETS.glob("skills-*.svg"), *ASSETS.glob("stats-*.svg")]:
        stale.unlink()
    for mode, t in THEMES.items():
        (ASSETS / f"hero-{mode}.svg").write_text(hero(t))
        (ASSETS / f"skills-{mode}.svg").write_text(skills(t, data))
        (ASSETS / f"stats-{mode}.svg").write_text(stats(t, data, img))


if __name__ == "__main__":
    main()
