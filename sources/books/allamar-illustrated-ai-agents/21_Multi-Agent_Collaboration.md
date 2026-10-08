---
title: "Multi-Agent Collaboration"
chapter_number: 21
page_start: 41
page_end: 41
part: "Part I. The Anatomy of an AI Agent"
---
# Multi-Agent Collaboration

Multi-Agent Collaboration
When systems grow larger and tasks are more specialized, we start looking toward
multi-agent collaborations. These are systems where multiple different agents are
deployed that are each responsible for different tasks. Compared to single-agent sys‐
tems, multi-agent systems interact with one another and might consult each other’s
specialties. The main differences lie in how many agents are deployed and their
interactions with one another (Figure 1-22).



![Figure 1-22: Multiple agents can collaborate to solve certain tasks and could achieve](images/fig_01-22_Multiple_agents_can_collaborate_to_solve.png)

*Figure 1-22: Multiple agents can collaborate to solve certain tasks and could achieve*


Figure 1-22. Multiple agents can collaborate to solve certain tasks and could achieve
better results than those possible by a single agent
These multi-agent systems often contain specialized agents, each equipped with dif‐
ferent toolsets. Although workflows may differ, there is often a supervisor agent
that manages communication among, and sometimes within, agents. In practice, the
supervisor agent tends to have the most capable LLM because the supervisor is in
charge of advanced behavior such as planning, decomposing, and assigning tasks
(Figure 1-23).
Although the supervisor agent is common, this does not always have to be the case.
In practice, there are dozens of multi-agent architectures to explore, some with struc‐
tured orchestration (like the supervisor) and some with unstructured orchestration.
Specializations
|