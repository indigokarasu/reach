# Discovered APIs

APIs, data sources, and endpoints found during research sessions but **not yet integrated** into `sources.yml`. Maintained by the `reach:api-mine` cron job (daily 4am PT).

For fully integrated sources, see `references/sources/index.md`.

---

## Data Index

_Lookup by what data you need. Cross-references the main source index._

### Prediction Markets
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Election odds | Kalshi API | Polymarket Gamma API | Real-time market prices via REST |
| Economic indicators (prediction) | Kalshi API | — | GDP, unemployment, inflation odds |
| Political event odds | Kalshi API | Polymarket Gamma API | Congressional votes, leadership |
| Climate/weather thresholds | Kalshi API | — | Temperature, emissions targets |

### Finance & Economics
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Stock prices (real-time) | `yahoo_finance` (main index) | Alpaca API, Finnhub | Alpaca: brokerage + market data |
| Trading/brokerage | Alpaca API | — | Paper + live trading, crypto, options |
| Company fundamentals | Finnhub | `alpha_vantage` (main index) | Financials, earnings, estimates |
| Alternative data | Massive API | — | Consumer sentiment, web scraping |
| Crypto podcast sentiment | AudioAlpha | — | Narrative sentiment, market themes |

### People & Social
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Social profiles | `linkedin` (main index) | `reddit` (main index) | |
| Reverse image search | Yandex Images | Google Images | Via browser (Yandex) or residential IP (Google) |

### Geocoding & Places
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Places / local business | Google Places API | `photon` (main index) | Used by Styx, Taste, Sands for enrichment |
| Address geocoding | `photon` (main index) | `nominatim` (main index) | |

### Health & Nutrition
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Drug recalls | FDA open data | — | Not yet integrated |

### Archives & Newspapers
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Historic US newspapers | Chronicling America API | Newspapers.com (no API, subscription) | 23M+ pages, 1790-1963, free, no auth |
| Book metadata & search | Google Books API | OpenLibrary API | Both free; Google has better snippet previews |
| Book metadata (open) | OpenLibrary API | Google Books API | Internet Archive project, fully open data |

### Creative & Media
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Image generation | Pollinations.ai | — | Used by ocas-imagine |

### Models & ML
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| ML model search | Hugging Face Hub API | — | 100K+ models, datasets, metadata |
| Dataset discovery | Hugging Face Hub API | — | Filter by task, language, license |

### Web Search
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| General web search | SearXNG (main index) | Google CSAPI | CSAPI: programmatic Google search |
| API discovery | RapidAPI marketplace | `public_apis` (main index) | 203 endpoints across all categories |

### Banking & Transactions
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Bank transactions | Plaid API | — | Used by ocas-styx for financial sync |
| Account balances | Plaid API | — | Real-time balance checks |

---

## Registry

_Full details per API. Organized by category. Quality-ranked within each category._

### Prediction Markets

#### Kalshi Prediction Market API
- **Endpoint**: `https://api.elections.kalshi.com/trade-api/v2`
- **Data**: Real-time prediction market prices (0-1, representing implied probability) for economics, politics, climate, science/tech, financials, health events
- **Auth**: None required for public market data
- **Rate limits**: Not documented; reasonable use assumed
- **Quality**: Active markets with significant volume. Prices represent crowd-sourced probability estimates. USD-denominated contracts ($0-$1).
- **Discovered**: 2026-06-12 (bones:research cron via docs.kalshi.com)
- **Notes**: Old endpoint was `/v2/`, migrated to `/trade-api/v2/`. Frontend (kalshi.com/markets) is behind Vercel JS challenge — use API directly. Covers non-sports categories: Economics, Politics, Elections, Climate, Science/Tech, Financials, Health.
- **Source session**: `20260612_145529_92eac6`

#### Polymarket Gamma API
- **Endpoint**: `https://gamma-api.polymarket.com`
- **Data**: Prediction market data from Polymarket (election odds, political events, sports-adjacent markets)
- **Auth**: None for public data
- **Rate limits**: Not documented
- **Quality**: Large volume on election/politics markets. Gamma API is the newer REST interface (replaces older CLOB API).
- **Discovered**: 2026-06-12 (bones skill references)
- **Notes**: Used alongside Kalshi in ocas-bones for cross-platform prediction market analysis.
- **Source session**: `20260612_145529_92eac6`

