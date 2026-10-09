#!/usr/bin/env python3
"""Generate the OXPID-style hero banner for the profile README.

GitHub strips CSS from README HTML but serves SVG images with full
styling, so the hero's typography (letterspacing, weights, gradient)
lives here. Section titles use colored math text in the README itself.

Output: assets/hero.svg
Pure stdlib, no network. Run: python3 .github/scripts/generate_banners.py
"""
import os

# Theme (OXPID-inspired, warm off-white + ink + purple)
INK = "#2E2E38"
SUB = "#8A8A9C"
ACCENT = "#B893C7"
PERI = "#6D8FD6"
LINE = "#E6E1EC"

FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

ASSETS = "assets"


def hero() -> str:
    W, H = 900, 260
    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Aniket Kumar. Building what shouldn't exist yet.">
<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#FAF4F7"/>
<stop offset="0.5" stop-color="#F0F4FF"/>
<stop offset="1" stop-color="#F1FAF5"/>
</linearGradient>
</defs>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="url(#g)" stroke="{LINE}"/>
<text x="56" y="70" font-family="{MONO}" font-size="13" letter-spacing="4" fill="{SUB}">&#9671; ANIKET KUMAR</text>
<text x="54" y="140" font-family="{FONT}" font-weight="700" font-size="52" letter-spacing="-1.5" fill="{INK}">Building what</text>
<text x="54" y="196" font-family="{FONT}" font-weight="700" font-size="52" letter-spacing="-1.5" fill="{INK}">shouldn&#39;t exist <tspan fill="{ACCENT}">yet.</tspan></text>
<text x="56" y="236" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{SUB}">AI SYSTEMS&#160;&#160;&#183;&#160;&#160;LLM RESEARCH&#160;&#160;&#183;&#160;&#160;DEVELOPER INFRASTRUCTURE</text>
<circle cx="800" cy="90" r="4" fill="{ACCENT}"/>
<circle cx="820" cy="90" r="4" fill="{PERI}"/>
<circle cx="840" cy="90" r="4" fill="{INK}"/>
</svg>"""


def main():
    os.makedirs(ASSETS, exist_ok=True)
    path = os.path.join(ASSETS, "hero.svg")
    with open(path, "w") as f:
        f.write(hero())
    print("wrote", path)


if __name__ == "__main__":
    main()
