# AI in Focus — Agent Overview

## What It Does

A weekly AI news agent that scouts the web, scores candidates, and renders a formatted HTML newsletter targeting a port-operator CFO audience. Each run produces a scored candidate pool, a curated selection, a polished draft, and a final HTML output.

---

## 1. News Sources

The agent searches across two tiers of sources every run.

### Digest Sweep (run first)

Fifteen curated AI newsletters and research publications are swept before any category search begins. These surface high-signal items quickly.

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

### Category Source Files (23 files across 5 categories)

After the digest sweep, the agent works through 23 source files grouped by category. Finance is always searched first and accounts for ~50% of the final newsletter.

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

**Physical AI (4 files — humanoid robotics is the priority focus)**

| File | Coverage |
|---|---|
| `sources_physical_humanoid.md` | Humanoid robotics makers: Figure, Boston Dynamics, Agility, Apptronik, Tesla, Unitree |
| `sources_physical_operators.md` | Port operator newsrooms |
| `sources_physical_maritime.md` | Port and maritime media |
| `sources_physical_media.md` | Robotics and automation media |

**Foundation Models (3 files)**

| File | Coverage |
|---|---|
| `sources_foundation_primary.md` | Model releases, benchmarks, pricing |
| `sources_foundation_trade.md` | Trade and analysis publications |
| `sources_foundation_demos.md` | Capability signals and demos |

**Tips (1 file)**

| File | Coverage |
|---|---|
| `sources_tips_youtube.md` | YouTube demos and how-to walkthroughs |

### Scout Modes

| | Full Scout | Simple Scout |
|---|---|---|
| Digest sweep queries | 8 | 4 |
| Queries per source file | All `search:` entries (multiple site-specific) | 1 broad `simple_query:` per file |
| Minimum relevance score | 7 | 6 |
| Minimum total score | 28 | 24 |
| Best for | Comprehensive weekly run | Quick scan or low-budget run |

All queries include an `after:{period_start}` date filter to restrict results to the specified news period.

---

### Simple Scout — All Queries

**Digest sweep (4 queries)**

```
site:therundown.ai AI finance agents enterprise [month] [year] after:{period_start}
site:a16z.com AI finance enterprise agents [year] after:{period_start}
site:mckinsey.com AI finance enterprise agents [year] after:{period_start}
site:tldr.tech AI finance agents models [month] [year] after:{period_start}
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

**Physical AI (4 queries)**

| Source File | Query |
|---|---|
| `sources_physical_humanoid.md` | humanoid robot production deployment pricing logistics warehouse Figure Apptronik Agility Tesla Optimus [year] after:{period_start} |
| `sources_physical_operators.md` | AI automation robotics port terminal AGV crane capex productivity deployment [year] after:{period_start} |
| `sources_physical_maritime.md` | AI automation port maritime robotics AGV terminal throughput deployment named [year] after:{period_start} |
| `sources_physical_media.md` | humanoid robot logistics warehouse industrial deployment production Boston Dynamics Figure Unitree [year] after:{period_start} |

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

**Total: 27 queries** (4 digest + 23 category)

---

## 2. The Four Phases

### Phase 1 — Scout

The agent searches all sources, scores every candidate item on four dimensions (Relevance, Novelty, Materiality, Narrative — each 1–10), filters out low scorers and previously published URLs, and saves surviving candidates to `data/issues/{run}/candidates.json`.

A history check (`check_history.py`) scans past newsletter archives so the same story is never published twice. This can be disabled with "ignore history" at runtime.

### Phase 2 — Review (Human Mode)

Candidates are rendered to `candidates.html` and committed. The agent pauses and waits for a human to edit `selections.json` — picking which items to include and optionally adding comments. The agent resumes when told to continue.

In **automated mode** this phase is skipped: the agent selects the top-scoring 5–7 items itself and proceeds immediately.

### Phase 3 — Polish

For each selected item the agent attempts to fetch the full article (`WebFetch`). If successful, new specifics (named clients, exact metrics) are used to sharpen the write-up. Each story is written as:

- **Headline** — verbatim from `candidates.json` (rewritten only if WebFetch reveals a materially better framing)
- **Body** — one sentence, ≤25 words, compressing the key fact; 2–4 key words bolded
- No source URL line (the headline is the link in the rendered HTML)

A short digest paragraph (~25 words) summarising the week's dominant theme is placed at the top of the draft.

Output: `data/issues/{run}/draft.md`. The agent pauses for a human edit before rendering.

### Phase 4 — Render & Archive

`scripts/render.py` reads `draft.md`, `candidates.json`, and `selections.json`, converts markdown to HTML via Jinja2 template, and writes `newsletter.html`. A copy is placed in `data/archive/` so future runs recognise these URLs as already published.

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
