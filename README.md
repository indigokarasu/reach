# 🛰️ Reach

Reach is the system's live world-data query engine. It queries real-time external APIs for factual ground truth — no synthesis, no opinion, no research — and routes each request through a registry of ~37 sources covering US government, scholarly literature, weather and hazards, geocoding, finance, court records, nutrition, news events, and property data.

Skill packages follow the [agentskills.io](https://agentskills.io/specification) open standard
and are compatible with OpenClaw, Hermes Agent, and any agentskills.io-compliant client.

---

## Overview

Reach is the sensory layer of the OCAS suite. Where Sift researches and Corvus interprets, Reach simply *fetches*. A declarative registry at `scripts/sources.yml` lists every source with its endpoints, auth requirements, account-creation flag, and quota caps. The `reach.py` orchestrator dispatches each call (generic HTTP for simple GET-and-JSON sources; custom Python under `scripts/sources/` for multi-step ones like SEC EDGAR, PubMed, Wikidata SPARQL), enforces quotas from `usage.jsonl`, writes an Observation Journal, and returns the JSON response verbatim.

Every source has a reference doc at `references/sources/<slug>.md` describing what data it has, response shapes, and pitfalls. The browsable index lives at [`references/sources/index.md`](references/sources/index.md).

Reach is explicitly authorized to register accounts at any source whose `account` field is `required` or `optional`, using `mx.indigo.karasu@gmail.com`. The registration playbook is at [`references/account_provisioning.md`](references/account_provisioning.md).

## Commands

| Command | Description |
|---|---|
| `reach.query <source> <action> [params]` | Execute a query against a registered source |
| `reach.sources` | List all registered sources |
| `reach.source <name>` | Show one source's actions, auth, and quota state |
| `reach.usage [--month YYYY-MM]` | Tally calls per source (today, this month, all-time) |
| `reach.init` | First-run init — create data dirs, register cron |
| `reach.update` | Pull latest from GitHub source |

## Setup

`reach.init` runs automatically on first invocation. It creates `{agent_root}/commons/data/ocas-reach/` (`usage.jsonl`, `accounts.json`) and `{agent_root}/commons/journals/ocas-reach/`, and registers the `reach:update` cron job.

Per-source credentials live in `~/.hermes/.env`. The full env-var list is in [`references/sources/index.md`](references/sources/index.md). Without a required env var set, calls to that source return an explicit error — they do not fall through to a different source silently. Reach can self-register at sources whose registration is automatable; see the [account provisioning playbook](references/account_provisioning.md).

## Dependencies

**OCAS Skills**

- None required. Reach functions standalone.

**External (free tiers)**

- 26 no-key sources including Wikipedia, Wikidata, SEC EDGAR, OpenAlex, GDELT, Open-Meteo, NOAA, USGS Earthquake, Nominatim, Overpass, World Bank, CrossRef, PubMed, arXiv, Federal Register, USAspending, Open Library, REST Countries
- 11 key-required sources including FRED, NASA, Congress.gov, BLS, GovInfo, Alpha Vantage, Semantic Scholar, USDA FoodData, CourtListener, FEC, GeoNames

Full list with limits and account URLs in [`references/sources/index.md`](references/sources/index.md).

## Scheduled Tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `reach:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

## Changelog

### v3.0.0 — April 26, 2026
- Added unified source registry (`scripts/sources.yml`) covering 35 new sources across knowledge / government / science / weather / geo / finance / health / media categories
- Added `scripts/reach.py` orchestrator with generic HTTP dispatch, custom-module hooks, daily/monthly quota enforcement, journal emission
- Added custom Python modules for multi-step sources: `sec_edgar`, `pubmed`, `wikidata_sparql`
- Added `references/sources/index.md` (the authoritative source index) plus per-source reference files
- Added `references/account_provisioning.md` with explicit account-creation grant for `mx.indigo.karasu@gmail.com`
- Added `references/usage_tracking.md` describing the call log and quota model
- Storage layout updated: `usage.jsonl` and `accounts.json` replace earlier `queries.jsonl`
- `katzilla` and `property_lookup` retained as legacy connectors; will migrate into the unified registry in a future minor release

### v2.0.0 — April 26, 2026
- Restructured to OCAS architecture standard (`scripts/`, `references/`, OCAS-compliant SKILL.md sections)
- Removed hardcoded API key from source documentation; all auth via env var
- Added `property_lookup.py` connector script (was previously documented but unimplemented)
- Added Observation Journal emission and `queries.jsonl` query log
- Storage moved out of skill package to `{agent_root}/commons/data/ocas-reach/`
- Added README and CHANGELOG per spec-ocas-skill-publishing.md

### v1.0.0 — April 26, 2026
- Initial release as `sources/<source>/connector.py` layout with Katzilla integration

---

*Reach is part of the [OCAS Agent Suite](https://github.com/indigokarasu) — a collection of interconnected skills for personal intelligence, autonomous research, and continuous self-improvement. Each skill owns a narrow responsibility and communicates with others through structured signal files, shared journals, and Chronicle, a long-term knowledge graph that accumulates verified facts over time.*
