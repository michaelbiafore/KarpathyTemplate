---
title: "Trajectory Evaluation: Did It Get There the Right Way?"
chapter_number: 110
page_start: 302
page_end: 302
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Trajectory Evaluation: Did It Get There the Right Way?

Trajectory Evaluation: Did It Get There the Right Way?
Outcome evaluation tells you whether the agent succeeded. Trajectory evaluation tells
you how it got there or how it failed. A trajectory is the full sequence of steps an agent
took: the reasoning it produced, the tools it called, the arguments it passed, and the
intermediate outputs it generated along the way.
One way to analyze an agent’s behavior is to look at statistics of its tool calls across a
number of runs. In Figure 7-8 from SWE-Atlas, we can see how three different agents
behave when tackling the same set of tasks. We can see the GPT-5.4 on the left tends
to search and conduct file operations heavily early in its trajectories and undertakes
execution steps after gaining enough context about the repo it’s operating in. We miss
such patterns if we look exclusively at outcomes.



![Figure 7-8: Tool-use distribution across the trajectory for three models on the same](images/fig_07-08_Tool-use_distribution_across_the_traject.png)

*Figure 7-8: Tool-use distribution across the trajectory for three models on the same*


Figure 7-8. Tool-use distribution across the trajectory for three models on the same
Codebase Q&A tasks under the mini-SWE agent scaffold. Adapted from M. Raghaven‐
dra et al., 2026, “SWE Atlas,” arXiv:2605.08366.
This is a way to read behavior across many runs at once. It’s often also useful to
examine trajectories individually.
In Figure 7-9, we can see multiple trajectories that pass outcome evaluation, but
trajectory inspection reveals deeper problems. In the first example, the agent output
was a lucky guess. In the second, the agent spends a large number of steps and tool
calls to arrive at an answer that should have only required one tool call. In the third,
the model overthinks before making the right tool call.
|
Chapter 7: Evaluating Agents