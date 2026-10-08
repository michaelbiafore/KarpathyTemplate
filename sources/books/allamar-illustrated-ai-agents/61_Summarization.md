---
title: "Summarization"
chapter_number: 61
page_start: 162
page_end: 164
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Summarization

Only the last two sets of messages are kept with this type of memory. This helps keep
the memory to a minimum but might remove important information discussed early
in the conversations. Note that you might see the book or the flamingos mentioned in
these messages. That can happen since information can still flow from the assistant’s
output if it keeps mentioning it:
- Turn 1: No memory
•
- Turn 2: Memory of turn 1
•
- Turn 3: Memory of turns 1 and 2
•
- Turn 4: Memory of turns 2 and 3
•
It’s important to keep track of the raw conversations in its trajectory since the agent’s
memory might be stripped or processed. As such, if you run the following yourself,
you will get a view with the full interaction (turns 1 through 4):
from illustrated_agents.utils import TrajectoryViewer
TrajectoryViewer(agent.trajectory)
In later chapters, you’ll see that the user and assistant roles do not always alternate.
A more autonomous agent (see Chapter 6) will have multiple turns of only assistant
roles.
Summarization
A common technique is to employ another LLM to summarize the conversation
history. After each conversation turn, the same or another LLM will summarize it and
add it to the full summary of the conversation (as shown in Figure 4-11).



![Figure 4-11: Each conversation turn may be summarized and merged into one long](images/fig_04-11_Each_conversation_turn_may_be_summarized.png)

*Figure 4-11: Each conversation turn may be summarized and merged into one long*


Figure 4-11. Each conversation turn may be summarized and merged into one long
summary to reduce the length of the full conversation history
As illustrated in Figure 4-12, the created summary will be shown together with the
query for the LLM to answer. This summary might still fill the context window
|
Chapter 4: Memory

over time as summaries are stacked on one another, but it is much slower than
filling the context window with the raw conversation history. Likewise, this can be
prevented by summarizing these again but that might compress too much of the
original information, which in turn could remove important information.



![Figure 4-12: A summary of the full conversation history can be given to the LLM for](images/fig_04-12_A_summary_of_the_full_conversation_histo.png)

*Figure 4-12: A summary of the full conversation history can be given to the LLM for*


Figure 4-12. A summary of the full conversation history can be given to the LLM for
more efficient usage of the context window
Stacking summaries is not the only method of summarization. Instead of adding a
summary of the most recent query/answer pair each time, you can instead summa‐
rize the conversation history of the last five conversations. Likewise, you can decide
to maintain one summary and ask the LLM to update it after each conversation.
Figure 4-13 illustrates such a method where conservation turns 1 through 5 are
summarized but not turn 6.



![Figure 4-13: A part of the conversation history can also be summarized to create a](images/fig_04-13_A_part_of_the_conversation_history_can_a.png)

*Figure 4-13: A part of the conversation history can also be summarized to create a*


Figure 4-13. A part of the conversation history can also be summarized to create a
balance between old information (summarized) and new information (uncompressed)
Let’s illustrate it with a simplified example. We are going to create a Summarization
Memory module where each time a turn has passed, the turn gets summarized by an
LLM. In this example, we assume that the role of the user is always followed by that of
the assistant. We will use the system role to track the summary so we can separate it
```
from the conversation between the user and assistant:
class SummarizationMemory(Memory):
```
 """Memory that compresses past turns into a running summary via an LLM."""

 def __init__(self, llm: LLM):
 super().__init__()
 self.llm = llm

 def add(self, role: str, content: str, **kwargs) -> None:
 # Add the new message first using the parent class (Memory)
 super().add(role, content, **kwargs)

 # After each completed turn, update the running summary
Short-Term Memory
|

if role == "assistant":
 # Split the existing summary from the new conversation turns
 summary = ""
 conversation = ""
 for message in self.messages:
 if message["role"] == "system":
 summary = message["content"]
 else:
 conversation += f"{message['role']}: {message['content']}\n"

 # Ask the LLM to extend the summary with the new conversation
 prompt = f"""Update the summary with the new conversation.

Summary: {summary}

Conversation:
{conversation}
Output the updated summary only."""
 response = self.llm.generate([{"role": "user", "content": prompt}])
 self.messages = [{"role": "system", "content": response.content}]
You can choose any LLM to perform the summarization task, but for illustration
purposes we are going to use the one we have been using so far. Then, we ask the
agent a question:
# Create the Agent
memory = SummarizationMemory(llm=llm)
agent = TinyAgent(llm=llm, memory=memory)

# Run a query
response = agent.run("Hi, my name is Sarah. Why are flamingos pink?")
This gives a response as you would expect. However, that raw response is not tracked
in the agent’s memory because during this .run, a summarization of the conversation
history takes place. Let’s inspect the memory:
print(agent.memory.get_messages())
This gives:
[
 {
 'role': 'system',
 'content': 'Sarah asked why flamingos are pink. The assistant explained
 that flamingos are not born pink; they are born with grey or white
 feathers. They turn pink due to carotenoid pigments found in their diet
 of shrimp, algae, and brine flies. These pigments are absorbed and
 deposited into their feathers, causing the pink coloration.
 The intensity of the pink depends on the amount of
 carotenoid-rich food they consume.'
 }
]
|
Chapter 4: Memory