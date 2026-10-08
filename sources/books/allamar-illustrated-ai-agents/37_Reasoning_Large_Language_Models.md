---
title: "Chapter 3. Reasoning Large Language Models"
chapter_number: 37
page_start: 103
page_end: 105
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Chapter 3. Reasoning Large Language Models

Reasoning Large Language Models
LLMs such as DeepSeek-R1, OpenAI GPT-5, and Google Gemini are prime examples
of how LLMs can be scaled to new heights through reasoning frameworks. Reasoning
in LLMs attempts to mimic human thinking by generating thoughts through tokens
before giving a final answer. As shown in Figure 3-1, these tokens explain LLMs’
chain-of-thought and allow reasoning LLMs to break down a problem into smaller
steps (often called reasoning steps or thought processes).



![Figure 3-1: The differences between a non-reasoning and reasoning LLM](images/fig_03-01_The_differences_between_a_non-reasoning.png)

*Figure 3-1: The differences between a non-reasoning and reasoning LLM*


Figure 3-1. The differences between a non-reasoning and reasoning LLM
Reasoning LLMs first “think” and generate intermediate information before finally
answering the query.

Interestingly, the differences between non-reasoning and reasoning LLMs can be
viewed through the lens of human cognition, specifically System 1 and System 2
thinking from Daniel Kahneman’s dual-process theory,1 which describes two modes
of human cognition.
System 1, in human cognition, operates automatically and quickly, relying on intu‐
ition and learned associations to make snap judgments. Non-reasoning LLMs operate
much like System 1 thinking and generate responses quickly based on patterns
they learned during training. They produce immediate answers without step-by-step
(explicit) thinking.
System 2, in human cognition, engages in slower, more deliberate reasoning that
requires conscious effort and attention. Reasoning LLMs operate much like System 2
thinking and generate more deliberate step-by-step analyses before reaching conclu‐
sions. They explicitly work through problems and catch errors that a non-reasoning
LLM might miss.
System 1 is efficient for routine tasks but is prone to cognitive biases, whereas
System 2 relies on logical reasoning and tends to result in more accurate decisions.
Reasoning is critical in AI agents because it allows them to plan out behavior, decide
which actions to take, and reflect on the actions they have taken (see Figure 3-2).
This involves enabling them to actively seek information, utilize diverse tools, and
dynamically refine their reasoning.



![Figure 3-2: Agents use extended reasoning to plan their behavior, act out each step, and](images/fig_03-02_Agents_use_extended_reasoning_to_plan_th.png)

*Figure 3-2: Agents use extended reasoning to plan their behavior, act out each step, and*


Figure 3-2. Agents use extended reasoning to plan their behavior, act out each step, and
reflect on the results
AI agents need reasoning to devise a plan, decide on the actions they take, and reflect
on the results. This is especially true for planning out actions and reflecting on them.
For instance, in typical AI-assisted coding environments, such as Cursor and Cline,
the agents might create special Markdown files to track their plan and revise when
necessary.
1 Kahneman, Daniel. Thinking, Fast and Slow. (Macmillan, 2011).
|
Chapter 3: Reasoning Large Language Models

As shown in Figure 3-3, before we go into how AI agents showcase autonomous
behavior, we first explore how LLMs can demonstrate advanced thinking processes.
In Chapters 5 and 6, we explore how reasoning enables tool selection and enables
planning and reflection.



![Figure 3-3: Reasoning LLMs are a vital component for enabling advanced planning and](images/fig_03-03_Reasoning_LLMs_are_a_vital_component_for.png)

*Figure 3-3: Reasoning LLMs are a vital component for enabling advanced planning and*


Figure 3-3. Reasoning LLMs are a vital component for enabling advanced planning and
tool use. Without reasoning, methodologies such as reflection will be less accurate.
In this chapter, we uncover the history of reasoning LLMs through an important
paradigm shift from training to inference and explore various methods for creating
reasoning LLMs. We will also introduce coding examples for enabling and improving
reasoning behavior for the section “Search Against Verifiers” on page 102. Note
that there will be no changes to the TinyAgent because this chapter demonstrates
reasoning behavior.
Many terms in this chapter normally appear in abbreviated form.
To prevent confusion, we have spelled them out in this chapter,
with the acronyms included in parentheses in the first instance. We
have also included a glossary of key terms and acronyms in the
book’s repository.



![Figure on page 17](images/fig_p017_x95.png)


Reasoning Large Language Models
|