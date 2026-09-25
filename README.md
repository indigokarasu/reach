# ⚙️ Reach

  <img src="./assets/readme/hero.jpg" width="100%" alt="Reach">

Live world-data query engine. Queries real-time external APIs for factual ground truth — no synthesis, no opinion, no research. Routes requests through a registry of 60+ sources covering US government data, scholarly literature, weather and hazards, geocoding, finance and macro indicators, court records, nutrition, news events, property records, land due-diligence, academic papers, satellite imagery, and product manuals (3M+). Do not use for web research (use Sift), entity investigations (use Scout), or pattern analysis over historical signals.

**Skill name:** `ocas-reach`
**Version:** 3.13.0
**Type:** Query engine (CLI + connectors)
**Layer:** data-science
**Author:** <agent-name>

---

## 📖 Overview

Each registered source is a deterministic connector: structured query in, structured response with citation out. The live registry lives in `scripts/sources.yml`; the count is whatever `python3 scripts/reach.py sources` prints, never a number hardcoded in docs.

An unkeyed call fails explicitly (`auth_missing`) or returns a body you must not mistake for data — `exchangerate`, for example, answers HTTP 200 with `success: false`. Check the envelope, not the status code.

---

## 🔧 Commands

```bash
python3 scripts/reach.py query weather brief '{"lat": 37.77, "lon": -122.42}'
python3 scripts/reach.py sources                  # live registry: auth, quota, reference per source
python3 scripts/reach.py source alpha_vantage     # one source's actions + quota state
python3 scripts/reach.py usage --month 2026-09    # calls / errors / quota blocks per source
python3 scripts/reach.py --help
```

Exit codes: `0` success · `1` source, auth or connector failure · `2` quota exhausted.

---

## 📊 Outputs

See `SKILL.md` for journal, evidence and persistence rules, and `references/storage-layout.md` for the on-disk tree.

---

## 🧪 Tests

```bash
python3 -m unittest discover -s tests -v     # offline contract tests
python3 -m py_compile scripts/*.py scripts/sources/*.py
```

Both run in CI (`.github/workflows/ci.yml`).

---

## 📄 Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition and operating rules |
| `references/` | Supporting documentation (indexed by `references/support-file-map.md`) |
| `scripts/` | Orchestrator CLI, registry, connectors |
| `tests/` | Offline contract tests |

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) — latest: 3.13.0 (broken connectors repaired, tests + CI added).

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.

---

## 📄 License

MIT License — see `LICENSE` for details.
