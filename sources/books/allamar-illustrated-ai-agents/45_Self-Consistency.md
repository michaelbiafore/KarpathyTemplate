---
title: "Self-Consistency"
chapter_number: 45
page_start: 124
page_end: 125
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Self-Consistency

A major advantage of using verifiers is that there is no need to retrain or fine-tune
the LLM that you use for answering the question. Likewise, you can easily scale the
test-time compute up by sampling more answers or restricting it by sampling fewer.
Self-Consistency
One of the first methods for search against verifiers is called self-consistency and
actually does not use a reward model or verifier.10 Instead, it samples a user-defined
number of answers and performs a majority vote to select the most frequent answer
(Figure 3-25).



![Figure 3-25: Self-consistency samples many thoughts and answers and will choose the](images/fig_03-25_Self-consistency_samples_many_thoughts_a.png)

*Figure 3-25: Self-consistency samples many thoughts and answers and will choose the*


Figure 3-25. Self-consistency samples many thoughts and answers and will choose the
most frequent answer
To generate many different reasoning traces and answers, a high temperature is
usually combined with Chain-of-Thought-like prompting. Note that varying values
of temperature can also be used to get more randomized behavior. Self-consistency
can then easily be scaled by generating more answers, each with reasoning steps.
Let’s explore how we would do this in practice. We use a seating puzzle that the model
has to reason through. The model is queried 10 times and each time can generate
a different reasoning trace and answer. We ask the model to put its answer after
“Answer:” so we can easily separate the answer from the reasoning. The answers are
then counted:
10 Wang, Xuezhi et al. 2022. “Self-Consistency Improves Chain of Thought Reasoning in Language Models,”
arXiv, 2203.11171.
|
Chapter 3: Reasoning Large Language Models

from collections import Counter

answers = []
for _ in range(10):
 query = """Six friends (Maarten, Ilse, Sarah, Jor, Irene, and Chris)
 are sitting in a row.

- Sarah is in seat 3.
- Chris is sitting at one of the ends of the row.
- Jor is sitting immediately to the right of Chris.
- Ilse is sitting exactly in the middle of Sarah and Maarten.
- Irene is not sitting next to Sarah.
- Maarten is sitting somewhere to the left of Irene.

In which seat is Maarten sitting?
Let's think step by step and give back your answer only after 'Answer:'.
"""

 # Generate response
 messages = [{"role": "user", "content": query},]
 response = llm.generate(messages)
 answer = response.content.split("Answer:")[-1].replace("\n", "").strip()
 answers.append(answer)

Counter(answers)
This gives us:
Counter({'5': 4, '1': 3, '4': 1, '2': 2})
The most common answer is 5 (which is correct). However, in some runs the model
has produced the incorrect answer. By rerunning the model several times, we increase
the likelihood that the model gets the answer correct.
Self-consistency works surprisingly well, considering that it selects
the most frequent answer and not necessarily the best answer.
As it turns out, sampling over many answers reduces the chance
of selecting an infrequent and potentially incorrect answer. How‐
ever, for very complex tasks that the LLM seldom gets correct,
self-consistency is unlikely to improve the output.



![Figure on page 17](images/fig_p017_x95.png)


The previous code example illustrates this nicely because it is right
on the edge of what the model knows. In our experiments, the
model tends to lean toward the correct answer (5) but sometimes
might produce too many incorrect answers. Since we have a tem‐
perature of 1, the results will be different each time you run the
model.
Search Against Verifiers
|