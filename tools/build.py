#!/usr/bin/env python3
"""Render the SVG assets used by the profile README.

Everything is self-contained: system font stacks, colours as CSS custom properties
that flip on `prefers-color-scheme`, animations disabled under `prefers-reduced-motion`.
Nothing is fetched at render time, so no third party can break the profile.

    python3 tools/build.py
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

SANS = "ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

MONO_W = 0.6  # advance width per char, as a fraction of font-size

TOKENS = """
  :root{
    --bg:#f6f8fa; --border:#d8dee4; --grid:#e9edf1; --card:#ffffff; --sunk:#eef1f4;
    --fg:#1f2328; --muted:#59636e; --dim:#818b98; --line:#d8dee4;
    --green:#1a7f37; --blue:#0969da; --violet:#8250df; --amber:#9a6700; --cyan:#1b7c83;
  }
  @media (prefers-color-scheme: dark){
    :root{
      --bg:#0d1117; --border:#283039; --grid:#161c24; --card:#111820; --sunk:#0a0f16;
      --fg:#e6edf3; --muted:#9198a1; --dim:#6e7781; --line:#2b3542;
      --green:#3fb950; --blue:#58a6ff; --violet:#a371f7; --amber:#d29922; --cyan:#39c5cf;
    }
  }
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def mono_w(text, fs):
    return len(text) * fs * MONO_W


def chip(x, cy, label, fs=13, h=30, cls="chip", tcls="v"):
    """A pill with centred monospace text. Returns (svg, width)."""
    w = round(mono_w(label, fs)) + 28
    s = (f'<rect class="{cls}" x="{x}" y="{cy - h / 2:g}" width="{w}" height="{h}" rx="{h / 2:g}"/>'
         f'<text class="{tcls}" x="{x + w / 2:g}" y="{cy + fs * 0.35:g}" text-anchor="middle">'
         f'{esc(label)}</text>')
    return s, w


# --------------------------------------------------------------- hero

# The headline cycles through these. Colour is the point: each domain owns a hue,
# and the same hues are reused in the device cluster and the stack strip.
WORDS = [
    ("mobile apps", "violet"),
    ("web apps", "blue"),
    ("desktop apps", "amber"),
    ("Linux internals", "green"),
    ("cloud platforms", "cyan"),
    ("ML pipelines", "violet"),
]

PLATFORMS = ["Android", "iOS", "Linux", "Web", "Kubernetes"]


