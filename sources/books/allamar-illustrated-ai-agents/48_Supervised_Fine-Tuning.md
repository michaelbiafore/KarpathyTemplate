---
title: "Supervised Fine-Tuning"
chapter_number: 48
page_start: 131
page_end: 133
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Supervised Fine-Tuning



![Figure 3-30: Modifying the proposal distribution is essentially reranking the tokens such](images/fig_03-30_Modifying_the_proposal_distribution_is_e.png)

*Figure 3-30: Modifying the proposal distribution is essentially reranking the tokens such*


Figure 3-30. Modifying the proposal distribution is essentially reranking the tokens such
that it is much more common for the LLM to choose tokens that allow for a degree of
reasoning
We can achieve modifying or reranking this distribution by training the LLM. Two
common methods of training are:
Supervised fine-tuning (SFT)
Reasoning behavior is mimicked through supervised fine-tuning, where the LLM
is asked to reproduce pre-defined reasoning traces. The model learns to approxi‐
mate the reasoning patterns present in the training data.
Reinforcement learning (RL)
The LLM discovers reasoning itself through a reward system. During training,
the LLM discovers good reasoning strategies by being rewarded for generating
high-quality responses.
In other words, supervised fine-tuning stabilizes the model outputs by serving as
a memory process to uncover learned reasoning behavior, while reinforcement learn‐
ing enables self-learning and generalization.
Supervised Fine-Tuning
The most straightforward method for enabling reasoning behavior in LLMs is to
apply supervised fine-tuning. Similar to what we saw in Chapter 2, the model is
exposed to triplet-like data, which contains the user’s query, a reasoning trace, and an
answer.
Although using supervised fine-tuning is quite straightforward, collecting these large
amounts of reasoning traces is quite difficult, as they generally have to be manually
created by potentially labeling hundreds of thousands of samples.
Modifying Proposal Distribution
|

Flan-PaLM
An early example of using supervised fine-tuning on Chain-of-Thought-like data
was the Flan-PaLM paper.12 Chung et al.’s main method of fine-tuning is called Flan
(Fine-tuning language models; not to be confused with the FLAN models),13 in which
a variety of instruction templates are used on more than 1,800 tasks to fine-tune
LLMs.
In several of these tasks, examples were added that included annotated Chain-of-
Thought traces that the model could train on. They include arithmetic reasoning,
multi-hop reasoning, and natural language inference (determining the truthfulness of
a given statement).
As shown in Figure 3-31, the training data contained both reasoning and non-
reasoning examples, both without (zero-shot) and with (few-shot) examples. Chung
et al. fine-tuned various LLMs, including PaLM, which has 540 billion parameters,
and prefixed the fine-tuned models with “Flan.”



![Figure 3-31: Flan-PaLM is created through supervised fine-tuning on various data](images/fig_03-31_Flan-PaLM_is_created_through_supervised.png)

*Figure 3-31: Flan-PaLM is created through supervised fine-tuning on various data*


Figure 3-31. Flan-PaLM is created through supervised fine-tuning on various data
By mixing in Chain-of-Thought data in their pool of training data, the resulting
models could be more easily prompted to demonstrate reasoning (e.g., through
prompting “let’s think step-by-step”).
This is an early example of enforcing reasoning in LLMs through supervised fine-
tuning. However, the researchers’ data mostly contained non-reasoning examples
mixed in with reasoning traces to improve the model’s performance, such as straight‐
forward queries and answers combined with more extensive queries that include
examples of thoughts. Although this model can demonstrate Chain-of-Thought
through proper prompting, it’s still a bit premature to call this a reasoning model.
12 Chung, Hyung Won et al. 2024. “Scaling Instruction-Finetuned Language Models,” Journal of Machine Learn‐
ing Research, 25(70): 1-53.
13 Wei, Jason et al. 2021. “Finetuned Language Models Are Zero-Shot Learners,” arXiv, 2109.01652.
|
Chapter 3: Reasoning Large Language Models

Instead, let us explore supervised fine-tuning variants that purely focus on instilling
reasoning.
s1: Simple test-time scaling
Since Flan-PaLM, reasoning in LLMs has gained more traction. However, creating
reasoning data is quite difficult as it typically requires human annotators for large
amounts of query/answer pairs. Training data can easily reach hundreds of thousands
of examples, and adding reasoning traces to each can become costly.
The authors of “s1: Simple test-time scaling” demonstrate that you could get a reason‐
ing LLM using only small data.14 Using only 1,000 questions paired with reasoning
traces, they successfully fine-tuned the Qwen2.5 32B-Instruct LLM to demonstrate
stable reasoning.
Compared to Flan-PaLM, they used special tokens to separate the thinking stage from
the answering stage. To do so, the thinking stage was enclosed with <|im_start|>
think while the following answer was enclosed with <|im_start|>answer (see Fig‐
ure 3-32).



![Figure 3-32: A reasoning model could be created by using a dataset as small as 1,000](images/fig_03-32_A_reasoning_model_could_be_created_by_us.png)

*Figure 3-32: A reasoning model could be created by using a dataset as small as 1,000*


Figure 3-32. A reasoning model could be created by using a dataset as small as 1,000
samples
Using special types of tokens to separate thinking from the final answer is a common
method you will see employed by recent LLMs, such as Qwen3 and GPT-OSS.15
14 Muennighoff, Niklas et al. 2025. “s1: Simple Test-Time Scaling,” Proceedings of the 2025 Conference on
Empirical Methods in Natural Language Processing.
15 Yang, An et al. 2025. “Qwen3 Technical Report,” arXiv, 2505.09388.
Modifying Proposal Distribution
|