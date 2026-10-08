# Context As the Specification → Tool Learning (ch. 68–78)

## Context As the Specification

Order matters as much as content. LLMs attend most to the beginning and end of a context and lose material in the middle — the "lost-in-the-middle" phenomenon, an analogue of the human serial-position effect. It bites only at long contexts, which is largely why context engineering exists.

![Figure 4-37: An annotated figure of the “lost-in-the-middle” phenomenon from “Lost in](images/fig_04-37_An_annotated_figure_of_the_lost-in-the-m.png)

*Figure: Accuracy on retrieved documents dips sharply when the answer sits mid-prompt, falling below even the closed-book baseline.*

The deeper shift is in mindset: context is a communication tool aimed at both the agent and your colleagues.

## Summary

The query, `PLAN.md`, `REQUIREMENTS.md`, and codebase are the *specification* of the feature. When a coding agent opens a PR autonomously, reviewing the diff is not enough — the inputs that produced it must be tracked too. Prompt engineering is user-facing; context engineering is developer-facing and answers *why* the agent acted. Keeping only the LLM's output while discarding its input is strange: retaining it buys reproducibility, debuggability, and transparency of intent. Context is also irreducibly domain-specific — health care differs wholly from law — so no single framework applies. This closes the memory arc (short-term compression; long-term and agentic RAG via MemoryBank, A-MEM, Search-o1; context engineering).

## Tool Usage

Tools are what let an agent touch its environment. Usage decomposes into five steps: creation, definition, selection, calling, output processing. Critically, ==the LLM never executes a tool — it only emits the *intention* to==; an external automated process does the work.

![Figure 5-5: An example of tool creation, definition, selection, tool calling, and output](images/fig_05-05_An_example_of_tool_creation_definition_s.png)

*Figure: The full round trip for "What is 5.1 times 7.3?" — the user creates and defines `multiply`, the LLM selects it, an external process calls it and returns 37.23, and the LLM phrases the answer.*

## Tool Creation

Tools are ordinary functions reachable by API or code. `multiply(a: str, b: str) -> float` takes strings because LLMs emit only text. Docstrings are often passed verbatim to the model, making documentation a first-class concern: edge cases the agent cannot infer from code must be written down. Functions live in a `registry` dict keyed by name.

## Tool Definition

Definition tells the model what exists. Models learn tools during fine-tuning or from the prompt; modern models (Qwen3, DeepSeek-V3.2) favour general instruction-following over memorised tool sets. You can describe tools in prose with an invented call syntax plus a parser — flexible but error-prone — or pass JSON Schema objects through an API's `tools` parameter, which usually lands in the system prompt anyway.

![Figure 5-6: The system prompt may contain the full JSON schema for the LLM to use](images/fig_05-06_The_system_prompt_may_contain_the_full_J.png)

*Figure: The messages list at call time — a system message carrying the `multiply` JSON schema, then the user's question.*

Best practices: document heavily, ==keep the tool count under about ten==, and keep each tool's scope and parameter list small.

## Tool Selection

The model must pick the right tool, or none. Reasoning models shine here, spending tokens deliberating over fit and arguments.

![Figure 5-7: The reasoning process of an LLM deciding which tool to use](images/fig_05-07_The_reasoning_process_of_an_LLM_deciding.png)

*Figure: The model reasons aloud that `multiply` rather than `divide` matches the question, and fixes a = 5.1, b = 7.3.*

As tool counts grow, stuffing every schema into the window degrades performance; store schemas in a vector database and retrieve only what's relevant.

![Figure 5-8: An example of Retrieval-Augmented Generation (RAG) for searching and](images/fig_05-08_An_example_of_Retrieval-Augmented_Genera.png)

*Figure: RAG over a tool database — the query searches embedded tool definitions and only top matches are injected alongside it.*

## Tool Calling

The model emits a string; nothing runs. `Tools.parse` locates the JSON and attaches it as a `tool_call`; `Tools.execute` looks the name up, pauses for human approval if the tool is on a `requires_approval` list, and invokes it. Regex extraction is brittle — prefer jsonschema or Pydantic.

## Tool Output Processing

The result returns as messages. Natively trained models accept an `assistant` message with `tool_calls` plus a `tool`-role result — a polite fiction, since the model never ran anything.

![Figure 5-11: An example of how the user role can be used to relay the output of the tool](images/fig_05-11_An_example_of_how_the_user_role_can_be_u.png)

*Figure: For models without tool tokens, the result comes back as a plain `user` message prefixed `OBSERVATION: 37.23`.*

## TinyAgent with Tools

`TinyAgent` gains a `Tools` object whose `prompt` folds into the system prompt. A `_step` runs THOUGHT (generate) → parse → stop-check (`is_done` fires on no tool call or on `final_answer`) → `_execute_action`, which calls the tool and appends the OBSERVATION. Caveat: `SummarizationMemory` overwrites the system prompt and would erase the tool definitions. The capitalised THOUGHT/ACTION/OBSERVATION/ANSWER labels foreshadow Chapter 6's ReAct loop.

## Tool Learning

Running the query on Gemma 3 12B — no native tool calling — returns `OBSERVATION: 37.23`, and the message log confirms the tool really fired. Reliability still rests on the model's orchestration skill, which motivates training for tool use: in-context learning, supervised fine-tuning, and reinforcement learning.
