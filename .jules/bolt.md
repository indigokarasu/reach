# Bolt's Journal - Critical Learnings

## 2026-05-28 - PyYAML C Extensions (CSafeLoader) Speedup
**Learning:** PyYAML's pure Python `safe_load` / `SafeLoader` can be slow on large YAML files (e.g. `scripts/sources.yml` at 1800+ lines parsing takes ~186ms). Using C-backed `CSafeLoader` (via `yaml.CSafeLoader` or `yaml.load(text, Loader=CSafeLoader)`) speeds up parsing by ~8x (~23ms), significantly reducing start-up CLI latency for orchestrator queries.
**Action:** Always prefer `CSafeLoader` over pure Python `SafeLoader` in Python CLI utilities that load large YAML configurations on every execution.
