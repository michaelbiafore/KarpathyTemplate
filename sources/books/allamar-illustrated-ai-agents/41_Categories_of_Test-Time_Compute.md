---
title: "Categories of Test-Time Compute"
chapter_number: 41
page_start: 114
page_end: 115
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Categories of Test-Time Compute



![Figure 3-16: Each diagonal line represents a fixed performance that can be achieved by](images/fig_03-16_Each_diagonal_line_represents_a_fixed_pe.png)

*Figure 3-16: Each diagonal line represents a fixed performance that can be achieved by*


Figure 3-16. Each diagonal line represents a fixed performance that can be achieved by
balancing train-time and test-time compute
Test-time compute doesn’t necessarily mean scaling-only thinking;
it refers to scaling time and compute spent on inference. Instead
of thinking longer, we could also generate many different answers
and vote on the best one. By creating more answers, we could
likewise scale time to run inference, and stabilize and improve on
the output.



![Figure on page 17](images/fig_p017_x95.png)


Categories of Test-Time Compute
Throughout this chapter, we’ll explore methodologies in scaling test-time compute
with a focus on extending and improving the thinking processes of LLMs. There
are many methods for scaling test-time compute, such as search-based techniques,
reward modeling, self-improvement, and more.6
To keep things manageable, these can also be put into the following two categories
that we will use throughout this chapter:7
Search against verifiers
Sampling generations and selecting the best answer
6 Qu, Xiaoye et al. 2025. “A Survey of Efficient Reasoning for Large Reasoning Models: Language, Multimodal‐
ity, and Beyond,” arXiv, 2503.21614.
7 Snell, Charlie et al. 2024. “Scaling LLM Test-Time Compute Optimally Can Be More Effective Than Scaling
Model Parameters,” arXiv, 2408.03314.
|
Chapter 3: Reasoning Large Language Models

Modifying proposal distribution
Trained “thinking” process
Search against verifiers is a set of techniques that revolve around sampling many
answers and/or reasoning traces. Selecting the best answer is done through some
form of reward model (RM; or verifier), a model that scores the quality of the given
answer and/or reasoning trace.
Modifying proposal distribution involves tuning or prompting the model in such a
way that it outputs improved reasoning steps. The proposal distribution is commonly
referred to the token probabilities, which propose the tokens to generate next. This
distribution from which tokens are sampled is modified to show more advanced
reasoning traces. Compared to search against verifiers, it may also use RMs during
training to score more promising reasoning traces.
An overview of both methods is shown in Figure 3-17.



![Figure 3-17: Search against verifiers (left) generates multiple traces and from them](images/fig_03-17_Search_against_verifiers_left_generates.png)

*Figure 3-17: Search against verifiers (left) generates multiple traces and from them*


Figure 3-17. Search against verifiers (left) generates multiple traces and from them
chooses the best answer by often using reward models. Modifying proposal distribution
(right) typically fine-tunes the model.
Due to its focus on sampling generations, search against verifiers is output-focused,
whereas modifying the proposal distribution is input-focused since it focuses on
either training or prompting the model. Figure 3-18 shows how these techniques
relate to one another.
Categories of Test-Time Compute
|