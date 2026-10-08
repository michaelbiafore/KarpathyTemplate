---
title: "Summary"
chapter_number: 97
page_start: 280
page_end: 280
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Summary



![Figure 6-26: Test-time training moves compute more during inference where we can](images/fig_06-26_Test-time_training_moves_compute_more_du.png)

*Figure 6-26: Test-time training moves compute more during inference where we can*


Figure 6-26. Test-time training moves compute more during inference where we can
more easily scale existing models
Summary
In this chapter, we explored how LLMs can plan out behavior and reflect on actions
taken when executing this plan. We covered how task decomposition allows LLMs
to break down complex problems into small problems that each can be solved on its
own. CoT-like techniques were explored and demonstrated how they can be used to
perform explicit planning. We then explored how, after planning, agents can perform
sequences of actions through a widely used technique, Reason and Act. Several
techniques were explored from the domains of prompting, SFT, and RL to enable this
behavior of action sequencing in agents. ReAct is the final missing link in what makes
agents potentially autonomous, as it decides on its own when to stop and how long to
continue within these ReAct-like frameworks.
We then discussed how agents can be taken a step further and reflect on their
sequences of actions to get into a mode of self-improvement. In that, reflection is
vital for LLMs and agents to prevent being stuck in local minima of solutions and
thought processes. We finished this chapter with an exciting new paradigm of agents
that continuously improve as they interact with their environment. This test-time
training paradigm has the potential to bring agents into a new realm of performance
and generalization.
In the next chapter, we’ll cover various methodologies of evaluating agents. Due to
their potentially complex behaviors, agents are significantly more difficult to evaluate
than LLMs. We’ll explore what to look for when evaluating your agent and agentic
system.
|
Chapter 6: Planning and Reflection