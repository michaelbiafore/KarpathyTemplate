---
title: "Reinforcement Learning"
chapter_number: 49
page_start: 134
page_end: 139
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Reinforcement Learning

Additionally, the authors applied test-time scaling explorations by controlling test-
time compute in two ways:
- Forcefully terminating the model’s thinking process
•
- Lengthening the thinking process by spending “Wait” multiple times to the
•
generation when it tries to end
Doing so allowed them to explore test-time scaling and the impact it has on perfor‐
mance on various tasks. Figure 3-33 is an annotated figure from their paper illustrat‐
ing this idea of limiting and lengthening the thinking process to explore test-time
scaling.



![Figure 3-33: Continuing the generation allows for more reasoning, which in turn tends](images/fig_03-33_Continuing_the_generation_allows_for_mor.png)

*Figure 3-33: Continuing the generation allows for more reasoning, which in turn tends*


Figure 3-33. Continuing the generation allows for more reasoning, which in turn tends
to increase performance
Going back to OpenAI’s experiment, the s1 paper showed similar results in scaling
test-time compute; more test-time compute resulted in a better performance.
Reinforcement Learning
In Chapter 2, we saw how RLVR uses verifiable rewards to update model weights and
met GRPO as the algorithm DeepSeek used. Here we’ll see what that looks like in
practice and how it produces reasoning behavior as an emergent property.
Reasoning with DeepSeek-R1 Zero
A key stepping stone to DeepSeek-R1 was an experimental variant called DeepSeek-
R1-Zero. It began with the DeepSeek-V3-Base model, but instead of applying
supervised fine-tuning on large reasoning datasets, the authors relied solely on rein‐
forcement learning to enable reasoning behavior.
|
Chapter 3: Reasoning Large Language Models

In their training procedure, they used a custom system prompt that outlined how the
LLM should respond. To do so, the thinking stage was enclosed with <think> and
</think> while the following answer was enclosed with <answer> and </answer> (see
Figure 3-34). Note that the tags are mentioned but not what the reasoning process
itself should look like. That’s for the LLM to figure out during training.



![Figure 3-34: The system prompt used to steer DeepSeek-V3-Base during training](images/fig_03-34_The_system_prompt_used_to_steer_DeepSeek.png)

*Figure 3-34: The system prompt used to steer DeepSeek-V3-Base during training*


Figure 3-34. The system prompt used to steer DeepSeek-V3-Base during training
DeepSeek used the same two rule-based rewards we saw in Chapter 2: an accuracy
reward for arriving at the correct answer, and a format reward for using the <think>
and <answer> tags correctly.
You can see these rewards and the general training process in Figure 3-35. The
algorithm is GRPO, which we covered in Chapter 2.



![Figure 3-35: The training process of DeepSeek-R1-Zero](images/fig_03-35_The_training_process_of_DeepSeek-R1-Zero.png)

*Figure 3-35: The training process of DeepSeek-R1-Zero*


Figure 3-35. The training process of DeepSeek-R1-Zero
Modifying Proposal Distribution
|

Again, note how the rewards state only whether the correct format is used and
whether the output is correct. How it gets there (through reasoning) is something for
the model to figure out.
By providing these indirect rewards related to Chain-of-Thought-like behavior, the
model found that longer and more complex reasoning processes would often lead to
better answers. These results are shown in Figure 3-36, which is an annotated figure
of the paper indicating how the model started to create longer reasoning traces.



![Figure 3-36: An annotated figure from the DeepSeek-R1 paper demonstrating that the](images/fig_03-36_An_annotated_figure_from_the_DeepSeek-R1.png)

*Figure 3-36: An annotated figure from the DeepSeek-R1 paper demonstrating that the*


Figure 3-36. An annotated figure from the DeepSeek-R1 paper demonstrating that the
model learned by itself that longer responses tend to be more accurate
Interestingly, this graph can also be used to reinforce test-time scaling, where the
model scales test-time compute itself through lengthening its response.
The model, however, still had a significant drawback. By skipping over supervised
fine-tuning and going directly to reinforcement learning, the model suffered from
a “cold start” problem. Without any initial guidance, the model started to mix lan‐
guages (e.g., mixing English and French in its reasoning traces) and showed poor
readability because it lacked Markdown formatting to highlight answers for users.
This is an interesting perspective because they assumed that any reasoning trace
should also be readable by users and not merely used to improve its own output.
|
Chapter 3: Reasoning Large Language Models

