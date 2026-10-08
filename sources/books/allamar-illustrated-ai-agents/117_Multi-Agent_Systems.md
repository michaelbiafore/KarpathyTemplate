---
title: "Chapter 8. Multi-Agent Systems"
chapter_number: 117
page_start: 313
page_end: 313
part: "Part II. Specialized Agents"
---
# Chapter 8. Multi-Agent Systems

Multi-Agent Systems
Thus far, we have discussed the agent in isolation. A single entity that autonomously
creates plans, executes them, and reflects on these processes. These single-agent
systems are solely responsible for achieving the initial goal without interaction with
intelligent systems other than humans. As powerful as these entities can become by
themselves, a system where multiple agents work together to reach a common goal
has even more potential. This is the multi-agent system (MAS), which may feature
one or more environments in which many agents, some differently than others, can
interact with each other.
Each agent in such a system will have a level of autonomy, but may have different sets
of tools, (sub)goals, or even personalities. Regardless of their potential differences,
these agents will need to collaborate to reach common goals through their own
skill sets. Multi-agent systems are quite adept at handling intricate tasks that require
balancing multiple complex dependencies.
Imagine you are creating an agentic research system that helps you with exploring
a topic of choice. A single agent would have to juggle between many different tasks,
such as searching the web, processing papers and figures, reading and critiquing
the papers, and finally summarizing the findings. Each of these tasks could also be
handled by a different agent specialized in that task. As a result, you would get a
system with a search agent, processing agent, paper agent, summarization agent, etc.
In this chapter, we’ll explore how to organize multi-agent systems and allow for vari‐
ous types of communication in these systems. We cover general-purpose frameworks
for building multi-agents and how these entities interact in social simulations.