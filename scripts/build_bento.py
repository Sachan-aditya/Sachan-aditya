#!/usr/bin/env python3
"""Generate the bento-grid tiles (light + dark) used by README.md. Static SVGs, no animation."""
import pathlib
from xml.sax.saxutils import escape as esc
ROOT = pathlib.Path(__file__).resolve().parent.parent
SANS = "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
M = 5  # outer margin baked into each tile (gives the grid its gutters)

THEMES = {
 "light": dict(card="#f6f8fa", line="#d0d7de", text="#1f2328", mute="#59636e", acc="#b45309", tint="#fff1d6",
               chip="#ffffff", chipline="#d0d7de", ok="#1a7f37", glow="#f39c12"),
 "dark":  dict(card="#161b22", line="#30363d", text="#e6edf3", mute="#8b949e", acc="#f5a524", tint="#3a2a0c",
               chip="#21262d", chipline="#30363d", ok="#3fb950", glow="#f39c12"),
}

def tw(s, size, bold=False):  # rough text width
    return len(s) * size * (0.58 if bold else 0.54)

def wrap(text, size, width):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if tw(t, size) > width and cur: out.append(cur); cur = w
        else: cur = t
    return out + [cur]

class Tile:
    def __init__(s, name, w, h, th):
        s.name, s.w, s.h, s.t, s.b = name, w, h, th, []
        s.iw = w - 2 * M
    def text(s, x, y, txt, size=14, color=None, bold=False, spacing=0, anchor="start"):
        c = color or s.t["text"]; wt = 700 if bold else 400
        sp = f' letter-spacing="{spacing}"' if spacing else ""
        s.b.append(f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{wt}" text-anchor="{anchor}"{sp} style="{SANS}">{esc(txt)}</text>')
    def para(s, x, y, txt, size=14, color=None, lh=1.45, width=None):
        for i, ln in enumerate(wrap(txt, size, width or s.iw - 2 * (x - M))):
            s.text(x, y + i * size * lh, ln, size, color or s.t["mute"])
        return y + (i + 1) * size * lh
    def label(s, txt, x=28, y=38):
        s.text(x, y, txt, 11.5, s.t["mute"], True, 1.6)
    def chips(s, items, x, y, maxx=None, accent=()):
        maxx = maxx or (s.w - M - 24); cx = x
        for it in items:
            w = tw(it, 12) + 20
            if cx + w > maxx: cx = x; y += 30
            a = it in accent
            fill = s.t["tint"] if a else s.t["chip"]; ln = s.t["acc"] if a else s.t["chipline"]
            s.b.append(f'<rect x="{cx}" y="{y-16}" width="{w:.1f}" height="24" rx="12" fill="{fill}" stroke="{ln}"/>')
            s.text(round(cx + w / 2, 1), y, it, 12, s.t["acc"] if a else s.t["text"], a, anchor="middle")
            cx += w + 6
        return y
    def svg(s, extra=""):
        t = s.t
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.w}" height="{s.h}" viewBox="0 0 {s.w} {s.h}">'
                f'<defs><clipPath id="c"><rect x="{M}" y="{M}" width="{s.w-2*M}" height="{s.h-2*M}" rx="20"/></clipPath>'
                f'<radialGradient id="gl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{t["glow"]}" stop-opacity=".30"/><stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient></defs>'
                f'<rect x="{M}" y="{M}" width="{s.w-2*M}" height="{s.h-2*M}" rx="20" fill="{t["card"]}" stroke="{t["line"]}"/>'
                f'<g clip-path="url(#c)">{extra}</g>' + "".join(s.b) + "</svg>")

def build(name, w, h, fn):
    for tn, th in THEMES.items():
        t = Tile(name, w, h, th); extra = fn(t) or ""
        (ROOT / "assets" / tn / f"{name}.svg").write_text(t.svg(extra))

# ------------------------------------------------------------------ tiles
def intro(t):
    t.b.append(f'<circle cx="{t.w-40}" cy="40" r="10" fill="{t.t["ok"]}"/>')
    t.text(t.w - 60, 45, "Building multi-agent systems", 12.5, t.t["mute"], anchor="end")
    t.text(32, 118, "Aditya Sachan", 46, bold=True)
    t.text(32, 156, "Full-stack developer & AI builder", 21, t.t["acc"], True)
    t.text(32, 192, "Crafting tech solutions that make a difference.", 15.5, t.t["mute"])
    t.chips(["Java", "Spring Boot", "Angular", "Python", "AI Agents"], 32, 246, accent=("AI Agents",))
    return f'<circle cx="{t.w-30}" cy="30" r="150" fill="url(#gl)"/>'

