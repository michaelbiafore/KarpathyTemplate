---
title: "Summary"
chapter_number: 116
page_start: 309
page_end: 310
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Summary

just like unit tests in the software development life cycle, run and update the test
suite automatically on meaningful changes to the system so that improvements are
confirmed and breaking changes are caught as early as possible.
Getting started is more important than getting it immediately right. Even a small
custom eval of 5 or 10 cases can give eye-opening signals about your agent’s perfor‐
mance—and you can grow it as you learn more about where the system fails.
Running evals at any scale requires an eval harness: the infrastructure that takes a
set of test cases, runs the agent against each one, captures the full trajectory, applies
your scoring methods, and aggregates the results. harbor is a recent open source
harness designed specifically for agents, with infrastructure for running trials in
containerized environments at scale and a standardized format for defining tasks and
their success criteria. Popular benchmarks such as Terminal-Bench ship through the
harbor registry, so you can run established benchmarks alongside your own custom
eval suite.
Summary
In this chapter, we examined how evaluation is the foundation of confident
agent development and the difference between intuition and evidence. We started
with benchmarks, the evaluation artifacts most commonly encountered in model
announcements and research papers, mapping the major categories from coding
and tool use to computer use and real-world task completion. We then outlined
the questions worth asking when reading benchmark scores critically, from data
contamination and prompt tuning to cost and benchmark saturation.
We then broke down the core methods for outcome evaluation. We saw how human
evaluation, despite its cost, remains the gold standard against which automated
methods are validated. We covered the automated evaluation spectrum from exact
match and programmatic checks, through LLM-as-a-judge, to rubric-based evalua‐
tion, which improves reliability by decomposing complex judgements into independ‐
ently scorable criteria. We contrasted outcome evaluation with trajectory evaluation,
which examines the sequence of steps an agent took and can surface failure modes
like unsound reasoning, inefficiency, and unnecessary overhead that outcome scores
miss entirely.
We then turned to two properties that deserve dedicated evaluation: reliability and
safety.
Reliability asks not just whether an agent can succeed but whether it succeeds every
time: because outputs are stochastic, running a task repeatedly lets you separate a
capability ceiling (pass@k) from a measure of consistency (pass^k), and the two
can rank models differently. Safety is best organized by who is causing the harm: a
Summary
|

malicious user the agent should refuse, an attacker steering it through injected or
poisoned data, or no adversary at all when the agent errs on a benign task.
We closed with building your own evaluations, where a small, well-curated set of
representative cases, scored with the methods covered earlier and run automatically
on every change, beats waiting for a perfect suite.
In Part II, called specializations, we explore the more advanced and complex com‐
ponents of managing and using agents. We start with multi-agent systems where
agents collaborate and/or compete to solve tasks. Then, it follows with a chapter
on multi-modal understanding so that agents can’t just read but also see and hear.
Finally, we end with arguably the most popular variant of an agent, namely the
coding agent.
|
Chapter 7: Evaluating Agents