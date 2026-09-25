# exchangerate — ExchangeRate.host (Currency Exchange Rates)

## What this source has

ExchangeRate.host provides current and historical foreign exchange rates. Data includes:

- Latest exchange rates for 150+ currencies
- Historical rates by date
- Currency conversion
- Time-series data for date ranges

Use exchangerate for: currency conversion, historical exchange rate lookups, financial calculations involving multiple currencies, and complementing FRED's economic data with direct forex rates.

## Auth

| | |
|---|---|
| Required | `EXCHANGERATE_KEY` (query param `access_key`) |
| Account | required — free key from https://exchangerate.host/ |

**Live-verified:** an unkeyed call does NOT fail with an HTTP error — it returns **HTTP 200** with `{"success": false, "error": {"code": 101, "type": "missing_access_key"}}`. Any caller that only checks the HTTP status will read that body as success. Reach injects `access_key` automatically once the env var is set in the active profile's `.env`; until then the source fails explicitly with an `auth_missing` envelope.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | throttle to <1/sec |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `latest` | Latest exchange rates | none (optional: `base`, `symbols`) |
| `historical` | Rates for a specific date | `date` (YYYY-MM-DD) |
| `convert` | Convert between currencies | `from`, `to`, `amount` |
| `timeseries` | Rates over a date range | `start_date`, `end_date` |

## Worked examples

```bash
# Get latest rates (USD base)
python3 scripts/reach.py query exchangerate latest '{}'

# Get latest rates with specific base and symbols
python3 scripts/reach.py query exchangerate latest '{"base": "EUR", "symbols": "USD,GBP,JPY"}'

# Get historical rates for a date
python3 scripts/reach.py query exchangerate historical '{"date": "2024-01-01"}'

# Convert currency
python3 scripts/reach.py query exchangerate convert '{"from": "USD", "to": "EUR", "amount": 100}'

# Get time series
python3 scripts/reach.py query exchangerate timeseries '{"start_date": "2024-01-01", "end_date": "2024-01-31", "base": "USD", "symbols": "EUR,GBP"}'
```

## Response shape

**Latest** returns:
```json
{
  "motd": { "msg": "...", "url": "..." },
  "success": true,
  "base": "USD",
  "date": "2024-01-15",
  "rates": {
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 148.50
  }
}
```

**Historical** uses the date as path parameter: `/{date}`.

**Convert** returns:
```json
{
  "success": true,
  "query": { "from": "USD", "to": "EUR", "amount": 100 },
  "result": 92.00
}
```

## Pitfalls

- **A missing key looks like success.** HTTP 200 + `success: false` + `code 101 missing_access_key`. Check the body's `success` field, not just the status code.
- **Default base is USD.** Use the `base` parameter to change.
- **Historical dates must be weekdays.** Weekend/holiday rates may not be available (markets closed).
- **Rate data is from European Central Bank (ECB).** Updated daily around 4pm CET.
- **Complements Alpha Vantage.** Alpha Vantage has forex with a 25/day cap; this source has no documented daily cap once keyed.

## Source links

- API docs: https://exchangerate.host/#/
- GitHub: https://github.com/Formicka/exchangerate.host
