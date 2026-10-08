# Self-Improvement through Outcome Evaluation (Chapters 96–107)

## Self-Improvement

Reflection alone is a prompt-level heuristic; continual improvement needs parameter-level change, and RL delivers it with almost no labeled data. RISE iterated over attempts with introspection; two newer methods go further. **Test-Time Reinforcement Learning (TTRL)** updates the model during inference: given a query it samples candidates (16 at temperature 0.6, across Qwen, LLaMA, Mistral and DeepSeek), picks a winner by majority vote, turns agreement with that vote into a reward, and feeds the rewards to GRPO.

![Figure 6-21: In Test-Time Reinforcement Learning (TTRL), GRPO is used on the sam‐](images/fig_06-21_In_Test-Time_Reinforcement_Learning_TTRL.png)

*Figure: TTRL samples many answers to one query, scores each 1/0 against the most frequent answer, and feeds that reward vector back through GRPO.*

Majority voting is fallible, but vague rewards push exploration rather than trapping the model in local minima — and when the majority is wrong, samples disagreeing with it still earn correct negative rewards ("lucky hits"). **R-Zero** extends this to two models from one base: a Challenger inventing queries hard for a Solver, and the Solver answering them. The Challenger trains on a composite reward (uncertainty minus repetition penalty, plus a format reward) steering it toward queries at the edge of solvability; the Solver then trains on a filtered set of them with a binary reward. The asymmetry is deliberate: continuous reward lets the Challenger explore difficulty, binary reward keeps the Solver precise.

![Figure 6-25: Challenger and Solver training are done after each other. In this process, the](images/fig_06-25_Challenger_and_Solver_training_are_done.png)

*Figure: The coevolution loop — Challenger training (right, Solver frozen) alternates with Solver training (left, Challenger frozen), each GRPO-driven.*

## Summary (Chapter 6)

The chapter closes by tying together task decomposition, CoT planning, ReAct sequencing and reflection, framing test-time training as a shift of compute toward inference.

![Figure 6-26: Test-time training moves compute more during inference where we can](images/fig_06-26_Test-time_training_moves_compute_more_du.png)

*Figure: Three generations — non-reasoning LLMs (compute almost all at train time), reasoning LLMs (long inference), and test-time training (RL on unlabeled data during inference).*

## Evaluating Agents

Evaluation moves you from "it seems to work" to "I have evidence it works," and is among the most underinvested areas in agent development — teams lean on intuition until they can neither ship confidently nor diagnose regressions.

![Figure 7-01: This chapter covers how LLMs and agents are evaluated and explores how we](images/fig_07-01_This_chapter_covers_how_LLMs_and_agents.png)

*Figure: The agent loop with Chapter 7 marked at the Answer edge — evaluate the final output, and also the process (steps, efficiency) along the feedback path.*

## Public Benchmarks and Leaderboards

A benchmark is a fixed task set plus a scoring procedure: dataset, attempt protocol, single number. SWE-bench Verified scores the share of real GitHub issues an agent patches so hidden tests pass. The danger: 80% on SWE-bench and 80% on MMLU are incomparable claims about different capabilities.

![Figure 7-02: A benchmark table from Google](images/fig_07-02_A_benchmark_table_from_Google.png)

*Figure: A vendor comparison table — Humanity's Last Exam, ARC-AGI-2, GPQA Diamond, Terminal-Bench 2.0, SWE-Bench Verified/Pro and LiveCodeBench Pro across six frontier models, with harness and attempt conditions in fine print.*

## Benchmark Families

*(Chapters 100–105 are one catalog, folded here.)* **Coding** is the most mature family because code is verifiable — SWE-bench went from ~2% solved in 2023 to over 70% on Verified by 2026; Terminal-Bench puts the agent in a Linux terminal. **Tool use**: BFCL (function-calling accuracy over hundreds of API schemas), τ-bench (multi-turn policy adherence). **Computer use**: OSWorld (desktop GUIs), WebArena (replica websites). **Real-world tasks**: GAIA and GDPval; the 2026 analysis *How Well Does Agent Development Reflect Real-World Work?* found benchmarks cluster around programming while high-employment occupations go untested. **Reasoning and knowledge**: MMLU, GPQA Diamond, Humanity's Last Exam — mostly testing the underlying LLM, not agentic capability. **Specialized**: ARC-AGI, MMMU, needle-in-a-haystack retrieval.

## Reading Benchmark Scores Critically

Ten questions separate seasoned readers from score-takers: how the score was produced (deterministic test vs. LLM judge); whether partial credit is given (it hides agents that never finish end to end); which agentic harness was used — SWE Atlas runs models in vendor harnesses and in a minimal bash-only one, and rankings flip, so a score is a model-and-harness pair; single run or variance-aggregated (pass@k); training-data contamination; who ran it (self-reported vs. Artificial Analysis or Chatbot Arena — gameable too, per *The Leaderboard Illusion*); whether prompts were tuned for it; whether the scaffolding generalizes; whether it is saturated (past ~85%, differences are noise); which variant (GPQA vs. Diamond, MMLU vs. MMLU-Pro); and cost — a system scoring 20% higher at 10x the tokens is not straightforwardly better.

## Outcome Evaluation: Did the Agent Get the Right Output?

Outcome evaluation scores the final artifact — patch, answer, report — ignoring how the agent got there; trajectory evaluation (later) scores the steps. The most direct method is human: an annotator reads the output and scores it against criteria.

![Figure 7-03: A human evaluator rates a single agent output against scoring criteria,](images/fig_07-03_A_human_evaluator_rates_a_single_agent_o.png)

*Figure: Generation and evaluation split — the agent turns a task prompt into an output, then a human applying scoring criteria returns 4/5.*

Absolute scores are hard to assign consistently, which motivates **preference evaluation**: two agents' outputs side by side, with one question — which is better? Relative judgments are more reliable; it is easier to say A beats B than that A deserves 4 and B deserves 3.
