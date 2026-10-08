---
title: "Planning"
chapter_number: 91
page_start: 244
page_end: 244
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Planning

This plan and the steps that it contains can often be taken multiple times, such as
implementing and testing the feature whenever the agent encounters a bug. Iterative
loops are similarly a fundamental component of what makes an agent. As such, the
initial plans are made malleable and should be open to change when there is an issue
with the plan or its execution. Reflection on what has been done and what could
be improved is, therefore, vital for the autonomous nature of the agent. Planning
and reflection go hand in hand, and by implementing a feedback loop, the system
prevents ending up in a local minimum.
In this chapter, we explore planning and reflection in agents and how they can be
used to plan out multi-step actions and improve their behavior as they go through the
necessary steps. This brings us to the final component of a single agent (Figure 6-1).



![Figure 6-1: Planning is the final core component of a single agent](images/fig_06-01_Planning_is_the_final_core_component_of.png)

*Figure 6-1: Planning is the final core component of a single agent*


Figure 6-1. Planning is the final core component of a single agent
Planning
In Chapter 3, we explored how reasoning and extended thinking can bring LLMs to
new heights. We briefly touched upon something vital in these systems, namely that
advanced reasoning allows LLMs to plan out their behavior. There is a wide variety of
methodologies to enable planning in reasoning LLMs effectively.
|
Chapter 6: Planning and Reflection