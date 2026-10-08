---
title: "The Multi-Agent System"
chapter_number: 118
page_start: 314
page_end: 316
part: "Part II. Specialized Agents"
---
# The Multi-Agent System

The Multi-Agent System
Instead of a single agent, a multi-agent system (MAS) contains multiple agents collab‐
orating, coordinating, or at times even competing to achieve a goal (see Figure 8-1).
Although these agents work toward a common goal, each may have specific goals
they need to achieve. The search agent and summarization agent have different roles
but serve the same end goal.



![Figure 8-1: The difference between a single agent and multi-agentic behavior](images/fig_08-01_The_difference_between_a_single_agent_an.png)

*Figure 8-1: The difference between a single agent and multi-agentic behavior*


Figure 8-1. The difference between a single agent and multi-agentic behavior
Agents may share an environment in which they can make decisions, like being char‐
acters in a virtual game. However, these systems do not have to share an environment
and may be responsible for different tasks. A booking system, for example, might
have an agent searching the web for nice places to visit, another agent to research
cheap flights, and an agent scheduling the vacation. Likewise, the environments they
occupy can be physical (real-world agents typically in the form of robotic agents),
virtual (game-like environments for agents to interact with), and text (environments
like coding IDEs or chat interfaces).1 These different environments and patterns are
illustrated in Figure 8-2.
Compared to a single-agent system, which has issues scaling to large or complex
use cases, a multi-agent system can excel in these environments by, for instance,
deploying more agents, each solving a different task.
1 Xi, Zhiheng et al. 2025. “The Rise and Potential of Large Language Model-based Agents: A Survey,” Science
China Information Sciences, 68.2: 121101.
|
Chapter 8: Multi-Agent Systems



![Figure 8-2: An overview of environments and patterns in agentic systems](images/fig_08-02_An_overview_of_environments_and_patterns.png)

*Figure 8-2: An overview of environments and patterns in agentic systems*


Figure 8-2. An overview of environments and patterns in agentic systems
Depending on the system, agents may collaborate or compete and take on different
roles.2 Homogeneous agents have similar capabilities and are typically used for effi‐
cient parallel task execution. Heterogeneous agents typically differ in roles, where each
has different goals and tasks to complete. The search agent and summarization agent
have different roles and may be initialized with different LLMs, memory systems,
and tools. Emergent specialization arises when identical agents evolve into specialized
roles through interaction with each other and their environments. For instance,
in game-like simulations, some agents may learn specific abilities such as resource
gathering or defensive roles (Figure 8-3).3
2 Liu, Bang et al. 2025. “Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to
Evolutionary, Collaborative, and Safe Systems,” arXiv, 2504.01990.
3 Altera.AL et al. 2024. “Project Sid: Many-Agent Simulations Toward AI Civilization,” arXiv, 2411.00114.
The Multi-Agent System
|



![Figure 8-3: An overview of agent roles within systems](images/fig_08-03_An_overview_of_agent_roles_within_system.png)

*Figure 8-3: An overview of agent roles within systems*


Figure 8-3. An overview of agent roles within systems
The collective nature of multi-agent systems, therefore, allows for a wide range of
benefits:
Collaboration
Complex and diverse problems can be solved more easily by increasing the
number of agents and having them work together.
Scalability
Depending on the system, the number of agents can be increased without slow‐
ing down the system by running them in parallel or fully asynchronously.
Speed
Instead of having a single agent sequentially solve each task, multiple agents can
not only solve them in parallel, but specialized agents tend to solve each task
faster than a single non-specialized agent would.
However, MASs are not a free lunch and have several disadvantages:
Complex
They are complex systems that require careful management of the orchestration
of the agents and how they interact. Likewise, there are additional layers of
abstraction due to the interaction of agents.
Cost
Increasing the number of agents can be a computationally costly process if the
agents rely on powerful LLMs.
Evaluation
Evaluating an agent is already a tricky process, now imagine having to evaluate
many working together.
|
Chapter 8: Multi-Agent Systems