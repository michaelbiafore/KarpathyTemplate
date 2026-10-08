# Augmenting the LLM through the TinyAgent (Chapters 18–25)

## Augmenting the Large Language Model

A reasoning LLM alone is incomplete: a stateless text-to-text function with no grip on its environment and no recall. **Memory** turns single-turn answering machines into multi-turn participants — simplest by replaying history into the prompt. Because too much context causes information overload, the discipline is **context engineering**: balancing quantity against quality. **Tools** let the model act, but an LLM only *expresses* intent — asked "What is 5.1 times 7.3?" it emits `multiply(5.1, 7.3)`, and surrounding software must parse and execute it (standardized in Ch5 via the Model Context Protocol). Memory plus tools give Anthropic's **augmented LLM**.

![Figure 1-14: Augmenting a reasoning LLM with memory and tools: the “augmented](images/fig_01-14_Augmenting_a_reasoning_LLM_with_memory_a.png)

*Figure: A reasoning LLM with Memory and Tools attached takes a query, acts on the environment, consumes feedback, answers.*

The last ingredient is **planning and reflection**: decompose into a plan, execute stepwise, then revise — adding Semantic Scholar and PubMed when Google and arXiv prove insufficient.

## An Agentic System

Autonomy is a spectrum. Guardrails restrict destructive actions; goal-directed decision-making qualifies as agency even inside orchestrated workflows.

![Figure 1-19: AI agents have more autonomy or agency than a single LLM generation or](images/fig_01-19_AI_agents_have_more_autonomy_or_agency_t.png)

*Figure: Three rungs — plain prompting, a fixed-step pipeline, and an agent that plans, acts, and updates its own plan.*

Agents shine where the goal is clear but the path is not: **coding**, **deep research**, **automation**. Responsible use demands human-in-the-loop checks, guardrails, and hallucination vigilance. Evaluation needs two lenses — **outcome** (did it get done?) and **trajectory** (were the steps sound?) — plus **reliability** and **safety**. You evaluate a system, not a model.

## Specializations

![Figure 1-20: Part I covers the major components of a single AI agent](images/fig_01-20_Part_I_covers_the_major_components_of_a.png)

*Figure: The Part I map — Ch2 LLMs through Ch7 evaluation — pinned onto the single-agent diagram.*

## Multi-Agent Collaboration

Specialized workloads push toward multiple agents with distinct toolsets. A **supervisor agent** — usually the most capable LLM, since it plans, decomposes, and assigns — is the common pattern among dozens of orchestrations.

![Figure 1-23: One way to design multi-agent collaboration is with a capable supervisor](images/fig_01-23_One_way_to_design_multi-agent_collaborat.png)

*Figure: A supervisor treats coding, messaging, and search sub-agents as tools, each wrapping its own agent-specific toolset.*

## The Multi-Modal Agent

An agent is multi-modal if its brain is. **Understanding** needs an encoder to vectorize images/audio/video and a connector to map those into the LLM; **generating** other modalities needs a separate generator.

![Figure 1-24: AI agents can have better representation of their environments if they can](images/fig_01-24_AI_agents_can_have_better_representation.png)

*Figure: Encoder plus connector feed image, audio, and video embeddings into the LLM alongside the text question.*

## The Coding Agent

A coding agent runs programs in a dedicated environment — reading codebases, writing functions, fixing bugs, testing its own output — the basis of "vibe coding." Chapter 10; SWE-bench in Chapter 7.

## The TinyAgent

You build a **TinyAgent** in Python with minimal dependencies. The surrounding code is the **harness**, in five families: terminal (Claude Code, Codex CLI), code-based (LangGraph, Pydantic AI), personal assistant (OpenClaw — 300,000 GitHub stars in months), hosted (Replit, Manus), UI-based (Cursor, Copilot). All share one scaffolding.

![Figure 1-27: A sneak peek into the different modules that we’re going to explore and](images/fig_01-27_A_sneak_peek_into_the_different_modules.png)

*Figure: The TinyAgent class and the modules bolted on chapter by chapter — LLM, Trajectory, Memory, Tools, MCP, ReAct, Display.*

Chapter 1 ships only the skeleton: `llm`, `memory`, `tools`, `planner` slots set to `None`, with `run`/`_step`/`_execute_action` stubs that echo input.

## Summary

Part I builds the single agent: brain, memory, tools, planning, autonomy, evaluation. Part II covers specializations. Chapters 2 and 3 take up the brain itself.
