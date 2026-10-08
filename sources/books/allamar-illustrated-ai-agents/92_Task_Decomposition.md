---
title: "Task Decomposition"
chapter_number: 92
page_start: 245
page_end: 251
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Task Decomposition

Task Decomposition
The first step in planning is to decompose an initial query into subtasks. Like the
example at the beginning of the chapter, when you ask an agent to create a certain
feature, it will split that query up into smaller tasks to execute. This is called task
decomposition and allows the agent to simplify complicated tasks.1 Figure 6-2 shows
an example of the reasoning LLM creating this plan, where each task may also have a
set of subtasks to complete.



![Figure 6-2: The reasoning LLM turning a user’s query into a structured plan of steps](images/fig_06-02_The_reasoning_LLM_turning_a_users_query.png)

*Figure 6-2: The reasoning LLM turning a user’s query into a structured plan of steps*


Figure 6-2. The reasoning LLM turning a user’s query into a structured plan of steps
The tasks and subtasks in this plan may describe a tool that the reasoning LLM may
use. As shown in Figure 6-3, the plan comes first, after which each (sub)task can be
processed using tools. In this example, the agent creates a three-step plan to add a
new feature to a codebase. The first task, analyzing the existing codebase, is done with
a tool call to retrieve the code. It continues to analyze that code and communicate the
core features. After that, it may update the plan and continue with the next task.
1 Huang, Xu et al. 2024. “Understanding the Planning of LLM Agents: A Survey,” arXiv, 2402.02716.
Planning
|



![Figure 6-3: Combining planning with tool use, where the agent decomposes a goal into a](images/fig_06-03_Combining_planning_with_tool_use_where_t.png)

*Figure 6-3: Combining planning with tool use, where the agent decomposes a goal into a*


Figure 6-3. Combining planning with tool use, where the agent decomposes a goal into a
multi-step execution plan
Chain-of-Thought
A major component of task decomposition, aside from having a reasoning LLM, is
prompt engineering. We covered several of them in Chapter 3 from the perspective
of reasoning traces, where several “thoughts” are sampled. We also covered Chain-of-
Thought (CoT) as a common approach to create these reasoning traces. Remember
that CoT is a process where the LLM is asked to solve problems step-by-step. This
can be achieved by either providing examples to the LLM (few-shot prompting) or
by simply stating, “Let’s think step-by-step” (zero-shot prompting). This step-by-step
process is, in fact, task decomposition. The original query is processed through
separate reasoning traces that rely on the ones that came before (Figure 6-4). In other
words, it breaks down the problem into sequential reasoning substeps.
|
Chapter 6: Planning and Reflection



![Figure 6-4: Chain-of-Thought carries out task decomposition in its reasoning steps by](images/fig_06-04_Chain-of-Thought_carries_out_task_decomp.png)

*Figure 6-4: Chain-of-Thought carries out task decomposition in its reasoning steps by*


Figure 6-4. Chain-of-Thought carries out task decomposition in its reasoning steps by
prompting the LLM to “think step-by-step”
The original idea of CoT was to make the model “think aloud” as a way to scale
test-time compute and its performance. However, the “thinking” may very well be
used as part of the planning process. For instance, when asked to create a plan and
end it with “think step-by-step,” a reasoning LLM will first think about the steps
needed to resolve the original query. This is the reasoning trace the LLM can leverage
to create the plan:
User: Add a new feature to my existing codebase. Let's think step-by-step.

LLM (CoT):
First, I need to clarify the requirements. What kind of feature is needed?
Second, I should analyze the existing codebase to understand the architecture.
Third, I need to design the feature and make sure nothing is left out.
Fourth, I should implement the feature in the existing codebase but without
changing its original functionality.
Fifth, I must test the feature thoroughly through unit and integration tests.
Finally, I need to update the documentation to explain how the new feature works.

LLM (Plan):
The plan will be as follows:

[ ] Clarify requirements
[ ] Analyze the existing codebase
[ ] Design the feature
[ ] Implement the feature
[ ] Test the feature
[ ] Update documentation
As such, CoT is a flexible technique that can be used for task decomposition in
general, not just for “thinking aloud.”
Planning
|

Since CoT, there have been many variants that similarly attempt to create more
advanced reasoning traces for the purpose of task decomposition. These techniques,
such as self-consistency and tree of thoughts,2,3 sample multiple CoT traces from the
LLM to find the most optimal trace. As shown in Figure 6-5, the original task is
decomposed into “thoughts” (but could have been subtasks just the same), and from
various “thoughts,” the most optimal set is chosen.



![Figure 6-5: Four ways to handle a query: regular prompting, Chain-of-Thought, Self-](images/fig_06-05_Four_ways_to_handle_a_query_regular_prom.png)

