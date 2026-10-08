---
title: "Mixture of Experts"
chapter_number: 35
page_start: 93
page_end: 99
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Mixture of Experts



![Figure 2-38: DeepSeek Sparse Attention (DSA) adds a Lightning Indexer and a Top-K](images/fig_02-38_DeepSeek_Sparse_Attention_DSA_adds_a_Lig.png)

*Figure 2-38: DeepSeek Sparse Attention (DSA) adds a Lightning Indexer and a Top-K*


Figure 2-38. DeepSeek Sparse Attention (DSA) adds a Lightning Indexer and a Top-K
Selector to compute attention over a sparse subset
Together, the Lightning Indexer and Top-K Selector reduce the number of tokens to
attend to K. In the paper referenced, the authors selected 2,048 tokens to attend to,
which drastically reduces the computation necessary for the attention computations.
Note that since MLA is used, there is already a significant memory benefit due to the
compression of the KV-cache. In their construction of MLA, instead of using MHA
as the core attention mechanism, MQA was used. The authors mentioned optimizing
for computational efficiency, which is true for MQA, considering it uses fewer keys
and values than MHA.
Mixture of Experts
MoE is a technique that is becoming more mainstream to create more efficient LLMs.
MoE uses several submodels or “experts” to improve the quality and efficiency of
LLMs. There are two main components of an MoE:
Experts
Each feed-forward neural network in an LLM is replaced by a set of “experts.”
Router or gate network
Determines which tokens are sent to which experts.
Part 2: A Deeper Dive Into Large Language Models
|

Let’s first explore experts. Remember that a typical Transformer-based LLM uses
self-attention followed by a feed-forward neural network. As shown in Figure 2-39,
we call this a dense model because everything is activated.



![Figure 2-39: In a dense Transformer block, the feed-forward neural network (FFNN) is](images/fig_02-39_In_a_dense_Transformer_block_the_feed-fo.png)

*Figure 2-39: In a dense Transformer block, the feed-forward neural network (FFNN) is*


Figure 2-39. In a dense Transformer block, the feed-forward neural network (FFNN) is
active for every single token passing through
A sparse model, in contrast, may deploy several feed-forward neural networks
instead. These are typically smaller than a regular network, but together they tend
to be bigger. Each feed-forward neural network in a sparse model is typically referred
to as an “expert” because, during training, each “expert” learns different information
and may specialize in the processing of certain tokens (Figure 2-40). For instance,
one expert might be used for processing numbers, whereas another processes verbs.
It’s still a bit unclear what these experts actually learn, but there has been some
research suggesting that they specialize in fine-grained information such as verbs
versus numbers rather than each learning an entirely different domain.5
Note that in this example, all experts are used, which does not allow for any efficiency
gains. To choose a subset of experts during inference, we make use of the router (also
called a gate network). This is a small feed-forward neural network that is trained to
choose an expert for a given token. The router, together with the experts, makes up
the MoE layer as shown in Figure 2-41.
5 Zoph, Barret et al. 2022. “ST-MoE: Designing Stable and Transferable Sparse Expert Models.” arXiv,
2202. 08906.
|
Chapter 2: Large Language Models

The router is arguably the most important component because the experts are noth‐
ing more than just small feed-forward neural networks. So, how exactly does the
router then choose which expert to use for each token? Let’s go through a minimal
example step-by-step.



![Figure 2-40: A dense block (left) applies a single network to all tokens, while a sparse](images/fig_02-40_A_dense_block_left_applies_a_single_netw.png)

*Figure 2-40: A dense block (left) applies a single network to all tokens, while a sparse*


Figure 2-40. A dense block (left) applies a single network to all tokens, while a sparse
block (right) routes different tokens to different experts



![Figure 2-41: An MoE layer uses a router to score experts and direct each token to a small](images/fig_02-41_An_MoE_layer_uses_a_router_to_score_expe.png)

*Figure 2-41: An MoE layer uses a router to score experts and direct each token to a small*


Figure 2-41. An MoE layer uses a router to score experts and direct each token to a small
active subset, leaving others inactive
Part 2: A Deeper Dive Into Large Language Models
|

The router, as a neural network, will have its own weight matrix, which is used to
multiply the input token embeddings. Applying a softmax on the output will result
in a probability distribution per expert. This probability distribution provides the
likelihood that an expert will be chosen given an input token. Figure 2-42 shows
everything put together, demonstrating how the input flows through the router and
experts.



![Figure 2-42: Inside the router, the token representation is mapped to a probability](images/fig_02-42_Inside_the_router_the_token_representati.png)

