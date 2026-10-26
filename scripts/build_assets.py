"""Generates the profile SVGs that sit around vinyl-sleeve.svg, in its palette and type.

    python scripts/build_assets.py            # writes into ./assets
"""
import math, random, sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets"

GROUND, STOCK, ORANGE, ORANGE_LT, NAVY = "#151110", "#efe4d4", "#c8552e", "#e6763f", "#1c2a4a"
MUTED, DIM, LINE, GROOVE, GROOVE_HI, INK = "#8a7a68", "#6b5d4f", "#2e2620", "#241d19", "#3a302a", "#15100d"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, Menlo, Consolas, monospace"
SERIF = "Georgia, serif"

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def grooves(cx, cy, r0, r1, scale=1.0):
    """Same groove rule as the sleeve: every 4th ring spaced wider, every 7th brighter."""
    out, r, i = [], r0, 0
    while r < r1:
        bright = i % 7 == 3
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="{GROOVE_HI if bright else GROOVE}" stroke-width="{1 if bright else 0.7}"/>')
        r += (3.1 + (1.4 if i % 4 == 0 else 0)) * scale
        i += 1
    return "".join(out)


def disc_defs(prefix):
    return f'''<radialGradient id="{prefix}-disc" cx="0.42" cy="0.36" r="0.72">
<stop offset="0" stop-color="#2a221d"/><stop offset="0.55" stop-color="#15100d"/><stop offset="1" stop-color="#0c0908"/>
</radialGradient>
<linearGradient id="{prefix}-sheen" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#ffffff" stop-opacity="0.11"/>
<stop offset="0.42" stop-color="#ffffff" stop-opacity="0"/>
<stop offset="0.62" stop-color="#ffffff" stop-opacity="0.07"/>
<stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>'''


