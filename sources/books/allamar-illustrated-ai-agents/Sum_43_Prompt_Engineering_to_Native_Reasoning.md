# Prompt Engineering → Native Reasoning (Chapters 43–50)

## Prompt Engineering

Non-reasoning LLMs already hold reasoning ability in their parameters; prompting pulls it out. Chain-of-Thought (Wei et al., 2022) demonstrates the desired reasoning style in the prompt — one-shot (one example) or few-shot (two or more, generally more accurate). The worked example is blunt: given a terse exemplar on a penguin-counting puzzle, Gemma 3 12B answers wrong; given one that spells out the arithmetic, it reasons correctly.

![Figure 3-22: An example of one-shot learning where a single example is given to the](images/fig_03-22_An_example_of_one-shot_learning_where_a.png)
*Figure: a single worked Q/A exemplar teaches the model a reasoning-then-answer output structure, which it reproduces on a new question.*

Zero-shot CoT — just appending "Let's think step by step" (Kojima et al., 2022) — gets the same result with no examples. Ranking: zero-shot < one-shot < few-shot.

## Search Against Verifiers

That same prompt is all it takes to make TinyAgent reason. Search against verifiers builds on it: (1) sample many traces/answers, (2) score them with a reward model (an ORM judging outcomes or a PRM judging process), (3) pick the best — closer to majority voting or tree search than to thinking. Diversity comes from temperature. No retraining is needed; compute scales by sampling more or fewer answers.

## Self-Consistency

The earliest variant uses no verifier at all: sample N answers at high temperature with CoT, then take a majority vote.

![Figure 3-25: Self-consistency samples many thoughts and answers and will choose the](images/fig_03-25_Self-consistency_samples_many_thoughts_a.png)
*Figure: seven thought/answer pairs are generated and the most frequent answer wins, regardless of any quality score.*

On a seating puzzle, ten samples gave `{'5': 4, '1': 3, '2': 2, '4': 1}` — the plurality answer 5 being correct. It works because frequent answers are rarely the wildly wrong ones, but cannot rescue tasks the model almost never gets right.

## Best-of-N Samples

Add a real verifier: generate N candidates at high temperature, score each, keep the winner. ORMs score only final answers (LLM judge, unit tests, compiler); PRMs score each reasoning step and average across a trace.

![Figure 3-26: Best-of-N samples can use Outcome Reward Models (ORMs; left) and/or](images/fig_03-26_Best-of-N_samples_can_use_Outcome_Reward.png)
*Figure: answer-level ORM scoring contrasted with step-level PRM scoring averaged over each reasoning trace.*

The Roman-numeral example: ten generated `roman_to_int` functions scored against twelve test cases produced ==exactly one perfect 1.0==, the rest between 0.25 and 0.92.

## Modifying Proposal Distribution

The second test-time-compute category is input-focused: train the model so reasoning tokens are likelier up front. Every next-token distribution holds "answer" tokens (which trigger an immediate stop) and "reason" tokens (which open a chain of thought).

![Figure 3-30: Modifying the proposal distribution is essentially reranking the tokens such](images/fig_03-30_Modifying_the_proposal_distribution_is_e.png)
*Figure: reranking the distribution so reasoning openers like "Adding" and "If" outrank the direct answers 5, 3, 4.*

## Supervised Fine-Tuning

SFT achieves that reranking by training on (query, trace, answer) triplets. Flan-PaLM was the early example, mixing annotated CoT into 1,800+ instruction tasks — promptable to reason, but not yet a reasoning model. The s1 paper showed the data bar is low: ==1,000 curated question/trace pairs== turned Qwen2.5-32B-Instruct into a stable reasoner, using `<|im_start|>think` / `<|im_start|>answer` tokens to split the stages. They also scaled test-time compute directly, terminating thinking early or injecting "Wait" to force continuation — more thinking tokens, higher accuracy.

## Reinforcement Learning

DeepSeek-R1-Zero skipped SFT entirely: from DeepSeek-V3-Base, GRPO with only two rule-based rewards — accuracy, and format (correct `<think>`/`<answer>` tags). What the reasoning should look like was never specified.

![Figure 3-35: The training process of DeepSeek-R1-Zero](images/fig_03-35_The_training_process_of_DeepSeek-R1-Zero.png)
*Figure: the GRPO loop scoring format rewards (tags used?) and accuracy rewards (compiles? passes tests?) to iteratively update the base model.*

Reasoning emerged unprompted — the model discovered longer traces produce better answers, scaling its own test-time compute.

![Figure 3-36: An annotated figure from the DeepSeek-R1 paper demonstrating that the](images/fig_03-36_An_annotated_figure_from_the_DeepSeek-R1.png)
*Figure: average response length climbs from ~500 to ~10,000 tokens over 8,000 training steps, with no instruction to do so.*

The cost was a cold start: language mixing and unreadable output. Full DeepSeek-R1 fixed this in five steps — a ~5,000-sample SFT warm-up, reasoning RL with a language-consistency reward, rejection sampling to build 800,000 mixed samples, SFT on that set, then final RL adding helpfulness and harmlessness rewards.

## Native Reasoning

Using a trained reasoner comes down to the chat template. Gemma 4 E4B wraps turns in `<|turn>system`, `<|turn>user`, `<|turn>model` and `<turn|>`; reasoning is toggled by a single `<|think|>` token in the system turn — include it and the model emits a `<|channel>thought` block before answering, omit it and thinking is off. Ollama handles this parsing invisibly.
