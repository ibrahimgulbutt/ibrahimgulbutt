#!/usr/bin/env python3
"""Render assets/dashboard.svg from live GitHub data.

An observability panel for a person: contribution volume as a time series, language
mix as a bar set, and a few counters. Every number comes from the GraphQL API at
render time, and .github/workflows/refresh.yml re-runs this daily, so the panel on
the profile is never more than 24 hours stale.

    python3 tools/dashboard.py [--user LOGIN]

Token resolution: $GH_TOKEN, then $GITHUB_TOKEN, then `gh auth token`.
"""

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import ASSETS, MONO, SANS, TOKENS, esc  # noqa: E402

QUERY = """
query($login:String!){
  user(login:$login){
    contributionsCollection{
      contributionCalendar{
        totalContributions
        weeks{ contributionDays{ date contributionCount } }
      }
      totalCommitContributions
      totalRepositoriesWithContributedCommits
    }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false){
      totalCount
      nodes{ primaryLanguage{ name } }
    }
  }
}
"""

# Hues are the same domain colours the rest of the profile uses.
LANG_HUE = {
    "Python": "cyan", "TypeScript": "blue", "JavaScript": "amber", "Rust": "amber",
    "Kotlin": "violet", "Dart": "violet", "HTML": "green", "PLpgSQL": "cyan",
}


def token():
    for var in ("GH_TOKEN", "GITHUB_TOKEN"):
        if os.environ.get(var):
            return os.environ[var]
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True,
                          check=True).stdout.strip()


def fetch(login):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token()}",
                 "Content-Type": "application/json",
                 "User-Agent": "profile-dashboard"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if "errors" in body:
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]


def digest(user):
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    weekly = [sum(d["contributionCount"] for d in w["contributionDays"])
              for w in cal["weeks"]]

    streak = 0
    for d in reversed(days):
        if d["date"] > dt.date.today().isoformat():
            continue
        if d["contributionCount"] > 0:
            streak += 1
        else:
            break

    langs = {}
    for n in user["repositories"]["nodes"]:
        if n["primaryLanguage"]:
            langs[n["primaryLanguage"]["name"]] = langs.get(n["primaryLanguage"]["name"], 0) + 1

    return {
        "total": cal["totalContributions"],
        "commits": user["contributionsCollection"]["totalCommitContributions"],
        "active": user["contributionsCollection"]["totalRepositoriesWithContributedCommits"],
        "repos": user["repositories"]["totalCount"],
        "weekly": weekly,
        "months": [(i, d["contributionDays"][0]["date"])
                   for i, d in enumerate(cal["weeks"])],
        "streak": streak,
        "langs": sorted(langs.items(), key=lambda kv: -kv[1]),
        "busiest": max(weekly) if weekly else 0,
    }


def spark_path(vals, x0, y0, w, h):
    """Smoothed area path. Catmull-Rom control points keep it from looking jagged."""
    if not vals:
        return "", ""
    top = max(max(vals), 1)
    pts = [(x0 + i * w / (len(vals) - 1), y0 + h - v / top * h) for i, v in enumerate(vals)]
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        d += f" C{x1 + (x2 - x1) / 2:.1f},{y1:.1f} {x1 + (x2 - x1) / 2:.1f},{y2:.1f} {x2:.1f},{y2:.1f}"
    return d, d + f" L{pts[-1][0]:.1f},{y0 + h:.1f} L{pts[0][0]:.1f},{y0 + h:.1f} Z"


