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
| Tech/news social feed | Hacker News API | `reddit` (main index) | Top/New/Best stories, comments, users; Firebase JSON, no auth |
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
| Album cover art | Cover Art Archive API | — | Peer-reviewed, CC0 metadata, no auth, no rate limit. Pairs with MusicBrainz (below) |

### Music & Audio
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Music metadata / identifiers | MusicBrainz API | — | MBID backbone; ~1 req/sec, descriptive UA required |
| Album cover art | Cover Art Archive API | — | Returns the picture MusicBrainz's MBID points at |

### Standards & RFC
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Internet standards / RFCs | IETF Datatracker API | — | 157K+ documents, drafts, groups, meetings; no auth |
| IETF working groups | IETF Datatracker API | — | WG charters, chairs, milestones |
| IETF meetings / agendas | IETF Datatracker API | — | Meeting materials, proceedings |

### Creative & Media
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Image generation | Pollinations.ai | — | Used by ocas-imagine |

### Museums & Cultural Heritage
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Museum open-data source discovery | Digital Art History Directory — Open Data Collections | `public_apis`, web search | Curated list of art/museum open datasets and APIs; WordPress JSON accessible |
| Metropolitan Museum of Art collections | The Met Collection API | Met Open Access CSV | 470k+ object records + public-domain images; no auth; CC0 dataset |
| Harvard Art Museums collections | Harvard Art Museums API | IIIF manifests | Object/person/exhibition/publication/gallery metadata + images; key required; non-commercial |
| Walters Art Museum collections | Walters static collections data | Online Collection / future API v2 | 10k+ object records + media CSVs; v1 API closed; CC0; static GitHub data now |

### Models & ML
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| ML model search | Hugging Face Hub API | — | 100K+ models, datasets, metadata |
| Dataset discovery | Hugging Face Hub API | — | Filter by task, language, license |

### Web Search
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| General web search | SearXNG (main index) | Google CSAPI | CSAPI: programmatic Google search |
| API discovery | RapidAPI marketplace | `public_apis` (main index) | hundreds of hosts across all categories |
| Product manuals | `manualslib` (main index) | ManualZZ (mirror) | 3M+ manuals, 140K+ brands. Vue.js SPA, direct access blocked. Wayback CDX + image OCR. |
| WordPress venue calendars | The Events Calendar (Tribe) REST v1 | — | Plugin surface: `/wp-json/tribe/events/v1/events` on any WP install running it. No auth. Real ISO datetimes, `cost`, `categories`, nested `venue`. |
| WordPress venue roster + addresses | Tribe v1 `/venues` | — | Plugin surface: `/wp-json/tribe/events/v1/venues`. Carries street `address`, `city`, `stateprovince`, `zip`, `phone`, `website`. Core `wp/v2/tribe_venue` CPT does NOT. |
| WordPress content enumeration | WordPress core REST (`/wp-json/wp/v2/`) | — | Platform surface: `/wp-json/wp/v2/types` lists every CPT + `rest_base` in one call — the cheapest way to find a site's event post type. No auth. |
| Shopify storefront catalogue | Shopify `products.json` | — | Platform surface: `/products.json` and `/collections/<handle>/products.json`, no key. Title + price + availability; date only in `body_html`. |

### Web Data Extraction
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| JS-rendered page content + unblocking | Zyte API | donsetch, sift.webwright | Paid API (usage-based); unblocking, browser rendering, auto-extraction (Product, Article, jobPosting, SERP). Not yet evaluated. |

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

### Museums & Cultural Heritage

#### Digital Art History Directory — Open Data Collections
- **Endpoint**: `https://dahd.hcommons.org/open-data-collections/`
- **Machine-readable endpoint**: `https://dahd.hcommons.org/wp-json/wp/v2/pages?slug=open-data-collections`
- **Data**: Curated directory of open digital art history / museum collection datasets and APIs. Entries currently include Artsy Art Genome Project, Art Institute of Chicago API, Biodiversity Heritage Library, Carnegie Museum of Art dataset, Cleveland Museum of Art Open Access API, Getty Vocabularies LOD, Harvard Art Museums API, Library of Congress Prints & Photographs API, Smithsonian American Art Museum LOD/SPARQL, Met Collection API + CSV, MoMA datasets, National Gallery of Art open data, Nationalmuseum Sweden Wikidata collection, Cooper Hewitt open data/API, Tate dataset, Wikidata Sum of All Paintings, Yale Center for British Art IIIF resources.
- **Auth**: None for the WordPress JSON endpoint.
- **Rate limits**: Not documented; treat as low-volume source-discovery endpoint.
- **Quality**: Curated domain-specific source directory from the Digital Art History Directory / Art Libraries Society of North America context. Useful for discovering candidate Reach sources, not for answering object-level factual queries directly.
- **Cost/terms**: Open web page; individual linked datasets have their own licenses/terms.
- **Discovered**: 2026-07-11 (<operator> suggested DAHD Open Data Collections as an ocas-reach source)
- **Verified**: Browser-like page request redirects through HCommons silent login with HTTP 202, but WordPress REST API returns the published page JSON without login. Extracted 26 links from the page content.
- **Notes**: Register, if integrated, as a `source_directory` / discovery source rather than a primary factual source. Initial Reach actions should be `list_sources` (parse page content into name, URL, description), `get_source` by normalized name, and maybe `refresh_catalog`. Deduplicate against `sources.yml` and this discovered catalog before adding linked APIs. Do not treat directory summaries as authoritative for the linked API's current terms; verify each linked source directly before integration.
- **Source session**: current

#### The Metropolitan Museum of Art Collection API
- **Endpoint**: `https://collectionapi.metmuseum.org/public/collection/v1`
- **Docs**: `https://metmuseum.github.io/`; GitHub/Open Access page: `https://github.com/metmuseum/openaccess`
- **Data**: Open Access metadata for 470,000+ artworks in The Met collection plus high-resolution public-domain JPEGs where available. Endpoints cover all object IDs, single object records, departments, and search. Object records include accession data, public-domain/image flags and URLs, constituents/artist metadata, department, title, culture/period/dynasty, dates, medium, dimensions/measurements, credit line, geography fields, classification, rights, metadata date, repository, object URL, tags with AAT/Wikidata links, object Wikidata URL, Timeline flag, and gallery number.
- **Auth**: None. No API key or registration required.
- **Rate limits**: 80 requests/second. No documented daily/monthly cap.
- **Quality**: Primary source maintained by The Metropolitan Museum of Art; REST JSON API; unrestricted Open Access dataset; direct public-domain image URLs. Stronger immediate Reach candidate than Harvard because no key is needed and commercial/noncommercial use is allowed under CC0 where applicable.
- **Cost/terms**: Free. The Met states it has waived copyright/neighboring rights to the selected dataset using Creative Commons Zero to the extent possible under law; API use remains subject to The Met terms and conditions. Images returned are high-resolution public-domain JPEGs when available.
- **Discovered**: 2026-07-11 (<operator> suggested docs as an ocas-reach source)
- **Verified**: Live API calls succeeded for `/departments`, `/search?q=sunflowers&hasImages=true`, and `/objects/436524`.
- **Notes**: Initial Reach actions should be `list_objects` (with `metadataDate` and `departmentIds` filters), `get_object`, `departments`, and `search_objects` with supported search filters (`q`, `isHighlight`, `title`, `tags`, `departmentId`, `isOnView`, `artistOrCulture`, `medium`, `hasImages`, `geoLocation`, `dateBegin`, `dateEnd`). Citation should prefer `objectURL` for object records and docs URL for aggregate endpoints. Because search returns object IDs only, a higher-level helper may optionally fetch first N object details after search, but should preserve raw IDs/result counts.
- **Source session**: current

#### Harvard Art Museums API
- **Endpoint**: `https://api.harvardartmuseums.org`
- **Docs**: `https://github.com/harvardartmuseums/api-docs`
- **Data**: Harvard Art Museums collections metadata and media: objects, people, exhibitions, publications, galleries, classifications, centuries, colors, cultures, groups, media/technique/support/worktype vocabularies, places, activities, sites, video, image, audio, annotations. Object records include provenance, credit line, dates, culture/classification/medium, people, publications, exhibitions, gallery, colors, images, and IIIF links.
- **Auth**: API key required via Google Form request. Key passed as `apikey` query parameter.
- **Rate limits**: 2,500 requests/day. Default page size 10; max `size=100`.
- **Quality**: Primary source maintained by Harvard Art Museums; data powers the public museum website; refreshed daily around 6am. JSON REST API plus IIIF Image/Presentation services. Strong fit for factual cultural-heritage lookups and collection/image/provenance queries.
- **Cost/terms**: Free, non-commercial only. Do not cache/store content for more than two weeks without written permission. Must identify/link Harvard Art Museums content; use returned image URLs rather than local copies; logo/name hostname restrictions.
- **Discovered**: 2026-07-11 (<operator> suggested GitHub API docs as an ocas-reach source)
- **Notes**: Better than scraping the collection website. Initial Reach actions should likely be `search_objects`, `get_object`, `search_people`, `get_person`, `search_exhibitions`, `get_exhibition`, `search_publications`, `get_publication`, `list_vocab`/resource passthrough, and `iiif_manifest`. Generic resource passthrough may cover the long tail, but object/person/exhibition deserve typed helpers. Citation should include `url` field for object/person records and docs URL otherwise. Requires account provisioning before full integration/testing.
- **Source session**: current