def hero():
    W, H = 1200, 380
    rot = len(WORDS) * 2.3          # full headline cycle
    slot = 100.0 / len(WORDS)       # % of the cycle per word
    fs_w = 36                       # headline size

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-labelledby="ht hd">',
        '<title id="ht">Ibrahim Gul Butt — I build mobile apps, web apps, desktop apps, '
        'Linux internals, cloud platforms and ML pipelines</title>',
        '<desc id="hd">A rotating headline beside a phone, a browser window and a terminal, '
        'each running.</desc>',
        "<style>" + TOKENS + f"""
  .nm  {{font:700 50px {SANS};fill:var(--fg);letter-spacing:-1.4px}}
  .eye {{font:500 12px {MONO};fill:var(--dim);letter-spacing:3.4px}}
  .wd  {{font:700 {fs_w}px {MONO};letter-spacing:-.5px}}
  .sub {{font:400 16px {SANS};fill:var(--muted)}}
  .sub2{{font:400 14px {SANS};fill:var(--dim)}}
  .v   {{font:500 12px {MONO};fill:var(--muted)}}
  .chip{{fill:var(--card);stroke:var(--line);stroke-width:1.5}}
  .frm {{fill:var(--card);stroke:var(--line);stroke-width:1.5}}
  .snk {{fill:var(--sunk)}}
  .tt  {{font:400 9px {MONO}}}
  .lbl {{font:500 8.5px {MONO};fill:var(--dim);letter-spacing:1.2px}}

  .rw{{opacity:0;animation:rot {rot}s ease-in-out infinite}}
  @keyframes rot{{
    0%           {{opacity:0;transform:translateY(9px)}}
    2%,{slot - 3:.1f}%  {{opacity:1;transform:translateY(0)}}
    {slot:.1f}%,100%    {{opacity:0;transform:translateY(-9px)}}
  }}
  .car{{animation:blink 1.06s steps(1) infinite}}
  @keyframes blink{{0%,50%{{opacity:1}}50.01%,100%{{opacity:0}}}}

  .row{{opacity:0;animation:slide 6s ease-out infinite}}
  @keyframes slide{{
    0%,6%    {{opacity:0;transform:translateX(14px)}}
    14%,86%  {{opacity:1;transform:translateX(0)}}
    94%,100% {{opacity:0;transform:translateX(0)}}
  }}
  .bar{{transform-box:fill-box;transform-origin:bottom;animation:grow 6s ease-out infinite}}
  @keyframes grow{{
    0%,8%    {{transform:scaleY(.06)}}
    26%,84%  {{transform:scaleY(1)}}
    96%,100% {{transform:scaleY(.06)}}
  }}
  .tl{{opacity:0;animation:tline 6s steps(1) infinite}}
  @keyframes tline{{0%,8%{{opacity:0}}12%,92%{{opacity:1}}96%,100%{{opacity:0}}}}
  .nav{{animation:hop 6s steps(1) infinite}}
  @keyframes hop{{0%,33%{{fill:var(--violet)}}33.01%,100%{{fill:var(--line)}}}}

  @media (prefers-reduced-motion: reduce){{
    .rw,.car,.row,.bar,.tl,.nav{{animation:none}}
    .rw:first-of-type{{opacity:1}}
    .row,.tl{{opacity:1}}
  }}
""" + "</style>",
        '<defs>'
        '<pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">'
        '<path d="M40 0H0V40" fill="none" stroke="var(--grid)" stroke-width="1"/></pattern>'
        f'<clipPath id="c"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18"/></clipPath>'
        '<radialGradient id="glow" cx="50%" cy="50%" r="50%">'
        '<stop offset="0%" stop-color="var(--blue)" stop-opacity="0.13"/>'
        '<stop offset="100%" stop-color="var(--blue)" stop-opacity="0"/></radialGradient>'
        '</defs>',
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="var(--bg)"/>',
        f'<rect clip-path="url(#c)" x="1" y="1" width="{W-2}" height="{H-2}" fill="url(#g)"/>',
        '<ellipse cx="930" cy="190" rx="330" ry="230" fill="url(#glow)"/>',
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="none" '
        f'stroke="var(--border)" stroke-width="1.5"/>',

        '<text class="nm" x="64" y="92">Ibrahim Gul Butt</text>',
        '<text class="eye" x="66" y="136">I BUILD</text>',
    ]

    # rotating headline, each word carrying its own caret
    for i, (word, hue) in enumerate(WORDS):
        d = f"{i * rot / len(WORDS):.2f}s"
        cx = 64 + mono_w(word, fs_w) + 8
        p.append(f'<g class="rw" style="animation-delay:{d}">'
                 f'<text class="wd" x="64" y="182" fill="var(--{hue})">{esc(word)}</text>'
                 f'<rect class="car" x="{cx:g}" y="155" width="13" height="34" rx="2" '
                 f'fill="var(--{hue})"/></g>')

    p += [
        '<text class="sub" x="64" y="228">Site reliability by day. Mobile, web and systems '
        'the rest of the time.</text>',
        '<text class="sub2" x="64" y="253">Lahore, Pakistan · Final year Software Engineering '
        '@ FAST-NUCES · graduating December 2026</text>',
    ]

    x = 64
    for label in PLATFORMS:
        s, w = chip(x, 300, label, fs=12, h=28)
        p.append(s)
        x += w + 8

    p += _phone(700, 44, 132, 292) + _browser(856, 44, 280, 150) + _terminal(856, 214, 280, 122)
    p.append("</svg>")
    return "\n".join(p)


def _phone(x, y, w, h):
    p = [f'<rect class="frm" x="{x}" y="{y}" width="{w}" height="{h}" rx="20"/>',
         f'<rect class="snk" x="{x + w / 2 - 17:g}" y="{y + 8}" width="34" height="6" rx="3"/>',
         f'<text class="lbl" x="{x + 14}" y="{y + 40}">NODE MIND</text>',
         f'<rect class="snk" x="{x + 14}" y="{y + 50}" width="{w - 28}" height="1"/>']
    for i in range(5):
        ry = y + 66 + i * 30
        p.append(f'<g class="row" style="animation-delay:{i * 0.28:.2f}s">'
                 f'<rect x="{x + 14}" y="{ry}" width="{w - 28}" height="22" rx="6" '
                 f'fill="var(--sunk)"/>'
                 f'<rect x="{x + 20}" y="{ry + 6}" width="10" height="10" rx="3" '
                 f'fill="var(--violet)" fill-opacity="{0.9 if i < 2 else 0.25:g}"/>'
                 f'<rect x="{x + 36}" y="{ry + 9}" width="{(w - 62) - i * 9}" height="4" rx="2" '
                 f'fill="var(--dim)" fill-opacity=".55"/></g>')
    for i in range(3):
        p.append(f'<circle class="{"nav" if i == 0 else ""}" cx="{x + 34 + i * 32}" '
                 f'cy="{y + h - 22}" r="4.5" fill="var(--line)"/>')
    return p


