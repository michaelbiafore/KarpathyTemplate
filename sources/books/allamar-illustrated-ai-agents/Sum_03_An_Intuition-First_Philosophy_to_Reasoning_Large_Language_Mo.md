# Preface and Chapter 1 (Introduction) — Combined Summary

## An Intuition-First Philosophy

LLMs "stopped just talking and started doing": given a goal, tools, and memory, they search, write and run code, revise plans, and work through multi-step problems. The book's goal is **intuition**, not currency — frameworks churn weekly, so it targets the principles that stay constant underneath. It continues the visual method of the authors' *Hands-On Large Language Models*, with hundreds of original illustrations, one of which (the anatomy of an agent, Chapter 1) anchors every later chapter.

## Building As You Read: The TinyAgent

Alongside the illustrations, readers build **TinyAgent** in Python, one component per chapter, until it reasons, remembers, uses tools, plans, and reflects. Printed code teaches; the GitHub repository (`HandsOnLLM/An-Illustrated-Guide-To-AI-Agents`) is the maintained, runnable version, shipped as the `illustrated-agents` package.

## Audience and Prerequisites

Three audiences: developers (the TinyAgent thread), researchers (deeper sections on model internals, training, evaluation methodology), and technical leaders or non-coding readers, for whom the illustrations carry the full conceptual story — the code can be skipped or "handed to your coding agent." The conceptual thread needs no programming or math.

## Book Structure, Tooling, and Keys

Part 1 (*The Anatomy of an AI Agent*) builds one agent: Ch1 introduction, Ch2 LLMs, Ch3 reasoning LLMs, Ch4 memory, Ch5 tools and the Model Context Protocol, Ch6 planning and reflection, Ch7 evaluation (outcomes *and* trajectories, reliability, safety — evaluating a system, not a model). Part 2 (*Specialized Agents*) covers multi-agent systems, multi-modal agents, and coding agents. Chapters are independently readable. Examples run free in Google Colab (NVIDIA T4) or locally and default to open source models, needing API keys only for a few free-tier proprietary ones. Conventions, code-reuse permissions, and O'Reilly contact details are standard front matter.

## Introduction and What Is an AI Agent?

The mid-2020s shift is framed as a redefinition, not an increment: where LLMs need handholding, agents decide ==which actions to take, when, and how==. The book adopts the classical definition — an agent "perceives its environment through sensors and acts upon that environment through actuators" (Russell & Norvig) — decomposed into **environment, sensors, actuators, and agent program**.

![Figure 1-1: An agent perceives its environment through sensors and acts on it via tools or](images/fig_01-01_An_agent_perceives_its_environment_throu.png)

*Figure: The classical agent box — an "agent program" brain converting percepts from sensors into actions through actuators, all against an external environment.*

Mapped onto LLMs: the agent program is a reasoning LLM, the actuators are its tools, multi-modal inputs are its sensors, and the user sits inside the environment, usually initiating the loop. Figure 1-2 is the book's anchor diagram.

![Figure 1-2: Agents operate in regular contact with a user and environment, and use](images/fig_01-02_Agents_operate_in_regular_contact_with_a.png)

*Figure: The anchor figure of the whole book — a reasoning LLM augmented by memory, tools, and planning, cycling query/answer with the user and action/feedback with the environment.*

## Large Language Models

An LLM is, traditionally, a next-token predictor: input is split into tokens, the model scores the vocabulary, one token is sampled, the input is updated, and the loop repeats (autoregression) until a full answer — or an action on the environment — emerges.

![Figure 1-3: LLMs process their input messages by breaking them into tokens and produce](images/fig_01-03_LLMs_process_their_input_messages_by_bre.png)

*Figure: Query → tokenizer → LLM → probability distribution over the whole vocabulary → one sampled output token.*

## Reasoning Large Language Models

GPT-3.5/ChatGPT launched an era of **train-time scaling** — more data, compute, and parameters in pre-training — which hit a cost-effectiveness ceiling. The breakthrough (OpenAI o1, DeepSeek-R1) was training models to think *out loud*, spending extra compute on reasoning tokens before answering; playgrounds usually hide or summarize that trace.

![Figure 1-6: Reasoning improves the behavior of LLMs by allowing them to explicitly state](images/fig_01-06_Reasoning_improves_the_behavior_of_LLMs.png)

*Figure: Same flamingo word problem to both models — the regular LLM emits an answer directly, while the reasoning LLM writes out the subtraction steps first and then answers.*

Reasoning underpins planning, tool selection, reflection, and dynamic replanning, so reasoning LLMs are central to the book — though plain LLMs stay preferable when responses must be fast and cheap. Chapters 1–3 are the agent's "brain."
