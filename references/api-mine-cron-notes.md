# reach:api-mine Cron Notes

Operational observations from running the api-mine cron (daily 4am PT).

## Expected Behavior

### "0 new APIs" is the norm, not a failure

When the cron runs and finds zero new APIs, this is **expected and correct** behavior. It means:

1. All sites/services mentioned in recent sessions are already cataloged in `discovered-apis.md` or `sources.yml`
2. The catalog is up-to-date
3. No new skills or workflows have introduced uncataloged data sources

The cron is a **gap-detection** tool, not a continuous-discovery tool. It fires daily to catch anything missed, and most days it should find nothing.

### When it finds new APIs

The cron produces value when:
- A new skill is introduced that uses an uncataloged data source
- An existing skill starts using a new external service
- A session mentions a site with an API but the agent doesn't realize it (the cron's broader extraction pattern catches these)

## Session Retention Limitation

The session database (via `session_search`) only retains recent sessions (typically 48-72h of FTS5-indexed content). Implications:

- **API discoveries in old sessions are lost** — if a session mentioned an API but the session aged out before the cron ran, the discovery is gone
- **Mitigation**: Write API discoveries to `discovered-apis.md` immediately when found in a session, don't rely on the cron to catch them later
- The cron is a safety net, not the primary discovery mechanism

## Catalog Maturity (as of Jun 2026)

The `discovered-apis.md` catalog covers:
- Prediction markets (Kalshi, Polymarket)
- Finance (Alpaca, Finnhub, Massive, AudioAlpha)
- Banking/Transactions (Plaid)
- Places (Google Places)
- Creative (Pollinations.ai)
- Web Search (Google CSAPI, RapidAPI)
- Archives (Chronicling America, Google Books, OpenLibrary)
- Models & ML (Hugging Face Hub)

Plus 60 sources in `sources.yml`. Coverage is broad. New discoveries will be increasingly rare.

## Cron-Skew: Periods Without Interactive Sessions

When the agent is running primarily or exclusively as cron jobs (health monitors, dispatchers, updaters), there may be **zero interactive sessions** (telegram/web) in the mining window. During these periods:

- The cron will always return `[SILENT]` — this is **correct behavior**
- No new APIs will be discovered because cron sessions don't contain user-facing data source usage
- The catalog remains static — also correct
- Discovery resumes naturally when interactive sessions occur again

**Do not** treat a `[SILENT]` result during high-cron periods as a problem. The cron is working; there's simply nothing to mine.

**Confirmed pattern (Jun 27, 2026):** A 7-day window contained 50+ cron sessions and 0 interactive sessions. The cron correctly returned `[SILENT]`. No action needed.

## Cron cannot use pipes into an interpreter (Tirith, confirmed 2026-09-27)

`approvals.cron_mode` is not `approve`, so a cron run has nobody to approve a flagged command and
the scanner **blocks** rather than prompting. Two shapes got blocked in one run:

- `reach.py sources | python3 -c "..."` — "pipe to interpreter" (HIGH)
- `python3 -c "<multi-line body with a regex literal>"` — "nested executable body could not be
  resolved" (HIGH), even when the body is harmless

**Rule:** in a cron, never pipe output into an interpreter and never pass a real program as
`python3 -c`. Write the probe to a file under `~/.hermes/profiles/indigo/cache/scratch/` with
`write_file`, run it with `python3 <path>`, and read the output. `subprocess.run([...])` on
`reach.py` from inside such a file is fine and is the supported way to read the registry.

## A 404 on a per-tenant endpoint is not a dead API (confirmed 2026-09-27)

Nine of nine Lever board tokens returned 404, which reads exactly like "the API is retired." It
wasn't: `https://api.lever.co/v0/postings/leverdemo?mode=json` returned **200 with a real JSON
array** in the same run. The 404s meant those companies had migrated off Lever to a different
ATS.

Before recording any API as dead, prove the negative with a **known-good tenant**: the vendor's
own demo account, a large real customer named in their docs, or a row already in `sources.yml`.
A negative claim carries the burden of proof a positive one does not. Note the shape difference
in the catalog entry too, so the next run does not re-litigate it.

