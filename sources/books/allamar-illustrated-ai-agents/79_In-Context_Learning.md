---
title: "In-Context Learning"
chapter_number: 79
page_start: 216
page_end: 216
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# In-Context Learning

In-Context Learning
In-context learning, the ability of LLMs to learn from a few examples in their context,7
is an exceptionally useful technique to enable new behavior in LLMs without the need
to fine-tune them. As we covered in Chapter 3, it is also known as few-shot prompting
or few-shot learning, where you provide several examples to the LLM to learn from.
Specifically, it’s a prompt engineering technique where you give some examples of
the behavior that you want the LLM to repeat. In our case, and as illustrated in
Figure 5-13, we want the LLM to output the tool call in a specific format by following
the examples we created ourselves.



![Figure 5-13: An example of few-shot prompting to enable tool calling](images/fig_05-13_An_example_of_few-shot_prompting_to_enab.png)

*Figure 5-13: An example of few-shot prompting to enable tool calling*


Figure 5-13. An example of few-shot prompting to enable tool calling
In-context learning is especially helpful when leveraging the messages structure that
we explored previously. Remember when we pretended the assistant called a tool by
adding it to the messages? We can apply the same concept and act as if the model
called tools before. As shown in Figure 5-14, we can create our messages in such a
way that the model thinks it has already used some of the tools before. So, when it
subsequently gets a query, it has examples of how the tools should be called and what
kinds of output can be expected.
7 Dong, Qingxiu et al. 2022. “A Survey on In-context Learning,” arXiv, 2301.00234.
|
Chapter 5: Tool Usage, Learning, and Protocols