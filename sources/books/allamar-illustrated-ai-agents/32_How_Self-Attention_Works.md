---
title: "How Self-Attention Works"
chapter_number: 32
page_start: 84
page_end: 87
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# How Self-Attention Works

Part 2: A Deeper Dive Into Large Language Models
We’ll now switch gears and move into a collection of LLM-related concepts in more
depth. Namely, we’ll build on what we’ve learned in the first half of the chapter on
LLM architectures and training and take a closer look at self-attention, some of its
more efficient variants, and MoE models.
How Self-Attention Works
Earlier in the chapter, we saw how self-attention allows the model to attend to previ‐
ous tokens, thus enriching the representation of the token we’re currently processing,
as shown in Figure 2-29.



![Figure 2-29: Self-attention takes the current token’s vector (pink) along with those of](images/fig_02-29_Self-attention_takes_the_current_tokens.png)

*Figure 2-29: Self-attention takes the current token’s vector (pink) along with those of*


Figure 2-29. Self-attention takes the current token’s vector (pink) along with those of
preceding tokens and produces an enriched output vector for the current position that
incorporates context from the rest of the sequence
Going into the attention calculation are a collection of vectors: the vector for the
current position and the vectors for the previous positions.
|
Chapter 2: Large Language Models

A trained model is able to attend properly by utilizing three projection matrices
that resulted from the training process. We multiply the input vectors by each of
these projection matrices, resulting in matrices we call the queries, keys, and values
matrices (Figure 2-30).



![Figure 2-30: Inside an attention head, the input vectors for the current and preceding](images/fig_02-30_Inside_an_attention_head_the_input_vecto.png)

*Figure 2-30: Inside an attention head, the input vectors for the current and preceding*


Figure 2-30. Inside an attention head, the input vectors for the current and preceding
positions are multiplied by three learned projection matrices to produce the queries, keys,
and values used in the attention calculation
Part 2: A Deeper Dive Into Large Language Models
|

The first step of self-attention, relevance scoring, involves multiplying the query for
the token we’re currently processing by the key vectors associated with all the input
tokens. This results in a relevance score for each vector, as Figure 2-31 shows.



![Figure 2-31: Relevance scoring multiplies the current token’s query vector by key vectors](images/fig_02-31_Relevance_scoring_multiplies_the_current.png)

*Figure 2-31: Relevance scoring multiplies the current token’s query vector by key vectors*


Figure 2-31. Relevance scoring multiplies the current token’s query vector by key vectors
of all input tokens to produce relevance scores
After deciding the relevance values, self-attention then proceeds to combine informa‐
tion from these tokens, weighted by how relevant they are, and merge them into
the vector of the current token we’re processing. We see that weighted summation
calculation in Figure 2-32.
|
Chapter 2: Large Language Models



![Figure 2-32: Information-combining multiplies each token’s value vector by its relevance](images/fig_02-32_Information-combining_multiplies_each_to.png)

*Figure 2-32: Information-combining multiplies each token’s value vector by its relevance*


Figure 2-32. Information-combining multiplies each token’s value vector by its relevance
score and sums the results, producing the enriched output vector for the current position
This vector becomes the output of the self-attention layer. Figure 2-33 presents
this in another way, closer to the mathematical formula you’ll often see in LLM
literature. The current and previous tokens are projected into queries, keys, and
values; the query-key product (scaled by √dk and passed through softmax) produces
the relevance scores, which are then multiplied by the values to produce the attention
output for the current position.
Part 2: A Deeper Dive Into Large Language Models
|