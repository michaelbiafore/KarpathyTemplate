---
title: "Reinforcement Learning"
chapter_number: 81
page_start: 221
page_end: 225
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Reinforcement Learning

In the context of SFT, getting quality data for tool calling can
be a challenge. For many prompts, there is not a single correct
tool call. Multiple tools, argument formats, or call sequences
may all lead to valid outcomes. For instance, if we want to
extract the README.md from a given GitHub repository, a model
could call get_readme(repo="owner/repo" or it could use get_con
tents(path="README.md", repo="owner/repo"), both of which
return the same file. Likewise, quality data often assumes that tools
never fail, while in reality, tools may fail, return partial errors,
change schemas, or behave inconsistently. These problems are less
pronounced when using RL, which we cover in the next section.



![Figure on page 17](images/fig_p017_x95.png)


In other words, the original data was adjusted to include tool calls instead of the LLM
generating the answer by itself. All inputs were essentially updated to contain the
appropriate tool.
Finally, the LLM (GPT-J, a variant of GPT-3) was fine-tuned using this updated
data using SFT. At the time, this technique showed significant improvements over
zero-shot performance and competed with larger models. However, SFT on this data
made generalization difficult. SFT tends to be sensitive to the exact wording and
prompt that is being used because it attempts to re-create what it is being shown. As
we will explore next, RL tends to be a much more stable technique for generalization
in tool use.
Reinforcement Learning
As we explored in Chapters 2 and 3, RL is an excellent method of training or
fine-tuning to align your model to certain rewardable tasks. Compared to SFT, where
an LLM trains on fixed examples with the correct answer, RL relies on trial and error.
LLMs, through SFT, tend to mimic the input data and have difficulties generalizing
what they learned. In RL, LLMs develop improved reasoning strategies not from
being told exactly what to do (the mimicking behavior of SFT) but from repeatedly
exploring feedback signals.
In the context of RL for tool usage, tool-learning is often integrated into the thinking
process of models that support advanced reasoning. This is called Tool-Integrated
Reasoning (TIR), which involves incorporating tools into the reasoning traces of
an LLM. Figure 5-20 illustrates this process of calling a tool during reasoning and
continuing the reasoning process after receiving the output.
Tool Learning
|



![Figure 5-20: An overview of Tool-Integrated Reasoning](images/fig_05-20_An_overview_of_Tool-Integrated_Reasoning.png)

*Figure 5-20: An overview of Tool-Integrated Reasoning*


Figure 5-20. An overview of Tool-Integrated Reasoning
Note that such a TIR trajectory might involve multiple tool invocations, where the
final answer is determined by all these intermediate tool calls and outputs.
Although we will delve more deeply into RL in other chapters, let’s explore how it can
be used to enable tool learning and TIR.
ToolRL
A recent example showcasing how RL can be used to enable TIR is ToolRL.9
This framework uses GRPO, which we briefly covered in DeepSeek-R1’s training
procedure in Chapters 2 and 3. To differentiate between stages of thinking, tool
calling, and answering the query, the developers used the <thinking></thinking>,
<tool_call></tool_call>, and <answer></answer> tokens, respectively.
Compared to DeepSeek-R1, their usage of rewards in GRPO is quite straightforward.
Two rewards are defined to enable tool usage:
Correctness
Is a tool called correctly?
9 Qian, Cheng et al. 2025. “ToolRL: Reward Is All Tool Learning Needs,” arXiv, 2504.13958.
|
Chapter 5: Tool Usage, Learning, and Protocols

Scores are given based on whether the correct tool names and parameters were
used.
Format
Is the appropriate format used?
A positive reward is given if all required fields appear in the correct order.
To train the model, 4,000 samples of TIR traces were sampled from various datasets
and used for fine-tuning various Qwen2.5 models.10 Figure 5-21 illustrates how
GRPO was used to fine-tune these models.



![Figure 5-21: The training process of ToolRL](images/fig_05-21_The_training_process_of_ToolRL.png)

*Figure 5-21: The training process of ToolRL*


Figure 5-21. The training process of ToolRL
Interestingly, the authors also experimented with length rewards to encourage longer
reasoning traces but found that longer traces do not consistently improve task perfor‐
mance and may even harm smaller models. Long reasoning traces might therefore
not be ideal for tool use tasks.
Note that GRPO is a very flexible framework and allows you to develop the rewards
that are best suited for a given use case. As such, this strategy of using tool-based
rewards in GRPO can also be used for non-reasoning models by simply removing or
updating the format reward.
10 Yang, An et al. 2024. “Qwen2.5 Technical Report,” arXiv, 2412.15115.
Tool Learning
|

Search-R1
To further explore what RL is capable of, let’s take a closer look at Search-R1, an
efficient RL framework for integrating search as a tool into an LLM’s reasoning
process.11 In this framework, the LLM learns to generate one or more search queries
during step-by-step reasoning autonomously.
The framework starts with specifying how the model should interleave reasoning
with the search engine call. As illustrated in Figure 5-22, the prompt template is
structured into three parts. First, the reasoning traces are created with <think></
think> tokens, then the search engine calling function with <search></search>
where the output is reintegrated with <information></information>, and finally, the
answer through <answer></answer> tokens. Note that the reasoning traces and the
search engine can be interleaved several times.



![Figure 5-22: The system prompt of Search-R1](images/fig_05-22_The_system_prompt_of_Search-R1.png)

*Figure 5-22: The system prompt of Search-R1*


Figure 5-22. The system prompt of Search-R1
What makes this template particularly interesting is that the authors focus on a single
tool, search. The reason for this was the upcoming popularity of DeepResearch, a
framework where reasoning LLMs are coupled with search engines to create agentic
systems that allow for in-depth research on various topics. The authors of Search-R1
created this framework as a strong open source alternative to the proprietary systems
out there.
The result of such a template is, like ToolRL, tool-interleaved reasoning with multi-
turn search engine calls. We illustrated an example of such a process in Figure 5-23.
Note that the <search></search> tool can be any application, like the open-access
archive of academic papers, arXiv, or a combination of various sources.
11 Jin, Bowen et al. 2025. “Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforce‐
ment Learning,” arXiv, 2503.09516.
|
Chapter 5: Tool Usage, Learning, and Protocols



![Figure 5-23: Examples of tool-interleaved reasoning with multi-turn search engine calls](images/fig_05-23_Examples_of_tool-interleaved_reasoning_w.png)

*Figure 5-23: Examples of tool-interleaved reasoning with multi-turn search engine calls*


Figure 5-23. Examples of tool-interleaved reasoning with multi-turn search engine calls
The approach of training the algorithm with RL is rather straightforward. The
authors adopted a simplified outcome-based reward function. Instead of creating
all different kinds of formatting and accuracy rewards (like DeepSeek-R1), only accu‐
racy rewards were used (based on the task). Since the underlying model (Qwen2.5)
already has strong structural adherence, there was no need for formatting rewards.
Among others, the authors explored GRPO (which we covered in Chapter 2) as the
RL algorithm (illustrated in Figure 5-24) for fine-tuning the model. Note that the
losses in GRPO are typically calculated over the entire sequence of tokens, including
the output of the search engine. In Search-R1, the tokens of the search engine’s
output were masked (ignored) to prevent the model from attempting to control the
search engine’s output, which were not directly LLM-generated (which can create
unexpected dynamics). This is called loss masking for retrieved tokens.
Tool Learning
|