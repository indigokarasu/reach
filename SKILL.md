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
metadata:
  author: Indigo Karasu
  version: 3.5.0
---

# ocas-reach: Live World-Data Query Engine

Reach is the system's **sensory layer** for verified ground truth. It answers "what *is*" — not "what was," not "what should be," not "what might be." Each registered source is a deterministic connector: structured query in, structured response with citation out. No synthesis. No interpretation. Reach returns the fact; downstream skills synthesize.

## Trigger conditions

Use Reach when:
- The user asks about real-time external data with a known authoritative source (USGS, NOAA, FDA, FRED, Congress, Redfin, Open-Meteo, NASA, Wikidata, etc.)
- The user wants a factual lookup ("what's the current GDP figure," "any recent FDA recalls of <X>," "is 123 Main St for sale," "papers about transformers since 2022")
- The agent needs a citation-bearing fact to ground a downstream response
- The request is a specific entity, measurement, or list, not an open-ended exploration

Do not use Reach when:
- The task is open-ended research over many sources → use Sift
- The task is investigating a person → use Scout
- The task is detecting patterns in historical signals → use Corvus
- The request requires summarization or synthesis (Reach returns the fact; the agent or another skill does the writing)

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

## Source registry

The authoritative source list lives in [`scripts/sources.yml`](scripts/sources.yml). The browsable index is [`references/sources/index.md`](references/sources/index.md). Every source has:

- A slug (`<source>` argument)
- An auth declaration (`none` / `optional` / `required`) plus env var name (see `references/credential-files.md` for credential storage)
- An `account` flag (`null` / `optional` / `required`) plus signup URL
- Endpoint definitions per action
- Optional daily / monthly hard caps

Sources currently registered (48): see the [index](references/sources/index.md).

## Account-creation grant (explicit)

Reach is **explicitly authorized** to register accounts at any source whose `account` field in `sources.yml` is `required` or `optional`.

**Registration identity and procedure:** See `references/credential-files.md` for the OCAS persona details, and `references/account_provisioning.md` for the full registration playbook.

After registering, store the issued credential per `references/credential-files.md`, append a ledger entry, write an Action Journal, and notify the user once via the next briefing.

What Reach is **not** authorized to do: pay for paid tiers, use a different identity, accept ToS with arbitration waivers, register at sources outside `sources.yml`. See the playbook for the full constraints.

## Decision model

For each request:

1. **Identify the source**. Match the request to a registered source. If no source matches, refuse and suggest Sift.
2. **Validate auth**. Each source declares its env var. Missing required auth → return an explicit error (do not fall through to a different source silently).
3. **Check quota**. Daily / monthly caps are enforced from `usage.jsonl`. Exhausted quota → return `quota_exhausted` envelope; do not call.
4. **Build the query**. Translate natural-language input into the source's parameter shape (consult `references/sources/<source>.md`).
5. **Execute and capture**. Either generic dispatch (HTTP GET/POST per registry) or a custom Python module under `scripts/sources/` for sources with multi-step logic (SEC EDGAR, PubMed, Wikidata SPARQL).
6. **Log usage**. Append one row to `usage.jsonl` with source, action, status, http_status.
7. **Write Observation Journal**. One per query at `{agent_root}/commons/journals/ocas-reach/YYYY-MM-DD/{run_id}.json`.
8. **Return verbatim**. The structured JSON response goes back to the caller without paraphrasing.

## Execution loop

```
reach.query <source> <action> [params_json]
  → load registry from scripts/sources.yml
  → resolve auth from env (required → exit 1 with actionable msg if missing)
  → check daily/monthly quota from usage.jsonl
  → if source.custom: import scripts/sources/<custom>.py and call .query()
    else: generic HTTP dispatch per action's method/path/params_in
  → append usage.jsonl row
  → write Observation Journal
  → print JSON response, exit 0 on success / 1 on error / 2 on quota_blocked
```

## CLI surface

```bash
# List all registered sources
python3 scripts/reach.py sources

# Show one source's metadata + actions + current quota state
python3 scripts/reach.py source fred

# Show usage tally per source (all-time or for one month)
python3 scripts/reach.py usage
python3 scripts/reach.py usage --month 2026-04

# Run a query
python3 scripts/reach.py query <source> <action> '<params_json>'
```

## Adding a new source