def svg(w, h, label, title, body, style=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">
<title>{title}</title>
{f"<style>{style}</style>" if style else ""}
{body}
</svg>
'''


# ---------------------------------------------------------------- now playing
def now_playing():
    W, H = 1200, 150
    titles = ["Artificial Intelligence", "Natural Language Processing", "Creative Engineering", "Interactive Web Experiences"]
    cycle = 4 * len(titles)

    rnd = random.Random(7)
    x0, x1, cy = 600, 1128, 66
    n, step = 88, 6
    bars, peaks = [], []
    for i in range(n):
        t = i / (n - 1)
        env = 0.35 + 0.65 * math.sin(math.pi * t) ** 0.6
        v = 0.5 + 0.3 * math.sin(i * 0.37) + 0.2 * math.sin(i * 1.13 + 1.2) + rnd.uniform(-0.18, 0.18)
        h = max(4, min(46, 46 * env * max(0.12, v)))
        peaks.append(h)
    for i, h in enumerate(peaks):
        x = x0 + i * step
        dur = 2.4 + (i * 37 % 19) / 10
        delay = -((i * 53) % 31) / 10
        bars.append(f'<rect class="b" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s" x="{x:.1f}" y="{cy - h / 2:.1f}" width="2.4" height="{h:.1f}" rx="1.2"/>')
    bars = "".join(bars)

    # Titles run on the SMIL timeline so each swap lands in step with the playhead.
    def swap(i):
        s = i / len(titles)
        kt = [0, s, s + 0.035, s + 0.215, s + 0.25, 1]
        ov = ["0", "0", "1", "1", "0", "0"]
        tv = ["0 8", "0 8", "0 0", "0 0", "0 -8", "0 -8"]
        if i == 0:
            kt, ov, tv = kt[1:], ov[1:], tv[1:]
        if kt[-2] >= 1:
            kt, ov, tv = kt[:-1], ov[:-1], tv[:-1]
        timing = (f'calcMode="spline" keySplines="{";".join(["0.4 0 0.2 1"] * (len(kt) - 1))}" '
                  f'keyTimes="{";".join(f"{k:.3f}" for k in kt)}" dur="{cycle}s" repeatCount="indefinite"')
        return (f'<animate attributeName="opacity" values="{";".join(ov)}" {timing}/>'
                f'<animateTransform attributeName="transform" type="translate" values="{";".join(tv)}" {timing}/>')

    title_els = "".join(
        f'<text x="196" y="86" opacity="{1 if i == 0 else 0}" font-family="{SANS}" font-size="24" font-weight="700" fill="{STOCK}">{t}{swap(i)}</text>'
        for i, t in enumerate(titles))

    style = f"""
.dot{{animation:pulse 2.4s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
.b{{transform-box:fill-box;transform-origin:center;animation:breathe 3s ease-in-out infinite alternate}}
@keyframes breathe{{from{{transform:scaleY(1)}}to{{transform:scaleY(.62)}}}}
{REDUCED}
"""
    body = f'''<defs>
{disc_defs("np")}
<clipPath id="np-played"><rect x="{x0 - 2}" y="0" width="0" height="{H}"><animate attributeName="width" values="0;{x1 - x0 + 4}" dur="{cycle}s" repeatCount="indefinite"/></rect></clipPath>
</defs>
<rect width="{W}" height="{H}" fill="{GROUND}"/>
<line x1="72" y1="0.5" x2="1128" y2="0.5" stroke="{LINE}"/>
<g>
<animateTransform attributeName="transform" type="rotate" from="0 110 72" to="360 110 72" dur="8s" repeatCount="indefinite"/>
<circle cx="110" cy="72" r="40" fill="url(#np-disc)"/>
{grooves(110, 72, 18, 39, 0.42)}
<circle cx="110" cy="72" r="15" fill="{ORANGE}"/>
<circle cx="110" cy="72" r="15" fill="none" stroke="{ORANGE_LT}" stroke-width="0.8"/>
<circle cx="110" cy="62" r="1.6" fill="{STOCK}" opacity="0.8"/>
<circle cx="110" cy="72" r="2" fill="{GROUND}"/>
</g>
<circle cx="110" cy="72" r="40" fill="url(#np-sheen)"/>
<circle class="dot" cx="200" cy="47" r="3" fill="{ORANGE}"/>
<text x="212" y="51" font-family="{MONO}" font-size="10" fill="{MUTED}" letter-spacing="4">NOW PLAYING</text>
{title_els}
<text x="196" y="112" font-family="{MONO}" font-size="10" fill="{DIM}" letter-spacing="2.5">MINH TRIET · ON REPEAT</text>
<g fill="{GROOVE_HI}">{bars}</g>
<g fill="{ORANGE}" clip-path="url(#np-played)">{bars}</g>
<line x1="{x0}" y1="108" x2="{x1}" y2="108" stroke="{LINE}"/>
<line x1="{x0}" y1="108" x2="{x0}" y2="108" stroke="{ORANGE}" stroke-width="1.5"><animate attributeName="x2" values="{x0};{x1}" dur="{cycle}s" repeatCount="indefinite"/></line>
<circle cx="{x0}" cy="108" r="3" fill="{STOCK}"><animate attributeName="cx" values="{x0};{x1}" dur="{cycle}s" repeatCount="indefinite"/></circle>
<text x="{x0}" y="128" font-family="{MONO}" font-size="9" fill="{DIM}" letter-spacing="2.5">A1 — B3</text>
<text x="{x1}" y="128" text-anchor="end" font-family="{MONO}" font-size="9" fill="{DIM}" letter-spacing="2.5">33⅓ RPM</text>
<line x1="72" y1="{H - 0.5}" x2="1128" y2="{H - 0.5}" stroke="{LINE}"/>'''
    return svg(W, H, "Now playing: Artificial Intelligence, Natural Language Processing, Creative Engineering, Interactive Web Experiences",
               "Now Playing", body, style)


# ---------------------------------------------------------------- liner notes
def liner_notes():
    W, H = 1200, 400
    para = [
        "Computer Science at the University of Information",
        "Technology, VNU-HCM. I build where AI and language",
        "meet things people actually touch, and I care as much",
        "about how it feels to use as about what runs underneath.",
    ]
    credits = [
        ("STUDYING", "Computer Science, UIT (VNU-HCM)"),
        ("FOCUS", "AI · Natural Language Processing"),
        ("ALSO", "Creative Engineering · Interactive Web"),
        ("WRITTEN IN", "Python · TypeScript"),
        ("BASED IN", "Ho Chi Minh City"),
    ]
    p = "".join(f'<text x="72" y="{262 + i * 24}" font-family="{SANS}" font-size="15" fill="#5c5147">{l}</text>' for i, l in enumerate(para))
    c = []
    for i, (k, v) in enumerate(credits):
        y = 150 + i * 44
        c.append(f'<text x="700" y="{y}" font-family="{MONO}" font-size="9" fill="#5c5147" letter-spacing="2.5">{k}</text>'
                 f'<text x="820" y="{y}" font-family="{SANS}" font-size="15" fill="{INK}">{v}</text>'
                 f'<line x1="700" y1="{y + 18}" x2="1128" y2="{y + 18}" stroke="#d6cab6"/>')
    c = "".join(c)
    body = f'''<defs>
<filter id="ln-stock" x="0" y="0" width="100%" height="100%">
<feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" seed="31" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0.14  0 0 0 0 0.11  0 0 0 0 0.08  0 0 0 0.4 0"/>
</filter>
<clipPath id="ln-card"><rect width="{W}" height="{H}"/></clipPath>
</defs>
<rect width="{W}" height="{H}" fill="{STOCK}"/>
<g clip-path="url(#ln-card)">
<circle cx="1160" cy="-6" r="92" fill="{ORANGE}"/>
<circle cx="1060" cy="-6" r="92" fill="none" stroke="{NAVY}" stroke-width="1.4" opacity="0.7"/>
<circle cx="1060" cy="-6" r="64" fill="none" stroke="{NAVY}" stroke-width="1.4" opacity="0.55"/>
<rect x="0" y="{H - 10}" width="{W}" height="10" fill="{NAVY}"/>
</g>
<text x="72" y="74" font-family="{MONO}" font-size="10" fill="#5c5147" letter-spacing="4">LINER NOTES</text>
<line x1="72" y1="88" x2="120" y2="88" stroke="{ORANGE}" stroke-width="2"/>
<text x="72" y="156" font-family="{SERIF}" font-style="italic" font-size="40" fill="{INK}">Rigorous underneath,</text>
<text x="72" y="204" font-family="{SERIF}" font-style="italic" font-size="40" fill="{INK}">considerate on the surface.</text>
{p}
<text x="700" y="74" font-family="{MONO}" font-size="10" fill="#5c5147" letter-spacing="4">CREDITS</text>
<line x1="700" y1="88" x2="748" y2="88" stroke="{ORANGE}" stroke-width="2"/>
{c}
<rect width="{W}" height="{H}" fill="none" stroke="#c9bda9" stroke-width="1"/>
<rect width="{W}" height="{H}" filter="url(#ln-stock)" opacity="0.45"/>'''
    return svg(W, H, "Liner notes: Minh Triet studies Computer Science at UIT (VNU-HCM), working on AI, NLP, creative engineering and interactive web.",
               "Liner Notes", body)


# ---------------------------------------------------------------- track cards
TRACKS = [
    ("a1", "SIDE A · TRACK 1", "4:27", "UIT Campus Explorer", ["Interactive 3D campus", "exploration experience."], ["3D", "INTERACTIVE", "WEB"]),
    ("a2", "SIDE A · TRACK 2", "3:52", "Vietnamese Sarcasm", ["Context-aware Vietnamese sarcasm", "dataset and research."], ["NLP", "DATASET", "RESEARCH"]),
    ("a3", "SIDE A · TRACK 3", "5:16", "AI Video Retrieval", ["Multimodal video search", "and retrieval system."], ["MULTIMODAL", "SEARCH", "AI"]),
    ("b1", "SIDE B · TRACK 1", "3:09", "Packed", ["Collaborative group travel", "planning experience."], ["COLLABORATIVE", "TRAVEL", "PRODUCT"]),
    ("b2", "SIDE B · TRACK 2", "6:04", "Mental Health RAG", ["Retrieval-augmented", "conversational AI."], ["RAG", "CONVERSATIONAL AI"]),
    ("b3", "SIDE B · HIDDEN TRACK", "––:––", "Untitled", ["Still in the studio.", "Next pressing, in progress."], ["WORK IN PROGRESS"]),
]


CARD_W, CARD_H, GAP = 589, 240, 22


def track_card(slug, side, dur, title, desc, tags):
    W, H = CARD_W, CARD_H
    hidden = slug == "b3"
    cx, cy = 600, 132
    label = NAVY if hidden else ORANGE
    label_edge = "#2c3d63" if hidden else ORANGE_LT
    title_el = (f'<text x="32" y="112" font-family="{SERIF}" font-style="italic" font-size="30" fill="{STOCK}">{title}</text>' if hidden
                else f'<text x="32" y="110" font-family="{SANS}" font-size="28" font-weight="700" fill="{STOCK}" letter-spacing="-0.4">{title}</text>')
    d = "".join(f'<text x="32" y="{146 + i * 22}" font-family="{SANS}" font-size="15" fill="{MUTED}">{l}</text>' for i, l in enumerate(desc))
    pills, x = [], 32
    for t in tags:
        w = len(t) * 7.6 + 18
        pills.append(f'<rect x="{x}" y="191" width="{w:.1f}" height="22" rx="11" fill="none" stroke="{GROOVE_HI}"/>'
                     f'<text x="{x + w / 2:.1f}" y="205.5" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{MUTED}" letter-spacing="2">{t}</text>')
        x += w + 8
    body = f'''<rect width="{W}" height="{H}" fill="{GROUND}"/>
<g{' opacity="0.55"' if hidden else ''}>
<g>
<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="24s" repeatCount="indefinite"/>
<circle cx="{cx}" cy="{cy}" r="112" fill="url(#tc-disc)"/>
{grooves(cx, cy, 44, 110, 0.82)}
<circle cx="{cx}" cy="{cy}" r="40" fill="{label}"/>
<circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{label_edge}" stroke-width="1"{' stroke-dasharray="3 4"' if hidden else ''}/>
<circle cx="{cx - 26}" cy="{cy}" r="2" fill="{STOCK}" opacity="0.75"/>
<circle cx="{cx}" cy="{cy}" r="3.5" fill="{GROUND}"/>
</g>
<circle cx="{cx}" cy="{cy}" r="112" fill="url(#tc-sheen)"/>
</g>
<text x="32" y="48" font-family="{MONO}" font-size="9" fill="{MUTED}" letter-spacing="3">{side}</text>
<text x="440" y="48" text-anchor="end" font-family="{MONO}" font-size="11" fill="{DIM}">{dur}</text>
<line x1="32" y1="62" x2="440" y2="62" stroke="{LINE}"/>
<line x1="32" y1="62" x2="72" y2="62" stroke="{label if hidden else ORANGE}" stroke-width="2"/>
{title_el}
{d}
{"".join(pills)}
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{LINE}"/>'''
    return body


def tracks():
    # One file, cards as nested viewports: every outer edge lines up with the full-width images.
    W, H = CARD_W * 2 + GAP, CARD_H * 3 + GAP * 2
    cards = []
    for n, t in enumerate(TRACKS):
        x, y = (n % 2) * (CARD_W + GAP), (n // 2) * (CARD_H + GAP)
        cards.append(f'<svg x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">\n{track_card(*t)}\n</svg>')
    label = "Tracklist. " + " ".join(f"{t[3]}: {' '.join(t[4])}" for t in TRACKS)
    return svg(W, H, label, "Selected Works", f"<defs>\n{disc_defs('tc')}\n</defs>\n" + "\n".join(cards))


# ---------------------------------------------------------------- run-out groove
def runout():
    W, H = 1200, 132
    R, cy = 1800, 1800 + 22            # the top edge of a large record: the rings arc away at both sides
    rings, r, i = [], R, 0
    while r > R - 40:
        bright = i % 7 == 3
        rings.append(f'<circle cx="600" cy="{cy}" r="{r:.1f}" fill="none" stroke="{GROOVE_HI if bright else GROOVE}" stroke-width="{1 if bright else 0.7}"/>')
        r -= 3.1 + (1.4 if i % 4 == 0 else 0)
        i += 1
    lead = R - 40 - 10
    text_r = lead - 22
    arc = f"M {600 - 420} {cy - math.sqrt(text_r**2 - 420**2):.2f} A {text_r} {text_r} 0 0 1 {600 + 420} {cy - math.sqrt(text_r**2 - 420**2):.2f}"
    style = f".glint{{animation:glint 9s ease-in-out infinite}}@keyframes glint{{0%{{transform:translateX(-500px)}}60%,100%{{transform:translateX(1300px)}}}}{REDUCED}"
    body = f'''<defs>
<radialGradient id="ro-disc" cx="0.5" cy="0" r="1"><stop offset="0" stop-color="#1d1714"/><stop offset="1" stop-color="#0c0908"/></radialGradient>
<linearGradient id="ro-glint" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.07"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>
<clipPath id="ro-vinyl"><circle cx="600" cy="{cy}" r="{R}"/></clipPath>
<path id="ro-arc" d="{arc}"/>
</defs>
<rect width="{W}" height="{H}" fill="{GROUND}"/>
<circle cx="600" cy="{cy}" r="{R}" fill="url(#ro-disc)"/>
{"".join(rings)}
<circle cx="600" cy="{cy}" r="{lead}" fill="none" stroke="{GROOVE_HI}" stroke-width="0.8"/>
<text font-family="{MONO}" font-size="9" fill="{DIM}" letter-spacing="3.5"><textPath href="#ro-arc" startOffset="50%" text-anchor="middle">MT–MMXXVI–A  ·  THANKS FOR LISTENING  ·  ℗ LÊ PHẠM MINH TRIẾT</textPath></text>
<g clip-path="url(#ro-vinyl)"><rect class="glint" x="0" y="0" width="420" height="{H}" fill="url(#ro-glint)"/></g>'''
    return svg(W, H, "Run-out groove: thanks for listening", "Run-out", body, style)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "now-playing.svg").write_text(now_playing(), encoding="utf-8", newline="\n")
(OUT / "liner-notes.svg").write_text(liner_notes(), encoding="utf-8", newline="\n")
(OUT / "tracks.svg").write_text(tracks(), encoding="utf-8", newline="\n")
(OUT / "runout.svg").write_text(runout(), encoding="utf-8", newline="\n")
print("written to", OUT)
