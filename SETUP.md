# Setup (5 minutes)

1. Create a public repo named exactly `Sachan-aditya` and push everything in this folder.
2. Repo Settings > Secrets and variables > Actions > New secret: `ANTHROPIC_API_KEY`.
3. Repo Settings > Actions > General > Workflow permissions: **Read and write**.
4. Actions tab > "Update README with AI" > Run workflow. After that it runs daily.

Local test (no network, no key): `MOCK=1 python scripts/update_readme.py`
Real run: `pip install -r scripts/requirements.txt && ANTHROPIC_API_KEY=... python scripts/update_readme.py`

Tweaks: `MAX_PROJECTS` (default 6), `ANTHROPIC_MODEL` (default claude-sonnet-4-5), prompts live in `scripts/update_readme.py`.
Without an API key it still runs and falls back to your plain repo descriptions.
