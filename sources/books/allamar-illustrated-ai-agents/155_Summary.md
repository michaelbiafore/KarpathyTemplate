---
title: "Summary"
chapter_number: 155
page_start: 434
page_end: 436
part: "Part II. Specialized Agents"
---
# Summary



![Figure 10-21: A synthetic data generation recipe uses those models to produce data](images/fig_10-21_A_synthetic_data_generation_recipe_uses.png)

*Figure 10-21: A synthetic data generation recipe uses those models to produce data*


Figure 10-21. A synthetic data generation recipe uses those models to produce data
that feeds both pre-training and post-training across categories like code, reasoning,
multi-step tool use, and more
If you want a closer look at synthetic data generation, several open source projects
share code and details on these pipelines. This includes NVIDIA’s Nemotron 3
Nano and Nemotron 2 Nano, AI21 “Scaling Text-Rich Image Understanding via
Code-Guided Synthetic Multimodal Data Generation” (GitHub), and “OmniSQL -
Synthesizing High-quality Text-to-SQL Data at Scale” as some examples with scripts.
Summary
In this chapter, we examined how code agents are among the most impactful cat‐
egories of AI agents. We saw how they extend basic LLM code generation into
multi-step problem-solving by writing code, executing it, debugging failures, and
iterating until a larger task is completed. We stressed how general users, not just
software developers, stand to benefit, starting with a data analysis example in which a
non-coder never has to see the code.
We then broke down the core tool and environment design space that lets a code
agent act on the world. We saw building blocks such as file manipulation tools, sand‐
boxed code interpreters, and command-line access to dedicated virtual machines,
along with the security trade-offs each one carries and the principle of least privilege
that helps manage them. We also highlighted computer-use tools that let a model
interact with GUIs, code search methods that go beyond text matching, and SQL
tools that connect agents to organizational databases.
From there we turned to how software engineering agents manage their context,
using prompt caching, repository maps, and context compaction to keep long
|
Chapter 10: Code Agents and Code LLMs

trajectories affordable. We looked at what changes when the user is a software
engineer instead of a non-coder, how benchmarks such as SWE-bench frame the
task as resolving a real GitHub issue until its tests pass, and how planning, memory,
and task-specific workflows like agentless tackle that task, sometimes without a full
agent at all.
We then pulled these threads together and built a coding agent ourselves, extending
the TinyAgent from earlier chapters with file and code-execution tools and a terminal
interface so you could watch its THOUGHT, ACTION, and OBSERVATION loop
run in your own environment.
Finally, we went underneath the agent to the model that powers it. We outlined how
a coding LLM is built across pre-training, SFT, and RL, why these models need far
more code, tool-use, and software engineering data than a generalist, and how rein‐
forcement learning with verifiable rewards turns the chapter’s opening observation,
that code can be checked by running it, into a training signal. We closed on the
synthetic data feedback loop, where each generation of models increasingly trains the
next.
Summary
|