*Figure 2-42: Inside the router, the token representation is mapped to a probability*


Figure 2-42. Inside the router, the token representation is mapped to a probability
distribution over experts using a small network and softmax
Note that any number of experts can be selected, but generally a fixed number are
selected for training and inference. When selecting multiple experts, there is a need to
balance how much each expert is trained. If the same set of experts is always chosen
during training and inference, then all other experts are undertrained.
To balance the distribution of training among experts, the router will have to dynami‐
cally balance which expert to choose and when. This is referred to as load balancing.
To prevent one expert from dominating the training time, there are two main tech‐
niques that are often employed in one way or another, namely expert capacity and
auxiliary loss.
|
Chapter 2: Large Language Models

Expert capacity gives each expert in the MoE layer a limit to how many tokens it can
process.6 Instead of having a single expert do all the work, the tokens are somewhat
more equally distributed. For instance, by the time an expert has reached capacity,
each subsequent token routed to it will be sent to the next-highest scoring expert, as
shown in Figure 2-43.



![Figure 2-43: Expert capacity caps how many tokens each expert can process per batch,](images/fig_02-43_Expert_capacity_caps_how_many_tokens_eac.png)

*Figure 2-43: Expert capacity caps how many tokens each expert can process per batch,*


Figure 2-43. Expert capacity caps how many tokens each expert can process per batch,
routing excess tokens to the next-highest expert
In contrast, instead of limiting the experts, the router can also be adjusted to account
for this probability imbalance. A straightforward technique is to add Gaussian noise
just before the router produces its probabilities. By introducing noise, the distribu‐
tions will slightly change, and by (slight) chance, sometimes choose different experts
to use. A more advanced technique to balance how the router selects experts is called
auxiliary loss.7 These are loss functions that can be added to the router to reward it for
equally distributing the experts during training or punish it when the same expert is
chosen.
6 Lepikhin, Dmitry et al. 2020. “Gshard: Scaling Giant Models with Conditional Computation and Automatic
Sharding,” International Conference on Learning Representations, poster.
7 Shazeer, Noam et al. 2017. “Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts
Layer,” International Conference on Learning Representations, poster.
Part 2: A Deeper Dive Into Large Language Models
|

The main benefit of MoE is its computational requirements. Although using MoE
does not make the resulting model smaller, it runs much faster because only a few
experts are activated at a given time. As Figure 2-44 shows, all parameters that a
MoE model has need to be loaded into memory and are called sparse parameters. The
active parameters, in contrast, are those that are activated only during inference.



![Figure 2-44: In an MoE model, all experts must be loaded into memory, but only an](images/fig_02-44_In_an_MoE_model_all_experts_must_be_load.png)

*Figure 2-44: In an MoE model, all experts must be loaded into memory, but only an*


Figure 2-44. In an MoE model, all experts must be loaded into memory, but only an
active subset is used per forward pass
Most recent models tend to use MoE layers, such as OpenAI’s GPT-OSS and NVI‐
DIA’s Nemotron 3. Often, you’ll see models like Qwen3-30B-A3B that put the num‐
ber of sparse parameters (30 billion) and active parameters (3 billion) in their name.8
As such, even though 30 billion parameters need to be loaded in memory, only 3
billion are used, which makes it much faster for inference.
8 Yang, An et al. 2025. “Qwen3 Technical Report,” arXiv, 2505.09388.
|
Chapter 2: Large Language Models

Another example of MoE is the previously discussed DeepSeek-R1. As Figure 2-45
shows, DeepSeek-R1 has 256 experts, of which 8 are always chosen. Note that there is
also a shared expert bypassing the router. This expert is always chosen, which often
helps the model divert all general knowledge to that expert and more specialized
knowledge to all others.



![Figure 2-45: DeepSeek-R1 uses MoE layers with 256 experts per layer, of which 8 are](images/fig_02-45_DeepSeek-R1_uses_MoE_layers_with_256_exp.png)

*Figure 2-45: DeepSeek-R1 uses MoE layers with 256 experts per layer, of which 8 are*


Figure 2-45. DeepSeek-R1 uses MoE layers with 256 experts per layer, of which 8 are
selected by the router for each token. A shared expert bypasses the router and is always
active
In practice, there are many different choices for the number of experts chosen for
a given LLM and the sizes of each expert compared to the overall size of the LLM.
Table 2-1 demonstrates various open-weight LLMs and their implementations of
MoE.
Part 2: A Deeper Dive Into Large Language Models
|