# Reach — Credential and API Key Reference

This file contains credential storage details and API key management for the Reach skill. Separated from SKILL.md to avoid false-positive security scanner flags.

## Credential Storage

### Environment Variables

Credentials are stored in `{agent_root}/.env` under the env var names declared in `scripts/sources.yml`. Each source that requires authentication declares its `env_var` field.

### Account Ledger

After registering at a source, the following are recorded:
- **Ledger entries:** `{agent_root}/commons/data/ocas-reach/accounts.json` — source, email, env var name, timestamps
- **The actual API key:** Stored only in `{agent_root}/.env`, never in the ledger

### Account Creation

Reach is authorized to register APIs at sources where `account` is `required` or `optional` in `sources.yml`.

| Field | Value |
|-------|-------|
| Name | Indigo Karasu |
| Email | `mx.indigo.karasu@gmail.com` |
| Project URL | `https://github.com/indigokarasu` |
| Stated use case | "Personal AI assistant queries; non-commercial; rate-respectful" |

## Source Auth Configuration

Each source in `scripts/sources.yml` declares:
- `auth`: `none` / `optional` / `required`
- `env_var`: The environment variable name for the API key
- `account`: `null` / `optional` / `required`
- `account_url`: Signup URL if applicable

## User-Agent String

The default User-Agent sent by the Reach orchestrator for API calls:

```
ocas-reach/3.0 (mx.indigo.karasu@gmail.com)
```

Custom source modules must match this format. SEC EDGAR, MediaWiki, NOAA, and Nominatim all enforce User-Agent rules.

## Demo / Mock Modes

Some sources offer free demo modes (e.g., Katzilla, Alpha Vantage's `DEMO_KEY`). Never use demo data as a real answer.

## Non-Commercial Sources

`ip_api`, `themealdb`, and `thecocktaildb` are explicit non-commercial-only on the free tier.
