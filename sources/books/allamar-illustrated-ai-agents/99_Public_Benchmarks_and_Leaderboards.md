---
title: "Public Benchmarks and Leaderboards"
chapter_number: 99
page_start: 282
page_end: 282
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Public Benchmarks and Leaderboards



![Figure 7-1: This chapter covers how LLMs and agents are evaluated and explores how we](images/fig_07-01_This_chapter_covers_how_LLMs_and_agents.png)

*Figure 7-1: This chapter covers how LLMs and agents are evaluated and explores how we*


Figure 7-1. This chapter covers how LLMs and agents are evaluated and explores how we
move from evaluating the output to evaluating an agent’s intermediate steps (trajectory)
Public Benchmarks and Leaderboards
A benchmark is a fixed set of tasks paired with a way to score them, so that different
models can be measured against the same yardstick and compared directly. Take
SWE-bench Verified, one of the rows in Figure 7-2. It’s a collection of real GitHub
issues from open source projects. To score a point, a model (or an agent built on
top of it) has to read the description of the issue, explore the code repository, and
produce a patch that makes the project’s existing tests pass (they exist but are hidden
from the model). The score is simply the percentage of issues the agent solves.
Most benchmarks follow the same outline: a dataset of problems, a procedure for
attempting them, and a metric that collapses performance into a single number you
can drop into a table.
These numbers are the scores most people see. AI labs publish them in model
announcements, researchers cite them in their papers, and builders use them to select
LLMs and agent frameworks.
The problem is that reading tables that compare models on various benchmarks
requires a bit of care and nuance. A score of 80% on SWE-bench Verified and a score
of 80% on MMLU represent completely different claims about completely different
capabilities, measured in completely different ways. Some scores come from running
an agent once while other scores aggregate many runs (sometimes in ways that
could be deceptive). Some use deterministic test suites while others rely on an LLM
judge that introduces its own biases. And some benchmarks in these tables aren’t
really measuring agent capability at all, but rather the non-agentic capabilities of the
underlying LLM that powers it.
|
Chapter 7: Evaluating Agents