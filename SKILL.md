---
name: ocas-reach
license: MIT
description: 'Live world-data query engine. Use when a request needs a verifiable real-time fact ("what is X now", "latest Y for Z"). Queries external APIs for factual ground truth — no synthesis, no opinion, no research. Routes requests through a registry of 60+ sources covering US government data, scholarly literature, weather and hazards, geocoding, finance and macro indicators, court records, nutrition, news events, property records, land due-diligence, academic papers, satellite imagery, and product manuals (3M+). NOT for web research (use Sift), entity investigations (use Scout), or pattern analysis over historical signals.'
source: https://github.com/<agent-handle>/reach
includes:
- references/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "3.13.0"
  hermes:
    category: data-science
    tags:
    - live-data
    - api
    - real-time
    - facts
    - OCAS-core
    config:
    - key: OCAS_AGENT_EMAIL
      description: Contact address sent in the outbound User-Agent (SEC EDGAR, Wikidata, NOAA and Nominatim refuse anonymous callers)
      default: agent@example.com
    - key: KZ_KEY
      description: Katzilla API key for the legacy `katzilla` source
      default: null
    - key: RT_KEY
      description: RealtyAPI key for the legacy `property_lookup` source
      default: null
tags:
- live-data
- API
- real-time
- facts
- research
triggers:
- live data query
- real-time API
- fact check
- current data
- external API query
---

# ocas-reach: Live World-Data Query Engine

Reach is the system's **sensory layer** for verified ground truth: it answers "what *is*." Each registered source is a deterministic connector — structured query in, structured response with citation out. No synthesis, no interpretation; downstream skills synthesize.

**Support files:** `references/support-file-map.md` indexes every bundled script and reference — check it before assuming a file is (not) available.

## When to Use

- The user asks about real-time external data with a known authoritative source (USGS, NOAA, FDA, FRED, Congress, Redfin, Open-Meteo, NASA, Wikidata, etc.)
- The user wants a factual lookup ("current GDP figure," "recent FDA recalls of <X>," "is 123 Main St for sale," "papers about transformers since 2022")
- The agent needs a citation-bearing fact to ground a downstream response
- The request is a specific entity, measurement, or list — not an open-ended exploration

For example, "any recent FDA recalls of peanut butter" → one FDA API query → the verbatim recall list with citations.

## When NOT to Use

- Open-ended research over many sources → Sift
- Investigating a person → Scout
- Detecting patterns in historical signals → query Chronicle directly
- Anything needing summarization or synthesis — Reach returns the fact, the caller writes

## Responsibility Boundary

Reach owns: external API calls, connector logic, the source registry, query/response logging, quota tracking, account ledger.

