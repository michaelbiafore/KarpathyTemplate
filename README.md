# LLM Wiki Starter Kit

A personal knowledge base managed by Claude Code. Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

You feed it sources (articles, books, podcasts, quick notes). Claude compiles them into a living wiki of summary pages, entity pages, and cross-references. Everything viewable in Obsidian. All of it gets denser and more connected as you use it.

## What's Inside

```
llm-wiki-starter-kit/
  sources/        Raw, immutable source material (articles, books, podcasts)
  inbox/          Quick capture for fleeting thoughts
  wiki/           LLM-generated knowledge pages — Claude writes and maintains this
  CLAUDE.md       The schema that tells Claude how the wiki operates
  .claude/
    commands/     3 slash commands: /ingest-url, /ingest-inbox, /maintain-wiki
    skills/       5 Obsidian Skills by Steph Ango (Obsidian CEO)
```

## Setup (5 minutes)

1. Open this folder in Obsidian as a new vault
2. Right-click on the folder and select "New Terminal at Folder"
3. In the terminal, run: `claude`
4. That's it. Claude Code loads the skills, commands, and schema automatically.

## Personalize It (Optional, 10 minutes)

Current categories are defined in the **Categories table in `CLAUDE.md`** — that table is the single source of truth (the slash commands and `wiki/index.md` reference it). To change them, you have two options:

**Option A — edit `CLAUDE.md` directly.** Open `CLAUDE.md`, edit the rows in the Categories table (folder slug + scope description), and save. The next ingest will use the new categories. You can also pre-create matching empty folders under `sources/` and `wiki/`, or let them be created lazily on first use.

**Option B — let Claude interview you.** Paste this prompt into Claude:

> I want to personalize this knowledge base. Interview me about my interests, what I read about most, and what I want to go deeper on. Based on my answers, suggest 4-7 categories. Once I approve them, update CLAUDE.md's Categories table, rename any existing subfolders in `sources/` and `wiki/` to match, update the category headers in `wiki/index.md`, and confirm when everything is done.

Claude will ask a few questions, suggest categories, and update every file that needs changing in one pass.

## The Three Operations

| Command | What it does |
|---------|--------------|
| `/ingest-url <url>` | Fetches an article with Defuddle, saves clean markdown to `sources/`, compiles into the wiki |
| `/ingest-inbox` | Classifies and integrates every note in `inbox/` into the wiki |
| `/maintain-wiki` | Health-checks the wiki: broken links, orphans, missing cross-refs, content gaps |

## Daily Rhythm

- When you read something good, clip with [Obsidian Web Clipper](https://obsidian.md/clipper) or save the URL
- Run `/ingest-url` once a day on saved URLs
- Drop fleeting thoughts into `inbox/` anytime
- End of week: `/ingest-inbox` then `/maintain-wiki`

## Requirements

- [Obsidian](https://obsidian.md)
- [Claude Code](https://www.anthropic.com/claude-code)
- [Node.js](https://nodejs.org) (for Defuddle: `npm install -g defuddle`)

## Credits

- Pattern: [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- Obsidian Skills: [Steph Ango](https://github.com/kepano/obsidian-skills)
- Implementation: [The AI Maker](https://theaimaker.substack.com)
