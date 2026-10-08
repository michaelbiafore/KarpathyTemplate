## Table of Contents

- What an Agent Is
- The Substrate: Tokens, Transformers, Training
- Reasoning and Test-Time Compute
- Memory and Context Engineering
- Tools, MCP, and Skills
- Planning, Reflection, Self-Improvement
- Evaluating a System, Not a Model
- Multi-Agent Systems
- Multi-Modal Understanding
- Code Agents
- Where the Book Says This Is Heading

## What an Agent Is

The book takes the classical definition — an agent "perceives its environment through sensors and acts upon that environment through actuators" (Russell & Norvig) — and maps it onto LLMs: the **agent program** is a reasoning LLM, the **actuators** are tools, multi-modal inputs are **sensors**, and the user sits inside the environment, usually starting the loop.

![Figure 1-2: Agents operate in regular contact with a user and environment, and use](images/fig_01-02_Agents_operate_in_regular_contact_with_a.png)

*Figure: The anchor diagram of the whole book — a reasoning LLM augmented by Memory, Tools, and Planning, cycling query/answer with the user and action/feedback with the environment.*

Every later chapter is one block of that picture. A bare LLM is a stateless text-to-text function; **memory** makes it multi-turn, **tools** let it act, and **planning and reflection** let it decompose a goal and revise. Autonomy is a spectrum: goal-directed decision-making counts as agency even inside an orchestrated workflow. Agents pay off where the goal is clear but the path is not — coding, deep research, automation. The reader builds a Python **TinyAgent** one component per chapter; the surrounding code is the **harness**, and terminal, hosted, and UI harnesses all share the same scaffolding.

## The Substrate: Tokens, Transformers, Training

An LLM tokenizes input, scores the whole vocabulary, samples one token, appends it, and repeats — **autoregression**. The architecture is a Transformer decoder: tokenizer, a stack of blocks, and an LM head.

![Figure 2-22: Inside each Transformer block are a self-attention layer for gathering](images/fig_02-22_Inside_each_Transformer_block_are_a_self.png)

*Figure: Embeddings pass block to block at constant size; inside each block, self-attention supplies context while the feed-forward network holds the learned factual associations.*

Self-attention projects each token into **queries, keys, and values**, scores the current query against all keys, and sums the values by those weights. The number of parallel token tracks is the **context size** — the hard limit that makes context engineering a discipline. Because earlier tokens' keys and values can be reused, **kv-caching** is the cheapest latency lever an agent builder has; its memory cost drives GQA, MQA, Multi-head Latent Attention, and DeepSeek Sparse Attention. **Mixture-of-experts** replaces the feed-forward network with a router plus specialists, so `Qwen3-30B-A3B` loads 30B parameters but runs 3B per token. Training runs pre-training → SFT → RLHF, with **RLVR** swapping the human rater for an automated verifier and **GRPO** scoring each sample against its group. Chat format, system prompts, and tool calls are post-training conventions, not architecture.

## Reasoning and Test-Time Compute

Reasoning LLMs emit thinking tokens before answering — Kahneman's System 2 against a non-reasoning System 1. Train-time scaling hit a cost-effectiveness wall around 2024, so compute moved to inference. The book splits **test-time compute** into two families.

![Figure 3-17: Search against verifiers (left) generates multiple traces and from them](images/fig_03-17_Search_against_verifiers_left_generates.png)

*Figure: Left, many thought/answer pairs scored by reward models and the best one kept; right, fine-tuning on thought processes so the model reasons by default.*

