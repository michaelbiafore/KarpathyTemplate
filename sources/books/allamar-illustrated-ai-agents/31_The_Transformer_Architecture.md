---
title: "The Transformer Architecture"
chapter_number: 31
page_start: 71
page_end: 83
part: "Part 1: What You Should Know About Large Language Models"
---
# The Transformer Architecture



![Figure 2-13: GRPO generates multiple responses to a single prompt, assigns rewards, and](images/fig_02-13_GRPO_generates_multiple_responses_to_a_s.png)

*Figure 2-13: GRPO generates multiple responses to a single prompt, assigns rewards, and*


Figure 2-13. GRPO generates multiple responses to a single prompt, assigns rewards, and
updates the model based on relative scores
This concludes the main intuitions for model training we think are useful for builders
of AI agents to know about how LLMs are trained. Next, we’ll take a closer look at the
architecture of the neural network that this process trains.
The Transformer Architecture
Now that we’ve seen the inputs and outputs of the model and covered how the model
gets trained, it’s time to look inside the trained model and get a sense of the inner
workings. LLMs have predominantly been neural networks built in the Transformer
decoder architecture since around 2020.
The tokenizer, Transformer blocks, and language modeling head
A Transformer decoder has three major components: a tokenizer, a stack of Trans‐
former blocks, and a language modeling head (LM head). We see these components
in Figure 2-14.
The tokenizer is the piece of software responsible for breaking the text input into
tokens. It is carefully optimized earlier in the training process of the LLM to help
bring out the capabilities we need in the trained LLM. The vast majority of agent
developers will work with a ready-made tokenizer prepared by the model provider.
For an LLM intended to power agents, careful tuning for a tokenizer includes support
for generating software code, the various languages intended for use, and adding
special tokens (like <|start|>) that are used in the specified data format.
Part 1: What You Should Know About Large Language Models
|



![Figure 2-14: The three main components of a Transformer LLM: a tokenizer, a stack of](images/fig_02-14_The_three_main_components_of_a_Transform.png)

*Figure 2-14: The three main components of a Transformer LLM: a tokenizer, a stack of*


Figure 2-14. The three main components of a Transformer LLM: a tokenizer, a stack of
Transformer blocks, and an LM head
A tokenizer has a set number of tokens in its vocabulary, say 50,000. We see an
example of these in Figure 2-15.
We can also see in the figure that the model has an equal number of vector embed‐
dings—one per token in our vocabulary. These embeddings vectors are numeric
representations of each token and they are what the model uses to calculate language
and how it processes its inputs.



![Figure 2-15: The tokenizer maps input text to token IDs drawn from a fixed vocabulary](images/fig_02-15_The_tokenizer_maps_input_text_to_token_I.png)

*Figure 2-15: The tokenizer maps input text to token IDs drawn from a fixed vocabulary*


Figure 2-15. The tokenizer maps input text to token IDs drawn from a fixed vocabulary
(here, 50,000 tokens), each of which is then looked up in an embeddings table to retrieve
a numeric vector before being passed to the Transformer blocks
|
Chapter 2: Large Language Models

Almost the entirety of the processing done inside a language model is conducted
inside the stack of Transformer blocks, which we cover in more detail in the next
section. But what results from that process is a single vector containing information
on what the next token should be.
That vector is passed to the LM head to interpret. It makes a simple calculation,
which results in a probability score for each token in its vocabulary. That score is
informed by everything the model learned in its training phases, and tokens with
high probabilities are the ones most likely to appear as a completion in response
to the input tokens. In Figure 2-16, we can see an example of such a scoring of
probabilities.



![Figure 2-16: The LM head converts final representations into a probability distribution](images/fig_02-16_The_LM_head_converts_final_representatio.png)

*Figure 2-16: The LM head converts final representations into a probability distribution*


Figure 2-16. The LM head converts final representations into a probability distribution
over the entire vocabulary
The next natural step would be to actually pick the output token as informed by these
probabilities. We may choose the highest probability token, but there are often good
reasons for picking other tokens. The method to pick tokens from the probability
distribution is called a decoding strategy.
If you’ve played with the temperature setting of an LLM, then you have interacted
with these probabilities. A temperature value of zero leads to always choosing the
single token with the highest probability. Increasing that temperature allows sam‐
pling, which means choosing from the distribution in a way where higher-probability
tokens have a higher chance of being picked (Figure 2-17).
Part 1: What You Should Know About Large Language Models
|



![Figure 2-17: The decoding strategy selects a token from the probability distribution,](images/fig_02-17_The_decoding_strategy_selects_a_token_fr.png)

*Figure 2-17: The decoding strategy selects a token from the probability distribution,*


Figure 2-17. The decoding strategy selects a token from the probability distribution,
where higher temperatures increase the chance of lower-probability tokens
Processing through the Transformer blocks
A neural network processes inputs and produces an output in a forward pass. This
means that the calculation flows sequentially through the various layers. This is
exactly what happens with the Transformer blocks. First the first block starts process‐
ing, then it passes its results of processing to the next block, and so on. The final
block passes its result to the LM head, and we proceed to decoding as we saw in the
previous section.
Figure 2-18 shows this flow through the stack of Transformer blocks. It also shows
how each token can be seen flowing through its own track.
|
Chapter 2: Large Language Models



