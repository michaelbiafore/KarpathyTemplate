---
title: "Safety: Does It Avoid Harm?"
chapter_number: 114
page_start: 308
page_end: 308
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Safety: Does It Avoid Harm?

Safety: Does It Avoid Harm?
Agents are more consequential than LLMs. Their actions could be sending a high-
impact email, deleting a file, or dropping an entire database. This is why safety
evaluation deserves its own place in your eval suite from the start.
“Safety” covers a few distinct questions, and the cleanest way to separate them is by
who, if anyone, is trying to cause the harm. Each is a different threat model with its
own metric, so you build test cases for the ones that match how your agent will be
used.
The first is misuse: a malicious user asks the agent to carry out a harmful task, and
the question is whether it refuses. Benchmarks such as AgentHarm measure this with
a refusal rate and a harm score.
The second is manipulation through the data the agent reads. Prompt injection
plants instructions in content the agent processes, such as a retrieved document, a
tool result, or a web page, to hijack its behavior. Memory poisoning corrupts what
the agent stores and later retrieves, so it acts on false premises many steps later.
AgentDojo and Agent Security Bench (ASB)4,5 measure these and report an attack
success rate; ASB covers both surfaces, while AgentDojo focuses on prompt injection
and also tracks whether the agent stays on its real task while resisting.
The third has no adversary at all: on a benign task, the agent harms the user through
its own error, deleting the wrong files or taking an irreversible step it should have
paused on. This is the least standardized of the three, and it leans on your own test
cases, guardrails, and harness choice and design.
Building Your Own Evals
The best signal you’ll get about how well an agent matches your target task is to
build your own evaluation that’s actually representative of the specific problem you’re
building for. A small, well-curated set of test cases that reflect real usage and data will
help you pick the best LLM and agent framework for your deployment, as well as
help you catch regressions when you update any part of the system.
Aim for cases that capture a wide set of failure modes and edge cases, not just
successes. You can score these tests using a collection of the methods we’ve outlined
earlier in the section “Outcome Evaluation: Did the Agent Get the Right Output?”
on page 268: exact match, programmatic checks, LLM-as-a-judge, and rubrics. And
4 Debenetti, Edoardo et al. 2024. “AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks
and Defenses for LLM Agents,” arXiv, 2406.13352.
5 Zhang, Hanrong et al. 2024. “Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and
Defenses in LLM-based Agents,” arXiv, 2410.02644.
|
Chapter 7: Evaluating Agents