# Setup

1. Create a public repo named exactly `Sachan-aditya` and push everything in this folder (keep the folder structure).
2. Optional AI project radar: add secret `ANTHROPIC_API_KEY` (Settings > Secrets and variables > Actions) and set
   Settings > Actions > General > Workflow permissions to **Read and write**. Then run the "Update README with AI" workflow once.
   If you don't want it, delete the `.github/` folder and the "AI project radar" block at the bottom of README.md.

Edit the tiles: change text in `scripts/build_bento.py`, then run `python scripts/build_bento.py` (regenerates assets/light and assets/dark).
Project tiles link to your repositories page; point each to its exact repo by editing the links in README.md.
Local test of the AI script without a key: `MOCK=1 python scripts/update_readme.py`
