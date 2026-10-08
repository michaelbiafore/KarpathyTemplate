---
title: "Reasoning Large Language Models"
chapter_number: 17
page_start: 27
page_end: 29
part: "Part I. The Anatomy of an AI Agent"
---
# Reasoning Large Language Models



![Figure 1-4: LLMs operate in an autoregressive loop, outputting one token at a time](images/fig_01-04_LLMs_operate_in_an_autoregressive_loop_o.png)

*Figure 1-4: LLMs operate in an autoregressive loop, outputting one token at a time*


Figure 1-4. LLMs operate in an autoregressive loop, outputting one token at a time
In Chapter 2, we’ll explore in detail how this system, the LLM, works. The common
architecture of LLMs, attention, and its many variants, will be explored to give you an
understanding of its internal mechanisms.
Reasoning Large Language Models
Arguably, one of the most impactful LLMs is GPT-3.5, which powered the original
ChatGPT released in November 2022. As a chat model, GPT-3.5 could hold entire
conversations, making it eerily similar to how humans would interact. It’s safe to
say that this model changed the world as we know it. Over the years since, OpenAI
and many other LLM providers have focused on scaling GPT-3.5-like models to new
heights by throwing more data, compute, and parameters at them. This is called
train-time scaling (shown in Figure 1-5), where training on more data and making
models larger led to reliable, predictable improvements in performance. The idea was
that pre-training, the first and most expensive stage of training an LLM, was where
the gains came from: the larger your pre-training budget, the better the resulting
model.



![Figure 1-5: A lot of major LLM progress has been due to train-time compute: scaling](images/fig_01-05_A_lot_of_major_LLM_progress_has_been_due.png)

*Figure 1-5: A lot of major LLM progress has been due to train-time compute: scaling*


Figure 1-5. A lot of major LLM progress has been due to train-time compute: scaling
data, compute, and model size
What Is an AI Agent?
|

Although this improved the performance of these models, it uncovered a ceiling
effect. Continuously scaling the model’s size is not cost-effective, and soon, training
simply became too expensive for the small increase in performance. As it turns out,
scaling your model can be done in more ways than one.
A major breakthrough in model performance was achieved with the introduction of
LLM reasoning abilities in models such as OpenAI o1 and DeepSeek-R1. Instead of
having the model “think” quietly (or implicitly through the model’s parameters) for a
fixed amount of time, models were now trained to “think” out loud and spend more
time to arrive at a correct answer (by generating reasoning tokens before deriving
the answer). As shown in Figure 1-6, reasoning LLMs first generate “thoughts” and
leverage that to generate the final answer.



![Figure 1-6: Reasoning improves the behavior of LLMs by allowing them to explicitly state](images/fig_01-06_Reasoning_improves_the_behavior_of_LLMs.png)

*Figure 1-6: Reasoning improves the behavior of LLMs by allowing them to explicitly state*


Figure 1-6. Reasoning improves the behavior of LLMs by allowing them to explicitly state
and keep track of subproblems of the task at hand
The main idea is that it allows LLMs to write down their thoughts first through
their autoregressive behavior before coming to an answer. Instead of spending all
of its compute to generate only the answer, the LLM spends additional compute
to first generate its “thoughts.” By structuring its thoughts, more complex queries
that require multi-step reasoning are easier to solve. In some LLM playgrounds, like
ChatGPT, these thoughts are typically hidden from the user or summarized, whereas
the answer to the user’s query generally represents a conclusion building on the
model’s “thoughts” (Figure 1-7).
|
Chapter 1: Introduction



![Figure 1-7: The final answers displayed in reasoning-LLM applications and playgrounds](images/fig_01-07_The_final_answers_displayed_in_reasoning.png)

*Figure 1-7: The final answers displayed in reasoning-LLM applications and playgrounds*


Figure 1-7. The final answers displayed in reasoning-LLM applications and playgrounds
are aided by a reasoning trace that may be hidden or summarized
Part of what makes AI agents more capable is their ability to make extensive plans,
select the appropriate tools, reflect on their mistakes, and even dynamically revise
and update these plans. All of these require advanced reasoning behavior in LLMs.
Reasoning LLMs are particularly capable at complex decision-making tasks, breaking
down multi-step problems, and generalizing to novel problems. However, if you want
fast and cheap responses, “regular” LLMs are preferred.
As such, reasoning LLMs will take a central role throughout most of this book, as
reasoning is a key capability enabling these complex behaviors. In Chapter 3, you’ll
learn about various ways to create reasoning LLMs. We look at the fundamentals of
reasoning LLMs, explore the famous reasoning LLM, DeepSeek-R1, and look beyond
at what the future might hold in this field. Chapters 2 and 3 will therefore focus on
the “brain” of the agent (Figure 1-8).



![Figure 1-8: The first three chapters of the book focus on introducing agents, LLMs, and](images/fig_01-08_The_first_three_chapters_of_the_book_foc.png)

*Figure 1-8: The first three chapters of the book focus on introducing agents, LLMs, and*


Figure 1-8. The first three chapters of the book focus on introducing agents, LLMs, and
reasoning because these are foundational ideas for AI agents
What Is an AI Agent?
|