![Figure 2-18: Each input token is processed through the full stack of Transformer blocks](images/fig_02-18_Each_input_token_is_processed_through_th.png)

*Figure 2-18: Each input token is processed through the full stack of Transformer blocks*


Figure 2-18. Each input token is processed through the full stack of Transformer blocks
in parallel, with every token position producing its own output vector passed to the LM
head—though only the final token’s output is used to predict the next token
The number of tracks that a model supports is commonly known as its context
size. So, a model that has a context length of 100,000 can have only that number of
tokens flowing through it simultaneously, which generally limits its input and output
capacity to text of that size.
For text generation, the processing flow of the last token is what’s used to generate the
next token, as we can see in Figure 2-19. That calculation is informed, however, by
all the processing conducted on the previous tokens, as we’ll see next when looking
closer at the insides of a Transformer block.
Part 1: What You Should Know About Large Language Models
|



![Figure 2-19: Each token flows through its own track in the stack, with only the final](images/fig_02-19_Each_token_flows_through_its_own_track_i.png)

*Figure 2-19: Each token flows through its own track in the stack, with only the final*


Figure 2-19. Each token flows through its own track in the stack, with only the final
token’s track passed to the LM head to predict the next token
For agent developers, context length is a key property for selecting the best model
to build an agent around. It sets a limit on how much information we can pack in
the input of the model. This limitation gives rise to a whole discipline of context
engineering that we’ll revisit repeatedly in this book. This is the discipline of choosing
the most relevant information for the model to fit within this architectural limitation
of the Transformer model.
Another key concept for agent developers is to realize that after that first pass where
all the input tokens are processed, it’s common to cache the results so that in the next
forward pass, we process the information along only the one track associated with the
new token we’re generating. This is referred to as prompt-caching, prefix-caching, or
more technically, kv-caching.
|
Chapter 2: Large Language Models

In Figure 2-20, we can see how only one track is active and information from
previous tracks is cached and used for that one active calculation. This leads to
dramatically increased speed and reduces the amount of processing required.



![Figure 2-20: Previous token calculations are cached so each subsequent generation step](images/fig_02-20_Previous_token_calculations_are_cached_s.png)

*Figure 2-20: Previous token calculations are cached so each subsequent generation step*


Figure 2-20. Previous token calculations are cached so each subsequent generation step
processes only the single new token’s track
Optimizing for the kv-cache is a key responsibility for agent developers to increase
the speed and reduce the cost of the agents they build. In Chapter 10, we cover
some strategies used by developers of software engineering agents to optimize for this
cache, reducing the latency and improving the economics of their agents.
Inside the Transformer block
We’ve seen how the input text is broken down into tokens. And we’ve also seen that
each token has an associated static embedding vector in the model. The Transformer
operates on these embedding vectors. The first Transformer block is presented with
the embedding vectors associated with the tokens in the input text.
Part 1: What You Should Know About Large Language Models
|

As we can see in Figure 2-21, the first block does a bit of processing on these input
vectors and hands off the results of its processing (as the same number and size of
vectors) to the next Transformer block. This goes on block by block until the last
block in the stack.



![Figure 2-21: Token embeddings flow through the stack as fixed-size vectors, with each](images/fig_02-21_Token_embeddings_flow_through_the_stack.png)

*Figure 2-21: Token embeddings flow through the stack as fixed-size vectors, with each*


Figure 2-21. Token embeddings flow through the stack as fixed-size vectors, with each
Transformer block progressively refining representations while keeping size constant
But what processing actually happens inside a Transformer block?
There are two major components inside a Transformer block: a self-attention layer
and a feed-forward neural network layer (Figure 2-22). Without going into too much
detail, in the next section we explain the intuition for each of these two components,
starting with feed-forward neural networks and then coming back to self-attention.
|
Chapter 2: Large Language Models



![Figure 2-22: Inside each Transformer block are a self-attention layer for gathering](images/fig_02-22_Inside_each_Transformer_block_are_a_self.png)

*Figure 2-22: Inside each Transformer block are a self-attention layer for gathering*


Figure 2-22. Inside each Transformer block are a self-attention layer for gathering
context and a feed-forward neural network for processing representations
The Transformer block: the feed-forward neural network
Let’s first talk about the feed-forward neural network because it’s simpler, even
though in the architecture it comes after self-attention. This layer does the heavy
lifting in predicting the next token because the training process shapes its ability to
predict the patterns encoded in the training dataset.
If we train a feed-forward neural network on vast amounts of web data, when we
give it the words “The Shawshank,” it would be able to predict that the next word
would be “Redemption,” because the 1994 film with that name is the most common
occurrence of this sequence of tokens. Figure 2-23 shows this oversimplified exam‐
ple, which suggests the feed-forward layers store factual associations learned during
training.
Part 1: What You Should Know About Large Language Models
|



