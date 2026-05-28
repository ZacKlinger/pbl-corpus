# Research web

Live: **https://zacklinger.github.io/pbl-corpus/** (once GitHub Pages is enabled — see deployment below)

Interactive force-directed graph of the resource bank. Nodes = claim-evidence threads, verified sources, leads, raw files awaiting processing. Edges = supports, counters, frames, relates-to, tracked-in. Node size scales with degree (connectivity), so the most-referenced pillars and resources visually grow as the corpus matures.

## Local preview

```sh
python3 -m http.server -d web 8000
# open http://localhost:8000
```

## How it gets regenerated

`bin/build-graph.py` walks `sources/`, `claim-evidence/`, `leads/`, `canon-map.md`, `thesis-seeds.md`, and `sources-raw/`, then writes `web/graph.json`. Run as part of the Saturday session's index-build step (`bin/build-index.sh` invokes it at the end). The rendered page (`index.html`) fetches `graph.json` on load and lays out a Cytoscape.js force-directed graph.

## Deployment

`.github/workflows/deploy-pages.yml` deploys the `web/` directory to GitHub Pages on every push to `main`. **One-time setup:** go to **Settings → Pages** on the GitHub repo and set the source to "GitHub Actions" (not "Deploy from a branch"). After that, every push that touches the corpus rebuilds the graph and redeploys.

## Conventions

- **Layer colors** come from frontmatter `layer:` field (empirical / visionary / practitioner). Add a new layer? Add a color in `LAYER_COLOR` in `index.html`.
- **Edge kinds** come from which section a source link appears under in a claim-evidence file (`### Supporting evidence` → supports; `### Counter-evidence` → counters; `### Cross-listed` → frames).
- **Thread slugs** are canonical: each slug names a file in `claim-evidence/<slug>.md` AND a heading prefix in `thesis-seeds.md`. The script's `SEED_TITLES` and `title_to_slug` in `bin/build-graph.py` must stay in sync with both.
- The graph is a derived artifact: never edit `graph.json` by hand. Edit the underlying markdown and re-run the extractor.
