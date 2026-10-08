---
title: "Agentic Retrieval-Augmented Generation"
chapter_number: 64
page_start: 174
page_end: 180
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Agentic Retrieval-Augmented Generation

Agentic Retrieval-Augmented Generation
In vanilla RAG, the vector database can be considered the long-term memory of the
LLM. However, the LLM is only given information that is relevant to the query and
has no agency over what is being retrieved.
In agentic RAG, there is an agent instead of an LLM that can access the external
database as a tool and have control over which information it retrieves. Agency over
what is being retrieved is given back to the agent, who typically has access to one
or more external databases of information. Figure 4-19 illustrates this idea of having
the agent select from which source to retrieve contextual information before deciding
whether to generate the answer or to again retrieve additional information.



![Figure 4-19: Agentic RAG](images/fig_04-19_Agentic_RAG.png)

*Figure 4-19: Agentic RAG*


Figure 4-19. Agentic RAG
In single-agent systems, agentic RAG is a router where you have several external
knowledge sources, and the agent decides which one(s) to use. You’re essentially
adding all these knowledge sources and databases as tools instead of being a static
step that runs before the LLM generates output. Moreover, such an agentic RAG
system does not always have to run the agentic RAG based on the query itself. As
shown in Figure 4-20, it may decide to extract information from one search and then
run a subsequent search based on that information in another database.



![Figure 4-20: Agentic RAG using a single agent to control multiple processes](images/fig_04-20_Agentic_RAG_using_a_single_agent_to_cont.png)

*Figure 4-20: Agentic RAG using a single agent to control multiple processes*


Figure 4-20. Agentic RAG using a single agent to control multiple processes
|
Chapter 4: Memory

Agentic RAG does not limit itself to single-agent systems. In multi-agent RAG
systems, multiple agents have the capabilities to extract information from external
sources. Oftentimes, you have smaller retrieval agents that are being coordinated by a
single agent with more capabilities. These smaller retrieval agents are each specialized
in extracting specific information or working with specific knowledge sources (see
Figure 4-21). Note that it does not always have to be a vector database as an external
knowledge source; it can also be a web search or querying some API for information
(like your Slack or Gmail).



![Figure 4-21: Agentic RAG using multiple agents to control different processes](images/fig_04-21_Agentic_RAG_using_multiple_agents_to_con.png)

*Figure 4-21: Agentic RAG using multiple agents to control different processes*


Figure 4-21. Agentic RAG using multiple agents to control different processes
In other words, instead of querying the vector database through a static step only
once, by hooking it as a tool, the agent can dynamically decide how many times it
needs to query the semantic memory until it has enough context to answer a given
query. Note how we discussed LLMs in the context of RAG but agents in the context
of agentic RAG instead. It demonstrates the agency and autonomy in accessing their
respective RAG capabilities.
Using either a single or multiple agents comes with their own sets of advantages and
disadvantages, each requiring a thorough understanding of the use case in which
they’re employed. We advise to start with a single agent system as a good baseline and
to minimize complexity. In Table 4-1, an non-exhaustive list is given advantages and
disadvantages of these systems.
Long-Term Memory
|

Table 4-1. Pros and cons of RAG systems
Single-agent RAG
Multi-agent RAG
Advantages
Cost effective–Fewer API calls are needed.
Simpler system–Easier to debug due to fewer
dependencies.
Modularity–Specialized LLMs can be used and easily
replaced.
Higher accuracy ceiling–Agents can give each other
feedback and check for hallucinations.
Disadvantages Single point of failure–Errors may compound
Higher costs–Multiple agents need to be run in parallel,
which drives costs.
Complexity–Harder to check where errors may arise and
how they relate to the entire flow.
without external feedback.
Lower accuracy ceiling–The context window can
be overloaded with too many sources and
retrievals of information.
Let’s go over some examples of how these agentic RAG systems work through impact‐
ful papers and implementations in the field.
The implementation of agentic RAG is shown in the associated
notebooks in the GitHub repository. Since our current implemen‐
tation of your TinyAgent isn’t yet autonomous, the notebooks
where we’ll cover this principle are going to be shown in the
notebooks after we have covered Chapter 6. There, everything will
come together to make your agent have a degree of autonomy.



![Figure on page 17](images/fig_p017_x95.png)


Moreover, and as discussed previously, agentic RAG makes use of
tools that we will cover in depth in Chapter 5.
A-MEM
An interesting approach to agentic RAG is A-MEM, an agentic memory sys‐
tem derived from the note-taking method known as Zettelkasten.7 Zettelkasten
approaches note-taking as having three important components, namely atomicity,
hypertextual notes, and personalization.
Atomicity means that each Zettel (a note) should contain only one unit of knowledge,
referred to as an atom. This note could, for example, contain a brief description of
how memory works in agentic systems.
Then, hypertextual notes refer to the idea that all notes refer to each other and
may explain or expand on each other’s content. For instance, the previously created
note can be connected to another note that has some information about RAG.
Because both are memory systems, they’re likely to be related. The ideas of atomicity
and hypertextual notes are illustrated in Figure 4-22. Together, they may create an
interconnected web of notes and ideas and larger topics of interconnected notes
7 Xu, Wujiang et al. 2025. “A-Mem: Agentic Memory for LLM Agents,” arXiv, 2502.12110.
|
Chapter 4: Memory

demonstrating how these interconnect notes are personalized to one’s own sets of
ideas.



![Figure 4-22: In Zettel, each note has a single subject (atomicity) and may link to other](images/fig_04-22_In_Zettel_each_note_has_a_single_subject.png)

*Figure 4-22: In Zettel, each note has a single subject (atomicity) and may link to other*


