#!/usr/bin/env python3
"""AI project showcase for a GitHub profile README.

Pipeline:  GitHub API -> collect repos -> Claude writes punchy cards -> inject into README markers.

Env:
  GITHUB_USER        default: Sachan-aditya
  GITHUB_TOKEN       optional (higher rate limit)
  ANTHROPIC_API_KEY  optional; without it the script falls back to plain repo descriptions
  ANTHROPIC_MODEL    default: claude-sonnet-4-5
  MAX_PROJECTS       default: 6
  MOCK=1             offline demo mode (no network), used for testing
"""
import hashlib, json, os, re, sys, urllib.request, datetime, pathlib

USER = os.getenv("GITHUB_USER", "Sachan-aditya")
MAX_PROJECTS = int(os.getenv("MAX_PROJECTS", "6"))
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")
MOCK = os.getenv("MOCK") == "1"
ROOT = pathlib.Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CACHE = ROOT / "data" / "projects_cache.json"
PROFILE_REPO = USER.lower()  # skip the profile repo itself

# ---------------------------------------------------------------- GitHub
def gh(path, raw=False):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("User-Agent", "readme-bot")
    req.add_header("Accept", "application/vnd.github.raw+json" if raw else "application/vnd.github+json")
    if os.getenv("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", "replace")
    return body if raw else json.loads(body)

def collect_repos():
    if MOCK:
        return json.loads((ROOT / "data" / "mock_repos.json").read_text())
    repos = gh(f"/users/{USER}/repos?per_page=100&sort=pushed")
    repos = [r for r in repos if not r["fork"] and not r["archived"] and r["name"].lower() != PROFILE_REPO]
    repos.sort(key=lambda r: (r["stargazers_count"], r["pushed_at"]), reverse=True)
    out = []
    for r in repos[:MAX_PROJECTS]:
        try:
            readme = gh(f"/repos/{USER}/{r['name']}/readme", raw=True)[:3500]
        except Exception:
            readme = ""
        try:
            langs = list(gh(f"/repos/{USER}/{r['name']}/languages").keys())[:5]
        except Exception:
            langs = []
        out.append({"name": r["name"], "url": r["html_url"], "description": r["description"] or "",
                    "stars": r["stargazers_count"], "topics": r.get("topics", []), "languages": langs,
                    "pushed_at": r["pushed_at"], "readme": readme})
    return out

# ---------------------------------------------------------------- LLM
def llm(prompt, max_tokens=700):
    if MOCK:
        return None
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return None
    import anthropic
    client = anthropic.Anthropic(api_key=key)
    msg = client.messages.create(model=MODEL, max_tokens=max_tokens,
                                 messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in msg.content if b.type == "text")

def parse_json(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    return json.loads(m.group(0)) if m else None

CARD_PROMPT = """You write punchy, honest GitHub profile project cards.
Project: {name}
Description: {description}
Languages: {languages}
Topics: {topics}
README excerpt:
{readme}

Return ONLY JSON with keys:
  emoji (one emoji), hook (max 8 words, catchy, no clickbait lies),
  what (one sentence, max 22 words, concrete),
  wow (one sentence on the most impressive technical aspect, max 22 words),
  stack (array of up to 4 short strings).
Only claim things supported by the input. No hype words like 'revolutionary'."""

def make_card(repo, cache):
    sig = hashlib.sha256((repo["pushed_at"] + repo["description"] + repo["readme"]).encode()).hexdigest()[:16]
    hit = cache.get(repo["name"])
    if hit and hit["sig"] == sig:
        return hit["card"]
    card = None
    try:
        raw = llm(CARD_PROMPT.format(name=repo["name"], description=repo["description"],
                  languages=", ".join(repo["languages"]), topics=", ".join(repo["topics"]),
                  readme=repo["readme"] or "(none)"))
        card = parse_json(raw)
    except Exception as e:
        print(f"[warn] LLM failed for {repo['name']}: {e}", file=sys.stderr)
    if not card:  # graceful fallback
        card = {"emoji": "🧪", "hook": repo["name"], "what": repo["description"] or "Work in progress.",
                "wow": "", "stack": repo["languages"][:4]}
    cache[repo["name"]] = {"sig": sig, "card": card}
    return card

IDEA_PROMPT = """Suggest ONE original, buildable-in-a-weekend project idea for a developer whose stack is:
{stack}
Their recent projects: {projects}
Make it fresh (not another todo app), concrete, and a little surprising.
Return ONLY JSON: {{"title": "...", "pitch": "one sentence", "stack": ["..."], "first_step": "one sentence"}}"""

def make_idea(repos):
    today = datetime.date.today().isoformat()
    stack = sorted({l for r in repos for l in r["languages"]}) or ["Java", "Python"]
    try:
        raw = llm(IDEA_PROMPT.format(stack=", ".join(stack), projects=", ".join(r["name"] for r in repos)), 400)
        idea = parse_json(raw)
    except Exception as e:
        print(f"[warn] idea failed: {e}", file=sys.stderr); idea = None
    if not idea:
        idea = {"title": "Self-healing README bot", "pitch": "A bot that notices stale project descriptions and rewrites them.",
                "stack": ["Python", "GitHub Actions", "LLM"], "first_step": "Diff each repo's latest commit against its README."}
    return today, idea

# ---------------------------------------------------------------- Render
def esc(s):  # keep table cells safe
    return (s or "").replace("|", "\\|").replace("\n", " ")

def render_projects(repos, cards):
    rows = ["| | Project | What it does | The cool part | Stack |", "|---|---|---|---|---|"]
    for r in repos:
        c = cards[r["name"]]
        stack = " ".join(f"`{s}`" for s in c.get("stack", []))
        rows.append(f"| {c['emoji']} | **[{esc(r['name'])}]({r['url']})**<br/><sub>{esc(c['hook'])}</sub> | "
                    f"{esc(c['what'])} | {esc(c.get('wow',''))} | {stack} |")
    return "\n".join(rows)

def render_idea(today, idea):
    stack = " ".join(f"`{s}`" for s in idea.get("stack", []))
    return (f"> 💡 **Today's AI project idea** <sub>({today})</sub>\n>\n"
            f"> **{esc(idea['title'])}**: {esc(idea['pitch'])}\n>\n"
            f"> {stack}  \n> 🚀 *First step:* {esc(idea['first_step'])}")

def inject(text, name, content):
    pat = re.compile(rf"(<!-- START_SECTION:{name} -->)(.*?)(<!-- END_SECTION:{name} -->)", re.S)
    if not pat.search(text):
        print(f"[warn] marker {name} not found", file=sys.stderr); return text
    return pat.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", text)

def main():
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    repos = collect_repos()
    cards = {r["name"]: make_card(r, cache) for r in repos}
    today, idea = make_idea(repos)
    text = README.read_text()
    text = inject(text, "ai-projects", render_projects(repos, cards))
    text = inject(text, "ai-idea", render_idea(today, idea))
    README.write_text(text)
    CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False))
    print(f"updated {len(repos)} projects")

if __name__ == "__main__":
    main()