def render(s, login):
    W, H = 1200, 430
    pad = 30
    tiles = [
        ("CONTRIBUTIONS", f"{s['total']:,}", "last 365 days", "green"),
        ("COMMITS", f"{s['commits']:,}", f"across {s['active']} repos", "blue"),
        ("REPOSITORIES", str(s["repos"]), "authored, not forked", "violet"),
        ("CURRENT STREAK", f"{s['streak']}d", "consecutive days", "amber"),
    ]
    tw = (W - pad * 2 - 3 * 14) / 4
    cx, cy, cw, ch = pad, 196, W - pad * 2 - 300, 150   # chart box
    lx = cx + cw + 24                                    # language column

    line, area = spark_path(s["weekly"], cx + 24, cy + 26, cw - 48, ch - 46)

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
        f'height="{H}" role="img" aria-labelledby="dt dd">',
        f'<title id="dt">Live activity dashboard for {esc(login)}</title>',
        f'<desc id="dd">{s["total"]} contributions in the last year across '
        f'{s["active"]} repositories, refreshed daily.</desc>',
        "<style>" + TOKENS + f"""
  .h {{font:600 13px {MONO};fill:var(--dim);letter-spacing:2.4px}}
  .k {{font:500 10px {MONO};fill:var(--dim);letter-spacing:1.6px}}
  .n {{font:700 34px {SANS};fill:var(--fg);letter-spacing:-1px}}
  .s {{font:400 11px {SANS};fill:var(--muted)}}
  .ax{{font:400 9.5px {MONO};fill:var(--dim)}}
  .lb{{font:500 11px {MONO};fill:var(--fg)}}
  .lc{{font:400 10px {MONO};fill:var(--dim)}}
  .card{{fill:var(--card);stroke:var(--line);stroke-width:1.5}}
  .grid{{stroke:var(--line);stroke-width:1;stroke-dasharray:2 5;opacity:.65}}

  .line{{fill:none;stroke:var(--green);stroke-width:2.5;stroke-linecap:round;
         stroke-linejoin:round;stroke-dasharray:4000;stroke-dashoffset:4000;
         animation:draw 3.4s cubic-bezier(.4,0,.2,1) forwards}}
  @keyframes draw{{to{{stroke-dashoffset:0}}}}
  .area{{fill:url(#ag);opacity:0;animation:fade 1.6s ease-out 1.5s forwards}}
  @keyframes fade{{to{{opacity:1}}}}

  .scan{{stroke:var(--green);stroke-width:1.5;opacity:.5;
         animation:sweep 6s linear infinite}}
  @keyframes sweep{{
    0%{{transform:translateX(0);opacity:0}}
    6%{{opacity:.5}}
    94%{{opacity:.5}}
    100%{{transform:translateX({cw - 48}px);opacity:0}}
  }}

  .bar{{transform-box:fill-box;transform-origin:left;transform:scaleX(0);
        animation:grow 1.1s cubic-bezier(.2,.8,.2,1) forwards}}
  @keyframes grow{{to{{transform:scaleX(1)}}}}

  .dot{{animation:beat 2s ease-in-out infinite}}
  @keyframes beat{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}

  @media (prefers-reduced-motion: reduce){{
    .line{{stroke-dashoffset:0;animation:none}}
    .area{{opacity:1;animation:none}}
    .bar{{transform:scaleX(1);animation:none}}
    .scan,.dot{{animation:none}}
    .scan{{opacity:0}}
  }}
""" + "</style>",
        '<defs><linearGradient id="ag" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0%" stop-color="var(--green)" stop-opacity=".34"/>'
        '<stop offset="100%" stop-color="var(--green)" stop-opacity="0"/>'
        '</linearGradient></defs>',
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="var(--bg)" '
        f'stroke="var(--border)" stroke-width="1.5"/>',
        f'<text class="h" x="{pad}" y="46">ACTIVITY</text>',
        f'<circle class="dot" cx="{W-pad-96}" cy="41" r="4" fill="var(--green)"/>',
        f'<text class="k" x="{W-pad-84}" y="45">LIVE · DAILY</text>',
    ]

    for i, (key, num, sub, hue) in enumerate(tiles):
        x = pad + i * (tw + 14)
        p.append(f'<rect class="card" x="{x:.0f}" y="70" width="{tw:.0f}" height="98" rx="12"/>')
        p.append(f'<rect x="{x:.0f}" y="70" width="3" height="98" rx="1.5" fill="var(--{hue})"/>')
        p.append(f'<text class="k" x="{x+18:.0f}" y="96">{esc(key)}</text>')
        p.append(f'<text class="n" x="{x+18:.0f}" y="134">{esc(num)}</text>')
        p.append(f'<text class="s" x="{x+18:.0f}" y="154">{esc(sub)}</text>')

    p.append(f'<rect class="card" x="{cx}" y="{cy}" width="{cw:.0f}" height="{ch}" rx="12"/>')
    p.append(f'<text class="k" x="{cx+18}" y="{cy+24}">CONTRIBUTIONS PER WEEK</text>')
    p.append(f'<text class="ax" x="{cx+cw-18:.0f}" y="{cy+24}" text-anchor="end">'
             f'peak {s["busiest"]}</text>')
    for f in (0.34, 0.67, 1.0):
        gy = cy + 26 + (ch - 46) * f
        p.append(f'<line class="grid" x1="{cx+10}" y1="{gy:.0f}" x2="{cx+cw-10:.0f}" y2="{gy:.0f}"/>')
    p.append(f'<path class="area" d="{area}"/>')
    p.append(f'<path class="line" d="{line}"/>')
    p.append(f'<g class="scan"><line x1="{cx+24}" y1="{cy+26}" x2="{cx+24}" '
             f'y2="{cy+ch-20}"/></g>')

    seen, step = set(), (cw - 48) / max(len(s["months"]) - 1, 1)
    for i, date in s["months"]:
        mon = dt.date.fromisoformat(date).strftime("%b")
        if mon in seen:
            continue
        seen.add(mon)
        p.append(f'<text class="ax" x="{cx+24+i*step:.0f}" y="{cy+ch-6}" '
                 f'text-anchor="middle">{mon}</text>')

    p.append(f'<rect class="card" x="{lx:.0f}" y="{cy}" width="{W-pad-lx:.0f}" '
             f'height="{ch}" rx="12"/>')
    p.append(f'<text class="k" x="{lx+18:.0f}" y="{cy+24}">LANGUAGES BY REPO</text>')
    top = s["langs"][:5]
    peak = max((c for _, c in top), default=1)
    bw = W - pad - lx - 36 - 108
    for i, (name, count) in enumerate(top):
        by = cy + 44 + i * 20
        hue = LANG_HUE.get(name, "blue")
        p.append(f'<text class="lb" x="{lx+18:.0f}" y="{by+9}">{esc(name)}</text>')
        p.append(f'<rect class="bar" x="{lx+92:.0f}" y="{by}" width="{bw*count/peak:.0f}" '
                 f'height="11" rx="3" fill="var(--{hue})" fill-opacity=".85" '
                 f'style="animation-delay:{0.6+i*0.09:.2f}s"/>')
        p.append(f'<text class="lc" x="{W-pad-14:.0f}" y="{by+9}" text-anchor="end">'
                 f'{count}</text>')

    p.append(f'<text class="ax" x="{pad}" y="{H-14}">generated '
             f'{dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC by '
             f'tools/dashboard.py</text>')
    p.append("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="ibrahimgulbutt")
    a = ap.parse_args()
    stats = digest(fetch(a.user))
    (ASSETS / "dashboard.svg").write_text(render(stats, a.user), encoding="utf-8")
    print(f"wrote assets/dashboard.svg  "
          f"({stats['total']} contributions, {stats['streak']}d streak, "
          f"{len(stats['langs'])} languages)")
