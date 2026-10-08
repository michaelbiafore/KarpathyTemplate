---
title: "General-Purpose Frameworks for Collaborative Task-Solving Patterns"
chapter_number: 121
page_start: 323
page_end: 326
part: "Part II. Specialized Agents"
---
# General-Purpose Frameworks for Collaborative Task-Solving Patterns

General-Purpose Frameworks for Collaborative Task-Solving Patterns
With MASs, there’s not a single framework, pattern, or orchestration workflow that
is best for all use cases. As such, many different general-purpose frameworks have
been developed that allow users to build their own MAS. Each framework, however,
does have a distinct “flavor” of implementation and philosophy, which are worth
exploring.
CAMEL
One of the first frameworks for a collaborative MAS is Communicative Agents
for “Mind” Exploration of Large Language Model Society (CAMEL). CAMEL is an
agentic framework that revolves around having agents roleplay as a way to create
specialized entities that collaborate.
CAMEL starts with an idea proposed by the user. This is generally a simple task
description of what the user wants the system to achieve. For instance, an idea could
be: “create a website for my blog.” Then, two agents with specific roles are created,
namely the AI user and AI assistant. The AI user represents the user and is in charge
of giving instructions and directing the AI assistant. The AI assistant executes the
given instructions and is specialized in its execution. Roles for the AI user and AI
assistant could be “blogger” and “programmer,” respectively. Then, these entities are
fed to the task specifier agent to provide a more detailed description of the initial
task. Because it has knowledge about the assigned roles, it can rewrite the user’s
query to something that is more aligned with the task. These user-driven concepts are
illustrated in Figure 8-5.
Finally, the AI user and AI assistant will take up their roles and converse with each
other about how to best solve the query as provided by the task specifier agent. This
is achieved by multi-turn conversations until the AI user ends the conversation and
returns a completed answer. This role playing–like structure is shown in Figure 8-6,
where the AI user takes on the role of the user and the AI assistant the role of the
programmer.
This role-playing methodology enables collaborative communication between agents
and is an interesting first look into general-purpose frameworks.
Orchestrating Agents
|



![Figure 8-5: Different agents working together to solve a given task in CAMEL](images/fig_08-05_Different_agents_working_together_to_sol.png)

*Figure 8-5: Different agents working together to solve a given task in CAMEL*


Figure 8-5. Different agents working together to solve a given task in CAMEL



![Figure 8-6: The interaction between the AI user and AI assistant when solving a](images/fig_08-06_The_interaction_between_the_AI_user_and.png)

*Figure 8-6: The interaction between the AI user and AI assistant when solving a*


Figure 8-6. The interaction between the AI user and AI assistant when solving a
user-defined task
|
Chapter 8: Multi-Agent Systems

MetaGPT
This idea of role-playing has found its way to many such general-purpose frame‐
works, as LLMs are quite adaptable to different situations that require specialized
perspectives and capabilities. MetaGPT takes it one step further and attempts to
mimic entire organizational structures with specialized roles.4 This framework has
three components to its MAS:
Specialization of roles
Tasks are broken down into smaller, specific tasks that can be solved with special‐
ized agents.
Communication protocol
A protocol that enhances the efficiency of communication while also providing
structured interfaces.
Iterative programming with executable feedback
External feedback incorporated as a self-correction mechanism.
The specialization of roles in MetaGPT starts with breaking down complex tasks
and queries into smaller and more specific tasks, as we explored in Chapter 6. To
solve these individual tasks, MetaGPT defines specialized agent roles that collaborate
through diverse skills and expertise. This framework takes inspiration from organi‐
zational structures by often referencing software companies, where, for instance, a
product manager will have different skills and tasks to complete compared to an
engineer. As such, each role will have a profile including name, goal, skills, and
constraints for that particular role. Through those specializations, MetaGPT adheres
to a standard operating procedure (SOP) for software development where all agents
will work sequentially. Each agent is powered by ReAct.
The authors also developed a communication protocol to allow for both structured
and unstructured information to be shared. Instead of communicating primarily
through dialogue, MetaGPT does so through artifacts like documents and diagrams
(structured output).
Finally, each agent will be tasked with iterating on their own output as a way to
self-correct and improve their behavior. For instance, an engineer might be tasked
not only with creating code but also with running and debugging if necessary
(Figure 8-7).
4 Hong, Sirui et al. 2023. “MetaGPT: Meta Programming for a Multi-agent Collaborative Framework,” The
Twelfth International Conference on Learning Representations.
Orchestrating Agents
|



![Figure 8-7: A pipeline of agents working together in MetaGPT](images/fig_08-07_A_pipeline_of_agents_working_together_in.png)

*Figure 8-7: A pipeline of agents working together in MetaGPT*


Figure 8-7. A pipeline of agents working together in MetaGPT
MetaGPT takes role-playing quite literally and attempts to reconstruct existing
organizational structures to enforce task decomposition and specialization.
Production-grade frameworks
Although the previous methodologies were open sourced, the following frameworks
were created from a developer’s perspective, rather than being an important artifact of
a research paper. In other words, these were meant to be products used to build and
scale MASs in production.
At the end of 2025, the most common frameworks were Microsoft’s AutoGen,5
LangGraph, and CrewAI. Each of these frameworks focuses on modularity and allows
you to build any MAS in whichever way you would like. As shown in Figure 8-8, this
entails all different kinds of roles, memory modules, and tools that can be selected for
each agent, as well as the pattern of the system.
5 Wu, Qingyun et al. 2024. “Autogen: Enabling Next-Gen LLM Applications Via Multi-agent Conversations,”
First Conference on Language Modeling.
|
Chapter 8: Multi-Agent Systems