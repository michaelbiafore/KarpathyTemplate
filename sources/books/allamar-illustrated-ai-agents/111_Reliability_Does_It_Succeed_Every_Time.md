---
title: "Reliability: Does It Succeed Every Time?"
chapter_number: 111
page_start: 303
page_end: 303
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Reliability: Does It Succeed Every Time?



![Figure 7-9: Three correct outcomes, three different problems in the trajectory. Agent A](images/fig_07-09_Three_correct_outcomes_three_different_p.png)

*Figure 7-9: Three correct outcomes, three different problems in the trajectory. Agent A*


Figure 7-9. Three correct outcomes, three different problems in the trajectory. Agent A
guessed and got lucky, Agent B spent several tool calls where one would do, and Agent
C made the right tool call but overthought its way there. Outcome evaluation passes all
three; only trajectory evaluation tells them apart.
These three failure modes are distinct enough to warrant separate measurement:
unsound reasoning, inefficiency, and unnecessary overhead. Measuring a trajectory
means scoring the steps along the way, not just the endpoint. A few axes do most of
the work. Did the agent reach for the right tools and pass them valid arguments? How
efficiently did it get there, in tool calls, steps, and reasoning tokens? Did each step
follow reasonably from what the agent learned in the steps before it?
These questions can be put to an LLM judge that is handed the full trajectory to
observe. As we saw earlier, that is a rubric, just one that examines the steps and
not just the final output. Works such as T-Eval (2024), AgentBoard (2024), TRACE
(2025), and AgentProcessBench (2026) formalize this approach, introduce measures
for individual steps in the trajectory, and show how this line of evaluation has been
tracking over the last several years.
Reliability: Does It Succeed Every Time?
Just like LLMs, agent outputs are stochastic: the same input can produce different
outputs across runs, which means a single run score can flatter or unfairly penalize
an agent. A better picture comes from running multiple trials of the same task and
measuring how often the agent succeeds. From these trials you can read two different
things: how capable the agent is, meaning whether it can succeed at all, and how
reliable it is, meaning whether it succeeds every time. The following two metrics
measure each.
Measuring Capability with pass@k
When evaluating agents on tasks with a clear pass or fail check, one metric stands
out for measuring capability while accounting for the probabilistic nature of the
underlying model.
Reliability: Does It Succeed Every Time?
|