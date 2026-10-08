---
title: "Self-Improvement"
chapter_number: 96
page_start: 274
page_end: 279
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Self-Improvement

Self-Improvement
Reflecting on its behavior is the first step to the continuous self-improvement of
agents, and although prompt-level heuristics are an important component, more
fundamental changes are needed to guide agents toward continual self-improvement.
To create this self-sustaining loop of reflection, reasoning, and task generation, RL
has been shown to enable seemingly unbounded self-improvement with limited need
for human-labeled data.
There have been initial approaches attempting to mimic or use RL by iterating over
attempts and updating policies, such as RISE,16 which includes additional introspec‐
tion steps to continuously improve outputs. More recent approaches, like R-ZERO
and TTRL, generate their own training data and use RL to continuously self-improve
and evolve as it critiques and improves its own output. Let’s explore these methods to
get an understanding of how RL can be used for continuous self-improvement.
Test-time reinforcement learning
Labeled data for agentic traces that generalize well to other experiences is hard
to create and generally a costly task, as it requires significant manual labor. This
motivates the need for LLMs to learn by themselves rather than being directed purely
by labeled data. The idea of self-play and self-experience is central in RL but often
requires supervised data (such as query/reasoning/answer triplets) that are difficult to
collect for complex and large-scale real-world tasks. This poses a substantial barrier
to the self-improvement of LLMs.
Test-Time Reinforcement Learning (TTRL) is a framework that proposes to update
models at test-time using RL.17 Instead of having models remain static entities dur‐
ing inference, TTRL allows LLMs to learn as they interact with their environment
without the need for supervised data. Instead of learning through their memory
modules, their parameters are updated using RL.
TTRL is a four-step process. First, given a query, it applies repeated sampling to
generate several candidate outputs. The authors generated 16 responses per query
using a temperature of 0.6 to make sure that the outputs differ sufficiently. In
their experiments, they used models from several model families, including Qwen
(e.g., Qwen2.5-7B), LLaMA (e.g., LLaMA-3.1-8B-Instruct), Mistral (e.g., Mistral-8b-
Instruct-2410), and DeepSeek (e.g., DeepSeek-R1-LLaMa-8B). Second, a majority
voting strategy is used to select the best answer among the 16 generated outputs.
Third, a reward is generated based on the alignment between the voted output
16 Qu, Yuxiao et al. 2024. “Recursive Introspection: Teaching Language Model Agents How to Self-Improve,”
Advances in Neural Information Processing Systems, 37: 55249-55285.
17 Zuo, Yuxin et al. 2025. “TTRL: Test-Time Reinforcement Learning,” arXiv, 2504.16084.
|
Chapter 6: Planning and Reflection

and the 16 generated outputs. Finally, the calculated rewards are used as a signal
during RL (GRPO) to improve the model as it acts with its environment. Figure 6-21
demonstrates this process of sampling, majority vote, and calculating the reward.



![Figure 6-21: In Test-Time Reinforcement Learning (TTRL), GRPO is used on the sam‐](images/fig_06-21_In_Test-Time_Reinforcement_Learning_TTRL.png)

*Figure 6-21: In Test-Time Reinforcement Learning (TTRL), GRPO is used on the sam‐*


Figure 6-21. In Test-Time Reinforcement Learning (TTRL), GRPO is used on the sam‐
pled answers. The most frequent answer is used as a signal for training.
As you might have noticed, we already covered each of these steps in some form
over the previous chapters. Majority voting is a common strategy for scaling test-time
compute and improving the outputs, whereas GRPO has been a popular strategy
for supervised RL. Elegantly combining these techniques allows TTRL to learn as it
interacts with its environment without the need for labeled data since it produces
those itself (the calculated rewards).
However, majority voting strategies are not flawless by definition. The majority does
not always need to be correct. The authors argue that rewards in RL can be vague to
a certain extent, as they signal the need for further exploration instead of continuous
exploitation, which prevents models from being stuck in local minima. Likewise, even
if the majority is incorrect and no correct predictions are made at all, then the reward
will still be negative. This is referred to as a “lucky hit,” and although they were
created from an incorrect process, they are still “correct” rewards. This is illustrated in
Figure 6-22.
Agents That Continuously Improve
|



![Figure 6-22: Lucky hits in TTRL are correct signals despite the most frequent answer](images/fig_06-22_Lucky_hits_in_TTRL_are_correct_signals_d.png)

*Figure 6-22: Lucky hits in TTRL are correct signals despite the most frequent answer*


