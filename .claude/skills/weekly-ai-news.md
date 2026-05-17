---
name: weekly-ai-news
description: Generates the weekly AI news executive summary for a port-operator
  CFO. Use when the user asks to "run the weekly AI scan", "draft this week's AI
  newsletter", "find this week's AI news", or starts the weekly briefing workflow.
---

# Weekly AI News -- Procedure

## Setup
- Determine the **run mode**:
  - If the user says "run automated", "fully automated mode", or similar → **automated mode**.
  - Otherwise → **human mode** (default).
- Ask the user for the **news period** if not specified (default: last 7 days).
  Accept natural language such as "last 14 days", "May 5-12", or "since May 1".
  Derive a concrete date range: {period_start} to {period_end} (YYYY-MM-DD).
  Use this range as the recency filter for all searches in Phase 1.
- Determine the current ISO week: YYYY-WNN (e.g. 2026-W20).
- Create the issue directory: data/issues/{week}/ if it does not exist.
- Run `python scripts/setup_db.py` to confirm data/archive/ exists and report how many
  past newsletters are loaded for history checking.
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
site:a16z.com AI finance enterprise agents [year]
site:mckinsey.com AI finance enterprise agents [year]
site:bain.com AI finance enterprise agents [year]
site:sequoiacap.com AI finance enterprise [year]
site:menlovc.com AI finance enterprise [year]
```

Digests to sweep:
- The Rundown AI (therundown.ai)
- TLDR AI (tldr.tech/ai)
- Ben's Bites (bensbites.com)
- Superhuman AI (superhuman.ai)
- Air Street Press (press.airstreet.com)
- Import AI (jack-clark.net) -- Jack Clark, weekly, research + reflection
- Benedict Evans (ben-evans.com) -- weekly, strategic framing
- One Useful Thing (oneusefulthing.org) -- Ethan Mollick, executive-forwardable
- Interconnects (interconnects.ai) -- Nathan Lambert, model/research signal
- Latent Space (latent.space) -- enterprise AI deployment economics
- a16z (a16z.com) -- VC portfolio + AI commentary
- McKinsey QuantumBlack (mckinsey.com/quantumblack)
- Bain (bain.com) -- AI insights
- Sequoia (sequoiacap.com)
- Menlo Ventures (menlovc.com) -- State of AI in Business

Pull any finance-relevant or port-relevant items found into the candidate pool
before proceeding to per-category source searches.

### Step 1b: Category scout (sequential, one category at a time)

Work through the four categories below. For each:

1. Read the corresponding source file (references/sources_{category}.md).
2. **Run queries using the two-tier system:**
   - Run every `search:` (core) query in the file — no source may be skipped.
   - Collect all `rotation:` queries in the file into a single pool. Pick 25% at
     random and run those. Vary the selection across runs to maximise coverage over time.
   - Substitute the current year for `[year]` and the current month for
     `[current month]` (e.g. "May 2026") throughout.
3. For each result returned, attempt WebFetch on the article URL to retrieve full content.
   If WebFetch returns 403 or times out, write `what`/`so_what` from the search snippet.
4. For each candidate item, run: `python scripts/check_history.py --url "{url}"` -- skip any that return `SEEN`.
4. Score each surviving item on four dimensions (1-10 each):
   - **Relevance** to a CFO of a global port operator (apply +1 materiality bonus for finance items per audience.md)
   - **Novelty** -- genuinely new development, not a restatement of old news
   - **Materiality** -- near-term financial or operational impact
   - **Narrative** -- how compelling is the story; scores high for: named actor + specific outcome
     ("DP World cut close cycle by 23%"), surprise or contradiction ("AI flagged fraud humans missed
     for 6 months"), consequence ("AI agent approved a duplicate $2M payment"), or first-ever
     production deployment at scale. Scores low for vendor press releases, generic capability claims,
     and incremental product updates with no human or financial drama.
5. Drop any item where Relevance < 7 or total score < 28.
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
     "paywalled": false,
     "scores": { "relevance": N, "novelty": N, "materiality": N, "narrative": N, "total": N }
   }
   ```
   Use the article's actual publication date for `published_date`. If only a
   month/year is known, use the first of that month (e.g. "2026-03-01").
   Set `"paywalled": true` if the source requires a subscription to read the
   full article (e.g. taxnotes.com, lloydslist.com, theinformation.com, FT).
   In that case, the `what` field is based on headline + teaser only -- flag
   this in the `what` field with "(headline/teaser only)" at the end.

Categories (scout order -- finance goes first in both scout and output):
- `finance`    -- references/sources_finance.md   (target 3+ items, 50% of total)
- `agents`     -- references/sources_agents.md
- `physical`   -- references/sources_physical.md
- `foundation` -- references/sources_foundation.md

