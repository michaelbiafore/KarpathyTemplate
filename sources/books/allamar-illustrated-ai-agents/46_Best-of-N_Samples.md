---
title: "Best-of-N Samples"
chapter_number: 46
page_start: 126
page_end: 128
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Best-of-N Samples

Best-of-N Samples
A common and straightforward method for using a verifier is called Best-of-N
samples.11 In this method, the LLM generates N candidate answers, typically using a
high or varying temperature to encourage diversity. Then, a verifier evaluates each
answer and selects the highest-scoring one.
There are two main forms of Best-of-N samples, using:
Outcome Reward Models (ORM)
Only the answers are scored using a verifier (e.g., LLM, unit tests, compiler) and
the highest scoring answer is chosen.
Process Reward Models (PRM)
Only the processes (thoughts) are scored using verifiers. When there are multiple
reasoning traces for a given question, each trace is scored and averaged. The
answer that has traces with the highest scores is selected.
An overview of these two techniques is shown in Figure 3-26. For more information
on how to create and train reward models, we highly suggest reading Cameron R.
Wolfe’s post on reward models.



![Figure 3-26: Best-of-N samples can use Outcome Reward Models (ORMs; left) and/or](images/fig_03-26_Best-of-N_samples_can_use_Outcome_Reward.png)

*Figure 3-26: Best-of-N samples can use Outcome Reward Models (ORMs; left) and/or*


Figure 3-26. Best-of-N samples can use Outcome Reward Models (ORMs; left) and/or
Process Reward Models (PRMs; right)
11 Lightman, Hunter et al. 2023. “Let’s Verify Step by Step,” The Twelfth International Conference on Learning
Representations.
|
Chapter 3: Reasoning Large Language Models

Let’s go through an example on how we could verify the output of an LLM and
choose the best one through sampling. We will ask the model to generate a function
that converts Roman numerals (e.g., IV) to integers (e.g., 4). There are many differ‐
ent ways you can verify this output, such as using another LLM, creating tests, or
checking whether the code compiles. The choice depends on what you have available.
Checking if the code compiles is a great first step but does not check the correctness
of the output. Let’s assume that we have a couple of test cases. With those, we can
create a simple verification function that checks how many test cases pass:
test_cases = [
 ("III", 3),
 ("IV", 4),
 ("IX", 9),
 ("LVIII", 58),
 ("MCMXCIV", 1994),
 ("MMMCMXCIX", 3999),
 ("", 0),
 ("IIII", 0), # invalid: four in a row
 ("VV", 0), # invalid: V can't repeat
 ("IC", 0), # invalid: I can only subtract from V or X
 ("ABC", 0), # invalid: non-Roman characters
 ("MMMM", 0), # invalid: exceeds 3999
]


def verify(answer):
 try:
 # Extract the function
 namespace = {}
 exec(answer, namespace)
 fn = namespace["roman_to_int"]

 # Evaluate the function on test cases
 score = sum(fn(inp) == expected for inp, expected in test_cases) / len
 (test_cases)
 return score
 except Exception:
 # Return 0 if the code is not valid Python
 return 0.0
Using those test cases, we can run a similar loop as we did with the self-consistency
example:
responses = []
for _ in range(10):
 # The query we want to ask the model
 query = """Write a Python function `roman_to_int(s)` that converts a Roman
 numeral
string to an integer. The function should:
- Handle standard Roman numerals from 1 to 3999.
- Correctly handle subtractive notation (e.g., IV=4, IX=9, XL=40, XC=90, CD=400,
Search Against Verifiers
|

CM=900).
- Return 0 for invalid inputs (empty string, non-Roman characters, or invalid
patterns
 like "IIII" or "VV").

Give only the function definition, no explanation or markdown formatting."""

 # Generate response
 response = llm.generate([{"role": "user", "content": query}])

 # Verify the response and compute a score
 score = verify(response.content)

 # Store the response and its score
 responses.append((response.content, score))

# Get highest score and the corresponding answer
best_answer, best_score = max(responses, key=lambda x: x[1])

# Show all scores
[response[1] for response in responses]
When you run this, the model creates 10 answers, each of which is judged with the
verify function. In our case, this gives the following range of scores:
[0.6666666666666666,
0. 5833333333333334,
0. 9166666666666666,
0. 9166666666666666,
0. 8333333333333334,
0. 75,
0. 9166666666666666,
0. 9166666666666666,
1. 0,
0. 25]
Note that we have found only one answer that is correct. Without having a verify
function and without sampling, it’s unlikely the model would have gotten the correct
answer.
The great thing about the Best-of-N samples method is that it allows for a wide
degree of creativity and flexibility in how you structure the application of these verifi‐
ers. For instance, we can also weigh each answer candidate by the Process Reward
Model and use that to create an aggregate score for answers that appear multiple
times. An example is given in Figure 3-27 of this weighted Best-of-N samples.
|
Chapter 3: Reasoning Large Language Models