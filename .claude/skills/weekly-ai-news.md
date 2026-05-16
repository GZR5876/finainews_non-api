---
name: weekly-ai-news
description: Generates the weekly AI news executive summary for a port-operator
  CFO. Use when the user asks to "run the weekly AI scan", "draft this week's AI
  newsletter", "find this week's AI news", or starts the weekly briefing workflow.
---

# Weekly AI News -- Procedure

## Setup
- Ask the user for the **news period** if not specified (default: last 7 days).
  Accept natural language such as "last 14 days", "May 5-12", or "since May 1".
  Derive a concrete date range: {period_start} to {period_end} (YYYY-MM-DD).
  Use this range as the recency filter for all searches in Phase 1.
- Determine the current ISO week: YYYY-WNN (e.g. 2026-W20).
- Create the issue directory: data/issues/{week}/ if it does not exist.
- Run `python scripts/setup_db.py` to ensure data/history.db exists.
- Read references/audience.md and references/voice.md before writing anything.

## Phase 1: Scout

### Step 1a: Digest sweep (run first, before per-category sources)

Search the following weekly AI digests for items published in the last 7 days.
**Important:** These sites block WebFetch with 403. Use WebSearch with
site-specific queries instead -- do NOT try to WebFetch their homepages.

Search patterns to use:
```
site:therundown.ai AI finance agents enterprise [current month] [year]
site:bensbites.com AI finance enterprise agents [current month] [year]
site:tldr.tech AI finance agents models [current month] [year]
```

Digests to sweep:
- The Rundown AI (therundown.ai)
- TLDR AI (tldr.tech/ai)
- Ben's Bites (bensbites.com)
- Superhuman AI (superhuman.ai)
- Air Street Press (press.airstreet.com)

Pull any finance-relevant or port-relevant items found into the candidate pool
before proceeding to per-category source searches.

### Step 1b: Category scout (sequential, one category at a time)

Work through the four categories below. For each:

1. Read the corresponding source file (references/sources_{category}.md).
2. Use WebSearch + WebFetch to find items published in the last 7 days.
3. For each candidate item, run: `python scripts/check_history.py --url "{url}"` -- skip any that return `SEEN`.
4. Score each surviving item on three dimensions (1-10 each):
   - **Relevance** to a CFO of a global port operator (apply +1 materiality bonus for finance items per audience.md)
   - **Novelty** -- genuinely new development, not a restatement of old news
   - **Materiality** -- near-term financial or operational impact
5. Drop any item where Relevance < 7 or total score < 21.
6. Keep top 5-8 items per category. Record each as a JSON object:
   ```json
   {
     "id": "{category}_{NNN}",
     "category": "{category}",
     "published_date": "YYYY-MM-DD",
     "headline": "...",
     "what": "2 sentences -- what happened",
     "so_what": "1 sentence -- why a port CFO cares",
     "source_url": "...",
     "scores": { "relevance": N, "novelty": N, "materiality": N, "total": N }
   }
   ```
   Use the article's actual publication date for `published_date`. If only a
   month/year is known, use the first of that month (e.g. "2026-03-01").

Categories (scout order -- finance goes first in both scout and output):
- `finance`    -- references/sources_finance.md   (target 3+ items, 50% of total)
- `agents`     -- references/sources_agents.md
- `physical`   -- references/sources_physical.md
- `foundation` -- references/sources_foundation.md

Also check Anthropic's finance-specific resources every run:
- https://www.anthropic.com/news/finance-agents (and related Anthropic finance pages)

These pages carry heavier weight -- any named finance agent deployment from
Anthropic should be scored at full value regardless of recency within the last 30 days.

### Step 1c: Tips scout (run after category scout)

Read references/sources_tips.md for the full source list. Target **3-5 tip
candidates** per run so the user has meaningful choice. Search across all
four source types:

**YouTube** -- Use WebSearch (WebFetch to youtube.com returns 403). Run at
least 3 separate searches targeting different platforms and use cases:
```
site:youtube.com anthropic claude finance agents tutorial [year]
site:youtube.com SAP OR Oracle OR Workday AI finance agents demo [year]
site:youtube.com microsoft copilot finance reconciliation tutorial [year]
site:youtube.com AI treasury "cash flow" forecast tutorial [year]
site:youtube.com "AI agent" CFO accounts payable month-end close [year]
```
Pick videos with clearly instructional titles ("How to...", "Demo:", "Step-by-step").
Avoid opinion pieces or news summaries.

