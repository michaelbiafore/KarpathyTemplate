---
title: "Agent Laboratory"
chapter_number: 129
page_start: 343
page_end: 346
part: "Part II. Specialized Agents"
---
# Agent Laboratory

The Generation agent starts with a first draft of research hypotheses, which are then
reviewed by the Reflection agent and ranked in the tournament by the Ranking agent.
The best hypotheses are fed to the Proximity, Evolution, and Meta-review agents to
improve the quality of hypotheses and update the current state of information.
All information is stored in the context memory, which contains information about
the generated hypotheses, the outputs of each agent, and their current state. Based on
this information, the supervisor agent may then orchestrate the specialized agents by
choosing which to run when. The interactions between the user, the supervisor agent,
and the specialized agents are illustrated in Figure 8-18.



![Figure 8-18: The AI co-scientist uses specialized agents to perform its research](images/fig_08-18_The_AI_co-scientist_uses_specialized_age.png)

*Figure 8-18: The AI co-scientist uses specialized agents to perform its research*


Figure 8-18. The AI co-scientist uses specialized agents to perform its research
What makes this framework particularly useful is that the user can guide the system
while it’s computing and creating hypotheses. That way, the scientist can interact
with the AI co-scientist and provide manual reviews of the generated hypotheses
and evaluate proposals. The scientist can likewise prompt the system to follow up
on specific proposals or prioritize specific fields. It’s the type of system that, instead
of attempting to replace people, empowers them through a collaboration between
human and machine.
Agent Laboratory
A similar, but more static system than the AI co-scientist is Agent Laboratory, a
framework that takes a more structured approach by pre-defining the stages of its
Deep Research Agents
|

MAS, namely, literature review, experimentation, and report writing.24 Like the AI
co-scientist, the Agent Laboratory is driven by the human researcher but also reduces
time-intensive tasks like coding and documentation.
The main goal of the Agent Laboratory is to create a research report along with
the code needed for running the experiments. To do so, it follows three distinctive
phases.
In phase 1, literature review, relevant research papers are curated based on the user’s
research idea. In this phase, a PhD student agent (initialized with GPT-4o) uses
the arXiv API to retrieve the related papers. This agent can summarize relevant
papers, extract the full content of papers, and add selected summaries for its curated
review. As shown in Figure 8-19, this is an iterative process as the PhD student
agent continuously refines its query to the API. It stops iteration when a pre-defined
number of relevant papers is reached. The literature review is therefore a selection of
paper summaries.



![Figure 8-19: Phase 1 of the Agent Laboratory](images/fig_08-19_Phase_1_of_the_Agent_Laboratory.png)

*Figure 8-19: Phase 1 of the Agent Laboratory*


Figure 8-19. Phase 1 of the Agent Laboratory
In phase 2, experimentation, the previously generated literature review is used across
the following three distinct stages:
Plan formulation
A PhD student agent collaborates with a postdoc agent to generate a research
objective, including experimental steps needed. The output is a plan detailing the
steps needed for experimentation.
24 Schmidgall, Samuel et al. 2025. “Agent laboratory: Using LLM Agents as Research Assistants,” arXiv,
2501. 04227.
|
Chapter 8: Multi-Agent Systems

Data preparation
A machine learning engineer agent has access to the HuggingFace datasets
library and searches for the best datasets for the experiment. The software engi‐
neer agent then submits the code and checks for any bugs.
Running experiments
The machine learning engineer agent attempts to implement the experimental
plan in code. A specialized module, the mle-solver, is used to autonomously
generate the code. This is essentially an advanced coding agent (see Chapter 10
for more information on coding agents).
After these steps, the experimental plan has been created, and the experiments have
been executed, as shown in Figure 8-20.



![Figure 8-20: Phase 2 of the Agent Laboratory](images/fig_08-20_Phase_2_of_the_Agent_Laboratory.png)

*Figure 8-20: Phase 2 of the Agent Laboratory*


Figure 8-20. Phase 2 of the Agent Laboratory
In phase 3, report writing, the results from phase 2 are used to write a report, which is
split up into two steps:
Report writing
The PhD student agent and the professor agent collaborate to convert the
research findings into an academic report. This is a highly collaborative step
because frequent reviews take place, both by the professor agent and additional
arXiv research.
Report refinement
Three reviewer agents (based on NeurIPS peer reviewers) evaluate the draft
report on originality, quality, clarity, and significance. The PhD agent then
decides whether feedback needs to be addressed or if it’s complete.
Deep Research Agents
|

These steps allow the agents to continuously improve the research report until all
agents agree that it is of sufficient quality, as shown in Figure 8-21.



![Figure 8-21: Phase 3 of the Agent Laboratory](images/fig_08-21_Phase_3_of_the_Agent_Laboratory.png)

*Figure 8-21: Phase 3 of the Agent Laboratory*


Figure 8-21. Phase 3 of the Agent Laboratory
The three phases (literature review, experimentation, and report writing) mimic a
real-world academic exploration and revision process. An interesting feature of Agent
Laboratory is that there are larger degrees of freedom for the agents to behave
autonomously within each step, but the order of steps is still fixed. On the overall
architecture of the system, there is no autonomy because it’s a fixed pattern. However,
within each step, the agents iterate until they are satisfied with the completed results
and can act with a high degree of autonomy. This full system is shown in Figure 8-22.



![Figure 8-22: All phases of the Agent Laboratory](images/fig_08-22_All_phases_of_the_Agent_Laboratory.png)

*Figure 8-22: All phases of the Agent Laboratory*


Figure 8-22. All phases of the Agent Laboratory
|
Chapter 8: Multi-Agent Systems