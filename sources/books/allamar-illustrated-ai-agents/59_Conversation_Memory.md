---
title: "Conversation Memory"
chapter_number: 59
page_start: 155
page_end: 159
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Conversation Memory

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

differences between system prompts, the user’s query, and the LLM’s answer. It’s a
conversation where the user tells something about themselves, namely that they love
flamingos.



![Figure 4-5: An example of how conversations can be represented using JSON](images/fig_04-05_An_example_of_how_conversations_can_be_r.png)

*Figure 4-5: An example of how conversations can be represented using JSON*


Figure 4-5. An example of how conversations can be represented using JSON
These messages are updated every time the user or assistant replies and are fed back
into the LLM as input for the next query, as shown in Figure 4-6. The query (“What
is my favorite animal?”) does not trigger the LLM to recall the past on its own.
Rather, it is provided with the entire conversation history, which contains the relevant
information, namely that the user loves flamingos. In other words, the LLM does not
truly “remember” past conversations but is instead told what the conversation was by
explicitly inserting it into the prompt.



![Figure 4-6: The LLM is given both the conversation history as well as the current query](images/fig_04-06_The_LLM_is_given_both_the_conversation_h.png)

*Figure 4-6: The LLM is given both the conversation history as well as the current query*


Figure 4-6. The LLM is given both the conversation history as well as the current query
Let’s explore this by integrating a Memory module into your TinyAgent. The module
is quite straightforward and is merely a list of dictionaries that track the role and its
content, exactly as shown in Figure 4-5:
class Memory:
 """Simple memory module to store conversation history."""

 def __init__(self):
 self.messages = []
|
Chapter 4: Memory

def add(
 self, role: str, content: str, tool_call: dict | None = None, **kwargs
 ) -> None:
 """Add a message to memory."""
 message = {"role": role, "content": content}

 # Tool call
 if tool_call:
 message["tool_calls"] = [tool_call]

 # Append message to memory
 self.messages.append(message)

 def get_messages(self) -> list[dict]:
 """Get all messages."""
 return self.messages
The Memory module has two functions, one to add new messages (.add) and one to
get them (.get_messsages). Note that we also have the option to add a tool call. This
is something we will use in Chapter 5 when we explore how LLMs can call tools.
In your TinyAgent, the roles are then updated as follows:
- Response of the LLM: memory.add("assistant", LLM_RESPONSE)
•
- User’s query: memory.add("assistant", USER_QUERY)
•
To use the Memory module in TinyAgent, we initialize the module and call.add when
we want to add roles and content to the memory. Then, whenever a request is made
of the LLM, we use.get_messages to get the entire conversation history. Note that we
highlighted the code that was added to your TinyAgent:
from illustrated_agents.chapters.ch2 import Trajectory

class TinyAgent:
 """A minimal, modular, and educational agent framework."""

 def __init__(self, llm: LLM, memory: Memory):
 self.llm = llm
 self.memory = memory
 self.tools = None # Chapter 5: Add Tools
 self.planner = None # Chapter 6: Add Planning

 self.trajectory = Trajectory()

 def run(self, task: str) -> str:
 """Run the agent on a task."""
 self.memory.add("user", task)
 self.trajectory.initialize(task)

 return self._step()
Short-Term Memory
|

def _step(self) -> str:
 """Perform a single step."""
 # Generate response and add to memory
 response = self.llm.generate(self.memory.get_messages())
 self.memory.add("assistant", response.content)
 self.trajectory.add(response)
 return response.content

 def _execute_action(self, action: str) -> str | None:
 """Execute a tool action."""
 # Placeholder - will be implemented in later chapters
 return f"Executed action: {action}"
Note how in run and _step we used the self.memory.add function to track the
conversation history and use self.memory.get_messages() to give that full context
to the LLM.
We run the new agent twice to see if it tracked the history and ask it the same
question we did before:
# Add memory to the Agent
memory = Memory()
agent_with_memory = TinyAgent(llm=llm, memory=memory)

# First query
first_response = agent_with_memory.run("Hi! We are Maarten and Jay, authors of
'An Illustrated Guide to AI Agents'.")

# Second query
second_response = agent_with_memory.run("Hi! What are our names?")
print(second_response)
This gives us:
"Your names are **Maarten and Jay**."
It knows our names! It’s not that the LLM remembers our names, but instead we
merely told it what conversation we had before. We can then inspect the full conver‐
sation history:
agent_with_memory.memory.get_messages()
This gives us:
[
 {'role': 'user',
 'content': "Hi! We are Maarten and Jay, authors of
 'An Illustrated Guide to AI Agents'."},
 {'role': 'assistant',
 'content': 'Hi Maarten and Jay! It\'s great to "meet" you.\n\n
 **"An Illustrated Guide to AI Agents"** sounds like a fascinating
 and very timely topic. Are you:\n\n
 * **Looking for feedback** on the book\'s content or structure?\n*'},
|
Chapter 4: Memory

{'role': 'user', 'content': 'Hi! What are our names?'},
 {'role': 'assistant', 'content': 'Your names are **Maarten and Jay**.'}
 ]
That is exactly the information that we gave to the LLM, which now has the full
context it needs to answer our questions. It was straightforward, but the agent now
actually has memory.
However, most LLMs have a limited context window, which is the number of tokens
that the LLM can process. This counts both the input and the output tokens, as
shown in Figure 4-7.



![Figure 4-7: The context window defines the maximum number of tokens an LLM can](images/fig_04-07_The_context_window_defines_the_maximum_n.png)

*Figure 4-7: The context window defines the maximum number of tokens an LLM can*


Figure 4-7. The context window defines the maximum number of tokens an LLM can
process, while context length refers to the actual length of either the input, the generate
output, or both
In this example, a short query and answer are given that total 13 tokens out of
a potential 8,192. Shown in Figure 4-8, there are many potential tokens that are
left unused and could potentially be filled with additional information or reasoning
tokens, as discussed in Chapter 3.



![Figure 4-8: The full context window should manage both the input and output tokens](images/fig_04-08_The_full_context_window_should_manage_bo.png)

*Figure 4-8: The full context window should manage both the input and output tokens*


Figure 4-8. The full context window should manage both the input and output tokens
However, as the conversation history grows, so do the number of tokens. Eventually,
and as shown in Figure 4-9, if the conversation history gets too large, it will not fit
within the context windows. This might cut the answer short or even prevent the
LLM from processing the prompt at all.
Short-Term Memory
|