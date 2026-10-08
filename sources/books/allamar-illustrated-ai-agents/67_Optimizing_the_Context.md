---
title: "Optimizing the Context"
chapter_number: 67
page_start: 186
page_end: 191
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Optimizing the Context

conversation history. Likewise, Search-o1 compresses the retrieved context and gives
back only the relevant components without any noise. These dynamic memory tech‐
niques are exceptionally useful for context engineering as the information flows grow
more complex.
Context Engineering for Multi-Agent Systems
As we will cover in more depth in Chapter 8, multi-agent systems deploy groups of
agents working together to solve a given problem. Our example of a deep research
agent used a summarization agent in its system, thereby working together. What
makes context engineering especially difficult in multi-agent systems is that not only
the context of the main agents needs to be carefully managed, so do the contexts of
all other agents in the system. Moreover, the interaction between agents is also part of
the shared context between those respective agents.
To manage this complex network of contexts, smaller agents can be used to handle
some of the context “burden,” as we illustrated in the deep research agent. By using
a smaller agent with a smaller LLM for specific tasks, part of the context can be
handled separately, leaving significant compute for the main agent (also called the
orchestrator agent). What makes these small and/or specialized agents great for
context engineering is that they can work on smaller and more manageable contexts,
have clear responsibilities, and are easier to test and debug. These systems can be
more reliable by separating tasks instead of having one agent juggle all kinds of
different tasks and contexts.
Optimizing the Context
Throughout this chapter, we covered many different methods and techniques for
handling the memory and context of LLMs and agents. Optimizing what you put into
the context and how is a multi-faceted problem that requires an understanding of
various parts of your agent’s architecture. Most strategies to optimize the context are
built upon the main source of context, the memory modules of the agent, but often
also include system prompts and tool schemas.
Although there are many strategies, let’s explore the most common ones.
Context tracking and storage
Before you give the agent a possible relevant context, it first needs to be tracked and
stored somewhere. We covered most of it already, as this relates to various forms of
memory, and in particular episodic memory, which contains the actions the agent has
taken thus far. Although episodic memory is seen as long-term memory, it is highly
related to the conversation history of the agent, which tends to capture the agent’s
actions.
|
Chapter 4: Memory

However, tracking the context goes beyond just the event traces of the agent. It
also involves managing external knowledge sources, such as a database of your
proprietary data, which can serve as additional context. To set up these sources of
knowledge, you’ll have to decide beforehand what kinds of information you want to
track. Although it may seem obvious at first, there are many types of information you
can track:
Agent behavior
Tool usage by the agent (and any subagents)
Tool outputs and intermediate results
Interactions between (sub)agents
Internal reasoning steps
Conversation history
Failures/successes
User behavior
User intent (explicit requests and goals)
User feedback (edits, approvals, rejections)
Knowledge sources
Snapshots of your proprietary database(s) for reproducibility and auditing
External documents (RAG, APIs, etc.)
Structured artifacts like PLAN.md, REQUIREMENTS.md, etc.
System-level
Configuration (LLM hyperparameters, available tools, etc.)
Policies (guardrails, constraints, etc.)
All of these are merely examples of what you could possibly track. In practice, not
everything is going to be useful, and at the same time, many other things should
be included, such as privacy and safety constraints. As we’ll explore later, tracking
these kinds of contexts and information also helps communicate the user’s intent and
debug these complex systems.
Context selection
Assuming you have set up all your databases, the very first thing you can do to
optimize the context is to have a system in place that selects the right context. As
we discussed before, RAG is an amazing technique and example for selecting what is
relevant. Although we have seen variants of RAG that improve on this, we haven’t yet
explored how we can further improve this selection process.
Context Engineering
|

In RAG, the input documents are typically split into smaller parts, such as sentences
or paragraphs, to isolate the information they contain and keep it to a single subject.
However, when you then run a RAG pipeline, you typically get a collection of
documents in return. For example, if we search a vector database for the “causes
of climate change,” the system might return documents about greenhouse gases,
industrial activity, and deforestation. Although those documents might not directly
answer our question, they are related.
To improve this process, we can use a reranker to refine the set of documents that
were retrieved. This technique, often a language model, takes in both the query and
retrieved documents to rerank the retrieved documents based on their relevance to
the query and to each other (Figure 4-32). By providing the reranker with additional
context (each retrieved document), it can operate on far fewer documents than
if we were to give it the entire database. Moreover, after the results have been
reranked according to their relevance, we can choose to keep only the most relevant
documents.



![Figure 4-32: Reranking involves optimizing a candidate set of results](images/fig_04-32_Reranking_involves_optimizing_a_candidat.png)

*Figure 4-32: Reranking involves optimizing a candidate set of results*


