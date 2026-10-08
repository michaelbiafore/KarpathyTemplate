---
title: "Summary"
chapter_number: 55
page_start: 150
page_end: 150
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Summary

Latent space reasoning is a relatively new field, and new technologies are seemingly
being released daily. One interesting perspective is how to balance the implicit and
explicit Chain-of-Thought-like behavior of an LLM, given what users might want to
see. There is a big advantage to actually seeing how a model reasons, as it will make
debugging much easier. However, reasoning in latent space can be a more efficient
process and does not limit the LLM to text-based reasoning. Imagine the LLM not
reasoning in text but in symbolic language instead, or perhaps purely in latent space
through mathematical equations.
Summary
In this chapter, we explored how LLMs could develop advanced reasoning. We first
covered the paradigm from a focus on train-time compute to test-time compute, of
which scaling reasoning is an important component. Reasoning is often shown as
either short or long Chain-of-Thought traces. We covered two broad categories for
scaling test-time compute. The first, search against verifiers, involved expanding the
output of LLMs dynamically through methods such as self-consistency and Best-of-N
samples. The second, modifying the proposal distribution, typically involves training
or fine-tuning an LLM to demonstrate advanced reasoning traces. We covered two
categories of modifying the proposal distribution, namely supervised fine-tuning
(e.g., Flan-PaLM, s1) and reinforcement learning (e.g., DeepSeek-R1 Zero, DeepSeek-
R1).
We ended the chapter by exploring upcoming fields in reasoning LLMs, including
reasoning in latent space, making reasoning more efficient, and methods for multi-
modal reasoning.
In the next three chapters, we start from reasoning LLMs and iteratively give them
more capabilities until they reach the state of being called an agent. In Chapter 4,
we explore methods to give them memory and track the actions they have taken. In
Chapter 5, we show how to give the tools to use and what best practices are for doing
so. In Chapter 6, everything comes together where advanced reasoning is used to
create plans for agents and reflect to them; reasoning LLMs are especially important
here.
|
Chapter 3: Reasoning Large Language Models