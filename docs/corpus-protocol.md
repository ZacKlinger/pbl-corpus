# Corpus Protocol

A portable specification for research repos that need to share a RAG index.

Two repos that follow this protocol produce artifacts shaped the same way: a retriever can rank claims from corpus A against claims from corpus B, filter by the same metadata, and resolve citations the same way. Deviate from the **structural** parts of this spec only with reason. Domain — your thesis, your canon, your threads — is yours to define.

---

## Why structure is load-bearing for RAG

- **The retrievable unit must be the same shape across repos.** A `## Claim:` block here and a `## Claim:` block in the other corpus need to be structurally identical, or the retriever cannot rank them against the same query.
- **Metadata must be joinable.** `layer: empirical` has to mean the same thing everywhere. A frontmatter field that's `authors` in one repo and `author` in the other silently breaks filters.
- **Verified and unverified must be mechanically separable.** A retriever asked for evidence should never surface unverified material by accident. Different directories make this trivial.
- **Citations must resolve.** A verbatim quote points to a source note; the source note points to the primary source. Every link is relative; every locator is typed.

---

## Three non-negotiables

These survive across domains. Port them verbatim.

1. **No fabrication.** Every claim entering `claim-evidence/` includes a verbatim quote, a link to the source note, and a locator (page, section, timestamp, paragraph). Paraphrase without a quote is not evidence.
2. **Leads ≠ evidence.** Material you've heard about but not read goes in `leads/`. Material you've read and quoted goes in `claim-evidence/`. Never collapse the two — the directory boundary is what keeps the RAG honest.
3. **Steelman before agreement.** When you find a counter-position with real warrant, give it its own entry. Don't bury it inside a supporting entry. The retriever must be able to surface both sides of a disagreement when asked.

---

## Three-layer taxonomy

Every source and every claim is tagged with one of:

- **empirical** — peer-reviewed cognitive science, ed psych, NRC reports, meta-analyses, RCTs. Highest evidentiary weight for causal claims.
- **visionary** — philosophical, theoretical, programmatic writing. Highest weight for framing and aims.
- **practitioner** — observation and design from inside the work. Highest weight for what works in real settings over time.

This taxonomy is shared across compatible repos. Don't introduce new layer values without coordinating across all repos — a new value silently breaks every filter that uses the field.

---

## Directory layout (mandatory)

```
canon-map.md            # living map of canon entries across the three layers
queue.md                # prioritized list of next work
thesis-seeds.md         # current thesis threads (allowed to evolve)
claim-evidence/         # one file per thread; verified verbatim quotes only
leads/                  # unverified material, hypotheses, things to investigate
sources/                # one note per work actually read (with frontmatter)
sources-raw/            # raw bytes of primary sources (PDF / HTML / TXT)
sources-wishlist.txt    # URLs to fetch into sources-raw/ (if sandboxed)
sessions/               # session logs (per agent run, dated YYYY-MM-DD.md)
digests/                # outward-facing digests for the human reader, dated
steers/                 # human-authored direction notes the agent reads
INDEX.md                # generated browsable entry point
bin/                    # build-index, build-graph, health-check
.github/workflows/      # fetcher workflow + any other automation
```

Three boundaries are load-bearing:

- **`sources/` (verified notes) and `leads/` (unverified) are different directories.** Never collapse.
- **`sources-raw/` holds bytes; `sources/` holds notes that reference those bytes.** The note's frontmatter `url` field can be the original URL or the local raw path — be consistent within a repo.
- **Generated artifacts (`INDEX.md`, `web/graph.json`) are rebuilt by `bin/` scripts** and not hand-edited.

---

## Per-source note schema (mandatory)

Filename: `AUTHOR-YEAR-shortname.md` in `sources/`. Lowercase, hyphenated, no spaces.

Frontmatter (YAML, all fields required):

```yaml
---
title:          # full work title
authors:        # comma-separated, "Last, First" preferred
year:           # integer
layer:          # empirical | visionary | practitioner
url:            # canonical source URL (where the quotes can be checked)
access_date:    # ISO date (YYYY-MM-DD) when you read the source for this note
read_status:    # read | skimmed | excerpted
---
```

Body sections (in this order, headings exact):

```markdown
## Thesis
One paragraph: what the work argues.

## Key quoted claims
- "verbatim quote" — locator (e.g., p. 76; §3.2; 12:45; ¶4)
- "verbatim quote" — locator
- ...

## Methods
(Empirical works only. Omit otherwise.)

## Where this sits in the corpus
Relative links to `../canon-map.md` entries and other `sources/` notes.

## Tensions / contradictions
Where this disagrees with other corpus entries. Name them.
```

---

## Claim-evidence schema (mandatory)

