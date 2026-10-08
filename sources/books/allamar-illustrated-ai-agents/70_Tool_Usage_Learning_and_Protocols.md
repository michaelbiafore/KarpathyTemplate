---
title: "Chapter 5. Tool Usage, Learning, and Protocols"
chapter_number: 70
page_start: 195
page_end: 196
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Chapter 5. Tool Usage, Learning, and Protocols

Tool Usage, Learning, and Protocols
The tool module is such an interesting module for augmenting your LLM and gener‐
ating autonomous behavior in agents. By themselves, regular LLMs are nothing more
than functions that take in some text and output some text. Although that creates
interesting chatbots, they cannot yet interact with their environment. Tools, in the
form of functions and APIs, allow LLMs to step into the real world and interact with
any system exposed to the LLM, ranging from codebases and internal tools to online
databases and even home assistants.
A key trait that defines an agent is its ability to autonomously search for, select,
and utilize tools, allowing it to interact with and influence its environment. With
enough capabilities, agents can even create their own set of tools to use. Generally,
tools allow an LLM to take action and interact with the external environment or
extract data and use external applications (see Figure 5-1). The benefit of tools is
not contained to interaction with the environment. Tools are typically used to access
external knowledge or memories, as we discussed in Chapter 4. We can even use tools
to access specialized LLMs that have capabilities that extend beyond what the agent
is capable of, such as multi-modal LLMs or LLMs specialized for certain tasks (like
coding).



![Figure 5-1: Tools can be categorized as either taking an action or retrieving information](images/fig_05-01_Tools_can_be_categorized_as_either_takin.png)

*Figure 5-1: Tools can be categorized as either taking an action or retrieving information*


Figure 5-1. Tools can be categorized as either taking an action or retrieving information
However, regular LLMs cannot search the web, use a calculator, or schedule appoint‐
ments. They can only communicate the intention of doing so, without being able to

act upon it. Without tools, agents can only think and plan autonomously but not act
autonomously.
The degree of autonomy also decides how tools are used. As shown in Figure 5-2, if
there is no autonomy but there is a fixed flow, then tools can be used in a predefined
order. For instance, a research agent might always call tools like arXiv and Google to
extract results, which are subsequently summarized.



![Figure 5-2: An example of a fixed flow in tool usage](images/fig_05-02_An_example_of_a_fixed_flow_in_tool_usage.png)

*Figure 5-2: An example of a fixed flow in tool usage*


Figure 5-2. An example of a fixed flow in tool usage
In contrast, systems with larger degrees of autonomy allow agents to choose which
tool to use and when. Illustrated in Figure 5-3, they are still sequences of LLM calls
but with autonomous selection of tools decided by the agent.



![Figure 5-3: An agent dynamically using tools—it first searches using the Google tool,](images/fig_05-03_An_agent_dynamically_using_toolsit_first.png)

*Figure 5-3: An agent dynamically using tools—it first searches using the Google tool,*


Figure 5-3. An agent dynamically using tools—it first searches using the Google tool,
then the arXiv tool, then it generates an answer informed by the results of both searches
There’s a lot more to tools than merely using them. How are they created? How is the
output of a tool processed by the LLM or agent? How are tools selected? How many
tools can an LLM effectively handle?
Throughout this chapter, we’ll not only explore several types of tools but also how
LLMs and agents learn to use them and even how these tools can be standardized
across different agentic systems. As shown in Figure 5-4, this allows interaction with
the environment. It makes the next chapter, about planning out actions to take, more
|
Chapter 5: Tool Usage, Learning, and Protocols