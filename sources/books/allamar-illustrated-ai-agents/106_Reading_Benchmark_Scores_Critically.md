---
title: "Reading Benchmark Scores Critically"
chapter_number: 106
page_start: 286
page_end: 287
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Reading Benchmark Scores Critically

Reading Benchmark Scores Critically
Seasoned researchers and builders often develop a sense for things to look for and
questions to ask instead of taking reported numbers at face value. Here’s a list
of important questions that are frequently raised to critically examine benchmark
scores:
How was the score produced?
The next section, “Outcome Evaluation: Did the Agent Get the Right Output?”
on page 268, explains the various methods for scoring a model. This is important
knowledge because different evaluation setups can produce different results even
on the same benchmark. Some come from deterministic checks such as unit tests
or exact answers, while others rely on LLM judges to evaluate outputs that are
subjective or open-ended.
Is partial success rewarded?
Some benchmarks score each task as all-or-nothing while others may assign
partial credit for getting part of the way there. The difference matters most
for agents because they’re often used for tasks that have several steps. A high
partial-credit score can hide an agent that rarely completes a task end to end,
which is usually what you need it to do.
Which agentic harness was used?
The same model can post different scores on a benchmark depending on the
agentic harness it runs in. How the harness constructs prompts, parses tool calls,
handles retry logic, and manages context and conversation history all move the
number even with the model held fixed. The SWE Atlas benchmark paper shows
this directly: it runs each frontier model both in its vendor harness (Codex
CLI, Claude Code, Gemini CLI) and in a common minimal harness (mini-SWE-
agent, which exposes only a bash tool) to separate the model from its scaffold.
Scores shift between the two, and the ranking of the top models can even flip, so
a reported number is best read as a model-and-harness pair.
Single run or multiple?
A score from one run can flatter a lucky result. More trustworthy results would
often report a metric that aggregates the score over many runs with a variance
estimate. Some metrics are aggregate in nature, such as pass@k (pass-AT-k),
which we’ll see in the next section.
Is the benchmark in the training data?
Data contamination is one of the most insidious issues in machine learning. If
a model was trained on examples drawn from the benchmark, then the score
is skewed by the model’s memorization instead of being strictly measured on
capability. This is hard to verify aside from completely open models that disclose
the training datasets in detail.
|
Chapter 7: Evaluating Agents

Who ran the evaluation?
Self-reported scores from the lab releasing a model deserve more scrutiny than
third-party replications. Independent evaluations sometimes find meaningful
gaps from the reported numbers, even with identical setup. Artificial Analysis and
Chatbot Arena are two widely cited independent sources. Yet even independent
leaderboards can be gamed, as described in The Leaderboard Illusion.1
Were prompts tuned specifically for that benchmark?
Prompt engineering against a known benchmark can meaningfully move scores
without reflecting any generalizable capability improvement. If the same prompt‐
ing approach is not applied to all systems in the comparison table, the compari‐
son can be uneven.
Does the scaffolding generalize?
A system that includes a retrieval pipeline, a custom tool, or a verification step
may score well on the benchmark while requiring significant engineering to
transfer to a real deployment. When the scored evaluation system includes extra
scaffolding, the question worth asking is whether that scaffolding transfers to
your use case or was engineered specifically to perform well on this benchmark.
Is the benchmark saturated?
Once leading models exceed a certain threshold, say 85%, on a benchmark, score
differences start to become noisy and less indicative of actual performance. That’s
when you see the industry move to a more difficult benchmark (or variant)
tackling the next level of difficulty in that type of task.
Which subset or variant was used?
Many benchmarks have multiple versions that often vary in difficulty. Examples
include GPQA versus GPQA Diamond, ARC Easy versus ARC Challenge, and
MMLU versus MMLU-Pro.
What was the cost?
A system that scores 20% more while spending 10 times the tokens or wall-clock
time of a competitor isn’t straightforwardly better. Some evaluations report this;
many don’t. Cost, token count, and latency all matter in your production system
more than they might in the evaluation setup.
1 Singh, Shivalika et al. 2025. “The Leaderboard Illusion,” arXiv, 2504.20879.
Public Benchmarks and Leaderboards
|