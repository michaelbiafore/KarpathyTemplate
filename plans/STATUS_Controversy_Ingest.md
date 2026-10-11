# STATUS — Controversy Reference Downloads (§3.2)

**Date:** 2026-10-10
**Source list:** `inbox/Coming Up to Speed on Robotics  A Reading List for a STEM PhD.md`, §3.2 "The central controversy: will data and scaling 'solve' robotics?"
**Destination:** `inbox/controversies/`

## Summary

All 10 distinct references in §3.2 are downloaded. ==No outstanding failures.==
Files are named after their titles; archived web pages are saved as self-contained
`.html` with their content figures mirrored into a sibling `<title>_figs/` folder.

## Numbered reading list (1–7)

| # | Reference | File | Status |
|---|-----------|------|--------|
| 1 | Sutton (2019), "The Bitter Lesson" | `The Bitter Lesson.html` | OK (no figures in source) |
| 2 | Kumar (2023), "Will Scaling Solve Robotics? Perspectives from CoRL 2023" | `Will Scaling Solve Robotics_ Perspectives from CoRL 2023.html` | OK (no figures in source) |
| 3 | Goldberg (2025), "Good old-fashioned engineering can close the 100,000-year 'data gap' in robotics", *Science Robotics* 10(105) eaea7390 | `Good Old-Fashioned Engineering Can Close the 100,000-Year Data Gap in Robotics.pdf` | OK — publisher page is paywalled; obtained the author PDF from Berkeley AUTOLab |
| 3a | Berkeley news summary for the above (supplementary link in the list) | `Are We Truly on the Verge of a Humanoid Robot Revolution.html` + `_figs/` (2) | OK |
| 4 | Amato, Hutchinson, Garg, Billard, Rus, Tedrake, Park & Goldberg (2025), "'Data will solve robotics and automation: True or false?': A debate", *Science Robotics* 10(105) eaea7897 | `Data will solve robotics and automation_ True or false_ A debate.pdf` | OK (free AUTOLab PDF) |
| 5 | Brooks (2025-09-26), "Why Today's Humanoids Won't Learn Dexterity" | `Why Today's Humanoids Won't Learn Dexterity.html` + `_figs/` (45) | OK |
| 6 | Brooks (2026-01-01), "Predictions Scorecard, 2026 January 01" | `Predictions Scorecard, 2026 January 01.html` + `_figs/` (18) | OK |
| 7 | Condliffe (2026-10-08), "AI breakthroughs in robotics won't change your life any time soon", *MIT Technology Review* | `AI Breakthroughs in Robotics Won't Change Your Life Any Time Soon.html` + `_figs/` (12) | OK — full body captured (LeCun, Raibert and air-fryer passages all present) |

## Empirical evidence on scaling

| Reference | File | Status |
|-----------|------|--------|
| Lin, Hu, Sheng, Wen, You & Gao (2025), "Data Scaling Laws in Imitation Learning for Robotic Manipulation", ICLR 2025, arXiv:2410.18647 | `Data Scaling Laws in Imitation Learning for Robotic Manipulation.pdf` (14 pp) | OK |
| Sartor & Thompson (2024), "Neural Scaling Laws in Robotics", arXiv:2405.14005 | `Neural Scaling Laws in Robotics.pdf` (3 pp) | OK |
| TRI LBM Team, Barreiros, … Tedrake (2025), "A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation", arXiv:2507.05331 | `A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation.pdf` (15 pp) | OK (free arXiv preprint) |

## Notes and known gaps

- **science.org is hard-blocked.** Direct fetches of `https://www.science.org/doi/10.1126/scirobotics.aea7390`
  and `.../scirobotics.aea6201` both return **HTTP 403** (Cloudflare + paywall). Neither is a gap:
  - eaea7390 (Goldberg) — author PDF obtained from AUTOLab instead; same paper.
  - eaea6201 — the *Science Robotics* publication of the TRI "Careful Examination" paper; the reading
    list designates the arXiv preprint as the free version, and that is what is on disk. Only the
    typeset journal version is missing.
- `The Bitter Lesson` and the CoRL 2023 blog post contain no images in the source, so they have no
  `_figs/` folder.
- Archive method: `requests` + `beautifulsoup4` — scripts stripped, content images mirrored locally and
  `src` rewritten; site-chrome assets (theme images, logos, favicons) deliberately left pointing at
  their remote hosts.
- These files are raw captures sitting in `inbox/`. They have **not** been ingested into `wiki/` yet —
  next step is `/ingest-inbox` (or `/ingest-pdf` per PDF) to produce the §3.2 controversy pages.
