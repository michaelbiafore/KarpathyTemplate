# Summary: Emerging Directions in Reasoning Research → Conversation Memory

## Emerging Directions in Reasoning Research

Reasoning has moved past text-only chains of thought. Three frontiers are pushing it forward: reasoning over new modalities (images, audio, video), efficient reasoning that buys the same gains with less compute, and latent-space reasoning where the model thinks in compressed, non-textual representations. (Chapters 51 and 52 share this page; the material is covered once here.)

## Reasoning in Multi-Modal LLMs

An agent's "brain" often has to reason about a screenshot or a web design, not just prose. Multi-modal models extend naturally to reasoning, but without explicit reasoning grounding they underperform. The same toolkit applies — prompting, search against verifiers, SFT, and RL — adapted so the Chain-of-Thought data itself is multi-modal rather than text-only. Multi-modal Chain-of-Thought (MCoT) splits this into two stages: a rationale-generation pass over language plus image, then an answer pass that appends that rationale to the original inputs.

![Figure 3-42: A two-step approach to sample reasoning data using supervised fine-tuning](images/fig_03-42_A_two-step_approach_to_sample_reasoning.png)

*Figure: A "reasoning" LLM first turns image + question into a rationale, which is then fed back alongside the same inputs to a separately fine-tuned "answering" LLM.*

Llava-CoT extends this by using GPT-4o to synthesize 100,000 records across four stages (summary, caption, reasoning, answer) to fine-tune Llama 3.2v. Reason-RFT then mirrors DeepSeek-R1's recipe — SFT to activate reasoning, RL to generalize it — with mathematical, function-based, and discrete-valued rewards.

## Efficient Reasoning

Test-time compute is expensive, so the aim is shorter traces at equal accuracy. The cheapest lever is prompting: Chain-of-Draft keeps each step to roughly five words.

![Figure 3-45: Comparing a standard prompt with Chain-of-Thought and Chain-of-Draft](images/fig_03-45_Comparing_a_standard_prompt_with_Chain-o.png)

*Figure: The three system prompts side by side — Chain-of-Draft is just Chain-of-Thought plus a "minimum draft, 5 words at most" constraint.*

Length can also be trained in. Token-budget-aware models adapt trace length to problem difficulty; RL length rewards favor short correct answers over long ones. Kimi k1.5 warms up its length penalty gradually (it slowed early learning); O1-Pruner scores length against a reference model; L1 is told its budget up front ("think for 30 tokens"). Qwen3 instead offers hybrid reasoning — `/think` and `/no_think` tokens that switch thinking off entirely.

## Reasoning in Latent Space

Explicit Chain-of-Thought lets us hear the model think out loud. Latent-space reasoning internalizes it: hidden states replace visible tokens. Chain-of-Continuous-Thought skips decoding altogether, feeding the last hidden state straight back as the next input, bracketed by `<bot>`/`<eot>` tokens.

![Figure 3-49: Chain-of-Continuous-Thought reasons in latent space by not producing](images/fig_03-49_Chain-of-Continuous-Thought_reasons_in_l.png)

*Figure: Between the begin- and end-of-thought tokens no text is emitted — the last hidden state is recycled as the input embedding until the answer appears.*

CODI distills this: a teacher trained on explicit CoT and a student reasoning only in hidden states are compared, implicitly teaching the chain.

## Summary

The tradeoff is visibility versus efficiency — explicit traces are debuggable, latent ones are cheaper and need not be textual. Chapter 3 overall traced train-time to test-time compute, search against verifiers, and modifying the proposal distribution via SFT and RL. Chapters 4–6 add memory, tools, and planning.

## Memory

LLMs are stateless and forgetful; hosted assistants only appear otherwise because they are augmented.

![Figure 4-1: LLMs without any additional processing are forgetful and will not remember](images/fig_04-01_LLMs_without_any_additional_processing_a.png)

*Figure: Across two sessions the model greets Maarten, then flatly denies having been told his name.*

Memory here means more than conversation: past actions, intermediate steps, and external material like documentation. Deciding what to store, retrieve, and forget is application-specific and shapes agent behavior — it is how agents learn from failures rather than repeating them.

## Types of Memory

Following "Cognitive Architectures for Language Agents," agents use working memory (short-term, essentially the chat history) plus three long-term forms: episodic (past events and outcomes), semantic (world knowledge, often an external database or codebase), and procedural (how-to patterns, held in the system prompt or the weights themselves as parametric memory).

![Figure 4-4: Memory can be divided into four different types when interacting with](images/fig_04-04_Memory_can_be_divided_into_four_differen.png)

*Figure: Working, procedural, episodic, and semantic memory shown as separate load/store paths around the LLM within a single session.*

## Short-Term Memory and Conversation Memory

(Chapters 58 and 59 overlap on page 155; shared material is summarized once.) A TinyAgent without memory, told the authors' names, answers the follow-up with "I do not know what your name is." Every call starts blank. The fix is a `Memory` module — a list of `{role, content}` dicts with `.add()` and `.get_messages()` — whose full history is passed on every request. The agent then answers correctly, but it never truly remembers: it is simply re-told. The ceiling is the context window, which counts input and output tokens together.

![Figure 4-7: The context window defines the maximum number of tokens an LLM can](images/fig_04-07_The_context_window_defines_the_maximum_n.png)

*Figure: A 5-token question and 8-token answer consume 13 of an 8,192-token window — context length is what you use, the window is what you get.*

As history grows it eventually will not fit, truncating answers or blocking the prompt entirely.
