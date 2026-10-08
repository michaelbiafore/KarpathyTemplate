---
title: "Patterns"
chapter_number: 120
page_start: 317
page_end: 322
part: "Part II. Specialized Agents"
---
# Patterns

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

Hierarchical
Each agent is structured into a layered system where each level has a different
degree of authority, and agents have distinct roles.
Federated
Agents are distributed among parallel environments (organizations) that only
communicate indirectly to safeguard the privacy of data. Each agent adheres to
different regulations but can still communicate the results with other agents.
These types are visualized in Figure 8-4.



![Figure 8-4: Four different patterns of agent orchestration](images/fig_08-04_Four_different_patterns_of_agent_orchest.png)

*Figure 8-4: Four different patterns of agent orchestration*


Figure 8-4. Four different patterns of agent orchestration
|
Chapter 8: Multi-Agent Systems

In practice, a centralized MAS is most often used due to its ease of implementation
and management compared to the other patterns. A downside of this approach is that
the entire system might collapse if the orchestration agent fails.
A decentralized MAS has the benefit of being more stable than the other patterns.
Even if some agents fail, the system can continue working as each agent has similar
responsibilities and capabilities. As such, scaling only requires adding agents. How‐
ever, it requires many capable agents and significant communication overhead, which
all require extensive resources.
The hierarchical MAS is similar to how traditional organizations operate and is
therefore an intuitive pattern to use. By distributing tasks across levels and having
many specialized roles, resource allocation can be made efficient. However, it’s still a
complex system that requires the most communication.
Lastly, a federated MAS is a relatively new pattern and is used when agents need
to be distributed among different organizations. Although this pattern encourages
cross-system collaboration, it relies on shared standards that might not always be in
place.
Creating MASs can quickly require significant code to manage all agents. There
have been many different frameworks that handle the complexity of managing and
creating agents. Before we explore various general-purpose frameworks, let’s create a
simple version of a centralized MAS to showcase the fundamentals and intricacies of
having and building MASs.
An interesting trick that we can use to create a centralized and potentially hierarchical
system is by viewing subagents not as agents but as tools to use. To illustrate, let’s first
create a specialized subagent:
```
from illustrated_agents.chapters.ch2 import LLM
from illustrated_agents.chapters.ch4 import Memory
from illustrated_agents.chapters.ch5 import NativeTools
from illustrated_agents.chapters.ch6 import NativeReAct, TinyAgent
from illustrated_agents.toolbox import add, subtract, multiply
```

# Gemma 4 E4B (with native thinking and tool calling)
llm = LLM(model="gemma4:e4b", think=True)

# Math specialist
math_tools = NativeTools()
math_tools.add_tool("add", add)
math_tools.add_tool("subtract", subtract)
math_tools.add_tool("multiply", multiply)

# Math Agent
math_agent = TinyAgent(
 llm=llm,
 tools=math_tools,
Orchestrating Agents
|

memory=Memory(),
 planner=NativeReAct()
)
This agent “specializes” in using basic mathematical tools, such as adding, subtract‐
ing, and multiplying values, as we have seen often throughout this book.
To make the example a bit more comprehensive, let’s add another subagent. This
agent will have access to tools related to date handling:
import datetime

def today() -> str:
 """Return today's date (YYYY-MM-DD)."""
 return datetime.date.today().isoformat()

