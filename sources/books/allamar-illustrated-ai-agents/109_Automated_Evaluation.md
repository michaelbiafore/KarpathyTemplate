---
title: "Automated Evaluation"
chapter_number: 109
page_start: 290
page_end: 301
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Automated Evaluation

Comparing two models like this in a pair-wise fashion can be extended to comparing
more than two agents through an Elo rating system, borrowed from competitive
chess. Rather than running every possible head-to-head comparison between tens of
models, each pairwise result updates a running score of both models/agents; wins
increase the score and losses decrease it according to a specific formula that takes
into consideration the relative strength of the opponent. Chatbot Arena (LMSYS)
is the most prominent example of this applied at scale, where thousands of users
compare anonymous model outputs and stable rankings emerge over time (using a
rating similar to Elo).
Human evaluation is slow and expensive, but it remains the baseline against which
all automated methods are validated. When a new LLM judge or scoring metric is
proposed, showing that it correlates with human judgement is often how researchers
establish that it measures something real.
Automated Evaluation
Human evaluation does not scale to the continuous feedback loops that agent devel‐
opment requires. Agent builders iterate over hundreds if not thousands of prompt
changes, model swaps, versions of the agent, and example test points that can easily
add up to requiring millions of complex judgements. That’s where automated evalua‐
tion comes in.
Automated evaluation covers a spectrum from static automated checks to judgements
made by another model. The right method depends on the kind of output your agent
produces.
Building a simple agent evaluator
Before going into specific methods, let’s first create a simple framework that we
can use to perform automated evaluation on your TinyAgent. To do so, we first
need to create the Benchmark dataclass. The Benchmark contains information on the
task (name), the examples in the benchmark to test (examples), and the method of
performing automated evaluation (scorer). The scorer is a function that takes in a
prediction and an example from the benchmark. Depending on the scorer, it should
either always return a boolean to indicate whether the prediction is correct or not, or
it should always return a score:
```
from dataclasses import dataclass
from typing import Callable
```

# Type hint for the scorers
## (prediction: str, example: dict) -> bool | float
Scorer = Callable[[str, dict], bool | float]

@dataclass
|
Chapter 7: Evaluating Agents

class Benchmark:
 name: str
 examples: list[dict]
 scorer: Callable
We then need an Evaluator class that runs a set of examples against a selected scorer.
We also need a new agent every time we run a benchmark to reset its memory and
trajectory, so we create a small function for that:
```
from illustrated_agents.chapters.ch2 import LLM
from illustrated_agents.chapters.ch4 import Memory
from illustrated_agents.chapters.ch5 import NativeTools
from illustrated_agents.chapters.ch6 import NativeReAct, TinyAgent
```

# Gemma 4 E4B (with native thinking and tool calling)
llm = LLM(model="gemma4:e4b", think=True)


class Evaluator:
 """Run a TinyAgent over a Benchmark and aggregate the results."""

 def __init__(self, create_agent: Callable):
 """Initialize with a function that creates a new agent instance."""
 self.create_agent = create_agent

 def run(self, benchmark: Benchmark) -> dict:
 """Run the agent on examples in the benchmark and score the results."""

 # Run each example and collect results
 results = []
 for example in benchmark.examples:
 agent = self.create_agent()
 prediction = agent.run(example["task"]) or ""
 passed = benchmark.scorer(prediction, example)
 results.append(
 {
 "prediction": prediction,
 "passed": passed,
 }
 )

 # Aggregate pass rate
 if results:
 pass_rate = sum(
 result["passed"] for result in results
 ) / len(results)
 else:
 pass_rate = 0.0

 # Return detailed results and overall pass rate
 return {
 "name": benchmark.name,
Outcome Evaluation: Did the Agent Get the Right Output?
|

"pass_rate": pass_rate,
 "results": results,
 }


def create_agent():
 """Create a new instance of TinyAgent"""
 return TinyAgent(
 llm=llm,
 memory=Memory(),
 tools=NativeTools(),
 planner=NativeReAct(),
 )
