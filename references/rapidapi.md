# RapidAPI

MCP multiplexer that provides access to hundreds of RapidAPI-hosted APIs through a single connection. The host registry (below) is the live list — treat any count quoted in older notes as a snapshot, not a fact.

## Endpoint

`rapidapi` (MCP stdio server at `<hermes-home>/scripts/rapidapi-mcp-server.py`)

## Auth

RapidAPI key (configured in the MCP server). No per-API auth needed — the key covers all RapidAPI-hosted APIs.

## Registry

Available APIs: the **host-side** registry at `<hermes-home>/scripts/references/rapidapi-hosts-registry.json` — a host file, not bundled in this skill package. Read it for the live host list instead of trusting a count here.

Key categories:
- **Finance**: alpha-vantage, yahoo-finance, polygon, finnhub, tiingo, eodhistoricaldata, marketstack, intrinio, financialmodelingprep
- **Crypto**: coingecko, coinranking, coincap, coinlore, coinpaprika, crypto-compare, binance, kraken, coinbase
- **News**: newsapi, newsdata, currentsapi, mediastack, bing-news, google-news, nytimes, guardian, bbc, associated-press
- **Social**: reddit, twitter, linkedin, youtube, instagram, tiktok, pinterest, facebook, telegram, discord, twitch
- **Geocoding**: ipgeo, ip-api, ipinfo, ip2location, geocode, opencage, positionstack, bigdatacloud, geoapify, mapbox, here, tomtom
- **Weather**: weather, weatherbit, openweather, weatherapi, weatherstack, stormglass, worldweather
- **Travel**: booking, airbnb, tripadvisor, skyscanner, flightradar, aviationstack
- **Security**: haveibeenpwned, virustotal, abuseipdb, greynoise, shodan, phishtank, google-safe-browsing, wot, ssl, crtsh
- **Other**: openlibrary, imdb, tmdb, spotify, shazam, genius, booking, stripe, paypal, amazon, ebay, shopify

## Usage

Via MCP tool `mcp_rapidapi_rapidapi_call`:
```
mcp_rapidapi_rapidapi_call(
  api="<api-name>",      # e.g., "google-search-master-mega"
  action="<action>",      # e.g., "_Places", "_Search"
  params={...}            # API-specific params
)
```

## Rate Limits

Varies per underlying API. Most RapidAPI free tiers are 100-500 calls/day. The MCP server handles rate limiting per-host.

## Notes

- The MCP server discovers available endpoints from config.yaml at runtime
- Semantic index (host-side, not bundled): `<hermes-home>/scripts/references/rapidapi-semantic-index.json`
- To reindex: run `python3 scripts/rapidapi-reindex.py` on the host
- The old `google-search-master-mega` Sift fallback should now route through this source

**Why this is general-purpose**: RapidAPI is a marketplace of hundreds of third-party APIs, NOT "local business search." A skill that uses one narrow slice (Sift's old Google Search fallback) must not define the tool for every other skill — on a shared tool, check the canonical definition before narrowing it.