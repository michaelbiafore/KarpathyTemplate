# Chapters 35–42: Mixture of Experts through Reward Models

## Mixture of Experts

MoE replaces the single feed-forward network (FFNN) in each Transformer block with a set of smaller "experts" plus a **router** (gate network) that decides which experts see which token. A dense block runs one FFNN for every token; a sparse block routes tokens to a few specialists — research suggests experts learn fine-grained distinctions (verbs vs. numbers) rather than whole domains.

![Figure 2-41: An MoE layer uses a router to score experts and direct each token to a small](images/fig_02-41_An_MoE_layer_uses_a_router_to_score_expe.png)

*Figure: The MoE block sits where the FFNN normally does — a router scores the experts and only the top-scoring FFNN processes the token, its output weighted by the router score.*

The router multiplies the token embedding by its own weight matrix and applies softmax to get a probability per expert. Because always picking the same experts leaves the rest undertrained, **load balancing** is needed: *expert capacity* caps tokens per expert (overflow spills to the next-highest scorer), while Gaussian noise or an *auxiliary loss* nudges the router toward even usage.

![Figure 2-44: In an MoE model, all experts must be loaded into memory, but only an](images/fig_02-44_In_an_MoE_model_all_experts_must_be_load.png)

*Figure: Every expert must be loaded (sparse parameters), but only a subset runs per forward pass (active parameters) — the source of MoE's speed.*

Hence names like Qwen3-30B-A3B: 30B loaded, 3B active. DeepSeek-R1 uses 256 experts per layer with 8 chosen, plus a shared expert that bypasses the router and absorbs general knowledge.

## Summary

Chapter 2 closes by recapping chat/tool formats, pre-training vs. post-training (SFT, RL, RLVR, GRPO), the Transformer stack, and the attention-efficiency ladder — KV cache, GQA/MQA, Multi-head Latent Attention, DeepSeek Sparse Attention — ending with MoE.

## Reasoning Large Language Models

Reasoning LLMs generate thinking tokens before answering, mapping onto Kahneman's dual-process theory: non-reasoning models are fast, intuitive System 1; reasoning models are deliberate System 2. Agents need this to plan, choose actions, and reflect.

![Figure 3-1: The differences between a non-reasoning and reasoning LLM](images/fig_03-01_The_differences_between_a_non-reasoning.png)

*Figure: Both models answer "3 flamingos," but the reasoning LLM emits explicit intermediate steps first.*

## The Paradigm Shift from Train-Time Compute to Test-Time Compute

Train-time compute means scaling model size, dataset size, and FLOPs across pre-training and post-training.

## Train-Time Compute Versus Test-Time Compute

Test-time compute instead scales inference: more generated tokens means more computational work spent reaching the answer — provided the tokens carry genuine new relationships, not filler.

![Figure 3-10: The switch from train-time compute to test-time is a focus toward inference](images/fig_03-10_The_switch_from_train-time_compute_to_te.png)

*Figure: Non-reasoning LLMs spend almost nothing at inference; reasoning LLMs shift a large compute block to it.*

## Scaling Laws

Kaplan and Chinchilla scaling laws are power laws with diminishing returns — straight lines on log-log axes, flattening curves on normal ones. By 2024 the field was hitting that wall, pushing research toward inference.

![Figure 3-14: The left graph demonstrates increasing train-time compute, and the right](images/fig_03-14_The_left_graph_demonstrates_increasing_t.png)

*Figure: OpenAI's o1 AIME accuracy rises log-linearly with both more RL training and more thinking time — the test-time curve climbing at least as steeply.*

Jones' AlphaZero/Hex study showed the two are interchangeable: to hold an Elo target, less test-time compute demands more train-time compute, and best results come from raising both.

## Categories of Test-Time Compute

Two families: **search against verifiers** (sample many traces, pick the best via a reward model — output-focused) and **modifying the proposal distribution** (train or prompt the model to emit better reasoning steps — input-focused).

![Figure 3-17: Search against verifiers (left) generates multiple traces and from them](images/fig_03-17_Search_against_verifiers_left_generates.png)

*Figure: Left, parallel thought/answer pairs scored by reward models (.75/.5/.9/.2) with the best chosen; right, fine-tuning on thought processes to produce a reasoning LLM.*

## Reward Models

Verifiers are fine-tuned LLMs or rule-based systems (e.g., unit tests), in two flavors.

![Figure 3-19: An ORM judges only the output and not intermediate reasoning steps](images/fig_03-19_An_ORM_judges_only_the_output_and_not_in.png)

*Figure: The Outcome Reward Model scores only the final answer, ignoring every reasoning step.*

![Figure 3-20: A PRM judges only the intermediate reasoning steps and not the output](images/fig_03-20_A_PRM_judges_only_the_intermediate_reaso.png)

*Figure: The Process Reward Model scores each thought process separately, so a bad step can be penalized and a later correction rewarded.*

A mix of PRM and ORM is often preferred.
