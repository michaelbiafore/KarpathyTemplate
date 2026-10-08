# Agentic RAG through Context Optimization (Chapters 64-67)

## Agentic Retrieval-Augmented Generation

In vanilla RAG the vector database is the LLM's long-term memory, but retrieval is a static step the model has no control over. Agentic RAG hands that agency back: knowledge sources become tools, and the agent decides which one to query, how to interpret the result, and whether to search again before answering.

![Figure 4-19: Agentic RAG](images/fig_04-19_Agentic_RAG.png)
*Figure: The agent runs a four-step loop — select a knowledge source, retrieve, augment its context with the hits, then generate — and can loop back to retrieve again instead of answering.*

In single-agent systems this makes the agent a router over several databases, web search, or APIs like Slack and Gmail. Multi-agent RAG instead uses specialized retrieval agents coordinated by an orchestrator. The authors advise starting single-agent: cheaper, fewer dependencies, easier to debug — though it is a single point of failure whose context window can be overloaded. Multi-agent setups gain modularity and a higher accuracy ceiling (agents cross-check each other's hallucinations) at the cost of parallel API spend and harder error attribution.

Two implementations illustrate the space. **A-MEM** borrows the Zettelkasten method: each memory is one atomic interaction plus timestamp, LLM-generated keywords, tags, and a contextual description, embedded as a single vector. New notes are linked to their top-K nearest neighbors (the LLM picks which links to keep), and the older notes' tags and descriptions are then rewritten — an ever-evolving, hypertextual memory graph. **Search-o1** moves retrieval *inside* the reasoning trace, using `<|begin_search_query|>` / `<|begin_search_result|>` tokens so the model searches mid-thought and iterates until confident. Its Reason-in-Documents module condenses retrieved documents against the current reasoning trace so bulky, noisy passages do not derail the flow.

![Figure 4-26: Search-o1 compresses the context using an LLM to create a more optimized](images/fig_04-26_Search-o1_compresses_the_context_using_a.png)
*Figure: A thought emits a search query, the retrieved chunk plus thought and query are passed through an LLM compressor, and only the compressed context re-enters the reasoning chain.*

## Context Engineering

Memory is only one input. The full context also holds the system prompt (procedural), conversation history and internal thoughts (working), past experiences (episodic), retrieved information (semantic), tool schemas, and output schemas — the user's prompt is just a subset.

![Figure 4-27: A non-exhaustive overview of the kinds of information that can be put into](images/fig_04-27_A_non-exhaustive_overview_of_the_kinds_o.png)
*Figure: Everything that competes for the context window — system prompt, user prompt, tool schemas, retrieved information, conversation history, JSON output schema.*

Treating the LLM as a function from input tokens to output tokens, you can improve outputs by training the model or by optimizing the input. The latter is context engineering: finding the context that maximizes output quality. Where prompt engineering tunes the system and user prompts, context engineering governs the whole window.

Bigger windows are not a substitute. The needle-in-a-haystack benchmark flattered long-context models, but RULER's multi-hop tracing and aggregation tasks showed sharp degradation as length grows — "context rot."

![Figure 4-30: An artificial example of a typical needle-in-a-haystack test. In this example,](images/fig_04-30_An_artificial_example_of_a_typical_needl.png)
*Figure: Retrieval accuracy heatmap by needle depth and context length — failures cluster at longer contexts and mid-document placement.*

Cost and latency compound the problem. The goal is the right information, in the right place, in the right format — an architectural problem of tracking, storing, and retrieving.

## Context Engineering for Multi-Agent Systems

Multi-agent systems multiply the difficulty: every agent's context needs management, and inter-agent interaction is itself shared context. Offloading work to smaller, specialized agents with smaller LLMs isolates part of the burden, frees compute for the orchestrator, and yields clearer responsibilities that are easier to test and debug.

## Optimizing the Context

*(Chapters 66 and 67 overlap; the shared multi-agent material is summarized above.)*

Three strategies dominate. **Tracking and storage**: decide upfront what to persist — agent behavior (tool calls, outputs, inter-agent messages, reasoning steps, failures), user behavior (intent, feedback, edits, rejections), knowledge sources (database snapshots for auditing, external documents, artifacts like PLAN.md), and system-level configuration and guardrails. **Selection**: a reranker takes the query plus the retrieved candidate set and reorders by relevance, letting you drop everything below a threshold.

![Figure 4-32: Reranking involves optimizing a candidate set of results](images/fig_04-32_Reranking_involves_optimizing_a_candidat.png)
*Figure: Semantic search returns an initial list; a reranker scores it against the query and the low-relevance tail is cut.*

Structured output and business rules help too, as does routing the right context to the right agent. **Compression**: LLM summarization of conversation history or RAG output, plus redundancy reduction. Maximal Marginal Relevance computes a relevance vector (query-to-document similarity) and a redundancy matrix (document-to-document similarity), then iteratively picks documents that are relevant but dissimilar to those already chosen, with λ controlling the diversity tradeoff.

![Figure 4-36: Maximal Marginal Relevance (MMR) uses redundancy vectors to calculate](images/fig_04-36_Maximal_Marginal_Relevance_MMR_uses_redu.png)
*Figure: MMR subtracts (1−λ) times the redundancy vector from λ times the relevance vector, selecting doc 3 as the next most diverse-and-relevant pick.*
