---
title: "Orchestrating Agents"
chapter_number: 119
page_start: 317
page_end: 317
part: "Part II. Specialized Agents"
---
# Orchestrating Agents

This chapter explores many more advantages and disadvantages because these com‐
plex systems are used for a wide array of use cases. Due to their flexibility, MASs can
be used across many industries and applications. Examples include the following:
Anthropic
Anthropic, a leading AI organization building the Claude models, used multiple
Claude agents to build a research system, allowing users to explore complex
topics more effectively.
Uber
Uber created a data-retrieval MAS that uses a supervisor agent and several data-
retrieval agents (such as an SQL agent) to transform user requests into real-time
financial intelligence.
Delivery Hero
Delivery Hero, a multinational online food ordering and food delivery company,
uses several agents to extract entities and create product titles, thereby building a
product knowledge base.
These are just some examples of MASs, but we’ll cover many more of them as we
explore specific architectures and general-purpose frameworks.
Orchestrating Agents
Deploying multiple agents in a system is not straightforward. You’ll have to ask
yourself how they should be deployed, in what kind of architectures and specialisms,
and how they communicate with one another. As such, the orchestration of agents
is a vital component in creating a stable and future-proof system. Before we go into
specific frameworks, let’s first explore common patterns in orchestrating agents and
how we can standardize communication techniques between agents.
Patterns
Patterns in MASs refer to how agents are set up in relation to one another. It’s
the topology of the system and how agents are defined to specific roles and tasks,
but most importantly, how they interact and communicate. There are four types of
communication structure of MASs:
Centralized
The responsibility of communication and its management is controlled by a
single orchestration agent that allocates responsibilities and tasks to other agents.
Decentralized
Each agent shares similar responsibilities, and the communication is distributed
among them with no clear “leader.”
Orchestrating Agents
|