# pbl-corpus

A research corpus on project-based learning — execution frameworks (PBLWorks Gold Standard, EL Education, HTH, NTN), impact literature (Chen & Yang, Condliffe, Lucas Education Research, Hattie), and foundational theory (Dewey, Kilpatrick, UbD, How People Learn, Vygotsky).

Companion to [`learning-thesis`](../learning-thesis). The two repos share the [corpus protocol](docs/corpus-protocol.md) so a future RAG can rank claims across both.

## How to read this repo

- **Start at [`INDEX.md`](INDEX.md)** — auto-generated entry point listing every source, claim-evidence thread, and digest.
- **Latest digest** in [`digests/`](digests/) is the weekly artifact written for the human reader.
- **[`thesis-seeds.md`](thesis-seeds.md)** is the strawman direction document. Edit it before the first Saturday agent run.

## How this corpus gets built

A scheduled Claude routine runs weekly. Each run:

1. Pulls the latest from `main`.
2. Reads `thesis-seeds.md` and `queue.md` for direction.
3. Audits 2–3 existing claims (re-verify quote + URL + locator).
4. Advances the queue (reads new sources from `sources-raw/`, writes verified `sources/` notes + claim-evidence updates).
5. Writes the weekly digest.
6. Rebuilds `INDEX.md`.
7. Commits per-source, pushes once at the end.

Sources arrive in `sources-raw/` via the `fetch-sources` GitHub Action that polls `sources-wishlist.txt`. Files the workflow can't fetch (paywalled, dead URLs) get demoted to `leads/`.

See [`CLAUDE.md`](CLAUDE.md) for the full agent protocol.