![Figure 2-23: The feed-forward neural network layer highlighted within the Transformer](images/fig_02-23_The_feed-forward_neural_network_layer_hi.png)

*Figure 2-23: The feed-forward neural network layer highlighted within the Transformer*


Figure 2-23. The feed-forward neural network layer highlighted within the Transformer
block
In the original Transformer as well as in the majority of LLMs at the time of writing,
the feed-forward neural network layer is one big neural network, as we can see in
Figure 2-24. The training process prunes and adapts its connections in a way that
encodes the patterns in language. Recall that by now, we’re no longer talking about a
specific human language, we’re talking about a model that supports multiple human
languages, multiple programming languages, as well as the patterns we need to
define tool calling, multi-turn conversations, and, as we’ll see in Chapter 3, reasoning
patterns.



![Figure 2-24: The feed-forward neural network in a dense model expands the token](images/fig_02-24_The_feed-forward_neural_network_in_a_den.png)

*Figure 2-24: The feed-forward neural network in a dense model expands the token*


Figure 2-24. The feed-forward neural network in a dense model expands the token
representation to a larger hidden dimension before compressing it back down
|
Chapter 2: Large Language Models

In recent years, there has been a trend away from having a single large network,
and replacing it with a large number of smaller, more specialized networks. This
architecture is called a mixture-of-experts (MoE), and we talk about it more in the
second part of this chapter. We mention this here because as you select a model to
power your agent, you may come across a choice of a dense model and an MoE
model, especially if you’re looking at open source models.
In Figure 2-25, we see a basic MoE feed-forward layer that contains four sublayers;
each is called an expert. These are preceded by a router that looks at the input token
and decides which expert (or set of experts) is best suited to process this particular
token.



![Figure 2-25: A mixture-of-experts feed-forward layer replaces a single large neural](images/fig_02-25_A_mixture-of-experts_feed-forward_layer.png)

*Figure 2-25: A mixture-of-experts feed-forward layer replaces a single large neural*


Figure 2-25. A mixture-of-experts feed-forward layer replaces a single large neural
network with multiple smaller expert neural networks, routed per token to save capacity
Let’s now turn to the other major component of the Transformer block.
The Transformer block: an overview of self-attention
Language encodes a lot of information in the order of words in a sequence and the
context that a word is used in. A word such as bank can mean a financial institution
or can mean a riverbank. We would only know which is meant by looking at the
context where the word is used. The self-attention layer allows the Transformer to
make these distinctions.
As we can see in Figure 2-26, a model is presented with an input sentence that
is, “The dog chased the llama because it.” When processing the word it in its own
processing track, the model needs to know whether it refers to the dog or the llama.
Self-attention is tuned to resolve this kind of problem.
Part 1: What You Should Know About Large Language Models
|



![Figure 2-26: Self-attention allows each token to draw on context from other positions](images/fig_02-26_Self-attention_allows_each_token_to_draw.png)

*Figure 2-26: Self-attention allows each token to draw on context from other positions*


Figure 2-26. Self-attention allows each token to draw on context from other positions
in the sequence. Here, when processing “it” (red track), the model attends back to
“lama” (orange arc) to resolve the ambiguity of what “it” refers to—a distinction the
feed-forward layer alone could not make.
Part 2 of this chapter goes into how self-attention is calculated, but the high-level
intuition is that it attends to the most relevant previous tokens in the sequence. It
learns that relevance from the training process. Figure 2-27 shows this function in
its most basic form: we have the token we’re currently processing (in red), and four
previous tokens. Self-attention enriches the information encoded in the input vector
with information from the most relevant previous tokens in the sequence.



![Figure 2-27: Self-attention enriches the current token’s representation by drawing in](images/fig_02-27_Self-attention_enriches_the_current_toke.png)

*Figure 2-27: Self-attention enriches the current token’s representation by drawing in*


Figure 2-27. Self-attention enriches the current token’s representation by drawing in
information from the most relevant preceding positions
|
Chapter 2: Large Language Models

Self-attention does this by taking two steps: first, it scores the relevance of the
previous tokens and then proceeds to a step of combining the relevant information
into the token we’re processing, as we can see in Figure 2-28.



![Figure 2-28: Self-attention operates in two steps: relevance scoring determines how much](images/fig_02-28_Self-attention_operates_in_two_steps_rel.png)

*Figure 2-28: Self-attention operates in two steps: relevance scoring determines how much*


Figure 2-28. Self-attention operates in two steps: relevance scoring determines how much
attention to pay to each preceding position, and combining information blends those
positions’ representations into the current token’s output vector in proportion to their
relevance scores
Self-attention is one of the most resource-intensive operations in the Transformer.
That’s why it’s commonly one of the areas most targeted for improvement. Now
we’ll turn to the second half of this chapter, where we look at how self-attention is
calculated and newer and more efficient forms of self-attention.
Part 1: What You Should Know About Large Language Models
|