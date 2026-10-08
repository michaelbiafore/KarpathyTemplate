---
title: "Outcome Evaluation: Did the Agent Get the Right Output?"
chapter_number: 107
page_start: 288
page_end: 288
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Outcome Evaluation: Did the Agent Get the Right Output?

Outcome Evaluation: Did the Agent Get the Right Output?
The benchmarks we’ve looked at score models based on a number of scoring meth‐
ods. Understanding these methods is what lets you read a benchmark table critically
and design your own evaluations well. Outcome evaluation scores the final results of
a task—the patch produced, the answer returned, the report written—without regard
to how the agent got there. We contrast this with a smaller subsequent section on
trajectory evaluation, which examines the sequence of steps and tool calls the agent
made along the way.
Human Evaluation
The most direct way to score an agent’s output is to have a person read it and judge
it. Figure 7-3 shows the direct scoring, where a human evaluator/annotator reads the
output from an agent and assigns a score, say 4 out 5, based on some criteria.



![Figure 7-3: A human evaluator rates a single agent output against scoring criteria,](images/fig_07-03_A_human_evaluator_rates_a_single_agent_o.png)

*Figure 7-3: A human evaluator rates a single agent output against scoring criteria,*


Figure 7-3. A human evaluator rates a single agent output against scoring criteria,
producing a direct quality score
This works well when you have an absolute sense of quality and have clear criteria
that evaluators apply consistently. The challenge here is that it’s often difficult to get
an objective score in isolation, which creates the need for the second form of human
evaluation.
Preference evaluation, which we see in Figure 7-4, presents the evaluator with outputs
from two agents side-by-side on the same task and asks a simpler question: which
answer do you prefer? Relative judgments tend to be more reliable than absolute
ones. It’s easier for a human evaluator to say that “A is better than B” than to decide
that A deserves 4 points and that B deserves 3 points.
|
Chapter 7: Evaluating Agents