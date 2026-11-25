# Setup

1. Create a public repo named exactly `Sachan-aditya` and push everything in this folder (keep `assets/`).
2. Now Playing card: edit `data/now_playing.json` (title, artist), then run `python scripts/build_card.py`.
   It is a static card; a live Spotify feed needs a third-party service that you authorise with your own Spotify account.
3. Optional AI project cards: add secret `ANTHROPIC_API_KEY`, set Settings > Actions > General > Workflow permissions to Read and write,
   then run the "Update README with AI" workflow once. Don't want it? Delete `.github/`.
4. Regenerate the terminal and character sheet with `python scripts/build_terminal.py`.