## Cron sessions are a real source of discoveries (revised 2026-09-27)

The Jun 2026 guidance above says high-cron periods should yield `[SILENT]`. That is true for
*discovery of new services*, but wrong as a blanket rule: **cron prompts name the workflows and
tools they drive**, and those workflows are the lead worth mining. Two paths that worked this run:

- `session_search` for a data-source *shape* ("job board", "archive", "weather") surfaces the
  cron session that drives it, then `jobs.json` gives the cron ID.
- Read the cron `prompt` in `~/.hermes/cron/jobs.json` to see what the workflow actually does
  today. This run, the headhunter cron showed Step 3 discovery was SearXNG + career-page
  scraping, while 61 Reach sources included zero ATS entries — the gap was visible only after
  reading the prompt.

A paused or `enabled: true / paused: true` job still counts: the workflow stays a consumer even
while its schedule is off.

## A negative claim needs a control, and a uniform failure is a different fact than a selective one (2026-09-28)

Two probes this run returned "the API is dead" and were both wrong. What separated them was
whether a **control** request was run in the same pass:

- **Workday**: every path variant returned the same `HTTP_400` with a structured
  `{"errorCode":"HTTP_400","errorCaseId":...,"message":""}`. A wrong *path* fails
  **differentially** (404/406); a wrong *verb* fails **uniformly**, because the router rejects
  the request before resolving the resource. A deliberately-bogus control path returned 400
  alongside the real paths — which is the tell that the address was never the variable. The
  list call is **POST with a JSON body**, not GET; once switched, the same URL returned
  `total: 1169`. Four passes had already written off a live, no-auth, high-value source.
- **Host pattern**: the obvious `<tenant>.myworkday.com` resolves and 404s. The real public
  careers host is `<tenant>.wd<N>.myworkdayjobs.com`. Two of the three candidate hosts probed
  this way failed DNS outright, which looks identical to "no such company uses this ATS."

**Rules this earned:**

1. **A connection failure with no HTTP status is not a negative result.** The first Workday
   probe printed `HTTP None` for every URL and I could not tell a dead API from a broken client
   — the exception text was being swallowed. A probe that cannot print *why* it failed must
   return a status of its own, or it does not get to make a claim about the world.
2. **Probe the transport layer separately from the application layer** (DNS → TCP → TLS → HTTP).
   A layered `getaddrinfo` failure and an HTTP 500 are not the same finding, and conflating them
   produces exactly the "source is dead" entry that a later run has to disprove.
3. **Before writing any negative claim, re-read the vendor's own documentation** for the request
   shape. The `errorCaseId` in the response body is vendor-specific and worth parsing — a blank
   `message` with a populated `errorCode` reads as "server refused" when it actually means
   "wrong method."
4. **Recover real URLs from the corpus, not from memory or guessing.** The Workday host pattern
   was recovered by regexing the actual `myworkday*` hostnames out of recent session
   transcripts (`roche.wd3.myworkdayjobs.com` ×27) rather than by constructing candidates.
   Session text is ground truth about what the system actually talks to; a guess is not.

## A control is needed for a POSITIVE platform claim, not only for a negative one

The 2026-09-27 and 2026-09-28 rules both protect a **negative** claim ("this API is dead").
A universal **positive** claim needs its own control, and 2026-09-30 produced two instances of
the same failure in one pass:

- **Tribe / Events Calendar**: 200 at `workshopsf.org` proves that *one venue* exposes it. It
  does not prove the plugin path is stable across WordPress installs. A bogus route on the
  same host (`/definitely-not-a-route`) returned **404 `rest_no_route`** while the real route
  returned 200 in the same pass — that is the control that upgrades "one venue has an API" to
  "this is a platform surface." Note the asymmetry: the bogus route 404ing is what proves the
  200 is *the route answering*, not the host answering everything with 200.