Search against verifiers needs no retraining: self-consistency takes a majority vote, best-of-N scores candidates with an **ORM** (final answer only) or a **PRM** (each step), and verifiers can be rule-based — unit tests, compilers. Modifying the proposal distribution is input-focused: the `s1` paper turned Qwen2.5-32B into a stable reasoner on ==1,000 curated question/trace pairs==, while DeepSeek-R1-Zero skipped SFT entirely and used GRPO with only accuracy and format rewards. Reasoning emerged unprompted — average trace length climbed from ~500 to ~10,000 tokens with no instruction to do so. The frontier now runs toward efficient reasoning (Chain-of-Draft, budget-aware length rewards, Qwen3's `/no_think`) and latent reasoning, trading debuggable visible traces for cheaper hidden ones.

## Memory and Context Engineering

Memory is working (chat history), episodic (past events), semantic (world and application knowledge), and procedural (how-to patterns in the system prompt or the weights). Short-term memory is just replay, bounded by the context window; trimming drops old turns, summarization compresses them. Long-term memory means an external store.

![Figure 4-15: The full pipeline of retrieval- (2) augmented (3) generation (4)](images/fig_04-15_The_full_pipeline_of_retrieval-_2_augmen.png)

*Figure: The four-step RAG loop — embed the query, retrieve nearest vectors, augment the prompt with that context, generate the answer.*

**Agentic RAG** hands retrieval back to the model: knowledge sources become tools, and the agent chooses which to query and whether to search again. From there the argument widens. The context window holds the system prompt, history, retrieved text, tool schemas, and output schemas — the user's prompt is a small subset. Bigger windows do not fix this: RULER showed sharp degradation with length ("context rot"), and "lost-in-the-middle" means position matters as much as content. The levers are selection (rerankers, Maximal Marginal Relevance) and compression. The deeper claim is that context *is* the specification — prompt engineering is user-facing, context engineering is developer-facing and answers *why* the agent acted.

## Tools, MCP, and Skills

Tool usage decomposes into creation, definition, selection, calling, and output processing.

> The LLM never executes a tool — it only emits the *intention* to.

![Figure 5-5: An example of tool creation, definition, selection, tool calling, and output](images/fig_05-05_An_example_of_tool_creation_definition_s.png)

*Figure: The full round trip for "What is 5.1 times 7.3?" — the user defines `multiply`, the LLM selects it, external code runs it and returns 37.23, and the LLM phrases the answer.*

Tools are ordinary functions described by JSON Schema in the system prompt; docstrings are the real interface, so document heavily, ==keep the tool count under about ten==, and retrieve schemas from a vector store once there are more. Three routes instill the capability: in-context examples, SFT (Toolformer splices `[calculator(5.1*7.3)→37.23]` inline), and RL — ToolRL trains on correctness and format rewards, Search-R1 masks loss on retrieved tokens so the model cannot learn to fake its own search results. **MCP** standardizes access through a host, one client per server, and servers wrapping each data source. What MCP does not supply is *when* to act; **Skills** do, bundling procedural knowledge behind a `SKILL.md` whose frontmatter costs ==~100 always-resident tokens== and whose body loads only on activation — progressive disclosure as context engineering.

## Planning, Reflection, Self-Improvement

Planning starts with task decomposition — a query becomes subtasks, each possibly nested. Chain-of-Thought is itself decomposition; least-to-most feeds each sub-answer into the next prompt, plan-and-solve does it zero-shot, Tree of Thoughts branches and prunes. But decomposition alone does not give an *order*.

![Figure 6-11: ReAct fuses reasoning and acting, allowing the LLM to produce a reasoning](images/fig_06-11_ReAct_fuses_reasoning_and_acting_allowin.png)

*Figure: The ReAct loop — the model emits a reasoning trace, fires an action into the environment, and feeds the observation back into its own next thought.*

ReAct's THOUGHT / ACTION / OBSERVATION cycle is the agent loop, and in TinyAgent it is literally a `for` loop over `max_steps`. Prompted ReAct is brittle and eats context, so FireAct fine-tunes on filtered GPT-4 trajectories and ETO adds DPO over failed-versus-correct pairs. Reflection is the internal counterpart to environment feedback: Self-Refine has one model critique and revise its own output; **Reflexion** splits the work into an Actor, an Evaluator, and a Self-Reflection LLM whose verbal feedback is written to long-term memory. Beyond prompting, TTRL rewards agreement with a majority vote at inference time, and R-Zero co-evolves a Challenger that invents hard problems against a Solver that answers them.

## Evaluating a System, Not a Model

Evaluation is the book's most underinvested area. Public benchmarks (SWE-bench Verified, τ-bench, BFCL, OSWorld, GAIA) are a fixed task set plus a scoring procedure, and a score is really a *model-and-harness pair* — rankings flip when the same model is run in a minimal harness. Read scores for contamination, prompt tuning, partial credit, saturation above ~85%, and cost.

![Figure 7-9: Three correct outcomes, three different problems in the trajectory. Agent A](images/fig_07-09_Three_correct_outcomes_three_different_p.png)

*Figure: Three agents all answer correctly — one guessed, one burned five tool calls, one overthought — and outcome evaluation passes all three.*

Hence two lenses. **Outcome evaluation** scores the artifact, via exact match, programmatic checks, LLM-as-a-judge (watch position bias and same-family favoritism), or rubrics. **Trajectory evaluation** scores the steps: right tools, valid arguments, efficiency, and whether each step follows from the last. Because output is stochastic, multiple trials separate capability from reliability: `pass@k` asks whether *any* of k attempts succeeded, `pass^k` whether *all* did, and they rank models differently. Safety gets its own suite — misuse, prompt injection and memory poisoning, and plain error. The practical advice: 5–10 curated cases weighted toward your real failure modes beat any leaderboard.

## Multi-Agent Systems

A multi-agent system gives each agent its own tools, subgoals, and sometimes personality. Agents may be homogeneous (identical workers in parallel), heterogeneous (predefined specialists), or emergent. The benefits are collaboration, scalability, and speed; the costs are orchestration complexity, compute per capable model, and evaluation multiplied across agents.

![Figure 8-4: Four different patterns of agent orchestration](images/fig_08-04_Four_different_patterns_of_agent_orchest.png)

*Figure: Centralized hub, decentralized mesh, hierarchical tree, and federated clusters that exchange only summaries across a privacy boundary.*

Centralized is most common and collapses with its orchestrator; decentralized is most stable but communication-heavy; federated keeps data inside organizational walls. A framework-free shortcut builds the centralized case by wrapping each subagent as a plain function and registering it as a tool. CAMEL does role-play, MetaGPT scales it to a software-development SOP passing structured artifacts, and A2A standardizes discovery via an agent card at `/.well-known/agent.json`. Left in a shared environment without tasks, agents form societies — Smallville's generative agents run perceive → memory → plan/reflect → act over a recency/importance/relevance memory stream. Deep Research and Google's AI co-scientist are the flagship production cases.

## Multi-Modal Understanding

A multi-modal LLM has four parts: an **encoder** per modality, a **connector**, the LLM, and an optional **generator**. Most systems only understand, since generating other modalities costs far more. Encoders are nearly all Transformers — ViT and CLIP for images, wav2vec 2.0 and Whisper for audio, ViViT and TimeSformer for video, ImageBind binding six modalities through the visual one — but each emits embeddings of different length, range, and precision, so a trained connector must bridge them.

![Figure 9-41: The three types of connectors: the projection, query, and fusion connectors](images/fig_09-41_The_three_types_of_connectors_the_projec.png)

*Figure: The three connector families side by side — an MLP projection, a Q-Former driven by learnable queries, and fusion injecting image K/V into attention inside the LLM.*

| Connector | Mechanism | Trade-off |
|---|---|---|
| Projection | MLP maps patch embeddings into token space (LLaVA, Qwen2.5-VL) | Simple and cheap; never compresses, so it floods the context window |
| Query | Q-Former compresses to a fixed set of learnable queries (BLIP-2) | Input length constant at any resolution; complex training, may skip detail |
| Fusion | Gated cross-attention inserted between frozen LM blocks (Flamingo) | Best performance — features seen at every layer; architectural surgery |

## Code Agents

Code came first and stayed ahead for one reason: ==it is automatically verifiable — run it and get a clear signal== — which makes it tractable to train on and the reason coding benchmarks moved from ~2% to over 70% on SWE-bench Verified.

![Figure 10-14: The shift from writing isolated functions to full-scale software engineering](images/fig_10-14_The_shift_from_writing_isolated_function.png)

*Figure: One prompt yielding a LeetCode-style function, versus a GitHub issue driving an agent with code tools and a VM through N plan-and-think steps to a repository diff.*

The tool catalog is file manipulation, a resource-capped ephemeral interpreter sandbox, and command-line access — each capability trading convenience for blast radius. Per-command approval suits a developer in an IDE and barely protects anyone else, so the real safeguard is the builder's design-time choice of least privilege; one 2026 study found poisoning any single dimension of a personal agent's persistent state ==raises attack success from ~25% to 64–74%==. Long trajectories force context management: prefix caching pays only if the cached prefix stays byte-identical, so partition the trajectory into static, stable, and dynamic sections and let only the last churn. A fixed workflow often beats an agent — Agentless localizes, samples candidate patches, and ranks them with generated tests.

## Where the Book Says This Is Heading

Compute keeps migrating toward inference — from reasoning traces to test-time *training*, where RL runs on unlabeled data while the agent works. Each model generation increasingly trains the next, and code's verifiability is the training signal that makes it possible. The warning is evaluation: benchmarks cluster around programming while high-employment occupations go untested, so your own small eval suite is the only honest measure. Which is why the book argues for intuition over frameworks — the diagrams, not the APIs, are what survives the churn. The afterword makes the point plainly, borrowing Robin Wall Kimmerer: a transaction is even and closes, a gift is uneven and never closes, asking only that it keep moving.

> Build well; make something that outlasts the book and its authors' names.
