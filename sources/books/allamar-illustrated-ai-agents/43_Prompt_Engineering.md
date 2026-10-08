---
title: "Prompt Engineering"
chapter_number: 43
page_start: 118
page_end: 121
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Prompt Engineering



![Figure 3-21: Reasoning steps can each be judged by a reward model](images/fig_03-21_Reasoning_steps_can_each_be_judged_by_a.png)

*Figure 3-21: Reasoning steps can each be judged by a reward model*


Figure 3-21. Reasoning steps can each be judged by a reward model
How these scores are then used to judge the quality of the answer or select the best
answer depends on the specific category of test-time compute.
Prompt Engineering
In some of our previous examples, non-reasoning LLMs were assumed to be able to
output reasoning traces (thoughts). This was especially true of techniques in search
against verifiers that sample many reasoning traces and answers before selecting the
best one.
So, how are these non-reasoning LLMs able to output reasoning traces?
Prompt engineering plays a vital role in this process, with a technique called Chain-
of-Thought (CoT).8 This is one of the first techniques to elicit reasoning in LLMs that
were not trained for reasoning tasks.
Chain-of-Thought prompting requires the model to explain its reasoning process
by specifying that in the prompt. LLMs are quite adept at following examples. By
demonstrating the desired reasoning style, it increases the likelihood that the LLM
will replicate it, as illustrated in Figure 3-22. Such demonstrations in a prompt
are typically referred to as one-shot prompting or few-shot prompting. One-shot
prompting uses a single example to demonstrate a task or targeted behavior while
few-shot prompting uses two or more examples, which tends to result in higher
accuracy as it helps the model recognize patterns.
8 Wei, Jason et al. 2022. “Chain-of-Thought Prompting Elicits Reasoning in Large Language Models,” NIPS ’22:
Proceedings of the 36th International Conference on Neural Information Processing Systems, 24824-24837.
|
Chapter 3: Reasoning Large Language Models



![Figure 3-22: An example of one-shot learning where a single example is given to the](images/fig_03-22_An_example_of_one-shot_learning_where_a.png)

*Figure 3-22: An example of one-shot learning where a single example is given to the*


Figure 3-22. An example of one-shot learning where a single example is given to the
LLM that describes how it should reason
We can use the LLM we created in Chapter 2 to demonstrate the behavior. Let’s first
load in the LLM:
from illustrated_agents.chapters.ch2 import LLM

# Gemma 3 12B (no native thinking or tool calling)
llm = LLM(model="gemma3:12b", temperature=1)
Note that we set the temperature to 1 as that will allow us to generate different
answers that we can use later for sampling. If we were to set it to 0, then the output
would always be the same regardless of how many times we run it.
After doing so, let’s give the LLM a riddle and ask it to be concise in its answer as an
example. As discussed, this is a form of few-shot learning where you give examples of
what you want the answer to the interaction to be:
# Example of one-shot prompting
prompt_example = "I saw 6 flamingos. 2 flew away. 1 hid behind a tree. How many
can I see? Be concise."
prompt_answer = "3"

# The query we want to ask the model
query = "I saw 9 penguins. 2 slid in the water and disappeared from sight
while 4 waddled up from the shore. How many can I see?"
Categories of Test-Time Compute
|

# Messages
messages = [
 {"role": "user", "content": prompt_example},
 {"role": "assistant", "content": prompt_answer},
 {"role": "user", "content": query},
]

# Generate response
response = llm.generate(messages)
print(response)
This gives us:
Response(
 content='7\n',
 reasoning=None,
 tool_call=None,
 metadata={'model': 'gemma3:12b', 'prompt_tokens': 82, 'completion_tokens': 3}
)
Note how it got the answer wrong! Without any extensive reasoning, the LLM
directly goes to answering the question without properly thinking of this puzzle.
Instead of using a concise answer, let’s give the LLM a more thorough one that
mimics the type of reasoning we would like to see:
pprompt_example = "I saw 6 flamingos. 2 flew away. 1 hid behind a tree.
How many can I see?"
prompt_answer = "You saw 6 flamingos 2 flew away. 6 - 2 = 4.
Then, 1 flamingo hid. You see now 4 - 1 = 3."

# Messages
messages = [
 {"role": "user", "content": prompt_example},
 {"role": "assistant", "content": prompt_answer},
 {"role": "user", "content": query},
]

# Generate response
response = llm.generate(messages)
print(response)
This gives us:
Response(
 content="Okay, let's break it down:\n\n
* You started with 9 penguins.\n
* 2 slid into the water and disappeared: 9 - 2 = 7\n
* 4 waddled up from the shore: 7 + 4 = 11\n\nYou can see **11** penguins!",
 reasoning=None,
 tool_call=None,
 metadata={'model': 'gemma3:12b', 'prompt_tokens': 117, 'completion_tokens': 70}
)
|
Chapter 3: Reasoning Large Language Models

This is the correct answer! Just by giving the model a couple of examples on how to
reason, it follows that behavior and allows for a reasoning process.
This process can be further simplified by foregoing any examples of reasoning steps
and instead simply stating: “Let’s think step-by-step.”9 This is a form of zero-shot
prompting where no examples are used that has a chance of working with some
models.
Zero-shot prompting tends to perform worse than one-shot
prompting, which tends to perform worse than few-shot prompt‐
ing. Although providing examples helps guide the model, it can
still achieve similar behavior without them.



![Figure on page 17](images/fig_p017_x95.png)


What makes prompting special in the context of non-reasoning LLMs is that non-
reasoning LLMs do have reasoning capabilities hidden somewhere in their parame‐
ters. It’s a matter of prompting it in an elegant way to extract those capabilities.
Let’s see if we can reproduce the behavior we explored before by simply adding, “Let’s
think step-by-step” to the prompt:
# Messages with zero-shot Chain-of-Thought prompting
messages = [{"role": "user", "content": query + " Let's think step by step."}]

# Generate response
response = llm.generate(messages)
print(response)
This gives us:
Response(
 content="Okay, let's break this down step by step:\n\n
1. **Start:** You initially see 9 penguins.\n\n
2. **Penguins disappear:** 2 penguins slid into the water and
are no longer visible. So, 9 - 2 = 7 penguins.\n\n
3. **Penguins appear:**
4 penguins waddled up from the shore, and you can now see them.
So, 7 + 4 = 11 penguins.\n\n**Answer:** You can now see 11 penguins.\n",
 reasoning=None,
 tool_call=None,
 metadata=
 {
 'model': 'gemma3:12b', 'prompt_tokens': 51, 'completion_tokens': 112
 }
)
9 Kojima, Takeshi et al. 2022. “Large Language Models Are Zero-Shot Reasoners,” NIPS ’22: Proceedings of the
36th International Conference on Neural Information Processing Systems: 22199-22213.
Categories of Test-Time Compute
|