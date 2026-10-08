---
title: "Types of Memory"
chapter_number: 57
page_start: 153
page_end: 154
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Types of Memory

Throughout this chapter, we’ll explore many types of memory modules, ranging from
short-term and long-term memory to external memory modules, through methods
like (agentic) Retrieval-Augmented Generation. Shown in Figure 4-3, it forms the
foundation of the agent. After all, how would an agent be able to use tools or create
plans if it keeps forgetting them?



![Figure 4-3: Without memory, tool usage and planning would not be possible. Both](images/fig_04-03_Without_memory_tool_usage_and_planning_w.png)

*Figure 4-3: Without memory, tool usage and planning would not be possible. Both*


Figure 4-3. Without memory, tool usage and planning would not be possible. Both
require memory modules to track behavior over long traces.
Types of Memory
Memory for LLMs tends to follow human memory types, as the agents that we
attempt to create are often modeled after human behavior. Instead of going through
all forms of human memory types, of which there are many, the “Cognitive Archi‐
tectures for Language Agents” paper describes four types of external memory that
we often see in agents, working memory for short-term use, and three variants of
long-term memory: episodic, semantic, and procedural memory.1
Working memory is a type of short-term memory that is typically defined as a system
with limited capacity that temporarily holds information that we need for things like
decision-making and reasoning. For LLMs, it’s typically data that persists across LLM
calls. More specifically, it’s the chat history of the LLM that is continuously fed back
to the LLM.
1 Sumers, Theodore et al. 2023. “Cognitive Architectures for Language Agents,” Transactions on Machine
Learning Research.
Types of Memory
|

For long-term memory, there are three forms described:
Episodic memory
Involves remembering specific events and experiences from one’s past (e.g., your
last birthday party). For agents, this typically involves specific actions the agent
has taken thus far and their outcomes.
Semantic memory
Involves remembering knowledge about the world (e.g., the capital of France).
For agents, this may involve querying an external database like Wikipedia or the
codebase that you’re working on.
Procedural memory
Involves remembering patterns of how to do things (e.g., writing code in
Python). For agents, this can be information hidden in its parameters (also called
parametric memory) or the system prompt, which persists across calls.
Figure 4-4 shows an example of how these different forms of memory can be used
and interpreted during a single agent’s session.



![Figure 4-4: Memory can be divided into four different types when interacting with](images/fig_04-04_Memory_can_be_divided_into_four_differen.png)

*Figure 4-4: Memory can be divided into four different types when interacting with*


Figure 4-4. Memory can be divided into four different types when interacting with
LLMs, namely working, procedural, episodic, and semantic memory
As mentioned previously, we can also consider the type of memory that the model
already has, parametric memory.2 Without any memory modules, LLMs are trained
to a certain extent to retain information. If you ask an LLM what the capital of
France is, most LLMs will correctly remember that it is Paris. The answer is therefore
contained within the parameters of the model and the model attempts to retrieve
it. Although a relatively new field, it’s technically possible to instill information into
2 Zhang, Zeyu et al. 2024. “A Survey on the Memory Mechanism of Large Language Model based Agents,” ACM
Transactions on Information Systems, 43(6):1-47.
|
Chapter 4: Memory