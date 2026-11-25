#!/usr/bin/env python3
"""Hello card: an ID card that flips forever, a now-playing player, 'currently' list and rotating hello."""
import json, pathlib, random
from xml.sax.saxutils import escape as esc
ROOT = pathlib.Path(__file__).resolve().parent.parent
np_ = json.loads((ROOT / "data" / "now_playing.json").read_text())
F = "font-family:'Noto Sans Devanagari',Inter,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
HAND = "font-family:'Segoe Print','Bradley Hand','Comic Sans MS','Marker Felt',cursive"
AMB, TEAL, FG, DIM, BG, PANEL, LINE = "#f39c12", "#2dd4bf", "#e6edf3", "#8b949e", "#0d1117", "#161b22", "#30363d"
W, H = 840, 500
def t(x, y, s, size=14, fill=FG, w=400, anchor="start", extra="", style=F):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}" style="{style}" {extra}>{esc(str(s))}</text>'
rnd = random.Random(9)
def barcode(x, y, w, h, col):
    s = ""; bx = x
    while bx < x + w:
        bw = rnd.choice([1.5, 2, 3, 4]); s += f'<rect x="{bx:.1f}" y="{y}" width="{bw}" height="{h}" fill="{col}"/>'; bx += bw + rnd.choice([1.5, 2, 3])
    return s
CX = 215
css = """
@keyframes sw{0%,100%{transform:rotate(-3.5deg)}50%{transform:rotate(3.5deg)}}.sw{transform-origin:215px 0px;animation:sw 4.5s ease-in-out infinite}
@keyframes ff{0%,40%{transform:scaleX(1)}46%,96%{transform:scaleX(0)}100%{transform:scaleX(1)}}.ff{transform-origin:215px 290px;animation:ff 9s ease-in-out infinite}
@keyframes fb{0%,46%{transform:scaleX(0)}54%,90%{transform:scaleX(1)}96%,100%{transform:scaleX(0)}}.fb{transform-origin:215px 290px;animation:fb 9s ease-in-out infinite}
@keyframes eq{0%,100%{transform:scaleY(.25)}50%{transform:scaleY(1)}}.eq{transform-box:fill-box;transform-origin:bottom;animation:eq 1s ease-in-out infinite}
@keyframes vn{to{transform:rotate(360deg)}}.vn{transform-box:fill-box;transform-origin:center;animation:vn 4s linear infinite}
@keyframes pg{from{transform:scaleX(0)}to{transform:scaleX(1)}}.pg{transform-box:fill-box;transform-origin:left;animation:pg 28s linear infinite}
@keyframes hl{0%{opacity:0;transform:translateY(8px)}4%,18%{opacity:1;transform:none}22%,100%{opacity:0}}.hl{animation:hl 12s ease-in-out infinite}
@keyframes bk{0%,60%{opacity:1}61%,100%{opacity:.3}}.bk{animation:bk 1.2s steps(1) infinite}
"""
# ---------- ID card faces (card x 80..350, y 100..480)
cx0, cy0, cw, ch = 80, 100, 270, 380
front = f'''<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="20" fill="#fffaf0"/>
<path d="M{cx0} {cy0+20}a20 20 0 0 1 20-20H{cx0+cw-20}a20 20 0 0 1 20 20V{cy0+86}H{cx0}Z" fill="url(#hd)"/>
<rect x="{CX-24}" y="{cy0+14}" width="48" height="9" rx="4.5" fill="#fffaf0" opacity=".9"/>
{t(CX, cy0+58, "DEVELOPER ID", 15, "#1b1200", 800, "middle", 'letter-spacing="3"')}
{t(CX, cy0+150, "ADITYA", 36, "#1c2733", 800, "middle", 'letter-spacing="2"')}
{t(CX, cy0+186, "SACHAN", 36, "#1c2733", 800, "middle", 'letter-spacing="2"')}
{t(CX, cy0+214, "Full-stack developer & AI builder", 12.5, "#6b7280", 600, "middle")}
<line x1="{cx0+24}" y1="{cy0+232}" x2="{cx0+cw-24}" y2="{cy0+232}" stroke="#e5d9bd" stroke-dasharray="4 4"/>
{t(cx0+26, cy0+256, "ID NO.", 9.5, "#9a8f78", 700, extra='letter-spacing="1"')}{t(cx0+26, cy0+273, "ADI-0024", 14, "#1c2733", 700)}
{t(cx0+150, cy0+256, "COUNTRY", 9.5, "#9a8f78", 700, extra='letter-spacing="1"')}{t(cx0+150, cy0+273, "India", 14, "#1c2733", 700)}
{t(cx0+26, cy0+298, "STATE", 9.5, "#9a8f78", 700, extra='letter-spacing="1"')}{t(cx0+26, cy0+315, "उत्तर प्रदेश", 14, "#1c2733", 700)}
{t(cx0+150, cy0+298, "STACK", 9.5, "#9a8f78", 700, extra='letter-spacing="1"')}{t(cx0+150, cy0+315, "Java | Spring | AI", 12.5, "#1c2733", 700)}
{barcode(cx0+26, cy0+330, 96, 30, "#1c2733")}{t(cx0+cw-26, cy0+353, "VALID: ALWAYS", 9.5, "#9a8f78", 700, "end")}'''
back = f'''<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="20" fill="#fffaf0"/>
<path d="M{cx0} {cy0+20}a20 20 0 0 1 20-20H{cx0+cw-20}a20 20 0 0 1 20 20V{cy0+120}H{cx0}Z" fill="#e63946"/>
<rect x="{CX-24}" y="{cy0+14}" width="48" height="9" rx="4.5" fill="#fffaf0" opacity=".9"/>
{t(CX, cy0+80, "HELLO", 44, "#fff", 900, "middle", 'letter-spacing="4"')}{t(CX, cy0+106, "my name is", 15, "#ffd6d9", 600, "middle")}
<rect x="{cx0+20}" y="{cy0+136}" width="{cw-40}" height="74" rx="8" fill="#fff" stroke="#e63946" stroke-width="2"/>
{t(CX, cy0+183, "Aditya", 34, "#1c2733", 600, "middle", style=HAND)}
{t(CX, cy0+240, "Say hi:", 11, "#9a8f78", 700, "middle", 'letter-spacing="2"')}
{t(CX, cy0+262, "sachanaditya207@gmail.com", 12.5, "#1c2733", 700, "middle")}
{t(CX, cy0+282, "linkedin.com/in/aditya0024", 12.5, "#1c2733", 600, "middle")}
{t(CX, cy0+302, "medium.com/@sachanaditya", 12.5, "#1c2733", 600, "middle")}
{barcode(cx0+60, cy0+322, 150, 28, "#1c2733")}{t(CX, cy0+366, "Always open to a chat", 10.5, "#9a8f78", 600, "middle")}'''
strap = f'''<path d="M{CX-30} -4 L{CX-9} 82 L{CX+9} 82 L{CX+30} -4Z" fill="url(#st)"/>
<rect x="{CX-12}" y="78" width="24" height="26" rx="5" fill="#9aa4b2"/><rect x="{CX-6}" y="86" width="12" height="9" rx="3" fill="#0d1117"/>'''
card = f'<g class="sw">{strap}<g class="ff">{front}</g><g class="fb">{back}</g></g>'

