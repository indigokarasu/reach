---
name: ocas-reach
description: >
  Reach: live world-data query engine. Queries real-time external APIs for
  factual ground truth — no synthesis, no opinion, no research. Routes
  requests to a registered source (US government data via Katzilla, real
  estate via Property Lookup), returns the structured response with
  citation and quality fields. Trigger phrases: 'what's happening with',
  'lookup property', 'current government data', 'check earthquakes',
  'congress bills', 'fda recall', 'find listing', 'reach query'. Do not
  use for web research (use Sift), entity investigations (use Scout), or
  pattern analysis over historical signals (use Corvus).
metadata:
  author: Indigo Karasu
  email: mx.indigo.karasu@gmail.com
  version: "2.0.0"
  hermes:
    tags: [world-data, government, property, realty, hazards, sources]
    category: signal
    cron:
      - name: "reach:update"
        schedule: "0 0 * * *"
        command: "reach.update"
  openclaw:
    skill_type: system
    visibility: public
  git_source: https://github.com/indigokarasu/reach
  skill_source: https://github.com/indigokarasu/reach/raw/main/SKILL.md
---

# ocas-reach: Live World-Data Query Engine

Reach is the system's **sensory layer** for verified ground truth. It answers "what *is*" — not "what was," not "what should be," not "what might be." Each registered data source is a deterministic connector script that takes a structured query and returns a structured response with source citation and quality scoring.

Reach does not synthesize, summarize, or interpret. The agent receiving Reach's output is responsible for any synthesis.

## Trigger conditions

Use Reach when:
- The user asks about real-time external data with a known authoritative source (USGS, NOAA, FDA, FRED, Congress, Redfin, Zillow, county assessor)
- The user wants a factual lookup ("what's the current GDP figure," "any recent FDA peanut recalls," "is 123 Main St for sale")
- The agent needs a citation-bearing fact to ground a downstream response
- The request is a specific entity or measurement, not an open-ended exploration

Do not use Reach when:
- The task is open-ended research over many sources → use Sift
- The task is investigating a person → use Scout
- The task is detecting patterns in historical signals → use Corvus
- The task is general web search with no authoritative source registered

## Responsibility Boundary

Reach owns: real-time external API calls, source-specific connector scripts, source registry, query/response logging.

Reach does not own:
- Web research over open content (Sift)
- Person investigations (Scout)
- Knowledge graph queries (Elephas)
- Pattern analysis over journals (Corvus)
- Long-form synthesis or briefing (Vesper)

A query that needs synthesis after fetching is a two-step request: Reach returns the fact, the agent or downstream skill synthesizes.

## Optional Skill Cooperation

When present:
- **Vesper** may include Reach lookups in morning briefings (e.g., overnight USGS earthquake summary).
- **Sift** may invoke Reach as one of many sources during deep research.
- **Scout** may invoke Reach for property records during contact-context enrichment.

Reach functions normally when none of these are present.

## Decision model

For each request:

