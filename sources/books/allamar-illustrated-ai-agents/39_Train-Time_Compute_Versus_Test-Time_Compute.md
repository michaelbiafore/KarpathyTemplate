---
title: "Train-Time Compute Versus Test-Time Compute"
chapter_number: 39
page_start: 106
page_end: 108
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Train-Time Compute Versus Test-Time Compute

The Paradigm Shift from Train-Time Compute
to Test-Time Compute
Before we explore reasoning LLMs in more detail, it’s important to discover why
there is such a big focus on them currently. This relates to a fundamental shift that
has changed our focus from scaling train-time compute to test-time compute.
Train-Time Compute Versus Test-Time Compute
To improve the performance of LLMs during pre-training, developers used to focus
on three main factors (see Figure 3-4):
- Increasing the model size (number of parameters)
•
- Increasing the dataset size (number of tokens)
•
- Increasing compute (number of floating point operations per second [FLOPs])
•
This combination of factors, called train-time compute, has been a key strategy. The
basic principle is that more pre-training resources lead to a better, more powerful
model.



![Figure 3-4: Train-time compute relates to the entire training process of LLMs](images/fig_03-04_Train-time_compute_relates_to_the_entire.png)

*Figure 3-4: Train-time compute relates to the entire training process of LLMs*


Figure 3-4. Train-time compute relates to the entire training process of LLMs
When we explore train-time compute, it does not only relate to pre-training but also
what you can tweak during post-training. In Figure 3-5, you can see how both data
and compute can also be increased to improve its performance. When you fine-tune
a model, you can often decide how many of its parameters you would like to update.
In a way, even during post-training, you can increase the “model size.”
|
Chapter 3: Reasoning Large Language Models



![Figure 3-5: Train-time compute relates to both pre-training and post-training LLMs](images/fig_03-05_Train-time_compute_relates_to_both_pre-t.png)

*Figure 3-5: Train-time compute relates to both pre-training and post-training LLMs*


Figure 3-5. Train-time compute relates to both pre-training and post-training LLMs
Shown in Figure 3-6, train-time compute means a focus on increasing pre-training
and post-training resources, and little attention is spent on inference. This generally
applies to non-reasoning LLMs.



![Figure 3-6: The distribution of train-time compute when training non-reasoning LLMs](images/fig_03-06_The_distribution_of_train-time_compute_w.png)

*Figure 3-6: The distribution of train-time compute when training non-reasoning LLMs*


Figure 3-6. The distribution of train-time compute when training non-reasoning LLMs
In contrast, test-time compute focuses more on scaling inference instead of pre-
training and post-training. Scaling inference generally applies to reasoning LLMs
and allows them to “think longer” during inference.
Let’s illustrate this with an example. Figure 3-7 shows how non-reasoning LLMs
directly generate an answer without any intermediate generated tokens. To the ques‐
tion, “What is 3 + 2?,” it answers “5.” All of its compute is used to generate this one
token.
In this example, scaling inference means generating more tokens in the output so
that the model has spent more resources getting to the final answers. Simplified, if
one token is one “compute,” then dozens of tokens would mean dozens of “compute.”
“Compute” can mean several things, but it generally refers to how much computa‐
tional work the model performs during inference.
The Paradigm Shift from Train-Time Compute to Test-Time Compute
|



![Figure 3-7: Non-reasoning LLMs output only the answer. Although this may include](images/fig_03-07_Non-reasoning_LLMs_output_only_the_answe.png)

*Figure 3-7: Non-reasoning LLMs output only the answer. Although this may include*


Figure 3-7. Non-reasoning LLMs output only the answer. Although this may include
reasoning or prefixes such as “The answer is…”, the reasoning is not a separate stage.
This is especially true for reasoning models, as they would use more tokens (which
we can think of as “thinking” tokens) to derive their answer (Figure 3-8).



![Figure 3-8: Each token requires computational resources to generate, which adds up the](images/fig_03-08_Each_token_requires_computational_resour.png)

*Figure 3-8: Each token requires computational resources to generate, which adds up the*


Figure 3-8. Each token requires computational resources to generate, which adds up the
more tokens that are generated
The underlying idea is that the more tokens you generate, the better the resulting
performance will be. However, you cannot just produce many random tokens to
get a better output. Instead, tokens need to be generated that, for instance, contain
additional relationships and new thoughts about the original problem.
|
Chapter 3: Reasoning Large Language Models