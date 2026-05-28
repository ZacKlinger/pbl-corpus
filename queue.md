# Research queue

> ⚠️ **STRAWMAN — for Zack to edit before the first Saturday agent run.**
> Priorities and reading order below are a default. The agent will work from
> the top.

**Status (2026-05-27):** v0. Repo just scaffolded; no `sources/` notes yet. The first Saturday run should establish the steelman (KSC + HSDC, already in `learning-thesis`) and one anchor empirical source (Condliffe et al. as the most-cited synthesis) before doing anything else.

## Next up

1. **Read Condliffe et al. (2017) — MDRC literature review of PBL.** Top priority because it's the empirical synthesis most-cited in current PBL discourse, and because its central finding (implementation variation as the dominant moderator) is load-bearing for thread #1 in `thesis-seeds.md`. Add to `sources-wishlist.txt`.

2. **Read PBLWorks Gold Standard PBL framework (Larmer, Mergendoller & Boss, 2015 / updates).** Practitioner-layer anchor. Quote the design elements verbatim; record the framework as *aspirational*, not as a finding (per the framework-document caveat in `CLAUDE.md`).

3. **Read Kilpatrick (1918) "The Project Method."** Visionary-layer origin. Short enough to read in one session. The originating document for "project" as a pedagogical unit.

4. **Cross-link from `learning-thesis/sources/Kirschner-Sweller-Clark-2006-minimal-guidance.md`.** Do not duplicate; set up the first claim-evidence entry that pulls KSC from the sibling corpus per the cross-corpus rule in `canon-map.md`.

5. **Read Chen & Yang (2019) PBL meta-analysis.** Empirical-layer headline-effect source. Pair with critical reading: effect size, study quality, publication bias.

6. **Audit pass on this session's claims** (per protocol). Sample 2–3 of the first claims and re-verify quote + URL + locator. Becomes a standing item once threads exist.

## Standing items (every Saturday)

- **Audit pass: re-verify 2–3 random existing claims** in `claim-evidence/`.
- **Tension scan:** surface the most interesting complication from this week's reading.
- **Thesis-fit check:** quote a current line from `thesis-seeds.md` and ask whether the week's reading still supports it.
- **Wishlist maintenance:** when reading reveals a needed source, append a line to `sources-wishlist.txt`. Demote persistently-failing URLs to `leads/` and replace with a working mirror.
- **Source-fetch failure triage:** inspect new files in `sources-raw/` for the landing-page-masquerading-as-PDF problem. The workflow now has a MIME check, but the first runs may still surface edge cases.
- **`steers/` check:** if any files exist in `steers/`, read them first. They are course corrections Zack added between sessions.

## Backlog

- **Mehta & Fine (2019)** — *In Search of Deeper Learning.* The honest practitioner-empirical reckoning with how rare deeper learning actually is. Likely paywalled; record as a lead if no open chapter is found.
- **Hmelo-Silver, Duncan & Chinn (2007)** — already in `learning-thesis` wishlist. Pull when the KSC/HSDC tension needs to be staged in a claim-evidence entry here.
- **Lucas Education Research / Knowledge in Action papers (Saavedra et al., 2021).** AP Gov/Environmental Science RCTs. Open-access PDFs typically available from LucasEdResearch.org.
- **Lucas Education Research / Multiple Literacies in PBL (Krajcik et al., 2023).** Third-grade science RCT.
- **HQPBL Framework (2018 coalition document).** Practitioner layer. Short.
- **EL Education's *Leaders of Their Own Learning* (Berger et al., 2014).** Practitioner. Likely a lead until a chapter PDF is located.
- **High Tech High Center for Research on Equity and Innovation publications.** Practitioner case studies.
- **Hattie's PBL/PBL-adjacent effect sizes** — controversial; pull the underlying meta-analyses Hattie aggregates, not Hattie's table alone.
- **Boaler (2002) Railside studies.** Equity-focused implementation evidence for problem-based math.
- **Lemov (2010) *Teach Like a Champion.*** The strongest practitioner counter to PBL-as-default. Must enter before thread #1 ("PBL works at fidelity") can do heavy lifting.
- **Wiggins & McTighe (1998) *Understanding by Design.*** Visionary/practitioner hybrid; architecture under most PBL planning.
- **Bransford et al. (2000) *How People Learn* (NRC).** Visionary anchor for transfer + prior knowledge + metacognition claims.

## Backlog (deferred until canon is read)

- **Synthesis essay 1:** What does "high-fidelity PBL" mean operationally, and is the definition stable across PBLWorks, HQPBL, EL, NTN, and HTH? Draft only after frameworks + one empirical synthesis are read.
- **Synthesis essay 2:** Where does the empirical case for PBL overreach? Specifically: which named outcomes (transfer, deeper learning, agency) are robust as constructs, and which are doing rhetorical work? Draft only after Condliffe + at least one Lucas RCT + Mehta & Fine.
- **Synthesis essay 3 (product-relevant):** Given the implementation-fidelity moderator effect, what would a tool that genuinely lowered the fidelity bar look like? Distinguish from a tool that lowers the *visible* bar by automating away the deliberation that fidelity requires. Draft only after the implementation-account literature is read.

## Workflow-level items for Zack

- **`gh repo create` and initial push** required before the fetcher workflow runs. See `bootstrap/README.md`.
- **Schedule the routine** via the `/schedule` skill once the strawman direction docs above have been edited. The agent's first run should not execute on un-reviewed thesis seeds.
