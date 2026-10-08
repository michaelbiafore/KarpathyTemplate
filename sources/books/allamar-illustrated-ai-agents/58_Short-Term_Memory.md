---
title: "Short-Term Memory"
chapter_number: 58
page_start: 155
page_end: 155
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Short-Term Memory

an LLM through SFT. Note that this is not a stable method, as we are not entirely
sure beforehand which information gets retained explicitly and which is incorrectly
reconstructed.
Although these memory types may differ, they may not always be stored as such.
Depending on the specific implementation, they could be seen as one big pile of
information or separated into different databases to be remembered for specific tasks
and actions.
Short-Term Memory
Short-term memory in agents is the information it has about recent interactions, typ‐
ically the ongoing conversations with the user or the behavior of the LLM. Without
short-term memory, the LLM or agent does not know what was said before and
therefore does not retain any information.
Let’s illustrate with an example. We can start by querying the agent we made in
Chapter 2 with a basic question:
from illustrated_agents.chapters.ch2 import LLM, TinyAgent

# Gemma 3 12B (no native thinking or tool calling)
llm = LLM(model="gemma3:12b")

# Run a query
ch_2_agent = TinyAgent(llm=llm)
response = ch_2_agent.run("Hi! We are Maarten and Jay, authors of
'An Illustrated Guide to AI Agents'.")
We then give it a follow-up question to see if the agent knows the interaction we had
before:
response = ch_2_agent.run("Hi! What are our names?")
print(response)
This gives us:
"I do not know what your name is, as you have not told me!"
The agent doesn’t seem to know our names. Every time you query an LLM directly
with only the query you have, it starts from a blank slate. You’ll have to fill this in
yourself through the message structure that we explored in previous chapters.
Let’s start with the most fundamental way of adding memory to the messages, namely
tracking the conversation history.
Conversation Memory
The conversation history of the LLM serves as the context for generating responses.
Illustrated in Figure 4-5, they are generally formatted as messages demonstrating the
Short-Term Memory
|