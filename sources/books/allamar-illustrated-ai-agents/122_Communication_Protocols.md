---
title: "Communication Protocols"
chapter_number: 122
page_start: 327
page_end: 331
part: "Part II. Specialized Agents"
---
# Communication Protocols



![Figure 8-8: Agentic frameworks and harnesses all deploy different tactics for handling](images/fig_08-08_Agentic_frameworks_and_harnesses_all_dep.png)

*Figure 8-8: Agentic frameworks and harnesses all deploy different tactics for handling*


Figure 8-8. Agentic frameworks and harnesses all deploy different tactics for handling
things like memory and planning
With the ever-changing landscape of AI agents, it’s difficult to suggest a single plat‐
form as the “best.” Experimentation will be key when deciding on frameworks, but
also the independence of certain platforms and the continued development.
Depending on how autonomous you would want your agent(s) to be, the open
source framework n8n might also be an interesting tool to use. Compared to the
previous frameworks, it’s an AI workflow automation tool that requires you to create
predefined workflows for the LLMs and agents to follow. However, agents might still
have a degree of autonomy within such a framework, making it just on the edge of a
MAS.
Communication Protocols
Setting up communication between agents can be challenging, as the way they
exchange information greatly affects performance. Effective context engineering, as
we covered in Chapter 4, requires optimizing both inputs and outputs. Too much or
too little information, or using the wrong format, can degrade results. Achieving the
right balance of communication is therefore essential.
Before LLMs, agent communication languages (ACLs) such as FIPA-ACL and KQML
offered a standardization for agents to interact and share information using message
types such as “request” and “inform.”6,7 Since the rise of modern LLMs, beginning
6 Poslad, Stefan. 2007. “Specifying Protocols for Multi-agent Systems Interaction,” ACM Transactions on Auton‐
omous and Adaptive Systems (TAAS), 2.4:15-es.
Orchestrating Agents
|

with GPT-3.5 in late 2022, protocols have been developed to facilitate communication
between agents and tools, such as the Model Context Protocol (MCP; see Chapter 5).
MAS, as a typically collaborative system, would greatly benefit from standardized
Agent2Agent (A2A) communication protocols.
A2A, first developed by Google, is a major protocol for inter-agent communication.8
A2A allows agents developed on different frameworks and by different organizations
to work together regardless of their underlying architecture. Imagine you want to
create a MAS of several agents working together, but each agent is developed by
different frameworks (LangGraph, CrewAI, AutoGen, etc.) and on different cloud
platforms (e.g., Azure, AWS, Google Cloud, etc.). To connect all these agents, you
would generally have to create custom connections. A2A allows agents to communi‐
cate with each other through a standardized inter-agent communication protocol. As
shown in Figure 8-9, this reduces the complexity of needing to continuously create
custom connections.



![Figure 8-9: The A2A protocol standardizes and reduces the number of custom agent](images/fig_08-09_The_A2A_protocol_standardizes_and_reduce.png)

*Figure 8-9: The A2A protocol standardizes and reduces the number of custom agent*


Figure 8-9. The A2A protocol standardizes and reduces the number of custom agent
connections needed
Much like MCP, A2A is an open standard that enables communication, but for
collaboration between agents instead. Figure 8-10 shows an example of how this
7 Finin, Tim et al. 1994. “KQML As an Agent Communication Language,” Proceedings of the Third International
Conference on Information and Knowledge Management.
8 Google. “Announcing the Agent2Agent Protocol (A2A),” https://developers.googleblog.com/en/a2a-a-new-era-
of-agent-interoperability. Accessed December 4, 2025.
|
Chapter 8: Multi-Agent Systems

protocol provides communication between two agents that both have access to MCP
but are hosted on different infrastructures.



![Figure 8-10: An overview of the interaction between MCP and A2A](images/fig_08-10_An_overview_of_the_interaction_between_M.png)

*Figure 8-10: An overview of the interaction between MCP and A2A*


