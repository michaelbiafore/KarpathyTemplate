---
title: "Measuring Capability with pass@k"
chapter_number: 112
page_start: 303
page_end: 305
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Measuring Capability with pass@k



![Figure 7-9: Three correct outcomes, three different problems in the trajectory. Agent A](images/fig_07-09_Three_correct_outcomes_three_different_p.png)

*Figure 7-9: Three correct outcomes, three different problems in the trajectory. Agent A*


Figure 7-9. Three correct outcomes, three different problems in the trajectory. Agent A
guessed and got lucky, Agent B spent several tool calls where one would do, and Agent
C made the right tool call but overthought its way there. Outcome evaluation passes all
three; only trajectory evaluation tells them apart.
These three failure modes are distinct enough to warrant separate measurement:
unsound reasoning, inefficiency, and unnecessary overhead. Measuring a trajectory
means scoring the steps along the way, not just the endpoint. A few axes do most of
the work. Did the agent reach for the right tools and pass them valid arguments? How
efficiently did it get there, in tool calls, steps, and reasoning tokens? Did each step
follow reasonably from what the agent learned in the steps before it?
These questions can be put to an LLM judge that is handed the full trajectory to
observe. As we saw earlier, that is a rubric, just one that examines the steps and
not just the final output. Works such as T-Eval (2024), AgentBoard (2024), TRACE
(2025), and AgentProcessBench (2026) formalize this approach, introduce measures
for individual steps in the trajectory, and show how this line of evaluation has been
tracking over the last several years.
Reliability: Does It Succeed Every Time?
Just like LLMs, agent outputs are stochastic: the same input can produce different
outputs across runs, which means a single run score can flatter or unfairly penalize
an agent. A better picture comes from running multiple trials of the same task and
measuring how often the agent succeeds. From these trials you can read two different
things: how capable the agent is, meaning whether it can succeed at all, and how
reliable it is, meaning whether it succeeds every time. The following two metrics
measure each.
Measuring Capability with pass@k
When evaluating agents on tasks with a clear pass or fail check, one metric stands
out for measuring capability while accounting for the probabilistic nature of the
underlying model.
Reliability: Does It Succeed Every Time?
|

Imagine that we’re comparing two models on a single problem, as we see in Fig‐
ure 7-10. We can generate a single solution and measure its correctness, but if we
use only one sample then the model might simply be lucky in that single generation.
So let’s sample two solutions for the same problem from each model so we have
more data to compare against. If you’re starting to think about the temperature value,
then you’re thinking of the right parameter. We’re assuming a temperature value that
allows for a certain amount of variance, so say something like 0.7.



![Figure 7-10: Two models, each sampled twice on the same problem, with every solution](images/fig_07-10_Two_models_each_sampled_twice_on_the_sam.png)

*Figure 7-10: Two models, each sampled twice on the same problem, with every solution*


Figure 7-10. Two models, each sampled twice on the same problem, with every solution
checked against held-out tests. LLM 1 passes both of its samples and LLM 2 only one, so
the two differ on pass@1, 1.0 against 0.5, but tie on pass@2 at 1.0, since each produced
at least one passing solution.
We can use the two samples to compute a pass@1, which shows us that LLM 1 is
better than LLM 2 in this problem. For pass@1, the formula is simply to divide the
number of correct answers by the total number of samples. So for LLM 1, that’s 2/2 =
1 and for LLM 2 that’s 1/2 = 0.5.
Note that using the same data, we can also compute a pass@2 score, which is 1
for both models, since each produced at least one correct sample across its two
attempts. But this is exactly where small samples mislead. A pass@k estimate is only
trustworthy when the number of samples is much larger than k, and here we have just
two samples at k=2. With more samples, that inflated number would settle lower.
So a more rigorous way would be to run, say, 100 samples, then calculate the pass@k
as we can see in Figure 7-11.
|
Chapter 7: Evaluating Agents



![Figure 7-11: The same setup scaled to 100 samples per model, where the pass@k esti‐](images/fig_07-11_The_same_setup_scaled_to_100_samples_per.png)

*Figure 7-11: The same setup scaled to 100 samples per model, where the pass@k esti‐*


Figure 7-11. The same setup scaled to 100 samples per model, where the pass@k esti‐
mates become far more trustworthy. LLM 1 passes 85 of its 100 samples (pass@1 0.85,
pass@2 0.98) and LLM 2 passes 45 (pass@1 0.45, pass@2 0.70).
Statistically, we can assign more confidence to these scores because they provide
more coverage of probable model outputs. And because we have 100 samples, we can
calculate results at higher values of k such as 4, 8, 16, 32, etc.
To calculate pass@k for values of k over 1, we can use the following snippet adap‐
ted from Evaluating Large Language Models Trained on Code,3 which is statistically
more robust than the simple division (which works perfectly for pass@1) because
it accounts for the dependency between samples when drawing k candidates, while
simple division assumes independence and breaks down once k exceeds 1:
import numpy as np

def pass_at_k(n_samples, n_correct_samples, k):
 """
 :param n_samples: total number of samples
 :param n_correct_samples: number of correct samples
 :param k: k in pass@k
 """
 if n_samples - n_correct_samples < k:
```
 return 1.0
 return 1.0 - np.prod(
```
3 Chen, Mark et al. 2021. “Evaluating Large Language Models Trained on Code,” arXiv, 2107.03374.
Reliability: Does It Succeed Every Time?
|