**Categorization rule:** assign each candidate to the category that best describes
*what the story is about*, not where it was found. A story about a model provider
(e.g. Anthropic, OpenAI) integrating their model into an ERP, finance platform, or
enterprise workflow belongs in `finance` or `agents`, not `foundation`. Reserve
`foundation` for model releases, capability benchmarks, pricing changes, and model
provider strategy stories where the subject is the model itself.

Also check Anthropic's finance-specific resources every run:
- https://www.anthropic.com/news/finance-agents (and related Anthropic finance pages)

These pages carry heavier weight -- any named finance agent deployment from
Anthropic should be scored at full value regardless of recency within the last 30 days.

### Step 1c: Tips scout (run after category scout)

Read references/sources_tips.md for the full source list. Apply the same two-tier
system: run every `search:` (core) query, then pick 25% of all `rotation:` queries
in the file at random and run those. Cover all source categories (YouTube, webinars,
written guides, editorial). No `search:` source may be skipped.
Target **3-5 tip candidates** per run so the user has meaningful choice.

Pick videos/articles with clearly instructional titles ("How to...", "Demo:",
"Walkthrough", "Step-by-step"). Avoid opinion pieces or news summaries.

Record tips as `tips_NNN` with `"category": "tips"`. Score and filter the same
way as other candidates (Relevance < 7 or total < 28 → drop).

### Step 1d: Write candidates.json

Write all candidates (news + tips) to `data/issues/{week}/candidates.json` as
a JSON array, ordered: finance items first, then agents, physical, foundation, tips.

## Phase 1.5: Automated selection (automated mode only)

Skip this phase entirely in human mode — go directly to Phase 2.

In **automated mode**, after Step 1d is complete:

1. Render `data/issues/{week}/candidates.html` using the same command as Phase 2
   step 1 (jinja2 template render). Commit and push candidates.json and
   candidates.html so the user can review the full candidate pool later.

2. Read `data/issues/{week}/candidates.json`.

3. Acting as a **senior financial process and automation specialist** advising a
   port-operator CFO, select the final items for the newsletter:
   - Pick **5 to 7 items** total (news + tip combined).
   - Rank candidates by total score; higher score wins.
   - Category balance is a secondary preference — do not force it.
     A category may be dropped entirely if its best candidate scores below the
     weakest item from another category.
   - Include the highest-scoring `tips_NNN` item **only if** it is genuinely
     useful (strong score, actionable same day). If no tip clears the bar, omit
     the tip entirely.
   - Do not force inclusion of failure/risk stories. If they scored high,
     they are already in the ranking.
   - Two items covering the same underlying news event count as duplicates;
     keep only the higher-scoring one.

4. Write `data/issues/{week}/selections.json` as a JSON array in the same
   format as the human-mode file:
   ```json
   [
     {"id": "finance_001", "user_comment": null},
     {"id": "agents_002", "user_comment": null}
   ]
   ```
   Set `user_comment` to `null` for every entry.

5. Print a one-line summary for each selected item:
   `[id] (score: N) — headline`

6. **Do not stop.** Proceed immediately to Phase 3.

---

## Phase 2: Candidate review (human mode only)

Skip this phase entirely in automated mode — Phase 1.5 has already written
selections.json and Phase 3 follows immediately.

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

2. For each selected item, attempt `WebFetch` on its `source_url` to get full
   article content. Three outcomes:
   - **Full content retrieved**: use it to improve or verify `what` and `so_what`.
   - **403 / bot-blocked**: write from the `what` and `so_what` already in candidates.json.
   - **Paywalled** (`"paywalled": true` or paywall detected): write from candidates.json
     content only; do not invent details beyond what the teaser provides.

3. Write a **digest paragraph** (~25 words, no bullet points) that goes between
   the dateline and the first section. One or two sentences: the dominant theme
   this week and the single most material signal for a port CFO.
   Place it in draft.md directly after the italicised dateline, before the first `---`.

3. For each selected **news item** (non-tips), write a newsletter entry following
   the voice defined in references/voice.md. Hard rules for every item:
   - **Headline**: "Company/who did what" format -- subject + verb + object, max 10
     words, no qualifiers. Plain text title above the body.
   - **No em dashes** anywhere. Use a comma, colon, or recast the sentence.
   - **One sentence** (~25 words): combine the key fact (who/what/scale) with the CFO's action or watch item. Bold only the 2-4 key words or phrase that carry the most weight (e.g. the metric, the actor, the deadline) using `**...**` inline.
   - `Source: {url}` on its own line after the sentence.
   - Total target: ~25 words per item.

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
2. Copy (or instruct the user to copy) `data/issues/{week}/newsletter.html` into
   `data/archive/` so future runs detect these URLs as already published.
   The file is automatically picked up by check_history.py on the next scout.
3. Commit and push all output files to the remote branch.
4. Report the output paths to the user.