Figure 4-22. In Zettel, each note has a single subject (atomicity) and may link to other
notes (hypertextual notes)
A-MEM uses this idea of note-taking to agentic memory by creating these intercon‐
nected notes. In the context of agents, each note contains the following information
and can be considered a piece of memory:
- The original interaction with the environment (i.e., one turn)
•
- The timestamp of the interaction
•
- LLM-generated keywords that capture key concepts
•
- LLM-generated tags to categorize the interaction
•
- LLM-generated contextual description
•
By focusing on a single unit, namely a single interaction, A-MEM adheres to the
principle of atomicity. Then, all pieces of information are embedded so that they
can be used to later easily retrieve related information (Figure 4-23). Note that all
information, except for the timestamp, is concatenated so that a single embedding
is created for the entire note/memory. However, the timestamp is still maintained as
metadata to query.
Long-Term Memory
|



![Figure 4-23: The atomicity of an A-MEM note, which contains a single turn that is](images/fig_04-23_The_atomicity_of_an_A-MEM_note_which_con.png)

*Figure 4-23: The atomicity of an A-MEM note, which contains a single turn that is*


Figure 4-23. The atomicity of an A-MEM note, which contains a single turn that is
embedded using an embedding model
Interestingly, the authors use this generated note embedding as one of the main IDs
of the note. To link this note to other memories, they run a similarity search between
this note’s embeddings and all other memories and extract the Top-K memories.
After doing so, the LLM is asked to decide which of these candidate memories should
be linked to the newly added memory.
After the memory is added and linked to other memories, the LLM is prompted to
update the LLM-generated tags, keywords, and description based on the newly added
memory. This results in an evolutionary approach where newly added memories are
linked to older memories, which are, in turn, updated to be in line with the newly
added memories. Figure 4-24 illustrates this ever-evolving database of notes in the
form of memories.



![Figure 4-24: The embeddings of each note in A-MEM are used in this RAG-like pipeline](images/fig_04-24_The_embeddings_of_each_note_in_A-MEM_are.png)

*Figure 4-24: The embeddings of each note in A-MEM are used in this RAG-like pipeline*


Figure 4-24. The embeddings of each note in A-MEM are used in this RAG-like pipeline
with steps to search, retrieve, update, and add notes
|
Chapter 4: Memory

This agentic RAG system allows the agent to access the A-MEM and search for
memories that relate to the query. The links that are made between notes are used
when retrieving relevant information. The agent can choose to retrieve all notes that
have links to the retrieved note.
We again see that these memory systems mirror aspects of human memory. Many
insights from how we store and use knowledge often serve as inspiration for the
design of agentic memory systems.
Search-o1
A recent approach to agentic RAG is Search-o1, a method that attempts to retrieve
relevant context and put it throughout the reasoning traces to enhance the rea‐
soning LLM’s capabilities further.8 Instead of autonomously searching for relevant
information and using it in the prompt of the model, the information can be
searched and retrieved during the LLM’s reasoning process. As such, it’s the differ‐
ence between the information that is provided to the LLM and the information
retrieved during the thinking stage of the LLM. The agent is instructed to use the
<|begin_search_query|> and <|end_search_query|> tokens to start a search and
then use the <|begin_search_result|> and <|end_search_result|> tokens to indi‐
cate what the retrieved information is. Figure 4-25 demonstrates this agentic RAG
during reasoning.



![Figure 4-25: Agentic RAG can be used during reasoning to enhance its performance](images/fig_04-25_Agentic_RAG_can_be_used_during_reasoning.png)

*Figure 4-25: Agentic RAG can be used during reasoning to enhance its performance*


Figure 4-25. Agentic RAG can be used during reasoning to enhance its performance
before finally giving back an answer
8 Li, Xiaoxi et al. 2025. “Search-o1: Agentic Search-Enhanced Large Reasoning Models,” arXiv, 2501.05366.
Long-Term Memory
|

By enabling RAG during reasoning, using synchronous retrieval tools and structured
model calls, the model can iteratively refine its reasoning process until it is confident
in the final result. This dynamic approach is different from regular agentic RAG
because it can be done autonomously within a single call rather than iterating over
calls.
A downside to simply embedding documents within the reasoning traces is that the
retrieved documents can be quite large and often contain irrelevant information and
may therefore disrupt the reasoning flow. To solve this issue, the authors extend the
reasoning agentic RAG by incorporating a module called the Reason-in-Documents
module. Using the search query, retrieved documents, and reasoning trace, this mod‐
ule attempts to condense all information into focused reasoning steps. The agent’s
reasoning LLM is used to process the retrieved documents to align with the model’s
specific reasoning traces.
With regular agentic RAG, information is just passed to the context without taking
into account how the information needs to be processed. By enabling the same rea‐
soning LLM to further process that information such that it fits within the reasoning
traces, the flow of the traces can be kept intact. An overview of this system, called
Search-o1, is given in Figure 4-26.



![Figure 4-26: Search-o1 compresses the context using an LLM to create a more optimized](images/fig_04-26_Search-o1_compresses_the_context_using_a.png)

*Figure 4-26: Search-o1 compresses the context using an LLM to create a more optimized*


Figure 4-26. Search-o1 compresses the context using an LLM to create a more optimized
context with less redundant information
Note that this is typically used for long-term memory or external semantic memory
that the agent might need to answer a given query. For instance, when given the
query “Why are flamingos pink?,” it will search for relevant information in Wikipedia
during its reasoning process. The first result it finds mentions that it is due to specific
pigments in their specific diet. It will use that information during its reasoning until it
needs further clarification. For instance, a second call to a different external database
|
Chapter 4: Memory