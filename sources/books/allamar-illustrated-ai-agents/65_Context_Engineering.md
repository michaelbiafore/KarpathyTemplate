---
title: "Context Engineering"
chapter_number: 65
page_start: 181
page_end: 185
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Context Engineering

(e.g., arXiv) will clarify that the specific pigments are carotenoid pigments, which are
commonly found in brine shrimp.
This iterative process of querying information and compressing it within its reason‐
ing process allows the model to reason about information when it is retrieved rather
than stuffing all potential relevant information in the context.
Context Engineering
We have explored various types of memory that we can use to provide additional
context to the agent, including semantic memory, working memory, and other forms
of memory. However, there might be more forms of context that we could give to the
agent, such as the following:
System prompt
The core context and rules for the agent, which define how it should behave
(procedural memory)
Conversation history
Both the conversation between the user and assistant, but also the LLM’s internal
thoughts (working memory)
Past experiences
Storing specific events, actions, or observations from tool use or user-related
facts (episodic memory)
Retrieved information
External information that is typically stored in a vector database and accessed
through RAG-like techniques (semantic memory)
This is not an exhaustive list, however. As the fields of LLMs and agents grow, so do
the sources of information that we could give to them. As such, we can provide the
agent with all kinds of information sources to produce the answer that we want. As
illustrated in Figure 4-27, the user’s query or prompt is a subset of the LLM’s entire
context.
Context Engineering
|



![Figure 4-27: A non-exhaustive overview of the kinds of information that can be put into](images/fig_04-27_A_non-exhaustive_overview_of_the_kinds_o.png)

*Figure 4-27: A non-exhaustive overview of the kinds of information that can be put into*


Figure 4-27. A non-exhaustive overview of the kinds of information that can be put into
an LLM
This context is given to the LLM, which in turn produces a list of tokens. As such,
we can view an LLM as a function that takes several tokens (context), processes them,
and outputs tokens. To optimize the output tokens for a given task, we can either
optimize the LLM itself by training or fine-tuning it, or we can optimize the input,
namely the context (see Figure 4-28).



![Figure 4-28: To create better outputs, we can either optimize the input tokens or create](images/fig_04-28_To_create_better_outputs_we_can_either_o.png)

*Figure 4-28: To create better outputs, we can either optimize the input tokens or create*


Figure 4-28. To create better outputs, we can either optimize the input tokens or create
better LLMs. In this context, the LLM can be seen as part of a function to optimize.
To optimize the quality of the output (the output tokens), we can either optimize
the LLM itself by training or fine-tuning it, or we can optimize what goes into the
LLM, namely, the context. The act of optimizing input tokens so they produce the
best possible output is called context engineering. Formally, it is finding the best
context such that it maximizes the quality of the LLM’s output for a given task.9
As illustrated in Figure 4-29, where prompt engineering involves optimizing the
system/user prompts, context engineering aims to optimize the entire context.
9 Mei, Lingrui et al. 2025. “A Survey of Context Engineering for Large Language Models,” arXiv, 2507.13334.
|
Chapter 4: Memory



![Figure 4-29: Prompt engineering involves giving the most relevant pieces of information](images/fig_04-29_Prompt_engineering_involves_giving_the_m.png)

*Figure 4-29: Prompt engineering involves giving the most relevant pieces of information*


Figure 4-29. Prompt engineering involves giving the most relevant pieces of information
to the LLM
Context windows have grown larger, to the point where Google’s Gemini 1.5 already
reached a context window of a million tokens in February 2024. It would be natural
to conclude that context engineering means attempting to fill up this humongous
context window with all kinds of information that relates to the task at hand. More‐
over, there would be no more need for RAG because the context window is large
enough to potentially hold your entire database.
A common benchmark for evaluating long-context LLMs in 2023 and early 2024 was
the needle-in-a-haystack (NIAH) test.10 The test is rather straightforward; a random
fact (needle) is placed somewhere in the middle of a long context window (haystack),
and the model is asked to retrieve this statement. By iterating over different places
and context lengths, we can measure how well LLMs perform over long contexts. It
produced nice-looking visuals and was used by large LLM providers, like Anthropic’s
Claude 2.1 and Google’s Gemini 1.5.11,12
An example of such a visual is shown in Figure 4-30, which illustrates the results for
a typical needle-in-a-haystack test, where the upper-right quadrant (needle at the top
of the document and large context length) shows the degradation of LLMs at higher
context lengths.
10 Kamradt, Gregory. 2023. “Needle in a Haystack–Pressure Testing LLMs,” GitHub, https://github.com/gkam
radt/needle-in-a-haystack.
11 Anthropic. 2023. “Long Context Prompting for Claude 2.1,” Blog post, https://www.anthropic.com/index/
claude-2-1-prompting.
12 Gemini Team Google et al. 2024. “Gemini 1.5: Unlocking Multimodal Understanding Across Millions of
Tokens of Context,” arXiv, 2403.05530.
Context Engineering
|