Figure 8-10. An overview of the interaction between MCP and A2A
A2A allows agents to discover each other and their capabilities, exchange (un-)struc‐
tured information across modalities such as text and images, stream responses, and
even handle multi-turn conversations. Likewise, this allows agents to collaborate
remotely and exchange relevant information and states needed to solve complex
tasks.
There are three core actors in A2A interactions:
User
The user, generally a human but can be an automated process, that initiates a
request and/or defines a goal.
A2A client (client agent)
The client is the agent that initiates communications to other agents on behalf of
the user. This is the entity that uses the A2A protocol.
A2A server (remote agent)
These are the agents that are being called upon by the client agent to execute a
given task. It can be a single agent or an entire MAS.
Using these three actors, let’s go through an example of how communication works
through the following steps:
Orchestrating Agents
|

1. Task initiation
1.
2. Discovery
2.
3. Authentication
3.
4. Client agent communication
4.
5. Remote agent communication
5.
In step 1, the user defines a task to be completed for the A2A client. This is done
without the need for an A2A protocol since the communication is not between two
(or more) agents.
In step 2, discovery, the client agent will first need to discover which agents are
available and what they can do. Defined by the A2A protocol, each agent needs to
expose a .json file describing their capabilities, endpoint URL, and other relevant
information. This is called the agent card and is accessible at /.well-known/agent-
card.json. Here is an example of the agent card for a train agent that helps users
book train tickets:
{
 "name": "Train Agent",
 "description": "Helps book train tickets",
 "url": "http://localhost:8000/",
 "version": "1.0.0",
 "capabilities": {
 "streaming": true,
 "pushNotifications": true,
 "stateTransitionHistory": false
 },
 "defaultInputModes": [
 "text",
 "text/plain"
 ],
 "defaultOutputModes": [
 "text",
 "text/plain"
 ],
 "skills": [
 {
 "id": "book_train_tickets",
 "name": "Book Train Tickets",
 "description": "Helps with booking train tickets",
 "tags": [
 "Book train tickets"
 ],
 "examples": [
 "Book return tickets from Eindhoven to Brussels on November 20"
 ]
 }
|
Chapter 8: Multi-Agent Systems

]
}
In step 3, after the client agent has decided which remote agent to access, it goes
through the authentication described in the agent card’s security scheme, which
allows for various security schemes, such as API keys and OAuth 2.0.
In step 4, the communication has been authenticated, and the client agent sends a
request to the remote agent through HTTPS with JSON-RPC 2.0, much like MCP.
The remote agent receives the communication and will start working. If the remote
agent requires more information, it will send a message back to the client agent to
request more information. While working on the task, the remote agent can stream
updates to notify the client agent when the task is completed.
In step 5, once the remote agent has completed its tasks, it will send a message to the
client agent along with any relevant information or artifacts.
The steps of discovery, authentication, task communication, and task execution are
illustrated in Figure 8-11.
Although A2A is not the only protocol out there, with a technology as new as
A2A, there are not many competitors. One notable framework is Internet of Agents
(IoA), which describes an agent integration protocol for creating MASs.9 Based on
the concept of the internet, it features an instant messaging–like design and dynamic
modules for agent conversation and collaboration. In contrast, improving the stand‐
ardization and collaboration can be explored through the lens of RL for MAS.10 Here,
RL can be used to train LLMs and agents in the context of MAS, thereby having these
entities already experienced with such systems.
Standardized protocols and communication are rather new fields in MAS, as is MAS
itself. The important thing to note is to start thinking about what it means to have
standardization, why it’s required, and with what common methodologies it can be
achieved.
9 Chen, Weize et al. 2024. “Internet of Agents: Weaving a Web of Heterogeneous Agents for Collaborative
Intelligence,” arXiv, 2407.07061.
10 Sun, Chuanneng et al. 2024. “LLM-based Multi-Agent Reinforcement Learning: Current and Future Direc‐
tions,” arXiv, 2405.11106.
Orchestrating Agents
|