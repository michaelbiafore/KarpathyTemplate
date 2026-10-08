---
title: "Efficient Reasoning"
chapter_number: 53
page_start: 145
page_end: 146
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Efficient Reasoning

Efficient Reasoning
Scaling test-time compute can significantly improve performance and has been a
main focus of scaling LLMs. However, it can be quite expensive to calculate these
additional thousands of tokens or to explore multiple solutions and reasoning
paths. Consequently, there has been a growing interest in strategies that achieve
similar gains but through more select reasoning and adaptive computation. Typically,
this involves reducing the length of the reasoning trace. A nice example is the
ever-increasing length of reasoning we explored in DeepSeek-R1. If left without any
additional constraints, reasoning LLMs might learn to create unnecessarily large
reasoning traces during reinforcement learning.
The most straightforward method to reduce the reasoning length is through prompt‐
ing. Traditionally, Chain-of-Thought-like prompting techniques emphasize verbose,
step-by-step reasoning, which can create long and expensive reasoning traces that
contain redundant information. Chain-of-Draft (CoD), inspired by human cognitive
processes, instead employs a more efficient strategy by drafting concise intermediate
thoughts.17
In Figure 3-45, you can see the system prompts used for Chain-of-Draft compared
to regular prompting and Chain-of-Thought. Note how similar it is to Chain-of-
Thought, but it adds that each reasoning step should be kept to a draft and use five
words at most. Other values are possible, but the authors of Chain-of-Draft used five
words as a general guideline to create short prompts rather than strictly enforcing it.



![Figure 3-45: Comparing a standard prompt with Chain-of-Thought and Chain-of-Draft](images/fig_03-45_Comparing_a_standard_prompt_with_Chain-o.png)

*Figure 3-45: Comparing a standard prompt with Chain-of-Thought and Chain-of-Draft*


Figure 3-45. Comparing a standard prompt with Chain-of-Thought and Chain-of-Draft
Compared to Chain-of-Thought, Chain-of-Draft generates shorter reasoning traces
with less verbosity while having similar performance (shown in Figure 3-46).
The balance between minimizing verbosity and keeping the accuracy of reasoning
traces is difficult to maintain in Chain-of-Draft. Moreover, it is more difficult to read
for users compared to the verbose reasoning traces of traditional Chain-of-Thought.
The length of reasoning traces can also be controlled more directly during training.
These are often referred to as token-budget-aware LLMs that have been trained to
17 Xu, Silei et al. 2025. “Chain of Draft: Thinking Faster by Writing Less,” arXiv, 2502.18600.
Emerging Directions in Reasoning Research
|

adaptively change the length of the reasoning trace they create based on the complex‐
ity of the initial problem. Likewise, they may be trained to prefer shorter reasoning
traces through specific length rewards.



![Figure 3-46: Comparing the processes of Chain-of-Thought and Chain-of-Draft](images/fig_03-46_Comparing_the_processes_of_Chain-of-Thou.png)

*Figure 3-46: Comparing the processes of Chain-of-Thought and Chain-of-Draft*


Figure 3-46. Comparing the processes of Chain-of-Thought and Chain-of-Draft
As shown in Figure 3-47, the idea of reinforcement learning with length reward
designs generally rewards short, correct answers while penalizing lengthy or wrong
answers to achieve efficient reasoning. Often, short, correct answers are given greater
rewards than long, correct answers.



![Figure 3-47: An example of length rewards that may punish reasoning traces that are too](images/fig_03-47_An_example_of_length_rewards_that_may_pu.png)

*Figure 3-47: An example of length rewards that may punish reasoning traces that are too*


Figure 3-47. An example of length rewards that may punish reasoning traces that are too
long and reward those that are short and succinct
|
Chapter 3: Reasoning Large Language Models