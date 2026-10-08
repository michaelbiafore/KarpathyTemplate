---
title: "KV-Caching Revisited"
chapter_number: 33
page_start: 88
page_end: 89
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# KV-Caching Revisited



![Figure 2-33: The same self-attention calculation expressed in the form commonly seen in](images/fig_02-33_The_same_self-attention_calculation_expr.png)

*Figure 2-33: The same self-attention calculation expressed in the form commonly seen in*


Figure 2-33. The same self-attention calculation expressed in the form commonly seen in
the literature: projecting tokens into queries, keys, and values to calculate attention
As we’ll see in the next section, there is one final operation after calculating attention
this way.
KV-Caching Revisited
What we’ve described so far are major components of self-attention as described
in the Transformer paper, which is often called “vanilla attention.” This early form
of self-attention, however, does a lot of redundant calculations of the K and V
weights for each generated attention score if we apply it naively to text generation.
Specifically, at each step, attention is recalculated for the entire sequence despite
having calculated the K and V vectors of the previously seen tokens before. Imagine
that a model is processing the attention scores for the tokens “My” and “name.” As
shown in Figure 2-34, regular attention would recalculate the K and V vectors at each
subsequent step despite having calculated them before.
|
Chapter 2: Large Language Models



![Figure 2-34: Vanilla attention recomputes the keys and values for every previous token](images/fig_02-34_Vanilla_attention_recomputes_the_keys_an.png)

*Figure 2-34: Vanilla attention recomputes the keys and values for every previous token*


Figure 2-34. Vanilla attention recomputes the keys and values for every previous token
at each generation step, causing redundant calculations
This is where the KV cache comes in. Instead of having to recalculate those vectors,
we can simply cache and reuse them for subsequent decoding steps. This makes
inference much faster by reducing the redundant computation. A basic KV cache is
shown in Figure 2-35 and demonstrates how the K and V vectors are reused from
previous steps instead. Also note that the query (Q) vectors do not need to be cached
because they become unnecessary in subsequent iterations. Specifically, we need only
the query vector of the latest token to compute the self-attention.



![Figure 2-35: The KV cache stores keys and values from previous steps to avoid recompu‐](images/fig_02-35_The_KV_cache_stores_keys_and_values_from.png)

*Figure 2-35: The KV cache stores keys and values from previous steps to avoid recompu‐*


Figure 2-35. The KV cache stores keys and values from previous steps to avoid recompu‐
tation, processing only the new token’s query
Although such a KV cache can make inference much faster, it does require signifi‐
cantly more memory if all KV values are cached. For that, there are many different
forms of attention created that attempt to reduce the calculations needed, which
should therefore also reduce the KV cache that needs to be maintained.
Part 2: A Deeper Dive Into Large Language Models
|