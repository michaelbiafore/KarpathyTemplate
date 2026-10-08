---
title: "Tool Selection"
chapter_number: 74
page_start: 205
page_end: 205
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Tool Selection

Tool Selection
Now that the tools are created and defined, we can start the process of calling the
tool. The LLM first needs to select the right tool for a given query, which can be
a difficult task. Especially with potentially dozens of complex tools available, the
LLM not only needs to select the most appropriate one (if one at all) but also use it
correctly. Although we can share an extensive JSON schema for each tool, the LLM
needs to be capable enough to actually follow it through. This is where reasoning
LLMs shine. They can spend any number of tokens “thinking” about which tools
to use and how to properly use them as long as they fit within the context window
and leave enough for generating the answer. Illustrated in Figure 5-7 is the reasoning
process of LLMs to decide which tool to use and how.



![Figure 5-7: The reasoning process of an LLM deciding which tool to use](images/fig_05-07_The_reasoning_process_of_an_LLM_deciding.png)

*Figure 5-7: The reasoning process of an LLM deciding which tool to use*


Figure 5-7. The reasoning process of an LLM deciding which tool to use
Discovering the tools that exist or might be relevant becomes more important when
the number of tools increases. As discussed in Chapter 4, even when you have a large
context window, filling it up to the brim with tool JSON schemas is bound to decrease
the LLM’s performance. As with context engineering, the process of discovering tools
might be helped with methodologies like RAG, where you store all tool schemas in a
separate database for the LLM to discover. Figure 5-8 illustrates this idea of using a
vector database to discover which tools are most relevant to a user’s query.
Note that the planning capabilities of LLMs are vital to having a good selection. For
simple queries, such as “What is 1 + 1?,” the selection of tools is not going to be a
challenge. However, when planning a vacation with a budget, a multi-step process is
going to be needed where the agent first needs to plan out its behavior. This planning
(and reflection) behavior is going to be discussed in Chapter 6 in more detail.
Tool Usage
|