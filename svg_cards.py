"""Render the profile SVG cards (hero / skills / opensource) in light and dark themes."""
from html import escape

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(bg="#0d1117", card="#11161f", border="#222b38", text="#e6edf3",
                 muted="#8b97a8", faint="#4b5566", accent="#7dd3fc", accent2="#c4b5fd",
                 chip="#161d29"),
    "light": dict(bg="#ffffff", card="#f8fafc", border="#e2e8f0", text="#0f172a",
                  muted="#64748b", faint="#cbd5e1", accent="#0369a1", accent2="#6d28d9",
                  chip="#f1f5f9"),
}

LANG_COLORS = {"TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Java": "#b07219", "Vue": "#41b883",
               "Go": "#00add8", "Rust": "#dea584", "Python": "#3572a5", "Kotlin": "#a97bff",
               "C#": "#178600", "C": "#555555", "Other": "#8b97a8"}
REPO_COLORS = ["#3b82f6", "#f59e0b", "#10b981", "#8b5cf6", "#ef4444", "#06b6d4", "#ec4899"]

DIRECTIONS = [
    ("Multi-platform Frontend", ["React 19", "Vue 3", "Taro", "Mini-program / H5", "Electron"]),
    ("AI Applications", ["Node.js", "HTTP / SSE", "structured UI", "contract tests"]),
    ("Agent Tooling", ["LLM gateways", "coding agents", "agent skills"]),
    ("Engineering", ["TypeScript", "Go", "Python", "pnpm", "Oxlint / Oxfmt"]),
]
CHIPS = ["Python", "TypeScript", "Node.js", "Go", "Rust"]


def svg(width, height, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label)}">\n{body}\n</svg>\n')


def chips(x, y, labels, t, size=11):
    out, cx = [], x
    for label in labels:
        w = len(label) * size * 0.62 + 18
        out.append(f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="22" rx="11" fill="{t["chip"]}" stroke="{t["border"]}"/>'
                   f'<text x="{cx + w / 2:.1f}" y="{y + 15}" text-anchor="middle" font-family="{MONO}" font-size="{size}" fill="{t["muted"]}">{escape(label)}</text>')
        cx += w + 8
    return "".join(out)


def hero(t):
    w, h = 880, 280
    lines = [
        ("$", "whoami", t["text"]),
        ("", "frontend engineer", t["muted"]),
        ("$", "cat now.txt", t["text"]),
        ("", "ai developer tooling:", t["muted"]),
        ("", "agents, llm gateways, skills", t["muted"]),
        ("$", "status", t["text"]),
    ]
    term = []
    y = 98
    for prompt, text, color in lines:
        if prompt:
            term.append(f'<text x="534" y="{y}" font-family="{MONO}" font-size="13" fill="{t["accent"]}">$</text>')
            term.append(f'<text x="550" y="{y}" font-family="{MONO}" font-size="13" fill="{color}">{escape(text)}</text>')
        else:
            term.append(f'<text x="550" y="{y}" font-family="{MONO}" font-size="13" fill="{color}">{escape(text)}</text>')
        y += 20
    term.append(f'<text x="550" y="{y}" font-family="{MONO}" font-size="13" fill="{t["muted"]}">mostly debugging</text>'
                f'<rect x="680" y="{y - 11}" width="8" height="14" fill="{t["accent"]}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    body = f'''<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["accent"]}"/><stop offset="1" stop-color="{t["accent2"]}"/></linearGradient>
<pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t["border"]}"/></pattern>
</defs>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="{t["bg"]}" stroke="{t["border"]}"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="url(#dots)" opacity="0.6"/>
<text x="44" y="70" font-family="{MONO}" font-size="13" fill="{t["muted"]}">hi there, I'm</text>
<text x="42" y="122" font-family="{FONT}" font-size="50" font-weight="700" letter-spacing="-1.5" fill="{t["text"]}">ggbdpq</text>
<rect x="44" y="140" width="64" height="3" rx="1.5" fill="url(#g)"/>
<text x="44" y="178" font-family="{FONT}" font-size="18" font-weight="600" fill="{t["text"]}">Frontend Engineer <tspan fill="url(#g)">→ AI Developer Tooling</tspan></text>
<text x="44" y="206" font-family="{FONT}" font-size="14" fill="{t["muted"]}">Multi-platform frontends by day, agent tools by night.</text>
{chips(44, 228, CHIPS, t)}
<rect x="510" y="44" width="330" height="192" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>
<circle cx="530" cy="64" r="4.5" fill="#ff5f57"/><circle cx="545" cy="64" r="4.5" fill="#febc2e"/><circle cx="560" cy="64" r="4.5" fill="#28c840"/>
<text x="824" y="68" text-anchor="end" font-family="{MONO}" font-size="11" fill="{t["faint"]}">~/ggbdpq</text>
{"".join(term)}'''
    return svg(w, h, body, "ggbdpq, Frontend Engineer building AI developer tools")


def skills(t, data):
    w, h = 880, 280
    parts = [f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{t["card"]}" stroke="{t["border"]}"/>',
             f'<text x="32" y="44" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{t["accent"]}">WHAT I WORK ON</text>']
    for i, (title, items) in enumerate(DIRECTIONS):
        x, y = 32 + (i % 2) * 420, 78 + (i // 2) * 62
        parts.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="15" font-weight="700" fill="{t["text"]}">{escape(title)}</text>')
        parts.append(f'<text x="{x}" y="{y + 22}" font-family="{FONT}" font-size="13" fill="{t["muted"]}">{escape(" · ".join(items))}</text>')

    parts.append(f'<line x1="32" y1="180" x2="{w - 32}" y2="180" stroke="{t["border"]}"/>')
    parts.append(f'<text x="32" y="208" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{t["accent"]}">LANGUAGES</text>')
    parts.append(f'<text x="{w - 32}" y="208" text-anchor="end" font-family="{FONT}" font-size="11" fill="{t["faint"]}">by code size across my public repositories</text>')
    x, bar_w = 32, w - 64
    parts.append(f'<clipPath id="bar"><rect x="32" y="222" width="{bar_w}" height="8" rx="4"/></clipPath><g clip-path="url(#bar)">')
    for name, pct in data["languages"]:
        seg = bar_w * pct / 100
        parts.append(f'<rect x="{x:.1f}" y="222" width="{seg + 0.5:.1f}" height="8" fill="{LANG_COLORS.get(name, LANG_COLORS["Other"])}"/>')
        x += seg
    parts.append("</g>")
    x = 32
    for name, pct in data["languages"]:
        color = LANG_COLORS.get(name, LANG_COLORS["Other"])
        text = f"{name} {pct:g}%"
        parts.append(f'<circle cx="{x + 4}" cy="253" r="4" fill="{color}"/>'
                     f'<text x="{x + 13}" y="257" font-family="{FONT}" font-size="12" fill="{t["muted"]}">{escape(text)}</text>')
        x += len(text) * 6.6 + 30
    label = "Multi-platform Frontend, AI Applications, Agent Tooling, Engineering. Languages: " + ", ".join(f"{n} {p}%" for n, p in data["languages"])
    return svg(w, h, "\n".join(parts), label)


def opensource(t, data):
    rows = data["merged_by_repo"]
    total = sum(count for _, count in rows)
    w, row_h, bar_x, bar_max = 880, 26, 150, 660
    h = 66 + row_h * (len(rows) - 1) + 8 + 16
    parts = [f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{t["card"]}" stroke="{t["border"]}"/>',
             f'<text x="32" y="40" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{t["accent"]}">MERGED PULL REQUESTS</text>',
             f'<text x="{w - 32}" y="40" text-anchor="end" font-family="{FONT}" font-size="11" fill="{t["faint"]}">{total} merged in {len(rows)} third-party repos</text>']
    peak = max(count for _, count in rows)
    for i, (name, count) in enumerate(rows):
        y = 66 + i * row_h
        color = REPO_COLORS[i % len(REPO_COLORS)]
        bar_w = max(bar_max * count / peak, 4)
        parts.append(f'<text x="32" y="{y + 8}" font-family="{FONT}" font-size="12" font-weight="600" fill="{t["text"]}">{escape(name)}</text>')
        parts.append(f'<rect x="{bar_x}" y="{y}" width="{bar_w:.1f}" height="8" rx="4" fill="{color}"/>')
        parts.append(f'<text x="{bar_x + bar_w + 8:.1f}" y="{y + 8}" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{count}</text>')
    label = "Merged pull requests in third-party repos: " + ", ".join(f"{n} {c}" for n, c in rows)
    return svg(w, h, "\n".join(parts), label)
