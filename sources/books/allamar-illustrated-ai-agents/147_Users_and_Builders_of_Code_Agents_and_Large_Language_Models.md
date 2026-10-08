---
title: "Users and Builders of Code Agents and Large Language Models"
chapter_number: 147
page_start: 397
page_end: 399
part: "Part II. Specialized Agents"
---
# Users and Builders of Code Agents and Large Language Models

Code Agents and Code LLMs
Coding agents are some of the most potent types of AI agent in terms of the size
of their likely impact. Code generation became one of the earliest applications of
LLMs once they hit the scale of GPT-3 in 2020. As we saw in Chapter 3, code
generation was also a major component for reasoning problems that reasoning LLMs
tackle. Code is a key investment area for LLMs for two reasons. First, an enormous
range of knowledge work, from software engineering to research, data analysis, and
visualization, can be expressed as code. Second, and more useful for training, code
can often be verified automatically: you can run it, or test it, and get a clear signal
of whether it worked. That verifiability is what makes coding more tractable than
open-ended tasks where there is no objective check.
This chapter walks through that world. We’ll meet the people who use and build code
agents, see what makes software engineering agents distinct, build one ourselves, and
finish with how the underlying code LLMs are trained.
Users and Builders of Code Agents
and Large Language Models
Before we get into how code agents are built, it helps to know who they’re for, because
the people who use and build them have very different needs. Figure 10-1 lays out the
cast.



![Figure 10-1: The target audience for code agents, ranging from end users to professional](images/fig_10-01_The_target_audience_for_code_agents_rang.png)

*Figure 10-1: The target audience for code agents, ranging from end users to professional*


Figure 10-1. The target audience for code agents, ranging from end users to professional
software developers and AI researchers
Broadly, there are users and there are builders. Users of coding agents fall into three
groups that differ in how closely they work with the code itself: those who just want
a non-code output like a chart or an analysis and may never see the code; vibe coders
who want working software but build it through natural language and let the agent
handle the details; and software engineers who read, review, and direct the agent
inside a codebase. Builders are split in two: those who build the agents, assembling
the tools, context, and loop around a model, which we will do ourselves later in this
chapter, and those who train the coding LLMs that everything else depends on.
People often ask LLMs to generate code. Coding agents take this to a whole new
level by having the ability to execute that code, debug any errors it produces, and
iterate over multiple steps to solve bigger and bigger problems. The three examples in
Figure 10-2 show the evolution from coding generation with LLMs to more advanced
code agent use cases.
|
Chapter 10: Code Agents and Code LLMs



![Figure 10-2: Coding agents take LLM capabilities of generating code to the next level and](images/fig_10-02_Coding_agents_take_LLM_capabilities_of_g.png)

*Figure 10-2: Coding agents take LLM capabilities of generating code to the next level and*


Figure 10-2. Coding agents take LLM capabilities of generating code to the next level and
enable solving more complex problems
The first shows a common pattern of asking LLMs, mostly within a playground UI,
to write a specific piece of code. The second is more important because the user
here doesn’t have to be a developer. In this example, the LLM has generated the
code, executed it in an execution environment, and then presented the results to the
user. Flows like this open up coding agents to a massive audience of users. The third
example demonstrates using code agents to help the software development process.
Here the agent solves larger tasks that can include tens or even hundreds of steps
before that final result is produced. Here it also has to rely on a richer execution
environment.
In this chapter, we’ll start by looking at how coding agents are built and the tools they
rely on. We’ll then go into more detail into the LLM that powers such an agent and
what makes a model a better fit to power coding agents.
Users and Builders of Code Agents and Large Language Models
|