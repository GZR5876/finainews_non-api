# AI in Focus — Agent Overview

## What It Does

A weekly AI news agent that scouts the web, scores candidates, and renders a formatted HTML newsletter targeting a port-operator CFO audience. Each run produces a scored candidate pool, a curated selection, a polished draft, and a final HTML output.

---

## 1. News Sources

The agent searches across two tiers of sources every run.

### Digest Sweep (run first)

Fifteen curated AI newsletters and research publications are swept before any category search begins, by navigating to each site directly with the Chrome browser tool and reading the page (`get_page_text`) rather than guessing from search snippets. Most of these sites 403 a raw `WebFetch`, but a real browser tab isn't bot-blocked, so this reads the actual current issue. Full scout mode falls back to a `site:` WebSearch query for the three sites that have one (The Rundown, TLDR, Ben's Bites) if the browser attempt fails; simple scout mode just skips a failed site.

| Source | Focus |
|---|---|
| The Rundown AI | Daily AI news digest |
| TLDR AI | Developer and enterprise AI |
| Ben's Bites | AI product and business |
| Superhuman AI | Enterprise productivity |
| Air Street Press | AI industry analysis |
| Import AI (Jack Clark) | Research and safety |
| Benedict Evans | Strategic technology framing |
| One Useful Thing (Ethan Mollick) | Executive-forwardable insights |
| Interconnects (Nathan Lambert) | Model and research signals |
| Latent Space | Enterprise AI deployment economics |
| a16z | VC portfolio and AI commentary |
| McKinsey QuantumBlack | Enterprise AI adoption |
| Bain | AI business insights |
| Sequoia | Technology investment signals |
| Menlo Ventures | State of AI in Business |

Simple scout mode visits only the 4 highest-signal sites (The Rundown, a16z, McKinsey QuantumBlack, TLDR).

A **broad news sweep** runs alongside the digest sweep to catch major-outlet stories outside the curated source list. It has two parts: a live **Google News RSS feed** (`scripts/fetch_google_news_rss.py --query "finance AI"`, all modes) that returns real headlines with verified publication dates straight from `news.google.com/rss/search`, plus 2 unrestricted WebSearch queries in full scout mode (0 in simple mode, since the RSS feed alone covers it). Every item must trace back to a primary source (vendor newsroom, regulator, or major outlet); SEO aggregators and content farms are discarded.

The feed's `link` field is a Google News redirect stub, not the article URL — it's a client-side JS app with no server-side redirect, so it can't be resolved by `WebFetch` or a plain HTTP client, and would defeat `check_history.py`'s exact-URL dedup if stored as-is (every fresh fetch of the same story gets a different stub). Before scoring, each surviving candidate's link is opened in a browser tab and replaced with the resolved URL.

### Category Source Files (19 files across 4 categories)

After the digest sweep, the agent works through 19 source files grouped by category. Finance is always searched first and accounts for ~50% of the final newsletter. There is no relevance/score threshold for dropping candidates -- every category (finance, agents, foundation) is scored and ranked, then capped at the top 15 by score (fewer if a category has fewer than 15 candidates).

**AI in Finance (11 files)**

| File | Coverage |
|---|---|
| `sources_finance_highpri.md` | High-priority AI providers: Anthropic, OpenAI, Google Cloud |
| `sources_finance_media.md` | CFO & finance leadership media, Gartner, Forrester |
| `sources_finance_close.md` | Financial close, reporting, and board packs |
| `sources_finance_treasury.md` | Treasury and cash management |
| `sources_finance_tax.md` | Tax and customs automation |
| `sources_finance_bigfour.md` | Big-4 advisory: KPMG, Deloitte, PwC, EY |
| `sources_finance_fintech.md` | Fintech media |
| `sources_finance_erp.md` | ERP/EPM vendors: SAP, Workday, Microsoft |
| `sources_finance_pointsolutions.md` | Finance point solutions |
| `sources_finance_peers_sg.md` | Peer operators — Temasek portfolio |
| `sources_finance_peers_portops.md` | Peer operators — major port groups |

**AI Agents & Applications (4 files)**

| File | Coverage |
|---|---|
| `sources_agents_general.md` | General AI agent news |
| `sources_agents_frameworks.md` | Agent frameworks and infrastructure |
| `sources_agents_enterprise.md` | Enterprise software with AI agents |
| `sources_agents_bigfour.md` | Big-4 AI agent announcements |

**Foundation Models (3 files)**

| File | Coverage |
|---|---|
| `sources_foundation_primary.md` | Model releases, benchmarks, pricing |
| `sources_foundation_trade.md` | Trade and analysis publications |
| `sources_foundation_demos.md` | Capability signals and demos |

**Tips (1 file, optional)**

Skipped by default. Only runs if the user explicitly asks for a tip this run
("include a tip", "tip of the week") -- across every real run so far, a
scouted tip was never once selected into a final newsletter, so it's no
longer part of the default scout.

| File | Coverage |
|---|---|
| `sources_tips_youtube.md` | YouTube demos and how-to walkthroughs |

### Scout Modes

| | Full Scout | Simple Scout |
|---|---|---|
| Digest sweep | 15 sites, browser navigation | 4 sites, browser navigation |
| Queries per source file | All `search:` entries (multiple site-specific) | 1 broad `simple_query:` per file |
| Candidates kept per category | Top 15 by score (no relevance/total floor) | Top 15 by score (no relevance/total floor) |
| Best for | Comprehensive weekly run | Quick scan or low-budget run |

All queries include an `after:{period_start}` date filter to restrict results to the specified news period.

---

### Simple Scout — All Queries

**Digest sweep (4 sites via browser navigation, no fallback query) + Google News RSS feed (1 fetch, no WebSearch queries in simple mode)**

