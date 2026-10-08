# Evaluating Agents: Outcomes, Trajectories, and Reliability

## Human Evaluation

Outcome evaluation scores the final result of a task — the patch, the answer, the report — without regard to how the agent got there. The most direct form is human scoring: an annotator reads one output and assigns an absolute score against stated criteria. That works only when quality is judgeable in isolation, which it often isn't. Preference evaluation sidesteps the problem by showing two agents' outputs side by side and asking "which do you prefer?" Relative judgments are more reliable — it is easier to say A beats B than to decide A is a 4 and B a 3. Aggregated across a task suite, preferences become a win rate.

![Figure 7-5: Human evaluators compare agent outputs across a task suite, and per-task](images/fig_07-05_Human_evaluators_compare_agent_outputs_a.png)

*Figure: Per-task pairwise preferences across Task 1..N aggregate into a win rate — Agent A 80%, Agent B 20%.*

## Automated Evaluation

Pairwise comparison extends to many models through an Elo-style rating (Chatbot Arena/LMSYS is the canonical large-scale instance). Human evaluation stays the baseline automated methods are validated against — correlation with human judgment is how a new metric earns credibility — but it cannot keep up with the thousands of prompt tweaks, model swaps, and agent versions a builder iterates through. The chapter builds a small TinyAgent harness: a `Benchmark` dataclass (name, examples, scorer) and an `Evaluator` that spins up a fresh agent per example and averages a `pass_rate`. Four scoring methods follow. **Exact match** is deterministic and powers many benchmarks (MMLU-Pro, 10 options A–J; TinyAgent scores 0.33), but breaks on open-ended output and trivial formatting drift (`1482.81` vs `$1,482.81.`). **Programmatic checks** generalize to verifiers — valid JSON, unit tests, SWE-bench patches that must flip a failing suite to passing; IFEval's per-instruction validators give TinyAgent a 1.0. Cheap, objective verification is much of why coding agents advanced fastest. **LLM-as-a-judge** handles open-ended output, scoring absolutely or by preference.

![Figure 7-6: A judge model takes agent outputs and scoring criteria as input and evalu‐](images/fig_07-06_A_judge_model_takes_agent_outputs_and_sc.png)

*Figure: A judge model plus scoring criteria either picks the preferred output or assigns each an absolute score.*

Judges have real failure modes: preferring confident-sounding over correct, position bias, and favoring their own model family — mitigated by cross-family judges, order swapping, written rationales, and judge ensembles. Re-running MMLU-Pro open-ended through a Gemini judge yields 0.8, and ==the judge wrongly awards 1.0 to "happiness" where ground truth was "good"==. **Rubric-based evaluation** refines this: decompose quality into named axes with defined score levels (ScholarQABench, HealthBench).

![Figure 7-7: A detailed rubric decomposes output quality into named dimensions, each](images/fig_07-07_A_detailed_rubric_decomposes_output_qual.png)

*Figure: A rubric splits judging into fluency, correctness, completeness, and groundedness, each scored independently per output.*

## Trajectory Evaluation: Did It Get There the Right Way?

Outcome evaluation says whether the agent succeeded; trajectory evaluation says how. A trajectory is the full sequence — reasoning, tool calls, arguments, intermediate outputs. Aggregate tool-call statistics across runs expose signatures invisible in outcome scores.

![Figure 7-8: Tool-use distribution across the trajectory for three models on the same](images/fig_07-08_Tool-use_distribution_across_the_traject.png)

*Figure: GPT-5.4 front-loads search and file ops then shifts to execution, while Opus 4.6 and Gemini 3.1 Pro stay flat across the trajectory.*

## Reliability: Does It Succeed Every Time?

Individual trajectories matter too: three agents can all return the right answer for different wrong reasons.

![Figure 7-9: Three correct outcomes, three different problems in the trajectory. Agent A](images/fig_07-09_Three_correct_outcomes_three_different_p.png)

*Figure: Agent A guesses and gets lucky, Agent B burns five tool calls where one suffices, Agent C overthinks before one correct call — outcome evaluation passes all three.*

Those failure modes — unsound reasoning, inefficiency, overhead — warrant separate measurement along a few axes: right tools with valid arguments, efficiency in calls/steps/reasoning tokens, and whether each step follows from the last. Hand the full trajectory to an LLM judge and that is simply a rubric over steps, formalized by T-Eval, AgentBoard, TRACE, and AgentProcessBench. Because agent output is stochastic, a single run flatters or unfairly penalizes; multiple trials separate *capability* (can it succeed at all) from *reliability* (does it succeed every time).

## Measuring Capability with pass@k

pass@k measures capability under stochastic sampling. Sample each model twice at a temperature like 0.7: pass@1 is correct/total (LLM 1 scores 1.0, LLM 2 scores 0.5), but both tie at pass@2 = 1.0 — the trap, since a pass@k estimate is only trustworthy when samples greatly exceed k.

![Figure 7-11: The same setup scaled to 100 samples per model, where the pass@k esti‐](images/fig_07-11_The_same_setup_scaled_to_100_samples_per.png)

*Figure: At 100 samples per model, checked against held-out tests the model never sees, LLM 1 scores 85 correct (pass@1 0.85, pass@2 0.98) against LLM 2's 45 (0.45, 0.70).*

With 100 samples you can report k = 4, 8, 16, 32. For k > 1, use the unbiased estimator from the Codex paper (`pass_at_k`), which accounts for dependency between drawn candidates where simple division wrongly assumes independence.