**Vendor webinars (recorded/on-demand):**
- https://www.anthropic.com/webinars
- https://www.kognitos.com/webinars
- https://www.cfoconnect.eu/resources/event-recaps

**Written step-by-step guides:**
- https://finstoryai.substack.com
- https://buildingprofit.substack.com
- https://reruption.com/en/knowledge/how-to-ai/finance/
- https://chatfin.ai/blog

**Editorial with actionable takeaways:**
- https://hbr.org/topic/subject/artificial-intelligence
- https://www.cfo.com/technology/

Record tips as `tips_NNN` with `"category": "tips"`. Score and filter the same
way as other candidates (Relevance < 7 or total < 21 → drop).

### Step 1d: Write candidates.json

Write all candidates (news + tips) to `data/issues/{week}/candidates.json` as
a JSON array, ordered: finance items first, then agents, physical, foundation, tips.

## Phase 2: Candidate review (human checkpoint)

After all categories and tips are scouted:

1. Render the candidates to `data/issues/{week}/candidates.html`:
   ```python
   python -c "
   from jinja2 import Environment, FileSystemLoader
   from datetime import datetime
   import json
   from pathlib import Path
   candidates = json.loads(Path('data/issues/{week}/candidates.json').read_text())
   env = Environment(loader=FileSystemLoader('templates'))
   tmpl = env.get_template('candidates.html.j2')
   html = tmpl.render(items=candidates, week='{week}', generated_at=datetime.now().strftime('%Y-%m-%d %H:%M'), period='{period_start} to {period_end}')
   Path('data/issues/{week}/candidates.html').write_text(html)
   "
   ```
   The template renders 5 sections in order: AI in Finance, AI Agents &
   Applications, Physical AI, Foundation Models, Tips & How-To.

2. Print a summary table: id | category | headline | total score.

3. Commit and push candidates.json and candidates.html to the remote branch.

4. **STOP.** Tell the user:
   > "Phase 1 complete -- {N} candidates ({T} tips) in data/issues/{week}/candidates.html.
   > Review and edit data/issues/{week}/selections.json to choose items and add
   > comments, then tell me to continue."

5. Wait for the user to say "continue" or equivalent before proceeding.

## Phase 3: Polish (human checkpoint)

1. Read `data/issues/{week}/selections.json`.

2. Write a **digest paragraph** (60-80 words, no bullet points) that goes between
   the dateline and the first section. Structure:
   - Sentence 1: the dominant theme across all items this week.
   - Sentence 2: the most material finance-specific signal.
   - Sentence 3: one risk or watch item.
   Place it in draft.md directly after the italicised dateline, before the first `---`.

3. For each selected **news item** (non-tips), write a newsletter entry following
   the voice defined in references/voice.md. Hard rules for every item:
   - **Headline**: "Company/who did what" format -- subject + verb + object, max 10
     words, no qualifiers. Plain text title above the body.
   - **No em dashes** anywhere. Use a comma, colon, or recast the sentence.
   - **Three sentences maximum:**
     1. Bold impact lead -- one sentence, operational or financial consequence.
     2. One context sentence: who, what, key facts or scale.
     3. One implication sentence: what the CFO's team should do or watch.
   - `Source: {url}` on its own line after the three sentences.
   - Total target: ~60 words per item.

4. Assemble news sections into `data/issues/{week}/draft.md`:
   ```
   ## 1. AI in Finance
   ## 2. AI Agents & Applications
   ## 3. Physical AI
   ## 4. Foundation Models
   ```
   Omit any section with no selected items. Separate items within a section
   with a single blank line. Separate sections with `---`.

5. If a `tips_NNN` item was selected, append a **Tip of the Week** block at the
   very end of draft.md (after all news sections), following the format in
   references/sources_tips.md. The tip should be 2-3 sentences: what to do,
   how to do it, what outcome to expect -- actionable enough to try the same day.

6. **STOP.** Tell the user:
   > "Draft ready at data/issues/{week}/draft.md. Edit freely, then tell me to
   > render when ready."

7. Wait for the user to say "render" or equivalent before proceeding.

## Phase 4: Render & archive

1. Run `python scripts/render.py --week {week}` -- produces newsletter.html and
   newsletter.pdf in data/issues/{week}/.
2. The script also inserts all rendered items into data/history.db to prevent
   future duplicates.
3. Commit and push all output files to the remote branch.
4. Report the output paths to the user.
