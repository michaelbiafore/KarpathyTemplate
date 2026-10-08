---
title: "More Efficient Self-Attention"
chapter_number: 34
page_start: 90
page_end: 92
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# More Efficient Self-Attention

More Efficient Self-Attention
Variants of attention mechanisms have since been developed to alleviate the memory
issue of the KV cache and optimize the attention calculations. Popular techniques
include Grouped-Query Attention and FlashAttention.1 More recently, however,
DeepSeek introduced two attention mechanisms that showed tremendous improve‐
ments in the efficiency of attention calculations, namely Multi-head Latent Attention
(MLA) and DeepSeek Sparse Attention (DSA).
Multi-head Latent Attention
A major step in making the KV-cache more memory efficient is through MLA,
first used in DeepSeek-V2 and popularized by DeepSeek-R1.2,3 MLA is a variant of
Multi-head Attention, which maintains separate Q, K, and V projection matrices for
each attention head, producing a different Q, K, and V matrix per head. MLA uses
low-rank joint compression of the keys and values to reduce the KV cache during
inference. At its core, it compresses the keys and values into a smaller latent represen‐
tation that is cached in place of the full K and V. In practice, this compressed cache is
often combined with quantization (reducing the numerical precision of stored values)
for additional memory savings.
MLA first compresses the input embeddings into lower-dimensional representations
called the latent Q and latent KV. These representations are significantly smaller than
the full Q and KV, which allows us to cache the latent KV instead of the full K
and V. Positional information via Rotary Position Embedding (RoPE) is applied to a
decoupled component of the latent Q, since the latent Q is recomputed at every step.
RoPE is not applied to the latent K itself, because the cached K would then need to
be recomputed at every step, breaking the benefit of caching. Therefore, positional
information is carried by a separate small key instead. Note that at this step, the
Q, K, and V representations are split across multiple attention heads, much like
standard Multi-head Attention. Finally, the content and positional components are
concatenated and passed through standard Multi-head Attention. The full procedure
is shown in Figure 2-36.
1 Dao, Tri et al. 2022. “FlashAttention: Fast and Memory-efficient Exact Attention with IO-Awareness,”
NIPS’22: Proceedings of the 36th International Conference on Neural Information Processing Systems, 1189:
16344-16359.
2 Shao, Zhihong et al. 2024. “DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language
Model.” arXiv, 2405.04434.
3 Guo, Daya et al. 2025. “DeepSeek-R1 Incentivizes Reasoning in LLMs Through Reinforcement Learning.”
Nature 645: 633–638. https://doi.org/10.1038/s41586-025-09422-z.
|
Chapter 2: Large Language Models



![Figure 2-36: Multi-head Latent Attention compresses input into low-rank representa‐](images/fig_02-36_Multi-head_Latent_Attention_compresses_i.png)

*Figure 2-36: Multi-head Latent Attention compresses input into low-rank representa‐*


Figure 2-36. Multi-head Latent Attention compresses input into low-rank representa‐
tions and caches the smaller latent KV to save memory
As such, MLA is essentially Multi-head Attention but with a compressed KV cache
containing the previously mentioned Latent KV representation. This compression
reduces the KV cache quite a bit and allows for much faster inference. It’s also more
efficient than previous methods, such as Grouped-Query Attention. An overview of
MLA versus other common attention mechanisms can be found in Figure 2-37. Note
that Grouped-Query Attention and Multi-Query Attention share K and V across
query heads to reduce the memory necessary for the KV cache but tend to be less
accurate.
Part 2: A Deeper Dive Into Large Language Models
|



![Figure 2-37: Four approaches to attention: MHA uses full K and V; GQA and MQA](images/fig_02-37_Four_approaches_to_attention_MHA_uses_fu.png)

*Figure 2-37: Four approaches to attention: MHA uses full K and V; GQA and MQA*


Figure 2-37. Four approaches to attention: MHA uses full K and V; GQA and MQA
reduce K and V directly; MLA caches compressed latent KV
DeepSeek Sparse Attention
The next step in making MLA more efficient was first introduced in DeepSeek-V3.2.
This new attention mechanism, called DeepSeek Sparse Attention (DSA), is instanti‐
ated under MLA and is an additional module to more efficiently select the tokens to
attend to.4 It has two main components, a lightning indexer and a Top-K Selector.
The lightning indexer determines how relevant each preceding token is to the current
query. For that, it uses the Q/K values that both have RoPE applied to them. Likewise,
it takes in a scalar weight parameter w that helps the lightning indexer make better
decisions about which tokens to select for the full attention mechanism. The output
of the lightning indexer is scores fed to the Top-K Selector, which in turn retrieves
only the KV entries that correspond to the Top-K index scores. As a result, the
attention output is computed through the query token and a subset of KV entries.
This full procedure is shown in Figure 2-38.
4 Liu, Aixin et al. 2025. “DeepSeek-V3. 2: Pushing the Frontier of Open Large Language Models,” arXiv,
2512. 02556.
|
Chapter 2: Large Language Models