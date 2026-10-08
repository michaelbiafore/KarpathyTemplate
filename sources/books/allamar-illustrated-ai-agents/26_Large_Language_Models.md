---
title: "Chapter 2. Large Language Models"
chapter_number: 26
page_start: 51
page_end: 52
part: "Part I. The Anatomy of an AI Agent"
---
# Chapter 2. Large Language Models

Large Language Models
As we saw in Chapter 1, the LLM powers agents to go from observations to actions.
In Figure 2-1, we can see this general workflow. Here, we color-code the areas where
the agent interacts with the user (on the left) and where the agent interacts with the
environment (on the right).



![Figure 2-1: The agent acts as a bridge between user and environment](images/fig_02-01_The_agent_acts_as_a_bridge_between_user.png)

*Figure 2-1: The agent acts as a bridge between user and environment*


Figure 2-1. The agent acts as a bridge between user and environment
Let’s take a simple example to unroll the loop we see in the figure. The example is a
simple information-seeking agent trying to answer a question for a user using a web
search tool.
In Figure 2-2, we can see that interaction:
1. The user asks the agent a question.
1.
2. The agent uses a web search tool, effectively pulling in information from the
2.
environment.
3. The retrieved information is presented to the agent, which decides that it now
3.
has enough information to answer the user’s question.

4. The agent prints out its answer to the user.
4.



![Figure 2-2: The agent receives a user’s question (left), calls a web search tool to retrieve](images/fig_02-02_The_agent_receives_a_users_question_left.png)

*Figure 2-2: The agent receives a user’s question (left), calls a web search tool to retrieve*


Figure 2-2. The agent receives a user’s question (left), calls a web search tool to retrieve
information from the environment, then uses the retrieved information to generate and
return an answer (right)
In LLM-backed agents, the LLM is tasked with processing the user query, choosing
the right action, processing the feedback or observation resulting from the action,
and communicating back to the user.
In this chapter, you’ll learn how LLMs work and how they’re created. We’ve struc‐
tured the chapter in two parts with intentionally different audiences in mind.
Part 1 offers a high-level overview of LLMs aimed at agent developers: the core
intuitions, capabilities, and limitations you need to build and reason about agent
systems—without requiring a deep understanding of the underlying machinery.
Part 2 takes a significantly deeper dive into model internals and training techniques.
This section assumes more comfort with machine learning concepts and is intended
for readers who want to understand why LLMs behave the way they do, not just
how to use them. This understanding can be valuable when diagnosing agent failures,
selecting models, or pushing the boundaries of what agents can do.
If you’re primarily focused on building agents, feel free to proceed to the next chapter
after reading Part 1—you’ll have everything you need. You can return to Part 2 when
you’re ready to go deeper.
|
Chapter 2: Large Language Models