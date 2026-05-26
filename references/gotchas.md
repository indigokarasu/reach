# Reach Gotchas

- **Quota exhaustion is not the source's fault.** When a daily/monthly cap is hit, the orchestrator refuses the call before it leaves the host. Surface the `quota_exhausted` envelope as-is; suggest the user wait for the reset or upgrade the plan.
- **`User-Agent` matters.** SEC EDGAR, MediaWiki, NOAA, and Nominatim all enforce User-Agent rules. See `references/credential-files.md` for the User-Agent string and contact email.
- **Mock / demo modes are synthetic.** Some sources (Katzilla, Alpha Vantage's `DEMO_KEY`) offer free demo modes. Never use demo data as a real answer.
- **Rate-limit error responses still count toward usage.** A `429` response means the source got the call and rejected it; `usage.jsonl` records it. A `quota_blocked` (orchestrator-side) does NOT count against the source's cap because it never reached them.
- **Account creation is logged but the secret is never logged.** See `references/credential-files.md` for credential storage details.
- **Non-commercial sources.** `ip_api`, `themealdb`, and `thecocktaildb` are explicit non-commercial-only on the free tier. Don't use them in commercial-bearing user contexts.
- **No silent fall-through.** When a source doesn't match or auth is missing, return an explicit error. Never silently redirect to a different source.