def _browser(x, y, w, h):
    p = [f'<rect class="frm" x="{x}" y="{y}" width="{w}" height="{h}" rx="11"/>',
         f'<line x1="{x}" y1="{y + 30}" x2="{x + w}" y2="{y + 30}" stroke="var(--line)"/>']
    for i, hue in enumerate(("--dim", "--dim", "--dim")):
        p.append(f'<circle cx="{x + 16 + i * 13}" cy="{y + 15}" r="3.5" fill="var({hue})" '
                 f'fill-opacity=".5"/>')
    p.append(f'<rect x="{x + 62}" y="{y + 9}" width="{w - 78}" height="13" rx="6.5" '
             f'fill="var(--sunk)"/>')
    p.append(f'<text class="lbl" x="{x + 16}" y="{y + 50}">DASHBOARD</text>')
    base = y + h - 18
    for i, hgt in enumerate((26, 44, 34, 58, 40, 66)):
        p.append(f'<rect class="bar" style="animation-delay:{i * 0.09:.2f}s" '
                 f'x="{x + 16 + i * 24}" y="{base - hgt}" width="14" height="{hgt}" rx="3" '
                 f'fill="var(--blue)" fill-opacity="{0.35 + i * 0.11:.2f}"/>')
    for i in range(3):
        p.append(f'<rect x="{x + 176}" y="{y + 62 + i * 14}" width="{88 - i * 22}" height="5" '
                 f'rx="2.5" fill="var(--dim)" fill-opacity=".4"/>')
    return p


def _terminal(x, y, w, h):
    lines = [
        ("$ kubectl rollout status deploy/api", "var(--fg)"),
        ('deployment "api" successfully rolled out', "var(--green)"),
    ]
    p = [f'<rect class="frm" x="{x}" y="{y}" width="{w}" height="{h}" rx="11"/>',
         f'<line x1="{x}" y1="{y + 28}" x2="{x + w}" y2="{y + 28}" stroke="var(--line)"/>',
         f'<text class="lbl" x="{x + 16}" y="{y + 18}">bash</text>']
    for i, (txt, fill) in enumerate(lines):
        p.append(f'<text class="tt tl" style="animation-delay:{i * 0.75:.2f}s" x="{x + 16}" '
                 f'y="{y + 52 + i * 18}" fill="{fill}">{esc(txt)}</text>')
    ly = y + 52 + len(lines) * 18
    p.append(f'<text class="tt tl" style="animation-delay:1.5s" x="{x + 16}" y="{ly}" '
             f'fill="var(--fg)">$</text>')
    p.append(f'<rect class="car" x="{x + 26}" y="{ly - 8}" width="6" height="10" '
             f'fill="var(--green)"/>')
    return p


# --------------------------------------------------------------- stack

ROWS = [
    ("MOBILE", "violet", ["React Native", "Flutter", "Ionic", "Capacitor", "Kotlin", "Android"]),
    ("WEB", "blue", ["React", "TypeScript", "Vite", "Tailwind", "Electron"]),
    ("BACKEND", "cyan", ["Python", "FastAPI", "Flask", "Node.js", "PostgreSQL", "Redis", "Supabase"]),
    ("PLATFORM", "green", ["Kubernetes", "Azure AKS", "Oracle OKE", "Terraform", "ArgoCD", "Helm", "Docker"]),
    ("RELIABILITY", "green", ["GitHub Actions", "Jenkins", "NGINX Ingress", "SigNoz", "PagerDuty"]),
    ("SYSTEMS & ML", "amber", ["Rust", "PyTorch", "YOLO", "OpenCV", "Streamlit"]),
]


def stack():
    W = 1200
    pad, row_h = 30, 56
    H = pad * 2 + row_h * len(ROWS)
    rule_x, chips_x = 250, 282

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-labelledby="st">',
        '<title id="st">Stack, by domain: mobile, web, backend, platform, reliability, '
        'systems and ML</title>',
        "<style>" + TOKENS + f"""
  .k{{font:600 12px {MONO};letter-spacing:2.2px}}
  .v{{font:500 13px {MONO};fill:var(--fg)}}
  .chip{{fill:var(--card);stroke:var(--line);stroke-width:1.5}}
""" + "</style>",
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="var(--bg)" '
        f'stroke="var(--border)" stroke-width="1.5"/>',
        f'<line x1="{rule_x}" y1="24" x2="{rule_x}" y2="{H-24}" stroke="var(--border)"/>',
    ]
    for i, (key, hue, items) in enumerate(ROWS):
        cy = pad + row_h * i + row_h / 2
        p.append(f'<rect x="44" y="{cy - 7:g}" width="3" height="14" rx="1.5" fill="var(--{hue})"/>')
        p.append(f'<text class="k" x="60" y="{cy + 4:g}" fill="var(--{hue})">{esc(key)}</text>')
        x = chips_x
        for item in items:
            s, w = chip(x, cy, item)
            p.append(s)
            x += w + 9
    p.append("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "hero.svg").write_text(hero(), encoding="utf-8")
    (ASSETS / "stack.svg").write_text(stack(), encoding="utf-8")
    print(f"wrote {ASSETS/'hero.svg'}\nwrote {ASSETS/'stack.svg'}")
