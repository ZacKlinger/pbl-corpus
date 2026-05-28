#!/usr/bin/env python3
"""Extract the implicit graph from the resource bank and emit web/graph.json.

Nodes: claim-evidence threads, verified sources, leads, raw primary-source
       files awaiting processing.
Edges: thread -> source (supports / counters / frames), source <-> source
       (canon-map "Relates to"), thread -> lead.

Run at the end of each session as part of the index-build step. Re-runs are
idempotent: same inputs produce the same JSON.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    block = text[4:end]
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"')
    return meta


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", s.lower()).strip("-")


# --- Threads (slug -> short label shown in the graph) -----------------------
#
# Slugs are the canonical IDs. Each slug corresponds to a claim-evidence file
# (claim-evidence/<slug>.md) and to a heading in thesis-seeds.md.

SEED_TITLES = {
    "design-elements": "Design elements",
    "pedagogy-in-practice": "Pedagogy in practice",
    "assessment-and-rigor": "Assessment & rigor",
    "intellectual-lineage": "Intellectual lineage",
    "literature-findings": "Literature findings",
    "system-conditions": "System conditions",
}


def extract_seed_framings() -> dict[str, str]:
    """Pull each thread's framing paragraph from thesis-seeds.md, keyed by
    slug. The framing is the body under `### N. <Title>` until the next
    heading. Attached to the thread node so a click surfaces the conviction
    text without a separate seed node.
    """
    seeds = ROOT / "thesis-seeds.md"
    if not seeds.exists():
        return {}
    text = read(seeds)
    out: dict[str, str] = {}

    # Map each heading-text prefix to a slug. Match on the first few words
    # so light edits to the heading don't break the lookup.
    title_to_slug = {
        "The design elements": "design-elements",
        "PBL pedagogy in practice": "pedagogy-in-practice",
        "Assessment and rigor": "assessment-and-rigor",
        "The intellectual lineage": "intellectual-lineage",
        "What the literature describes": "literature-findings",
        "The system conditions": "system-conditions",
    }
    pattern = re.compile(r"^###\s+\d+\.\s+(.+?)\s*$", re.M)
    matches = list(pattern.finditer(text))
    for i, m in enumerate(matches):
        heading_title = m.group(1).strip()
        slug = None
        for needle, s in title_to_slug.items():
            if heading_title.startswith(needle):
                slug = s
                break
        if slug is None:
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        next_h2 = re.search(r"^##\s", text[start:end], re.M)
        if next_h2:
            end = start + next_h2.start()
        body = text[start:end].strip()
        if len(body) > 800:
            body = body[:800].rsplit(" ", 1)[0] + "…"
        out[slug] = body
    return out


def build_thread_nodes() -> list[dict]:
    framings = extract_seed_framings()
    nodes = []
    for f in sorted((ROOT / "claim-evidence").glob("*.md")):
        if f.name == "README.md":
            continue
        text = read(f)
        n_claims = sum(1 for line in text.splitlines() if line.startswith("## Claim"))
        stem = f.stem
        nodes.append(
            {
                "id": f"thread:{stem}",
                "label": SEED_TITLES.get(stem, stem.replace("-", " ")),
                "type": "thread",
                "layer": "thread",
                "claims": n_claims,
                "path": str(f.relative_to(ROOT)),
                "seed_framing": framings.get(stem, ""),
            }
        )
    return nodes


# --- Sources ----------------------------------------------------------------

_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)


def extract_section(text: str, heading: str, max_len: int = 600) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.M)
    m = pattern.search(text)
    if not m:
        return ""
    start = m.end()
    next_section = _SECTION_RE.search(text, start)
    end = next_section.start() if next_section else len(text)
    body = text[start:end].strip()
    if len(body) > max_len:
        body = body[:max_len].rsplit(" ", 1)[0] + "…"
    return body


def extract_quotes(text: str, max_n: int = 3) -> list[str]:
    pattern = re.compile(r"^##\s+Key quoted claims\s*$", re.M)
    m = pattern.search(text)
    if not m:
        return []
    start = m.end()
    next_section = _SECTION_RE.search(text, start)
    end = next_section.start() if next_section else len(text)
    body = text[start:end]
    quotes = []
    current: list[str] = []
    for line in body.splitlines():
        if line.startswith("- "):
            if current:
                quotes.append(" ".join(current).strip())
                current = []
                if len(quotes) >= max_n:
                    break
            current = [line[2:].strip()]
        elif line.strip().startswith("  ") and current:
            current.append(line.strip())
        elif not line.strip():
            continue
    if current and len(quotes) < max_n:
        quotes.append(" ".join(current).strip())
    return quotes[:max_n]


def build_source_nodes() -> tuple[list[dict], dict[str, str]]:
    nodes = []
    index: dict[str, str] = {}
    for f in sorted((ROOT / "sources").glob("*.md")):
        if f.name == "README.md":
            continue
        text = read(f)
        meta = parse_frontmatter(text)
        node_id = f"source:{f.stem}"
        nodes.append(
            {
                "id": node_id,
                "label": meta.get("authors", f.stem).split(",")[0].split(";")[0] + " " + meta.get("year", ""),
                "title": meta.get("title", ""),
                "type": "source",
                "layer": meta.get("layer", "?"),
                "year": meta.get("year", ""),
                "read_status": meta.get("read_status", ""),
                "path": str(f.relative_to(ROOT)),
                "thesis_excerpt": extract_section(text, "Thesis"),
                "quotes": extract_quotes(text),
            }
        )
        index[f.stem] = node_id
    return nodes, index


# --- Leads ------------------------------------------------------------------


def build_lead_nodes() -> list[dict]:
    nodes = []
    for f in sorted((ROOT / "leads").glob("*.md")):
        if f.name == "README.md":
            continue
        nodes.append(
            {
                "id": f"lead:{f.stem}",
                "label": f.stem.replace("-leads", "").replace("-", " ") + " (leads)",
                "type": "lead",
                "layer": "lead",
                "path": str(f.relative_to(ROOT)),
            }
        )
    return nodes


# --- Raw files awaiting processing -----------------------------------------


def build_raw_nodes(source_index: dict[str, str]) -> list[dict]:
    raw_dir = ROOT / "sources-raw"
    if not raw_dir.exists():
        return []
    nodes = []
    for f in sorted(raw_dir.iterdir()):
        if not f.is_file() or f.name == "README.md":
            continue
        stem = f.stem
        if stem in source_index:
            continue
        nodes.append(
            {
                "id": f"raw:{stem}",
                "label": stem.replace("-", " ") + " (raw)",
                "type": "raw",
                "layer": "raw",
                "path": f"sources-raw/{f.name}",
            }
        )
    return nodes


# --- Edges ------------------------------------------------------------------

SOURCE_LINK_RE = re.compile(r"\]\(\.\.\/sources\/([^)]+)\.md\)")


def build_thread_source_edges(source_index: dict[str, str]) -> list[dict]:
    """Walk each claim-evidence file, classify each link as supports vs counters
    by which section heading it lives under."""
    edges: list[dict] = []
    for f in sorted((ROOT / "claim-evidence").glob("*.md")):
        if f.name == "README.md":
            continue
        thread_id = f"thread:{f.stem}"
        section = None
        for line in read(f).splitlines():
            stripped = line.strip().lower()
            if stripped.startswith("### supporting evidence"):
                section = "supports"
            elif stripped.startswith("### counter-evidence"):
                section = "counters"
            elif stripped.startswith("### cross-listed"):
                section = "frames"
            elif stripped.startswith("###"):
                section = None
            if section is None:
                continue
            for m in SOURCE_LINK_RE.finditer(line):
                stem = m.group(1)
                src_id = source_index.get(stem)
                if src_id:
                    edges.append({"source": thread_id, "target": src_id, "kind": section})
    return edges


LEAD_LINK_RE = re.compile(r"`leads/([^`]+)\.md`|\]\(\.\.\/leads\/([^)]+)\.md\)")


def build_thread_lead_edges() -> list[dict]:
    edges = []
    for f in sorted((ROOT / "claim-evidence").glob("*.md")):
        if f.name == "README.md":
            continue
        thread_id = f"thread:{f.stem}"
        for m in LEAD_LINK_RE.finditer(read(f)):
            stem = m.group(1) or m.group(2)
            if (ROOT / "leads" / f"{stem}.md").exists():
                edges.append(
                    {"source": thread_id, "target": f"lead:{stem}", "kind": "tracked-in"}
                )
    for f in sorted((ROOT / "leads").glob("*.md")):
        if f.name == "README.md":
            continue
        thread_stem = f.stem.replace("-leads", "")
        if (ROOT / "claim-evidence" / f"{thread_stem}.md").exists():
            edges.append(
                {
                    "source": f"thread:{thread_stem}",
                    "target": f"lead:{f.stem}",
                    "kind": "tracked-in",
                }
            )
    seen = set()
    out = []
    for e in edges:
        k = (e["source"], e["target"], e["kind"])
        if k in seen:
            continue
        seen.add(k)
        out.append(e)
    return out


CANON_HEADING_RE = re.compile(r"^### \[([^\]]+)\] (.+)$")


def build_source_source_edges(source_index: dict[str, str]) -> list[dict]:
    """Extract Relates-to links from canon-map.md."""
    canon = ROOT / "canon-map.md"
    if not canon.exists():
        return []
    edges = []
    label_to_id: dict[str, str] = {}
    for stem in source_index:
        parts = stem.split("-")
        year_idx = next((i for i, p in enumerate(parts) if p.isdigit() and len(p) == 4), -1)
        if year_idx == -1:
            continue
        authors = parts[:year_idx]
        year = parts[year_idx]
        label_to_id[f"{' '.join(authors)} {year}"] = source_index[stem]
        label_to_id[f"{', '.join(authors)} ({year})"] = source_index[stem]
        label_to_id[f"{authors[-1]} {year}"] = source_index[stem]
        label_to_id[f"{authors[-1]} ({year})"] = source_index[stem]

    current_source_id: str | None = None
    for line in read(canon).splitlines():
        m = CANON_HEADING_RE.match(line)
        if m:
            heading = m.group(1) + " " + (m.group(2) or "")
            current_source_id = None
            for label, sid in label_to_id.items():
                if label in heading:
                    current_source_id = sid
                    break
            continue
        if current_source_id and line.strip().lower().startswith("- relates to:"):
            tail = line.split(":", 1)[1]
            for label, sid in label_to_id.items():
                if label in tail and sid != current_source_id:
                    edges.append(
                        {"source": current_source_id, "target": sid, "kind": "relates-to"}
                    )
    seen = set()
    out = []
    for e in edges:
        k = tuple(sorted([e["source"], e["target"]])) + (e["kind"],)
        if k in seen:
            continue
        seen.add(k)
        out.append(e)
    return out


def main() -> None:
    WEB.mkdir(exist_ok=True)

    thread_nodes = build_thread_nodes()
    source_nodes, source_index = build_source_nodes()
    lead_nodes = build_lead_nodes()
    raw_nodes = build_raw_nodes(source_index)

    edges = (
        build_thread_source_edges(source_index)
        + build_thread_lead_edges()
        + build_source_source_edges(source_index)
    )

    graph = {
        "nodes": thread_nodes + source_nodes + lead_nodes + raw_nodes,
        "edges": edges,
        "generated_at": os.popen("date -u +%Y-%m-%dT%H:%M:%SZ").read().strip(),
    }

    out = WEB / "graph.json"
    out.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {out}: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges"
    )


if __name__ == "__main__":
    main()
