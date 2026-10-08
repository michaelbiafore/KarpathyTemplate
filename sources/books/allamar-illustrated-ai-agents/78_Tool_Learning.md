---
title: "Tool Learning"
chapter_number: 78
page_start: 215
page_end: 215
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Tool Learning

Let’s run a simple query to see if it can properly choose, parse, and execute its tool:
# A query that requires the use of a tool
agent.run("What is 5.1 times 7.3?")
This gives us:
'OBSERVATION: 37.23'
This is the correct answer, but did the model do that calculation by itself, or did it use
a tool? To find out, let’s inspect the full conversation history:
print(agent.memory.get_messages())
This gives us:
[
 {
 'role': 'system',
 'content': 'You are a helpful assistant.\n\n\n# Tools\n\n
 If needed, you can only use the following },
 {
 'role': 'user',
 'content': 'What is 5.1 times 7.3?'},
 {
 'role': 'assistant',
 'content': '{"tool": "multiply", "kwargs": {"a": "5.1", "b": "7.3"}}\n'},
 {
 'role': 'user',
 'content': 'OBSERVATION: 37.23'}
]
It used the tool! Note that the assistant role returned a string with a JSON-like
structured output. Moreover, the user role was added with an observation of this
output.
With the many steps an LLM has to correctly follow to call the appropriate tool, it
requires the LLM to be an effective orchestrator, which is dependent upon the model’s
reasoning capabilities and overall reliability (as explored in Chapter 3).
A more stable approach tends to be to train a model on specific tool-calling tasks so
it can generalize better. Before, we briefly mentioned the use of the tool role. In the
next section, we explore in depth how models learn to use that.
Tool Learning
Instilling tool-calling capabilities into LLMs can be a difficult task, especially when an
LLM has not been trained to do so. Learning tools can be achieved through various
methodologies. In this section, we’ll explore the three most common categories of
tool learning, namely in-context learning, supervised fine-tuning, and reinforcement
learning.
Tool Learning
|