### Finance & Economics

#### Alpaca Trading API
- **Endpoint**: `https://paper-api.alpaca.markets` (paper) / `https://api.alpaca.markets` (live)
- **Data**: Stock/crypto prices, fundamentals, options chain, order execution, portfolio management, account balances
- **Auth**: API key + secret (free tier available)
- **Rate limits**: 200 req/min (free tier)
- **Quality**: Well-documented, reliable, supports paper trading. Used by ocas-rally for trade execution.
- **Discovered**: 2026-06-05 (ocas-rally skill audit)
- **Notes**: Brokerage API — can place real trades. Paper trading environment available for testing. Also provides market data (IEX feed on free tier, SIP on paid).
- **Source session**: `20260605_235610_02d858`

#### Finnhub
- **Endpoint**: `https://finnhub.io/api/v1`
- **Data**: Company fundamentals, earnings estimates, financial statements, news sentiment, insider transactions, crypto prices
- **Auth**: API key (free tier: 60 req/min)
- **Rate limits**: 60 req/min (free), higher on paid tiers
- **Quality**: Good fundamentals data, used by ocas-rally for company analysis.
- **Discovered**: 2026-06-05 (ocas-rally skill audit)
- **Notes**: Free tier sufficient for research. WebSocket available for real-time prices.
- **Source session**: `20260605_235610_02d858`

#### Massive API
- **Endpoint**: `https://api.massivedata.io` (approximate — verify current URL)
- **Data**: Alternative data: consumer sentiment, web scraping results, ESG scores, patent filings
- **Auth**: API key (paid)
- **Rate limits**: Varies by tier
- **Quality**: Used by ocas-rally for alternative signal generation. Paid service.
- **Discovered**: 2026-06-05 (ocas-rally skill audit)
- **Notes**: Niche alternative data provider. Verify current endpoint and pricing before integration.
- **Source session**: `20260605_235610_02d858`

#### AudioAlpha
- **Endpoint**: Not publicly documented — requires API key
- **Data**: Crypto podcast narrative sentiment, market themes, trending topics in crypto media
- **Auth**: `AUDIOALPHA_API_KEY` (optional but recommended)
- **Rate limits**: Not documented
- **Quality**: Niche signal source for crypto market sentiment. Used by ocas-rally.
- **Discovered**: 2026-06-11 (ocas-rally Yahoo Finance fix session)
- **Notes**: Small/indie API. May have limited uptime. Treat as supplementary signal only.
- **Source session**: `20260611_231040_0f9966`

### Banking & Transactions

#### Plaid API
- **Endpoint**: `https://production.plaid.com` (production) / `https://sandbox.plaid.com` (sandbox)
- **Data**: Bank transactions, account balances, institution metadata, auth (routing/account numbers), identity verification
- **Auth**: Client ID + secret + public key (OAuth 2.0)
- **Rate limits**: Varies by tier; sandbox is generous
- **Quality**: Industry standard for financial data aggregation. Used by ocas-styx for daily transaction sync.
- **Discovered**: 2026-06-05 (ocas-styx skill audit)
- **Notes**: Requires Plaid account and app registration. Sandbox available for testing. Production requires compliance review. Covers 12,000+ financial institutions in US/Canada/EU.
- **Source session**: `20260605_235610_02d858`

### Geocoding & Places

#### Google Places API
- **Endpoint**: `https://maps.googleapis.com/maps/api/place`
- **Data**: Place search (text/nearby), place details, photos, reviews, opening hours, price level
- **Auth**: API key (Google Cloud Console)
- **Rate limits**: 100 req/sec (with billing enabled)
- **Quality**: Best-in-class place data. Used by ocas-styx (merchant enrichment), ocas-taste (restaurant discovery), ocas-sands (travel time).
- **Discovered**: 2026-06-05 (ocas-styx, ocas-taste, ocas-sands skill audits)
- **Notes**: Requires billing enabled on Google Cloud. Not a Reach-registered source — accessed via MCP or direct API calls from consuming skills.
- **Source session**: `20260605_235610_02d858`

### Creative & Media

