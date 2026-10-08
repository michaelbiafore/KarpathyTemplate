---
title: "Scaling Laws"
chapter_number: 40
page_start: 109
page_end: 113
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Scaling Laws

In other words, it is giving the reasoning LLM more time to “think” (see Figure 3-9).



![Figure 3-9: Generally, the more computational resources are spent generating the answer,](images/fig_03-09_Generally_the_more_computational_resourc.png)

*Figure 3-9: Generally, the more computational resources are spent generating the answer,*


Figure 3-9. Generally, the more computational resources are spent generating the answer,
the better the performance
To sum up, train-time compute focuses on scaling resources (e.g., data and compute)
spent during pre-training and post-training, while test-time compute focuses on
scaling resources (e.g., compute) spent during inference (Figure 3-10).



![Figure 3-10: The switch from train-time compute to test-time is a focus toward inference](images/fig_03-10_The_switch_from_train-time_compute_to_te.png)

*Figure 3-10: The switch from train-time compute to test-time is a focus toward inference*


Figure 3-10. The switch from train-time compute to test-time is a focus toward inference
instead of primarily focusing on the pre-training and fine-tuning stages
The question remains: “Why has there been a paradigm shift from scaling train-time
compute to test-time compute?” Let’s look at scaling laws to answer this question.
Scaling Laws
The relationship between a model’s scale (e.g., compute, dataset size, and parameter
counts) and its performance is described by scaling laws. They often take the form
of power laws, where increasing one variable (e.g., compute) leads to a proportional
change in another (e.g., performance).
In these power laws, these relationships tend to follow diminishing returns: each
doubling of compute gives smaller gains than the previous doubling.
The Paradigm Shift from Train-Time Compute to Test-Time Compute
|

When plotted on regular axes, this creates a curve that flattens out. But when both
axes are put on a log-log scale, the power-law relationship becomes a straight line,
making trends easier to see and compare across many orders of magnitude (see
Figure 3-11).



![Figure 3-11: A normal scale, shown on the left, has difficulty demonstrating the relation‐](images/fig_03-11_A_normal_scale_shown_on_the_left_has_dif.png)

*Figure 3-11: A normal scale, shown on the left, has difficulty demonstrating the relation‐*


Figure 3-11. A normal scale, shown on the left, has difficulty demonstrating the relation‐
ship between compute and performance at larger values compared to the log-log scale on
the right
The most influential scaling laws in train-time compute are the Kaplan and Chin‐
chilla scaling laws.2,3
Jared Kaplan found that a model’s performance improves predictably as you increase
compute, dataset size, and parameters, but with diminishing returns. It follows the
same power-law form just described. For a fixed compute budget, the best strategy
was to keep increasing the model size and train on as much data as possible without
overfitting. Figure 3-12 is an annotated image from Kaplan’s paper detailing this rela‐
tionship. Note that a balance is important between data, parameters, and compute.
Following Kaplan’s finding, the Chinchilla scaling law demonstrated similar findings
and reinforced these power-law relationships. However, they showed that models
were often undertrained and that for a fixed compute budget, it’s better to use a
smaller model and train it on much more data.
2 Kaplan, Jared et al. 2020. “Scaling Laws for Neural Language Models,” arXiv, 2001.08361.
3 Hoffmann, Jordan et al. 2022. “Training Compute-Optimal Large Language Models.” arXiv, 2203.15556.
|
Chapter 3: Reasoning Large Language Models



![Figure 3-12: A balance between the used compute, number of tokens, and parameters](images/fig_03-12_A_balance_between_the_used_compute_numbe.png)

*Figure 3-12: A balance between the used compute, number of tokens, and parameters*


Figure 3-12. A balance between the used compute, number of tokens, and parameters
tends to give the best performance according to Kaplan’s scaling laws
Both laws suggest that all three factors (compute, data, and model size) should be
scaled up in tandem for optimal performance.
However, these power laws state that at some point there will be diminishing returns,
which is what the field of LLM research started to see throughout 2024. Although
compute, data, and model sizes have steadily grown, the gains have not grown
linearly with them. As shown in Figure 3-13, we had likely reached a limit. Note
that this assumes that there are no major architectural improvements to the models.
Performance of models can be improved with things other than compute, data, and
model sizes.



