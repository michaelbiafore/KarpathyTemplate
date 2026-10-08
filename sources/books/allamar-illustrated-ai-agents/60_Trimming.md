---
title: "Trimming"
chapter_number: 60
page_start: 160
page_end: 161
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Trimming



![Figure 4-9: The generated output of LLMs may be clipped if they exceed the context](images/fig_04-09_The_generated_output_of_LLMs_may_be_clip.png)

*Figure 4-9: The generated output of LLMs may be clipped if they exceed the context*


Figure 4-9. The generated output of LLMs may be clipped if they exceed the context
window or no output can be generated if the entire input already exceeds the context
window
Moreover, the more information put in the prompt, the more difficult it will be for
the LLM to attend to everything.3 As a result, we cannot always put the entire conver‐
sation history into the prompt of the LLM. Instead, there are several techniques we
can use to provide the conversation history without filling up the context window.
Trimming
The first technique for efficient short-term memory is rather straightforward: trim‐
ming the messages as they grow. Whenever the number of messages grows too large
for the LLM’s context window to handle, we can decide to simply remove the first few
interactions until it fits that window. Shown in Figure 4-10, this might remove quite a
lot of information that may or may not be relevant to future queries.



![Figure 4-10: Efficient short-term memory may include keeping only the last couple of](images/fig_04-10_Efficient_short-term_memory_may_include.png)

*Figure 4-10: Efficient short-term memory may include keeping only the last couple of*


Figure 4-10. Efficient short-term memory may include keeping only the last couple of
conversations instead of keeping track of the entire conversation history
3 Hsieh, Cheng-Ping et al. 2024. “RULER: What’s the Real Context Size of Your Long-Context Language
Models?” arXiv, 2404.06654.
|
Chapter 4: Memory

Because we already did much of the heavy lifting with the Memory module, imple‐
menting this trimming behavior requires a minimal amount of code. We use inheri‐
tance to keep the same functionality of Memory but update the add function so that
only the last two turns (each a pair of user/assistant messages) are kept:
class TrimmingMemory(Memory):
 """Memory that keeps only the last two user/assistant turns."""

 def add(self, role: str, content: str, **kwargs) -> None:
 # Add the new message first using the parent class (Memory)
 super().add(role, content, **kwargs)

 # Then, keep system message plus the most recent two turns (4 messages)
 system = [
 message for message in self.messages if message["role"] == "system"
 ]
 turns = [
 message for message in self.messages if message["role"] != "system"
 ]
 self.messages = system + turns[-4:]
You can try it out with an example to see what happens if you ask it four questions:
from illustrated_agents.chapters.ch4 import TinyAgent

# Create the Agent
memory = TrimmingMemory()
agent = TinyAgent(llm=llm, memory=memory)

# Run some interactions
response_1 = agent.run("Hi! I'm reading 'An Illustrated Guide to AI Agents'.")
response_2 = agent.run("There are many flamingos in this book, why?")
response_3 = agent.run("What is 1+1?")
response_4 = agent.run("What is 2+2?")
We can then inspect the memory as we did before:
print(agent.memory.get_messages())
This gives us:
[
 {'role': 'user', 'content': 'What is 1+1?'},
 {
 'role': 'assistant',
 'content': "1 + 1 = 2\n\nIt's a classic!



![Figure on page 58](images/fig_p058_x638.png)


"
 },
 {'role': 'user', 'content': 'What is 2+2?'},
 {'role': 'assistant', 'content': '2 + 2 = 4! \n\n
 Just keeping the math train rolling, I see!



![Figure on page 58](images/fig_p058_x638.png)


}
 ]
Short-Term Memory
|