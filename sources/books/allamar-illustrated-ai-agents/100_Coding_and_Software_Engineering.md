---
title: "Coding and Software Engineering"
chapter_number: 100
page_start: 283
page_end: 283
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Coding and Software Engineering

Figure 7-2 shows a typical benchmark table from a recent model release.
In the next section, we’ll map common benchmark categories you’ll encounter. After
that, we’ll dive into key concepts for evaluating agents to set you up for building
your own evaluations. This is often a great investment that gives you greater visibility
throughout the life of your project.



![Figure 7-2: A benchmark table from Google](images/fig_07-02_A_benchmark_table_from_Google.png)

*Figure 7-2: A benchmark table from Google*


Figure 7-2. A benchmark table from Google
Coding and Software Engineering
Arguably the most mature family of agent benchmarks measures the ability to write,
fix, and reason about code. These have achieved a moment of being the gold standard
of agent evaluation precisely because code is verifiable: the code either executes and
passes unit tests or it does not.
SWE-bench and its subsequent variants are the canonical example. Each example is a
real GitHub issue that an agent must resolve by producing a passing software patch
that edits multiple files. When SWE-bench launched in 2023, best-in-class agents
resolved around 2% of tasks, but by 2026, leading agents on the public leaderboard
cracked 70% on SWE-bench Verified—a curated version of the benchmark designed
to remove ambiguous or unreliable test cases. Terminal-Bench is another coding
benchmark where the agent operates a Linux terminal to solve software, system, and
environment issues.
We cover coding agents and more of their evaluations in Chapter 10.
Public Benchmarks and Leaderboards
|