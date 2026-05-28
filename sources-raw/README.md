# sources-raw/

Primary-source files (PDF, text, HTML). The autonomous agent reads files in this directory and produces verified `sources/AUTHOR-YEAR-shortname.md` notes with verbatim quotes.

## How files get here

Files in this directory are written by the **`fetch-sources` GitHub Actions workflow**. The workflow reads `sources-wishlist.txt` at the repo root and downloads each listed URL. It runs:

- On every push that changes `sources-wishlist.txt`.
- Weekly on Friday as a safety net (before Saturday's agent run).
- Manually via the GitHub Actions tab ("Run workflow").

If the workflow can't push directly because the autonomous PAT lacks `workflow` scope, see `bootstrap/README.md` for the one-time install.

You can also drop files in here directly with a commit — manual drops are equally valid input for the agent. The agent itself maintains the wishlist; it appends entries when it identifies a source it needs to read.

## Why this exists

The agent's container blocks outbound HTTP to most primary-source hosts (publishers, university PDF mirrors, archive.org). GitHub Actions has unrestricted internet, so it can fetch what the agent cannot. Anything in this directory is then in-repo and reachable.

## Filename convention

`AUTHOR-YEAR-shortname.ext` — e.g. `Chen-Yang-2019-pbl-meta-analysis.pdf`, `PBLWorks-2019-gold-standard-pbl.pdf`, `Dewey-1938-experience-and-education.pdf`. The verified `sources/...md` note records the original URL, access date, and (for PDFs) page count + whether text is selectable.

Don't rename a file after the agent has cited it; if you have to, move + leave a placeholder so cite chains don't break.

## Parsing rules

- The agent reads PDFs only if their text layer is selectable. Scanned-image PDFs without OCR get demoted to `leads/` with a note; the wishlist line should be replaced with an OCR'd mirror.
- HTML and plain text are read directly.
- For long books, prefer the relevant chapter as its own file (e.g. `Dewey-1938-experience-and-education-ch1.pdf`) so the repo stays modest in size.

## Non-negotiables

- **No fabrication.** Files that can't be parsed produce a recorded blocker, not a guess.
- **No paraphrase-as-evidence.** Every claim that enters `claim-evidence/` cites a verbatim quote plus a locator (page/section) from a file in this directory or from a verified online source.
