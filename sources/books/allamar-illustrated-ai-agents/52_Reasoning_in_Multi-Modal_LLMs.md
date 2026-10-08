---
title: "Reasoning in Multi-Modal LLMs"
chapter_number: 52
page_start: 142
page_end: 144
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Reasoning in Multi-Modal LLMs

As such, any training and fine-tuning that we saw before can now be enabled by
the prompt template of that specific model. Instead of needing to use “tricks” like
Chain-of-Thought, the model was trained on Chain-of-Thought examples instead.
Emerging Directions in Reasoning Research
Reasoning in LLMs has started to advance beyond text-only reasoning, now using
new modalities, improved architectures, and more abstract ways of representing
information.
In this section, we look at three key areas pushing LLM reasoning forward:
Reasoning in multi-modal LLMs
Reasoning LLMs learn to reason with modalities other than text, like images,
audio, and video
Efficient reasoning
Focuses on improving reasoning while using less computation
Reasoning in latent space
Models think in compressed, abstract forms and often non-textual forms to reach
deeper insights
Reasoning in Multi-Modal LLMs
The LLMs serving as the main brains of agentic systems do not only need to reason
about text. They may need to think about the best way to design a website or interpret
what is happening in a given picture. This requires reasoning in ways that differ from
textual inputs as more modalities might be processed. As we will discuss in Chapter 9,
there are many methods for making LLMs multi-modal, which often naturally extend
them to include reasoning behavior. However, without any reasoning grounding,
performance on multi-modal reasoning tasks is usually worse.
As with mono-modal LLMs, reasoning is often enhanced through methods like those
we discussed before, such as prompting, search against verifiers, or modifying the
proposal distribution with supervised fine-tuning and/or reinforcement learning.
A common method for multi-modal prompting is called Multi-modal Chain-of-
Thought (MCoT). Multi-modal Chain-of-Thought, compared to traditional Chain-
of-Thought, attempts to incorporate text and vision into a two-stage framework.
As shown in Figure 3-42, Multi-modal Chain-of-Thought contains a two-step
approach where the first step creates reasoning by combining the original language
and visual input to produce an explicit reasoning process. In the second step, this
rationale is appended to the original language input and, together with the same
visual input, is used to infer the final answer. Both stages use models with the
|
Chapter 3: Reasoning Large Language Models

same architecture, trained separately on annotated rationale and answer data using
supervised fine-tuning.



![Figure 3-42: A two-step approach to sample reasoning data using supervised fine-tuning](images/fig_03-42_A_two-step_approach_to_sample_reasoning.png)

*Figure 3-42: A two-step approach to sample reasoning data using supervised fine-tuning*


Figure 3-42. A two-step approach to sample reasoning data using supervised fine-tuning
Making vision language models reason step-by-step through supervised fine-tuning
was further covered in Llava-Chain-of-Thought. Here, the authors used GPT-4o to
create synthetic data based on input images through four reasoning stages: summary,
caption, reasoning, and answer. These four structured reasoning stages allow for
the separation of thinking types and help the model to prevent errors in thinking.
As shown in Figure 3-43, this annotated dataset of 100,000 records is then used to
fine-tune Llama 3.2v, a vision LLM.



![Figure 3-43: Llava-Chain-of-Thought was trained using generated data](images/fig_03-43_Llava-Chain-of-Thought_was_trained_using.png)

*Figure 3-43: Llava-Chain-of-Thought was trained using generated data*


Figure 3-43. Llava-Chain-of-Thought was trained using generated data
Emerging Directions in Reasoning Research
|

Following this two-step supervised fine-tuning approach is Reason-RFT, a reinforce‐
ment fine-tuning approach for visual reasoning that follows the two-step approach
of DeepSeek-R1 quite closely. Its two-step approach is meant to go from a base
vision LLM to a reasoning vision LLM. The first step is supervised fine-tuning
with Chain-of-Thought that activates the reasoning capabilities of the vision LLM.
The second step uses reinforcement learning to further generalize the learned reason‐
ing capabilities. Compared to DeepSeek-R1, which included coding-based accuracy
rewards, Reason-RFT focuses on three types of rewards (Figure 3-44):
Mathematical
Scores numerical answers and gives larger scores for exact matches and lower
scores for small errors
Function-based
Compares predicted and target transformation steps, rewarding exact, partial,
and function-only matches with different weights, e.g., rotate(cube, 90°) versus
rotate(cube, 45°)
Discrete-valued
Uses binary scoring for categorical or integer answers, giving credit only for exact
matches



![Figure 3-44: A two-step approach of supervised fine-tuning using the reasoning traces](images/fig_03-44_A_two-step_approach_of_supervised_fine-t.png)

*Figure 3-44: A two-step approach of supervised fine-tuning using the reasoning traces*


Figure 3-44. A two-step approach of supervised fine-tuning using the reasoning traces
(left) and reinforcement learning using format and accuracy rewards (right)
As such, enabling reasoning in multi-modal LLMs is much like in text-only LLMs,
but the types of Chain-of-Thought data need to be adapted for the multi-modal
use cases. Often, existing Chain-of-Thought data is for text-only inputs and not
multi-modal inputs.
|
Chapter 3: Reasoning Large Language Models