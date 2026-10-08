---
title: "Chapter 6. Planning and Reflection"
chapter_number: 90
page_start: 243
page_end: 243
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Chapter 6. Planning and Reflection

Planning and Reflection
In Chapter 3, we covered reasoning LLMs and their capabilities to demonstrate
complex chains of thought. Advanced reasoning enables behavior that is vital in
agentic systems, namely the ability to plan actions and reflect on them.
Agents are multi-step entities and generally require planning the actions they will
take to complete their goals. Imagine you ask an agent to create a specific feature for
your codebase. To bring this to completion, typical steps the agent takes include:
1. Clarify requirements
1.
2. Analyze the existing codebase
2.
3. Design the feature
3.
4. Implement the feature
4.
5. Test the feature
5.
6. Update documentation
6.
To execute all these actions, the agent first needs to be aware of them and track the
status of its current state. Planning is essential to solidify this behavior and to allow
the agent to dynamically adjust the plan when necessary. After all, without a plan,
how would it know what to do next?