The Evaluator will run a check for each example in the benchmark, determine
whether the agent has generated the correct output, and simply track a pass or fail.
The pass/fail rate over all examples is averaged into the "pass_rate".
Let’s explore how to use this in practice by covering several methods for automated
evaluation.
Exact match
The most straightforward form of automated evaluation is a deterministic check: the
output either matches the expected answer or it doesn’t. If your agent is asked to
extract the invoice total from a document and the correct answer is $1,482.81, you
can make that comparison directly in software. This goes quite far and powers a large
number of benchmarks. Yet its beautiful simplicity is also its main drawback; many
tasks in practice don’t simply output a single value. If the agent, for example, was to
write a document, generate code, produce a plan, or synthesize information across
many sources, exact match breaks down because there are many valid ways to express
a correct answer.
Exact match is also brittle against trivial formatting differences. For the invoice exam‐
ple, a prompt that doesn’t pin down the format can yield answers such as 1,482.81
(no dollar sign), 1482.81 (no thousands separator), or $1,482.81. (with a trailing
period), and a strict check flags every one of them as wrong.
To implement the exact match scoring mechanism, let’s first consider the benchmark
for which we want to use this. MMLU-Pro, which consists of many different tasks with
multiple-choice answers, is a great benchmark to start with. Compared to MMLU, it
extends the number of multiple-choice options to 10 to make the tasks more difficult
and prevent random guessing. Those options are labeled A through J. As such, the
scoring mechanism needs to match only one of those with the ground truth:
import re

def exact_match_scorer(prediction: str, example: dict) -> bool:
 """Return True if the answer matches the prediction, False otherwise"""
|
Chapter 7: Evaluating Agents

match = re.search(r"\b([A-J])\b", prediction.upper())
 return match.group(1) == example["expected"]
The exact_match_scorer gives back either True or False depending on whether
the answer is correct. Since we know the answer beforehand, the check is relatively
straightforward.
If we were to use the full benchmark with more than 12,000 question/answer pairs,
running the evaluation would take significant time. Instead, we grab three examples
from the dataset and use them to showcase how you would run the evaluation:
# Three examples from MMLU Pro
mmlu_pro = Benchmark(
 name="MMLU Pro",
 examples=[
 {
 "task": """Which of the following is the body cavity that contains
the pituitary gland?
A) Ventral B) Dorsal C) Buccal D) Thoracic E) Pericardial F) Abdominal
G) Spinal H) Pelvic I) Pleural J) Cranial
Answer with only the letter.""",
 "expected": "J",
 },
 {
 "task": """What is the approximate mean cranial capacity of
Homo erectus?
A) 1200 cc B) under 650 cc C) 1700 cc D) 1350 cc E) just under 1000 cc
F) 1500 cc G) under 500 cc H) about 800 cc I) just over 1100 cc J) about 900 cc
Answer with only the letter.""",
 "expected": "E",
 },
 {
 "task": """
According to Moore’s "ideal utilitarianism," the right action is the one that
brings about the greatest amount of:
A) wealth. B) virtue. C) fairness. D) pleasure. E) peace. F) justice.
G) happiness. H) power. I) good. J) knowledge.
Answer with only the letter.""",
 "expected": "I",
 },
 ],
 scorer=exact_match_scorer,
)
Then, we can run it like so:
# Run evaluation
result = Evaluator(create_agent).run(mmlu_pro)
print(result)
Outcome Evaluation: Did the Agent Get the Right Output?
|

This gives:
{
 'name': 'MMLU Pro',
 'pass_rate': 0.3333333333333333,
 'results': [
 {'prediction': 'J', 'passed': True},
 {'prediction': 'H', 'passed': False},
 {'prediction': 'G', 'passed': False}
 ]
}
The model got one question right and two wrong. That is not too bad for such a small
model. These types of questions test knowledge, which tend to be easier for larger
models since they have more parameters to store information.
For some benchmarks, specific packages and harnesses were cre‐
ated in which you need to run your LLM. τ-bench, for instance, has
an entire framework that you can use to run the evaluation. This
also makes evaluation difficult at times since different benchmarks
might need different frameworks, which hinders tests of the gener‐
alizability of harnesses.



![Figure on page 17](images/fig_p017_x95.png)