There is something to say for reasoning that is not comprehensible by users, such as
reasoning in latent space, but we’ll get to this later in this chapter.
DeepSeek-R1
Using the lessons learned from DeepSeek-R1-Zero, the authors come up with the
following five training steps to create DeepSeek-R1:16
1. Cold start prevention
1.
2. Reasoning-oriented reinforcement learning
2.
3. Rejection sampling
3.
4. Supervised fine-tuning
4.
5. Reinforcement learning for all scenarios
5.
In step 1, to prevent the cold start problem, DeepSeek-V3-Base was fine-tuned with
a small but high-quality reasoning dataset containing about 5,000 samples with long
Chain-of-Thought traces (Figure 3-37). This supervised fine-tuning initialization acts
as a reliable starting point to improve readability and monolingual consistency before
the model enters the reinforcement learning training. Let’s call this resulting model
DeepSeek-V3-1 as the intermediate model.



![Figure 3-37: A small supervised fine-tuning step was taken to prevent the cold start](images/fig_03-37_A_small_supervised_fine-tuning_step_was.png)

*Figure 3-37: A small supervised fine-tuning step was taken to prevent the cold start*


Figure 3-37. A small supervised fine-tuning step was taken to prevent the cold start
problem
In step 2, DeepSeek-V3-1 was further fine-tuned using GRPO, much like was done
in DeepSeek-R1-Zero. To further prevent mixing languages in the reasoning traces, a
reward was added to ensure the target language remains consistent (see Figure 3-38).
The resulting model (DeepSeek-V3-2) is a model trained purely for reasoning, much
like DeepSeek-R1-Zero. Like DeepSeek-R1-Zero, this has its pros and cons. Although
the model excels at advanced reasoning tasks, it does not do well on tasks that do
not require extensive reasoning, such as translation or writing tasks. It did, however,
outperform DeepSeek-R1-Zero in most instances that required extensive reasoning
and had similar performance on all others.
16 Guo, Daya et al. 2025. “DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learn‐
ing,” arXiv, 2501.12948.
Modifying Proposal Distribution
|



![Figure 3-38: The training process to create a first version of the reasoning model](images/fig_03-38_The_training_process_to_create_a_first_v.png)

*Figure 3-38: The training process to create a first version of the reasoning model*


Figure 3-38. The training process to create a first version of the reasoning model
In step 3, the reasoning DeepSeek-V3-2 model was used to generate synthetic reason‐
ing data because it excelled at reasoning tasks. A reward model (DeepSeek-V3-Base)
was used to select the high-quality reasoning traces.
To make the model more adept at non-reasoning tasks, such as writing and transla‐
tion, DeepSeek-V3-Base was used to sample mostly non-reasoning data that could be
trained on.
The result was 800,000 samples that contained both reasoning and non-reasoning
data (see Figure 3-39).
|
Chapter 3: Reasoning Large Language Models



![Figure 3-39: Reasoning and non-reasoning traces were sampled to create 800,000 high-](images/fig_03-39_Reasoning_and_non-reasoning_traces_were.png)

*Figure 3-39: Reasoning and non-reasoning traces were sampled to create 800,000 high-*


Figure 3-39. Reasoning and non-reasoning traces were sampled to create 800,000 high-
quality samples
In step 4, this dataset of 800,000 samples was used to perform supervised fine-tuning
of the DeepSeek-V3-Base model. This was done, in part, to resolve the cold start
problem and to expose the model to these kinds of reasoning traces (Figure 3-40).
The resulting model was the first version of DeepSeek-R1.



![Figure 3-40: The first version of DeepSeek-R1 was created through a supervised fine-](images/fig_03-40_The_first_version_of_DeepSeek-R1_was_cre.png)

*Figure 3-40: The first version of DeepSeek-R1 was created through a supervised fine-*


Figure 3-40. The first version of DeepSeek-R1 was created through a supervised fine-
tuning step
Finally, in step 5, reinforcement learning was done on the first version of DeepSeek-
R1 so it could develop its own reasoning traces instead of mimicking them from
the data. However, to align with human preferences, additional reward signals were
added that focused on helpfulness and harmlessness (Figure 3-41). The model was
also asked to summarize the reasoning process to prevent readability issues.
Modifying Proposal Distribution
|