def days_between(a: str, b: str) -> int:
 """Days between two ISO dates."""
 return (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days

# Date specialist
date_tools = NativeTools()
date_tools.add_tool("today", today)
date_tools.add_tool("days_between", days_between)

# Date Agent
date_agent = TinyAgent(
 llm=llm,
 tools=date_tools,
 memory=Memory(),
 planner=NativeReAct()
)
To have the orchestrator be able to use and direct these subagents, we can leverage
them in an elegant way, namely as tools. Instead of having to devise a complex
harness, framework, or system, we wrap these subagents in Python functions for the
orchestrator to use:
def ask_math_agent(question: str) -> str:
 """Delegate to the math specialist."""
 return math_agent.run(question)

def ask_date_agent(question: str) -> str:
 """Ask queries to a sub-agent that handles ISO dates."""
 return date_agent.run(question)
|
Chapter 8: Multi-Agent Systems

Now, we can feed the two “tools” (which are actually subagents) to the orchestrator:
# Tools - Add the Math Agent and Date Agent as tools!
tools = NativeTools()
tools.add_tool("ask_math_agent", ask_math_agent)
tools.add_tool("ask_date_agent", ask_date_agent)

# Orchestrator Agent
orchestrator_agent = TinyAgent(
 llm=llm,
 tools=tools,
 memory=Memory(),
 planner=NativeReAct()
)
This creates a simple hierarchy. We can ask the orchestrator a question, and it can
decide whether to ask for help from one of the subagents. To illustrate, let’s ask the
orchestrator a question that requires the help of both subagents:
orchestrator_agent.run("If I save €4 per day until 2030, how much will I have?")
Which gives:
'If you save €4 per day until the end of 2030, you will have **€6,764**.'
Note that you will get a different answer because this answer was generated back in
May 2026.
As always, to understand what really happened, we would need to inspect the mem‐
ory and trajectory of the agent. However, we now have three agents to explore. We
start with the orchestrator and focus on its actions, observations, and final answer:
for index, step in enumerate(orchestrator_agent.trajectory.runs[0]["steps"]):
 print(f"-- Step {index+1} ---")
 if step.action:
 print(f"Tool: {step.action}")
 print(f"Observation: {step.observation}\n")
 else:
 print(f"Answer: {step.answer}\n")
This gives the following output:
- - Step 1 ---
Tool: {'tool': 'ask_date_agent', 'kwargs': {'question': 'How many days from
today until the end of 2030?'}}
Observation: There are **1691** days from today (May 15, 2026) until the end
of 2030 (December 31, 2030).

- - Step 2 ---
Tool: {'tool': 'ask_math_agent', 'kwargs': {'question': '€4 times 1691'}}
Observation: €6764

- - Step 3 ---
Answer: If you save €4 per day until the end of 2030, you will have **€6,764**.
Orchestrating Agents
|

Note that the orchestrator decided to call the date subagent to get the number of
days before calling the math subagent to perform the calculation. This idea of having
subagents and an orchestrator to manage them is particularly useful when you have
dozens and perhaps hundreds of tools that can be used. The orchestrator is likely
to make mistakes, having to sift through so many tools, and can instead dedicate a
subset of those tools to a subagent.
Note, though, that looking only at the trajectory of the orchestrator gives an abstract
overview of what has happened. We didn’t see what actions the subagents took and
whether that seemed like an efficient route. Let’s inspect one of the subagents:
for index, step in enumerate(date_agent.trajectory.runs[0]["steps"]):
 print(f"-- Step {index+1} ---")
 if step.action:
 print(f"Tool: {step.action}")
 print(f"Observation: {step.observation}\n")
 else:
 print(f"Answer: {step.answer}\n")
Which gives the following output:
- - Step 1 ---
Tool: {'tool': 'today', 'kwargs': {}}
Observation: 2026-05-15

- - Step 2 ---
Tool: {'tool': 'days_between', 'kwargs': {'a': '2026-05-15', 'b': '2030-12-31'}}
Observation: 1691

- - Step 3 ---
Answer: There are **1691** days from today (May 15, 2026) until the end of 2030
(December 31, 2030).
The subagent first needed to figure out what the current date was before calculating
the number of days between now and the end of 2030. By inspecting the trajectories
of even the subagents, you can see how well optimized they were for given tasks.
Although this was a minimal example of a MAS, the complexities of such systems can
grow quickly. As such, now that we have covered a basic technique for implementing
subagents, let’s explore how general-purpose frameworks approach this problem.
|
Chapter 8: Multi-Agent Systems