Figure 6-22. Lucky hits in TTRL are correct signals despite the most frequent answer
being incorrect
Due to this elegant technique, TTRL can apply on-the-fly adaptation by fine-tuning
the model as it encounters new problems. It is essentially an online approach to RL
focused on learning during inference.
R-Zero
The idea of self-evolving reasoning LLMs without labeled data was further explored
in R-Zero.18 This technique uses two independent models with distinct roles to
coevolve and challenge each other’s outputs. These models are initialized from the
same base model and take on the roles of a Challenger and a Solver. The authors
experimented with models from the Qwen3 family and the Llama-3.1 family.19,20
The Challenger is tasked with generating synthetic queries that are difficult for the
Solver to solve. The Solver generates multiple answers and selects the best one using
majority voting, much like is done with TTRL. During this process, the Challenger is
trained with RL (GRPO) based on the rewards it receives from the Solver.
There are several rewards/signals created during this process:
18 Huang, Chengsong et al. 2025. “R-Zero: Self-Evolving Reasoning LLM from Zero Data,” arXiv, 2508.05004.
19 Yang, An et al. 2025. “Qwen3 Technical Report,” arXiv, 2505.09388.
20 Dubey, Abhimanyu et al. 2024. “The Llama 3 Herd of Models,” arXiv, 2407.
|
Chapter 6: Planning and Reflection

Uncertainty reward (a value between 0 and 1)
This indicates how certain the Solver is that it has created the correct answer
frequently from all of its sampled answers. It is essentially the fraction of the
Solver’s responses that match the most common answer. This reward aims to
guide the Challenger to create difficult but solvable queries.
Repetition penalty (a value between 0 and 1)
This penalty makes sure that the Challenger generates diverse queries. Otherwise,
it would be stuck continuously optimizing the same difficult queries.
Format reward (either 0 or 1)
A reward given based on whether the Challenger generates queries between
<question> and </question> tags.
Composite reward (a value between 0 and 1)
A reward given to the Challenger by subtracting the repetition penalty from the
uncertainty reward and making sure it does not go below 0.
During this process, the Challenger is trained while the Solver is frozen and merely
used as a reward model when fine-tuning the Challenger. This process is illustrated in
Figure 6-23.



![Figure 6-23: The Challenger is trained by trying to give the Solver more difficult queries.](images/fig_06-23_The_Challenger_is_trained_by_trying_to_g.png)

*Figure 6-23: The Challenger is trained by trying to give the Solver more difficult queries.*


Figure 6-23. The Challenger is trained by trying to give the Solver more difficult queries.
The signal it gets is whether it can generate a difficult query.
Agents That Continuously Improve
|

After training the Challenger, a dataset of queries is sampled from the Challenger to
train the Solver. For each query, answers are sampled by passing them through the
Solver. Based on a majority vote, if the query is too difficult (too few correct answers)
or if the query is too easy (almost all answers are correct), then they are filtered out.
This process improves the quality of the training data by focusing on queries that are
just difficult enough.
The Solver is then fine-tuned on the curated dataset of challenging queries. As before,
GRPO is used for training. Compared to the Challenger, the reward is simplified to a
value of either 0 or 1. Like TTRL, this verifiable reward for each correct answer and 0
otherwise. As shown in Figure 6-24, this is a much simpler process and akin to TTRL.



![Figure 6-24: The Solver is trained by attempting to solve the Challenger’s query. The](images/fig_06-24_The_Solver_is_trained_by_attempting_to_s.png)

*Figure 6-24: The Solver is trained by attempting to solve the Challenger’s query. The*


Figure 6-24. The Solver is trained by attempting to solve the Challenger’s query. The
signal it gets during training is whether it can solve a difficult query.
Together, this creates a coevolving system where the Challenger continuously makes
harder queries, and the Solver gets better at solving them. In turn, the Challenger
adapts to make new challenging queries, and so on. The beauty of this system is
that the Challenger gets continuous rewards (composite uncertainty scores from 0 to
1. to encourage generating queries at the edge of difficulty, while the Solver gets a
binary reward (0 or 1) to encourage getting the answer exactly right. This asymmetry
allows the Challenger to explore a range of difficulties, while the Solver should be
precise and deterministic in its answers. This loop between the Challenger and Solver
training is shown in Figure 6-25.
|
Chapter 6: Planning and Reflection



![Figure 6-25: Challenger and Solver training are done after each other. In this process, the](images/fig_06-25_Challenger_and_Solver_training_are_done.png)

*Figure 6-25: Challenger and Solver training are done after each other. In this process, the*


Figure 6-25. Challenger and Solver training are done after each other. In this process, the
Solver and Challenger each try to win and are incentives to create competition.
Methods such as TTRL and R-Zero are, at the time of writing, newer techniques that
have tremendous potential for self-improving agents. These are potential paradigm
shifts that move the training focus toward unlabeled data and inference rather than
purely focusing on the traditional pre-training combined with SFT and RL. The
evolution from “traditional” training with SFT and RL all the way to this potential
test-time training paradigm is shown in Figure 6-26.
Agents That Continuously Improve
|