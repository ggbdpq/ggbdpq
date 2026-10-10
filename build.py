"""Build the profile SVG assets: fetch GitHub stats (cache fallback), write themed cards."""
import base64
import json
import os
from pathlib import Path

from github_stats import USERNAME, fetch_data
from svg_cards import THEMES, hero, skills, stats

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
DATA_CACHE = ROOT / "data.json"
CHAN = ASSETS / "deepseek-chan.png"


def load_data():
    token = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        try:
            data = fetch_data(token)
            DATA_CACHE.write_text(json.dumps(data, indent=2) + "\n")
            return data
        except Exception as exc:  # keep the last good numbers if the API fails
            print(f"using cached data: {exc}")
    return json.loads(DATA_CACHE.read_text())


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
