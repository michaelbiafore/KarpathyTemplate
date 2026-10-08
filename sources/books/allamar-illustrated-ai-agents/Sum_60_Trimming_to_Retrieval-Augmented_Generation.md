# Memory: Trimming, Summarization, and Long-Term Recall (Chapters 60-63)

> Note: chapters 62 and 63 overlap — 62 is the opening page of 63, repeated verbatim. The shared material on long-term memory and the RAG definition is summarized once, under "Long-Term Memory."

## Trimming

Context windows are finite, and overflowing one has two failure modes: the generated output gets clipped mid-stream, or nothing is generated at all because the input alone already exceeds the window. Worse, even when everything fits, the more you stuff into a prompt the harder it is for the model to attend to all of it (the RULER benchmark is cited here). So the full conversation history cannot simply be pasted in every turn.

The crudest fix is trimming: as messages accumulate, drop the oldest ones until the rest fits.

![Figure 4-10: Efficient short-term memory may include keeping only the last couple of](images/fig_04-10_Efficient_short-term_memory_may_include.png)
*Figure: turns 1 and 2 are struck out and discarded while only the most recent two user/assistant turns are fed to the LLM.*

Implementation is trivial on top of the book's `Memory` module — a `TrimmingMemory` subclass overrides `add` to keep the system message plus the last four messages. The cost is obvious: information introduced early is simply gone. The author notes an amusing leakage effect, though — facts can survive past the cutoff if the assistant keeps restating them in its own answers, since those answers stay in the window.

## Summarization

The alternative is to compress rather than delete: after each turn, an LLM (the same one or a cheaper one) rewrites the running summary to absorb the new exchange, and that summary — not the raw transcript — goes to the model alongside the next query.

![Figure 4-11: Each conversation turn may be summarized and merged into one long](images/fig_04-11_Each_conversation_turn_may_be_summarized.png)
*Figure: each turn's user/assistant message pair is passed through an LLM to produce per-turn summaries, which merge into one full summary.*

Stacked summaries still grow, just far more slowly than raw history; re-summarizing the summary buys more room but risks compressing away something important. Variants include summarizing every five turns, or keeping one summary that gets updated in place. A hybrid keeps older turns summarized while the newest turn stays uncompressed, balancing compression against fidelity. The `SummarizationMemory` example stores the running summary in the `system` role so it stays separable from live dialogue; after one turn, memory holds a single system message paraphrasing the whole exchange. In both schemes the raw trajectory remains inspectable via `TrajectoryViewer` — important, since agent memory is deliberately lossy.

## Long-Term Memory

Beyond conversation, agents need durable external knowledge: past traces and states (episodic memory) and application context such as organizational documents (semantic memory). This means one or more external databases that can be queried on demand.

## Retrieval-Augmented Generation

RAG is the standard mechanism. Ingestion embeds unstructured text into vectors via an embedding model and stores them in a vector database. Inference has four steps.

![Figure 4-15: The full pipeline of retrieval- (2) augmented (3) generation (4)](images/fig_04-15_The_full_pipeline_of_retrieval-_2_augmen.png)
*Figure: the four-step loop — embed the query, retrieve nearest vectors, augment the prompt with the retrieved context, generate the answer.*

The worked example uses EmbeddingGemma (308M parameters, 768 dimensions) served through Ollama, with cosine similarity doing the ranking: "I love flamingos" scores 0.64 against "Flamingos are pink birds" but only 0.35 against "Dolphins use echolocation." `RAGMemory` embeds a document set once, then intercepts every user message to prepend the top-3 matches as context. It answers correctly — but blindly taking the top three regardless of absolute score is the method's weakness; a minimum-similarity threshold is suggested instead. RAG's main payoff is reduced hallucination, assuming the retrieved context is actually correct.

MemoryBank extends this with continuous updating: retrieved items are reinforced, unused ones decay and may be deleted, modeled on the Ebbinghaus forgetting curve.

![Figure 4-16: An example of the forgetting curve theory that demonstrates how spaced](images/fig_04-16_An_example_of_the_forgetting_curve_theor.png)
*Figure: retention decays exponentially, but each active retrieval resets it to 100% and flattens the subsequent decay curve.*

It stores three memory types — raw conversation history, LLM-generated summaries of past events, and a dynamically updated "user portrait" of personality and emotion that is always passed as context.

![Figure 4-18: How MemoryBank is used for RAG](images/fig_04-18_How_MemoryBank_is_used_for_RAG.png)
*Figure: a query searches the vector store, retrieves a summary plus the user portrait, strengthens what it used while an unused item is marked for removal, and the answer is written back.*

The examples above are "vanilla" or "naive" RAG; GraphRAG and multimodal RAG carry their own considerations.
