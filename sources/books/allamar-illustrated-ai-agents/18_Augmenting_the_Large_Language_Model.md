---
title: "Augmenting the Large Language Model"
chapter_number: 18
page_start: 30
page_end: 35
part: "Part I. The Anatomy of an AI Agent"
---
# Augmenting the Large Language Model

Augmenting the Large Language Model
Although reasoning LLMs are vital to AI agents, they’re still incomplete and miss
certain functionalities. As static text-to-text entities, text-based LLMs have no control
over their environment, nor do they remember their interactions or learn from them.
Let’s explore how to go from an incredibly capable LLM to one that can remem‐
ber interactions, interact with its environment, and demonstrate various degrees of
autonomy.
Memory
Notice how, so far, we have shown only “single-turn” conversations. These conversa‐
tions contain a single question and answer pair in the interaction with the LLM.
If we were to continue this conversation and ask another question, we would turn
it into a “multi-turn” conversation. Multi-turn conversations expose a vital flaw of
LLMs, namely that they’re forgetful entities and do not remember past conversations
(Figure 1-9). They are stateless, which means that information is not persisted across
calls.



![Figure 1-9: An LLM without a memory system to keep track of longer user conversations](images/fig_01-09_An_LLM_without_a_memory_system_to_keep_t.png)

*Figure 1-9: An LLM without a memory system to keep track of longer user conversations*


Figure 1-9. An LLM without a memory system to keep track of longer user conversations
Without memory, LLMs are nothing more than answering machines. Ask an LLM
a question and get an answer. However, follow it up with another question, and the
LLM has no information about the former interaction.
|
Chapter 1: Introduction

Fortunately, there are many ways we can add memory modules to LLMs to mimic
memory. As shown in Figure 1-10, a common way to approach this is by simply
adding the previous conversation to the current prompt.



![Figure 1-10: Adding conversation history to the LLM input is one of the first ways used](images/fig_01-10_Adding_conversation_history_to_the_LLM_i.png)

*Figure 1-10: Adding conversation history to the LLM input is one of the first ways used*


Figure 1-10. Adding conversation history to the LLM input is one of the first ways used
to allow the model to glance at previous turns in the chat
In practice, however, memory modules can be quite complex. They share many
similarities with human memory systems, such as short-term and long-term memory,
but also how we process information. If we receive too much information, it becomes
difficult to process, which can lead to poor decision-making. This is called informa‐
tion overload and can be a real problem even for LLMs. As such, memorizing every
little detail might hurt the performance of an LLM, so a balance is needed between
the amount and quality of the information in the prompt. This is called context
engineering and, as shown in Figure 1-11, it attempts to balance the information
available and what we give the LLM.
What Is an AI Agent?
|



![Figure 1-11: It’s essential to carefully design the input we pass to the LLM to help it](images/fig_01-11_Its_essential_to_carefully_design_the_in.png)

*Figure 1-11: It’s essential to carefully design the input we pass to the LLM to help it*


Figure 1-11. It’s essential to carefully design the input we pass to the LLM to help it
tackle its present task, called context engineering
Tools
With memory, LLMs remember the conversations they previously had, but they’re
not yet capable of interacting with their environment. LLMs can interact with their
digital environment through external tools that may enhance their capabilities (like
web search, for example). These tools vary in complexity and can range from
straightforward calculators and search engines to more advanced tools with access
to your command shell and coding environment.
However, LLMs are not capable of using tools by themselves. Fundamentally, LLMs
can be seen as software or functions that, upon receiving input text, process it and
then output some text. As text-in/text-out functions, LLMs can only describe or show
the intent of taking the action when outputting text. This is shown in Figure 1-12,
where the LLM, upon receiving the query “What is 5.1 times 7.3?” generates the
string “multiply(5.1, 7.3)”. This string merely represents the LLM’s intention to take
an action, but the action itself is not taken without outside intervention.
|
Chapter 1: Introduction



![Figure 1-12: LLMs are able to invoke tools by outputting text in a specific format that](images/fig_01-12_LLMs_are_able_to_invoke_tools_by_outputt.png)

*Figure 1-12: LLMs are able to invoke tools by outputting text in a specific format that*


