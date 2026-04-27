# Changelog

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