# ---------- right column
rx, rw = 410, 410
def panel(y, h): return f'<rect x="{rx}" y="{y}" width="{rw}" height="{h}" rx="16" fill="{PANEL}" stroke="{LINE}"/>'
eqb = "".join(f'<rect class="eq" style="animation-delay:{i*0.17:.2f}s;animation-duration:{0.7+ (i%3)*0.2:.1f}s" x="{rx+rw-92+i*13}" y="{58}" width="8" height="28" rx="2" fill="{TEAL}"/>' for i in range(5))
grooves = "".join(f'<circle cx="0" cy="0" r="{r}" fill="none" stroke="#2a3140" stroke-width="1"/>' for r in (14, 20, 26))
now = f'''{panel(36, 140)}{t(rx+24, 64, "NOW PLAYING", 11, TEAL, 700, extra='letter-spacing="2"')}{eqb}
<g transform="translate({rx+66},118)"><g class="vn"><circle r="40" fill="#0b0f16" stroke="#2a3140"/>{grooves}<circle r="12" fill="url(#av)"/><circle r="3" fill="#0b0f16"/><line x1="0" y1="-40" x2="0" y2="-30" stroke="#4b5563"/></g></g>
{t(rx+128, 108, np_["title"], 18, FG, 700)}{t(rx+128, 130, np_["artist"], 13, DIM, 500)}
<rect x="{rx+128}" y="148" width="{rw-152}" height="5" rx="2.5" fill="#262d3a"/><rect class="pg" x="{rx+128}" y="148" width="{rw-152}" height="5" rx="2.5" fill="{AMB}"/>'''
rows = [("Building", "Agent Orchestrator"), ("Learning", "System design, by breaking things"), ("Writing", "Daily notes on Medium")]
cur = panel(194, 134) + t(rx+24, 222, "RIGHT NOW", 11, AMB, 700, extra='letter-spacing="2"')
for i, (k, v) in enumerate(rows):
    cur += f'<circle cx="{rx+30}" cy="{248+i*26}" r="4" fill="{AMB if i==0 else TEAL}"{" class=\"bk\"" if i==0 else ""}/>' + t(rx+46, 253+i*26, k, 13, DIM, 600) + t(rx+130, 253+i*26, v, 14, FG, 600)
greets = [("नमस्ते", "Hindi"), ("Hello", "English"), ("Hola", "Spanish"), ("Bonjour", "French"), ("Hallo", "German"), ("Ciao", "Italian")]
hello = panel(346, 118) + t(rx+24, 374, "SAYING HELLO TO THE WORLD", 11, "#a78bfa", 700, extra='letter-spacing="2"')
for i, (g, l) in enumerate(greets):
    hello += f'<g class="hl" style="animation-delay:{i*2:.0f}s;opacity:0">{t(rx+24, 428, g, 40, FG, 800)}{t(rx+rw-24, 428, l, 14, DIM, 600, "end")}</g>'
hello += t(rx+24, 452, "from India, to everyone", 12, DIM, 500)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>{css}</style>
<defs><linearGradient id="hd" x1="0" x2="1"><stop offset="0" stop-color="{AMB}"/><stop offset="1" stop-color="#ffb84d"/></linearGradient>
<linearGradient id="av" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2dd4bf"/><stop offset="1" stop-color="#f39c12"/></linearGradient>
<linearGradient id="st" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#b9770e"/><stop offset="1" stop-color="{AMB}"/></linearGradient>
<clipPath id="k"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>
<rect width="{W}" height="{H}" rx="16" fill="{BG}" stroke="{LINE}"/><g clip-path="url(#k)">{card}</g>{now}{cur}{hello}</svg>'''
(ROOT / "assets" / "hello-card.svg").write_text(svg); print("ok")
