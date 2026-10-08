---
title: "Reasoning in Latent Space"
chapter_number: 54
page_start: 147
page_end: 149
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Reasoning in Latent Space

Many such methods include a length reward. Kimi k1.5, a closed-sourced multi-
modal LLM, was trained using reinforcement learning to give extra rewards to
correct, short answers while penalizing wrong, long answers the most.18 Interest‐
ingly, this length reward slowed down early learning, so they gradually warmed
up the length penalty during training, which alleviated this problem. Similarly, the
O1-Pruner technique compares the length of the model’s answer to what a reference
model typically produces and rewards based on the difference between them.19
Longer answers get a penalty while same lengths get no change in rewards and
shorter answers get a high reward. They balance this with a dynamic accuracy reward
so that not only short, correct answers get high rewards but also long, correct answers
when it is needed for hard problems. Finally, L1 is a reasoning LLM that is trained
by telling it up front how long, in terms of tokens, it should think (e.g., “Think for
30 tokens”).20 The model gets rewarded for both being correct and matching the
requested length.
Some models attempt to go in a different direction to control the length of reason‐
ing and implement an on/off switch for reasoning that can either fully disable or
enable reasoning. A great example is the Qwen3 family of models, which, during
their release in April 2025, were known to be state-of-the-art for their sizes.21
They introduced special tokens for thinking mode (/think) and non-thinking mode
(/no_think), where each is trained respectively with and without Chain-of-Thought
data. This is also called hybrid reasoning, where thinking mode uses additional rea‐
soning, whereas no reasoning is used for the non-thinking mode, which will only
provide the answer, as was the case with traditional LLMs. Think of it as essentially
turning thinking off and on.
Reasoning in Latent Space
Chain-of-Thought, as we explored thus far, has been explicit. It’s like we are listening
to someone work through a problem out loud. The reasoning LLM “talks to itself”
in tokens so we can trace its logic. However, it’s not like we are always making our
thoughts explicit; we often internalize our thinking processes. An upcoming and
interesting take on reasoning is to make the explicit Chain-of-Thought of LLMs
internal via latent space reasoning. Here, the explicit Chain-of-Thought steps are
replaced by hidden representations. Instead of producing visible reasoning steps, the
model thinks entirely in its “mind’s eye,” its latent space. So instead of producing
18 Kimi Team et al. 2025. “Kimi k1. 5: Scaling Reinforcement Learning with LLMs,” arXiv, 2501.12599.
19 Luo, Haotian et al. 2025. “O1-Pruner: Length-Harmonizing Fine-Tuning for O1-Like Reasoning Pruning,”
arXiv, 2501.12570.
20 Aggarwal, Pranjal, and Sean Welleck. 2025. “L1: Controlling How Long a eReasoning Model Thinks With
Reinforcement Learning,” arXiv, 2503.04697.
21 Yang, An et al. 2025. “Qwen3 Technical Report,” arXiv, 2505.09388.
Emerging Directions in Reasoning Research
|

these long reasoning traces, the model will skip straight from the question to the
answer and perform all of its reasoning without us being able to see it.
To explore latent space reasoning, let’s first recap Chain-of-Thought reasoning. As
shown in Figure 3-48, Chain-of-Thought reasoning starts from a given query and
autoregressively generates a token at a time by continuously appending the output
to the updated input. After processing an input, the model produces an output by
sampling from its last hidden state. The output, a token, is then embedded together
with the rest of the input. In other words, the last hidden state is only used to
generate the next token.



![Figure 3-48: A recap of Chain-of-Thought reasoning and how data flows through the](images/fig_03-48_A_recap_of_Chain-of-Thought_reasoning_an.png)

*Figure 3-48: A recap of Chain-of-Thought reasoning and how data flows through the*


Figure 3-48. A recap of Chain-of-Thought reasoning and how data flows through the
model
One of the first methods of latent space reasoning is Chain-of-Continuous-Thought,
a method that skips over the decoding of the embeddings and instead directly oper‐
ates on the last hidden state.22 As shown in Figure 3-49, instead of embedding new
output tokens and adding them to the input, it generates the last hidden state and
uses it directly as the input. To differentiate between thoughts and answers, special
tokens are used (<bot> for beginning of thought and <eot> for end of thought). By
using the last hidden state as the input, the model does not produce any tokens until
it reaches the <eot>. After that, it can still generate intermediate reasoning steps if
necessary or directly give back the output.
22 Hao, Shibo et al. 2024. “Training Large Language Models to Reason in a Continuous Latent Space,” arXiv,
2412. 06769.
|
Chapter 3: Reasoning Large Language Models



![Figure 3-49: Chain-of-Continuous-Thought reasons in latent space by not producing](images/fig_03-49_Chain-of-Continuous-Thought_reasons_in_l.png)

*Figure 3-49: Chain-of-Continuous-Thought reasons in latent space by not producing*


Figure 3-49. Chain-of-Continuous-Thought reasons in latent space by not producing
reasoning tokens but by using the last hidden state instead
This methodology was further extended by Continuous Chain-of-Thought via Self-
Distillation (CODI).23 CODI simultaneously trains a teacher and student LLM. The
teacher LLM is trained on explicit Chain-of-Thought data and sees the reasoning
during training. The teacher LLM learns from this annotated Chain-of-Thought data
using cross-entropy loss and has to produce a correct answer with a reasoning trace.
In contrast, the student follows a Chain-of-Continuous-Thought-like process and
does not produce any explicit Chain-of-Thought but does so instead on the last
hidden states. Then, the answers of the teacher LLM and student LLM are compared,
and an additional loss is factored in during training. In other words, the explicit
Chain-of-Thought that the teacher learns is implicitly being taught to the student
LLM (Figure 3-50).



![Figure 3-50: CODI’s process of training a teacher and student LLM for implicit and](images/fig_03-50_CODIs_process_of_training_a_teacher_and.png)

*Figure 3-50: CODI’s process of training a teacher and student LLM for implicit and*


Figure 3-50. CODI’s process of training a teacher and student LLM for implicit and
explicit Chain-of-Thought
23 Shen, Zhenyi 2025. “CODI: Compressing Chain-of-Thought into Continuous Space via Self-Distillation,”
arXiv, 2502.21074.
Emerging Directions in Reasoning Research
|