def now(t):
    t.label("RIGHT NOW")
    rows = [("Building", "Agent Orchestrator"), ("Learning", "System design by breaking things"),
            ("Writing", "Daily notes on Medium"), ("Exploring", "RAG and tool-calling")]
    y = 76
    for k, v in rows:
        t.text(28, y, k, 12, t.t["acc"], True)
        y = t.para(28, y + 19, v, 14.5, t.t["text"], width=t.iw - 40) + 12

def stack(t):
    t.label("TECH STACK")
    groups = [("Languages", ["Java", "Python", "JavaScript", "Kotlin"]),
              ("Frameworks", ["Spring Boot", "Angular", "React", "TensorFlow"]),
              ("Data & infra", ["MySQL", "MongoDB", "Redis", "Kafka", "Docker", "Firebase"])]
    y = 74
    for k, items in groups:
        t.text(28, y, k, 12, t.t["mute"])
        y = t.chips(items, 28, y + 24) + 28

def whatido(t):
    t.label("WHAT I DO")
    rows = [("01", "Backend systems", "Spring Boot services, secure APIs and real-time data."),
            ("02", "Agentic AI", "Orchestrators that route work to specialised agents."),
            ("03", "System design", "Mini Redis and Kafka built from scratch to learn internals.")]
    y = 76
    for n, h, d in rows:
        t.text(28, y + 4, n, 22, t.t["acc"], True)
        t.text(76, y - 2, h, 16, bold=True)
        t.para(76, y + 18, d, 13, width=t.iw - 76)
        y += 66

def project(title, desc, stack_, status):
    def f(t):
        ok = status == "Shipped"
        col = t.t["ok"] if ok else t.t["acc"]
        t.b.append(f'<circle cx="34" cy="36" r="4.5" fill="{col}"/>')
        t.text(46, 40, status.upper(), 11, col, True, 1.4)
        t.text(28, 80, title, 21, bold=True)
        t.para(28, 106, desc, 13.5, width=t.iw - 40)
        t.chips(stack_, 28, t.h - 40)
    return f

def link(label, big, small=None, arrow=True):
    def f(t):
        t.label(label)
        t.text(28, 82, big, 20, bold=True)
        if small: t.para(28, 106, small, 13.5, width=t.iw - 40)
        if t.name == "mail": t.text(28, 106, "sachanaditya207@gmail.com", 11.5, t.t["mute"])
        if arrow: t.text(28, t.h - 28, "Open  →", 13.5, t.t["acc"], True)
    return f

TILES = {}
def reg(name, w, h, fn): TILES[name] = (w, h); build(name, w, h, fn)
reg("intro", 560, 290, intro); reg("now", 280, 290, now)
reg("stack", 420, 272, stack); reg("whatido", 420, 272, whatido)
reg("p_cricklive", 280, 215, project("CrickLive", "Real-time cricket scores platform.", ["Spring Boot", "Angular"], "Shipped"))
reg("p_agrofarm", 280, 215, project("Agrofarm", "Digital marketplace for farmers and customers.", ["React", "MongoDB", "Razorpay"], "Shipped"))
reg("p_museai", 280, 215, project("MuseAI", "Audio recognition and song recommendations.", ["TensorFlow", "Kotlin"], "Shipped"))
reg("p_taskapi", 280, 215, project("Task Manager API", "Secure REST API for task management.", ["Spring Boot", "JWT"], "Shipped"))
reg("p_orchestrator", 280, 215, project("Agent Orchestrator", "Master and domain orchestrators routing work to email, calendar and meeting agents.", ["Python", "LLMs"], "Building"))
reg("p_ministack", 280, 215, project("MiniStack", "Mini Redis, queue, Kafka and DB built from scratch to learn internals.", ["Python"], "Building"))
reg("writing", 420, 160, link("DAILY WRITING NOTES", "I write what I learn.", "Daily notes on engineering and AI."))
reg("resume", 210, 160, link("RESUME", "Download", None))
reg("mail", 210, 160, link("SAY HI", "Email me", None))
print("tiles:", len(TILES))
import json; (ROOT / "data").mkdir(exist_ok=True); (ROOT / "data" / "tiles.json").write_text(json.dumps(TILES))