![Figure 3-13: The normal scale demonstrates how there continuously needs to be more](images/fig_03-13_The_normal_scale_demonstrates_how_there.png)

*Figure 3-13: The normal scale demonstrates how there continuously needs to be more*


Figure 3-13. The normal scale demonstrates how there continuously needs to be more
computing to get the same rise in performance
The Paradigm Shift from Train-Time Compute to Test-Time Compute
|

This meant that researchers had to look elsewhere. Unsurprisingly, test-time compute
turned out to be a prime candidate to continue scaling LLMs. Although scaling laws
for test-time compute are relatively unexplored, there are several interesting sources
comparing scaling train-time compute with test-time compute.
First, a post by OpenAI detailed that increasing test-time compute might affect
performance the same as increasing train-time compute. They defined the train-time
compute as more reinforcement learning (RL), and the test-time compute as more
time spent thinking.
Figure 3-14 is an annotated image from the OpenAI post showcasing similar relation‐
ships. Note how OpenAI suggests that test-time compute might scale even further
than train-time compute.



![Figure 3-14: The left graph demonstrates increasing train-time compute, and the right](images/fig_03-14_The_left_graph_demonstrates_increasing_t.png)

*Figure 3-14: The left graph demonstrates increasing train-time compute, and the right*


Figure 3-14. The left graph demonstrates increasing train-time compute, and the right
graph demonstrates increasing test-time compute, suggesting that test-time compute
might scale similarly to train-time compute (from OpenAI)
|
Chapter 3: Reasoning Large Language Models

Second, “Scaling Scaling Laws with Board Games” an interesting paper by Andy L.
Jones,4 explores AlphaZero and trains it to various degrees of compute to play a board
game called Hex.5 Hex is a two-player board game in which players take turns placing
stones on a hexagonal grid to form a path between opposite sides of the board before
the opponent does. AlphaZero is a deep neural network that uses a tree-based search
method to consider the moves it can take in this game of Hex.
In Jones’ research, train-time compute was identified as increasing the number of
parameters in their model and training for more epochs. In contrast, test-time com‐
pute was defined as considering more solutions by scaling the depth of their tree
search. An overview of both is given in Figure 3-15.



![Figure 3-15: AlphaZero was trained to play Hex through reinforcement learning that](images/fig_03-15_AlphaZero_was_trained_to_play_Hex_throug.png)

*Figure 3-15: AlphaZero was trained to play Hex through reinforcement learning that*


Figure 3-15. AlphaZero was trained to play Hex through reinforcement learning that
allowed for scaling both train-time compute and test-time compute
Their results showed that both forms of compute are tightly related. As shown in the
annotated Figure 3-16, each dotted line represents the minimum compute needed to
reach a given Elo score. Elo is a rating system commonly used in chess that estimates
a player’s strength based on their past results. The figure suggests that, for a target
Elo score, train-time compute and test-time compute should be kept in balance. To
maintain the same score, a decrease in one form of compute should be offset by
an increase in the other. Likewise, for the best performance, both forms of compute
should be increased together.
Research in scaling laws for test-time compute all point to the significant benefit of
scaling test-time compute. As a result, a paradigm shift happened in 2024 and 2025
toward reasoning models that focus on using more test-time compute. Through this
paradigm shift, instead of focusing purely on train-time compute (pre-training and
fine-tuning), these reasoning models instead balance training with inference.
4 Jones, Andy L. 2021. “Scaling Scaling Laws with Board Games,” arXiv, 2104.03113.
5 Silver, David et al. 2018. “A General Reinforcement Learning Algorithm That Masters Chess, Shogi, and Go
Through Self-play,” Science, 362.6419:1140-1144.
The Paradigm Shift from Train-Time Compute to Test-Time Compute
|