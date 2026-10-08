---
title: "Agents That Continuously Improve"
chapter_number: 94
page_start: 270
page_end: 270
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Agents That Continuously Improve

the curtain. If we had jumped directly into native capabilities, much of the behavior
would have seemed like a closed box.
Agents That Continuously Improve
As AI agents evolve, instead of relying on training phases or reward models for
improvement, these systems start relying on self-generated feedback loops to con‐
tinuously improve their performance as they act. Feedback prevents agents from
ending up in local minima and provides valuable information on potentially better
solutions to pursue. In practice, not all feedback is equivalent, and continuous self-
improvement is tricky to pursue for LLMs that are fundamentally static when they
act. In this section, we explore methods for AI agents to reflect on their behavior and
pursue self-improvement as they act with their environment(s).
Reflection
The feedback that an agent gets from its environment is typically different from
process feedback. The environment gives feedback based on an action: “When I do
X (action), the environment gives back Y (feedback).” Feedback, as covered in this
section, is often referred to as “reflection” to demonstrate that it is typically an
internal process where the LLM should be critical of its own output and processes.
After all, reflecting on past behavior helps us learn from prior failings. Reflection,
however, can also be in tandem with external sources to supply feedback.
The techniques covered in this section are all based on prompting techniques and are
therefore relatively straightforward to implement.
Self-Refine
An elegant approach to feedback is Self-Refine,13 a prompting framework where the
LLM provides feedback and refines its own results. The approach is quite straightfor‐
ward and lets an LLM iteratively improve its answer by acting as its own editor. The
idea was inspired by how people draft and revise their solutions.
In this framework, the LLM generates an initial answer and then proceeds to critique
its own output (feedback). Based on that reflection step, the LLM refines its answer
and incorporates the necessary change (refine). This cycle repeats until a stopping
criterion has been reached, such as the number of steps or an LLM-guided stopping
mechanism. This cycle between feedback and refine is shown in Figure 6-18.
13 Madaan, Aman et al. 2023. “Self-Refine: Iterative Refinement with Self-Feedback,” Advances in Neural Infor‐
mation Processing Systems, 36: 46534-46594.
|
Chapter 6: Planning and Reflection