#### Pollinations.ai
- **Endpoint**: `https://image.pollinations.ai/prompt/{encoded_prompt}`
- **Data**: AI-generated images from text prompts (Stable Diffusion-based)
- **Auth**: None for basic use; API key for higher rate limits
- **Rate limits**: Generous free tier; no key required for low-volume use
- **Quality**: Good for concept art and illustration. Used by ocas-imagine for image generation.
- **Discovered**: 2026-06-05 (ocas-imagine skill audit)
- **Notes**: Free tier is sufficient for most use cases. Image quality comparable to basic Stable Diffusion. No account required.
- **Source session**: `20260605_235610_02d858`

### Web Search

#### Google Custom Search API (CSAPI)
- **Endpoint**: `https://www.googleapis.com/customsearch/v1`
- **Data**: Programmatic Google search results (title, URL, snippet, paginated)
- **Auth**: API key + Custom Search Engine ID
- **Rate limits**: 100 queries/day free; 5000/day per $5 (paid)
- **Quality**: Google-quality results via API. Used by ocas-sift as fallback search tier.
- **Discovered**: 2026-06-12 (ocas-sift CSAPI quota management)
- **Notes**: Quota tracking managed by Reach (CSAPI quota). Free tier is limited (100/day). Requires Google Cloud billing for higher volumes.
- **Source session**: `20260612_145529_92eac6`

#### RapidAPI Marketplace
- **Endpoint**: `https://rapidapi.com/hub` (marketplace); individual API endpoints vary
- **Data**: 203+ APIs across finance, crypto, news, geo, weather, security, social, travel, etc.
- **Auth**: RapidAPI key (single key for all APIs); individual APIs may have additional auth
- **Rate limits**: Varies by API; RapidAPI free tier: 500 req/month total
- **Quality**: Mixed — marketplace aggregates many APIs of varying quality. Useful for discovery, not primary sourcing.
- **Discovered**: 2026-06-12 (RapidAPI skill review)
- **Notes**: General-purpose marketplace, NOT "local business search." The `rapidapi` skill is the canonical reference for all 203 endpoints. Use for discovery, then integrate best APIs individually into Reach.
- **Source session**: `20260612_145529_92eac6`

### Models & ML

#### Hugging Face Hub API
- **Endpoint**: `https://huggingface.co/api/` (REST API); also `huggingface_hub` Python library
- **Data**: Search and browse 100K+ ML models, datasets, and Spaces. Returns model metadata (downloads, tags, pipeline type, license), dataset metadata, file listings. Supports filtering by task, language, license, size.
- **Auth**: None for public data; HF token for private repos and higher rate limits
- **Rate limits**: Generous for public data; authenticated users get higher limits
- **Quality**: Largest ML model hub. Useful for finding models for specific tasks (image generation, text classification, etc.), checking model licenses, and discovering datasets.
- **Discovered**: 2026-06-19 (backpopulate scan — sessions reference huggingface.co for model/dataset discovery)
- **Notes**: Not a traditional "data source" but a meta-source for ML capabilities. Could be useful for ocas-imagine (finding image generation models), ocas-finch (finding models for self-improvement experiments), or any skill that needs to programmatically discover ML resources.
- **Source session**: `20260618_215154_7efa2e` (subagent sessions)

### Archives & Newspapers

#### Chronicling America API (Library of Congress)
- **Endpoint**: `https://www.loc.gov/collections/chronicling-america/` (base URL for JSON API queries)
- **Data**: 23+ million digitized historic US newspaper pages (1790-1963). Search by keyword, date range, state, newspaper title (LCCN), language. Returns OCR text, page images, issue metadata, newspaper title directory.
- **Auth**: None required
- **Rate limits**: Undocumented but reasonable; queries returning 100K+ results should be narrowed with facets. Add `&fo=json` for JSON format.
- **Quality**: Primary source for historical newspaper research. Complements Newspapers.com (which has later coverage but no API). Covers African American newspapers (Chicago Defender, Pittsburgh Courier, Baltimore Afro-American, etc.) that are critical for underrepresented subjects.
- **Discovered**: 2026-06-19 (util-wiki skill review — sessions search Chronicling America via browser when researching biographical subjects)
- **Notes**: Preferred over Newspapers.com for programmatic access because: (1) no API, (2) requires subscription, (3) browser-only access. Chronicling America covers the same titles for the 1790-1963 period. Beginning in 2025, Chronicling America is accessible exclusively via the loc.gov API.
- **Source session**: `20260615_180741_fc0c7ced` (util-wiki article research)