Not Reach: web research (Sift), person investigations (Scout), knowledge-graph queries, pattern analysis over journals, long-form synthesis or briefing (Vesper), inbox/messaging (Dispatch), quota accounting for APIs outside the registry (CSAPI quota lives in Sift's own `scripts/csapi_quota.py`).

A query needing synthesis after fetching is a two-step request: Reach returns the fact, the agent or downstream skill synthesizes.

## Optional Skill Cooperation

When present: **Vesper** may include Reach lookups in morning briefings; **Sift** may use Reach as one of many research sources; **Scout** may pull property records and SEC filings for contact enrichment; **Custodian** may check Reach quota state when triaging rate-limit issues. Reach works normally when none are present.

## Source Registry

`scripts/sources.yml` is authoritative — 60+ entries, each declaring action templates, `auth`, `env_var`, quotas, and an optional `custom` connector. Never hardcode a count: `python3 scripts/reach.py sources` prints the live registry.

Per-source keys are named by each entry's `env_var`; skill-level env vars live in this file's `metadata.hermes.config`. Two shared MCP surfaces are **not** registry entries — there is no `csapi` or `rapidapi` source, so `reach.py query csapi` and `query rapidapi` exit `Unknown source`; call their MCP tools directly until entries exist (`references/rapidapi.md`).

## Account Creation

Reach is authorized to register accounts where a source's `account` field is `required` or `optional`, using the OCAS persona — never the user's personal identity. Playbook: `references/account_provisioning.md`. Not authorized: paying for tiers, using a different identity, accepting arbitration waivers, registering outside `sources.yml` (why: a key obtained under the wrong identity or terms can be neither audited nor revoked cleanly).

## Pipeline

One query, eight steps, in order. Skipping a step to save a call burns a metered cap (no quota check) or hides the run from the recovery audit (no journal).

- [ ] **Identify source** — pick from the registry (`references/sources/index.md` has routing hints)
- [ ] **Validate auth** — `auth: required` needs its `env_var` set in the active profile's `.env`
- [ ] **Check quota** — daily/monthly caps are enforced *before* the call leaves the host
- [ ] **Build query** — action name + `params_json` as documented in `references/sources/<slug>.md`
- [ ] **Execute** — one call per action; no silent fall-through to another source
- [ ] **Log usage** — one `usage.jsonl` row per attempt (`references/usage_tracking.md`)
- [ ] **Write journal** — Observation Journal per run (`references/storage-layout.md`)
- [ ] **Return verbatim** — the source's response plus citation, unrewritten

```bash
python3 scripts/reach.py query weather brief '{"lat": 37.77, "lon": -122.42}'
python3 scripts/reach.py sources
python3 scripts/reach.py source alpha_vantage
```

Stdout is a JSON envelope; diagnostics go to stderr. Exit codes: `0` success · `1` source/auth/connector failure · `2` quota exhausted. `--help` prints usage.

## Defaults

When the request names no source, take the default rather than asking: weather → `weather`; geocoding → `nominatim` (`photon` for speed); scholarly → `openalex` then `crossref`; earthquakes → `usgs_earthquake`; US legislation → `congress_gov`; world news → `gdelt`; exchange rates → `exchangerate` (key required). Deviate only when the default lacks the data.

## Adding a New Source

Checklist: `references/source-evaluation-framework.md`. Template: `references/sources/_template.md`. Runtime workflow: `references/source-integration-workflow.md`. Discovery is not integration — a source the operator supplies ends up registered in `sources.yml` or fails explicitly.

## Legacy Sources

`katzilla` and `property_lookup` predate the v3 registry and keep their own scripts: `references/katzilla.md`, `references/property_lookup.md`.

## Routing and Ownership Rules

**Shared tools are general-purpose** — RapidAPI is a marketplace of hundreds of third-party APIs, not "local business search." When one skill uses a narrow slice of a shared tool, check the canonical definition before narrowing it for everyone (`references/rapidapi.md`).

**Live-verify auth before trusting the registry** — `sources.yml` lags reality; an endpoint can start requiring `access_key` while its entry says `auth: none`. One cheap probe settles it; on mismatch treat it as key-required until the entry is fixed.

**Immediate capture beats the safety net** — the api-mine cron only sees sessions still in the store, so write a discovery into `references/discovered-apis.md` when you find it.

Dated provenance: `references/gotchas.md` § Provenance.

## Support File Map

| File | When to read |
|------|-------------|
| `references/sources/index.md` | Picking a source for a query; routing hints and auth/quota columns |
| `references/sources/<slug>.md` | Building a query for one source — actions, params, response shape, pitfalls |
| `references/credential-files.md` | A key "is not found" — which `.env` the active profile loads; env_var naming |
| `references/account_provisioning.md` | Before registering at a source; when a call returns `auth_missing` |
| `references/source-integration-workflow.md` | Adding a source the operator supplied; connector vs generic template |
| `references/source-evaluation-framework.md` | Judging a candidate API before adding it to the registry |
| `references/usage_tracking.md` | Quota status, rate-limit debugging, archiving the usage log |
| `references/storage-layout.md` | Inspecting the on-disk data and journal directories |
| `references/gotchas.md` | Quota, User-Agent, demo-mode and non-commercial pitfalls; § Provenance |
| `references/api-mine-cron-notes.md` | Reading a "0 new APIs" api-mine result or a cron gap |
| `references/discovered-apis.md` | Proposing a new source; cataloging a discovery |
| `references/rapidapi.md` | Routing to RapidAPI or the other shared MCP surfaces |
| `references/support-file-map.md` | Complete inventory of bundled scripts and reference files |
| `references/okrs.md` | Reviewing OKR definitions or scoring performance |
| `references/katzilla.md`, `references/property_lookup.md` | Using the two legacy sources |
| `references/cultural-heritage-apis.md` | A cultural-heritage or museum source is requested |
| `references/plugin-eval-hermes-weather.md` | Before installing a weather plugin — does Reach cover it? |

Do not read the whole `references/` tree — take the row that matches the task.

## Recovery Behavior

Implements the recovery contract from `spec-ocas-recovery.md`.

- **Evidence**: every query run appends a row to `{agent_root}/commons/data/ocas-reach/evidence.jsonl`; refusals carry `not_activity_reason` because no call reached the source.
- **Gap detection**: a gap over 24h between rows logs `gap_detected` on wake; the in-skill cadence is the daily `reach:api-mine` cron.
- **Degraded mode**: an unavailable API logs `degraded: <api>` and returns the error envelope.
- **Compaction**: evidence and usage logs older than 30 days are compacted; the last 7 days are kept.

State lives outside the package (`references/storage-layout.md`); the package itself is read-only at runtime.

## Journal Outputs

Every `reach.query` run emits an **Observation Journal**; account registration emits an **Action Journal** (side effects: form submission, key storage). Payload: `source`, `action`, `params`, `outcome`, `result_meta` (extracted `meta` / `citation` / `quality` / `http_status` — never the bulk payload).

## Error Handling

Failures return a JSON envelope on stdout with `ok: false`, plus the matching journal entry and usage row.

| `error` | Handling |
|---|---|
| `invalid_request` | Wrong action, missing path param or malformed registry — fix against `references/sources/<name>.md`, then retry |
| `auth_missing` | `env_var` unset — set it in the **active profile's** `.env` (`references/credential-files.md`), or register (`references/account_provisioning.md`) |
| `quota_exhausted` | Daily/monthly cap hit, refused before the call left the host — wait for the reset, use another source, or surface the envelope as-is |
| `connector_missing` | Registry declares `custom:` but the module or one of its imports is absent — restore the connector, or drop `custom:` for generic dispatch |
| `http_error` / `network_error` / `source_error` | Upstream refused or failed after the call — follow `actionable_guidance` (back off on 429/5xx, verify the key on 401/403, check the path on 404) |

Exit codes: `1` for every `ok: false`, `2` for quota refusals. Never fall through to another source silently — the operator will not know which source actually answered. Full pitfall list: `references/gotchas.md`.

## Validation rules

A query is valid when `source` is registered, the action is supported, the required env var is present (or `auth: optional`), and the daily/monthly budget has room.

## Background tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `reach:api-mine` | cron | `0 4 * * *` | Scan sessions for sites with APIs → `references/discovered-apis.md` |

There is **no in-skill updater** — the fleet-wide `skills:update-fleet` cron owns skill updates (why: one fleet updater beats per-skill pullers that silently drift). Apart from api-mine, Reach is purely reactive to user/agent queries: no `reach:update` job, no first-run registration step.

## Source Discovery (reach:api-mine)

The cron scans **all** session transcripts for sites, services, databases, and archives used or needed by any skill. For each site:

- [ ] **Has an API?** — REST, GraphQL, or other programmatic access
- [ ] **Accessible?** — free/freemium/paid; key or signup required
- [ ] **Useful data?** — which endpoints, what can be searched or retrieved
- [ ] **Better than today?** — beats scraping, SearXNG or browser for the skill that found it

Catalog only a **confirmed working API** an active skill needs and that beats the current approach; deduplicate against `sources.yml` and `references/discovered-apis.md`. Not a general search index — only sites specific skills already use or need, where an API reduces friction.

**"0 new APIs" is the normal result**, and `[SILENT]` during cron-only periods is correct: the catalog is current, not broken. Details: `references/api-mine-cron-notes.md`.

## Gotchas

`references/gotchas.md`: quota exhaustion, User-Agent requirements, demo mode, rate-limit accounting, account creation, non-commercial sources, plugin-install traps.

## Ontology types

Reach extracts no entities and emits no Signals to Chronicle — entity extraction from returned data is the calling skill's job.

## OKRs

`references/okrs.md`.

## Visibility

public
