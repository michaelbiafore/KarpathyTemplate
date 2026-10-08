---
title: "Input and Output Tokens"
chapter_number: 27
page_start: 53
page_end: 53
part: "Part 1: What You Should Know About Large Language Models"
---
# Input and Output Tokens

Part 1: What You Should Know About
Large Language Models
Language models are systems trained to predict and generate text sequences. Their
inputs and outputs are best understood initially as sequences of words, or more
precisely, tokens—which can be words, parts of words, numbers, or punctuation.
Input and Output Tokens
We can see the perspective of an LLM’s inputs and outputs in Figure 2-3. The input
text (which can be a query from the user or feedback from the environment) is
first broken down into tokens, then presented to the language model. The language
model generates the first token, then the next one, then the next, until its response is
completed.



![Figure 2-3: Input text is split into tokens—“flamingos” becomes two tokens (“flamingo”](images/fig_02-03_Input_text_is_split_into_tokensflamingos.png)

*Figure 2-3: Input text is split into tokens—“flamingos” becomes two tokens (“flamingo”*


Figure 2-3. Input text is split into tokens—“flamingos” becomes two tokens (“flamingo”
and “s”)—passed to the LLM, which generates output tokens sequentially to form the
final response
This one step of generating this output text is actually a loop where the model
generates a token, adds it to the input, and then processes this new input again to
generate the next token. We can see the first of these steps in Figure 2-4. Models that
operate like this, consuming their own output from one step as inputs in a following
step, are called autoregressive models.
Part 1: What You Should Know About Large Language Models
|