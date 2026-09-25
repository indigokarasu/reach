# Support File Index

Complete inventory of every bundled file, so an agent never concludes a file or tool is missing. SKILL.md's table covers the files reached for most often; the rows below are the long tail. Read the row that matches your task — never read the whole tree.

| File | When to read |
|------|-------------|
| `references/sources/index.md` | Choosing a source for a query; checking auth/quota columns; adding a row for a new source |
| `references/sources/_template.md` | Authoring a new per-source reference file |
| `references/credential-files.md` | A key is "not found"; you need the User-Agent / contact-email rules |
| `references/account_provisioning.md` | Registering an account; handling an `auth_missing` envelope |
| `references/gotchas.md` | Before touching quotas, demo modes, non-commercial sources or plugins; § Provenance for why the routing rules exist |
| `references/usage_tracking.md` | Reading or archiving `usage.jsonl`; debugging rate-limit accounting |
| `references/storage-layout.md` | Locating the data / journal / ledger tree on disk |
| `references/okrs.md` | Reviewing how this skill's health is scored |
| `references/api-mine-cron-notes.md` | Interpreting a "0 new APIs" api-mine run or a cron gap |
| `references/discovered-apis.md` | Cataloging a discovery; proposing a new source |
| `references/source-integration-workflow.md` | Integrating a source the operator supplied |
| `references/source-evaluation-framework.md` | Judging whether a candidate API belongs in the registry |
| `references/rapidapi.md` | Routing to the RapidAPI MCP surface |
| `references/katzilla.md`, `references/property_lookup.md` | Using the two legacy sources and their own CLIs |
| `references/cultural-heritage-apis.md` | A museum or cultural-heritage source is requested |
| `references/plugin-eval-hermes-weather.md` | A weather plugin is proposed — check Reach's coverage before installing |
| `references/sources/<slug>.md` | Writing a query for one source — actions, params, response shape, pitfalls |
| `references/sources/{dahd_open_data,harvard_art_museums,metmuseum,tiza,walters_art}.md` | Candidate sources documented but **not registered** — read before proposing a museum / cultural-heritage source |
| `.jules/bolt.md` | Repo-automation notes (the PyYAML `CSafeLoader` finding); nothing reads it at runtime |
| `scripts/reach.py` | The orchestrator CLI: `query`, `sources`, `source`, `usage`, `--help` |
| `scripts/sources.yml` | The registry itself — entries, action templates, auth, quotas |
| `scripts/sources/_http.py` | Shared stdlib HTTP helper and `user_agent()` for connectors |
| `scripts/sources/_mcp_client.py` | Helper for MCP-backed connectors |
| `scripts/sources/<slug>.py` | The connector implementation behind one source's `custom:` field |
| `scripts/_load_yaml.py` | The minimal YAML loader `reach.py` imports (PyYAML-backed, import-safe) |
| `scripts/katzilla.py`, `scripts/property_lookup.py` | Legacy CLIs (`KZ_KEY` / `RT_KEY`) kept outside the v3 registry |
| `tests/test_reach.py` | Changing a script or a reference path — run `python3 -m unittest discover -s tests` before and after |
| `.github/workflows/ci.yml` | Changing CI: `py_compile` on every script plus the offline test suite |
| `SKILL.md` | The operating rules themselves |
| `CHANGELOG.md`, `README.md` | Release history and the public-facing description |
| `config.json`, `config.yaml`, `evals/evals.json` | Institutional stubs (custodian stamp, empty config, eval cases) — no runtime code reads them |
| `LICENSE`, `.gitignore`, `assets/readme/hero.jpg` | MIT license text, ignore rules, README banner image |