Programmatic checks
Programmatic checks extend exact matches into the broader category of automated
verifiers. Rather than checking for a single string, you write code that verifies struc‐
tural properties of the output. If we expect a JSON string output, we can automati‐
cally check if the output is valid JSON. For a coding agent where we expect a function
implementation, we run unit tests and validate that the function behaves as expected.
For more advanced coding outputs such as SWE-bench, in which the output is a
patch that changes multiple files in a repository, the programmatic checks are a suite
of unit tests that fail before the patch and have to run successfully after the patch is
applied.
This approach is fast, cheap, and objective. It’s one reason coding agents rose much
faster than other kinds of agents—the code modality allows for automated checks,
which proves useful for evaluation that also guides the training process.
To implement programmatic checks, we’ll use the IFEval benchmark.2 This bench‐
mark contains verifiable instructions, such as “write in more than 400 words” or
“mention the keywords of AI at least 3 times.” These instructions can be verified by
heuristics and need a separate “validator” for each of these instructions. As before,
let’s start with the scoring mechanism:
2 Zhou, Jeffrey et al. 2023. “Instruction-Following Evaluation for Large Language Models,” arXiv, 2311.07911.
|
Chapter 7: Evaluating Agents

def programmatic_scorer(prediction: str, example: dict) -> bool:
 """Check a prediction against its related check."""
 return example["check"](prediction)
This programmatic_scorer doesn’t do much except for running the check for each
example in the benchmark. Some of these examples check the number of words,
while others check if there is no comma in the output. As before, we grab three
examples from the dataset to showcase how you would run this evaluation with the
corresponding checks:
# Three examples from IFeval
ifeval = Benchmark(
 name="IFeval",
 examples=[
 {
 "task": "Write me a funny song with less than 10 sentences for a
 proposal to build a new playground at my local elementary school.",
 "check": lambda text: sum(1 for c in text if c in ".!?") < 10,
 },
 {
 "task": "Write an ad copy for a new product, a digital photo frame
 that connects to your social media accounts and displays your photos.
 Respond with at most 150 words.",
 "check": lambda text: len(text.split()) <= 150,
 },
 {
 "task": "I am planning a trip to Japan, and I would like thee to
 write an itinerary for my journey in a Shakespearean style.
 You are not allowed to use any commas in your response.",
 "check": lambda text: "," not in text,
 },
 ],
 scorer=programmatic_scorer,
)
Note that each example now has a short function to check whether the output has
fewer than 10 sentences, at most 150 words, and if it has a comma.
Then, we can run the evaluation like so:
# Run evaluation
result = Evaluator(create_agent).run(ifeval)
print(result)
Which gives:
{
 'name': 'IFeval',
 'pass_rate': 1.0,
 'results': [
 {
 'prediction': '*(Sung to the tune of "Twinkle Twinkle Little Star"
 or a very upbeat, dramatic jingle)* ...
Outcome Evaluation: Did the Agent Get the Right Output?
|

Let’s give elementary school the perfect fair!',
 'passed': True
 },
 {
 'prediction': "**Caption/Headline Option:** Your Memories.
 Never Out of Sight. ... Available in multiple finishes.
 [Link/Store Name]",
 'passed': True
 },
 {
 'prediction': "Hark attend gentle traveler a
 journey most grand ... May this itinerary thy journey transcend",
 'passed': True
 }
 ]
}
We truncated the preceding long prediction (the full output is in the associated
GitHub repository). The pass rate gives a score of 1, meaning that the model correctly
followed all instructions!
LLM-as-a-judge
When the output is too open-ended for a programmatic check, a natural move is
to ask another capable language model to evaluate it. This is the LLM-as-a-judge
pattern. LLM-as-a-judge is typically used to produce a single score or to choose a
preferred output from two agents. Strong language models can assess fluency, logical
coherence, information consistency given a ground truth context, and tone in ways
that no programmatic check can. Figure 7-6 shows scoring with LLM-as-a-judge
doing both absolute scoring as well as preference selection from two outputs.
LLM judges have failure modes worth knowing, some of which they may share with
human judges. They can prefer outputs that sound confident over ones that are
actually correct. They can be sensitive to presentation order (e.g., tending to prefer
the first option presented to them). They inherit biases from their own training and
may tend to prefer their own output or those from their own family of models to that
of other models.
|
Chapter 7: Evaluating Agents



