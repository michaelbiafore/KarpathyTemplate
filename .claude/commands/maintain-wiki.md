Run a health check on the second brain wiki and fix issues.

## Instructions

Perform these checks across all files in `wiki/`:

### 1. Broken Wikilinks
- Find all `[[wikilinks]]` in wiki pages
- Verify each linked page actually exists
- Report broken links and suggest fixes (create missing pages or fix typos)

### 2. Orphan Pages
- A page is a true orphan only if it is **missing from `wiki/index.md`** AND **no other page links to it**
- Under lazy backlinks (see CLAUDE.md), `wiki/index.md` is the authoritative reachability check — a page reachable via the index alone is not an orphan
- Report true orphans so they can be added to the index or linked from a related page

### 3. Missing Index Entries
- Check that every wiki page appears in `wiki/index.md`
- Add any missing entries

### 4. Missing Frontmatter
- Check that every wiki page has proper YAML frontmatter (title, date, tags)
- Fix pages missing frontmatter

### 5. Missing Cross-References
- For each wiki page, check if there are other pages that mention similar topics but aren't linked
- Suggest new cross-references

### 6. Stale or Contradictory Claims
- Scan for pages that make conflicting claims about the same topic
- Flag these for review

### 7. Content Gaps
- Based on existing pages, suggest obvious topics that should have pages but don't
- E.g., "You have pages about AI coding but nothing about AI for writing"

## Output

Report findings in a clear checklist format:
- ✅ Checks that passed
- ⚠️ Issues found (with details)
- 🔧 Fixes applied automatically
- 💡 Suggestions for the user

Append a lint entry to `wiki/log.md` with the date and summary of findings/fixes.
