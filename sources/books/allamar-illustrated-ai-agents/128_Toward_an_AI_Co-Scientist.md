---
title: "Toward an AI Co-Scientist"
chapter_number: 128
page_start: 342
page_end: 342
part: "Part II. Specialized Agents"
---
# Toward an AI Co-Scientist

Toward an AI Co-Scientist
Deep Research can be more than asking it to summarize the current state of RL.
Although incredibly valuable, such systems might also help in uncovering new
insights. In February 2025, such a system was released, aiming to assist in the
scientific discovery process and uncover new and original knowledge; it’s called
the AI co-scientist.23 This multi-agent Deep Research system, built on Gemini 2.0,
takes inspiration from the scientific method and incorporates a thorough hypothesis
generation.
The main goal of this system is to generate hypotheses and a research proposal given
a research goal. The authors define several criteria that should be adhered to during
this process, such as plausibility, novelty, testability, and safety. However, due to the
general nature of the framework, the criteria can be adjusted to the user’s preference.
The framework works as follows. First, the user specifies a research goal, along with
relevant documents, and provides that as input to the AI co-scientist to parse and
derive a research plan through a supervisor agent. This supervisor agent is responsi‐
ble for the orchestration of specialized agents:
Generation agent
Initiates the research by generating preliminary focus areas through literature
research using search tools
Reflection agent
Reviews the correctness, quality, and explanatory power of the generated hypoth‐
eses
Ranking agent
Ranks generated hypotheses based on Elo-style tournaments through scientific
debates
Proximity agent
Identifies which hypotheses are similar to each other so they can be grouped,
cleaned of duplicates, and explored more efficiently
Evolution agent
Continuously refines the highest-scoring hypotheses using methodologies such
as leveraging literature for supporting details and exploring unconventional rea‐
soning
Meta-review agent
Combines insights from all reviews and debates to improve how the system
works over time
23 Gottweis, Juraj et al. 2025. “Towards an AI Co-Scientist,” arXiv, 2502.18864.
|
Chapter 8: Multi-Agent Systems