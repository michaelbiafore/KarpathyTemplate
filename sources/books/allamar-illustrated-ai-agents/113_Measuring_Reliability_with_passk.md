---
title: "Measuring Reliability with pass^k"
chapter_number: 113
page_start: 306
page_end: 307
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Measuring Reliability with pass^k

1. 0 - k / np.arange(n_samples - n_correct_samples + 1, n_samples + 1)
 )
Measuring Reliability with pass^k
The pass@k metric rewards an agent for succeeding at least once in k tries, so
it climbs as you grant more attempts. That makes it a measure of capability, not
reliability. For reliability, you want the answer to the opposite question: does the
agent succeed every single time?
That is pass^k (pass-HAT-k, sometimes written passk), the probability that all k of k
sampled attempts succeed. The same runs give you both metrics, and they can tell
very different stories.
Figure 7-12 shows pass^3, pass@1, and pass@3 for a number of models on Codebase
QnA. Notice how the first and third models, GPT-5.4 and Opus 4.7 have the same
pass@1 score of 40. If we stopped the evaluation there, we’d think they’re tied at the
same level of performance. But by looking at their pass^3 values we can see that
GPT-5.4 is more reliable, with a pass^3 of 28 compared to Opus 4.7’s score of 23.
Paradoxically, the highest pass@3 in the list belongs to Opus 4.7, at 60: given 3 tries,
it lands at least one success on more tasks than any other model here. So how do we
make the best use of this signal?
If we were in the middle of a training process and choosing between candidate
checkpoints, the higher pass@3 would be the one we select because that capability
ceiling indicates we can get more performance from the model with further training.
When comparing between API vendors, however, that ceiling is mostly out of reach
because we’re choosing a model to run as it ships, not to train.
Computing pass^k follows the same combinatorial logic as pass@k, flipped. pass@k
estimates the chance that at least one of k samples drawn from your n is correct;
pass^k estimates the chance that all of them are. From c correct samples out of n,
that is the count of all-correct k-subsets over the count of k-subsets in total, C(c, k) /
C(n, k):
from math import comb

def pass_hat_k(n_samples, n_correct_samples, k):
 """Probability that all k randomly drawn samples are correct."""
 if n_correct_samples < k:
```
 return 0.0
 return comb(n_correct_samples, k) / comb(n_samples, k)
```
This estimator comes from τ-bench (Yao et al., 2024), which introduced pass^k to
measure whether tool-using agents hold up across repeated trials instead of only on
their best attempt.
|
Chapter 7: Evaluating Agents



![Figure 7-12: Pass³, pass@1, and pass@3 across 10 models on the SWE Atlas Codebase](images/fig_07-12_Pass³_pass1_and_pass3_across_10_models_o.png)

*Figure 7-12: Pass³, pass@1, and pass@3 across 10 models on the SWE Atlas Codebase*


Figure 7-12. Pass³, pass@1, and pass@3 across 10 models on the SWE Atlas Codebase
QnA benchmark. For each model the three dots run left to right from pass³ (all three
trials pass), through pass@1 (the single-trial average), to pass@3 (at least one of three
passes); the spread between pass³ and pass@3 is the model’s reliability gap. Pass³ and
pass@3 are the same metrics the text writes as pass^3 and pass@3. Adapted from M.
Raghavendra et al., 2026. “SWE Atlas,” arXiv:2605.08366.
Reliability: Does It Succeed Every Time?
|