*Figure 6-5: Four ways to handle a query: regular prompting, Chain-of-Thought, Self-*


Figure 6-5. Four ways to handle a query: regular prompting, Chain-of-Thought, Self-
consistency, and Tree of Thoughts
For self-consistency, the original task is broken down into subtasks, much like CoT,
but multiple diverse paths are generated, and the most consistent answer is selected.
In contrast, Tree of Thoughts explores multiple possible reasoning paths (where each
node is a task or “thought”) instead of following a linear chain-of-thought. As we
explored in Chapter 3, methodologies like Beam Search and Monte Carlo Tree Search
using reward models can be used to choose the best path.
Explicit planning
A CoT-like prompting technique for task decomposition that works quite well in the
context of planning is least-to-most (LtM) prompting.4 Released in 2022, LtM builds
2 Wang, Xuezhi et al. 2022. “Self-consistency Improves Chain of Thought Reasoning in Language Models,”
arXiv, 2203.11171.
3 Yao, Shunyu et al. 2023. “Tree of Thoughts: Deliberate Problem Solving with Large Language Models,”
Advances in Neural Information Processing Systems, 36: 11809-11822.
4 Zhou, Denny et al. 2022. “Least-to-Most Prompting Enables Complex Reasoning in Large Language Models,”
arXiv, 2205.10625.
|
Chapter 6: Planning and Reflection

upon CoT by first decomposing the problem into subproblems. Then, these subpro‐
blems are solved one by one. Compared to CoT, the solution of each subproblem is
fed back into the LLM when attempting to solve the next problem (Figure 6-6).



![Figure 6-6: While Chain-of-Thought produces a linear trace, least-to-most prompting](images/fig_06-06_While_Chain-of-Thought_produces_a_linear.png)

*Figure 6-6: While Chain-of-Thought produces a linear trace, least-to-most prompting*


Figure 6-6. While Chain-of-Thought produces a linear trace, least-to-most prompting
explicitly decomposes a problem and solves subproblems sequentially
As in CoT prompting, the problem to be solved is decomposed into a set of subpro‐
blems that build upon each other. In a second step, these subproblems are solved one
by one. Contrary to CoT, the solution of previous subproblems is fed into the prompt,
trying to solve the next problem.
A more practical example is shown in Figure 6-7, where instead of attempting to
solve the problem directly, two stages are executed:
Problem reduction
The original problem is decomposed into a set of manageable tasks.
Sequentially solve subquestions
Each subtask is solved after the other. After each subtask, the previous subtask’s
question and answer are appended.
Planning
|



![Figure 6-7: Least-to-most prompting on a math word problem, solving subquestions](images/fig_06-07_Least-to-most_prompting_on_a_math_word_p.png)

*Figure 6-7: Least-to-most prompting on a math word problem, solving subquestions*


Figure 6-7. Least-to-most prompting on a math word problem, solving subquestions
step-by-step to arrive at the final answer
To create this behavior, few-shot prompting is used, where examples are provided to
the LLM to show how to decompose the initial tasks and subsequently solve them.
A zero-shot approach to task decomposition in the context of planning is plan-and-
solve prompting.5 This methodology is a direct extension of the zero-shot CoT, where
instead of using “Let’s think step-by-step,” the LLM is asked to devise a plan first and
then solve the problem step-by-step (Figure 6-8). It’s a two-step process that is akin to
the thinking and answer steps that we explored in Chapter 3:
5 Wang, Lei et al. 2023. “Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by
Large Language Models,” arXiv, 2305.04091.
|
Chapter 6: Planning and Reflection

Prompting for reasoning generation
The model generates a plan and then carries it out by solving the problem
step-by-step.
Answer extraction
The output of the previous step is processed to create the final answer.



![Figure 6-8: Plan-and-solve prompting on a math problem, where the plan and execution](images/fig_06-08_Plan-and-solve_prompting_on_a_math_probl.png)

*Figure 6-8: Plan-and-solve prompting on a math problem, where the plan and execution*


Figure 6-8. Plan-and-solve prompting on a math problem, where the plan and execution
happen within a single reasoning step
Note how we again used the Q/A structure throughout these prompts. That was
common in these early days of LLMs, where they were often trained primarily
to autocomplete the prompt, so additional steering was needed for the model to
understand that it should answer a given question. Their output is essentially the
“thinking” process we know of reasoning LLMs, but it works just the same for regular
LLMs, albeit an implicit process. Nowadays, most LLMs are already capable of creat‐
ing advanced plans without needing complex instructions or specialized prompts.
However, as explored in Chapter 3, they often need to be trained on these CoT- or
planning-like reasoning traces to effectively reason and plan.
Planning
|