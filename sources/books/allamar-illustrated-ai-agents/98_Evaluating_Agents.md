---
title: "Chapter 7. Evaluating Agents"
chapter_number: 98
page_start: 281
page_end: 281
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Chapter 7. Evaluating Agents

Evaluating Agents
The previous chapters built up the components of an agent one by one: how it
reasons, how it uses tools, how it stores and retrieves memory, and how it plans
across multiple steps. By now you have a mental model of how these pieces fit
together to form the system we call an AI agent. The natural next question to ask is,
how do we know if any of it is working?
That’s what this chapter is about, as we can see in Figure 7-1. Evaluation is how
you move from “it seems to work” to “I have evidence it works.” It’s also how you
catch the moment it stops working. Evaluations are one of the most underinvested
areas in agent development. Teams often rely on manual testing and intuition longer
than they should, then find themselves unable to ship improvements confidently or
diagnose regressions when they appear.
We’ll start with benchmarks, which you’ll encounter most often in model announce‐
ments and research papers. We’ll then build toward the tools and concepts you need
to design your own evaluations. By the end of the chapter, you’ll have a clear picture
of how agents are measured and what those measurements actually mean.