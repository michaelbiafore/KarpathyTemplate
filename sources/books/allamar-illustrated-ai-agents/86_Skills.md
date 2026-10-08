---
title: "Skills"
chapter_number: 86
page_start: 238
page_end: 238
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Skills

When the LLM receives the results (10), it can choose to run another tool or return
the output to the MCP host and then to the user. In our example, the LLM decides
to summarize the five latest commits that it received (11) and return the summary to
the user (12) (Figure 5-32).



![Figure 5-32: The results of the tool usage are processed by the LLM and returned to the](images/fig_05-32_The_results_of_the_tool_usage_are_proces.png)

*Figure 5-32: The results of the tool usage are processed by the LLM and returned to the*


Figure 5-32. The results of the tool usage are processed by the LLM and returned to the
MCP host before sending them back to the user
What makes these sets of steps so special is that the LLM can discover tools that exist,
choose which one to use, and does not have to think much about deprecated API
functionalities.
Note that the LLM should still have tool-calling capabilities. Whenever it wants to
execute a given tool, it should follow the MCP, which follows a JSON-like structure.
This structure, following the JSON-RPC 2.0 Specification, is also communicated by
the MCP client, which serves as the middleman between the LLM and the protocol.
In the book’s GitHub repository, you’ll find an additional notebook that goes through
implementing MCP into your TinyAgent step-by-step.
Skills
With modules like tools and MCP, we can give an agent access to various actions
it can take. However, when exactly to use those actions and how they fit into a
larger workflow is not covered by any of these modules. Your agent is not intimately
familiar with your team’s workflow, preferred tools, or coding standards. Having to
repeat to your agent, every time you initialize it, that it should use uv over pip can
|
Chapter 5: Tool Usage, Learning, and Protocols