# 🛰️ Reach

Reach is the system's live world-data query engine. It queries real-time external APIs for factual ground truth — no synthesis, no opinion, no research — and routes each request to a registered source connector that returns a structured response with citation and quality fields.

Skill packages follow the [agentskills.io](https://agentskills.io/specification) open standard
and are compatible with OpenClaw, Hermes Agent, and any agentskills.io-compliant client.

---

## Overview

Reach is the sensory layer of the OCAS suite. Where Sift researches and Corvus interprets, Reach simply *fetches*. Each source — `katzilla` for US government data (USGS, NOAA, FDA, CDC, FRED, Congress, FBI, SEC) and `property_lookup` for real estate (Redfin/Zillow + city/county assessors) — is a self-contained connector script under `scripts/`. Queries are deterministic: structured input, structured output, citation always present. Every run writes an Observation Journal that downstream skills (Vesper, Scout, Sift) can consume.

## Commands

| Command | Description |
|---|---|
| `reach.query <source> <action> [params]` | Execute a query against a registered source |
| `reach.sources` | List registered sources and their status |
| `reach.init` | First-run initialization: write config, register `reach:update` cron |
| `reach.update` | Pull latest from GitHub source (preserves journals and data) |

## Setup

`reach.init` runs automatically on first invocation. It creates `{agent_root}/commons/data/ocas-reach/` with `config.json` and `queries.jsonl`, and registers the `reach:update` cron job. Per-source credentials are required:

- `KZ_KEY` — Katzilla API key, in `~/.hermes/.env`
- `RT_KEY` — RealtyAPI key, in `~/.hermes/.env`

SF assessor calls require no auth. Without the relevant env var set, calls to that source return an explicit error rather than falling through.

## Dependencies

**OCAS Skills**
- None required. Reach functions standalone.

**External**
- [Katzilla API](https://api.katzilla.dev) — required for the `katzilla` source
- [RealtyAPI](https://realtyapi.io) — required for the `property_lookup` Redfin/Zillow paths
- [SF OpenData (SODA)](https://data.sfgov.org) — optional fallback for `property_lookup`, no auth

## Scheduled Tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `reach:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

## Changelog

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
