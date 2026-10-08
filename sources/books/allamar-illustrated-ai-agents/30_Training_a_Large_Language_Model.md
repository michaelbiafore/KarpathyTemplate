---
title: "Training a Large Language Model"
chapter_number: 30
page_start: 65
page_end: 70
part: "Part 1: What You Should Know About Large Language Models"
---
# Training a Large Language Model

such as reasoning (Chapter 3), memory (Chapter 4), tools (Chapter 5), and planning
(Chapter 6).
Trajectories can get unwieldy quickly when you have dozens of
steps, tool calls, long reasoning, and more. We created a small
helper utility that visualizes these components without seeming
unwieldy. As always, these can be found in the notebook on the
associated GitHub repository. The utility is called the Trajectory
Viewer and is used at the end of each notebook:



![Figure on page 17](images/fig_p017_x95.png)


from illustrated_agents.utils import TrajectoryViewer
TrajectoryViewer(agent.trajectory)
There was a lot of code to explore but it was vital for creating this foundation of LLM,
Response, Step, and Trajectory. These are things that are going to be used quite
often to standardize behavior in your TinyAgent.
What We Built
TinyAgent/
├── agent.py ← Updated (Integrated the `LLM` into your `TinyAgent`)
├── llm.py ← New (An LLM wrapper for local or cloud models)
└── trajectory.py ← New (Step and Trajectory tracking)
Now that you have a working LLM and added it to your TinyAgent, let’s explore how
these models are actually trained!
Training a Large Language Model
LLMs go through two major phases of training: pre-training and post-training (Fig‐
ure 2-7). Pre-training is where they get their name from, because they are trained on
a language processing task called language modeling.



![Figure 2-7: The two phases of LLM training: pre-training produces a base model, and](images/fig_02-07_The_two_phases_of_LLM_training_pre-train.png)

*Figure 2-7: The two phases of LLM training: pre-training produces a base model, and*


Figure 2-7. The two phases of LLM training: pre-training produces a base model, and
post-training applies supervised fine-tuning (SFT) and reinforcement learning (RL) to
produce the final model
Part 1: What You Should Know About Large Language Models
|

Pre-training: language modeling
Language modeling is the task of presenting a model with a sequence of words (or
more precisely, tokens) and asking it to predict the next word that is most likely to
appear. This phase requires vast amounts of data and it takes a major part of the
computing done during the training process.
Pre-training data is drawn from curated mixtures of sources including web text,
books, and code, each filtered to satisfy quality criteria. From this text data, we can
extract different spans of text and use each one as a training example. Say, for exam‐
ple, we handsomely pay O’Reilly Media to license the data on its website describing
our earlier book, Hands-On Large Language Models. As we can see in Figure 2-8, we
can take one span of that text and present it to the model. We hide the last token, give
the model all the previous tokens, and ask it to predict the next word in the sequence.



![Figure 2-8: Pre-training as next-token prediction, where the model attempts to predict](images/fig_02-08_Pre-training_as_next-token_prediction_wh.png)

*Figure 2-8: Pre-training as next-token prediction, where the model attempts to predict*


Figure 2-8. Pre-training as next-token prediction, where the model attempts to predict
the next word in a sentence and updates its weights based on errors
At the start, the model under training would almost always guess incorrectly, which
is part of the process. Now that we have its wrong prediction and the correct word,
we plug them both in our loss calculation and update the weights of the model so
|
Chapter 2: Large Language Models

that next time it has a better chance of making the right prediction. This is done
billions of times and in the end results in a base model. The most famous and
transformational of these is OpenAI’s GPT3, released in 2020. Since then, the later
steps in the training process were widely adopted to lead to a model that requires less
prompt engineering and behaves more in line with how people (and agent scaffolds)
expect it to behave.
Post-training: supervised fine-tuning
Base models have strong latent capabilities, including reasoning, summarization,
translation, and code generation, that often require heavy prompt engineering to
unlock. Post-training helps polish these model behaviors using a much smaller set of
training examples.
The first step of post-training is called supervised fine-tuning (SFT). It is also some‐
times referred to as instruction-tuning because it’s where a model is trained to follow
instructions we give it in prompts.
As we can see in Figure 2-9, an SFT training example is composed of a prompt and
a completion that shows how we want the model to behave if it sees such a prompt.
The update rule is almost identical to that of pre-training. The key difference is that
while prompt tokens are included in the input context, they are excluded from the
loss computation so the model is trained on only the response tokens. This is why
we’ve assigned these tokens different colors and borders in the figure.



