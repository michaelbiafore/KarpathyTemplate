---
title: "Context Engineering for Multi-Agent Systems"
chapter_number: 66
page_start: 186
page_end: 186
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Context Engineering for Multi-Agent Systems

conversation history. Likewise, Search-o1 compresses the retrieved context and gives
back only the relevant components without any noise. These dynamic memory tech‐
niques are exceptionally useful for context engineering as the information flows grow
more complex.
Context Engineering for Multi-Agent Systems
As we will cover in more depth in Chapter 8, multi-agent systems deploy groups of
agents working together to solve a given problem. Our example of a deep research
agent used a summarization agent in its system, thereby working together. What
makes context engineering especially difficult in multi-agent systems is that not only
the context of the main agents needs to be carefully managed, so do the contexts of
all other agents in the system. Moreover, the interaction between agents is also part of
the shared context between those respective agents.
To manage this complex network of contexts, smaller agents can be used to handle
some of the context “burden,” as we illustrated in the deep research agent. By using
a smaller agent with a smaller LLM for specific tasks, part of the context can be
handled separately, leaving significant compute for the main agent (also called the
orchestrator agent). What makes these small and/or specialized agents great for
context engineering is that they can work on smaller and more manageable contexts,
have clear responsibilities, and are easier to test and debug. These systems can be
more reliable by separating tasks instead of having one agent juggle all kinds of
different tasks and contexts.
Optimizing the Context
Throughout this chapter, we covered many different methods and techniques for
handling the memory and context of LLMs and agents. Optimizing what you put into
the context and how is a multi-faceted problem that requires an understanding of
various parts of your agent’s architecture. Most strategies to optimize the context are
built upon the main source of context, the memory modules of the agent, but often
also include system prompts and tool schemas.
Although there are many strategies, let’s explore the most common ones.
Context tracking and storage
Before you give the agent a possible relevant context, it first needs to be tracked and
stored somewhere. We covered most of it already, as this relates to various forms of
memory, and in particular episodic memory, which contains the actions the agent has
taken thus far. Although episodic memory is seen as long-term memory, it is highly
related to the conversation history of the agent, which tends to capture the agent’s
actions.
|
Chapter 4: Memory