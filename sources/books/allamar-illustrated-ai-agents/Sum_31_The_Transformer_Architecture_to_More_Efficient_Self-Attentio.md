# Transformer Internals: Architecture, Self-Attention, and KV-Caching (Ch. 31–34)

## The Transformer Architecture

Since roughly 2020, LLMs have been Transformer *decoders* with three major parts: a tokenizer, a stack of Transformer blocks, and a language modeling (LM) head.

![Figure 2-14: The three main components of a Transformer LLM: a tokenizer, a stack of](images/fig_02-14_The_three_main_components_of_a_Transform.png)

*Figure: A prompt enters the model, passes through tokenizer → stack of Transformer blocks 1..N → LM head, and one output token comes out.*

The tokenizer splits text into tokens drawn from a fixed vocabulary (say 50,000), each mapped to a learned embedding vector. The stack does nearly all the processing; the LM head turns the final vector into a probability score for every token in the vocabulary, and a *decoding strategy* (temperature zero = always the top token; higher temperature = sampling) picks the actual output.

Every token flows through its own "track" in parallel, but only the last token's track feeds the LM head to predict the next token. The number of tracks a model supports is its **context size** — the hard architectural limit that gives rise to the discipline of context engineering. Because the input tokens' intermediate results can be cached, each subsequent generation step activates only the single new token's track — prompt-caching / prefix-caching / **kv-caching**, a key cost-and-latency lever for agent developers.

![Figure 2-22: Inside each Transformer block are a self-attention layer for gathering](images/fig_02-22_Inside_each_Transformer_block_are_a_self.png)

*Figure: Embeddings flow block-to-block at constant size; each block contains a self-attention layer plus a feed-forward neural network.*

The feed-forward layer stores the learned factual/statistical associations ("The Shawshank" → "Redemption"). Dense models use one large network; mixture-of-experts (MoE) models replace it with several smaller expert networks plus a router that picks experts per token. Self-attention supplies context — resolving, for example, whether "it" refers to the dog or the llama.

## How Self-Attention Works

Input vectors are multiplied by three learned projection matrices to produce **queries, keys, and values**. Relevance scoring multiplies the current token's query against all keys; information-combining then sums the value vectors weighted by those scores.

![Figure 2-31: Relevance scoring multiplies the current token’s query vector by key vectors](images/fig_02-31_Relevance_scoring_multiplies_the_current.png)

*Figure: Inside one attention head, the current token's query times the key matrix yields percentage relevance scores across earlier tokens ("dog" 40%, "The" 30%).*

![Figure 2-33: The same self-attention calculation expressed in the form commonly seen in](images/fig_02-33_The_same_self-attention_calculation_expr.png)

*Figure: The familiar formula — softmax(QKᵀ/√d_k) × V — producing the attention output vector.*

## KV-Caching Revisited

Vanilla attention recomputes K and V for every previous token at every generation step. The KV cache stores and reuses them instead; only the newest token's Q is needed, so Q is never cached.

![Figure 2-35: The KV cache stores keys and values from previous steps to avoid recompu‐](images/fig_02-35_The_KV_cache_stores_keys_and_values_from.png)

*Figure: At step 3 ("My name is"), the orange K and V columns come from cache and only the green new-token row is computed.*

The tradeoff is memory: caching all KV values is expensive, which motivates cheaper attention variants.

## More Efficient Self-Attention

Grouped-Query Attention and FlashAttention came first; DeepSeek then introduced Multi-head Latent Attention (MLA) and DeepSeek Sparse Attention (DSA).

![Figure 2-36: Multi-head Latent Attention compresses input into low-rank representa‐](images/fig_02-36_Multi-head_Latent_Attention_compresses_i.png)

*Figure: MLA low-rank-compresses input into latent Q and latent KV, caches the small latent KV, applies RoPE to a decoupled Q/K component, then concatenates and runs standard multi-head attention.*

![Figure 2-37: Four approaches to attention: MHA uses full K and V; GQA and MQA](images/fig_02-37_Four_approaches_to_attention_MHA_uses_fu.png)

*Figure: MHA keeps full per-head K and V; GQA shares them across groups; MQA shares one K and V for all heads; MLA projects a compressed latent KV back up.*

DSA sits on top of MLA, adding a *lightning indexer* that scores how relevant each preceding token is (using RoPE'd Q/K plus a scalar weight w) and a *Top-K Selector* that retrieves only the highest-scoring KV entries, so attention is computed over a subset rather than the whole sequence.
