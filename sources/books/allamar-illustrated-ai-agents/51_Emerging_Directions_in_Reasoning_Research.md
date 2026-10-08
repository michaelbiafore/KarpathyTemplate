---
title: "Emerging Directions in Reasoning Research"
chapter_number: 51
page_start: 142
page_end: 142
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Emerging Directions in Reasoning Research

As such, any training and fine-tuning that we saw before can now be enabled by
the prompt template of that specific model. Instead of needing to use “tricks” like
Chain-of-Thought, the model was trained on Chain-of-Thought examples instead.
Emerging Directions in Reasoning Research
Reasoning in LLMs has started to advance beyond text-only reasoning, now using
new modalities, improved architectures, and more abstract ways of representing
information.
In this section, we look at three key areas pushing LLM reasoning forward:
Reasoning in multi-modal LLMs
Reasoning LLMs learn to reason with modalities other than text, like images,
audio, and video
Efficient reasoning
Focuses on improving reasoning while using less computation
Reasoning in latent space
Models think in compressed, abstract forms and often non-textual forms to reach
deeper insights
Reasoning in Multi-Modal LLMs
The LLMs serving as the main brains of agentic systems do not only need to reason
about text. They may need to think about the best way to design a website or interpret
what is happening in a given picture. This requires reasoning in ways that differ from
textual inputs as more modalities might be processed. As we will discuss in Chapter 9,
there are many methods for making LLMs multi-modal, which often naturally extend
them to include reasoning behavior. However, without any reasoning grounding,
performance on multi-modal reasoning tasks is usually worse.
As with mono-modal LLMs, reasoning is often enhanced through methods like those
we discussed before, such as prompting, search against verifiers, or modifying the
proposal distribution with supervised fine-tuning and/or reinforcement learning.
A common method for multi-modal prompting is called Multi-modal Chain-of-
Thought (MCoT). Multi-modal Chain-of-Thought, compared to traditional Chain-
of-Thought, attempts to incorporate text and vision into a two-stage framework.
As shown in Figure 3-42, Multi-modal Chain-of-Thought contains a two-step
approach where the first step creates reasoning by combining the original language
and visual input to produce an explicit reasoning process. In the second step, this
rationale is appended to the original language input and, together with the same
visual input, is used to infer the final answer. Both stages use models with the
|
Chapter 3: Reasoning Large Language Models