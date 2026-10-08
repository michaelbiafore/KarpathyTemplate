# Chapter 6 Bundle: Planning and Reflection → Task Decomposition

## Chapter 6. Planning and Reflection

Agents are multi-step entities, and advanced reasoning (Chapter 3) is what lets them plan actions and reflect on them. The chapter's running example is asking an agent to add a feature to a codebase: it must clarify requirements, analyze the existing codebase, design the feature, implement it, test it, and update documentation. To execute that sequence the agent has to be aware of the steps and track its current state. Without a plan, it has no basis for deciding what to do next.

## Planning

Steps are rarely taken once — implement and test recur every time a bug surfaces — so iterative loops are a fundamental part of being an agent. Initial plans must therefore stay malleable, revisable whenever the plan or its execution runs into trouble. Reflection on what has been done and what could be improved is what makes that autonomy work; planning and reflection operate as a feedback loop that keeps the system out of a local minimum. Planning is the last of the core single-agent components the book covers.

![Figure 6-1: Planning is the final core component of a single agent](images/fig_06-01_Planning_is_the_final_core_component_of.png)

*Figure: The single-agent block diagram — user query into a reasoning LLM backed by Memory, Tools, and Planning, acting on an environment and consuming its feedback — with Planning highlighted as the Chapter 6 component.*

## Task Decomposition

Planning begins by decomposing a query into subtasks, each of which may carry subtasks of its own, so that a complicated goal becomes a set of simple ones.

![Figure 6-2: The reasoning LLM turning a user’s query into a structured plan of steps](images/fig_06-02_The_reasoning_LLM_turning_a_users_query.png)

*Figure: "Add a new feature" becomes a six-item checklist plan, with "Update documentation" expanded to show nested subtasks like updating the README, API docs, and changelog.*

The plan comes first; each (sub)task is then executed, often via a tool call, after which the agent may revise the plan and move on. Prompt engineering supplies the decomposition. Chain-of-Thought — few-shot examples or simply "let's think step-by-step" — is itself task decomposition, breaking a problem into sequential reasoning substeps that each build on the last; a reasoning trace produced this way can be converted directly into a checklist plan. CoT variants sample multiple traces to find the best one: self-consistency generates diverse paths and takes a majority vote, while Tree of Thoughts explores a branching space of thoughts, selected with Beam Search or Monte Carlo Tree Search over reward models.

![Figure 6-5: Four ways to handle a query: regular prompting, Chain-of-Thought, Self-](images/fig_06-05_Four_ways_to_handle_a_query_regular_prom.png)

*Figure: Four side-by-side topologies from query to answer — a direct arrow, a linear thought chain, three parallel chains resolved by majority vote, and a branching tree with pruned paths.*

Two techniques make the planning explicit. Least-to-most (LtM) prompting first reduces the problem to subproblems, then solves them one at a time, feeding each previous question and answer into the next prompt — unlike CoT's single linear trace. It is driven by few-shot examples.

![Figure 6-6: While Chain-of-Thought produces a linear trace, least-to-most prompting](images/fig_06-06_While_Chain-of-Thought_produces_a_linear.png)

*Figure: CoT's single thought chain contrasted with LtM's two-column structure, where each subtask's answer loops back into the next subtask's prompt.*

Plan-and-solve prompting is the zero-shot counterpart: instead of "let's think step-by-step," the model is asked to devise a plan and then carry it out, followed by an answer-extraction pass.

![Figure 6-8: Plan-and-solve prompting on a math problem, where the plan and execution](images/fig_06-08_Plan-and-solve_prompting_on_a_math_probl.png)

*Figure: A cookie word problem where one LLM call emits a Plan, an Execution, and an Answer section, and a second "therefore, the answer is" call extracts the final value.*

These Q/A-style prompts reflect early LLMs trained mainly to autocomplete. Modern models plan well without such scaffolding — but, as Chapter 3 argued, only because they were trained on CoT- and planning-like reasoning traces.