Figure 4-32. Reranking involves optimizing a candidate set of results
Reranking is often used for search-based use cases, such as deep research where an
agent has to research a given subject by finding and summarizing the most relevant
papers for a given query. Often, thousands of relevant papers could be found but
reranking helps reduce that amount.
Reranking is only one of the many ways to select and create the right context. We
can also structure the output to ensure the responses of the agent are broken up into
logical parts and contain only the necessary components. Likewise, we can employ
business rules that give additional weight to certain pieces of information that always
provide important context (much like a system prompt).
|
Chapter 4: Memory

Note that selecting the right context can also mean selecting the right context for the
right agent. By isolating the context across multiple specialized agents, each agent is
able to focus on a smaller part of the problem without being overwhelmed by the full
context.
Context compression
The goal of context engineering is to find a balance between what you put in the
context and how much. As such, compressing the context as much as possible is an
important strategy for optimizing it.
A common way to handle compression is what we discussed at the beginning of
this chapter, using an LLM to create summaries of your conversation history. As we
explored in Search-o1, we can even compress the output of the RAG pipeline using
an LLM to summarize the retrieved documents.
Another method of compressing the context is reducing redundancy. Even with a
reranker, the top five most relevant results might all contain very similar documents.
Together, they’re not bigger than the sum of their parts but smaller because they
contain similar information. As such, we want not just the most relevant documents,
but those that each contain a new piece of information rather than redundant
information.
A common technique to use for documents, whether they’re the output documents
of your RAG pipeline or other pieces of retrieved information, is Maximal Marginal
Relevance (MMR).17 This technique uses a precalculated relevance vector and redun‐
dancy matrix to balance the diversity of documents.
First, the similarity between the retrieved document and query embeddings is calcu‐
lated. This results in a relevance vector that has a value per document to indicate how
similar/relevant the given document is to the query (Figure 4-33).
17 Carbonell, Jaime and Jade Goldstein. 1998. “The Use of MMR, Diversity-Based Reranking for Reordering
Documents and Producing Summaries,” Proceedings of the 21st Annual International ACM SIGIR Conference
on Research and Development in Information Retrieval.
Context Engineering
|



![Figure 4-33: A relevance vector is created by calculating the similarity between the query](images/fig_04-33_A_relevance_vector_is_created_by_calcula.png)

*Figure 4-33: A relevance vector is created by calculating the similarity between the query*


Figure 4-33. A relevance vector is created by calculating the similarity between the query
embedding and the retrieved document embeddings
Second, the similarity between the retrieved documents is likewise calculated to
construct a similarity matrix called the redundancy matrix. This matrix is used to
potentially discard documents that are too similar to the ones we already chose
(Figure 4-34).



![Figure 4-34: The redundancy matrix is created by calculating the similarity between all](images/fig_04-34_The_redundancy_matrix_is_created_by_calc.png)

*Figure 4-34: The redundancy matrix is created by calculating the similarity between all*


Figure 4-34. The redundancy matrix is created by calculating the similarity between all
combinations of retrieved document embeddings
Then, the relevance vector and redundancy matrix are used iteratively to decide
which retrieved documents are similar enough to a given query but dissimilar to all
other retrieved documents. An important component is the lambda (λ) parameter,
which we can tweak to decide how diverse the output should be (a higher score
indicates higher diversity). We now have all components of the main formula of
MMR, as shown in Figure 4-35.
|
Chapter 4: Memory



![Figure 4-35: The formula of Maximal Marginal Relevance](images/fig_04-35_The_formula_of_Maximal_Marginal_Relevanc.png)

*Figure 4-35: The formula of Maximal Marginal Relevance*


Figure 4-35. The formula of Maximal Marginal Relevance
Let’s break down each of those components. Since we haven’t chosen any documents,
we start by selecting the one with the highest score in the relevance vector, namely
document 1 (or i in this example). Then, we take the relevance vector and multiply it
by λ to decide the importance of similarity over diversity. From the resulting scores
(one for each document other than document 1), we subtract (1 – λ) times the
redundancy vector. This vector contains the highest scores in the redundancy matrix
that relate to the documents we already chose (document 1). As demonstrated in
Figure 4-36, document 3 is added as the next most diverse and relevant document.



![Figure 4-36: Maximal Marginal Relevance (MMR) uses redundancy vectors to calculate](images/fig_04-36_Maximal_Marginal_Relevance_MMR_uses_redu.png)

*Figure 4-36: Maximal Marginal Relevance (MMR) uses redundancy vectors to calculate*


Figure 4-36. Maximal Marginal Relevance (MMR) uses redundancy vectors to calculate
the next most diverse and relevant document to retrieve
We continue this process, but instead of comparing to document 1 only, the redun‐
dancy vector contains the highest similarity scores that relate to either document 1 or
3, whichever is highest. This process is only repeated for the next document, since we
wanted to bring down our original set of five documents to three in total.
Like reranking, MMR is merely an example of a technique that can be used to
compress the output. We’re not limited to using LLMs to directly compress the
retrieved documents; we can instead use techniques like MMR to simply ignore
certain documents because they’re too similar to each other. Likewise, deduplication
Context Engineering
|