One file per thread in `claim-evidence/`. You define your threads; the structure inside each file is fixed.

```markdown
# Thread: <thread name>

Thesis-seed: *"<verbatim seed sentence from thesis-seeds.md>"*

**Status (YYYY-MM-DD):** One paragraph on the current state of the thread.

---

## Claim: <one-sentence claim>

(Optional brief framing, 1–3 sentences.)

### Supporting evidence
- "verbatim quote" — [Author Year](../sources/AUTHOR-YEAR-shortname.md), p. N — layer: empirical
- "verbatim quote" — [Author Year](../sources/AUTHOR-YEAR-shortname.md), §3 — layer: visionary

### Counter-evidence
- "verbatim quote" — [Author Year](../sources/AUTHOR-YEAR-shortname.md), p. N — layer: empirical

### Open questions
- ...

---

## Claim: <next claim>
...
```

Each evidence bullet is a self-contained retrievable unit. The format guarantees four resolutions per unit: quote → source note (link), source note → primary source (frontmatter `url`), evidence → layer (filter), evidence → thread (parent file). That's what makes cross-corpus retrieval work.

---

## Quote-citation invariants

Small rules that compound:

- **Verbatim is literal.** Copy with exact punctuation, spacing, capitalization. If you must elide, use `[...]`. Never elide across a clause that changes meaning.
- **One quote per bullet.** Don't pack multiple quotes into one bullet — the retrieval unit is the bullet.
- **Locator goes after the link, before the layer.** Always: `"quote" — [Author Year](path) — locator — layer: X`. Parsers depend on this order.
- **Relative links only.** No absolute paths. Repos get cloned, vendored, indexed.
- **Access date is required on every source note.** URLs rot; access_date lets the RAG explain "this source was current as of YYYY-MM-DD."
- **Don't rename source files after creation.** The link graph depends on filenames; renaming silently breaks every reference.

---

## Wishlist + fetcher (recommended if your agent is sandboxed)

Some agents run in containers that block outbound HTTP. The pattern:

- **`sources-wishlist.txt`**: lines of `<filename> <url>`. The agent appends entries when it needs a source it can't fetch.
- **`.github/workflows/fetch-sources.yml`**: triggers on wishlist changes; fetches each URL from github.com infrastructure (which has unrestricted internet); commits bytes to `sources-raw/`; pushes back to main.

Two failure modes to guard against:
- Publishers return HTTP 200 with an HTML landing page instead of a PDF. Add a post-fetch `file --mime-type` check.
- URLs rot. Log failures clearly so the agent can demote dead links to `leads/` and find alternate mirrors.

If your agent runs unsandboxed (full outbound HTTP), skip the wishlist and fetch directly — but still keep `sources-raw/` as the canonical location for raw bytes, so the rest of the protocol works the same.

---

## Digest format (per agent run)

`digests/YYYY-MM-DD.md` is what a human reader actually reads. Write *for them*, not as internal bookkeeping. Suggested sections, in order:

- **What I read this week** — bulleted, with `../sources/` links and one-sentence takeaways
- **New claims added** — links into `claim-evidence/` with what's new
- **Audit results** — N claims re-verified, M issues found and fixed/demoted
- **Tensions I noticed** — the most interesting complication this week
- **Thesis-fit check** — quote a current thesis line; did the reading support or complicate it?
- **Next week's queue** — top 3 items
- **Where I need you** — blockers, decisions, paywalled sources

---

## What's yours to define

The protocol fixes structure, not content. These are yours:

- **Thesis seeds** — the threads you're arguing
- **Canon entries** — which works are in your corpus, in which layer
- **Thread topology** — how many threads, what they cover, how they connect
- **Layer emphasis** — your domain may lean heavily on one or two of the three layers
- **Verification ritual specifics** — your domain's tolerance for primary vs. secondary sources, for translations, for excerpts

Once you've made those decisions, structure your artifacts the way this spec specifies. That's what makes cross-corpus RAG possible.

---

## When two compatible corpora are indexed together

Index these into the RAG:
- `sources/*.md` — each as a document; frontmatter as metadata
- `claim-evidence/*.md` — split on `## Claim:`; each claim block is a document; thread name + thesis-seed travel as metadata
- `digests/*.md` — each as a document, dated
- `canon-map.md`, `thesis-seeds.md` — sections as documents

Don't index:
- `sources-raw/` — binary
- `leads/` — unverified; if you want them retrievable, build a separate index and never blend
- `sessions/` — internal logs
- `bin/`, `web/`, `INDEX.md`, other generated artifacts

A query against the combined index should return evidence ranked by relevance regardless of which corpus the evidence came from. If that doesn't work, something in this spec was deviated from — track down the deviation rather than hand-tuning the retriever.