#### Google Books API
- **Endpoint**: `https://www.googleapis.com/books/v1/volumes`
- **Data**: Search books by author, title, ISBN, subject. Returns metadata (title, authors, publisher, date, description, page count), snippet previews, cover thumbnails, embeddable viewer links. Supports full-text snippet search within books.
- **Auth**: Google API key (free tier: 1,000 queries/day). No billing required for basic use.
- **Rate limits**: 1,000 queries/day (free); higher with billing
- **Quality**: Best-in-class book metadata and snippet previews. Used by ocas-sift as a source finder. More reliable than OpenLibrary for ISBN and edition data.
- **Discovered**: 2026-06-19 (util-wiki Phase 2 source verification — finding books by/about biographical subjects)
- **Notes**: Preferred over scraping Google Books web pages. The API returns structured metadata that can be used to verify publication details, find related editions, and check whether a book covers a specific subject.
- **Source session**: `20260615_180741_fc0c7ced` (util-wiki article research)

#### OpenLibrary API (Internet Archive)
- **Endpoint**: `https://openlibrary.org/search.json` (search); `https://openlibrary.org/works/{OLID}.json` (work details); `https://openlibrary.org/books/{ISBN}.json` (edition by ISBN)
- **Data**: Search books, authors, subjects. Returns work-level and edition-level metadata, author data, cover images, subject tags, reading logs. Data dumps available for bulk access.
- **Auth**: None for search/lookup. Optional account for higher rate limits.
- **Rate limits**: 1 req/sec (anonymous); 3 req/sec (identified with User-Agent + email header)
- **Quality**: Fully open data (CC0). Internet Archive project with strong coverage of older and public-domain works. Complements Google Books — when Google lacks a preview, OpenLibrary often has the full text.
- **Discovered**: 2026-06-19 (util-wiki source verification — cross-referencing book sources for biographical articles)
- **Notes**: Preferred over scraping. The search API supports structured queries (author, title, subject, ISBN) with faceted results. For Wikipedia editing, useful for verifying book citations and finding open-access full-text sources.
- **Source session**: `20260615_180741_fc0c7ced` (util-wiki article research)

---

## Quality Rankings

_Force-ranked within each data type. Only populated when 2+ discovered APIs compete._

### Prediction Market Data

| Rank | API | Why |
|------|-----|-----|
| 1 | Kalshi API | Free REST API, structured JSON, covers multiple categories, no auth required, active markets with volume |
| 2 | Polymarket Gamma API | Good for elections/politics, but narrower category coverage than Kalshi |

### Brokerage & Trading

| Rank | API | Why |
|------|-----|-----|
| 1 | Alpaca API | Full brokerage (paper + live), well-documented, free tier, supports stocks/crypto/options |
| 2 | Finnhub | Good for fundamentals/market data, but no trading capability |

### Financial Fundamentals

| Rank | API | Why |
|------|-----|-----|
| 1 | Finnhub | Free tier sufficient, comprehensive fundamentals, WebSocket for real-time |
| 2 | Massive API | Alternative/ESG data, but paid and niche |

### General Web Search

| Rank | API | Why |
|------|-----|-----|
| 1 | SearXNG (self-hosted, in main index) | Metasearch 70+ engines, no key, no CAPTCHA from VPS |
| 2 | Google CSAPI | Google-quality results, but 100/day free limit is restrictive |
| 3 | RapidAPI Marketplace | Useful for discovery, but mixed quality and 500 req/month free limit |

### Image Generation

| Rank | API | Why |
|------|-----|-----|
| 1 | Pollinations.ai | Free, no key required, good quality for concept art |

### Archives & Newspapers

| Rank | API | Why |
|------|-----|-----|
| 1 | Chronicling America API | Free, no auth, 23M+ pages, covers 1790-1963, preferred over Newspapers.com (no API) |
| 2 | Google Books API | Free tier sufficient, best snippet previews, structured metadata |
| 3 | OpenLibrary API | Fully open data, good for older/public-domain works, but lower rate limits |

---

## Recently Discovered

_Newest additions go here first. When fully categorized and indexed, move to Registry._

_All discovered APIs have been moved to the Registry above. This section will populate with new discoveries from future cron runs._
