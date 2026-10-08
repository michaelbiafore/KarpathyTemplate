---
title: "TinyAgent with Tools"
chapter_number: 77
page_start: 211
page_end: 214
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# TinyAgent with Tools



![Figure 5-12: An example of how the LLM processes the tool’s output through the](images/fig_05-12_An_example_of_how_the_LLM_processes_the.png)

*Figure 5-12: An example of how the LLM processes the tool’s output through the*


Figure 5-12. An example of how the LLM processes the tool’s output through the
conversation history
TinyAgent with Tools
Now that we have all the components for calling tools, it’s finally time to update your
TinyAgent to make use of them. We highlighted the code that was added to your
TinyAgent:
```
from illustrated_agents.chapters.ch2 import LLM, Trajectory
from illustrated_agents.chapters.ch4 import Memory
```


class TinyAgent:
 """A minimal, modular, and educational agent framework."""

 def __init__(self, llm: LLM, memory: Memory, tools: Tools):
 self.llm = llm
 self.memory = memory
 self.tools = tools
 self.planner = None # Chapter 6: Add Planning

 self.trajectory = Trajectory()

 # Build system prompt with all components
 system_prompt = "You are a helpful assistant.\n\n"
 system_prompt += self.tools.prompt
 self.memory.add("system", system_prompt)

 def run(self, task: str) -> str:
 """Run the agent on a task."""
 self.memory.add("user", task)
 self.trajectory.initialize(task)

 return self._step()
Tool Usage
|

def _step(self) -> str:
 """Perform a single step."""
 # THOUGHT: Generate response and add to memory
 response = self.llm.generate(
 self.memory.get_messages(), tools=self.tools.schemas
 )
 self.memory.add(
 "assistant", response.content, tool_call=response.tool_call
 )

 # Tool parsing
 response = self.tools.parse(response)

 # ANSWER: Stopping mechanism
 if self.tools.is_done(response):
 self.trajectory.add(response)
 return response.content

 return self._execute_action(response)

 def _execute_action(self, response: Response) -> str:
 """Execute a tool action."""

 # ACTION: execute tools
 result = self.tools.execute(response)

 # OBSERVATION: add tool results to memory and display
 role, observation = self.tools.observation(result)
 self.memory.add(role, observation)
 self.trajectory.add(response, observation)

 return observation
Out of all the changes to your TinyAgent, this chapter and the next include the largest
set of them throughout the book. So, let’s go through them one by one!
The system prompt
In the __init__ of your TinyAgent, we now add a system prompt. As we covered in
the section “Tool Definition” on page 180, this serves as a nice way for the agent to
keep track of what tools it has available. With self.tools.prompt, we add the tools’
definitions to the system prompt as we did previously. As you will see in upcoming
chapters (e.g., Chapter 6), the system prompt is going to be used for tracking more
information than just tools.
|
Chapter 5: Tool Usage, Learning, and Protocols

Note that the SummarizationMemory would actually not work well
with Tools since it continuously overrides the system prompt to
track the summarized conversation history. Tools requires keeping
the tool definition in the system prompt; this would essentially
remove any information the LLM has about tools!



![Figure on page 17](images/fig_p017_x95.png)


A solution would be to always update a section of the system
prompt rather than replacing it entirely. Try it out yourself and see
if you can update the SummarizationMemory so that it will work
nicely with Tools.
A single step
A single step (_step) consists of the following components:
Generate a response
The LLM generates a response with self.llm.generate. You can call this the
THOUGHT of the LLM, as it contains what it thinks about the current situation
and how it would like to act.
Tool parsing
If there is a tool call, it is parsed with self.tools.parse. As we covered in the
section “Tool Calling” on page 186, this converts the string to a structured JSON
output.
Tool execution
If there is a parsed tool call, it is executed with _execute_action (more on that
coming up).
Stopping mechanism
If there is no tool call, we stop execution entirely. This is not behavior we need at
this moment since your TinyAgent does not yet run autonomously. However, it
will become important in the next chapter, where the agent can run continuously.
Executing an action
Executing an action (_execute_action) consists of two steps:
Execute tool call
Executing the JSON tool call with self.tools.execute(response), which per‐
forms the tool call as we covered in the section “Tool Calling” on page 186.
Track the result
Track the output of the tool call. The LLM has to know what the output is in
order to decide what to do next. As we covered in the section “Tool Output
Processing” on page 188, we do this by adding the output as the user role and
describing it with the prefix OBSERVATION.
Tool Usage
|

Finally, we track the state of the agent with the Trajectory module and the conversa‐
tion history with the Memory module.
You might have noticed capitalized words scattered throughout
this chapter’s code: THOUGHT, OBSERVATION, ACTION, and
ANSWER. These are steps relating to the Reason and Act (ReAct)
framework that we will use in Chapter 6 to create autonomous
behavior.6 As you might have guessed, these mean the following:



![Figure on page 17](images/fig_p017_x95.png)


THOUGHT
The reasoning of the LLM on what to do next.
ACTION
The action or tool calls of the LLM are structured as JSON.
OBSERVATION
The output of the ACTION the LLM took.
ANSWER
The LLM’s final answer after running for one or more steps.
Running your TinyAgent with tool-calling capabilities
Now that you have a TinyAgent with tools, we can initialize it. Here, we choose a
no-frills memory and simply track the entire conversation history:
from illustrated_agents.chapters.ch2 import LLM

# Gemma 3 12B (no native thinking or tool calling)
llm = LLM(model="gemma3:12b")

# Register tool
tools = Tools()
tools.add_tool(
 name="multiply",
 func=multiply,
 description="Multiplies two numbers: multiply(a: str, b: str)"
)

# Memory
memory = Memory()

# Initialize Agent
agent = TinyAgent(llm=llm, memory=memory, tools=tools)
Your TinyAgent now has access to an LLM, memory, and tools!
6 Yao, Shunyu et al. 2022. “ReAct: Synergizing Reasoning and Acting in Language Models,” arXiv, 2210.03629.
|
Chapter 5: Tool Usage, Learning, and Protocols