#!/usr/bin/env python3
"""Render data/tree.json into an animated, organic skill-tree SVG (assets/tree.svg)."""
import json, math, random, pathlib
from xml.sax.saxutils import escape
ROOT = pathlib.Path(__file__).resolve().parent.parent
tree = json.loads((ROOT / "data" / "tree.json").read_text())
e = escape
W, H, CX, CY = 1200, 800, 600, 700
RADII = [0, 150, 330, 500]; SPREAD = 72; GAP = 1.6
BG, FG, DIM = "#0b0f14", "#e6edf3", "#8b949e"
FONT = "font-family:'SF Mono','Fira Code',Consolas,'Courier New',monospace"
rnd = random.Random(7)

def pt(a, r):  # angle in degrees from vertical, clockwise
    t = math.radians(a); return CX + r * math.sin(t), CY - r * math.cos(t)

def edge(p, ap, c, ac, k=0.5):
    d = math.dist(p, c) * k
    t1, t2 = math.radians(ap), math.radians(ac)
    c1 = (p[0] + d * math.sin(t1), p[1] - d * math.cos(t1))
    c2 = (c[0] - d * math.sin(t2), c[1] + d * math.cos(t2))
    return f"M{p[0]:.1f},{p[1]:.1f} C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {c[0]:.1f},{c[1]:.1f}"

# ---- assign angles from leaf slots
slot = 0.0; leaves = []
for b in tree["children"]:
    for g in b["children"]:
        g["leaves"] = [{"name": n, "slot": (slot := slot + 1) - 1} for n in g["children"]]
    slot += GAP
last = slot - GAP - 1
ang = lambda s: -SPREAD + s / last * 2 * SPREAD
for b in tree["children"]:
    for g in b["children"]:
        for l in g["leaves"]: l["a"] = ang(l["slot"])
        g["a"] = (g["leaves"][0]["a"] + g["leaves"][-1]["a"]) / 2
    b["a"] = (b["children"][0]["a"] + b["children"][-1]["a"]) / 2

paths, sap, nodes, labels, twigs = [], [], [], [], []
def add_edge(d, color, w, delay, dur=1.1, flow=True):
    paths.append(f'<path d="{d}" pathLength="1" class="g" stroke="{color}" stroke-width="{w}" style="animation-delay:{delay:.2f}s;animation-duration:{dur}s"/>')
    if flow:
        sap.append(f'<path d="{d}" class="sap" stroke="{color}" style="animation-delay:{delay+4.5:.2f}s,{delay+4.5:.2f}s"/>')

# trunk + roots
trunk = f"M{CX},{H} C{CX-10},{H-40} {CX+8},{CY+40} {CX},{CY+8}"
paths.append(f'<path d="{trunk}" pathLength="1" class="g" stroke="url(#bark)" stroke-width="18" style="animation-delay:0s;animation-duration:1s"/>')
for i, (dx, dy) in enumerate([(-260, 30), (-150, 60), (150, 60), (260, 30), (-60, 70), (70, 75)]):
    d = f"M{CX},{CY+45} C{CX+dx*0.2},{CY+60+dy*0.3} {CX+dx*0.7},{H-90+dy*0.4} {CX+dx},{min(H-6, CY+55+dy*0.9+40)}"
    paths.append(f'<path d="{d}" pathLength="1" class="g" stroke="#5b4026" stroke-width="{4 if abs(dx)>100 else 3}" opacity=".7" style="animation-delay:{0.3+i*0.1:.2f}s;animation-duration:1.2s"/>')

root_p = (CX, CY)
for bi, b in enumerate(tree["children"]):
    col = b["color"]; bp = pt(b["a"], RADII[1] + [-22, 46, -22, 46, 52, -30][bi % 6]); bd = 1.0 + bi * 0.15
    add_edge(edge(root_p, 0, bp, b["a"], 0.55), col, 7, bd, 1.0)
    nodes.append(("branch", bp, b["name"], col, bd + 0.9))
    for gi, g in enumerate(b["children"]):
        r2 = RADII[2] + (-30 if (bi + gi) % 2 else 30)
        gp = pt(g["a"], r2); gd = bd + 0.9 + gi * 0.12
        add_edge(edge(bp, b["a"], gp, g["a"]), col, 3.6, gd, 1.0)
        nodes.append(("group", gp, g["name"], col, gd + 0.9))
        # decorative twigs around the group node
        for _ in range(3):
            ta = g["a"] + rnd.uniform(-14, 14); tl = rnd.uniform(28, 55)
            tp = (gp[0] + tl * math.sin(math.radians(ta)), gp[1] - tl * math.cos(math.radians(ta)))
            twigs.append((edge(gp, g["a"], tp, ta + rnd.uniform(-20, 20), 0.5), col, tp, gd + 1.0))
        for l in g["leaves"]:
            lp = pt(l["a"], RADII[3]); ld = gd + 0.9 + l["slot"] * 0.02
            add_edge(edge(gp, g["a"], lp, l["a"]), col, 1.8, ld, 1.0)
            nodes.append(("leaf", lp, l["name"], col, ld + 0.9, l["a"]))
            for _ in range(2):  # tiny twigs
                ta = l["a"] + rnd.uniform(-25, 25); tl = rnd.uniform(14, 26)
                mid = pt(l["a"], rnd.uniform(450, 485))
                tp = (mid[0] + tl * math.sin(math.radians(ta)), mid[1] - tl * math.cos(math.radians(ta)))
                twigs.append((f"M{mid[0]:.1f},{mid[1]:.1f} L{tp[0]:.1f},{tp[1]:.1f}", col, tp, ld + 0.6))

