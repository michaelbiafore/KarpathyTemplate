# Context Management → Afterword (Chapter 10, cont.)

## Context Management

Long engineering trajectories collide with the context window and with the cost and latency of very long prompts. Much of a code agent's context is static — persona, tool descriptions, security policy, repository structure — and that repetition is what makes prefix caching (kv-, prompt-, or prefix-caching) pay. A first call can already run to tens of thousands of tokens and recur across dozens of steps. Caching works only if the cached prefix stays byte-identical and new input is appended at the end, so the cache should grow to cover the whole prior trajectory.

![Figure 10-11: Serving the entire accumulated context from cache to optimize latency and](images/fig_10-11_Serving_the_entire_accumulated_context_f.png)
*Figure: By the third LLM call, everything accumulated over the earlier steps is served from cache as a single block, leaving only new output to compute.*

Two further levers: the **repository map** (Gitingest's directory dump; Aider's AST-derived signatures ranked by how widely a definition is used; or LLM-summarized files, as in CodeMonkeys, where amortizing across many sampled candidates keeps that read to ~15% of budget), and **context compaction**, which for code should preserve environment, style, test, and commit preferences. The two compose if the trajectory is partitioned by change frequency.

![Figure 10-13: Dividing a trajectory into static, slow-changing, and fast-changing sections](images/fig_10-13_Dividing_a_trajectory_into_static_slow-c.png)
*Figure: Static (instructions, persona, tool schemas), stable (task and plan), and dynamic (tool calls, responses, environment state) sections — only the last needs to churn.*

## Code Agents for Software Engineering

With an engineer as user, the agent moves from autocomplete to multi-file repository work. Early systems needed scaffolding — SWE-agent's purpose-built Agent-Computer Interface — while newer ones need less, because their models are trained on tool use and multi-step trajectories directly. The demand is for engineering skills: environment management, testing, debugging, reproducing bugs.

![Figure 10-14: The shift from writing isolated functions to full-scale software engineering](images/fig_10-14_The_shift_from_writing_isolated_function.png)
*Figure: One prompt yielding a LeetCode-style function, versus a GitHub issue driving an agent with code tools and a VM through N plan-and-think steps to a repository diff.*

SWE-bench made this measurable and competitive: real open source issues, each with a repo snapshot and the project's own tests, graded by running them. Planning became central — plans get revisited and revised, often delegated to the best available model, and must budget for exploration rather than assuming the approach is clear.

## Task-Specific Workflows

A fixed workflow often beats an agent. **Agentless** localizes relevant code, repairs by sampling several candidate patches, then selects using LLM-generated unit tests.

![Figure 10-16: Agentless resolves an issue in three fixed phases: localize the relevant code,](images/fig_10-16_Agentless_resolves_an_issue_in_three_fix.png)
*Figure: Localization, repair into multiple candidates, and patch selection where generated tests pick the winner.*

Two transferable ideas: sample at a temperature allowing variety, and treat generated tests as a ranking signal, not pass/fail — the winner need only pass more than its rivals. The chapter then gives TinyAgent `read_file`, `list_files`, `write_file`, and `execute_python` (the unsafe two behind `requires_approval`) plus an ANSI-colored `Display` and a terminal CLI.

![Figure 10-17: Running TinyAgent surfaces each step of its reasoning loop, showing the](images/fig_10-17_Running_TinyAgent_surfaces_each_step_of.png)
*Figure: The finished CLI agent listing a directory, with colored THOUGHT, ACTION, and OBSERVATION blocks.*

## Building Code LLMs

Agent quality is capped by model quality. Qwen3 Coder pre-trains on 7.5T tokens, 70% code; training data must look like deployment (tool-use trajectories, multi-step bug-fix sequences, code with its tests, issues with their diffs); and large-scale RLVR replaces RLHF polish, turning code's verifiability into a training signal.

![Figure 10-19: The specific types of code-related datasets used during each stage of](images/fig_10-19_The_specific_types_of_code-related_datas.png)
*Figure: Code datasets mapped to each stage, with reasoning, multi-step tool use, and other capabilities running underneath all of them.*

GLM-5 sizes the effort: ~28T pre-training tokens, mid-training to 200K context, SFT, then reasoning/agentic/general RL and distillation. Since ~2024, each model generation increasingly trains the next — Llama 3 for 3.1, Qwen2.5-Coder for Qwen3, DeepSeek-R1-Zero's traces.

## Summary

Code agents extend generation into write-execute-debug-iterate loops useful to non-coders too. The chapter covered tools and their security trade-offs under least privilege, context management, the engineer-facing shift and SWE-bench, agentless workflows, the TinyAgent build, and the model underneath.

## Afterword

The closing argument is about obligation, not technology. Buying the book was the last transaction in it; everything else arrived as a gift, hand-to-hand from people who worked something out and wrote it down instead of keeping it. Borrowing Robin Wall Kimmerer's distinction: a transaction is even and closes, a gift is uneven and never closes, asking only that it keep moving — held still, it rots. The book hands itself on as such a gift, traveling to people the reader will never see and for which the reader answers. Build well; make something that outlasts the book and its authors' names.