#### Walters Art Museum Collections Data
- **Endpoint**: `https://github.com/WaltersArtMuseum/api-thewalters-org` (static CSV data files); API homepage `https://api.thewalters.org/`
- **Docs**: GitHub wiki linked from repository: objects, images/media, collections, geographies, exhibitions.
- **Data**: Static data files for the Walters Art Museum collections. `art.csv` contains 10,000+ digital object records with fields including object ID/number/name, date begin/end/text, title, dimensions, medium, style, culture, inscriptions, classification, period, canonical resource URL, description, credit line, keywords, provenance, dynasty/reign, geography ID, related objects, image filenames, collection IDs, museum location note, creators, and exhibitions. Related CSVs cover media/images, relationships between objects, collections/categories, geographies, and exhibitions.
- **Auth**: None for GitHub/static files.
- **Rate limits**: GitHub raw/API rate limits apply; no museum API rate limit currently relevant because live v1 API closed in 2023.
- **Quality**: Primary institutional collection data from Walters Art Museum; CC0 and commercial reuse allowed. Good for offline/static factual lookups over Walters collection records and media, but not a live API until v2 comes online.
- **Cost/terms**: Free; repository README states data and images are CC0 for reuse, including commercial purposes. Verify image URL construction/media terms from `media.csv`/wiki before exposing image URLs.
- **Discovered**: 2026-07-11 (<operator> suggested GitHub repo as an ocas-reach source)
- **Verified**: Repository is active/unarchived; README states v1 closed in 2023 and static data files are available until v2. `art.csv` was readable via GitHub API and contains object records with canonical `https://purl.thewalters.org/art/...` citation URLs.
- **Notes**: Register, if integrated, as a static dataset/custom connector rather than a REST API. Initial Reach actions should be `search_objects` (CSV scan/filter), `get_object` by ObjectID/ObjectNumber, `list_collections`, `list_exhibitions`, `get_media` by ObjectID/ObjectNumber, and possibly `download_snapshot`/`refresh_snapshot`. Citation should use `ResourceURL` for object records and repository/docs URL for aggregate queries. Lower immediate priority than The Met for live REST behavior, but valuable because it is CC0 and adds Baltimore/Walters coverage.
- **Source session**: current

### Standards & RFC

