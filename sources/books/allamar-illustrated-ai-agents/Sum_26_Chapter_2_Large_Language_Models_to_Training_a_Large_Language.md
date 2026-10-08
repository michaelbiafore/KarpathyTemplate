# Chapter 2: Large Language Models (Chapters 26-30)

## Chapter 2. Large Language Models

The LLM carries an agent from observation to action, sitting between the user on one side and the environment on the other. A simple information-seeking agent unrolls the loop in four moves: the user asks, the agent calls a web search tool, the retrieved information returns as an observation, and the agent answers.

![Figure 2-2: The agent receives a user’s question (left), calls a web search tool to retrieve](images/fig_02-02_The_agent_receives_a_users_question_left.png)

*Figure: The same agent shown twice across one turn — query in and answer out on the user-interaction band, action out and feedback in on the environment band.*

The chapter splits by audience: Part 1 gives agent developers the intuitions without the machinery; Part 2 covers model internals and training, useful for diagnosing agent failures and selecting models.

## Input and Output Tokens

Language models predict and generate sequences of tokens — words, word pieces, numbers, or punctuation. Input text is tokenized, then the model emits output tokens one at a time until the response completes.

![Figure 2-3: Input text is split into tokens—“flamingos” becomes two tokens (“flamingo”](images/fig_02-03_Input_text_is_split_into_tokensflamingos.png)

*Figure: "Why are flamingos pink?" splits into six input tokens — "flamingos" becomes "flamingo" + "s" — and the model emits output tokens left to right.*

Generation is itself a loop: each generated token is appended to the input and the whole thing is reprocessed to produce the next one. Models that consume their own output this way are **autoregressive**.

## From Language Modeling to Powering Agents

Pre-training yields a *base model*; **post-training** adds the formatting and behaviors an agent needs. Three capabilities matter here. The **system prompt** is a privileged input that shapes behavior before the model sees any user token, letting deployers customize without retraining. **Multi-turn conversation** formats track who said what, giving the model a rudimentary memory. **Tool use** rides on the same format: the model emits a structured call, and the agentic wrapper detects the pattern and invokes the function. Available tools are usually listed in the system prompt.

![Figure 2-6: The LLM responds to a user question by emitting a tool call (web_search](images/fig_02-06_The_LLM_responds_to_a_user_question_by_e.png)

*Figure: A Harmony-style transcript — system prompt, alternating user/assistant turns, then an assistant message addressed `to=web_search` carrying a JSON query.*

## The TinyAgent

The book deliberately uses two local models: **Gemma 3 12B**, which cannot natively reason or call tools, and **Gemma 4 E4B**, trained for agentic tasks. Building reasoning and tool calling by hand via prompting first reveals what the native fields hide.

Everything goes through an **OpenAI-compatible endpoint** (`base_url`, `api_key`, `model`, `messages`), served locally by Ollama. The code adds four primitives: an `LLM` wrapper, a `Response` dataclass (content, reasoning, tool_call, metadata), a `Step` (thought, action, observation, answer), and a `Trajectory` recording steps for debugging. `TinyAgent` now holds the LLM plus stubs for memory, tools, and planning.

## Training a Large Language Model

![Figure 2-7: The two phases of LLM training: pre-training produces a base model, and](images/fig_02-07_The_two_phases_of_LLM_training_pre-train.png)

*Figure: Untrained → base (language modeling) → instruction-tuned (SFT) → trained (RL).*

**Pre-training** is next-token prediction over web text, books, and code — billions of guess-and-correct weight updates. **SFT** trains on prompt-completion pairs, with prompt tokens in context but excluded from the loss. **RLHF** scores responses by human or reward-model preference, pushing toward preferred and away from rejected completions. **RLVR** replaces the human with automated verifiers.

![Figure 2-12: RLVR training on math problems](images/fig_02-12_RLVR_training_on_math_problems.png)

*Figure: A math problem is scored on two verifiable axes — 0.3 format reward for using `<answer>` tags, 0.7 accuracy reward for the right number — and the sum updates the model.*

**GRPO** adds the group: generate several diverse responses per prompt and reward each relative to the group rather than in isolation.
