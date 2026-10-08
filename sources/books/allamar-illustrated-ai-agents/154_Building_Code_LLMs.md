---
title: "Building Code LLMs"
chapter_number: 154
page_start: 430
page_end: 433
part: "Part II. Specialized Agents"
---
# Building Code LLMs

What We Built
TinyAgent/
├── agent.py ← Updated (Add the Display to your TinyAgent)
├── cli.py ← New (Use the new TinyAgent with Display in the CLI)
├── display.py ← New (Added a Display to visualize ReAct loops)
├── evaluator.py
├── llm.py
├── memory.py
├── planning.py
├── toolbox.py ← Updated (Added various coding tools)
├── tools.py
└── trajectory.py
As you experiment, you’ll find the biggest lever on your agent’s behavior is the model
behind it. That’s where we turn next: what it takes to train an LLM capable of
powering a coding agent.
Building Code LLMs
The quality of a coding agent is limited, in large part, by the quality of the model
powering it. Not only must the model exhibit high performance on writing code, but
it should also be skilled at tool use and agentic software engineering tasks for it to
be capable of powering a coding agent. In this section, we’ll provide an overview on
how coding LLMs are created according to model training recipes up until the time of
writing (Figure 10-18).



![Figure 10-18: The training stages of a coding agent: language modeling, supervised](images/fig_10-18_The_training_stages_of_a_coding_agent_la.png)

*Figure 10-18: The training stages of a coding agent: language modeling, supervised*


Figure 10-18. The training stages of a coding agent: language modeling, supervised
fine-tuning, and reinforcement learning
|
Chapter 10: Code Agents and Code LLMs

The main areas to note when compared to a generalist LLM are:
The data
Data composition: These models have to see a lot more code data in the various
training stages. Qwen3 Coder, for example, is pre-trained on 7.5 trillion tokens,
70% of which is code.
Coding task data: To better serve as engines that power coding agents, coding
LLMs need to be trained on data that looks like what the model will see when it’s
in use, which includes:
Tool-use data
Trajectories where the model calls a tool and uses the result, like running
grep to locate a function and then acting on what it finds
Multi-step data
Tasks that play out over several turns, like reproducing a bug, editing a file,
running the tests, reading the failure, and patching again
Unit-test data
Code paired with the tests that verify it, like a function alongside the pytest
cases that exercise it
Software engineering tasks
Repository-level issues and the changes that resolve them, like a GitHub
issue paired with the diff that closes it.
Reinforcement learning
Now a major component of the training flow. Where in the past Reinforcement
Learning from Human Feedback (RLHF) had been useful to polish the behavior
of a model, coding LLMs are trained with large-scale Reinforcement Learning
with Verifiable Rewards (RLVR) as we covered in Chapter 2.
Building Code LLMs
|

Some of the types of coding data are shown in Figure 10-19.



![Figure 10-19: The specific types of code-related datasets used during each stage of](images/fig_10-19_The_specific_types_of_code-related_datas.png)

*Figure 10-19: The specific types of code-related datasets used during each stage of*


Figure 10-19. The specific types of code-related datasets used during each stage of
training a coding agent
While coding data is important, other capabilities are just as important for an LLM
to successfully empower a coding agent. These include reasoning, multi-step tool
calling, long-context, and planning, as well as trajectories that demonstrate proper
software engineering practices (how to reproduce issues, how to use coding tools and
common libraries…etc.).
For a sense of how much data each stage demands, open source model GLM-5’s
pipeline is a useful current example (Figure 10-20): pre-training on the order of 28
trillion tokens, mid-training that extends context out to 200K with long code and
agent data, SFT, and then RL split into reasoning, agentic, and general stages before a
final distillation step.
|
Chapter 10: Code Agents and Code LLMs



![Figure 10-20: In GLM-5’s full training pipeline, the token counts and context lengths at](images/fig_10-20_In_GLM-5s_full_training_pipeline_the_tok.png)

*Figure 10-20: In GLM-5’s full training pipeline, the token counts and context lengths at*


Figure 10-20. In GLM-5’s full training pipeline, the token counts and context lengths at
each stage give a sense of how much data building a competitive frontier model takes7
Bootstrapping Intelligence: The Synthetic Data Feedback Loop
A key inflection point that many outside the research industry may not know is
that around 2024, LLMs became a major source of the training data for the next
generation of LLMs. You start to see that more clearly with a lot of the Llama 3.1
post-training data actually having been generated with Llama 3. This repeats itself
with math and code; Qwen2.5-Math and Qwen2.5-Coder were both essential in
creating training data for Qwen3 and Qwen3-Coder. And as we saw in Chapter 3
with DeepSeek-R1, a lot of long chains of priceless reasoning traces were generated by
DeepSeek-R1-Zero (Figure 10-21).
7 Source: GLM-5 technical report (Zhipu AI et al. 2026).
Building Code LLMs
|