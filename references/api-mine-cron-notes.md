# reach:api-mine Cron Notes

Operational observations from running the api-mine cron (daily 4am PT).

## Expected Behavior

### "0 new APIs" is the norm, not a failure

When the cron runs and finds zero new APIs, this is **expected and correct** behavior. It means:

1. All sites/services mentioned in recent sessions are already cataloged in `discovered-apis.md` or `sources.yml`
2. The catalog is up-to-date
3. No new skills or workflows have introduced uncataloged data sources

The cron is a **gap-detection** tool, not a continuous-discovery tool. It fires daily to catch anything missed, and most days it should find nothing.

### When it finds new APIs

The cron produces value when:
- A new skill is introduced that uses an uncataloged data source
- An existing skill starts using a new external service
- A session mentions a site with an API but the agent doesn't realize it (the cron's broader extraction pattern catches these)

## Session Retention Limitation

The session database (via `session_search`) only retains recent sessions (typically 48-72h of FTS5-indexed content). Implications:

- **API discoveries in old sessions are lost** — if a session mentioned an API but the session aged out before the cron ran, the discovery is gone
- **Mitigation**: Write API discoveries to `discovered-apis.md` immediately when found in a session, don't rely on the cron to catch them later
- The cron is a safety net, not the primary discovery mechanism

## Catalog Maturity (as of Jun 2026)

The `discovered-apis.md` catalog covers:
- Prediction markets (Kalshi, Polymarket)
- Finance (Alpaca, Finnhub, Massive, AudioAlpha)
- Banking/Transactions (Plaid)
- Places (Google Places)
- Creative (Pollinations.ai)
- Web Search (Google CSAPI, RapidAPI)
- Archives (Chronicling America, Google Books, OpenLibrary)

Plus 53 sources in `sources.yml`. Coverage is broad. New discoveries will be increasingly rare.

## Operational Checklist

After each cron run:
- [ ] Verify journal entry written to `api-mine-journal.jsonl`
- [ ] If new APIs found: verify they're added to `discovered-apis.md` with full details
- [ ] If 0 new APIs: confirm this is expected (catalog current) — no action needed
- [ ] If the cron didn't run (gap > 24h): check gateway status, the cron depends on the scheduler ticker
