---
title: "Software and Computer-Use Environments"
chapter_number: 102
page_start: 284
page_end: 284
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Software and Computer-Use Environments

Tool Use
Tool use benchmarks test whether an agent calls the right tools with the right argu‐
ments. This is a more targeted check on the specific capabilities of tool calling that we
covered in Chapter 5 instead of end-to-end task completion. BFCL (Berkeley Func‐
tion Calling Leaderboard) is one key benchmark here, testing function-calling accu‐
racy across hundreds of API schemas including nested parameters and ambiguous
inputs. τ bench (pronounced “tau bench”) goes deeper, testing tool use across realistic
multi-turn customer service scenarios that require following specific business policies
and maintaining context over a long conversation.
Software and Computer-Use Environments
A key and growing area of agent benchmarks is one where the agent must navigate a
digital environment such as a desktop, browser, or application interface and conduct
a sequence of actions to achieve a specific goal. Benchmarks such as OSWorld place
agents inside simulated computer environments where they must complete realistic
tasks such as editing documents, managing files, or configuring software. Unlike
Terminal-Bench, however, this group of benchmarks often requires interacting with
graphical interfaces, clicking buttons, navigating menus, and interpreting visual ele‐
ments that appear in software designed for humans (e.g., Excel or online shops).
The WebArena benchmark narrows the scope to browser-based tasks, placing agents
inside realistic replicas of live websites (such as a Reddit forum or a GitLab instance)
to complete multi-step goals.
Real-World Task Completion
For agents to rise to their promise of tackling productive knowledge work, some
benchmarks present the challenge of messy, open-ended tasks that look like the kinds
of work knowledge workers actually tackle. These tasks typically require a mixture of
reasoning, information retrieval, navigating ambiguity, and synthesis across multiple
steps and sources. GAIA is one such benchmark that presents difficult (at the time),
real-world questions that often require reading files and using web search to arrive
at a verifiable final answer. GDPval is another one drawn from knowledge work of
multiple professions from various sectors and domains.
We have good reason to believe there will continue to be increasing demand for this
category of evaluations. A 2026 analysis titled How Well Does Agent Development
Reflect Real-World Work? found that today’s benchmarks cluster heavily around pro‐
gramming, while the occupations that employ the most people and generate the most
economic value go almost untested. That gap is where much of the expected demand
for evaluations is likely to land.
|
Chapter 7: Evaluating Agents