---
title: "Long-Term Memory"
chapter_number: 62
page_start: 165
page_end: 165
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Long-Term Memory

Note how there is only a system role with a summary of the conversation history. As
you continue the conversation, this summary gets updated. As always, if you want to
track the full conversation, you can use the TrajectoryViewer:
from illustrated_agents.utils import TrajectoryViewer
TrajectoryViewer(agent.trajectory)
Although this implementation may seem straightforward, maintaining the conversa‐
tion history can be a difficult task and requires understanding what is important: the
entire history, the recent history, or a summarized variant? For short conversations,
maintaining the entire history would work, but that might not be the case for long
sequences of actions. In Chapter 10, we will touch on customizing this summariza‐
tion process for a specific domain like code generation.
Long-Term Memory
As the conversation history and the number of actions that an agent has taken grows,
so does the need for long-term memory. However, its usefulness is not limited to
conversation history but may also include proprietary or external knowledge. Long-
term memory typically involves maintaining one or more external databases that can
be queried to extract additional information. This can contain information about
previous traces or states of the agent (episodic memory) or information unrelated
to the agent’s behavior but about the context of your application instead (semantic
memory), like your organization’s documents.
Retrieval-Augmented Generation
Arguably, the most common method for giving your agent, or any LLM for that mat‐
ter, long-term memory is Retrieval-Augmented Generation (RAG).4 RAG typically
consists of two stages: ingestion and inference.
In ingestion, your external data, typically unstructured text, is embedded into numer‐
ical representations and stored in a database (Figure 4-14). To create these representa‐
tions, a special variant of an LLM is used, an embedding model, which converts text
into numerical vectors (also called embeddings) that capture the semantic meaning of
the input. This embedding model is trained to create numerical representations such
that words and phrases with similar meaning will have similar representations. This
external database can be considered the long-term memory of the LLM, which can be
queried for relevant information.
4 Lewis, Patrick et al. 2020. “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,” NIPS’20:
Proceedings of the 34th International Conference on Neural Information Processing Systems, 9459-9474.
Long-Term Memory
|