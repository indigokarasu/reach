---
name: ocas-reach
description: 'Reach: live world-data query engine. Queries real-time external APIs
  for factual ground truth — no synthesis, no opinion, no research. Routes requests
  through a registry of ~48 registered sources covering US government data, scholarly
  literature, weather and hazards, geocoding, finance and macro indicators, court
  records, nutrition, news events, property records. Trigger phrases: ''what''s happening
  with'', ''lookup property'', ''current government data'', ''check earthquakes'',
  ''congress bills'', ''fda recall'', ''find listing'', ''reach query'', ''fred series'',
  ''recent papers about'', ''forecast for'', ''air quality at''. Do not use for web
  research (use Sift), entity investigations (use Scout), or pattern analysis over
  historical signals (use Corvus).

  '
license: MIT
source: https://github.com/indigokarasu/reach
includes:
  - references/**
  - scripts/**

metadata:
  author: Indigo Karasu
  version: 3.5.0
---

# ocas-reach: Live World-Data Query Engine

Reach is the system's **sensory layer** for verified ground truth. It answers "what *is*" — not "what was," not "what should be," not "what might be." Each registered source is a deterministic connector: structured query in, structured response with citation out. No synthesis. No interpretation. Reach returns the fact; downstream skills synthesize.

## When to Use

- The user asks about real-time external data with a known authoritative source (USGS, NOAA, FDA, FRED, Congress, Redfin, Open-Meteo, NASA, Wikidata, etc.)
- The user wants a factual lookup ("what's the current GDP figure," "any recent FDA recalls of <X>," "is 123 Main St for sale," "papers about transformers since 2022")
- The agent needs a citation-bearing fact to ground a downstream response
- The request is a specific entity, measurement, or list, not an open-ended exploration

## When NOT to Use

- Open-ended research over many sources → use Sift
- Investigating a person → use Scout
- Detecting patterns in historical signals → use Corvus
- Requests requiring summarization or synthesis (Reach returns the fact; the agent or another skill does the writing)

## Responsibility Boundary

Reach owns: real-time external API calls, source-specific connector logic, source registry, query/response logging, monthly quota tracking, account ledger.

Reach does not own:
- Web research over open content (Sift)
- Person investigations (Scout)
- Knowledge graph queries (Elephas)
- Pattern analysis over journals (Corvus)
- Long-form synthesis or briefing (Vesper)
- Inbox / messaging (Dispatch)

A query that needs synthesis after fetching is a two-step request: Reach returns the fact, the agent or downstream skill synthesizes.

## Optional Skill Cooperation

When present:
- **Vesper** may include Reach lookups in morning briefings (overnight USGS earthquake summary, weather, FRED indicator deltas).
- **Sift** may invoke Reach as one of many sources during deep research.
- **Scout** may invoke Reach for property records and SEC filings during contact enrichment.
- **Custodian** may verify a Reach quota state when triaging API rate-limit issues.

Reach functions normally when none of these are present.

## Source Registry

The authoritative source list lives in `scripts/sources.yml` (48 sources). Browsable index: `references/sources/index.md`. See `references/credential-files.md` for credential storage, `references/account_provisioning.md` for account registration.

## Account Creation

Reach is explicitly authorized to register accounts at sources requiring them. See `references/account_provisioning.md` for the registration playbook. Not authorized to: pay for tiers, use different identity, accept arbitration waivers, register outside `sources.yml`.

## Decision Model

8-step query pipeline: identify source → validate auth → check quota → build query → execute → log usage → write journal → return verbatim. No silent fall-through to alternative sources.

## Execution

CLI via `python3 scripts/reach.py`. See `references/sources/index.md` for command reference and `references/usage_tracking.md` for quota management.

## Adding a New Source

See `references/source-evaluation-framework.md` for the evaluation checklist and `references/sources/_template.md` for the source reference template.

## Legacy Sources

`katzilla` and `property_lookup` predate the v3 registry. References: `references/katzilla.md`, `references/property_lookup.md`.

## Support File Map

| File | When to read |
|------|-------------|
| `references/sources/index.md` | Before picking which source to use for a query; when checking routing hints |
| `references/sources/<slug>.md` | Before building a query for a specific source; when you need actions, params, response shape, or pitfalls |
| `references/account_provisioning.md` | Before registering at a source that requires an account; when creating API keys |
| `references/usage_tracking.md` | When checking quota status or usage counts; when debugging rate-limit issues |
| `references/source-evaluation-framework.md` | Before adding a new source to the registry; when evaluating candidate APIs |
| `references/storage-layout.md` | When inspecting or configuring the on-disk data and journal directories |
| `references/okrs.md` | When reviewing OKR definitions or scoring skill performance |

## Recovery Behavior

This skill implements the recovery contract from `spec-ocas-recovery.md`.

- **Evidence**: Every query run writes an evidence record to `{agent_root}/commons/data/ocas-reach/evidence.jsonl`, including no-op runs. The `not_activity_reason` field is mandatory when no side effects occur.
- **Gap detection**: On every wake, checks the evidence log. If gap exceeds 24h for update cron, logs `gap_detected`.
- **Degraded mode**: When external APIs are unavailable, logs `degraded: <api>` and returns partial results with error envelope.
- **Log compaction**: Evidence and usage logs older than 30 days compacted. Last 7 days retained.

## Storage Layout

See `references/storage-layout.md` for the full directory structure.

## Journal Outputs

Every `reach.query` run emits an **Observation Journal**. Account-registration runs (when Reach signs up at a new source) emit an **Action Journal** because side effects are involved (form submission, key storage).

Journal payload includes: `source`, `action`, `params`, `outcome` (`success` / `auth_missing` / `source_error` / `parse_error` / `quota_blocked`), and `result_meta` (extracted `meta` / `citation` / `quality` / `http_status` from the response — not the bulk payload).

## Background tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `reach:update` | cron | `0 0 * * *` | Self-update from GitHub source |

`reach.init` registers `reach:update` on first invocation. No operational background tasks beyond self-update — Reach is purely reactive to user/agent queries.

## Self-update

`reach.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

1. Read `source:` from frontmatter → extract `{owner}/{repo}` from URL
2. Read local version from SKILL.md frontmatter `metadata.version`
3. Fetch remote version from SKILL.md frontmatter: `gh api "repos/{owner}/{repo}/contents/SKILL.md" --jq '.content' | base64 -d | grep 'version:' | head -1 | sed 's/.*\"\(.*\)\".*/\1/'`
4. If remote version equals local version → stop silently
5. Download and install:
   ```bash
   TMPDIR=$(mktemp -d)
   gh api "repos/{owner}/{repo}/tarball/main" > "$TMPDIR/archive.tar.gz"
   mkdir "$TMPDIR/extracted"
   tar xzf "$TMPDIR/archive.tar.gz" -C "$TMPDIR/extracted" --strip-components=1
   cp -R "$TMPDIR/extracted/"* ./
   rm -rf "$TMPDIR"
   ```
6. On failure → retry once. If second attempt fails, report the error and stop.
7. Output exactly: `I updated Reach from version {old} to {new}`

## Validation rules

A query is valid when:
- `source` is registered in `sources.yml`
- The action is supported by the source
- Required env var is present (or `auth: optional`)
- The daily/monthly quota has remaining budget

Otherwise return an explicit error envelope and write the failure to `usage.jsonl` with the appropriate status. **Do not fall through to a different source silently** — the operator will not know which source actually answered.

## Gotchas

See `references/gotchas.md` for all operational pitfalls including quota exhaustion, User-Agent requirements, demo mode, rate-limit handling, account creation, non-commercial sources, and silent fall-through prevention.

## Ontology types

Reach does not extract entities or emit Signals to Chronicle. It is a query passthrough — entity extraction from returned data is the responsibility of the calling skill.

## OKRs

See `references/okrs.md`.

## Visibility

public
