---
title: "Chapter 4. Memory"
chapter_number: 56
page_start: 151
page_end: 152
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Chapter 4. Memory

Memory
Among all the added modules to the augmented LLM, memory is a key component
needed to go from an LLM to an agent. By themselves, LLMs are forgetful entities;
they do not remember past conversations, nor do they have access to all actions they
have taken. If you were to locally load up an LLM and ask it to remember your name,
it can’t—not without explicitly giving it memory. In contrast, the interactions that
you might have with hosted LLMs, like ChatGPT and Claude, are not regular LLMs.
Rather, they are LLMs augmented with modules like memory and tools. Figure 4-1
illustrates this forgetfulness well, as it demonstrates the interaction you might have
with a regular LLM. As such, LLMs are stateless, and information is not persisted
across calls.



![Figure 4-1: LLMs without any additional processing are forgetful and will not remember](images/fig_04-01_LLMs_without_any_additional_processing_a.png)

*Figure 4-1: LLMs without any additional processing are forgetful and will not remember*


Figure 4-1. LLMs without any additional processing are forgetful and will not remember
information between sessions
Over the years, significant attention has been paid to aspects of agents like tool usage,
reasoning LLMs, and multi-agent collaboration. Each is quite important by itself,
but don’t underestimate the importance of memory. Without memory, a personal
assistant agent wouldn’t be able to remember past conversations. Without memory, a

coding agent wouldn’t understand your entire codebase. Without memory, an agent
would forget that it has already taken an action and keep on repeating it.
Memory can be quite difficult to define. From a narrow view, it may relate to all
historical information during the execution of an agent. In this chapter, however, we
take a broader perspective. Memory relates not only to all past actions of an agent,
but also external information beyond the agent-environment interactions. A coding
agent’s memory would not only consist of the actions it has taken to fix your bugs,
but also your hosted documentation and issues pages.
Memory is not only the act of remembering information but also storing newly
generated information. Likewise, often a choice has to be made on which information
to store and how, which information to remember and which parts of the memory
to forget or delete. All these methodologies and choices have important implications
on the agent’s behavior. As shown in Figure 4-2, updating and using memory is an
iterative process that requires careful handling of intermediate information.



![Figure 4-2: Memory in agentic systems relates to more than the conversation and may](images/fig_04-02_Memory_in_agentic_systems_relates_to_mor.png)

*Figure 4-2: Memory in agentic systems relates to more than the conversation and may*


Figure 4-2. Memory in agentic systems relates to more than the conversation and may
include the query, answer, and intermediate steps that were taken and the outputs of
those steps
Memory allows the agent to remember past errors and failed experiences, so it can be
more effective for handling similar tasks in the future. Although the underlying LLMs
might still be the same entities, memory enables agents to learn and evolve as they
have more information through experiences that guide their behavior. By interacting
with the environment and storing the feedback, agents learn from their previous
experiences. Memory is, therefore, application-specific, and implementations may
not only decide what to remember but also how it is remembered.
|
Chapter 4: Memory