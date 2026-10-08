# Summary: TinyAgent (Multi-Modal) through Code Tools

## TinyAgent

Connectors trade off along three axes. Projection-based ones are simple and cheap but flood the context window, since the input is never compressed. Query-based ones hold input length constant regardless of image or video resolution, at the cost of complex training and lost fine detail. Fusion-based ones perform best — multi-modal features are visible at every layer, not just as a prefix — but require architectural changes and expensive fine-tuning.

Making TinyAgent multi-modal is nearly free. Gemma 4 E4B already carries vision and audio encoders; the vision encoder emits 70–1,120 image tokens (more tokens, higher resolution) and the inference engine builds that chat template for us. Since messages are both memory and communication channel, images belong in the `Memory` class: a `MultimodalMemory` subclass accepts `image_data` and emits an `image_url` block (URL or base64, depending on the engine) beside the text block, and `run` gains one `image_data` parameter to forward. Asked which animal is on the *Hands-On Large Language Models* cover with no image, the agent correctly refuses; handed the base64 cover, it answers "kangaroo."

## Summary

Chapter 9 recap: per-modality encoders (ViT/CLIP, wav2vec 2.0/Whisper/CLAP, ViViT/TimeSformer, ImageBind for six modalities at once), nearly all Transformers, joined to a pretrained LLM by MLP projection, query-based Transformer, or cross-attention fusion. Two TinyAgent files changed: `agent.py` and `memory.py`.

## Chapter 10. Code Agents and Code LLMs

Code generation was among the first LLM applications at GPT-3 scale in 2020 and underpins reasoning models. Code matters because a huge share of knowledge work is expressible as it, and because ==it is automatically verifiable — run it and get a clear signal== — which makes it far more tractable to train on than open-ended tasks.

## Users and Builders of Code Agents and Large Language Models

![Figure 10-1: The target audience for code agents, ranging from end users to professional](images/fig_10-01_The_target_audience_for_code_agents_rang.png)

*Figure: A stacked taxonomy — results-only users, vibe coders, and software engineers above builders of coding agents, with builders of coding LLMs at the base.*

The tiers differ by proximity to the code: results-only users may never see it, vibe coders steer in natural language, engineers direct the agent inside a codebase.

![Figure 10-2: Coding agents take LLM capabilities of generating code to the next level and](images/fig_10-02_Coding_agents_take_LLM_capabilities_of_g.png)

*Figure: The escalation in three panels — a playground LLM returning `import matplotlib.pyplot`, an agent with an execution environment and data source returning the finished plot, and a software-engineering agent with a repository reporting "applied the fix and it passes the unit tests."*

The middle panel is pivotal: the user need not be a developer. The third may run hundreds of steps against a richer environment.

## Building Code Agents

Rather than open with Cursor-like engineering agents, the chapter starts with the larger audience: non-programmers.

## Code Agents to Serve Non-Coders

![Figure 10-3: An agent generating a plot by writing code to retrieve data and using](images/fig_10-03_An_agent_generating_a_plot_by_writing_co.png)

*Figure: One plotting request fanning out to an execution environment (Python sandbox or VM) and a data source (database via SQL, spreadsheet via pandas), with only the rendered chart reaching the user.*

Three expected behaviors: data retrieval (file handed to a sandbox, files found via command line, or SQL against a database), plot creation, and troubleshooting. Feeding an execution error back is the ReAct loop working — the error is just another observation — but planning for specific failure cases still improves the experience markedly.

## Code Tools

![Figure 10-4: A code agent resolving a request via a two-step trajectory, employing](images/fig_10-04_A_code_agent_resolving_a_request_via_a_t.png)

*Figure: "Plot our sales over the last 8 quarters" resolved in two steps — SQL tool to the database, then pandas/matplotlib to the Python environment, yielding the chart.*

The catalog: file manipulation (read whole or partial file, list, glob, grep — usually command-line wrappers with per-tool permissions); code interpreter sandboxes, resource-capped and ephemeral because LLM-generated code is not guaranteed safe, each added capability trading convenience for blast radius; and command-line access, needed for installing packages and running tests, where security turns acute. *RedCode* (2024) benchmarks dangerous behaviors, *SandboxEval* (2025) enumerates security properties, and *"Your Agent, Their Asset"* (2026) finds poisoning any single dimension of a personal agent's persistent state ==raises attack success from ~25% to 64–74%==, calling the exposure architectural rather than a fixable bug. Per-command approval suits an IDE developer but barely protects non-technical users, so the real safeguard is the builder's design-time choice: least privilege and narrowly scoped tasks.

![Figure 10-6: A computer use agent interacting directly with a virtual machine’s browser](images/fig_10-06_A_computer_use_agent_interacting_directl.png)

*Figure: A computer-use agent answering a Wikipedia question through thought/action pairs — `click("left", 308, 120)`, `Type("wikipedia.org")` — reading each VM screenshot back into the vision-language model.*

Execution can be hosted (Gemini's code-execution tool; Modal, Daytona, E2B, Together) or self-rolled via Open Interpreter. Rounding out the set: `ast-grep`, which matches on the syntax tree and so ignores formatting and variable names, semantic code search over embeddings (benchmarked by CoIR), and the SQL tool, whose advanced form adds a semantic layer indexing relevant columns and the vocabulary users actually use.
