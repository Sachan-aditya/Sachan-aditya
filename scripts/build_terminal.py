import os
import pathlib
OUT=str(pathlib.Path(__file__).resolve().parent.parent / "assets")
BG="#0d1117"; AMB="#f39c12"; TEAL="#2dd4bf"; DIM="#6e7681"; FG="#e6edf3"
FONT="font-family:'SF Mono','Fira Code',Consolas,'Courier New',monospace"

# ---------- HERO: looping terminal ----------
lines=[("$ whoami",AMB,0),
 ("> aditya sachan | full-stack dev + ai builder",FG,1),
 ("$ cat stack.txt",AMB,2),
 ("> java . spring boot . angular . python . kafka . redis",FG,3),
 ("$ ./orchestrate --agents --mode=multi",AMB,4),
 ("> email.agent  calendar.agent  meeting.agent  [online]",TEAL,5)]
T=16.0; start=[0.4,1.6,3.4,4.6,6.8,8.0]; dur=[1.0,1.8,1.2,2.4,1.8,2.2]
css="";body=""
y0=112; dy=34
for i,(txt,col,_) in enumerate(lines):
    y=y0+i*dy
    s=start[i]/T*100; e=(start[i]+dur[i])/T*100
    n=len(txt)
    css+=f"@keyframes c{i}{{0%,{s:.2f}%{{transform:translateX(0)}}{e:.2f}%,99%{{transform:translateX(760px)}}100%{{transform:translateX(0)}}}}"
    css+=f".k{i}{{animation:c{i} {T}s steps({n},end) infinite}}"
    body+=f'<text x="48" y="{y}" fill="{col}" font-size="17" style="{FONT}">{txt}</text>'
    body+=f'<rect class="k{i}" x="46" y="{y-19}" width="760" height="26" fill="#0d1117"/>'
css+=f"@keyframes bl{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}.cur{{animation:bl 1s steps(1) infinite}}"
css+=f"@keyframes gl{{0%,100%{{opacity:.35}}50%{{opacity:.8}}}}.glow{{animation:gl 4s ease-in-out infinite}}"
hero=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="360" viewBox="0 0 900 360">
<style>{css}</style>
<defs><clipPath id="cp"><rect x="20" y="56" width="860" height="283"/></clipPath><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#0f2027"/><stop offset="1" stop-color="#1b2a33"/></linearGradient>
<radialGradient id="r" cx=".85" cy=".1" r=".7"><stop offset="0" stop-color="{AMB}" stop-opacity=".45"/><stop offset="1" stop-color="{AMB}" stop-opacity="0"/></radialGradient></defs>
<rect width="900" height="360" rx="14" fill="url(#g)"/>
<rect class="glow" width="900" height="360" rx="14" fill="url(#r)"/>
<rect x="20" y="20" width="860" height="320" rx="10" fill="{BG}" stroke="#30363d"/>
<rect x="20" y="20" width="860" height="36" rx="10" fill="#161b22"/><rect x="20" y="44" width="860" height="12" fill="#161b22"/>
<circle cx="44" cy="38" r="6" fill="#ff5f56"/><circle cx="64" cy="38" r="6" fill="#ffbd2e"/><circle cx="84" cy="38" r="6" fill="#27c93f"/>
<text x="450" y="43" fill="{DIM}" font-size="13" text-anchor="middle" style="{FONT}">aditya@github: ~/profile</text>
<text x="48" y="84" fill="{DIM}" font-size="13" style="{FONT}">Last login: today on ttys001 | welcome back</text>
<g clip-path="url(#cp)">{body}</g>
<rect class="cur" x="48" y="{y0+6*dy-18}" width="10" height="20" fill="{AMB}"/>
</svg>'''
open(f"{OUT}/hero.svg","w").write(hero)

# ---------- CHARACTER SHEET ----------
skills=[("JAVA",92),("SPRING BOOT",90),("ANGULAR",82),("PYTHON",84),("SYSTEM DESIGN",72),("AI AGENTS",78),("KAFKA / REDIS",68)]
css="@keyframes f{from{transform:scaleX(0)}to{transform:scaleX(1)}}.bar{transform-box:fill-box;transform-origin:left;animation:f 1.6s cubic-bezier(.2,.8,.2,1) both}"
css+="@keyframes p{0%,100%{opacity:.6}50%{opacity:1}}.pulse{animation:p 2.4s ease-in-out infinite}"
rows=""
for i,(n,v) in enumerate(skills):
    y=150+i*38
    rows+=f'<text x="40" y="{y}" fill="{FG}" font-size="14" style="{FONT}">{n}</text>'
    rows+=f'<rect x="200" y="{y-13}" width="300" height="14" rx="3" fill="#161b22" stroke="#30363d"/>'
    rows+=f'<rect class="bar" style="animation-delay:{i*0.15}s" x="200" y="{y-13}" width="{3*v}" height="14" rx="3" fill="url(#b)"/>'
    rows+=f'<text x="515" y="{y}" fill="{AMB}" font-size="14" style="{FONT}">LV {v}</text>'
attrs=[("STR","Backend depth"),("INT","AI / agents"),("DEX","Ships fast"),("WIS","Writes daily"),]
ax=""
for i,(a,d) in enumerate(attrs):
    x=640+(i%2)*120; y=182+(i//2)*70
    ax+=f'<rect x="{x}" y="{y-28}" width="105" height="56" rx="8" fill="#161b22" stroke="#30363d"/><text x="{x+52}" y="{y-4}" fill="{AMB}" font-size="18" text-anchor="middle" style="{FONT}">{a}</text><text x="{x+52}" y="{y+16}" fill="{DIM}" font-size="10" text-anchor="middle" style="{FONT}">{d}</text>'
card=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="440" viewBox="0 0 900 440">
<style>{css}</style>
<defs><linearGradient id="b" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{AMB}"/></linearGradient></defs>
<rect width="900" height="440" rx="14" fill="{BG}" stroke="#30363d"/>
<text x="40" y="52" fill="{FG}" font-size="24" style="{FONT}">CHARACTER SHEET</text>
<text x="40" y="78" fill="{DIM}" font-size="13" style="{FONT}">Class: Full-Stack Artificer | Subclass: Agent Orchestrator | Realm: India</text>
<text class="pulse" x="860" y="52" fill="{AMB}" font-size="14" text-anchor="end" style="{FONT}">* PLAYER ONLINE</text>
<line x1="40" y1="96" x2="860" y2="96" stroke="#30363d"/>
<text x="40" y="124" fill="{TEAL}" font-size="13" style="{FONT}">SKILL TREE</text>
{rows}
<text x="640" y="124" fill="{TEAL}" font-size="13" style="{FONT}">ATTRIBUTES</text>
{ax}
<text x="640" y="330" fill="{TEAL}" font-size="13" style="{FONT}">ACTIVE QUEST</text>
<text x="640" y="352" fill="{FG}" font-size="13" style="{FONT}">Build a self-running</text>
<text x="640" y="370" fill="{FG}" font-size="13" style="{FONT}">AI-powered profile</text>
<rect x="640" y="382" width="220" height="10" rx="3" fill="#161b22" stroke="#30363d"/>
<rect class="bar" x="640" y="382" width="95" height="10" rx="3" fill="url(#b)"/>
<text x="40" y="420" fill="{DIM}" font-size="11" style="{FONT}">Levels are self-assessed and will be updated by the profile bot.</text>
</svg>'''
open(f"{OUT}/character-sheet.svg","w").write(card)