- **Shopify `products.json`**: `omnivorebooks.myshopify.com` answering 200 says nothing about
  Shopify. Three unrelated storefronts (`allbirds.com`, `kith.com`, `mvmtwatches.com`)
  returned 200 with correct typed product records in the same pass; a fourth (`gymshark.com`)
  returned **403 with an Akamai HTML challenge page**. Read that 403 correctly: it is *that
  store's* edge WAF in front of the origin, not a platform property, and it must not be
  written up as "gymshark has no products.json" any more than a token 404 would be written up
  as "Lever is dead."

**Rule: for any claim of the form "platform X exposes Y," probe at least one tenant unrelated
to the one that surfaced it.** One tenant is an anecdote; three is a platform.

## A probe defect that produces a plausible negative is the most expensive kind

Two probe bugs in one 2026-09-30 pass, both of which first read as real findings about the
world and neither of which was:

1. **`rstrip` with a suffix.** `base.rstrip("/products.json?limit=2")` stripped a *character
   set* off three hostnames, turning `allbirds.com` into `www.allb`, `kith.com` into `kith`.
   Every "control tenant" then failed at DNS on a host that never existed. That output is
   **byte-identical in shape** to three stores genuinely lacking the endpoint — the exact trap
   the 09-28 note warns about ("recover real URLs from the corpus, not from memory or
   guessing"). The tell: three hosts failing DNS while a fourth on the same list succeeded is
   not a plausible distribution; if some controls work and the rest are name-resolution
   failures, suspect the URL construction before the world.
2. **A capped read reported as a payload defect.** `limit=250/300/1000` each failed to parse
   at the *identical* offset 598476. Three different limits cannot produce the same byte
   offset in the response; that is the client's read cap, not the server's payload. Reading
   the body whole returned 776,437 bytes parsing cleanly.

**Rules:** a negative reading is only trustworthy if the probe's own construction was checked
first; and **identical failure offsets across differing inputs mean the client, not the
origin** — investigate the probe before the service.

## A plugin/platform surface is a better catalog entry than a single site

Four cataloged entries from earlier runs (`greenhouse`, `ashby`, `lever`, `workday`) are
per-platform, and they are the ones that pay off. `tribe_events` and `shopify_products` belong
in the same class, and the catalog entry should say so explicitly: the connector takes a
*host*, not a token, because the path is identical across every install of the platform. A
per-site entry would be wrong in the useful direction — it would imply the surface is a quirk
of one venue, and the next session would re-derive the same probe from scratch.

Worth stating in the entry that the **plugin surface is often richer than the aggregator it
sits next to**: Tribe's first-party feed carries `cost` and `categories` for one venue, which
DoTheBay's city-wide feed does not carry for that venue at all.

## A key name is not a data contract, and a 200 is not the data you asked for

`/wp-json/wp/v2/tribe_venue` returns **200 with real venue records** and **every address
column `null`** — `venueaddress`, `city`, `state`, `zip`, `latitude`, `longitude`, `phone`,
`website`, on two independent tenants. It is a custom post type, so it serialises post fields;
the venue's address is the plugin's own postmeta, which only the v1 namespace exposes
(`/wp-json/tribe/events/v1/venues` → 6/6 records with a real street address). A connector that
reads the CPT looks correct, returns records, and imports zero addresses with no error anywhere.

This is the 09-28 wrong-layer error wearing a 200. The generalisation: **when a route exists
and answers, still verify that the specific field you need is in the payload.** Status is
transport; the field is the contract.

The same pass found the inverse: `event.venue` is fully populated on one tenant and **absent
entirely** on another, so the embedded object cannot be the contract either. The dedicated
collection is.

## A bounded negative is worth cataloguing; a bounded *guess* is not

Two pipeline hosts answered `?format=json` with 200 and a 21KB config containing a
`calendarView` key. The tempting next step is "Squarespace has a calendar API." Walking the
payload: `calendarView: false`, and **zero date-shaped leaves anywhere in it** — the only
dateish strings were booleans and the site's own `baseUrl`. It is site/template config.

Written up as a source, that entry would be a false positive that costs a future run a
re-probe. Written up as a *bounded negative* — "200 on this path, here is what it does not
contain, here is the control that shows the host does not serve JSON everywhere" — it saves
the next run and stops the inference. The line to hold: **a 200 whose payload does not contain
the field is a negative result about the field, not a positive result about the path.**

## The same probe defect twice in one day means the notes file is not being read as a rule

The `rstrip()` URL-truncation defect recorded this morning for `products.json` recurred
verbatim in this run's first pass: same `rstrip`, same mangled control hostnames, same
DNS-failure shape indistinguishable from a real negative. It was caught again by the *tell*
rather than by remembering the rule — several controls failing DNS while a fourth on the same
list succeeded is not a plausible distribution.

**The lesson is not "remember not to use rstrip."** It is that a note in a reference file did
not change behaviour on a later run the same day, which means the note is a *description* of a
past incident rather than a *procedure*. When a trap recurs, promote it: the actionable form
is the build rule — **construct every URL as an explicit f-string over a host DNS has already
resolved; never normalise a URL by stripping characters.** That is checkable while `rstrip` is
not.

## Probing a live surface: print the data, not the count (2026-10-01)

**2026-10-01 — a "$-anchored" price regex reported the single richest menu as empty.** Probing
16 SF restaurant sites for structured menu data, I counted prices with `\$\s?\d{1,3}(?:\.\d{2})?`.
Zuni's menu PDF writes prices as **bare numbers** (`24.00`, `95.00`) with no currency symbol, so
the one document containing a complete priced dinner menu scored **zero prices**. The count looked
exactly like a world fact — menus have no prices — and I nearly catalogued that. What caught it was
switching from counting to **printing the actual extracted text** (`pdftotext` output plus price
context), where the full menu was plainly visible. **Rule: when a probe yields a surprising zero,
re-run it printing the underlying records before believing it.** A count has no way to distinguish
"I found nothing" from "I looked for the wrong shape." This is the same family as the
"200 is not the data" trap above — the probe succeeded, the question was malformed.

**2026-10-01 — a validation filter that discarded the subject of the study.** I marked sites "is
this a restaurant?" with a title regex (`restaurant|menu|bakery|oyster|...`). It scored `Zuni Café`,
`Tartine`, `Nopa`, `Rich Table` and `Cotogna` as **not restaurants**, collapsing the sample from 16
to 1 — and the one survivor was a false positive. Every excluded site was plainly a restaurant; the
filter was matching my vocabulary, not the world. A denominator built by discarding unfamiliar
cases produces exactly the conclusion it was written to produce. **Rule: validate sample membership
against ground truth you did not author (a config file the skill itself reads), and report the
exclusion count rather than letting it silently shrink the denominator.**

**2026-10-01 — a parked-domain hijack page read as the richest data source.** `sushihon.com`
returns HTTP 200 with **9** JSON-LD blocks and looked like the best structured-data host in the
survey. Its `<title>` is `FAJARTOTO ... Peringkat No#1 Situs Togel` — an Indonesian gambling
landing page squatting an expired restaurant domain. It carried more `localbusiness`-shaped
markup than any real restaurant, and I had already written it into the catalog entry as evidence
before a second, independent pass failed to connect to it at all. **Rule: a 200 with rich
structured data is not evidence of a live business.** Print the `<title>` (and, for a
business-shaped claim, the `name` field) for every host you intend to cite as evidence. A domain
that has expired and been re-registered serves whatever the new owner serves, with the old
host's structured data gone and the new owner's replacing it. This one would have made the whole
entry wrong, and it was only caught because the "recheck the prior claim" step is part of the run,
not an optional extra.

## A relative link concatenates against the path that FETCHED it, not the one that displayed it (2026-10-05)

**Four consecutive passes got this wrong in the same direction.** `foopee.com` serves its
index at `/punk/the-list/`, and that index links 50 sibling files *relatively*
(`HREF="by-date.0.html"`). Fetching the index and then requesting
`http://www.foopee.com/punk/` + `by-date.0.html` returns **404**, and so does every one of
the 50 files. Four passes reported a 404 sweep, a `by-club` sweep, a
"S3 origin exposes nothing" claim and a "the site is empty" reading, all of them
**arithmetic on a base path I had invented**, and none of them about foopee. The correct
base is `http://www.foopee.com/punk/the-list/` and the record-bearing pages 200 there.

**The build rule, in the form that is checkable:** when a document's own relative hrefs are
your next targets, resolve them against **the URL the document was fetched from, as
`urllib.parse.urljoin(response.geturl(), href)`** — and print the resolved absolute URL
before fetching it. Do not hand-concatenate a directory. `geturl()` is the fetched URL *after*
redirects, which is why it is the right input and a remembered path is not.

The tell that this has happened: **a large batch of same-shaped paths 404ing in a regular
pattern** (`by-date.0` … `by-date.45` all 404) is not a missing-content shape, it is a
resolution shape. Real missing content is sparse and its boundaries mean something. And the
control only helps if it is on the *same* axis: a bogus filename 404ing at the wrong base
proves nothing about the right base. Probe `by-date.99.html` at **both** bases — the wrong
one 404s for the same reason the real file does, and only the right base's 404 is
informative.

Two adjacent traps from the same run, both mine:

- **A character class can exclude the thing you are looking for.** `HREF="(by-band[^"#]*\.html)"`
  can never match `by-band.0.html#Foo`, because `#` precedes `.html`. The class excluded a
  literal that appears *before* the extension. The empty result read as "the document
  references no page files" — when it referenced 50. When an extraction returns zero, print
  the raw `HREF="..."` values it is scanning before concluding the document lacks them.
- **A count of the wrong population is not a small error, it is a different claim.** Counting
  `, S.F.` in a *venue index* gave 48 and looked like 48 SF events; the venue index is
  alphabetical with one link per venue ever listed, not a listing. The same regex on the
  date-ordered page gave 78 rows, of which 78 were events. Identify the population from the
  document's own `<H2>` heading before quoting any count from it.

## A recorded negative can be disproven by a later session — re-probe before trusting it (2026-10-07)

The 2026-10-06 run wrote "ESPN API requires authentication / no public JSON endpoint" into a session
conclusion, from a probe of an auth-gated host. Three interactive sessions the next day (Fog & Found
/ SF Pink Pages) fetched a full WNBA season schedule from `site.api.espn.com` — **keyless, HTTP 200,
854 KB, 53 events** — and a second tenant (`.../wnba/teams/9/schedule`) returned 200 too, with a
bogus-path control 404ing. The negative was never cataloged, but it had been *concluded*, and a run
that trusted it would have skipped the source.

**Rule: a negative about a host is a claim about a layer, and a "no public endpoint" verdict must
name the exact host it probed.** `site.api.espn.com` and `sports.core.api.espn.com` are separate
hosts from `site.web.api.espn.com`; "ESPN requires auth" was true of one host and false of the
others. When a later session shows real data flowing from a host a prior run wrote off, re-probe
and correct the record — the session is evidence the negative was scoped too broadly.

## Operational Checklist

After each cron run:
- [ ] Verify journal entry written to `api-mine-journal.jsonl`
- [ ] If new APIs found: verify they're added to `discovered-apis.md` with full details
- [ ] If 0 new APIs: confirm this is expected (catalog current) — no action needed
- [ ] If the cron didn't run (gap > 24h): check gateway status, the cron depends on the scheduler ticker
- [ ] Any new negative claim about a dead API was proven with a known-good tenant first
- [ ] Any "no public endpoint" negative names the exact host probed, and a later session showing
      data from that domain triggers a re-probe (wrong-layer negatives recur)
- [ ] Probes ran as scratch files, not as `python3 -c` or a pipe into an interpreter
- [ ] Any host cited as evidence had its `<title>` printed — a parked/hijacked domain returns 200
      with better structured data than the live site it replaced
- [ ] Any surprising zero was re-derived by printing the underlying records, not by re-running the count
- [ ] Every URL built from a document's own `HREF=` was resolved with `urljoin(fetched_url, href)`
      and printed before fetching — never hand-concatenated onto a remembered directory
- [ ] Every extraction that returned zero had its raw input printed, to rule out a regex that
      cannot match its own target
- [ ] Every count was taken from a population identified by the document's own heading, not
      inferred from proximity
