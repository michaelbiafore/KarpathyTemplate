# Measuring Reliability with pass^k through Agent Society

## Measuring Reliability with pass^k

pass@k rewards succeeding at least once in k tries, so it climbs with more attempts — capability, not reliability. pass^k asks whether *all* k attempts succeed. The same runs yield both, and they can rank models differently. The estimator flips pass@k's combinatorics: from c correct of n samples, `comb(c, k) / comb(n, k)`, zero when c < k. It comes from τ-bench (Yao et al., 2024). The pass@3 ceiling guides checkpoint choice; for an API vendor shipping as-is, reliability wins.

![Figure 7-12: Pass³, pass@1, and pass@3 across 10 models on the SWE Atlas Codebase](images/fig_07-12_Pass³_pass1_and_pass3_across_10_models_o.png)

*Figure: GPT-5.4 and Opus 4.7 tie at pass@1 = 40, yet GPT-5.4's pass³ of 28 beats Opus 4.7's 23 while Opus 4.7 tops pass@3 at 60 — each model's dot spread is its reliability gap.*

## Safety: Does It Avoid Harm?

Agents send email, delete files, drop databases, so safety needs its own suite — organized by who causes the harm. Misuse: a malicious user requests a harmful task; AgentHarm scores refusal rate and harm. Manipulation through data: prompt injection hides instructions in retrieved documents, tool results, or web pages; memory poisoning corrupts what the agent later retrieves; AgentDojo and Agent Security Bench report attack success rates. Third, no adversary at all — the agent errs on a benign task, the least standardized case, leaning on your own guardrails and harness design.

## Building Your Own Evals

The best signal is a small curated eval representative of your real task and data, weighted toward failure modes, scored with exact match, programmatic checks, LLM-as-a-judge, and rubrics, re-run on every change. Even 5–10 cases are eye-opening; starting beats perfecting. Scale needs a harness — `harbor` is a recent agent-specific one, and Terminal-Bench ships through its registry.

## Summary

Chapter 7 covered benchmark categories, reading scores critically (contamination, prompt tuning, cost, saturation), human evaluation as gold standard, the automated spectrum from exact match to rubrics, trajectory evaluation, reliability, and safety. Part II turns to multi-agent systems, multi-modal understanding, and coding agents.

## Chapter 8. Multi-Agent Systems

A multi-agent system (MAS) replaces the lone planning-executing-reflecting agent with many agents, each with its own autonomy, tools, subgoals, even personality. A research system is canonical: rather than one agent juggling search, paper processing, critique, and summarization, assign specialists.

## The Multi-Agent System

Agents collaborate, coordinate, or compete; they may share an environment (game characters) or occupy separate ones. Environments can be physical, virtual, or text.

![Figure 8-1: The difference between a single agent and multi-agentic behavior](images/fig_08-01_The_difference_between_a_single_agent_an.png)

*Figure: a single agent loops over its own memory, tools, and planning, while a multi-agent system routes the query through a coordinating agent that delegates to peers before converging on one answer.*

![Figure 8-3: An overview of agent roles within systems](images/fig_08-03_An_overview_of_agent_roles_within_system.png)

*Figure: homogeneous agents (identical GitHub agents for parallel work), heterogeneous agents (GitHub, Search, Slack specialists with predefined roles), and emergent agents that start generic and evolve specializations through interaction.*

Benefits: collaboration, scalability, speed. Costs: orchestration complexity, compute, and evaluation difficulty multiplied across agents.

## Orchestrating Agents

MASs already ship: Anthropic built a research system from multiple Claude agents, Uber runs a supervisor plus data-retrieval agents (including SQL) for real-time financial intelligence, and Delivery Hero extracts entities and product titles for its knowledge base.

## Patterns

Patterns are topology — roles, and above all communication. Centralized is most common for its ease, but collapses with its orchestrator. Decentralized is most stable and scales by adding agents, at the price of heavy communication. Hierarchical mirrors org charts, allocating resources efficiently but communicating most. Federated spans organizations communicating indirectly to protect data privacy, where shared standards exist.

![Figure 8-4: Four different patterns of agent orchestration](images/fig_08-04_Four_different_patterns_of_agent_orchest.png)

*Figure: the four topologies drawn side by side — centralized hub, decentralized mesh, hierarchical tree, and federated clusters exchanging only summaries across a privacy boundary.*

A framework-free trick builds a centralized MAS: treat subagents as tools. Math and date `TinyAgent` specialists get wrapped in plain functions registered as the orchestrator's tools. Asked about saving €4/day until 2030, the orchestrator calls the date agent (1691 days) then the math agent (€6,764) — useful when hundreds of tools would swamp one agent.

## General-Purpose Frameworks for Collaborative Task-Solving Patterns

CAMEL is role-play based: a user idea, an AI user (instructor) and AI assistant (executor), a task specifier agent enriching the query given those roles, then dialogue until the AI user ends it. MetaGPT scales role-play to whole organizations via role profiles following a software-development SOP, a protocol passing structured artifacts instead of dialogue, and iterative programming with executable feedback. Production frameworks — AutoGen, LangGraph, CrewAI — emphasize modularity.

![Figure 8-7: A pipeline of agents working together in MetaGPT](images/fig_08-07_A_pipeline_of_agents_working_together_in.png)

*Figure: a user request flows to a project manager agent emitting a PRD, an architect agent emitting a sequence flow diagram, and a profiled engineer agent writing the codebase.*

## Agent Society

Agents sharing an environment without assigned tasks begin forming agentic societies — simulations where sociality, identity, and potentially theory of mind emerge, starting from emotional intelligence: LLMs take on identities through character profiles.

![Figure 8-11: The steps in A2A between the client agent and remote agent](images/fig_08-11_The_steps_in_A2A_between_the_client_agen.png)

*Figure: A2A in four phases — discovery via `GET /.well-known/agent.json` returning an agent card, authentication (e.g. OAuth2.0), a JSON task message, and execution returning a completed status with content.*
