---
title: "From Language Modeling to Powering Agents"
chapter_number: 28
page_start: 54
page_end: 55
part: "Part 1: What You Should Know About Large Language Models"
---
# From Language Modeling to Powering Agents



![Figure 2-4: The model generates “Flamingo” from the input tokens (step 1); that output](images/fig_02-04_The_model_generates_Flamingo_from_the_in.png)

*Figure 2-4: The model generates “Flamingo” from the input tokens (step 1); that output*


Figure 2-4. The model generates “Flamingo” from the input tokens (step 1); that output
token is appended to the input and the model generates the next token, “s” (step 2)
From Language Modeling to Powering Agents
The LLMs that power agents start out as general language models, as previously
discussed. This is done in the first training phase of a language model and creates
what’s called a base language model. But for an LLM to be able to power an agent,
it needs an additional set of capabilities to fit the expected role. LLM creators train
LLMs in the subsequent phase of training, called post-training, to be able to parse
inputs and generate outputs in a format that supports these expected capabilities.
System prompt
Language models are most often deployed by one entity, say a company, to serve a set
of users, say the employees of the company. The party that deploys the model needs
a way to describe the expected behavior of the model in a way that takes precedence
over what the end users ask of the model.
This is the role of the system prompt: a privileged input that shapes model behavior
before the model sees a single token from the user. Because it’s baked into how the
model is used rather than how it’s trained, system prompts let deployers customize
behavior without touching the underlying model.
In Figure 2-5, we see how a system prompt is added to the beginning of a user
message. We also see a simple example of a formatting style that identifies the various
parts of the input and output. Shown here is a simplified format that looks like the
OpenAI Harmony format used for models such as OpenAI’s GPT-OSS, released in
2025.
|
Chapter 2: Large Language Models



![Figure 2-5: A system prompt prepended to the user message shapes how the model will](images/fig_02-05_A_system_prompt_prepended_to_the_user_me.png)

*Figure 2-5: A system prompt prepended to the user message shapes how the model will*


Figure 2-5. A system prompt prepended to the user message shapes how the model will
respond—here instructing it to “answer truthfully”—before the full input is passed to the
LLM
Multi-turn conversations
Popular LLM systems like ChatGPT are modeled as a conversation between a user
and an AI chatbot. This way, the LLM can keep track of a longer conversation and
identify who said what in the history of the conversation. In Chapter 4, we’ll touch on
this as being one way we give an LLM some form of memory to be able to recollect
earlier messages in the conversation.
Tool use
The conversation formats define a specific way for a language model to take an
action. The LLM outputs a specific format, choosing a software function to invoke.
The agentic software wrapper around the language model looks for these patterns
and calls the functions that the LLM is trying to invoke. These functions are usually
listed in the system prompt telling the LLM what actions are available to it.
Chapter 5 is dedicated to tools, their definitions, invocations, and processing their
outputs. We touch on them here for an early example of the types of text that flow
into and out of language models, enabling them to power agents.
In Figure 2-6, we can see an example message passed to an LLM. It has a system
prompt, multiple turns in the chat history, and a final question asked by the user.
The LLM responds by choosing to call a web search tool to retrieve the information
required to answer the question.
Part 1: What You Should Know About Large Language Models
|