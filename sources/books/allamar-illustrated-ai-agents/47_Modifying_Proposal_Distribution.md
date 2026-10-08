---
title: "Modifying Proposal Distribution"
chapter_number: 47
page_start: 129
page_end: 130
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Modifying Proposal Distribution



![Figure 3-27: Weighted Best-of-N samples add a Process Reward Model (PRM) to judge](images/fig_03-27_Weighted_Best-of-N_samples_add_a_Process.png)

*Figure 3-27: Weighted Best-of-N samples add a Process Reward Model (PRM) to judge*


Figure 3-27. Weighted Best-of-N samples add a Process Reward Model (PRM) to judge
each output
Modifying Proposal Distribution
The second category of scaling test-time compute is called modifying proposal distri‐
bution and is a popular method of creating reasoning LLMs. Instead of searching for
the correct reasoning steps with verifiers (output-focused), the model is trained to
demonstrate advanced reasoning steps (input-focused). Remember that both the Pro‐
cess Reward Model and the Outcome Reward Model focus on the output generated
by the LLM, the reasoning traces, and the final answer, respectively.
The term “modifying proposal distribution” refers to the distribution from which
tokens are sampled. Imagine that we have a question that we pass to the LLM. As
shown in Figure 3-28, it creates a distribution of token probabilities from which
we can sample. A common strategy would be to select the token with the highest
probability.
Modifying Proposal Distribution
|



![Figure 3-28: Each LLM generates token probabilities, and by looking a bit closer at each](images/fig_03-28_Each_LLM_generates_token_probabilities_a.png)

*Figure 3-28: Each LLM generates token probabilities, and by looking a bit closer at each*


Figure 3-28. Each LLM generates token probabilities, and by looking a bit closer at each
token, we can consider them either related to output or to reasoning
However, some of the tokens in this distribution are not a direct answer but instead
the start of reasoning behavior. Shown in Figure 3-29, if we choose a token that
answers the question directly, then it immediately generates a stop token. However, if
a token is chosen that is the start of reasoning, then it completes its reasoning until
it reaches an answer. As such, you can view them as “answer” and “reason” tokens,
respectively.



![Figure 3-29: Forcing the LLM to choose tokens that are the start of a sentence rather](images/fig_03-29_Forcing_the_LLM_to_choose_tokens_that_ar.png)

*Figure 3-29: Forcing the LLM to choose tokens that are the start of a sentence rather*


Figure 3-29. Forcing the LLM to choose tokens that are the start of a sentence rather
than the immediate answer tends to generate simple forms of reasoning
When we modify the proposal distribution (the token probability distribution), we
are essentially making it so that the model re-ranks the distribution such that “rea‐
soning” tokens are selected more frequently (Figure 3-30).
|
Chapter 3: Reasoning Large Language Models