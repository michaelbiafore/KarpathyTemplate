---
title: "Chapter 10. Code Agents and Code LLMs"
chapter_number: 146
page_start: 397
page_end: 397
part: "Part II. Specialized Agents"
---
# Chapter 10. Code Agents and Code LLMs

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