![Figure 4-30: An artificial example of a typical needle-in-a-haystack test. In this example,](images/fig_04-30_An_artificial_example_of_a_typical_needl.png)

*Figure 4-30: An artificial example of a typical needle-in-a-haystack test. In this example,*


Figure 4-30. An artificial example of a typical needle-in-a-haystack test. In this example,
the accuracy of retrieval decreases as the context window is filled, with information in
the middle of the context being more difficult to retrieve accurately.
However, finding the needle is merely a retrieval task and is not indicative of more
complex forms of long-context understanding, such as reasoning over hundreds of
thousands of tokens. This holds especially true for agents that have to take into
account many forms and lengths of context, like semantic and working memory.
Other benchmarks, like the RULER benchmark,13 have since been released that intro‐
duce new tasks like multi-hop tracing and aggregation to test behaviors beyond sim‐
ple retrieval. The RULER paper, for instance, demonstrated models that performed
well on the needle-in-a-haystack test, all showed significant performance drops as
the context length increased when applied to the RULER benchmark. Many others
(e.g., Li, Tianle et al. 2024 and Levy, Mosh et al. 2024)14,15 found similar results and
concluded that arbitrarily filling up the context window of LLMs would hurt perfor‐
mance. Some even called it “context rot,”16 showcasing the importance of adding
quality information. Moreover, even if the entire context window is filled with quality
13 Hsieh, Cheng-Ping et al. 2024. “RULER: What’s the Real Context Size of Your Long-Context Language
Models?” arXiv, 2404.06654.
14 Li, Tianle et al. 2024. “Long-Context LLMs Struggle with Lng In-Context Learning,” arXiv, 2404.02060.
15 Levy, Mosh et al. 2024. “Same Task, More Tokens: The Impact of Input Length on the Reasoning Performance
of Large Language Models,” arXiv, 2402.14848.
16 Hong, Kelly et al. “Context Rot: How Increasing Input Tokens Impacts LLM Performance,” Chroma, July 2025.
https://research.trychroma.com/context-rot.
|
Chapter 4: Memory

information, it’s often hard for LLMs to shift through all pieces of information. This
might change as LLM capabilities grow but still requires knowing that all information
provided is vital. As such, there is a need to carefully construct and manage the
model’s context window, thereby pointing to the importance of context engineering.
Cost and latency are other reasons for managing the context window. You could
theoretically stuff everything in a 2-million-token context length, like your entire
external database, the full conversation history, some additional examples, etc. How‐
ever, the agent’s LLM has to process all these tokens, which significantly increases
latency. Costs also increase, considering more VRAM is needed when you increase
the context length. Just dumping everything in the context is, therefore, a recipe for
failure.
With context engineering, we aim to optimize the model’s context window with the
right information, at the right place, and in the right format. It’s the act of giving
the LLM the appropriate context without overwhelming it. As such, and as shown in
Figure 4-31, it’s not about filling up the context window, but strategically choosing
and placing information. Going back to our “LLM is a function” analogy, it’s about
optimizing the list of input tokens so that it produces the best possible output tokens.



![Figure 4-31: Context engineering involves strategically placing only the most relevant](images/fig_04-31_Context_engineering_involves_strategical.png)

*Figure 4-31: Context engineering involves strategically placing only the most relevant*


Figure 4-31. Context engineering involves strategically placing only the most relevant
information in the context
You don’t want too much or too irrelevant information because the costs of compute
go up and the performance goes down. Likewise, if you give the LLM too little con‐
text and in an inefficient form, it will operate without having a good understanding
of the context. It’s a careful balance of providing just enough relevant information
to the LLM to have it perform optimally. In other words, context engineering is
largely an architectural problem that needs to be solved with lots of moving parts, like
efficiently tracking, storing, and retrieving all existing and created information.
To help with context engineering, existing techniques for handling memory that
focus on efficiency can be used. MemoryBank, for instance, dynamically adjusts
the importance of memories and keeps only those that are truly important for the
Context Engineering
|