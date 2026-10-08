---
title: "Summary"
chapter_number: 36
page_start: 100
page_end: 102
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Summary

Table 2-1. Open-weight LLMs and their MoE
Model
Sparse parameters
Shared
experts
Mistral 7x8B
46. 7
12. 8
DeepSeek-R1
Llama 4 Maverick
Qwen3 235B-A22B
Kimi-K2
1,000
GPT-OSS 120B
5. 1
GPT-OSS 20B
3. 6
GLM 4.5
Qwen3 Next
Mistral Large 3
Nemotron-3-Nano-30B-A3B
31. 6
3. 6
Active parameters
Number of
Experts
activated
(billion)
(billion)
experts
Summary
This chapter covered the engine that powers every agent in this book: the LLM.
We structured the chapter in two parts because the depth of understanding needed
depends on what you’re trying to do.
Part 1 looked at LLMs from the perspective of an agent developer. Language models
consume and produce tokens, and the formats built on top of those tokens—system
prompts, multi-turn conversations, and tool calls—are what let a language model
serve as the reasoning core of an agent.
We then walked through how LLMs are created across two training phases. Pre-
training via next-token prediction produces a base model. Post-training via SFT and
RL shapes the base model into something that follows instructions and generates
responses aligned with human preferences. We looked at how RLVR and the GRPO
algorithm use verifiable signals such as format and correctness to push models
toward reliable behavior.
We also opened up the Transformer itself, tracing how tokens flow through a stack
of blocks, each containing a self-attention layer and a feed-forward neural network,
before the LM head converts the final representation into a next-token probability
distribution. For agent developers, the two architectural properties worth carrying
into later chapters are context length, which limits how much information we can
pack into a model’s input, and the KV cache, which shapes the economics and latency
of every agent we build.
Part 2 went deeper into the internals. We saw how self-attention is actually computed
through the queries, keys, and values produced by three projection matrices and how
|
Chapter 2: Large Language Models

relevance scoring and information combining make up the two steps of the attention
operation.
We then looked at how self-attention has evolved to address its memory and compute
costs. The KV cache itself avoids redundant recomputation. Grouped-Query and
Multi-query Attention shrink the cache by sharing K and V across heads. DeepSeek’s
Multi-head Latent Attention takes a different approach, caching a low-rank com‐
pressed representation that gets projected back up when needed. DeepSeek Sparse
Attention adds a Lightning Indexer and Top-K Selector to attend to only the most
relevant tokens instead of the entire sequence.
We closed with MoE architectures, which replaced the dense feed-forward layer with
a router and a set of smaller expert networks. This produces models where the total
and active parameter counts can differ by an order of magnitude, a distinction that
matters when selecting a model to deploy.
In the next chapter, we turn to reasoning LLMs, the class of models that has reshaped
what agents can do by producing long chains of thought before committing to an
answer.
Summary
|