# Changelog

## [3.0.0] - 2026-04-26

### Added
- Unified source registry at `scripts/sources.yml` declaring 35 new sources across knowledge / government / science / weather / geo / finance / health / media categories
- `scripts/reach.py` orchestrator: generic HTTP dispatch, custom-module hooks, per-source daily/monthly quota enforcement, journal emission, env-var auth resolution
- Custom Python modules for multi-step sources: `scripts/sources/sec_edgar.py`, `scripts/sources/pubmed.py`, `scripts/sources/wikidata_sparql.py`, plus shared `scripts/sources/_http.py`
- `references/sources/index.md` — authoritative source index with category, auth, account, quota, and routing-hints tables
- Per-source reference files at `references/sources/<slug>.md` (37 sources) covering data scope, endpoints, response shape, pitfalls
- `references/account_provisioning.md` with explicit account-creation grant authorizing Reach to register accounts at `account: required` and `account: optional` sources using `mx.indigo.karasu@gmail.com`
- `references/usage_tracking.md` documenting the `usage.jsonl` log and quota derivation
- New CLI subcommands: `reach.py sources`, `reach.py source <name>`, `reach.py usage [--month YYYY-MM]`
- `_template.md` skeleton for adding new source references

### Changed
- Storage: `queries.jsonl` replaced by `usage.jsonl` (call log) and `accounts.json` (account ledger)
- SKILL.md: added Source registry section, Account-creation grant section, expanded routing description, and an explicit list of what Reach is not authorized to do during registration
- Generic HTTP dispatch now handles auth via path/query/body/header insertion declared per-action in the registry
- README rewritten to describe the registry, cite the index, and list the new commands

### Removed
- The single-source `sources` field in SKILL.md (replaced by the registry pointer)

## [2.0.0] - 2026-04-26

### Changed
- Restructured to OCAS architecture standard: scripts moved from `sources/<source>/connector.py` to top-level `scripts/<source>.py`; per-source READMEs moved to `references/<source>.md`
- SKILL.md rewritten with required system-skill sections (Trigger conditions, Responsibility Boundary, Optional Skill Cooperation, Decision model, Execution loop, Storage Layout, Journal Outputs, Background tasks, Visibility)
- Storage moved out of the skill package to `{agent_root}/commons/data/ocas-reach/` per spec-ocas-storage-conventions.md
- Author email and version metadata added to SKILL.md frontmatter
- Update mechanism switched from `git source update` reference to `reach.update` cron job
- README description rewritten as routing-aware text, not branding copy

### Added
- `scripts/property_lookup.py` — first connector implementation for the Redfin/Zillow/SF-assessor lookup chain (previously only documented)
- Observation Journal emission for every query
- `queries.jsonl` append-only query log
- README.md and CHANGELOG.md per spec-ocas-skill-publishing.md
- `reach:update` daily self-update cron job

### Fixed
- Removed hardcoded `RT_KEY` value from SKILL.md and per-source documentation; all auth via `~/.hermes/.env`

### Removed
- `sources/` directory layout (non-standard, conflicted with OCAS scripts/references separation)

## [1.0.0] - 2026-04-26

### Added
- Initial release with `sources/katzilla/katzilla.py` connector for US government data
- Documentation stub for `sources/property-lookup/`
