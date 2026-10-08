---
title: "Code Agents for Software Engineering"
chapter_number: 152
page_start: 417
page_end: 419
part: "Part II. Specialized Agents"
---
# Code Agents for Software Engineering



![Figure 10-13: Dividing a trajectory into static, slow-changing, and fast-changing sections](images/fig_10-13_Dividing_a_trajectory_into_static_slow-c.png)

*Figure 10-13: Dividing a trajectory into static, slow-changing, and fast-changing sections*


Figure 10-13. Dividing a trajectory into static, slow-changing, and fast-changing sections
to maximize caching efficiency
Code Agents for Software Engineering
When the end user is a software engineer, code agents take on a completely different
nature. For most developers now, their first encounter with a code agent is inside
their IDE or code editor. These tools started by surfacing LLM code generation
features such as autocompletion, which can be handy in writing documentation or
writing a first draft of a function if we write the function signature first. Eventually,
agents started offering the capability to solve more complex problems that would
require editing code in multiple places to solve more challenging problems than what
autocomplete can do on its own.
The first generations of agents needed to be guided closely because this task took
on a different nature that’s not as well represented in their training data. Early
systems compensated with heavy external scaffolding. The original SWE-agent, for
instance, introduced a purpose-built Agent-Computer Interface, a constrained set of
commands designed to make a repository navigable for a model that couldn’t reliably
do it on its own. Newer agents rely far less on this kind of handholding because the
models powering them are now trained directly on tool use, multi-step trajectories,
and software engineering tasks, as we’ll see later in this chapter.
Building Code Agents
|

Going from writing function-level code to creating or making changes to entire
repositories requires a different set of skills, even if it’s all about writing code in
the end. A code agent needs software engineering skills, which include skills like
environment management, unit testing, debugging and troubleshooting, and the
ability to reproduce bugs and investigate what causes them, which entails reading
enough of the right places of the repository to understand the intention and flow of
the program.
Figure 10-14 shows this evolution in the nature and scope of code problems from
solving individual LeetCode-style problems to software engineering problems, as
we’ll see in the next section.



![Figure 10-14: The shift from writing isolated functions to full-scale software engineering](images/fig_10-14_The_shift_from_writing_isolated_function.png)

*Figure 10-14: The shift from writing isolated functions to full-scale software engineering*


Figure 10-14. The shift from writing isolated functions to full-scale software engineering
tasks requiring plan-and-code cycles
|
Chapter 10: Code Agents and Code LLMs

SWE-bench: code problems at the level of a GitHub issue
The SWE-bench benchmark was the first widely adopted code agent benchmark.4 It
is a collection of hundreds of software engineering issues collected from open source
repositories and actual issues reported by users. In each example, a single GitHub
issue is presented to the code agent alongside a snapshot of the repository at a specific
point in time. The model then has to resolve that issue in a way that passes a set of
test suites that verify the correctness of the fix.
SWE-bench caught on because it measures something real: the issues come from
actual open source projects, and each one ships with the repository’s own test suite,
so a fix can be graded objectively by running the tests rather than judged subjectively.
That verifiability, the same property that makes code a tractable target for LLMs in
the first place, together with the fact that early systems solved only a small fraction
of the issues and so left plenty of headroom, is what turned it into the number labs
compete on.
Planning for software engineering agents
Because agents tackle larger scale problems that often require multiple steps, the
planning step emerged as a key component of these systems. A coding agent often
has to not only write a detailed plan with concrete steps but also keep returning to
the plan and updating its status or even the entire plan as it learns more about the
task. The UIs for code agents started showing plans and to-do-list items as distinct
elements so the user keeps track of them (Figure 10-15).
4 Jimenez, Carlos E. et al. 2023. “SWE-bench: Can Language Models Resolve Real-World GitHub Issues?” arXiv,
2310. 06770.
Building Code Agents
|