![Figure 7-6: A judge model takes agent outputs and scoring criteria as input and evalu‐](images/fig_07-06_A_judge_model_takes_agent_outputs_and_sc.png)

*Figure 7-6: A judge model takes agent outputs and scoring criteria as input and evalu‐*


Figure 7-6. A judge model takes agent outputs and scoring criteria as input and evalu‐
ates them either as a pairwise preference or as an absolute score
Several techniques help mitigate these drawbacks. Using a judge from a different
model family reduces the tendency to favor its own outputs. Swapping presentation
order of preference sets across evaluation runs controls for position bias. Asking a
judge to produce a written rationale or using a reasoning model as judge can improve
consistency. We can also use ensembles of judges, where multiple models vote and we
aggregate their judgments.
Before we implement this scorer, we first need to decide on the judge to score the
output. As outlined previously, we’ll choose a different and more capable judge of
the output, namely Google’s Gemini model. There are many variants, but fortunately,
there is a free tier available that lets us choose a capable model, Gemini 3.1 Flash-Lite.
To use it, you can generate an API Key from the website. We then create the judge like
so:
# Judge
judge = LLM(
 model="gemini-3.1-flash-lite",
 base_url="https://generativelanguage.googleapis.com/v1beta/openai",
 api_key="MY_API_KEY"
)
Note that if you have enough (V)RAM available, you could also locally run another
model that is more capable, such as Gemma 4 26B A4B.
Outcome Evaluation: Did the Agent Get the Right Output?
|

Next, we implement a simple version of LLM-as-a-judge by asking Gemini to score
the output of your TinyAgent. Instead of returning a boolean, we’re now returning a
single score between 0 and 1. This allows for a much more fine-grained perspective
on how well the agent is doing:
def judge_scorer(prediction: str, example: dict) -> bool:
 """The LLM-as-a-judge scorer."""
 prompt = f"""
Score the response from 0.0 to 1.0.

```
Expected: {example["expected"]}
Response: {prediction}
```

Reply with only a single number.
"""
 response = judge.generate([{"role": "user", "content": prompt}])
 score = float(response.content.strip().split()[0])
 return score
The judge_scorer uses a straightforward prompt without frills to generate a score
between 0 and 1.
To illustrate this fine-grained perspective, we’ll use the same examples from MMLU-
Pro that we used before. Instead of using multiple-choice questions in the bench‐
mark, we now simply remove them and make them open-ended questions. That way,
the answer is more difficult to score programmatically or using an exact match and
instead requires a judge:
# Three examples adapted from MMLU Pro
mmlu_pro = Benchmark(
 name="MMLU Pro",
 examples=[
 {
 "task": "Which body cavity contains the pituitary gland?",
 "expected": "the cranial cavity",
 },
 {
 "task": "What is the approximate mean cranial capacity of Homo
 erectus?",
 "expected": "just under 1000 cc",
 },
 {
 "task": "According to Moore's 'ideal utilitarianism,' the right
 action is the one that brings about the greatest amount of what?",
 "expected": "good",
 },
 ],
 scorer=judge_scorer,
)
|
Chapter 7: Evaluating Agents

