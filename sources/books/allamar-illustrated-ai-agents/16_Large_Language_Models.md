---
title: "Large Language Models"
chapter_number: 16
page_start: 26
page_end: 26
part: "Part I. The Anatomy of an AI Agent"
---
# Large Language Models

Let’s go through each component in more detail and clarify how they relate to the
book structure.
Large Language Models
To understand what AI agents are, we first need to explore the basic capabilities of an
LLM, as the LLM is typically considered to be the “brain” of an agent. Traditionally,
an LLM is a model that does nothing more than predict the next word based on
a given input text. As shown in Figure 1-3, the LLM first breaks down a given
input query into tokens, which are subcomponents of words that allow the model to
generalize to words it has not seen before. The LLM processes these tokens, and a
prediction is made on what the next token could be.



![Figure 1-3: LLMs process their input messages by breaking them into tokens and produce](images/fig_01-03_LLMs_process_their_input_messages_by_bre.png)

*Figure 1-3: LLMs process their input messages by breaking them into tokens and produce*


Figure 1-3. LLMs process their input messages by breaking them into tokens and produce
their output as tokens—whether it be a message to the user or an action enacted on the
environment
The LLM therefore predicts the next token, uses the predicted token to update its
input, and then continues the predictions. By doing this iteratively (which is called
autoregression), it can create entire answers to the user’s query (shown in Figure 1-4).
|
Chapter 1: Introduction