```
navigate: https://www.therundown.ai
navigate: https://a16z.com
navigate: https://www.mckinsey.com/capabilities/quantumblack/our-insights
navigate: https://tldr.tech/ai
python scripts/fetch_google_news_rss.py --query "finance AI" --after {period_start} --limit 20
```

**AI in Finance (11 queries)**

| Source File | Query |
|---|---|
| `sources_finance_highpri.md` | AI finance agents enterprise deployment Anthropic OpenAI Google Cloud [year] after:{period_start} |
| `sources_finance_media.md` | AI finance CFO automation agents adoption survey Gartner Forrester [year] after:{period_start} |
| `sources_finance_close.md` | AI financial close month-end automation board reporting FP&A consolidation [year] after:{period_start} |
| `sources_finance_treasury.md` | AI treasury cash flow forecasting FX payments automation deployment [year] after:{period_start} |
| `sources_finance_tax.md` | AI tax customs duty classification e-invoicing transfer pricing automation port [year] after:{period_start} |
| `sources_finance_bigfour.md` | AI finance agents Big-4 CFO KPMG Deloitte PwC EY named deployment [year] after:{period_start} |
| `sources_finance_fintech.md` | AI trade finance payments B2B automation bank deployment [year] after:{period_start} |
| `sources_finance_erp.md` | AI ERP finance automation SAP Joule Workday Illuminate Microsoft Copilot deployment [year] after:{period_start} |
| `sources_finance_pointsolutions.md` | AI finance close reconciliation AP AR FP&A automation named deployment case study [year] after:{period_start} |
| `sources_finance_peers_sg.md` | AI finance technology automation Temasek PSA DBS Singapore conglomerate deployment [year] after:{period_start} |
| `sources_finance_peers_portops.md` | AI finance technology automation port operator DP World APM COSCO Hutchison deployment [year] after:{period_start} |

**AI Agents & Applications (4 queries)**

| Source File | Query |
|---|---|
| `sources_agents_general.md` | AI agents enterprise deployment incident failure finance logistics [year] after:{period_start} |
| `sources_agents_frameworks.md` | AI agent framework enterprise deployment LangChain AutoGen finance new release [year] after:{period_start} |
| `sources_agents_enterprise.md` | AI agents enterprise software production deployment Salesforce Agentforce SAP Workday Microsoft named outcome [year] after:{period_start} |
| `sources_agents_bigfour.md` | AI agents enterprise finance Big-4 KPMG Deloitte PwC EY client deployment outcome [year] after:{period_start} |

**Foundation Models (3 queries)**

| Source File | Query |
|---|---|
| `sources_foundation_primary.md` | foundation model release OpenAI OR Anthropic OR Gemini OR DeepSeek OR Mistral capability benchmark pricing [year] after:{period_start} |
| `sources_foundation_trade.md` | foundation model economics pricing analysis OpenAI OR Anthropic OR Gemini OR DeepSeek [year] after:{period_start} |
| `sources_foundation_demos.md` | AI model capability demo benchmark OpenAI OR Anthropic OR Gemini OR DeepSeek [year] after:{period_start} |

**Tips (1 query)**

| Source File | Query |
|---|---|
| `sources_tips_youtube.md` | site:youtube.com AI finance automation tutorial walkthrough CFO agents how-to [year] after:{period_start} |

**Total: 19 WebSearch queries + 4 browser navigations + 1 broad news RSS fetch**

---

## 2. The Four Phases

### Phase 1 — Scout

The agent searches all sources, scores every candidate item on four dimensions (Relevance, Novelty, Materiality, Narrative — each 1–10), filters out previously published URLs, ranks each category by score, and keeps the top 15 per category (finance, agents, foundation) in `data/issues/{run}/candidates.json`. There's no relevance/total-score floor — ranking alone decides what survives.

A history check (`check_history.py`) scans past newsletter archives so the same story is never published twice. This can be disabled with "ignore history" at runtime.

### Phase 2 — Review (Human Mode)

Candidates are rendered to `candidates.html` and committed. The agent pauses and waits for a human to edit `selections.json` — picking which items to include and optionally adding comments. The agent resumes when told to continue.

In **automated mode** this phase is skipped: the agent selects the top-scoring 5–7 items itself and proceeds immediately.

### Phase 3 — Polish

For each selected item the agent attempts to fetch the full article (`WebFetch`). If that 403s, it retries once with a real browser tab (`navigate` + `get_page_text`) before falling back to the candidates.json summary — a normal Chrome session often isn't bot-blocked where `WebFetch` is. The browser fallback is never used against a detected paywall, only against a bot block. If successful, new specifics (named clients, exact metrics) are used to sharpen the write-up. Each story is written as:

- **Headline** — verbatim from `candidates.json` (rewritten only if WebFetch reveals a materially better framing)
- **Body** — one sentence, ≤25 words, compressing the key fact; 1–4 key words bolded
- `Source: {url}` on its own line after the body

Output: `data/issues/{run}/draft.md`. The agent pauses for a human edit before rendering.

### Phase 4 — Render & Archive

The agent asks the user for this issue's number (e.g. "Issue No.5") if not already given -- the skill doesn't track or auto-increment it, the user supplies it each run. `scripts/render.py --week {run} --title "Issue No.{N}"` reads `draft.md`, `candidates.json`, and `selections.json`, converts markdown to HTML via Jinja2 template, and writes `newsletter.html`. A copy is placed in `data/archive/` so future runs recognise these URLs as already published.

```
data/issues/{run}/
  candidates.json   ← scored candidate pool
  candidates.html   ← human-readable candidate review page
  selections.json   ← curated item list (human or automated)
  draft.md          ← polished newsletter copy
  newsletter.html   ← final rendered output
data/archive/
  {run}.html        ← archived for history deduplication
```
