---
title: "Native Reasoning"
chapter_number: 50
page_start: 140
page_end: 141
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Native Reasoning



![Figure 3-41: The final version of DeepSeek-R1 was trained using reinforcement learning](images/fig_03-41_The_final_version_of_DeepSeek-R1_was_tra.png)

*Figure 3-41: The final version of DeepSeek-R1 was trained using reinforcement learning*


Figure 3-41. The final version of DeepSeek-R1 was trained using reinforcement learning
and various rewards
This resulted in the final DeepSeek-R1 model. Interestingly, the first three steps of the
training pipeline were purely done to create the synthetic data to eventually fine-tune
DeepSeek-V3.
In sum, DeepSeek-R1 is created through first using supervised fine-tuning on
DeepSeek-V3-Base and then applying GRPO with format, accuracy, and preference
rewards.
Native Reasoning
We have explored various techniques in supervised fine-tuning and reinforcement
learning. However, after the model has learned to reason, how do you then actually
use it? We covered an important part of that during the fine-tuning examples and in
Chapter 2, namely the chat template.
Let’s illustrate this with the Gemma 4 E4B model. Its chat template (when you don’t
consider any tool usage) uses, among others, the following special tokens:
<bos>
Signals the beginning of the sequence.
<|turn>system
The start of a system prompt.
|
Chapter 3: Reasoning Large Language Models

<|turn>user
The start of the user turn.
<|turn>model
The start of the model’s turn.
<turn|>
Signals the end of a turn.
<|think|>
Adding this token in the system turn enables reasoning. Removing this token in
the system turn disables reasoning.
Like DeepSeek-R1, Gemma 4 was trained with these special tokens to make sure it
understands when it’s your turn and when it’s the model’s turn. Ollama has been
parsing our queries automatically based on this chat template, but let’s explore what it
would look like if it did not automatically parse the queries.
The Gemma 4 E4B model expects the following chat template to differentiate
between roles and to enable thinking:
<bos><|turn>system
<|think|>
SYSTEM PROMPT<turn|>
<|turn>user
USER PROMPT<turn|>
<|turn>model
Note how there are separate turns for the system, user, and model. The thinking can
be enabled by adding the <|think|> token to the system turn. If you want to disable
thinking, you would only have to remove that token.
If we want to query the model, then we would need to send the following prompt to
the model:
<bos><|turn>system
<|think|>
You are a helpful assistant<turn|>
<|turn>user
I saw 6 flamingos. 2 flew away. 1 hid behind a tree. How many can I see?
<turn|>
<|turn>model
The model would then respond with a structure like so:
<|channel>thought
You started with 6, but 2 flew away, leaving 4 behind. Out of those 4,
1 is hiding behind a tree, so you can only actually see 3.
<channel|>
You can see **3** flamingos
Modifying Proposal Distribution
|