#### IETF Datatracker API
- **Endpoint**: `https://datatracker.ietf.org/api/v1`
- **Data**: Machine-readable metadata for IETF/IRTF standards documents — RFCs, Internet-Drafts, working-group charters, groups, persons, meetings, IPR disclosures, liaisons, and more. The `/doc/document/` endpoint alone indexes 157,549 records (drafts, RFCs, reviews, slides). Resource list (from API root): community, dbtemplate, doc, group, iesg, ipr, liaisons, mailinglists, mailtrigger, meeting, message, name, nomcom, person.
- **Auth**: None required for read access (anonymous GET returns 200).
- **Rate limits**: Not published; throttle conservatively (Datatracker is a shared community resource — <2/sec recommended).
- **Quality**: Primary source maintained by the IETF Secretariat. REST JSON (Tastypie-style: `?format=json`, `?limit=`, `?offset=`, filter params per resource). Each record carries a `resource_uri` and grouped `meta` block (total_count, next, previous). Strong structured alternative to scraping Datatracker HTML pages.
- **Cost/terms**: Free, open. IETF community content; attribute appropriately.
- **Discovered**: 2026-07-14 (reach:api-mine — surfaced from interactive sessions referencing `datatracker.ietf.org` during dashboard/MCP-cookie work)
- **Verified**: Live API calls confirmed: `/api/v1/?format=json` (resource list, 200), `/api/v1/doc/document/?limit=1&format=json` (200, total_count 157549), `/api/v1/group/group/?limit=1&format=json` (200), `/api/v1/person/person/?limit=1&format=json` (200), `/api/v1/meeting/meeting/?limit=1&format=json` (200). Anonymous requests succeed without auth. (`/doc/docalias/` 404'd — use `/doc/document/` and filter by `name` for RFC lookup.)
- **Notes**: Initial Reach actions should be `list_resources` (API root), `get_document` (by name, e.g. `rfc9000`), `search_documents`, `get_group`, `get_person`, `get_meeting`. Deduplicate against `sources.yml` and this catalog before integration — not currently present. Better than scraping Datatracker HTML for RFC/WG/meeting metadata. Potential consumer skills: ocas-sift (technical research), ocas-reach (standards fact lookup), ocas-scout.
- **Source session**: `20260713_001806_387698` (and related dashboard-cookie sessions)

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
- **Notes**: General-purpose marketplace, NOT "local business search." The `util-rapidapi` skill is the canonical reference for the host list; counts drift, so read the host registry rather than quoting a number. Use for discovery, then integrate best APIs individually into Reach.
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

### Museums & Cultural Heritage

| Rank | API | Why |
|------|-----|-----|
| 1 | The Met Collection API | Primary museum source, 470k+ objects, no auth, 80 req/sec, CC0/Open Access, direct public-domain image URLs |
| 2 | Harvard Art Museums API | Richer/more varied museum metadata and IIIF support, but requires key and is non-commercial with stricter caching/attribution terms |

### Archives & Newspapers

| Rank | API | Why |
|------|-----|-----|
| 1 | Chronicling America API | Free, no auth, 23M+ pages, covers 1790-1963, preferred over Newspapers.com (no API) |
| 2 | Google Books API | Free tier sufficient, best snippet previews, structured metadata |
| 3 | OpenLibrary API | Fully open data, good for older/public-domain works, but lower rate limits |

---

## Recently Discovered

_Newest additions go here first. When fully categorized and indexed, move to Registry._

### Web Data Extraction

#### Zyte API
- **Endpoint**: `https://api.zyte.com/v1/extract` (POST); docs `https://docs.zyte.com/`
- **Data**: Web page content extraction with three capabilities in one call: (1) **unblocking** — anti-bot bypass (proxy rotation, fingerprint matching, challenge solving) via `httpResponseBody` field; (2) **JS rendering** — headless browser load with optional actions (click, scroll, wait, screenshot, geolocation) via `browserHtml` field; (3) **automatic structured extraction** — named data types (Product, Article, ArticleList, productList, jobPosting, forumThread, SERP) extracted by model, no CSS/XPath selectors required. Each result includes a confidence score (`extractionProbability`) and typed/named fields.
- **Auth**: HTTP Basic Auth — API key as user name, empty password.
- **Rate limits**: Usage-based (paid); no published hard limit. Pay-per-request pricing on Zyte's website. Free trial available.
- **Quality**: Commercial-grade extraction maintained by Zyte (same company behind Scrapy). Extraction models are site-adaptive — layout changes don't break selectors. 0.997 extraction probability demonstrated on test page.
- **Cost**: Paid (usage-based). Requires credit card/billing account. Not currently budgeted.
- **Discovered**: 2026-09-16 (web research — efoss article "Web Scraping With A Single API" by Ayan Pahwa, Open Source For Us)
- **Source session**: current
- **Notes**: Integrates natively with Scrapy via `scrapy-zyte-api` addon and `scrapy-poet` DI. Zyte also publishes a Claude Code plugin for AI-assisted scraper generation. Not yet live-verified from this host. Candidate for sift.fetch tier 3.5 if budget permits and donsetch proves insufficient for anti-bot. For now, catalog only — requires account provisioning + billing authorization before integration.

### Satellite & Earth Observation

#### NASA GIBS (Global Imagery Browse Services)
- **Endpoint**: `https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/` (WMTS REST/KVP); also WMS, TWMS, XYZ/TMS
- **Data**: ~180+ satellite imagery layers — MODIS, VIIRS, Landsat, Sentinel-2 (best available), MERRA-2 climate reanalysis, GEDI biomass, sea surface temperature, fire detection, aerosols, vegetation indices, and more. Global coverage, daily cadence for many layers, some near-real-time. Time dimension: YYYY-MM-DD per tile, with date ranges per layer (some back to 1980).
- **Auth**: None required
- **Rate limits**: No documented hard cap; be reasonable
- **Quality**: Authoritative NASA source. WMTS standard (OGC). Tiles are pre-rendered PNG at fixed zoom levels (250m to 16km). GetCapabilities XML lists all layers with identifiers, date ranges, projections, tile matrix sets. Massive GetCapabilities response (~5MB).
- **Discovered**: 2026-06-24 (evaluating Earth View github.com/colincode0/earth-view as source reference)
- **Notes**: Different from existing `nasa` source (which covers api.nasa.gov query APIs like APOD/NEO/EONET). GIBS is a tile imagery service — complementary, not overlapping. The `nasa` source's `eonet` action covers natural events; GIBS covers the underlying imagery. Earth View (colincode0/earth-view) uses GIBS as its primary globe renderer. Also used by VEDA, OpenStreetMap, and many scientific visualization tools.
- **Integration plan**: Add as `gibs` source with actions: `get_capabilities` (parse layer list from WMTS GetCapabilities XML), `get_tile` (construct tile URL from layer/zoom/row/col/date params), `list_layers` (filtered search across capabilities). Custom connector needed because WMTS is not a simple REST query pattern.
- **Source session**: current

### News & Social

#### Hacker News API
- **Endpoint**: `https://hacker-news.firebaseio.com/v0` (Firebase REST)
- **Data**: Tech-news / social aggregator. `topstories.json`, `newstories.json`, `beststories.json` return arrays of item IDs; `item/<id>.json` returns a story/job/poll/comment object (`by`, `title`, `url`, `text`, `score`, `time`, `descendants`/comment count, `kids`/comment IDs, `parent`); `user/<id>.json` returns a user profile (`id`, `about`, `karma`, `created`, `submitted[]`); `updates.json` returns recently changed items/users. All JSON.
- **Auth**: None required (public Firebase API)
- **Rate limits**: Not published; Firebase-backed, generous. Throttle to <1-2/sec to be safe.
- **Quality**: Primary source maintained by Y Combinator. Real-time community-curated tech/news stories and discussion. Structured, no scraping needed.
- **Discovered**: 2026-07-23 (reach:api-mine — surfaced from ocas-haiku content-queue workflow that already fetches HN top stories via curl)
- **Verified**: Live calls confirmed: `/v0/topstories.json` (returns ID array), `/v0/item/<id>.json` (returns full story object with `by`/`descendants`/`kids`/`score` fields).
- **Notes**: Complements `reddit` (main index) as a social/news signal source. Candidate consumer skills: ocas-haiku (content queue already pulls HN top stories), ocas-sift (tech-news research), ocas-vesper (daily briefing top stories). Better than scraping HN web pages or relying on ad-hoc curl scattered across skills. Initial Reach actions: `top_stories` (fetch + resolve N items), `get_item`, `get_user`, `updates`. Deduplicate against `sources.yml` and this catalog before integration — not currently present.
- **Source session**: `20260716_175117_de5bb7` (and HN-referencing sessions in the 7d window)

_All other discovered APIs have been moved to the Registry above. This section will populate with new discoveries from future cron runs._

### Music & Audio

#### MusicBrainz API
- **Endpoint**: `https://musicbrainz.org/ws/2/` (REST); docs `https://musicbrainz.org/doc/MusicBrainz_API`; also `https://beta.musicbrainz.org/ws/2/` (beta)
- **Data**: Authoritative music metadata database — artists, releases/albums, release-groups, recordings (songs), works, labels, places, events, instruments, series, URLs. Each entity carries stable UUID (**MBID**) identifiers, artist-credit, dates, barcodes, ASIN, label/catalog info, track/medium counts, country, lyrics/relations via linked entities. Supports structured search (`?query=artist:"X" AND release:"Y"`) per entity type plus direct MBID lookups, browse (`?inc=`), and linked entity `inc` includes (release-groups, recordings, etc.).
- **Auth**: None required for public read (must send a descriptive `User-Agent` identifying the client; the API `403`s or `503`s bare/HTTP-client defaults).
- **Rate limits**: Public pool ~1 request/sec / 100 req/min; extremely strict. Self-host the data (MusicBrainz data is CC0, released under the Open Data license; monthly data dumps + `brainz-musicbrainz-docker` replication available) for heavier use.
- **Quality**: Community-curated primary source (the de-facto canonical music identifier system, used as the identifier backbone by Spotify, Wikipedia, and music fingerprinting). CC0/Open Data licensed.
- **Discovered**: 2026-09-11 (reach:api-mine — surfaced from the DroppedNeedle music-library session, which resolved 2021 albums / 897 artists from Google Drive to MBIDs via this API)
- **Verified**: Live `release` search (`query=artist:"Lykke Li" AND release:"Wounded Rhymes"`) returned real structured release JSON including MBID, artist-credit, barcode, label-info, track-count (HTTP 200). One subsequent rapid artist lookup returned `503 busy` — confirming the aggressive 1 req/sec limit; throttle strictly.
- **Notes**: Complements existing `openalex`/`arxiv` scholarly sources for a factual music-metadata domain. Candidate consumer skills: ocas-haiku (music content), ocas-sift (music research), ocas-reach (music fact lookup), ocas-voyage (venue/event context). No existing source in `sources.yml` covers music metadata. Initial Reach actions: `search` (per entity type: artist/release/release-group/recording/work/label), `get_entity` by MBID, `browse` with `inc` links. Mandatory descriptive User-Agent; throttle to ~1/sec.
- **Source session**: `20260911_020506_ebd047` (and `20260911_004332_793d948d` DroppedNeedle setup)

#### Cover Art Archive API
- **Endpoint**: `https://coverartarchive.org/release-group/{mbid}`, `.../release/{mbid}`,
  `.../artist/{mbid}`, `.../release/{mbid}/{id}` (a specific image),
  `.../release-group/{mbid}/front-{size}` (direct image bytes; sizes 250/500/1200/…),
  `.../release/{mbid}/front`, and `/release-group/{mbid}` with `?fmt=json`
- **Docs**: `https://musicbrainz.org/doc/Cover_Art_Archive/API`
- **Data**: JSON metadata describing the cover art for a release / release-group / artist:
  `images[]`, each with `types` (e.g. `Front`, `Back`, `Booklet`, `Medium`, `Liner`,
  `Spine`, `Track`, `Composer`, `Other`), `image` (full-size URL), `thumb` (small), `front`,
  `back`, `edit` (a revision number), `approved`, `comment`, `id`. Append a size segment to any
  entity URL to fetch a resized JPEG directly instead of the JSON.
- **Access**: **None required.** No key, no account.
- **Rate limits**: **None in place** — the official docs state plainly "There are currently no
  rate limiting rules in place at coverartarchive.org." Do not abuse that: the service is
  volunteer-run on donated hardware and the real cost is other people's latency.
- **Quality**: Joint Internet Archive / MusicBrainz project. Art is community-curated and
  **peer-reviewed**, which is the point — a `Front` image here is a specific, approved
  edition's artwork, not a scraped storefront thumbnail. CC0 for the metadata.
- **Verified**: Live 2026-09-28 from this host. Resolved MusicBrainz release-group
  `f9eab5ff-6eb5-4c4e-9136-afbbc491f7cb` (Lykke Li, *Wounded Rhymes*) →
  `GET /release-group/{mbid}` = **200**, 1 image, `types: ["Front"]`, full-size URL
  `.../release/cc73731a-.../39242083203.jpg`; `/release-group/{mbid}/front-1200` = **200**,
  a valid 308KB JPEG. Note `thumb` came back `None` on this record — a null thumb is a real
  state, not a failed read, so don't treat it as an error.
- **Notes**: The natural companion to the MusicBrainz entry above, and the missing half of it:
  MusicBrainz returns the MBID, the Cover Art Archive returns the picture. Directly relevant to
  the active DroppedNeedle library workflow, which was already proxying coverartarchive.org
  through nginx and logging "cover art archive requests are saturating the single uvicorn
  worker" — an existing consumer with a real scaling constraint. Suggested Reach actions:
  `get_cover_art` (`mbid`, optional `type`/`size`), `list_images` (`mbid`). Reached via MBID
  resolved from MusicBrainz; requires the same descriptive User-Agent convention and the same
  ~1/sec discipline as MusicBrainz, since they share an origin (`musicbrainz.org` and
  `coverartarchive.org` both resolved to `142.132.241.153` this run).
- **Source session**: `20260911_231021_82acd0f5` (DroppedNeedle cover-download queue)


#### DroppedNeedle REST API (self-hosted service)
- **Endpoint**: `/api/v1` on the deployed instance (`tunes.indigokarasu.com`); OpenAPI spec at `/openapi.json` on the same instance
- **Access**: Self-hosted Docker service (port 8688), behind nginx basic-auth + app login on `tunes.indigokarasu.com`; has an API key for the slskd backend integration. Uri is instance-specific — not a public shared API.
- **Data**: Music search/download via the slskd (Soulseek) backend — search artists/albums/tracks, queue downloads (FLAC preference), resolve albums to MusicBrainz IDs. Exposes song files through the shared storage mount.
- **Verdict**: Confirmed working + deployed and health-checked 2026-09-11 (container healthy, reaches slskd API 200). Integrated into the personal music-library workflow (GDrive album list → MBID resolve → queue FLAC downloads). Self-hosted/instance-scoped, so it belongs as a skill-integrated connector (like LetsFG/HotelsByDay) rather than a shared Reach world-data source.
- **Source session**: `20260911_004332_793d948d`, `20260911_020506_ebd047`

### Recruiting & Job Postings

No ATS source is registered in `sources.yml` (61 sources; only `linkedin` touches hiring), yet
`util-headhunter` — an active Mon/Wed/Fri cron — does its Step-3 discovery by SearXNG plus
scraping individual career pages. ATS boards expose a first-class public JSON API for exactly
that data. Four verified (2026-09-27 for the first three, 2026-09-28 for Workday);
deduplicated against `sources/index.md` and this file. **Registration remains the open gap** —
these four are cataloged here, none is in `sources.yml` yet.

#### Greenhouse Job Board API
- **Endpoint**: `https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs` (list) and
  `https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs/{id}` (detail, adds full posting)
- **Data**: Every open posting on a company's board. List entries carry `id`, `title`,
  `location.name`, `company_name`, `absolute_url` (direct apply link), `updated_at`,
  `first_published`, `application_deadline`, `metadata`. The detail endpoint adds `content`
  (full posting HTML, 4.7KB observed), plus `departments`, `offices`, `data_compliance`.
- **Access**: **None required.** No key, no account, no signup. Public per-company board.
- **Rate limits**: None published. Response is `ETag`-tagged with `x-cache` — send
  `If-None-Match` and a matching response is a cheap 304. Poll boards on a schedule, not in a loop.
- **Quality**: Primary source — the employer's own ATS, not an aggregator. Titles and locations
  are exact strings, so the skill's free-text `salary_display` / "never parse for arithmetic"
  rule stays intact.
- **Verified**: Live 2026-09-27. 200 OK, 0.07–0.1s. 24 boards scanned: figma 163 jobs,
  databricks 887, stripe 701, datadog 449, mongodb 396, elastic 384, scaleai 203, coinbase 210,
  vercel 88, airbnb 159. A 404 means "no such board token" (notion, linear, stripe-on-ashby etc.
  use other ATSes) — it is **not** an error to retry. Detail endpoint confirmed returning
  4,679 chars of inline `content`.
- **Notes**: Replaces SearXNG `site:` sweeps and career-page scraping for the discovery step.
  Suggested Reach actions: `boards` (list tokens), `list_jobs` (`board`, optional `?updated_at`
  since-filter for incremental runs), `get_job` (`board`, `id` → full text).
  Consumer: `util-headhunter` Step 3/4. Complements the existing `linkedin` source, which covers
  people/recruiter lookup rather than postings.

#### Ashby Public Postings API
- **Endpoint**: `https://api.ashbyhq.com/posting-api/job-board/{name}` — no auth, single
  unparameterised call returns the whole board.
- **Data**: Each job carries `id`, `title`, `location`, `address`, `secondaryLocations`,
  `department`, `team`, `employmentType`, `workplaceType`, `isRemote`, `publishedAt`, `applyUrl`,
  `jobUrl`, and — importantly — **`descriptionHtml` + `descriptionPlain` inline** (7,887 and
  19,126 chars observed). No second request needed to read a posting.
- **Access**: **None required.**
- **Rate limits**: None published; `cache-control: public, max-age=60, stale-while-revalidate=60`
  with an `ETag` — a 60s-cadence sweep costs one origin hit per board.
- **Quality**: Primary source. `department`/`team` give a clean, machine-filterable signal for
  product/design orgs — better than inferring function from a title string.
- **Verified**: Live 2026-09-27. 200 OK, 0.02–0.2s. openai 830 jobs, ramp 158, notion 128,
  whoop 159, ashby 66, linear 30, attio 42. Some boards return 200 with `jobs: []` (vercel,
  mercury, deel) — an empty board is a valid state, not a failure. 404 = wrong slug
  (figma, anthropic, stripe, robinhood are not on Ashby).
- **Notes**: The ATS of choice for the design-forward companies on the headhunter target list
  (Linear, Notion, Ramp, Ashby itself), i.e. exactly the Tier-2/Tier-4 companies the skill
  otherwise has to scrape. Suggested Reach actions: `list_jobs` (`name`, optional
  `isListed`/`department` filter), `get_job` (`name`, `id`). Consumer: `util-headhunter`.

#### Lever Postings API — LIVE but verify the board token
- **Endpoint**: `https://api.lever.co/v0/postings/{company}?mode=json` (path unchanged; see
  official `lever/postings-api` repo). Single call returns the full posting list with
  `additionalPlain` description text inline.
- **Access**: **None required.**
- **Verified**: Live 2026-09-27. `https://api.lever.co/v0/postings/leverdemo?mode=json` → **200
  with a real JSON array**, confirming the endpoint and path are current. Every real-company
  token tried (figma, databricks, notion, vercel, linear, pinterest, coinbase, robinhood, mongodb,
  openai, plaid) returned 404 — those firms have **migrated off Lever to other ATSes**, which is
  a 404-on-`{company}` *token* miss, not a dead API. `robots.txt` is permissive (`Crawl-delay: 1`).
  Do not record this source as dead on the strength of token 404s alone.
- **Rate limits**: None published for the public postings endpoint.
- **Quality**: Same primary-source benefits as the other two; `categories.team` /
  `categories.location` give the same org filter as Ashby's `department`.
- **Notes**: Lower priority than Greenhouse/Ashby for this particular target list, because so
  few of Jared's target companies still run on Lever. Worth registering only as a third-fallback
  ATS so a company that *does* run Lever is never silently missed. Suggested actions:
  `list_postings` (`company`).

#### Workday CxS careers API — the fourth major ATS, and the list call is POST not GET
- **Endpoint**: `https://<tenant>.wd<N>.myworkdayjobs.com/wday/cxs/<tenant>/<siteId>/jobs`
  — **POST**, `Content-Type: application/json`, body
  `{"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": ""}`.
  Detail: `GET {base}{externalPath}` (note: **detail is GET while list is POST**).
- **Access**: **None required.** No key, no account, no signup. Same property that makes
  Greenhouse/Ashby/Lever catalogable.
- **Data**: `total`, `jobPostings[]` with `title`, `externalPath`, `timeType`,
  `locationsText`, `postedOn`, `bulletFields`; plus `facets[]` = `timeType` (Full/Part-time),
  `workerSubType` (9 values), `jobFamilyGroup` (22 values), `locationMainGroup`. Detail returns
  `jobPostingInfo` (14+ fields incl. `jobDescription`, `jobReqId`, `startDate`, `canApply`,
  `country`), `hiringOrganization`, `similarJobs`, `userAuthenticated`. `searchText` and
  `appliedFacets` both genuinely filter (verified: `searchText:"director"` → 45 of 1169;
  a nonsense term → 0).
- **Rate limits**: None published. Responses are `cache-control: no-store, no-cache` — treat
  every call as an origin hit; poll on a schedule.
- **Quality**: Primary source. The `jobFamilyGroup` facet (22 values) is a cleaner
  function/org filter than parsing a title string, and it is machine-readable where
  Greenhouse's is not.
- **Verified**: Live 2026-09-28. roche `total=1169` (20 returned, 4 facet groups);
  nvidia `NVIDIAExternalCareerSite` `total=2000`. Detail endpoint 200 with a 2,482-char
  `jobDescription`.
- **Host + site discovery is the hard part, and the obvious host is wrong**: public careers
  boards are `<tenant>.wd<N>.myworkdayjobs.com` — **not** `<tenant>.myworkday.com` (that is
  the post-login tenant app host; it resolves and 404s, which reads like a dead API). Recover
  the real `tenant` and `siteId` from the careers landing page's inline `window.workday` bootdata
  (`tenant: "roche"`, `siteId: "roche-ext"`); the `token` in that block is **not** needed for
  CxS (verified: adding it as a bearer header changed nothing). `wdN.myworkdayjobs.com` as a
  bare host fails TLS with a hostname-mismatch certificate, and `ffive.wd5.myworkdayjobs.com`
  serves a `community.workday.com/invalid-url` stub — so validate the site slug from bootdata
  rather than guessing. Wrong siteId → `errorCode: S21` / HTTP 404.
- **Notes**: Completes ATS coverage for `util-headhunter` — Roche, NVIDIA, JPMorgan-class
  employers run Workday, and Step 3 discovery is currently SearXNG + career-page scraping.
  Suggested Reach actions: `list_jobs` (`tenant`, `site`, `searchText`, `limit`, `offset`,
  optional `appliedFacets`), `get_job` (`tenant`, `site`, `external_path`),
  `list_facets` (`tenant`, `site`). A connector should fetch bootdata to resolve
  host/siteId rather than taking them as caller-supplied strings.
- **Source session**: `20260926_112734` (Workday candidate-account mail in the triage window)


### Travel & Lodging
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Flight search + real booking | LetsFG API | `fli` lib (Google Flights data) | Agent-native CLI/SDK/MCP; booking requires card-on-file auth |
| Day-use hotel rates | HotelsByDay API | browser scrape | Internal JSON API at api.hotelsbyday.com; integrated in Voyage script |
| Overnight hotel rates + compare | HotelOracle MCP (SerpAPI backend) | Google Hotels (browser) | 8 research-only tools |
| Hotel booking w/ identity-verified tools | 1Stay MCP (mcp.stayker.com) | — | 8 tools incl. lookup/cancel/resend; Bearer auth |

#### LetsFG API
- **Endpoint**: CLI (`letsfg`), Python SDK, MCP (`npx letsfg-mcp`); docs https://letsfg.co/for-agents
- **Access**: Freemium search AFTER one-time `letsfg auth` (zero-amount Stripe card-on-file → 90-day Bearer token). NEVER use `/developers/api/v1/agents/register` or `setup-payment` (paid Developer billing).
- **Data**: Flight search/book across airlines+OTAs incl. budget carriers; hotel search/book (free-cancellation pay-later rates, 5% non-refundable reservation fee).
- **Verdict**: Confirmed working; already integrated into the Ocas Voyage skill, which owns `references/letsfg.md` (booking flow, auth steps). Reach does not bundle that doc. Better than scraping when an actual booking is required without an OTA redirect.

#### HotelsByDay API
- **Endpoint**: `https://api.hotelsbyday.com` (internal JSON API discovered from site JS)
- **Access**: No public key required for autocomplete/search/hotel-detail flows used by the site.
- **Data**: Day-use (daytime) hotel availability, rates, room detail.
- **Verdict**: Confirmed working; integrated into ocas-voyage as `scripts/hotelsbyday_search.py`. Better than browser scraping.

#### HotelOracle MCP
- **Endpoint**: Via Glama connector (io.tooloracle/hoteloracle); SerpAPI-backed
- **Access**: MCP tools: search_hotels, hotel_details, price_calendar, price_compare, area_guide, best_deals, nearby_attractions, health_check.
- **Data**: Multi-site hotel rate comparison.
- **Verdict**: Research-only (no booking); known failure mode: SerpAPI empty responses with auto-refunded credits. Integrated in ocas-voyage lodging-sources.md.

#### 1Stay MCP (stayker)
- **Endpoint**: `https://mcp.stayker.com/mcp`, Bearer auth (sandbox vs production key scopes)
- **Access**: 8 tools: search, details, lookup_booking, get_booking, cancel_booking (two-step), resend_confirmation, search_tools; chain_code brand filter.
- **Verdict**: Documented live 2026-08-08; integrated in ocas-voyage lodging-sources.md. Rate codes expire in 15 min; checkout URLs in 30 min.


### Events & Venues

No events source is registered in `sources.yml` (61 sources; nothing for live city events), yet
Jared asked on 2026-09-29 for a 3-day SF events aggregation and the pipeline built for it
(`indigokarasu.com/pinkpages/`, `sf-events-v2/fetch.mjs`) already consumes an undocumented public
JSON feed with no key and no signup. Both entries below were verified live 2026-09-29 and are
new against `sources/index.md` and this file. **Registration remains the open gap.**

#### DoTheBay JSON Feed
- **Endpoint**: `https://dothebay.com/events/today.json?per_page=25` (also `tomorrow.json`);
  **arbitrary future date** at `https://dothebay.com/events/{YYYY}/{M}/{D}.json?per_page=100`;
  venues at `https://dothebay.com/venues.json?per_page=200` (paged, 447 venues, 18 pages).
  Per-venue calendar is the permalink + `.json` (e.g. `dothebay.com/venues/greek-theatre.json`).
- **Access**: **None required.** No key, no account. Send a descriptive `User-Agent`.
- **Data**: Rich event objects with `id`, `title`, `permalink`, `buy_url` (the venue's own ticket
  URL), `sold_out`, `is_free`, `is_ongoing`, `doors`, `category`, `begin_date`/`begin_time`/
  `end_date`/`end_time`, `excerpt`, `imagery`, and a nested `venue` object carrying `title`,
  `permalink`, `latitude`/`longitude`, `full_address`, `city`, `neighborhood`, `capacity`.
  `sold_out` and `buy_url` are exactly the two fields the Pink Pages filter needs, and the
  nested `venue.latitude/longitude` is why that build geo-filters by bounding box rather than
  trusting the `city` string.
- **Rate limits**: None published. `per_page` appears to be **clamped to 25** — asking for 100
  still returns 25 (confirmed on the dated feed). Paging is real: `paging.next_page_path`
  (`today.json?per_page=25&page=2` returned the remaining 20 of 45), and `per_page=200` on
  venues also returns 25, so walk `paging` to exhaustion rather than trusting `per_page`.
- **Quality**: Aggregator (DoTheBay, a Scout-era/DoPages property) — a *secondary* source, not
  the venue's own page. That is acceptable here only because `buy_url` points through to the
  original organizer. Multi-day aggregation still requires one request per date, so the
  "find a multi-day window" question raised in the build session is answered by the dated path,
  not by a week feed.
- **Verified**: Live 2026-09-29. `today.json` 200, 124,161 bytes, `api_version: 0.005`,
  25 events; dated path `events/2026/10/01.json` 200, 202,921 bytes, 25 events, `date: 2026-10-01`
  — so a future date really is reachable, which is the fact the build session lacked.
  `venues.json` 200, 447 venues. `week.json` and `weekend.json` both return **200 with
  `events: []`** — they are not 404s, they are empty, so do not record a week feed as available.
  `events.json?date=` **ignores the `date` param** and returns today (byte-identical to
  `today.json`); use the path form. Venue `neighborhood` is `null` on every event object
  observed, so it cannot be relied on as a filter field.
- **Notes**: Suggested Reach actions: `events_on` (`date`, `page` → one dated feed),
  `list_venues` (`page`). Consumer: the SF events pipeline behind Pink Pages.
  Complements `open_meteo`/`transit_land` for local-life questions; adds nothing for
  ticket booking (it links out to organizers).

#### SF Funcheap WordPress REST API
- **Endpoint**: `https://sf.funcheap.com/wp-json/wp/v2/` — `posts` (144,419 entries, paged),
  `cityguide` (8,154 entries), `categories` (320), `tags` (12,891); RSS at `/feed/`.
  Enumerate the site with `/wp-json/wp/v2/types` — it reveals every custom post type and its
  `rest_base`, which is how `cityguide` was found.
- **Access**: **None required.** WP REST is public on this site; no key, no auth.
- **Data**: One post per event listing. Fields: `id`, `date`, `date_gmt`, `modified`, `link`
  (the canonical listing URL), `slug`, `title.rendered`, `excerpt.rendered`, `content.rendered`,
  `featured_media`, `categories`, `tags`, `meta`. Every entry is a *page* titled like
  `11/22/26: Golden Gate Park Sunday Roller Disco Party (SF) - FREE` — i.e. **the event date and
  the free/paid signal are in the structured title**, with a real `pubDate` in the RSS feed.
  Price appears as `$\d` tokens in content; the `is_free` signal is the `- FREE` title suffix.
- **Rate limits**: `X-WP-Total` and `X-WP-TotalPages` are returned on every request; page with
  `?per_page=` and follow `X-WP-NextPage` (`Link` header) to exhaustion. Note the totals are the
  whole archive (144k posts), so any date filter has to be applied client-side.
- **Quality**: Free editorial events calendar, entirely complementary to DoTheBay — Funcheap
  covers the free/community listings DoTheBay's paid listings index less well, and the two have
  little title overlap. As a WP site it is a far better surface than browser scraping.
- **Verified**: Live 2026-09-29. `/wp-json/wp/v2/types` 200 (6,581 bytes) listing 13 types incl.
  `cityguide` (`rest_base: cityguide`); `posts?per_page=1` 200 with `X-WP-Total: 144419`;
  `cityguide?per_page=3` 200, 28,563 bytes, 8,154 entries; `/feed/` 200, 10 items,
  `pubDate` present. **Caveat measured, not assumed**: the newest `posts` entry returned
  `content.rendered` of only **132 chars and an empty `excerpt`**, so the body is not a reliable
  field to parse price/date from on the latest posts — prefer the title and `date` fields over
  HTML-parsing `content`, and expect the full body on older posts.
- **Notes**: Suggested Reach actions: `list_events` (`after`/`before` ISO dates, `page`),
  `get_event` (`id`). Consumer: the same SF events pipeline. Complements DoTheBay — two
  independent Bay Area feeds, so a union pull is meaningfully better than either alone.

### Venue-Platform Feeds (plugin-level, not single-site)

Discovered 2026-09-30 while mining the SF events pipeline for `api-mine`. Both entries below
are **platform surfaces, not site feeds**: any venue running the underlying platform exposes
them with no key, so they generalise across every consumer of that stack. Neither is a single
quirk of one store or one venue. Both verified live with a known-good control in the same pass
(see `api-mine-cron-notes.md` — a positive claim needs a control too, not just a negative one).

#### The Events Calendar (Tribe) REST v1 — the standard WordPress events plugin
- **Endpoint**: `https://<site>/wp-json/tribe/events/v1/events`
- Also available, same auth: `/categories`, `/tags`, `/venues`, `/organizers`, `/venues/<id>`
- **Access**: **None required.** No key, no account, no signup — it is a WordPress REST
  namespace, and the plugin registers it automatically.
- **Data**: Each event carries ~45 fields including `id`, `title`, `excerpt`, `description`,
  `start_date` / `end_date` (real ISO-ish local `YYYY-MM-DD HH:MM:SS`) plus `start_date_utc` /
  `utc_start_date`, `timezone` / `timezone_abbr`, `all_day`, `url` (permalink), `slug`,
  **`venue`** (a nested object with the venue's own id/name/address/lat/lng), `organizer`,
  `categories` (taxonomy terms — usable as a machine filter), `tags`, **`cost`** (a human
  string like `"$58"`, with `cost_details` when structured), `image` (url + width/height),
  `featured`, `status`, `website`, and `rest_url` for the single-event resource.
- **Verified**: Live 2026-09-30 from this host against `workshopsf.org`.
  `?per_page=3` → 200, keys and field set exactly as above, first event
  `id=98161`, `start_date="2026-09-29 19:00:00"`, `cost="$58"`, real permalink.
  **Pagination measured**: `total=94`, `total_pages=94` at `per_page=1`; `total_pages=2` at
  `per_page=250` and 50 returned, so **`per_page` is honoured up to at least 250**.
  **The date filter genuinely works**: `?start_date=2026-10-01&end_date=2026-10-01&per_page=5`
  → `total=1`, returning `Beginner's Leatherworking`. This is the field that makes it
  strictly better than scraping a month-grid.
- **Control run**: a deliberately-bogus route on the same host
  (`/wp-json/tribe/events/v1/definitely-not-a-route`) returned **404 with
  `{"code":"rest_no_route"}`**, while the real route returned 200 on the same host in the same
  pass — so the 200 is the route answering, not the host answering everything. The vendor's own
  hosts were also probed: `wptribal.com` **timed out** and `allthingsevents.tribeplatform.com`
  returned **525** (Cloudflare origin down) — neither is evidence about the API, which is why
  neither is recorded as a source status.
- **Quality**: Primary source — the venue's own WordPress install, no aggregator in the path.
  `categories` gives a clean function filter, exactly the benefit Ashby's `department` provides
  in the ATS notes above, and `cost` supplies the price signal the SF pipeline currently has to
  infer. Complements DoTheBay and SF Funcheap (both already cataloged): those are *aggregator*
  calendars covering everything, this is *first-party* structured data for one venue's own
  calendar.
- **Notes**: Suggested Reach actions: `list_events` (`site`, optional `start_date`/`end_date`,
  `page`, `per_page`), `get_event` (`site`, `id`), `list_venues` (`site`), `list_categories`
  (`site`). A connector should take a *site*, not a token — the plugin path is identical
  everywhere, so one generic connector covers every WordPress venue rather than a per-venue
  entry. Two measured traps for whoever wires it:
  1. **`title`/`excerpt` are plain strings in this plugin, not `{rendered}`** as WP REST
     normally returns. Reading `.rendered` yields `undefined` and a `if (!title) continue`
     guard then drops every event silently — this is a live bug that took a venue to zero
     published events in the SF pipeline with no error logged anywhere.
  2. **HTML entities are not decoded** in the JSON: `cost="$58"` is clean, but
     `title="Beginner&#8217;s Leatherworking"` and `"Carve &#038; Print"` are not.
- **Source session**: `20260930_010742_f9476f` (SF events pipeline; Workshop SF venue)

#### Shopify `products.json` — the standard commerce platform's public catalogue
- **Endpoint**: `https://<store>/products.json` (whole catalogue) and
  `https://<store>/collections/<handle>/products.json` (one collection). Both accept `limit`
  (1–250 documented) and `page`.
- **Access**: **None required** on the storefront's `*.myshopify.com` host. No key, no
  Admin-API token, no app install. The Admin API is a different, authenticated thing — this is
  the *public storefront* JSON.
- **Data**: `products[]` with `id`, `title`, `handle`, `body_html`, `product_type`, `tags`,
  `created_at`, `published_at`, `updated_at`, `vendor`, `images[]`, `options[]`, and
  `variants[]` (each with `id`, `title`, **`price`**, `available`, `sku`). A bookseller
  running author talks as products gets the event in `title` + `product_type`/`tags`, the
  date in the `body_html`, and the price as a real numeric variant price.
- **Verified**: Live 2026-09-30 from this host against `omnivorebooks.myshopify.com`.
  `/collections/upcoming-events/products.json?limit=3` → 200, 3 products, first
  `product_type="Event"`, `tags=["Event","Events"]`, `variants[0].price="0.00"`.
  `/products.json?limit=3` → 200, first `product_type="New Books and Magazines"`, price
  `50.00`. The full `upcoming-events` collection is **24 products, all `price="0.00"`** —
  free events, which is exactly what that collection contains.
  **Collection membership is honoured**: a bogus handle returned `{"products":[]}` with 200,
  not a fall-through to the whole catalogue, so a bogus slug is distinguishable from a real
  one.
  **Limit clamping is not a thing here**: `limit=5→5`, `24→24`, and `25/50/250/1000` all
  returned exactly 24 (the collection's size) with byte-identical responses. Whatever the
  ceiling is, a request never returns more than the collection holds, so paging with `page`
  is optional for small collections and needed for large ones.
- **Control run — the important one, since a universal claim needs evidence**: four unrelated
  Shopify storefronts in the same pass, URLs built explicitly. `www.allbirds.com` → **200**
  (2 products, `type='Shoes'`), `kith.com` → **200** (`type='Low Top Sneakers'`), and
  `www.mvmtwatches.com` → **200** (`type='Watches'`). `www.gymshark.com` returned **403 with
  an Akamai HTML challenge page** — an edge WAF in front of the origin, i.e. *that store's*
  edge configuration, not a platform behaviour. **3 of 4 unrelated stores returning 200 makes
  this a general platform surface, not an Omnivore quirk.**
- **Two probe defects of mine, recorded because both produced a false reading first**:
  (1) pass 2 built control URLs with `base.rstrip("/products.json?limit=2")` — `rstrip` takes a
  *character set*, not a suffix, so it stripped the tails off three hostnames and produced
  `www.allb`, `www.gymshark`, `kith`; every "control" was then a DNS failure at a host that
  never existed, which reads identically to "these stores don't expose products.json".
  (2) pass 2 also reported `json_error: Invalid \uXXXX escape at offset 598476` for
  `limit=250/300/1000` alike — three different limits failing at the *identical* byte offset
  is a client artifact, not a payload defect; the same URL fetches as 776,437 bytes and parses
  cleanly when the body is read whole instead of through a capped read. Neither defect
  changed the conclusion, but the first pass's "3 DNS failures" would have been recorded as a
  real negative without the second look.
- **Notes**: Suggested Reach actions: `list_products` (`store`, `collection`, `page`, `limit`),
  `get_product` (`store`, `handle`). Same connector argument as Tribe: the path is identical
  across every store, so one generic connector covers every bookseller, museum shop, and
  ticket-selling venue rather than a per-store entry. Real caveat for the SF events use case:
  the **date is only in `body_html`**, which is unstructured and store-specific, so this source
  gives reliable *title + price + availability* but needs per-store date parsing for a
  3-day-window filter. `variants[0].available` is a usable stock/sold-out signal, which is the
  one field the pipeline's sold-out filter currently lacks a first-party source for.
- **Source session**: `20260930_010742_f9476f` (Omnivore Books venue in the SF events build)

#### Tribe REST v1 `/venues` — first-party venue addresses (the Pink Pages address gap)
- **Endpoint**: `https://<site>/wp-json/tribe/events/v1/venues` (collection, `per_page`
  honoured) and `/wp-json/tribe/events/v1/venues/<id>` (single).
- **Access**: **None required.** Same auth-free namespace as `/events`.
- **Why this entry exists**: the SF events build closed with an explicit boundary — *"closing
  that gap needs a per-venue source carrying addresses and contacts, a different data contract,
  not a better parser."* The Pink Pages build has venues with names and URLs but no street
  address, no phone, no lat/lng. This is that data contract, and it was already installed on
  the pipeline's own hosts.
- **Data**: `venues[]` with `id`, `venue` (name), `slug`, **`address`** (street line),
  **`city`**, **`stateprovince`**, **`zip`**, `province`, `country`, **`phone`**, **`website`**,
  `description`, `show_map`, `show_map_link`, `global_id` (a stable
  `<host>?id=<venue_id>` cross-referencing key), and `global_id_lineage`.
  `global_id` is the field that makes a union across many venue WordPress installs
  *deduplicable* — the same physical venue is listed by several organizers on different hosts
  and carries the same `global_id` when they are one site.
- **Verified — the important part, and the reason the boundary above was wrong**: live
  2026-09-30, **two independent tenants**, `?per_page=50`:
  - `www.atasite.org` → `total=2`, **2/2 with `address`**, 2/2 `city`, 2/2 `zip`, 1/2 `website`,
    0/2 `phone`. Rows: *Gray Area* — `2665 Mission Street`, San Francisco CA 94110,
    `website=https://grayarea.org/`; *Artists' Television Access* — `992 Valencia Street`,
    San Francisco CA 94110.
  - `workshopsf.org` → `total=4`, **4/4 with `address`**, 4/4 `city`, 4/4 `zip`, 2/4 `phone`.
    Rows include *WorkshopSF* — `1310 Haight Street` 94117, `(415) 926-8078`; *Mission
    Location* — `726 15th St.` 94103; *Inner Richmond — Studio Sumi* — `5031 Geary Blvd`
    94118; *Upper Haight — The Mellow SF* — `1401 Haight Street` 94117.
  **`address` was populated on 6 of 6 records across both tenants.** A field present on 1 of
  4 would not be a contract; 6 of 6 across two unrelated sites is one.
- **The core CPT does NOT work — test this before you rely on the core route**: the core
  route map *does* expose `tribe_venue` as a post type with `rest_base: tribe_venue`, and
  `https://<site>/wp-json/wp/v2/tribe_venue` returns **200 with real venue rows** (2 rows on
  atasite.org, 3 on workshopsf.org, titles `Gray Area`, `Upper Haight Location – The Mellow
  SF`). It looks like the answer. **Every address column in it is `null`** —
  `venueaddress`, `venueaddress_2`, `city`, `province`, `state`, `zip`, `postcode`, `country`,
  `countrystate`, `latitude`, `longitude`, `phone`, `website` — on *both* hosts. The CPT
  returns standard WP post fields (`title.rendered`, `slug`, `content`, `status`, `link`,
  `meta`) because that is what the CPT *is*; the venue's address is Tribe's own postmeta,
  which only the v1 namespace serialises. **A pipeline reading `wp/v2/tribe_venue` would get
  200, find real venue records, and silently import zero addresses** — the exact
  title-present-data-absent failure the 09-30 notes warn about, one layer down.
- **Control runs**: bogus route `/wp-json/tribe/events/v1/definitely-not-a-route` → **404** on
  both tenants while the real route returned 200 in the same pass; bogus CPT
  `/wp-json/wp/v2/tribe_definitely_not_a_type` → **404** on both. A third tenant already in the
  catalog as a *negative* control, `sf.funcheap.com` (WordPress, `cityguide` CPT, no Tribe),
  returned **404** on `/tribe/events/v1/venues` in the same pass — so the 200s are Tribe's
  plugin answering, not every WordPress site answering 200.
- **One real caveat, measured**: the `venue` object **embedded in the events feed is not
  always present**. `workshopsf.org` events carry a fully-populated embedded `venue`
  (address + phone). `www.atasite.org` events return **no `venue` key at all** on the sampled
  record. So *events* is not a reliable venue-address source across tenants — **the
  `/venues` collection is**. Any connector should call `/venues` for address data rather than
  harvesting `event.venue`, and must treat the embedded object as best-effort.
- **Quality**: Primary source, first-party, no aggregator in the path. This is a strict
  *supplement* to DoTheBay (already cataloged), not a replacement: DoTheBay's
  `venue.latitude/longitude` and `capacity` are not in Tribe's payload, and Tribe's venues are
  only the venues running the plugin. Together they cover each other's gaps — DoTheBay for
  coordinates and city-wide breadth, Tribe v1 for first-party addresses of the specific
  venues the pipeline already pulls events from.
- **Notes**: Suggested Reach actions: `list_venues` (`site`, `page`, `per_page`),
  `get_venue` (`site`, `id`). Note the existing `list_venues` action in the DoTheBay entry
  above is a *different source's* action; these would share a name only if the two connectors
  are namespaced, which the registry should decide deliberately. The connector takes a
  *site*, not a token.
- **Source session**: `20260930_021734_09a811` (Pink Pages venue-address gap; pipeline hosts
  `www.atasite.org`, `workshopsf.org`)

#### WordPress core REST `/wp-json/wp/v2/` — the enumeration surface under every site above
- **Endpoint**: `https://<site>/wp-json/` (route index) and
  `https://<site>/wp-json/wp/v2/types` (every registered post type + its `rest_base`).
- **Access**: **None required.** No key, no account. It can be disabled per-site, and some
  hosts front it with a WAF, so treat a 404 as "this site has it off" rather than universal.
- **Why it earns an entry**: the per-site discovery method the pipeline should use. One call
  to `/wp-json/wp/v2/types` returns the complete list of custom post types with their REST
  bases — that is how the SF Funcheap `cityguide` type was originally found, and it is the
  cheapest possible way to answer "is there structured event data on this site, and under
  what key" for *any* WordPress host, before writing a single scraper selector.
- **Data**: `/wp-json/` returns `namespaces[]`, `routes{}` (the full route map with regex
  patterns), `authentication`, and `site`, `site_name`, and `description`. `/wp-json/wp/v2/types`
  returns each type's `slug`, `rest_base`, `name`, `hierarchical`, `taxonomies`, and
  `supports`.
- **Verified live 2026-09-30 across four tenants** — the platform claim needs more than one
  tenant, per `api-mine-cron-notes.md`:
  - `grayarea.org` — `/wp-json/` 200, **1,722,538 bytes**, **46 namespaces, 1,208 routes**,
    27 types (`course`, `lesson`, `product`, `feedback` — a Sensei LMS + WooCommerce install,
    i.e. events are *not* a CPT here).
  - `www.atasite.org` — 200, **20 namespaces, 291 routes**, 16 types, incl.
    `tribe_events`→`tribe_events`, `tribe_venue`→`tribe_venue`, `tribe_organizer`,
    `tribe_rsvp_tickets`, `tec_calendar_embed`.
  - `workshopsf.org` — 200, **36 namespaces, 717 routes**, 21 types, incl. the same Tribe set
    plus `jetpack_form` and `spectra-popup`.
  - `sf.funcheap.com` — 200, **14 namespaces, 245 routes**, 13 types, incl. `cityguide`.
  - **Control**: a deliberately-bogus `/wp-json/definitely-not-a-route-xyz` returned **404**
    on all four hosts in the same pass while the real route answered 200 on each — so the 200
    is the route answering, not the host answering everything. Note the servers differ per
    host (Cloudflare, Apache, nginx, nginx), so this is not one host's configuration.
  - **Bounded by the hosts that are not WordPress**: `www.missionbowlingclub.com` and
    `www.sfcb.org` → `/wp-json/` **404**, `Server: Squarespace`; `www.clayroomsf.com` → 404,
    Cloudflare in front of Wix (`static.parastorage.com` + `static.wixstatic.com` in the root
    response's `link` header). Those are a *different platform* with a different surface, not
    a WordPress host that lacks the API — see the Squarespace note below.
- **One real defect of mine, recorded because it produced a plausible false positive first**:
  the first pass used `rstrip()` to normalise URLs, which takes a *character set* rather than
  a suffix, and turned control hostnames into hosts that never existed — the failure mode
  already recorded on 2026-09-30 for `products.json`. Same bug, second probe, same day. It
  was caught by the tell from that same note: several controls failing at DNS while a fourth
  on the same list succeeded is not a plausible distribution. All URLs in the final pass are
  built as explicit f-strings over hosts DNS had already resolved.
- **Notes**: Suggested Reach actions: `describe_site` (`site`) returning namespaces, route
  count and the type→`rest_base` map, and `list_posts` (`site`, `type`, `page`, `per_page`).
  This is the natural pre-flight for any venue pipeline: probe `describe_site` first, branch
  on the returned types, and only fall back to HTML scraping for the hosts that report no
  event-shaped type.
- **Source session**: `20260930_021734_09a811` (pipeline host enumeration)

#### Restaurant menu data — a bounded negative across 16 reached restaurants (no menu API to prefer)
- **Question**: `ocas-taste`'s `taste_menu_monitor.py` scrapes restaurant menus by stripping
  HTML and by running `pdftotext` over linked PDFs. Is there a structured menu API that would
  beat scraping, for the 27 SF restaurants in its own `menu_monitor.json`?
- **Access**: **None found.** Every probe below is a public, no-key GET.
- **Hypothesis 1 — schema.org JSON-LD `Menu`/`MenuItem` (the obvious one)**: **0 of 16** in the
  survey pass, re-verified on an independent second pass as **0 of 9** — *zero* hits on any host
  that answered, including hosts whose JSON-LD is otherwise rich. The recheck printed every
  `@type` it saw, which is the part worth keeping: `richtable`/`lazybear`/`waterbar` each carry
  `foodestablishment`, `postaladdress`, `openinghoursspecification`, `reservation`, `reserveaction`
  (3 blocks each); `delfina` also `geocoordinates` + `contactpoint`; `chefico`/`benu`/`nopa` carry
  `localbusiness`/`website`; `zunicafe` carries `breadcrumblist`/`searchaction`. These sites are
  emitting rich structured data and deliberately omitting the menu — an *engineered* absence
  rather than a site-by-site accident: search engines stopped consuming `Menu` markup years ago,
  so restaurants have no incentive to add it. A missing `@type` among a full sibling set is a
  stronger negative than a missing `@type` on a page with no JSON-LD at all.
- **Hypothesis 2 — an OpenMenu/online-ordering API** (OpenMenu powers a large share of US
  restaurant ordering): probe returned **HTTP 200 with `{"status": 417, ...key error...}`**,
  i.e. the "200 is not the data" trap again. `api.openmenu.co` is **NXDOMAIN**; `openmenu.com`
  answers but is not an API host. Neither is a source.
- **Hypothesis 3 — a WordPress menu custom-post-type**: 8 of 8 reached WordPress hosts expose
  no menu CPT and report **zero** menu-plugin namespaces in their `/wp-json/` namespace
  inventory. Zero, not "not found" — the namespace list is authoritative, and authoritative-looking
  things are where mistakes live.
- **What the menu data actually is** (the useful half of this entry):
  - **PDF menus** — 2 of 16 host a linked menu PDF (`zunicafe.com` 8 PDFs, `flourandwater.com` 5).
    Zuni's `Sample-Dinner-menu.pdf` fetched **200**, 656,005 bytes, magic `b'%PDF-'`, and
    `pdftotext -layout` returned **rc=0, 6,852 chars, 63 non-empty lines** carrying a full
    priced dinner menu ("Crostone with oyster mushrooms… 32.00", "Grilled Stemple Creek Ranch
    ribeye steak … 95.00").
  - **Server-rendered HTML** — prices live in markup, not a data structure; 5 of 16 show
    `$-` amounts in HTML.
- **The trap that nearly produced the wrong answer (record it)**: I counted prices with
  `\$\s?\d{1,3}(?:\.\d{2})?`. The Zuni PDF carries prices as **bare numbers with no `$`**
  (`24.00`, `95.00`) — so my probe reported the one PDF containing a *complete priced menu* as the
  one PDF with **no prices**. I nearly catalogued "menus are absent" from my own regex defect. The
  control that caught it: print the **actual extracted text**, not a count. A count can be wrong
  for a reason that looks exactly like a world fact.
- **Control**: `https://en.wikipedia.org/wiki/Restaurant` → HTTP 200, `ld_blocks=1`, `menu=0` —
  proving the extractor fires on real JSON-LD in this same pass, so `menu=0` is a true negative
  rather than a parser that silently matches nothing.
- **Bounded by transport failures, reported not hidden**: 16 of 27 config entries reached (200 +
  a title); 11 did not — 4 DNS NXDOMAIN (`statebirdprovisions.com`, `hogislandoyster.com`,
  `kokkariexpress.com`, `cortlandsf.com`), 1 SSL **expired** cert (`swanoysterdepot.com`),
  1 hostname mismatch (`perbacco.com` — the cert is not valid for that name), 1 TLS alert
  (`singlethread.com`), 3 timeouts, 1 HTTP 403 (`kokkari.com`). The expired/mismatched certs
  are real operational facts about the monitor's targets that no API would fix.
- **Verdict**: **no source to add.** No menu API beats the existing scrape for this skill. Nothing
  appended to `sources.yml`. Recorded as a negative so a later run does not re-probe WordPress
  menu CPTs, JSON-LD `Menu`, or OpenMenu for a fifth time.
- **Finding about *this* skill, not a new source**: `taste_menu_monitor.py`'s
  `extract_dishes_from_text` keys on `cfg["food_keywords"]` + noise patterns rather than on
  prices, so it is **not** subject to the bare-number trap. Confirmed by reading the function: it
  scores whole lines by food keyword, not arithmetic. Per the ethos rules no site-specific
  workaround is hardcoded — the monitor's keyword approach already survives the case that broke
  my probe.
- **Source session**: `reach:api-mine` cron run 2026-10-01 (delta since the 2026-09-30 run;
  27-entry survey from `commons/data/ocas-taste/menu_monitor.json`, probe scripts `apimine_*`
  under `cache/scratch`).

#### Squarespace `?format=json` — 200 on two hosts, and it is *not* event data (a bounded negative)
- **Endpoint**: `https://<site>/?format=json` (also `?format=json-pretty`).
- **Access**: **None required** on the two hosts probed.
- **Measured**: `www.sfcb.org` → **200**, `application/json;charset=utf-8`, **21,473 bytes**;
  `www.missionbowlingclub.com` → **200**, same content type, **21,079 bytes**. Top-level keys
  on both: `website`, `collection`, `template`, `mainContent`, `calendarView`, `shoppingCart`,
  `userAccountsContext`, `localizedStrings`, `pagePreviewContext`, `uiextensions`,
  `showCart`, `shareButtons`, `empty`, `emptyFolder`.
- **Why this is recorded as a bounded negative rather than dropped**: the obvious next
  inference from a `calendarView` key is "Squarespace has a calendar API." It does not follow.
  Walking the full config on both hosts found **`calendarView: false`** and **zero date-shaped
  leaves** anywhere in the payload — the only strings resembling dates are `Server` booleans
  and the site's own `baseUrl`/`authenticUrl`. **A key name is not a data contract.** This
  payload is site/template configuration (`collection.itemCount`, `navigationTitle`, SEO
  flags), not event records. `collection` describes the blog *collection* (categories, folder,
  ordering, `itemCount`), not individual items.
- **Control**: `/api/1.0/website-configuration` and `/app/` both returned **404** on both
  hosts, and a bogus `/api/1.0/definitely-not-a-route-xyz` also 404 — so the 200 on
  `?format=json` is that specific path answering, not the host serving JSON everywhere.
- **Implication for the pipeline**: the SF events host list mixes platforms. Squarespace and
  Wix hosts (Mission Bowling Club, SFCB, Clay Room) have **no** first-party structured event
  surface reachable without per-site reverse engineering, and the one public JSON endpoint
  carries no event data. For those hosts an aggregator (DoTheBay, SF Funcheap) remains the
  correct source. This entry exists so a later run does not re-probe Squarespace hosts for a
  fourth time, and does not mistake the 200 for a calendar API.
- **Source session**: `20260930_021734_09a811`