svg = []
for kind, p, name, col, delay, *rest in nodes:
    x, y = p
    if kind == "leaf":
        a = rest[0]
        svg.append(f'<circle class="n" cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{col}" filter="url(#glow)" style="animation-delay:{delay:.2f}s"/>')
        off = 11
        if a >= 0: tx, ty = pt(a, RADII[3] + off); rot = a - 90; anchor = "start"
        else:      tx, ty = pt(a, RADII[3] + off); rot = a + 90; anchor = "end"
        labels.append(f'<g transform="translate({tx:.1f},{ty:.1f}) rotate({rot:.1f})"><text class="n" text-anchor="{anchor}" dominant-baseline="central" fill="{FG}" font-size="12.5" style="{FONT};animation-delay:{delay+0.2:.2f}s">{e(name)}</text></g>')
    else:
        big = kind == "branch"; fs = 14 if big else 11.5; w = len(name) * (fs * 0.62) + 18; h = 26 if big else 20
        fill = col if big else "#111820"; tc = BG if big else col
        labels.append(f'<g class="n" style="animation-delay:{delay:.2f}s"><rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{col}" stroke-width="1.5"/><text x="{x:.1f}" y="{y+0.5:.1f}" text-anchor="middle" dominant-baseline="central" fill="{tc}" font-size="{fs}" font-weight="{700 if big else 500}" style="{FONT}">{e(name)}</text></g>')
for d, col, tp, delay in twigs:
    paths.append(f'<path d="{d}" pathLength="1" class="g" stroke="{col}" stroke-width="1" opacity=".55" style="animation-delay:{delay:.2f}s;animation-duration:.9s"/>')
    svg.append(f'<circle class="n" cx="{tp[0]:.1f}" cy="{tp[1]:.1f}" r="2" fill="{col}" opacity=".7" style="animation-delay:{delay+0.8:.2f}s"/>')

stars = "".join(f'<circle cx="{rnd.randint(10,W-10)}" cy="{rnd.randint(10,H-160)}" r="{rnd.choice([0.8,1,1.4])}" fill="#fff" class="tw" style="animation-delay:{rnd.uniform(0,4):.1f}s"/>' for _ in range(90))
rings = "".join(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="#1c2530" stroke-dasharray="2 8"/>' for r in RADII[1:])
root = f'<g class="n" style="animation-delay:.6s"><circle cx="{CX}" cy="{CY}" r="46" fill="#f39c12" opacity=".15" filter="url(#glow)"/><rect x="{CX-92}" y="{CY-22}" width="184" height="44" rx="22" fill="#111820" stroke="#f39c12" stroke-width="2.5"/><text x="{CX}" y="{CY+1}" text-anchor="middle" dominant-baseline="central" fill="#f39c12" font-size="16" font-weight="700" style="{FONT}">{tree["name"]}</text></g>'

css = """
.g{fill:none;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;animation:grow 1s ease-out forwards}
@keyframes grow{to{stroke-dashoffset:0}}
.n{opacity:0;animation:pop .6s ease-out forwards;transform-box:fill-box;transform-origin:center}
@keyframes pop{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:scale(1)}}
.sap{fill:none;stroke-width:2;stroke-dasharray:3 22;stroke-linecap:round;opacity:0;animation:show .5s forwards,flow 2.4s linear infinite}
@keyframes show{to{opacity:.9}}@keyframes flow{to{stroke-dashoffset:-50}}
.tw{animation:tw 3s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.15}50%{opacity:.8}}
"""
out = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>{css}</style>
<defs>
<linearGradient id="bark" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#3b2a1a"/><stop offset="1" stop-color="#b9772a"/></linearGradient>
<radialGradient id="bg" cx=".5" cy="1" r="1"><stop offset="0" stop-color="#1a2430"/><stop offset="1" stop-color="{BG}"/></radialGradient>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{W}" height="{H}" rx="16" fill="url(#bg)" stroke="#30363d"/>
{stars}{rings}
<text x="36" y="52" fill="{FG}" font-size="22" font-weight="700" style="{FONT}">THE SKILL TREE</text>
<text x="36" y="76" fill="{DIM}" font-size="13" style="{FONT}">branches grow as I learn | glowing sap = live knowledge</text>
{"".join(paths)}{"".join(sap)}{"".join(svg)}{"".join(labels)}{root}
</svg>'''
(ROOT / "assets" / "tree.svg").write_text(out)
print("tree.svg", len(out)//1024, "KB")
