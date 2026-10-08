---
title: "Core Components"
chapter_number: 84
page_start: 235
page_end: 235
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Core Components

Core Components
To achieve all these useful capabilities, MCP consists of three components:
MCP host
LLM application (such as Cursor) that manages connections, interprets tool
schema, and manages routing
MCP client
Maintains one-to-one connections with MCP servers
MCP server
Provides context, tools, and capabilities to the LLMs
The MCP host is any application that uses an LLM to use external tools. Typical
examples are chat assistants like ChatGPT or Claude and IDE extensions like Cursor
or GitHub Copilot. This is the “brain” of the MCP flow and it makes calls to the MCP
servers via the MCP clients.
The MCP client maintains connections with the MCP servers. They exist within the
host and handle the connection management, discovery of tool capabilities, request
forwarding, etc. Compared to the host, a client is a piece of code that handles the
communication with the MCP servers, whereas the MCP host only initiates the
communication.
The MCP server is a lightweight program that exposes APIs and tools via the MCP
standard. These servers often connect to a specific data source or service. For
instance, an MCP server might connect to all API endpoints of arXiv to search,
load, and view academic papers.
Servers expose three kinds of primitives to clients: tools (actions the LLM can invoke,
like /list_commits), resources (data the host can load as context, like files, docu‐
ments, and datasets), and prompts (reusable templates). The MCP host (e.g., GitHub
Copilot) contains one MCP client per server it connects to. The MCP servers expose
tools that may provide access to resources. These three components are depicted in
Figure 5-29.
Model Context Protocol
|