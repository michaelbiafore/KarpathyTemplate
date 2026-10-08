---
title: "The Paradigm Shift from Train-Time Compute to Test-Time Compute"
chapter_number: 38
page_start: 106
page_end: 106
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# The Paradigm Shift from Train-Time Compute to Test-Time Compute

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