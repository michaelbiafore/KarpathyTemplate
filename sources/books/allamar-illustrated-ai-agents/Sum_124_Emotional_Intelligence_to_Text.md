# Emotional Intelligence through Text (Chapters 124-134)

## Emotional Intelligence

As agents collaborate, *agentic societies* emerge — shared environments where sociality, identity, and theory of mind can arise without assigned tasks. Identity starts as prompting ("Your name is Alex, and you are a software engineer"), but because LLMs train on human data, human psychology partly applies; this field is **AI psychology**. Research shows LLMs doing multi-modal emotion recognition and even creating emotional-intelligence tests, and users with anxious attachment forming emotional dependency on GPT-4. On Theory of Mind, a r/changemyview study found GPT-4's reasoning overlapped human evaluators only ==35%==, rising to ==42%== when the poster's intent, emotion, and sentiment were injected via BERT-like models. Prompting 77 LLMs with "We are…" versus "They are…" showed human social-identity bias transfers too: in-group completions are reliably more positive.

## Simulations

The same page finishes that argument — identity comes from training data, prompting, and interaction alike, and whether the emotional capability is real or accurate mimicry is unclear. That makes anthropomorphizing hard to resist, raising unresolved responsibility questions for mental healthcare use. Simulated environments are where these capabilities actually surface.

## Interactive Simulacra of Human Behavior

A sufficiently accurate simulation becomes a **world model**. The landmark case is "Generative Agents," set in the pixel sandbox of Smallville.

![Figure 8-12: A figure of Smallville, the simulated town used in the paper: “Generative](images/fig_08-12_A_figure_of_Smallville_the_simulated_tow.png)
*Figure: The annotated top-down map of Smallville — houses, cafe, bar, park, college, dorm, stores — the world its 25 agents share.*

Each agent gets a one-paragraph identity plus memory, planning, and reflection. The **memory stream** scores timestamped states on recency, LLM-judged importance, and embedding relevance, distilling thousands into a usable few.

![Figure 8-14: The procedure of MemoryStream for giving memory to the inhabitants of](images/fig_08-14_The_procedure_of_MemoryStream_for_giving.png)
*Figure: A query searches the embedded memory stream, retrieves recent relevant states, then an LLM filters for importance.*

Reflection runs two or three times daily: the 100 latest states yield three salient questions, answered as five insights written back into the stream. Plans carry location, start time, and duration, revised ReAct-style against observations.

![Figure 8-16: The core agentic framework of inhabitants in Smallville](images/fig_08-16_The_core_agentic_framework_of_inhabitant.png)
*Figure: The Perceive → Memory → Plan/Reflect → Retrieve → Act loop driving each inhabitant.*

## Deep Research Agents

Successors include Agent Hospital (doctor agents improve by treating patients) and SimClass. The chapter then pivots to **Deep Research**, the flagship multi-agent use case adopted in 2025 by Anthropic, Perplexity, Google, and OpenAI; Anthropic's splits search agents, a citation agent, and a lead researcher.

## Toward an AI Co-Scientist

Google's AI co-scientist (Gemini 2.0) generates hypotheses judged on plausibility, novelty, testability, and safety. A supervisor orchestrates six specialists: Generation, Reflection, Ranking (Elo-style debate tournaments), Proximity (deduplication), Evolution, and Meta-review.

## Agent Laboratory

![Figure 8-18: The AI co-scientist uses specialized agents to perform its research](images/fig_08-18_The_AI_co-scientist_uses_specialized_age.png)
*Figure: Research goal and user feedback enter a supervisor agent dispatching six specialized agents over a shared context memory.*

Agent Laboratory is more static: three fixed phases — literature review (PhD-student agent querying arXiv), experimentation (plan formulation with a postdoc, data prep over HuggingFace, experiments via the `mle-solver` coding module), and report writing with a professor plus three NeurIPS-style reviewer agents. Autonomy is high *within* steps, zero *across* them.

![Figure 8-22: All phases of the Agent Laboratory](images/fig_08-22_All_phases_of_the_Agent_Laboratory.png)
*Figure: The pipeline as phases, subtasks, and the instructor/assistant agent pairs at each iteration point.*

## Summary

Chapter 8 covered orchestration patterns, frameworks (CAMEL, MetaGPT, AutoGen, LangGraph, CrewAI), A2A as the multi-agent MCP, agent societies, and Deep Research.

## Chapter 9. Multi-Modal Understanding

Real applications are not text-only. **Multi-modal understanding** fuses images, audio, and video with text; MLLMs like GPT-5, Gemini 3.0, and Claude 4.5 are usually the "brain" of agentic systems.

## What Are Multi-Modal LLMs?

Most MLLMs encode input rather than generate non-text output — cheaper, no major architectural change. Four parts: **encoder**, **connector**, **LLM**, and optional **generator**.

![Figure 9-4: Multi-modal understanding typically involves connecting the encoders of](images/fig_09-04_Multi-modal_understanding_typically_invo.png)
*Figure: Image/audio/video pass through encoder and connector into the LLM (understanding, left); a generator on the output side produces non-text modalities (generation, right).*

## Encoding Modalities

Encoding converts any input to embeddings — what the LLM expects — making the encoder the load-bearing first stage.

## Text

Text's encoder is just the tokenizer plus embedding layer of a decoder-only Transformer, which reveals where other modalities attach. But encoding alone is insufficient.

![Figure 9-11: Encoders are trained on specific data, and each encoder will therefore](images/fig_09-11_Encoders_are_trained_on_specific_data_an.png)
*Figure: Image, text, and audio encoders emit embeddings of differing length, range, and precision (FP8, BF16, FP16), so they cannot be compared directly.*

A **projection** model is needed to map every modality onto common dimensions and value distributions.