1. **Identify the source**. Match the request to a registered source under `scripts/`. If no source matches, refuse and suggest Sift.
2. **Validate auth**. Each source requires a specific env var (see Sources below). If missing, return an explicit error — do not fall through to a different source silently.
3. **Build the query**. Translate the natural-language request into the source's structured parameter format.
4. **Execute and capture**. Call the connector. The response is JSON with `meta`, `data`, `citation`, and `quality` fields (Katzilla's contract; Property Lookup follows a similar pattern).
5. **Return verbatim**. Pass the structured result back to the caller without paraphrasing.
6. **Log + journal**. Append the query/result envelope to `queries.jsonl` and write an Observation Journal for the run.

## Execution loop

```
reach.query <source> <action> [params_json]
  → load config from {agent_root}/commons/data/ocas-reach/config.json
  → resolve source connector under scripts/<source>.py
  → exec connector with action + params, capture JSON
  → append query record to queries.jsonl
  → write Observation Journal
  → return JSON to caller
```

Mock mode (when supported by the source) is invoked the same way but flags `_mock: true`. Use mock mode for connector pattern testing only — never for production answers.

## Sources

### katzilla — US Government Data

Federated wrapper over 27 agencies (USGS, NOAA, FDA, CDC, FRED, SEC, FBI, Congress, etc.).

- **Connector:** `scripts/katzilla.py`
- **Auth:** `KZ_KEY` (in `~/.hermes/.env`)
- **Reference:** `references/katzilla.md`

Quick commands:
```bash
python3 scripts/katzilla.py agents
python3 scripts/katzilla.py query <agent> <action> '<params_json>'
python3 scripts/katzilla.py mock  <agent> <action> '<params_json>'
```

### property_lookup — Real Estate Data

RealtyAPI (Redfin + Zillow) with city/county assessor fallback for off-market properties.

- **Connector:** `scripts/property_lookup.py`
- **Auth:** `RT_KEY` (in `~/.hermes/.env`); SF assessor calls require no auth
- **Reference:** `references/property_lookup.md`

Quick commands:
```bash
python3 scripts/property_lookup.py autocomplete "<query>" [listingStatus]
python3 scripts/property_lookup.py details_by_address "<address>"
python3 scripts/property_lookup.py details_by_id <property_id> <listing_id>
python3 scripts/property_lookup.py zillow_by_address "<address>"
python3 scripts/property_lookup.py sf_assessor "<address fragment>"
```

## Adding a new source

1. Add a connector script at `scripts/<source>.py` following the Katzilla shape: read auth from env, accept `<action> [params_json]` on argv, write JSON to stdout, exit non-zero on error.
2. Add a reference at `references/<source>.md` covering endpoints, auth, response shape, and pitfalls.
3. Register the source in `{agent_root}/commons/data/ocas-reach/config.json` under `sources`.
4. Add a row to the **Sources** section of this SKILL.md.
5. Bump version (MINOR — new behavior) and update README + CHANGELOG.

## Support file map

| File | When to read |
|---|---|
| `references/katzilla.md` | Building a Katzilla query — agent handles, action names, response shape |
| `references/property_lookup.md` | Building a property query — endpoints, parameter names, fallback order |

## Storage Layout

```
{agent_root}/commons/data/ocas-reach/
  config.json         — source registry, default params, rate-limit notes
  queries.jsonl       — append-only query log (request + response envelope)
{agent_root}/commons/journals/ocas-reach/
  YYYY-MM-DD/{run_id}.json
```

No data is stored inside the skill package. The skill package is read-only at runtime.

## Journal Outputs

Every `reach.query` run emits an **Observation Journal** at `{agent_root}/commons/journals/ocas-reach/YYYY-MM-DD/{run_id}.json`.

Journal payload includes: `source`, `action`, `params`, `meta`, `citation`, `quality.confidence`, `quality.certainty_score`, and `outcome` (success / auth_missing / source_error / parse_error).

Reach never executes external side effects, so it does not emit Action Journals.

## Background tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `reach:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

`reach.init` registers `reach:update` on first invocation. No operational background tasks beyond self-update — Reach is purely reactive to user/agent queries.

## Validation rules

A query is valid when:
- `source` is registered in `config.json`
- The connector script exists at `scripts/<source>.py`
- Required env var is present
- `action` is supported by the source

Otherwise return an explicit error envelope (`{"error": "<reason>", "source": "<name>"}`) and write the failure to `queries.jsonl` with `outcome: <failure_type>`. Do not fall through to a different source silently.

## Pitfalls

- **`KZ_KEY`/`RT_KEY` not set** — connector fails immediately with an env-var message. Set in `~/.hermes/.env`, do not hardcode.
- **Mock mode is synthetic** — only use for connector-shape testing, never as a real answer.
- **Quality scores are advisory** — `quality.confidence` and `quality.certainty_score` come from the source. Pass them through; do not invent or modify.
- **Off-market properties** — Redfin returns `status: 404` in JSON body with HTTP 200. Treat the JSON body as authoritative, not the HTTP code.
- **Assessor data ≠ market value** — SF OpenData returns Prop 13 assessed values, useful for ownership and historical record but not for current market price.
- **No bot-blocked sources** — Zillow's browser surface is PerimeterX-protected; the API endpoint is the only viable path.

## Visibility

public
