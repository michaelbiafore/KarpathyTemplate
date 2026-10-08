# Tool Learning, MCP, and Skills (Chapters 79-89)

## In-Context Learning

Few-shot prompting is the cheapest route to tool-calling behavior: show the LLM hand-written examples of the exact format you want and let pattern recognition do the rest.

![Figure 5-13: An example of few-shot prompting to enable tool calling](images/fig_05-13_An_example_of_few-shot_prompting_to_enab.png)
*Figure: A system prompt carrying multiply/add/subtract schemas, two worked Q/A pairs wrapping calls in `<tool_call>` tags, and the live query the model answers in the same shape.*

## Supervised Fine-tuning

The strongest variant puts the examples in the messages structure itself — fake `assistant` tool_calls and `tool` results, so the model believes it has already used the tools. But prompting burns context and risks instruction-following failure. Supervised fine-tuning (SFT) distills the capability into the weights instead. **Toolformer** embeds the call inline rather than round-tripping JSON: `[` opens a call, `→` pauses for execution, `]` closes once the result is spliced into its own token stream.

![Figure 5-18: An example flow of Toolformer](images/fig_05-18_An_example_flow_of_Toolformer.png)
*Figure: "What is 5.1 times 7.3?" becomes `[calculator(5.1*7.3)→37.23]` mid-generation, with the tool output returned as if it were a generated token.*

Training data was bootstrapped: a few-shot prompt per tool sampled candidates, filtered by correctness of call, correctness of output, and loss decrease; GPT-J was fine-tuned on the result. SFT beat zero-shot but generalized poorly — it mimics exact wording, while real tool data is ambiguous (several call shapes return the same file) and wrongly assumes tools never fail.

## Reinforcement Learning

RL replaces mimicry with trial and error, and suits tool calling because its rewards are verifiable. Tools fold into the reasoning trace itself — Tool-Integrated Reasoning (TIR).

![Figure 5-20: An overview of Tool-Integrated Reasoning](images/fig_05-20_An_overview_of_Tool-Integrated_Reasoning.png)
*Figure: The model thinks in `<think>`, emits a `<tool_call>`, receives the output, then resumes thinking before answering.*

**ToolRL** trains Qwen2.5 with GRPO on two rewards — correctness (right tool name and parameters) and format (required fields in order) — over 4,000 TIR traces. Length rewards for longer reasoning did not help and hurt smaller models.

![Figure 5-21: The training process of ToolRL](images/fig_05-21_The_training_process_of_ToolRL.png)
*Figure: GRPO scores each reasoning-plus-tools rollout on tool and format rewards and iteratively updates Qwen2.5 into Qwen2.5-ToolRL.*

**Search-R1** narrows to one tool, search, interleaving `<think>`, `<search>`, `<information>`, and `<answer>` across turns as an open-source DeepResearch alternative. It uses accuracy rewards only (Qwen2.5 already follows structure) and applies ==loss masking for retrieved tokens== so the model cannot learn to control search output. Qwen3 and GPT-OSS adopt similar tool-based rewards.

## TinyAgent with Native Tool-Calling Capabilities

Inference engines like Ollama hide the translation from a standard JSON schema to each model's private chat template and special tokens. Uncovering that "magic" takes `tool_to_schema` (inspecting a function's name, docstring, and parameters into an OpenAI-style schema) plus a `NativeTools` subclass that needs no prompt, parses `tool_calls` into `Response`, logs observations under the `tool` role, and stops when no tool call appears.

## Core Components

MCP has three parts: the **host** (the LLM app — Cursor, Copilot — the brain that initiates), the **client** (one per server; connection, discovery, forwarding), and the **server** (a lightweight program exposing a data source as tools, resources, and prompts).

![Figure 5-29: The main three components of MCP, namely the client, server, and host](images/fig_05-29_The_main_three_components_of_MCP_namely.png)
*Figure: Inside the host, one client per server speaks a unified MCP protocol outward, while each server speaks a custom API to GitHub, arXiv, or a database.*

## The MCP Flow

A numbered walkthrough of "Summarize the 5 latest commits."

![Figure 5-30: The first steps in using MCP, which mainly includes checking which tools are](images/fig_05-30_The_first_steps_in_using_MCP_which_mainl.png)
*Figure: Steps 1-4 — prompt to host, client asks server to list tools, server returns `/list_commits` and `/create_pr` from GitHub, prompt plus tools goes to the LLM.*

## Skills

The LLM picks `/list_commits`, the server executes it, and the output flows back to be summarized. The payoff is tool discovery without custom integrations or deprecated-API worries — the model still needs native tool calling, since MCP rides on JSON-RPC 2.0. What tools and MCP do *not* supply is **when** to act: your agent does not know your team's conventions or that you prefer `uv` over `pip`.

## The SKILL.md

Skills, from Anthropic, bundle instructions, scripts, and resources into procedural knowledge — the recipe for a recurring task. They work by **progressive disclosure** in three layers: metadata always loaded, instructions on activation, bundled resources on demand. Every Skill needs a `SKILL.md` whose YAML frontmatter holds just a name and description — all the agent sees when judging whether to open it.

## The Bundled Resources

The markdown body holds the instructions, withheld until requested — pure context engineering. Anything larger splits into referenced files.

![Figure 5-34: The agent can choose to run additional files if needed. Those files can](images/fig_05-34_The_agent_can_choose_to_run_additional_f.png)
*Figure: A `meeting_notes` SKILL.md whose numbered steps point out to per-meeting-type format files and an `extract_action_items.py` script, each loaded only when reached.*

## Summary

Table 5-1 quantifies the savings: ==~100 tokens of metadata always resident, under 5,000 for instructions once activated==, bundled files as needed. The chapter's arc: LLMs only signal intent (something else executes); three ways to instill the capability (ICL, SFT, RL); MCP for standardized access; Skills for procedural know-how. TinyAgent now has prompt-based and native tool calling, ready for Chapter 6 where it sequences tools itself.