Figure 1-12. LLMs are able to invoke tools by outputting text in a specific format that
other software systems parse and execute
The LLM can express the intent to use a tool, but it relies on us to turn that intent
into an actual tool call. The user will need to write software to convert that text
into an action. For instance, if the LLM’s output were JSON, we would use that to
choose the correct tool and fill in its parameters. Those actions would need to be
programmed separately (optionally by using existing agent frameworks). Figure 1-13
illustrates these steps, showing a possible representation of the overall flow.



![Figure 1-13: The workflow of an LLM calling a tool](images/fig_01-13_The_workflow_of_an_LLM_calling_a_tool.png)

*Figure 1-13: The workflow of an LLM calling a tool*


Figure 1-13. The workflow of an LLM calling a tool
There are many ways an LLM can use and learn tools, which we’ll cover in Chapter 5,
along with how using the same tools by different LLMs can be standardized with the
Model Context Protocol.
Chapters 2 through 5 give us what LLM company Anthropic calls: “the augmented
LLM” (Figure 1-14). This LLM is capable of deciding which tools to use, how to use
them, and what kind of information to retain. These augmentations (memory and
tools) allow for interaction with the environment in meaningful ways.
What Is an AI Agent?
|



![Figure 1-14: Augmenting a reasoning LLM with memory and tools: the “augmented](images/fig_01-14_Augmenting_a_reasoning_LLM_with_memory_a.png)

*Figure 1-14: Augmenting a reasoning LLM with memory and tools: the “augmented*


Figure 1-14. Augmenting a reasoning LLM with memory and tools: the “augmented
LLM” that serves as the building block we turn into an agent
Planning and reflection
The final ingredient to go from a “regular” LLM to an AI agent is its ability to plan
and reflect. These capabilities are important throughout much of an agentic system
because the agent will need to decide which steps to take, how to take them, and
when. For instance, if the LLM has access to dozens of GitHub API tools, such as
looking at pull requests or commits, how does it decide which to use?
This is where planning comes in, which involves breaking down a large task into
smaller, actionable steps, referred to as task decomposition. The first step is to
typically create a plan to execute when presented with a query (Figure 1-15).



![Figure 1-15: Plans enable agents to tackle larger tasks by breaking them down into](images/fig_01-15_Plans_enable_agents_to_tackle_larger_tas.png)

*Figure 1-15: Plans enable agents to tackle larger tasks by breaking them down into*


Figure 1-15. Plans enable agents to tackle larger tasks by breaking them down into
smaller steps and updating that plan as it’s executed to keep track of progress
By continuously referring back to this plan, the LLM is capable of executing each of
these tasks one at a time. Performing them all at once is seldom efficient, and each
task might influence another. As shown in Figure 1-16, after completing a specific
|
Chapter 1: Introduction

task, the LLM might still reason about which steps to take next. As such, reasoning is
fundamental and often a necessity for your agent to plan out complex behavior.



![Figure 1-16: After finishing a task, the agent reasons over its current plan to choose the](images/fig_01-16_After_finishing_a_task_the_agent_reasons.png)

*Figure 1-16: After finishing a task, the agent reasons over its current plan to choose the*


Figure 1-16. After finishing a task, the agent reasons over its current plan to choose the
next step, here marking the Google search complete and moving on to research papers on
arXiv
But creating a plan is not sufficient. The LLM might discover halfway through its
plan that some of its steps might not be appropriate. In our previous example, the
LLM would discover that Google and arXiv are insufficient as resources and instead
add a task to add Semantic Scholar and PubMed as resources to search.2
By reflecting on past behavior, agents can attempt to uncover their faults and make
attempts to fix them. Therefore, the initial plan can be continuously improved.
Illustrated in Figure 1-17, planning and reflection create an iterative loop of planning
out tasks, taking actions, and reflecting on the output.



![Figure 1-17: Reflection enables the agent to update a plan, often enabling it to adapt to](images/fig_01-17_Reflection_enables_the_agent_to_update_a.png)

*Figure 1-17: Reflection enables the agent to update a plan, often enabling it to adapt to*


Figure 1-17. Reflection enables the agent to update a plan, often enabling it to adapt to
new information uncovered during execution
Together, reasoning LLMs augmented with memory, tools, planning, and reflection
are what we consider to be an AI agent. In Chapter 6, we will explore planning and
reflection and how they connect all augmentations of the LLM to create the AI agent
(Figure 1-18).
2 arXiv is an open access archive hosting millions of research papers on computer science and other topics.
What Is an AI Agent?
|