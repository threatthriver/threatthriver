#!/usr/bin/env python3
"""Generate OXPID-style SVG banners for the profile README.

GitHub strips <style>/class from README HTML, but serves SVG images with
full styling intact. So all real typography (letterspacing, weights,
custom layout) lives here, in SVGs, and the README just references them.

Outputs:
  assets/hero.svg          - top hero banner
  assets/section-*.svg     - numbered editorial section titles

Pure stdlib, no network. Run: python3 .github/scripts/generate_banners.py
"""
import os

# ---- Theme (OXPID-inspired, warm off-white + ink + purple) ----
BG = "#FCF9FB"
INK = "#2E2E38"
SUB = "#8A8A9C"
ACCENT = "#B893C7"
PERI = "#6D8FD6"
LINE = "#E6E1EC"

FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

ASSETS = "assets"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def write(name: str, svg: str) -> None:
    os.makedirs(ASSETS, exist_ok=True)
    with open(os.path.join(ASSETS, name), "w") as f:
        f.write(svg)
    print("wrote", os.path.join(ASSETS, name))


def hero() -> str:
    W, H = 900, 260
    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Aniket Kumar — building what shouldn't exist yet">
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


def section(num: str, label: str, headline: str) -> str:
    W, H = 900, 118
    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(num)} - {esc(label)}: {esc(headline)}">
<rect width="{W}" height="{H}" fill="{BG}"/>
<text x="2" y="26" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{ACCENT}">{esc(num)}</text>
<line x1="40" y1="22" x2="78" y2="22" stroke="{LINE}" stroke-width="1.5"/>
<text x="92" y="26" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{SUB}">{esc(label)}</text>
<text x="0" y="78" font-family="{FONT}" font-weight="700" font-size="34" letter-spacing="-0.8" fill="{INK}">{esc(headline)}</text>
<line x1="2" y1="104" x2="{W-2}" y2="104" stroke="{LINE}"/>
</svg>"""


def footer() -> str:
    W, H = 900, 90
    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Build. Experiment. Ship.">
<rect width="{W}" height="{H}" fill="{BG}"/>
<line x1="2" y1="2" x2="{W-2}" y2="2" stroke="{LINE}"/>
<text x="{W/2}" y="44" text-anchor="middle" font-family="{MONO}" font-size="14" letter-spacing="6" fill="{INK}">BUILD. &#160; EXPERIMENT. &#160; SHIP.</text>
<text x="{W/2}" y="70" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{SUB}">INDEPENDENT BUILDER &#183; AI SYSTEMS &#183; RESEARCH &#183; PRODUCTS</text>
</svg>"""


def main():
    write("hero.svg", hero())
    write("section-about.svg", section("01", "ABOUT", "I build between research and real products."))
    write("section-building.svg", section("02", "BUILDING", "Two ventures. One argument: build the useful thing."))
    write("section-work.svg", section("03", "SELECTED WORK", "Experiments worth keeping around."))
    write("section-stack.svg", section("04", "STACK", "The tools, kept deliberately small."))
    write("section-github.svg", section("05", "GITHUB", "The numbers, published openly."))
    write("footer.svg", footer())


if __name__ == "__main__":
    main()
