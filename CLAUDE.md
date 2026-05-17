# finainews_non-api

This repo runs a weekly AI news newsletter for a port-operator CFO audience.

## On session start

**Do NOT explore the repository structure, read files, or run commands speculatively.**
Wait for the user to give an explicit instruction.

## Available skill

`/weekly-ai-news` — runs the full newsletter workflow (scout → select → draft → render).

**CRITICAL:** When the user says anything like the phrases below, you MUST call the
`Skill` tool with `skill: "weekly-ai-news"` and pass the user's message as `args`.
Do NOT attempt to implement the workflow yourself by reading files or running commands.

Trigger phrases (non-exhaustive):
- "run weekly-ai-news"
- "generate the newsletter"
- "run the weekly scan"
- "fully automated mode"
- "draft this week's AI news"
- any message containing "weekly-ai-news"
- any of the above combined with "ignore history", "skip history", or "force rescan"

## Development branch

All changes go to branch `claude/multi-agent-news-extract-2DBVH`.
Never push to a different branch without explicit permission.