1. Add the entry to `scripts/sources.yml`. Fields: `category`, `reference`, `auth`, `env_var`, `account`, `account_url`, `base_url`, `daily`, `monthly`, `rate`, `actions: { <action>: { method, path, params_in, defaults, auth_param/auth_header } }`. If multi-step, add `custom: <module>`.
2. Write `references/sources/<slug>.md` using `_template.md` as the skeleton; match the depth of the existing references.
3. Add a row to `references/sources/index.md` in the right table (no-key vs needs-key) and the routing-hints table when relevant.
4. If multi-step, write `scripts/sources/<slug>.py` exporting `query(action, params, auth) -> dict`.
5. Bump version (MINOR — new behavior). Update README + CHANGELOG entry.

## Existing sources (legacy)

`katzilla` and `property_lookup` predate the v3 registry but follow the same CLI shape. Their references live at `references/katzilla.md` and `references/property_lookup.md` (parallel to `references/sources/`). They will be migrated into the unified registry in a future minor version.

## Support file map

| File | When to read |
|------|-------------|
| `references/sources/index.md` | Before picking which source to use for a query; when checking routing hints |
| `references/sources/<slug>.md` | Before building a query for a specific source; when you need actions, params, response shape, or pitfalls |
| `references/account_provisioning.md` | Before registering at a source that requires an account; when creating API keys |
| `references/usage_tracking.md` | When checking quota status or usage counts; when debugging rate-limit issues |
| `references/source-evaluation-framework.md` | Before adding a new source to the registry; when evaluating candidate APIs |

## Recovery Behavior

This skill implements the recovery contract from `spec-ocas-recovery.md`.

- **Evidence**: Every query run writes an evidence record to `{agent_root}/commons/data/ocas-reach/evidence.jsonl`, including no-op runs. The `not_activity_reason` field is mandatory when no side effects occur.
- **Gap detection**: On every wake, checks the evidence log. If gap exceeds 24h for update cron, logs `gap_detected`.
- **Degraded mode**: When external APIs are unavailable, logs `degraded: <api>` and returns partial results with error envelope.
- **Log compaction**: Evidence and usage logs older than 30 days compacted. Last 7 days retained.

## Storage Layout

```
{agent_root}/commons/data/ocas-reach/
  config.json        — optional skill configuration (currently empty)
  usage.jsonl        — append-only call log; quota counts derive from this
  accounts.json      — account ledger (one entry per registered source)
  intents.jsonl      — append-only log of query intents (source, action, params, timestamp)
  evidence.jsonl     — append-only evidence log for recovery contract (all runs including no-ops)
{agent_root}/commons/journals/ocas-reach/
  YYYY-MM-DD/{run_id}.json   — Observation Journal per query (Action Journal for registrations)
```

No data is stored inside the skill package. The package is read-only at runtime.

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

## Pitfalls

- **Quota exhaustion is not the source's fault.** When a daily/monthly cap is hit, the orchestrator refuses the call before it leaves the host. Surface the `quota_exhausted` envelope as-is; suggest the user wait for the reset or upgrade the plan.
- **`User-Agent` matters.** SEC EDGAR, MediaWiki, NOAA, and Nominatim all enforce User-Agent rules. See `references/credential-files.md` for the User-Agent string and contact email.
- **Mock / demo modes are synthetic.** Some sources (Katzilla, Alpha Vantage's `DEMO_KEY`) offer free demo modes. Never use demo data as a real answer.
- **Rate-limit error responses still count toward usage.** A `429` response means the source got the call and rejected it; `usage.jsonl` records it. A `quota_blocked` (orchestrator-side) does NOT count against the source's cap because it never reached them.
- **Account creation is logged but the secret is never logged.** See `references/credential-files.md` for credential storage details.
- **Non-commercial sources.** `ip_api`, `themealdb`, and `thecocktaildb` are explicit non-commercial-only on the free tier. Don't use them in commercial-bearing user contexts.

## Ontology types

Reach does not extract entities or emit Signals to Chronicle. It is a query passthrough — entity extraction from returned data is the responsibility of the calling skill.

## OKRs

### schedule_adherence
- **Target**: `reach:update` cron runs within ±1h of scheduled time on ≥95% of days per month.
- **Measurement**: Compare wall-clock execution timestamps in `evidence.jsonl` against schedule (`0 0 * * *`). Runs outside the ±1h window are misses.

### data_integrity
- **Target**: Zero silent data loss events per month.
- **Measurement**: All query runs (including no-ops and errors) must have a corresponding entry in `evidence.jsonl` and `usage.jsonl`. Gaps detected during recovery audit are violations.

## Visibility

public
