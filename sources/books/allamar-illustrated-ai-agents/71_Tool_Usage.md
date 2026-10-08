---
title: "Tool Usage"
chapter_number: 71
page_start: 197
page_end: 198
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Tool Usage

than a theoretical exercise. After all, how could an LLM act autonomously without
tools?



![Figure 5-4: A collection of tools is the main component allowing for interaction with the](images/fig_05-04_A_collection_of_tools_is_the_main_compon.png)

*Figure 5-4: A collection of tools is the main component allowing for interaction with the*


Figure 5-4. A collection of tools is the main component allowing for interaction with the
environment
Tool Usage
Tool usage consists of more steps than you might expect. It does not start with an
LLM using a tool, but by actually creating and defining the tools, planning which tool
to use instead, and eventually calling them. The steps in tool usage can be seen from
many different perspectives, such as the comparison of tools to the human action
system inspired by the human brain or as action modules that revolve around the
agent’s decisions.1,2,3 We, however, explore the following set of steps as it focuses on
concrete implementations and executions of tools:
- Tool creation
•
- Tool definition
•
- Tool selection
•
- Tool calling
•
- Output processing
•
1 Liu, Bang et al. 2025. “Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to
Evolutionary, Collaborative, and Safe Systems,” arXiv, 2504.01990.
2 Wang, Lei et al. 2024. “A Survey on Large Language Model Based Autonomous Agents,” Frontiers of Computer
Science, 18: 186345.
3 Wang, Zhiruo et al. 2024. “What Are Tools Anyway? A Survey from the Language Model Perspective,” arXiv,
2403. 15452.
Tool Usage
|

Although agents might seem like they can do everything themselves (which they
can attempt to a certain degree), they require help from the user or developer to
use the tools. Specifically, an LLM does not actually call the tool but merely shows
the intention of doing so. The actual tool call is typically executed by an external
(automated) process. This high-level process is shown in Figure 5-5, which is an
adaptation of OpenAI’s tool calling flow, where we additionally focus on creating the
tool and highlight the steps a single tool call takes.



![Figure 5-5: An example of tool creation, definition, selection, tool calling, and output](images/fig_05-05_An_example_of_tool_creation_definition_s.png)

*Figure 5-5: An example of tool creation, definition, selection, tool calling, and output*


Figure 5-5. An example of tool creation, definition, selection, tool calling, and output
processing in the interaction between a user and the LLM
Note that each step may have various forms and implementations, many of which we
will cover later. For now, let’s explore the most common way tool usage happens in
these steps and explore them in more detail.
|
Chapter 5: Tool Usage, Learning, and Protocols