![Figure 2-9: SFT trains the model on prompt-completion pairs. The prompt tokens (light](images/fig_02-09_SFT_trains_the_model_on_prompt-completio.png)

*Figure 2-9: SFT trains the model on prompt-completion pairs. The prompt tokens (light*


Figure 2-9. SFT trains the model on prompt-completion pairs. The prompt tokens (light
purple) are fed as context but excluded from the loss; only the completion tokens (dark
purple) are trained on—here, the model predicts “flowers” where “verify” is correct, and
the weights are updated accordingly.
Part 1: What You Should Know About Large Language Models
|

The SFT training phase is essential, yet not enough to produce a cutting-edge model.
It teaches the model to follow instructions, but it cannot fully capture human prefer‐
ences about what makes a response genuinely helpful, accurate, or well-reasoned. The
reinforcement learning step that follows is what pushes the model in that direction.
Post-training: reinforcement learning
Notice how in SFT, we show the model what the desired output looks like. Reinforce‐
ment learning (RL) is a different training methodology that doesn’t require having
a complete targeted response. Instead, we use methods that evaluate the quality of
a model-generated response and update the model’s weights based on that quality
score, called a reward.
One of the most commonly used RL methods in training LLMs is Reinforcement
Learning from Human Feedback (RLHF), which relies on preference scores collected
from humans or specialized models called reward models, themselves often being
LLMs as well.
A single training example in an RLHF step, as shown in Figure 2-10, can be a prompt
and two completions for it: one that is preferred, and another that is rejected.



![Figure 2-10: The model generates multiple completions, which are scored by human](images/fig_02-10_The_model_generates_multiple_completions.png)

*Figure 2-10: The model generates multiple completions, which are scored by human*


Figure 2-10. The model generates multiple completions, which are scored by human
raters or a reward model trained on human preferences, and the model is updated
toward producing higher-scoring responses
The RLHF training objective is to update the model to increase the likelihood of gen‐
erating output like the preferred response and decrease the likelihood of generating
output like the rejected response. This can be used to polish model behaviors such as
|
Chapter 2: Large Language Models

response length, type of language the model uses, safe type of completions to generate
or to avoid, and many other types of behaviors.
The other major RL method widely used in post-training today’s leading LLMs is
Reinforcement Learning with Verifiable Rewards (RLVR). Similar to RLHF, it updates
the model based on a reward score. The difference here is that the rewards can be
obtained from automated ways of verifying the output; for example, if it follows a
certain format, or the final answer it results in is equal to the correct answer (that we
knew beforehand, in the case of math problems, for example). We see a couple of very
basic verifiers in Figure 2-11 that hint at the actual verifiers used in RLVR methods.



![Figure 2-11: With RLVR, correctness is determined automatically by verifiers rather](images/fig_02-11_With_RLVR_correctness_is_determined_auto.png)

*Figure 2-11: With RLVR, correctness is determined automatically by verifiers rather*


Figure 2-11. With RLVR, correctness is determined automatically by verifiers rather
than relying on human preference
We’ll dig deeper into RLVR and various types of verifiers at multiple points in the
book.
The Group Relative Policy Optimization reinforcement learning algorithm
To better grasp the intuitions behind RLVR, we can look at a more specific example
for a model that solves math problems. Let’s say we have a set of math problems and
the final correct answer for each of them. We want to train the model to solve them
correctly and to print the answer in the format <answer>42</answer>, if 42 was the
answer to a specific problem, for example.
In Figure 2-12, we can see an example showing an RL training dataset made up of
math word problems and their answers. In an RLVR training step, we take one of the
problems and pass it to the model with instructions about the format that we want.
Part 1: What You Should Know About Large Language Models
|

Once the model generates its output, we can automatically verify whether it followed
the requested format and if it arrived at the correct solution of the problem. The
model’s response is then scored on two verifiable dimensions: format (did it use the
correct tags?) and accuracy (was the answer right?). The combined reward signal is
used to update the model weights.



![Figure 2-12: RLVR training on math problems](images/fig_02-12_RLVR_training_on_math_problems.png)

*Figure 2-12: RLVR training on math problems*


Figure 2-12. RLVR training on math problems
In this example we had two kinds of rewards, a format reward scoring whether
the model uses the correct format for the output and assigning a reward of 0.3 if
correct or 0 if incorrect. Then there’s an accuracy reward that compares the final
result to the actual result and assigns a reward of 0.7 if correct and 0 if incorrect. In
Chapter 3, we’ll see how this method was used to train DeepSeek-R1, one of the first
open-weight reasoning LLMs.
The Group Relative Policy Optimization (GRPO) algorithm has another key ingre‐
dient beyond reward assignment. Rather than scoring a single response, at each
training step GRPO generates a group of responses for the same prompt using a
temperature setting that ensures diversity among them. Rewards are then computed
relative to this group, reinforcing responses that score higher than the others. This
comparative approach is what the word “group” in the name refers to.
In Figure 2-13, we can see this intuition for a group size of five. We generate five
answers from the model, assign a reward to each one, and use those scores to update
the model.
|
Chapter 2: Large Language Models