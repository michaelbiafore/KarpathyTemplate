---
title: "Reasoning and Knowledge"
chapter_number: 104
page_start: 285
page_end: 285
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Reasoning and Knowledge

Reasoning and Knowledge
Another family benchmark commonly seen in comparison tables is one that meas‐
ures a model’s ability to reason about complex questions and apply knowledge across
multiple domains. These are typically difficult exam-style questions. MMLU (Massive
Multitask Language Understanding) is one of the earliest and most widely cited
examples, covering dozens of subjects ranging from physics and medicine to law
and history. GPQA Diamond is a more recent benchmark that pushes the difficulty
further. It focuses on graduate-level questions in fields such as physics, biology, and
chemistry that are intentionally designed to be difficult even for domain experts
and resistant to simple memorization. Humanity’s Last Exam takes this even further,
assembling extremely challenging questions across many disciplines.
One thing that’s important to note is that these often test the underlying LLM, not
necessarily the agentic abilities of tool use across multiple steps.
Other Groups of Benchmarks
In addition to the main benchmarks we’ve discussed, you’ll come across a number
of others that measure specialized capabilities. Some focus on abstract reasoning
puzzles, such as ARC-AGI, which attempt to measure general problem-solving on
unfamiliar tasks. Others evaluate multi-modal reasoning, where models must com‐
bine visual and textual information, as in MMMU. There are also benchmarks for
long-context retrieval, sometimes called “needle-in-a-haystack” tests, that measure
whether a model can locate specific information within very large documents.
Table 7-1 provides a summary of categories we’ve looked at.
Table 7-1. Benchmark category examples
Category
Benchmarks
What’s measured
Coding and software
engineering
SWE-bench Verified, Terminal-Bench
Patch correctness, test passage
Tool use
BFCL, τ-bench
Function-calling accuracy, multi-turn-policy following
Computer use
OSWorld, WebArena
Action sequences in desktop/browser environments
Real-world task completion
GAIA, GDPval
Reasoning and retrieval on open-ended knowledge
tasks
Reasoning and knowledge
MMLU, GPQA Diamond, Humanity’s
Last Exam
Exam-style questions across domains
Specialized
ARC-AGI, MMMU, needle-in-a-
haystack
Abstract reasoning, multi-modal, long-context
retrieval
Public Benchmarks and Leaderboards
|