Note how we simply replace the expected multiple-choice answer with the actual
answer. This is what will be given to Gemini to help score the quality of your
TinyAgent’s answer.
Then, we can run the evaluation like so:
# Run evaluation
result = Evaluator(create_agent).run(mmlu_pro)
print(result)
This gives:
{
 'name': 'MMLU Pro',
 'pass_rate': 0.7999999999999999,
 'results': [
 {
 'prediction': 'The pituitary gland hangs within the **sella turcica**
 of the **sphenoid bone**.\n\nWhile the pituitary gland is housed
 within a specific bony indentation (the sella turcica), which is part
 of the skull, when discussing the major body cavities, it is situated
 near the boundaries of the **dura mater** that encloses the brain.
 \n\nTherefore, the most accurate general category is that it is within
 the **cranial cavity** (the skull cavity), but more specifically,
 it is physically housed in the sella turcica area.',
 'passed': 1.0
 },
 {
 'prediction': 'The approximate mean cranial capacity of
 *Homo erectus* is generally estimated to fall in the range of
 **600 to 900 cubic centimeters (cc)**.\n\nHowever, many
 paleoanthropologists and studies tend to cluster the average
 capacity closer to the **700 to 800 cc** range.\n\n
 ### Key Considerations:\n\n1. **Variation is High:**
 It is crucial to understand that this is a broad range.
 *Homo erectus* lived over a long period (from approximately
 2 million years ago to 100,000 years ago) and across diverse
 geographical locations. Specimens vary greatly in size.\n2.
 **Comparison:**\n * **Earlier Hominins (e.g., Australopithecus):
 ** Much lower, typically 300–550 cc.\n * **Modern Humans (Homo
 sapiens):** Typically 1200–1500 cc.\n3. **Scientific Debate:**
 Due to differing techniques in calculating endocranial volume
 (the internal volume of the brain cavity) from fossil skulls,
 the exact mean estimate can shift depending on the specific
 metrics, which contributes to the wide accepted range.',
 'passed': 0.4
 },
 {'prediction': '**Happiness** (or, more broadly, the greatest
 good/well-being).', 'passed': 1.0}
 ]
}
Outcome Evaluation: Did the Agent Get the Right Output?
|

We purposefully did not truncate the prediction because it showcases how close the
model was to the actual answer. The pass rate is now lower than the multiple-choice
variant, as it gave the incorrect answer to example two. It’s somewhat close, which
might be the reason why it got a score of 0.4 instead of 0.
What’s especially interesting about this output is that a score of 1 was given to the
final example. The multiple-choice variant specifically stated that the answer should
be “good” (I) and not “happiness” (G). Although “good” is mentioned, the answer
specifies “happiness” at the start. As such, this demonstrates a failure mode of using
LLMs to judge LLMs. They are not perfect by any means, just like human evaluation.
A mix of evaluation metrics and benchmarks is generally preferred to limit the
downsides of any one benchmark.
What We Built
TinyAgent/
├── agent.py
├── evaluator.py ← New (Run a `TinyAgent` over a `Benchmark`)
├── llm.py
├── memory.py
├── planning.py
├── toolbox.py
├── tools.py
└── trajectory.py
Rubric-based evaluation
A refinement on the raw LLM-as-a-judge approach is to give the judge an explicit
rubric: a structured set of criteria, each with defined score levels. Instead of asking
a single “Is this output good?” you score the output against multiple criteria, each
capturing a different axis of quality. You ask something more like “On a scale of
1–3, does this response correctly cite evidence from the provided sources? Score 1 if
no sources are cited, score 2 if sources are cited but not directly relevant, score 3 if
sources are cited and directly support the claim.”
Notable rubric-based benchmarks include ScholarQABench and HealthBench, both of
which provide detailed and structured rubrics that score many facets of the targeted
task. Each of these rubric items can be scored by a model judge.
In Figure 7-7, we see an example of using a rubric that scores outputs based on
four categories: fluency, correctness, completeness, and groundedness. To score each
of these axes, a rubric would contain examples such as these (summarized from
ScholarQABench’s Coverage rubric):
Score 1: Severely lacking
Misses core lines of research or fixates on a single work, with little usable depth
|
Chapter 7: Evaluating Agents

Score 2: Partial
Covers some key aspects but misses significant research or stays too narrow
Score 3: Acceptable
Discusses several representative works and gives a satisfactory overview, though
more sources or points would strengthen it
Score 4: Good
Covers a variety of representative papers and sources, missing only minor areas
Score 5: Comprehensive
Spans a diverse range of papers and viewpoints, and even surfaces important
points beyond what the question asked



![Figure 7-7: A detailed rubric decomposes output quality into named dimensions, each](images/fig_07-07_A_detailed_rubric_decomposes_output_qual.png)

*Figure 7-7: A detailed rubric decomposes output quality into named dimensions, each*


Figure 7-7. A detailed rubric decomposes output quality into named dimensions, each
scored independently to guide evaluation
Rubrics improve evaluation reliability because they break a complex judgement
into smaller, more objective criteria. They also allow us to evaluate individual sub-
behaviors of the agent, which can give us a much more high-resolution signal about
where specifically the agent is performing well or breaking down.
Outcome Evaluation: Did the Agent Get the Right Output?
|