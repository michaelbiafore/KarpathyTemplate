---
title: "Search Against Verifiers"
chapter_number: 44
page_start: 122
page_end: 123
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Search Against Verifiers

Also the correct answer! Now instead of having to create a bunch of examples, you
can just append “Let’s think step-by-step” to the prompt. To enable the TinyAgent’s
reasoning, all we have to do is add that “thinking” prompt to the task like we did
before:
from illustrated_agents.chapters.ch2 import TinyAgent

agent = TinyAgent(llm=llm)
response = agent.run(query + " Let's think step by step.")
We’ll use this idea of zero-shot Chain-of-Thought more in Chapter 6, where we will
enable reasoning by telling the model to use separate THOUGHT and ANSWER
fields for the reasoning and the answer, respectively.
A test-time compute category that relies heavily on Chain-of-Thought-like prompt‐
ing is search against verifiers. By sampling many reasoning traces through Chain-of-
Thought, much of its instability can be prevented.
Search Against Verifiers
Search against verifiers refers to a family of techniques that involve generating mul‐
tiple candidate answers or reasoning traces and then evaluating them to choose
the best answer. The scorer is typically referred to as the reward model (RM), also
called the verifier. However, as we will explore in the first example, not all of these
techniques have to use a reward model.
Search against verifiers does not necessarily enable reasoning but is more akin to
what we expect of non-human behavior. It programmatically goes through many
answers and scores the best ones. As such, the techniques that we will explore might
remind you of traditional methods, like majority voting or tree-search techniques.
As shown in Figure 3-23, search against verifiers typically consists of three steps:
1. Sampling multiple reasoning processes and/or answers.
1.
2. A reward model (verifier) scores the generated output.
2.
3. The best answer based on the generated scores is chosen.
3.
The verifier is typically an LLM, fine-tuned for either judging the outcome (ORM) or
the process (PRM). This fine-tuning can be through actual training or by creating a
specialized prompt with few-shot examples, as we explored before.
To sample many different thoughts and answers to a given question, LLMs can use
different temperature values. The temperature parameter in LLMs controls the ran‐
domness of the model’s output by changing the distribution of the model’s next token
probabilities. Shown in Figure 3-24, low temperatures focus on high-probability
|
Chapter 3: Reasoning Large Language Models

tokens and tend to generate similar texts, while high temperatures allow for more
creative and different texts to be generated.



![Figure 3-23: The three steps of search against verifiers](images/fig_03-23_The_three_steps_of_search_against_verifi.png)

*Figure 3-23: The three steps of search against verifiers*


Figure 3-23. The three steps of search against verifiers



![Figure 3-24: A higher temperature has a higher likelihood of the LLM generating](images/fig_03-24_A_higher_temperature_has_a_higher_likeli.png)

*Figure 3-24: A higher temperature has a higher likelihood of the LLM generating*


Figure 3-24. A higher temperature has a higher likelihood of the LLM generating
different outputs, whereas a lower temperature typically results in similar outputs
Search Against Verifiers
|