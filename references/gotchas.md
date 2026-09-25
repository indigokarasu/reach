# Reach Gotchas

- **Quota exhaustion is not the source's fault.** When a daily/monthly cap is hit, the orchestrator refuses the call before it leaves the host. Surface the `quota_exhausted` envelope as-is; suggest the user wait for the reset or upgrade the plan.
- **`User-Agent` matters.** SEC EDGAR, MediaWiki, NOAA, and Nominatim all enforce User-Agent rules. See `references/credential-files.md` for the User-Agent string and contact email.
- **Mock / demo modes are synthetic.** Some sources (Katzilla, Alpha Vantage's `DEMO_KEY`) offer free free demo modes. Never use demo data as a real answer.
- **Rate-limit error responses still count toward usage.** A `429` response means the source got the call and rejected it; `usage.jsonl` records it. A `quota_blocked` (orchestrator-side) does NOT count against the source's cap because it never reached them.
- **Account creation is logged but the secret is never logged.** See `references/credential-files.md` for credential storage details.
- **Non-commercial sources.** `ip_api`, `themealdb`, and `thecocktaildb` are explicit non-commercial-only on the free tier. Don't use them in commercial-bearing user contexts.
- **No silent fall-through.** When a source doesn't match or auth is missing, return an explicit error. Never silently redirect to a different source.
- **Check Reach before installing weather plugins.** Before installing any third-party weather plugin (e.g., hermes-weather-plugin), check whether ocas-reach already covers the needed data sources. `noaa_nws` handles US forecasts/alerts, `open_meteo` handles global weather, `usgs_earthquake` covers seismic events, `airnow` covers EPA air quality. If Reach already covers the required sources, prefer extending Reach over installing a heavy plugin — especially if the plugin depends on Rust/compiled binaries that may not be available on the host.
- **Check for Rust dependencies before installing plugins.** Some Hermes plugins (e.g., hermes-weather-plugin) have heavy Rust-backed features (model imagery, radar, ECAPE). Always run `which cargo rustc` first. If no Rust toolchain is present, those features silently fail at runtime. Either install Rust first (`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`) or limit the evaluation to the pure-Python features.
- **Hermes plugin install path.** Plugins are installed into the Hermes venv, not system Python. Use `<hermes-install>/venv/bin/pip3 install <package>` (not `pip`, not system `pip3`). Never use `--break-system-packages` on the Hermes host.
- **A registry `custom:` connector can be missing.** `acre_lens` and `metricduck` declare MCP connectors whose modules are not bundled in this package, so their queries fail with a `connector_missing` envelope. That is the intended failure mode — explicit, logged, and never a silent fall-through. Restore the connector module instead of retrying; do not drop the source from the registry just to make the error go away.
- **An unkeyed call can still look successful.** `exchangerate` returns HTTP 200 with `success: false` when the access key is missing. Read the body's `success`/`error` fields before treating a response as data.

## Provenance

Why the routing rules in SKILL.md exist. The rules are stated without dates so they outlive the incidents; the evidence stays here.

- **Shared tools are general-purpose** (Jun 12, 2026): one skill's narrow fallback ("Google Search Master Mega") was being treated as the definition of RapidAPI, which is a marketplace of hundreds of third-party APIs. Narrowing a shared tool for one skill silently removes capability from every other skill.
- **The Reach/Sift boundary** (Jun 12, 2026): Sift must not manage its own MCP connections or API quotas — Reach owns `sources.yml`, connectors, quota tracking and the discovery catalog; Sift owns synthesis, `web_search` and entity extraction.
- **Immediate capture beats the safety net** (Jun 18, 2026): the session store keeps roughly 48-72h of searchable content, so a discovery older than that window is invisible to the api-mine cron. Write it to `discovered-apis.md` when you find it.
- **Cron-only periods are not failures** (Jun 27, 2026): a 7-day window with 50+ cron sessions and 0 interactive sessions correctly produced `[SILENT]` from api-mine.
- **Live-verify auth** (Jul 24, 2026): `exchangerate` was declared `auth: none` while the endpoint already required an access key, and the failure arrived as HTTP 200 with `success: false` — the first symptom the agent saw was nonsense data, not an error. Probe before trusting the registry; fix the entry when the probe disagrees.
