---
name: ocas-reach
description: >
  Reach: live world-data query engine. Queries real-time external APIs for
  factual ground truth — no synthesis, no opinion, no research. Each data
  source lives under `sources/` with its own connector script and configuration.
metadata:
  author: Indigo Karasu
  version: "1.0.0"
  hermes:
    tags: [reach, world-data, sources, katzilla, property, realty, weather, market]
  git_source: https://github.com/indigokarasu/reach
  skill_source: https://github.com/indigokarasu/reach/raw/main/SKILL.md
---

# ocas-reach: Live World-Data Query Engine

Reach is the system's **sensory layer** — querying live, verified ground truth from external reality. Not research, not synthesis. You ask "what is" not "what was" or "what should be."

Each data source is a self-contained folder under `sources/` with its own connector script, API configuration, and operational notes.

## Trigger

- User asks about current government data (legislation, agencies, public records)
- User asks about property data (listings, ownership, valuations, sales history)
- User wants real-time live data from any configured source
- "What's happening with [entity]?" where the answer is a verified fact

## Pattern

```
reach → sources/<source>/ → live API → factual return
```

No opinion, no synthesis, no web search. Structured query → live data → structured output.

## Available Sources

### katzilla — US Government Data

Federated API wrapping 27 agencies, 217 actions covering hazards, economics, health, crime, government, and more.

**Connector:** `sources/katzilla/katzilla.py`

**Authentication:** Requires `KZ_KEY` env var (API key)

**Commands:**
```bash
# List all available agents
python3 sources/katzilla/katzilla.py agents

# Execute an action on an agent
python3 sources/katzilla/katzilla.py query <agent> <action> [json_params]

# Mock mode (free, no upstream hit)
python3 sources/katzilla/katzilla.py mock <agent> <action> [json_params]
```

**Known agents & actions:**
- `hazards` → `usgs-earthquakes`, `usgs-volcanoes`, `noaa-weather`
- `health` → `fda-recalls`, `cdc-diseases`
- `government` → `congress-bills`, `congress-members`, `white-house`
- `economic` → `fred-gdp`, `fred-inflation`, `sec-filings`
- `crime` → `fbi-wanted`, `fbi-ucr`

**Usage examples:**
```bash
# Check recent earthquakes (magnitude 5+)
python3 sources/katzilla/katzilla.py query hazards usgs-earthquakes '{"minMagnitude":5,"limit":3}'

# Search congress bills about climate
python3 sources/katzilla/katzilla.py query government congress-bills '{"query":"climate","limit":3}'

# FDA recalls for peanut products
python3 sources/katzilla/katzilla.py query health fda-recalls '{"search":"peanut","limit":5}'

# GDP data
python3 sources/katzilla/katzilla.py query economic fred-gdp '{"limit":5}'
```

**API spec:**
- Base: `https://api.katzilla.dev`
- Auth: `X-API-Key` header
- All queries return `meta`, `data`, `citation`, and `quality` fields
- Mock mode (`_mock: true`) is free on every plan

**Quality scoring:** Results include `quality.confidence` and `quality.certainty_score` (0-100). Use these to determine trust level. Source citation is always provided.

**Pitfalls:**
- `KZ_KEY` must be set in `~/.hermes/.env` — without it, all calls fail immediately
- Mock mode returns synthetic data — only use for testing the connector pattern
- Some agents have rate limits — check meta.creditsCharged to track usage

### property-lookup — Real Estate Data

Aggregates property data from RealtyAPI (Redfin/Zillow) with fallback to city/county assessor public records for off-market properties.

**Connectors:** `sources/property-lookup/` (direct API calls)

**RealtyAPI key:** `rt_KK5cq8SGBr3PlZXPFQP1a3SQ`

**Step 1: RealtyAPI (Redfin)**
- Base: `https://redfin.realtyapi.io`
- `GET /autocomplete` — requires `listingStatus` param (e.g. `"For_Sale"` or `"For_Sale_or_Sold"`)
- `GET /detailsbyaddress` — param: `property_address`
- `GET /detailsbyid` — needs property_id + listing_id
- `GET /byaddress` — param: `propertyaddress`
- `GET /search/byaddress` — paginated

**Step 2: RealtyAPI (Zillow)**
- Base: `https://zillow.realtyapi.io`
- `GET /client/byaddress` — param: `propertyaddress`
- `GET /byaddress` — param: `propertyaddress`

**Step 3: City/County Assessor (Fallback)**
- SF OpenData SODA API: `https://data.sfgov.org/resource/wv5m-vpq2.json`
- Query with `$where` property_location like pattern
- Returns assessed values (Prop 13 capped), not market values

**Usage flow:**
1. Try Redfin autocomplete → get property_id + listing_id
2. Use detailsbyid for full data
3. If off-market, try Zillow /byaddress
4. If still no luck, try city/county assessor
5. For comparables, search nearby properties in assessor data

**Pitfalls:**
- Redfin autocomplete returns `hasFakeResults: true` for addresses without dedicated pages
- `detailsByAddress` returns 404 in JSON body (200 HTTP) for off-market properties
- Zillow browser access blocked by bot detection — stick to API
- `realtor.realtyapi.io` and `api.realtyapi.io` don't resolve (DNS failures)
- Assessor data uses Prop 13 assessed values, NOT market values

## Adding New Sources

Create a new folder under `sources/`:
```
sources/<source_name>/
  ├── connector.py        # Script to query the API
  ├── README.md          # Agent/user guide for this source
  └── config.json        # API credentials, endpoints, rate limits (optional)
```

Then document it in this SKILL.md's Available Sources section.

Sources share the common Reach pattern: structured query → live API → factual return. No synthesis, no opinion.

## Updating This Skill

```
git_source: https://github.com/indigokarasu/reach
```

If the remote version differs, fetch via `git source update reach` or pull from GitHub. Always use the latest version — local edits are overwritten on update.
