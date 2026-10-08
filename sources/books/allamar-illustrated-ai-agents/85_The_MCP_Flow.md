---
title: "The MCP Flow"
chapter_number: 85
page_start: 236
page_end: 237
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# The MCP Flow



![Figure 5-29: The main three components of MCP, namely the client, server, and host](images/fig_05-29_The_main_three_components_of_MCP_namely.png)

*Figure 5-29: The main three components of MCP, namely the client, server, and host*


Figure 5-29. The main three components of MCP, namely the client, server, and host
The MCP Flow
MCP can be a bit of a mystery, even when showing and describing the core compo‐
nents. Instead, let’s go through an example of what it would be like to use the MCP to
discover and call tools. Imagine you want your AI assistant (perhaps GitHub Copilot
or Claude code) to summarize the five latest commits from your repository. This flow
is numbered in the upcoming figures so we can accurately track each individual step.
It would all start with the user’s query: “Summarize the 5 latest commits.” Shown in
Figure 5-30, this prompt is sent to the MCP host (1), which asks the MCP server,
through the MCP client, which tools are available (2). The MCP server is connected
to the set of tools (GitHub) and returns the list of all available API calls back to
the MCP host (3). API calls might include common methodologies like listing all
commits (/list_commits) or creating a pull request (/create_pr). Then, the initial
prompt, together with available tools, is sent to the LLM (4).
Next, the LLM may choose to use any of the tools that were returned. Since the
user’s query is about commits, the LLM decides that it wants the MCP server to use
the /list_commits tool (5). The MCP client communicates this action to the MCP
server (6), which finally executes the command (7). The output of the tool usage is
returned to the MCP server (8), which communicates it back to the MCP client and
host through the MCP (9) (Figure 5-31).
|
Chapter 5: Tool Usage, Learning, and Protocols



![Figure 5-30: The first steps in using MCP, which mainly includes checking which tools are](images/fig_05-30_The_first_steps_in_using_MCP_which_mainl.png)

*Figure 5-30: The first steps in using MCP, which mainly includes checking which tools are*


Figure 5-30. The first steps in using MCP, which mainly includes checking which tools are
available on the MCP server



![Figure 5-31: After listing the tools, the LLM decides which tool to use, executed via the](images/fig_05-31_After_listing_the_tools_the_LLM_decides.png)

*Figure 5-31: After listing the tools, the LLM decides which tool to use, executed via the*


Figure 5-31. After listing the tools, the LLM decides which tool to use, executed via the
MCP server
Model Context Protocol
|