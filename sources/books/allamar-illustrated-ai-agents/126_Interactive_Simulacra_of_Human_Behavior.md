---
title: "Interactive Simulacra of Human Behavior"
chapter_number: 126
page_start: 336
page_end: 340
part: "Part II. Specialized Agents"
---
# Interactive Simulacra of Human Behavior

accurate enough, it might serve as a representation to understand the mechanism of
the world it simulates. These simulations are then referred to as world models.18 The
simulations can be viewed from the perspective of world models, but in the context of
MASs, serve as a way to explore the behavior of agents in social situations.
Interactive Simulacra of Human Behavior
One of the most influential papers on MAS in social simulations is “Generative
Agents: Interactive Simulacra of Human Behavior,” which discusses agents that were
put in a pixel-sandbox environment to plan their days, go to group activities, and
form relationships.19 The simulation takes place in Smallville, which simulates a
small-town environment, as shown in Figure 8-12 (adapted from the paper).



![Figure 8-12: A figure of Smallville, the simulated town used in the paper: “Generative](images/fig_08-12_A_figure_of_Smallville_the_simulated_tow.png)

*Figure 8-12: A figure of Smallville, the simulated town used in the paper: “Generative*


Figure 8-12. A figure of Smallville, the simulated town used in the paper: “Generative
Agents: Interactive Simulacra of Human Behavior”
Each agent in the environment was given a distinct profile to make them behave
in unique ways and enforce more interesting and dynamic behavior. Figure 8-13
18 Ding, Jingtao et al. 2025. “Understanding World or Predicting Future? A Comprehensive Survey of World
Models,” ACM Computing Surveys, 58.3: 1-38.
19 Park, Joon Sung et al. 2023. “Generative Agents: Interactive Simulacra of Human Behavior,” Proceedings of the
36th Annual ACM Symposium on User Interface Software and Technology.
|
Chapter 8: Multi-Agent Systems

illustrates such a profile (including the current state) for one of the agents in this
simulation, namely Isabella Rodriguez, the owner of Hobbs Cafe.



![Figure 8-13: The profile of one of the inhabitants of Smallville, namely Isabella](images/fig_08-13_The_profile_of_one_of_the_inhabitants_of.png)

*Figure 8-13: The profile of one of the inhabitants of Smallville, namely Isabella*


Figure 8-13. The profile of one of the inhabitants of Smallville, namely Isabella
The authors created 25 unique agents that were each initialized with one paragraph
describing their identity, occupation, relationships, etc. Each agent was also initialized
with three modules, namely memory, planning, and reflection, much like the core
components in ReAct and Reflexion that we discussed extensively in Chapter 6.
The memory component is vital in tracking not only the states of the entire environ‐
ment but also the behavior of the agent itself and the ones it interacts with. Although
summarization would help reduce information overload, it would still require sum‐
marizing potentially non-relevant information. Instead, the memory stream module
the authors introduced balances three attributes, namely the recency, importance, and
relevance of a given state (memory). The relevance is calculated through the cosine
similarity between a question and a state, where each state is embedded. A state is a
current situation, where each is tracked like so:
"""
2023-02-13 22:48:20: desk is idle
2023-02-13 22:48:20: bed is idle
2023-02-13 22:48:10: closet is idle
2023-02-13 22:48:10: refrigerator is idle
2023-02-13 22:48:10: Isabella Rodriguez is stretching
2023-02-13 22:33:30: shelf is idle
2023-02-13 22:33:30: desk is neat and organized
2023-02-13 22:33:10: Isabella Rodriguez is writing in her journal
2023-02-13 22:18:10: desk is idle
2023-02-13 22:18:10: Isabella Rodriguez is taking a break
2023-02-13 21:49:00: bed is idle
2023-02-13 21:48:50: Isabella Rodriguez is cleaning up the kitchen
2023-02-13 21:48:50: refrigerator is idle
2023-02-13 21:48:50: bed is being used
2023-02-13 21:48:10: shelf is idle
2023-02-13 21:48:10: Isabella Rodriguez is watching a movie
2023-02-13 21:19:10: shelf is organized and tidy
2023-02-13 21:18:10: desk is idle
2023-02-13 21:18:10: Isabella Rodriguez is reading a book
Agent Society
|

2023-02-13 21:03:40: bed is idle
2023-02-13 21:03:30: refrigerator is idle
2023-02-13 21:03:30: desk is in use with a laptop and some papers on it
...
"""
The recency is simply a higher score given to more recent states. Lastly, the impor‐
tance is judged by another LLM, essentially asking how important the state is to the
agent, and might evoke strong emotions.
As shown in Figure 8-14, this RAG-like solution distills a large number of states into
a select few that are relevant to the agent’s current situation.



![Figure 8-14: The procedure of MemoryStream for giving memory to the inhabitants of](images/fig_08-14_The_procedure_of_MemoryStream_for_giving.png)

*Figure 8-14: The procedure of MemoryStream for giving memory to the inhabitants of*


Figure 8-14. The procedure of MemoryStream for giving memory to the inhabitants of
Smallville
Reflection is added as a second type of memory where agents are instructed to
periodically reflect on the latest events that happen roughly two or three times a
day. During a reflection, the 100 most recent states are retrieved and used to prompt
an LLM to extract the three most salient high-level questions. For instance, “What
topic is Isabella Rodriguez passionate about?” These questions are used to retrieve the
most relevant states, which are used to answer these questions through five insights.
Finally, their reflections are put back into the memory stream to potentially reflect
on. This memory system is shown in Figure 8-15.
|
Chapter 8: Multi-Agent Systems



![Figure 8-15: Reflection is an additional component to MemoryStream to give inhabi‐](images/fig_08-15_Reflection_is_an_additional_component_to.png)

*Figure 8-15: Reflection is an additional component to MemoryStream to give inhabi‐*


Figure 8-15. Reflection is an additional component to MemoryStream to give inhabi‐
tants more lifelike behavior
Agents create and continuously update plans that include a location, starting time,
and duration of the action to take. These plans are stored in the memory stream for
retrieval, much like the reflections. As such, agents consider observations from the
environment, reflections, and plans when deciding their next actions.
The agents use a ReAct-like schema to continuously execute actions and process their
environments. The plans are updated based on the observations if the observation
is of importance. Using a summary of the current context, the agent’s LLM is then
asked: “Should you react to the observation, and if so, what would be an appropriate
reaction?”
These components create the agent framework, as shown in Figure 8-16.
Agent Society
|



![Figure 8-16: The core agentic framework of inhabitants in Smallville](images/fig_08-16_The_core_agentic_framework_of_inhabitant.png)

*Figure 8-16: The core agentic framework of inhabitants in Smallville*


Figure 8-16. The core agentic framework of inhabitants in Smallville
Agents may interact with each other through dialogue, which can result in spontane‐
ous interactions based on their memory of the agents they interact with. Moreover,
they may converse about specific topics of interest, as shown in Figure 8-17 (which
was annotated from the interactive demo).



![Figure 8-17: Different types of behaviors that might appear in Smallville](images/fig_08-17_Different_types_of_behaviors_that_might.png)

*Figure 8-17: Different types of behaviors that might appear in Smallville*


Figure 8-17. Different types of behaviors that might appear in Smallville
|
Chapter 8: Multi-Agent Systems