---
title: "Model Context Protocol"
chapter_number: 83
page_start: 232
page_end: 234
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Model Context Protocol

agent = TinyAgent(llm=llm, memory=memory, tools=tools)
agent.run("What is 5.1 times 7.3?")
After running the agent, let’s look at the memory to see if and how it called the tool:
print(agent.memory.get_messages())
Which gives:
[
 {'role': 'system', 'content': 'You are a helpful assistant.\n\n'},
 {'role': 'user', 'content': 'What is 5.1 times 7.3?'},
 {
 'role': 'assistant',
 'content': '',
 'tool_calls': [
 {
 'id': 'call_vdc4hgze',
 'function': {
 'arguments': '{"a":"5.1","b":"7.3"}',
 'name': 'multiply'
 },
 'type': 'function',
 'index': 0
 }
 ]
 },
 {'role': 'tool', 'content': '37.23'}
]
The tool was called successfully! Note how it uses tool_calls to identify the tool and
parameters while the tool role is used to observe the output.
What We Built
TinyAgent/
├── agent.py ← Updated (Added `(Native)Tools` to your `TinyAgent`)
├── llm.py
├── memory.py
├── toolbox.py ← New (A place to store your functions/tools)
├── tools.py ← New (Added`Tools` and `Native`)
└── trajectory.py
Model Context Protocol
In the previous sections, we explored how to connect tools to LLMs, making them
capable of much more than text generation. Although their ability to then use tools
is incredible, it’s not a free lunch. Imagine you have developed several prompts to
instruct your LLM on how to use tools. As is typical in this field, a new LLM is
released that you would like to try out, together with all the tools. Now imagine it has
|
Chapter 5: Tool Usage, Learning, and Protocols

a new way of calling tools, which means you will have to create new integrations for
all your tools. This is the N × M problem, where N is the number of LLMs and M is
the number of tools available. You would have to write custom integrations for every
LLM/tool combination.
Model Context Protocol (MCP) solves this problem by standardizing how you would
connect tools and APIs with different structures to your LLM. MCP is an open
standard and framework developed by Anthropic and released in November 2024.14
As a protocol, it facilitates two-way communication between tools and LLMs. It’s
often referred to as the “USB-C port of AI” due to its universal nature, allowing for
any LLM to implement any tool that follows this protocol. Shown in Figure 5-27,
instead of manually creating connections between LLMs and tools, MCP creates only
a single connection that can be maintained indefinitely by the tool provider.



![Figure 5-27: MCP requires fewer custom connections than traditional tool integrations](images/fig_05-27_MCP_requires_fewer_custom_connections_th.png)

*Figure 5-27: MCP requires fewer custom connections than traditional tool integrations*


Figure 5-27. MCP requires fewer custom connections than traditional tool integrations
By having the MCP server handle the integrations and communicate the tools to the
LLMs, it becomes N + M connections that need to be maintained instead of N × M
connections. Moreover, as long as the tool provider has an MCP server, connecting
the server to your LLM is relatively straightforward, but more on that later.
The maintenance of the integration, therefore, also moves from the user to the tool
provider. Without MCP, if arXiv’s API were to suddenly change drastically, then
each user would have to adjust their integrations. With MCP, any changes to the
API would need to be resolved only once by the maintainers of that API. Then, the
updates can be rolled out to all users without any intervention from their side.
14 Anthropic, November 25, 2024. “Introducing the Model Context Protocol,”.
Model Context Protocol
|

To illustrate this point a bit further, if you were to add tools to your LLM manually, all
tools would have to be:
- Manually tracked and fed to the LLM
•
- Manually described (including its expected JSON schema)
•
- Manually updated whenever its API changes
•
As shown in Figure 5-28, this can be quite the hassle for maintaining your tools.



![Figure 5-28: An overview of the difficulty in describing tool definitions in the system](images/fig_05-28_An_overview_of_the_difficulty_in_describ.png)

*Figure 5-28: An overview of the difficulty in describing tool definitions in the system*


Figure 5-28. An overview of the difficulty in describing tool definitions in the system
prompt only
Thus, MCP not only solves the N × M problem but also the problem of standardiza‐
tion. Note that MCP is not the only protocol for standardizing communication, like
Agent2Agent (A2A) for standardizing interagent communication.15 Although there
are others, in 2026, it is arguably one of the most popular protocols out there.16 There
are MCP servers for Figma, GitHub, Home Assistant, and many others. You can find
a nice overview of MCP servers on GitHub.
15 Google. “a2aproject/A2A,” https://github.com/google/A2A. Accessed 02 October 2025.
16 Yang, Yingxuan et al. 2025. “A Survey of AI Agent Protocols,” arXiv, 2504.16736.
|
Chapter 5: Tool Usage, Learning, and Protocols