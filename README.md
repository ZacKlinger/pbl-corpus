# pbl-corpus

A domain-expertise corpus on project-based learning — its design frameworks (PBLWorks Gold Standard, HQPBL, EL Education, HTH, NTN), its literature (Condliffe/MDRC, Chen & Yang, Lucas Education Research, Mehta & Fine), and its intellectual lineage (Dewey, Kilpatrick, Bruner, Vygotsky, UbD, How People Learn).

**Scope:** This corpus is a *scholar of* PBL — it catalogs the field, including the field's internal disagreements, faithfully. It does **not** adjudicate whether PBL "works." That question lives in the [`learning-thesis`](../learning-thesis) sibling corpus, where PBL is one candidate instance of "ambitious learning that wasn't previously possible." External critiques of PBL (cognitive-load-theory objections, direct-instruction counter-arguments) belong there; they cross-link from here.

The two repos share the [corpus protocol](docs/corpus-protocol.md) so a future RAG can rank claims across both.

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