# ---------- PIPELINE with flowing dashes ----------
nodes=[("CRON","nightly"),("COLLECT","repos | medium"),("THINK","LLM"),("RENDER","README"),("COMMIT","live")]
css="@keyframes d{to{stroke-dashoffset:-24}}.flow{stroke-dasharray:6 6;animation:d 1s linear infinite}@keyframes g{0%,100%{opacity:.5}50%{opacity:1}}"
s=""
for i,(a,b) in enumerate(nodes):
    x=60+i*170
    col=AMB if a=="THINK" else TEAL
    s+=f'<g style="animation:g 3s ease-in-out infinite;animation-delay:{i*0.5}s"><rect x="{x}" y="70" width="120" height="70" rx="10" fill="#161b22" stroke="{col}" stroke-width="2"/><text x="{x+60}" y="100" fill="{col}" font-size="15" text-anchor="middle" style="{FONT}">{a}</text><text x="{x+60}" y="122" fill="{DIM}" font-size="11" text-anchor="middle" style="{FONT}">{b}</text></g>'
    if i<len(nodes)-1:
        s+=f'<line class="flow" x1="{x+120}" y1="105" x2="{x+170}" y2="105" stroke="{AMB}" stroke-width="2"/>'
s+=f'<path class="flow" d="M 490 140 C 490 190, 150 190, 150 140" fill="none" stroke="{TEAL}" stroke-width="1.5" opacity=".6"/><text x="320" y="196" fill="{DIM}" font-size="11" text-anchor="middle" style="{FONT}">feedback: embeddings -> vector store -> ask-my-profile bot</text>'
pipe=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="220" viewBox="0 0 900 220"><style>{css}</style>
<rect width="900" height="220" rx="14" fill="{BG}" stroke="#30363d"/>
<text x="30" y="38" fill="{FG}" font-size="16" style="{FONT}">THE AUTONOMOUS README LOOP</text>{s}</svg>'''
open(f"{OUT}/pipeline.svg","w").write(pipe)
print("ok")
