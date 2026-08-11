#!/usr/bin/env python3
"""Render the SVG assets used by the profile README.

Both assets are self-contained: fonts are system stacks, colours are CSS custom
properties that flip on `prefers-color-scheme`, and every animation is disabled
under `prefers-reduced-motion`. Nothing is fetched at render time, so the
profile cannot be broken by a third party going down.
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

SANS = "ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

TOKENS = """
  :root{
    --bg:#f6f8fa; --border:#d8dee4; --grid:#e9edf1; --card:#ffffff;
    --fg:#1f2328; --muted:#59636e; --dim:#818b98;
    --accent:#1a7f37; --flow:#0969da; --line:#d8dee4;
  }
  @media (prefers-color-scheme: dark){
    :root{
      --bg:#0d1117; --border:#283039; --grid:#161c24; --card:#111820;
      --fg:#e6edf3; --muted:#9198a1; --dim:#6e7781;
      --accent:#3fb950; --flow:#58a6ff; --line:#2b3542;
    }
  }
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- hero

def hero():
    w, h = 1200, 392
    loop = 7.0
    stage_w, stage_h, stage_y = 128, 42, 286
    stages = ["commit", "build", "test", "deploy"]
    xs = [64, 244, 424, 604]

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
        f'height="{h}" role="img" aria-labelledby="t d">'
    )
    parts.append('<title id="t">Ibrahim Gul Butt — Site Reliability and DevOps</title>')
    parts.append(
        '<desc id="d">A deploy moving through commit, build, test and deploy into a '
        'healthy production cluster.</desc>'
    )

    parts.append("<style>" + TOKENS + f"""
  .name{{font:700 54px {SANS};fill:var(--fg);letter-spacing:-1.2px}}
  .role{{font:500 14px {MONO};fill:var(--accent);letter-spacing:3.2px}}
  .tag {{font:400 19px {SANS};fill:var(--muted)}}
  .sub {{font:400 15px {SANS};fill:var(--dim)}}
  .cap {{font:400 12px {MONO};fill:var(--dim);letter-spacing:1.6px}}
  .stg {{font:500 13px {MONO};fill:var(--muted);letter-spacing:.6px}}
  .box {{fill:var(--card);stroke:var(--line);stroke-width:1.5}}
  .wire{{stroke:var(--line);stroke-width:2;stroke-linecap:round}}

  .box.live{{animation:lit {loop}s linear infinite}}
  @keyframes lit{{
    0%,4%    {{stroke:var(--line);}}
    9%,19%   {{stroke:var(--accent);}}
    25%,100% {{stroke:var(--line);}}
  }}
  .lbl.live{{animation:txt {loop}s linear infinite}}
  @keyframes txt{{
    0%,4%    {{fill:var(--muted);}}
    9%,19%   {{fill:var(--accent);}}
    25%,100% {{fill:var(--muted);}}
  }}

  .packet{{animation:fly {loop}s cubic-bezier(.45,.05,.55,.95) infinite}}
  @keyframes fly{{
    0%   {{transform:translateX(0px);opacity:0}}
    4%   {{opacity:1}}
    62%  {{transform:translateX(872px);opacity:1}}
    69%  {{transform:translateX(872px);opacity:0}}
    100% {{transform:translateX(872px);opacity:0}}
  }}

  .pod {{fill:var(--accent);stroke:var(--line);stroke-width:1.5;fill-opacity:.10;
         animation:land {loop}s linear infinite}}
  @keyframes land{{
    0%,63%   {{fill-opacity:.10;stroke:var(--line)}}
    68%,88%  {{fill-opacity:.80;stroke:var(--accent)}}
    94%,100% {{fill-opacity:.10;stroke:var(--line)}}
  }}

  @media (prefers-reduced-motion: reduce){{
    .box.live,.lbl.live,.packet,.pod{{animation:none}}
    .packet{{opacity:0}}
  }}
""" + "</style>")

    parts.append('<defs><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">'
                 '<path d="M40 0H0V40" fill="none" stroke="var(--grid)" stroke-width="1"/>'
                 '</pattern>'
                 f'<clipPath id="c"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18"/></clipPath></defs>')

    parts.append(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="var(--bg)"/>')
    parts.append(f'<rect clip-path="url(#c)" x="1" y="1" width="{w-2}" height="{h-2}" fill="url(#g)"/>')
    parts.append(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="none" '
                 f'stroke="var(--border)" stroke-width="1.5"/>')

    parts.append('<text class="name" x="64" y="104">Ibrahim Gul Butt</text>')
    parts.append('<text class="role" x="66" y="140">SITE RELIABILITY  ·  DEVOPS  ·  LAHORE, PAKISTAN</text>')
    parts.append('<text class="tag" x="64" y="188">I keep production systems up — and build the '
                 'things I wish existed.</text>')
    parts.append('<text class="sub" x="64" y="216">Final year, Software Engineering @ FAST-NUCES '
                 '· graduating December 2026</text>')

    parts.append('<line class="wire" x1="64" y1="252" x2="1136" y2="252" stroke="var(--border)" '
                 'stroke-width="1"/>')

    # connectors sit behind the stage boxes
    cy = stage_y + stage_h / 2
    for i in range(len(xs)):
        x1 = xs[i] + stage_w
        x2 = xs[i + 1] if i + 1 < len(xs) else 790
        parts.append(f'<line class="wire" x1="{x1}" y1="{cy:g}" x2="{x2}" y2="{cy:g}"/>')

    for i, (x, label) in enumerate(zip(xs, stages)):
        delay = f"{i * loop * 0.17:.2f}s"
        parts.append(f'<rect class="box live" x="{x}" y="{stage_y}" width="{stage_w}" '
                     f'height="{stage_h}" rx="9" style="animation-delay:{delay}"/>')
        parts.append(f'<text class="stg lbl live" x="{x + stage_w / 2:g}" y="{cy + 4.5:g}" '
                     f'text-anchor="middle" style="animation-delay:{delay}">{esc(label)}</text>')

    # production cluster
    parts.append('<rect x="790" y="270" width="346" height="76" rx="11" fill="var(--card)" '
                 'stroke="var(--line)" stroke-width="1.5"/>')
    n = 0
    for row in (281, 313):
        for col in range(6):
            delay = f"{n * 0.05:.2f}s"
            parts.append(f'<rect class="pod" x="{812 + col * 34}" y="{row}" width="26" height="26" '
                         f'rx="7" style="animation-delay:{delay}"/>')
            n += 1
    parts.append('<text class="cap" x="1026" y="312">production</text>')

    parts.append(f'<g class="packet"><circle cx="{xs[0] + stage_w / 2:g}" cy="{cy:g}" r="5" '
                 f'fill="var(--flow)"/></g>')

    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------- stack

ROWS = [
    ("PLATFORM", ["Kubernetes", "Azure AKS", "Oracle OKE", "Helm", "NGINX Ingress"]),
    ("DELIVERY", ["Terraform", "ArgoCD", "GitOps", "GitHub Actions", "Docker"]),
    ("RELIABILITY", ["SigNoz", "PagerDuty", "on-call"]),
    ("APPLICATION", ["Python", "FastAPI", "TypeScript", "Rust", "React",
                     "React Native", "PostgreSQL", "Redis"]),
]


def stack():
    w = 1200
    pad_top, row_h, pad_bot = 34, 58, 34
    h = pad_top + row_h * len(ROWS) + pad_bot
    fs, chip_h, pad_x, gap = 13, 30, 14, 10
    rule_x, chips_x = 272, 304

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
        f'height="{h}" role="img" aria-labelledby="st">',
        '<title id="st">Stack: platform, delivery, reliability and application tooling</title>',
        "<style>" + TOKENS + f"""
  .k{{font:500 12px {MONO};fill:var(--dim);letter-spacing:2.4px}}
  .v{{font:500 13px {MONO};fill:var(--fg)}}
  .chip{{fill:var(--card);stroke:var(--line);stroke-width:1.5}}
""" + "</style>",
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="var(--bg)" '
        f'stroke="var(--border)" stroke-width="1.5"/>',
        f'<line x1="{rule_x}" y1="26" x2="{rule_x}" y2="{h-26}" stroke="var(--border)" stroke-width="1"/>',
    ]

    for i, (key, items) in enumerate(ROWS):
        cy = pad_top + row_h * i + row_h / 2
        parts.append(f'<text class="k" x="48" y="{cy + 4:g}">{esc(key)}</text>')
        x = chips_x
        for item in items:
            cw = round(len(item) * fs * 0.6) + pad_x * 2
            parts.append(f'<rect class="chip" x="{x}" y="{cy - chip_h / 2:g}" width="{cw}" '
                         f'height="{chip_h}" rx="8"/>')
            parts.append(f'<text class="v" x="{x + cw / 2:g}" y="{cy + 4.5:g}" '
                         f'text-anchor="middle">{esc(item)}</text>')
            x += cw + gap
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "hero.svg").write_text(hero(), encoding="utf-8")
    (ASSETS / "stack.svg").write_text(stack(), encoding="utf-8")
    print("wrote assets/hero.svg, assets/stack.svg")
