---
title: "Task-Specific Workflows"
chapter_number: 153
page_start: 420
page_end: 429
part: "Part II. Specialized Agents"
---
# Task-Specific Workflows



![Figure 10-15: A coding agent analyzing a bug report to generate a reviewable codebase](images/fig_10-15_A_coding_agent_analyzing_a_bug_report_to.png)

*Figure 10-15: A coding agent analyzing a bug report to generate a reviewable codebase*


Figure 10-15. A coding agent analyzing a bug report to generate a reviewable codebase
modification plan
Writing a plan and then executing each part of it seems like two different tasks that
can be handled by two different prompts, or even different agents. So some agentic
code systems would assign the planning step to a dedicated planning agent and then
some or all steps to dedicated code agents to tackle the appropriate steps. But even in
a single-agent system, the plan is one of the most important components of resolving
the task. With that importance, it’s often a good idea to assign it to the best available
model and to have it think on it for a reasonable amount of time for the task.
When designing a planning prompt or agent, we have to bear in mind that some tasks
require a bit of investigation to know exactly how to solve the task. This is especially
the case for software tasks, which often require exploration and research phases or
asking the user for clarification or more information. So, it’s important to not assume
that the approach to solving a problem is crystal clear at planning time. The plan
likely needs to include exploration and investigation steps and have some flexibility
based on the findings from these steps.
Task-Specific Workflows
There are often scenarios in which a problem is simpler to tackle with a static
workflow than with an agent. A static workflow runs through a fixed set of steps
you lay out in advance, rather than letting the model decide what to do at each turn.
Plenty of routine tasks are simple enough that reaching for an agent is overkill. A
proficient agent developer keeps other tools within reach and picks the one that fits
the problem, rather than shoehorning an agent into every job.
|
Chapter 10: Code Agents and Code LLMs

Agentless
For software engineering tasks, the agentless approach stands out for its simplicity
and ability to compete with agentic approaches via a simple three-phase process,5 as
shown in Figure 10-16.



![Figure 10-16: Agentless resolves an issue in three fixed phases: localize the relevant code,](images/fig_10-16_Agentless_resolves_an_issue_in_three_fix.png)

*Figure 10-16: Agentless resolves an issue in three fixed phases: localize the relevant code,*


Figure 10-16. Agentless resolves an issue in three fixed phases: localize the relevant code,
generate several candidate patches, then pick the best using generated unit tests
In a way, the agentless approach works much like a Retrieval-Augmented Generation
(RAG) system. It starts with a search step, finding all the code snippets in the reposi‐
tory that are relevant to the issue we want to fix. This is localization. It then hands
those snippets and the issue to a coding LLM that generates a candidate solution. This
is repair.
The method improves the chances of resolving the bug by sampling multiple solu‐
tions from the LLM, so it has multiple attempts to solve the issue.
5 Xia, Chunqiu Steven et al. 2024. “Agentless: Demystifying LLM-based Software Engineering Agents,” arXiv,
2407. 01489.
Building Code Agents
|

But then how do we select the best solution candidate? Another powerful idea here
is that coding LLMs can also be great at generating unit tests. So, we can present the
issue to the LLM and ask it to generate a suite of unit tests to validate solutions for
this bug.
These generated unit tests can then be used to rank and choose the best solutions.
Because the unit tests are themselves generated, and we’re not fully confident in their
quality, the selected solution does not need to pass all of them. It just needs to pass
more than the other candidates do.
We do want to re-highlight these two ideas because they share an advanced concept
around using LLMs: we can use the probabilistic nature of LLMs to our advantage.
One way is by sampling multiple possible solutions (at temperature values that allow
some reasonable variety), and the second is by using generated unit tests as a ranking
signal and not a pass/fail signal. These are powerful ideas that belong to the agent
builder’s toolkit.
TinyAgent with code tools
We’ve now walked through the tools a code agent uses, how it manages context, and
how software engineering agents approach real tasks. Let’s pull those threads together
and build a coding agent ourselves.
A core part of the coding agent is the tools it uses, and these are what tie an LLM to a
software system. We covered several categories, but arguably the most common ones
are:
File manipulation tools
This lets the agent read, list, and write files.
Code interpreter
This lets the agent execute code it writes.
To give your TinyAgent coding capabilities, let’s create several tools that span these
two categories:
```
import subprocess
import sys
```

from pathlib import Path


def read_file(path: str) -> str:
 """Read a file's contents."""
 target = Path(path)
 if not target.exists():
```
 return f"Error: '{path}' not found."
 return target.read_text(encoding="utf-8")
```
|
Chapter 10: Code Agents and Code LLMs

def list_files(directory: str = ".") -> str:
 """List files in a directory."""
 target = Path(directory)
 if not target.is_dir():
 return f"Error: '{directory}' is not a directory."
 entries = sorted(target.iterdir())
 lines = [f"{p.name}/" if p.is_dir() else p.name for p in entries]
 return "\n".join(lines) or "(empty)"


def write_file(path: str, content: str) -> str:
 """Write content to a file."""
 target = Path(path)
 target.parent.mkdir(parents=True, exist_ok=True)
 target.write_text(content, encoding="utf-8")
 return f"Written to '{path}'."


def execute_python(code: str) -> str:
 """Execute Python code and return output."""
 try:
 result = subprocess.run(
 [sys.executable, "-c", code],
 capture_output=True,
 text=True,
 timeout=30,
 )
 except subprocess.TimeoutExpired:
 return "Error: Code execution timed out (30s limit)."

 if result.returncode != 0:
 return (
 f"Exit code {result.returncode}\n"
 f"STDOUT:\n{result.stdout}\n"
 f"STDERR:\n{result.stderr}"
 ).strip()
 return result.stdout.strip() or "(no output)"
As we saw in Chapter 5, these tools all return a string whether they succeed or not.
This output can then be used in the messages structure as an observation to indicate
whether the tool call succeeded.
Some of the tools, such as execute_python and write_file, are not safe by default.
If we were to give your TinyAgent complete freedom, it might corrupt files or
take dangerous actions. Instead, we’ll use the requires_approval parameter that we
explored in Chapter 5.
Building Code Agents
|

Before execution, you’ll be asked to reply with “Y” (yes) or “N” (no), so you can
inspect whether you believe the action is safe:
from illustrated_agents.chapters.ch5 import NativeTools

# Some tools require approval
tools = NativeTools(requires_approval=["write_file", "execute_python"])
tools.add_tool("read_file", read_file)
tools.add_tool("list_files", list_files)
tools.add_tool("write_file", write_file)
tools.add_tool("execute_python", execute_python)
With capabilities to write and execute code, this is already sufficient to turn your
TinyAgent into a basic coding agent! It can now be run with agent.run as we did
before to execute certain tasks.
This, however, is not an ideal interface. As we discussed previously, more advanced
interfaces like Cursor and agents that live in the terminal are common among coding
solutions. As such, let’s implement an interface ourselves such that your TinyAgent
can be used anywhere in the terminal.
The first thing we’ll have to do is create a Display class. This class will be used in
your TinyAgent to display what the agent is doing at any given moment. We separate
the steps in the ReAct loop as we have done before (with the color coding you’re
familiar with):
THOUGHT
The reasoning of the agent
ACTION
The tool the agent wants to use
OBSERVATION
The output of the tool use
ANSWER
The final answer of the agent
The Display class uses ANSI escape codes (e.g., "\033[35m") to color the output.
Assigning a distinct color to each phase of the ReAct loop makes the agent’s reason‐
ing, tool executions, and final answers easily readable and scannable at a glance:
from illustrated_agents.chapters.ch2 import Response

BOLD = "\033[1m"
RESET = "\033[0m"
GREEN = "\033[32m" # THOUGHT
RED = "\033[31m" # ACTION
YELLOW = "\033[33m" # OBSERVATION
PURPLE = "\033[35m" # ANSWER
|
Chapter 10: Code Agents and Code LLMs

class Display:
 """Chat interface with styling."""

 def __call__(self, event: str, data: str | Response = None) -> None:

 # "Thinking" line
 if event == "thinking":
 print(f" Thinking...\n{RESET}")

 # THOUGHT
 elif event == "response":
 print(f"{BOLD}{GREEN}{'▒▒ THOUGHT ▒▒':<13}{RESET}")
 print(f"{data.reasoning}{RESET}\n")

 # ANSWER
 if data.content:
 print(f"{BOLD}{PURPLE}{'▒▒ ANSWER ▒▒':<13}{RESET}")
 print(f"{data.content}{RESET}\n")

 # ACTION
 elif event == "tool_call" and data:
 tool = data.tool_call["tool"]
 kwargs = data.tool_call["kwargs"]
 print(f"{BOLD}{RED}{'▒▒ ACTION ▒▒':<13}{RESET}")
 print(f"{tool}({kwargs}){RESET}\n")

 # OBSERVATION
 elif event == "observation":
 print(f"{BOLD}{YELLOW}{'▒▒ OBSERVATION ▒▒':<13}{RESET}")
 print(f"{data}{RESET}\n")
 print(f"{'─' * 40}STEP{'─' * 40}{RESET}\n")
Let’s try out the display by using a Response object to mimic the output of the agent:
# Let's create a Response with a tool call and no final answer
response = Response(
 content="I executed Python.",
 reasoning="Let's execute some python!",
 tool_call= {
 "tool": "execute_python",
```
 "kwargs": {"code": "print('Hello World!')"}
 }
```
)


# Display the Response
display = Display()
display("thinking", response)
display("response", response)
display("tool_call", response)
display("observation", "Hello World!")
Building Code Agents
|

Which gives:
Thinking...

▒▒ THOUGHT ▒▒
Let's execute some python!

▒▒ ACTION ▒▒
execute_python({'code': "print('Hello World!')"})

▒▒ OBSERVATION ▒▒
Hello World!

▒▒ ANSWER ▒▒
I executed Python.
Note how each step is nicely styled to clearly make a distinction between the cycles
of THOUGHT/ACTION/OBSERVATION. The color coding was chosen to be in line
with all the visuals we explored throughout the previous chapters.
The Display now needs to be integrated into your TinyAgent. This is, fortunately,
straightforward because we need to add only self.display(...) where we want to
track a certain behavior. As in previous chapters, we highlight the code that was added:
```
from illustrated_agents.chapters.ch2 import Response, Trajectory
from illustrated_agents.chapters.ch4 import Memory
from illustrated_agents.chapters.ch5 import Tools
from illustrated_agents.chapters.ch6 import ReAct
```


class TinyAgent:
 """A minimal, modular, and educational agent framework."""

 def __init__(
 self,
 llm: LLM,
 memory: Memory,
 tools: Tools,
 planner: ReAct,
 display: Display,
 ):
 self.llm = llm
 self.memory = memory
 self.tools = tools
 self.planner = planner
 self.display = display

 self.trajectory = Trajectory()

 # Build system prompt with all components
 system_prompt = "You are a helpful assistant.\n\n"
 system_prompt += self.planner.prompt
|
Chapter 10: Code Agents and Code LLMs

system_prompt += self.tools.prompt
 self.memory.add("system", system_prompt)

 def run(self, task: str, image_data: str = None) -> str:
 """Run the agent on a task."""
 self.memory.add("user", task, image_data=image_data)
 self.trajectory.initialize(task)

 # *Autonomy* loop
 for step in range(self.planner.max_steps):
 result = self._step()
 if result is not None:
 return result

 return "Max steps reached without completion."

 def _step(self) -> str | None:
 """Perform a single step."""
 # THOUGHT: Generate response and add to memory
 self.display("thinking")
 response = self.llm.generate(
 self.memory.get_messages(), tools=self.tools.schemas
 )
 self.memory.add(
 "assistant", response.content, tool_call=response.tool_call
 )
 self.display("response", response)

 # Tool parsing
 response = self.planner.parse(response)
 response = self.tools.parse(response)

 # ANSWER: Stopping mechanism
 if self.tools.is_done(response):
 self.trajectory.add(response)
 return response.content

 return self._execute_action(response)

 def _execute_action(self, response: Response) -> None:
 """Execute a tool action."""

 # ACTION: execute tools
 self.display("tool_call", response)
 result = self.tools.execute(response)

 # OBSERVATION: add tool results to memory and display
 role, observation = self.tools.observation(result)
 self.memory.add(role, observation)
 self.trajectory.add(response, observation)
 self.display("observation", observation)
Building Code Agents
|

return None
To initialize the coding agent, we can add the display parameter like so:
```
from illustrated_agents.chapters.ch2 import LLM
from illustrated_agents.chapters.ch6 import NativeReAct
```

# Gemma 4 E4B (with native thinking and tool calling)
llm = LLM(model="gemma4:e4b", think=True)

# Coding Agent
agent = TinyAgent(
 llm=llm,
 tools=tools,
 memory=Memory(),
 planner=NativeReAct(),
 display=display
)
Before we start running the TinyAgent, let’s create a small function so that we can run
this coding agent in the terminal. Note that we add a bit of styling to make for a nicer
interface:
NAME = """
██████ ██ ███ ██ ██ ██ ▄████▄ ▄████ ██████ ███ ██ ██████
 ██ ██ ██ ▀▄██ ▀██▀ ██▄▄██ ██ ▄▄▄ ██▄▄ ██ ▀▄██ ██
 ██ ██ ██ ██ ██ ██ ██ ▀███▀ ██▄▄▄▄ ██ ██ ██
""" # ANSI Compact

```
def main():
 import shutil
```

 print(f"\n{NAME}\n")

 while True:
 try:
 query = input().strip()
 print("\033[0m")
 except (KeyboardInterrupt, EOFError):
 print("\033[0m", end="")
 break
 if not query or query.lower() in ("exit", "quit"):
 break
 try:
 agent.run(query)
 except Exception as e:
 print(f"ERROR: {e}\n")


if __name__ == "__main__":
 main()
|
Chapter 10: Code Agents and Code LLMs

All code we have created thus far lives in the illustrated-agents package, and because
it’s pure Python, you can run your coding agent like so:
python .\src\illustrated_agents\chapters\ch10.py
Running this will give you a nice interface to work with, as shown in Figure 10-17.



![Figure 10-17: Running TinyAgent surfaces each step of its reasoning loop, showing the](images/fig_10-17_Running_TinyAgent_surfaces_each_step_of.png)

*Figure 10-17: Running TinyAgent surfaces each step of its reasoning loop, showing the*


Figure 10-17. Running TinyAgent surfaces each step of its reasoning loop, showing the
THOUGHT, ACTION, and OBSERVATION for a task as it lists the files in the current
directory
As you can see, when you give it a task, the separation between THOUGHT/
ACTION/OBSERVATION will be shown. This will give you an intuitive understand‐
ing of what’s under the hood. Try it out and see where your TinyAgent shines and
where it needs improvement. Likewise, the LLM makes a large difference. If the
small 4-billion-parameter model doesn’t suit your needs, try a larger one, or a model
trained specifically for this kind of work. North Mini Code,6 for example, is an open
mixture-of-experts model from Cohere built for agentic coding: 30 billion parameters
total but only 3 billion active per token, released under Apache 2.0. It asks more of
your hardware than Gemma, but it’s purpose-built for the code-focused, multi-step,
tool-using work your TinyAgent is now doing.
You have created a coding agent in the CLI entirely from scratch
and in pure Python!
Congratulations!



![Figure on page 429](images/fig_p429_x5116.png)


6 Coauthor Jay was a member of the core team that built North Mini Code.
Building Code Agents
|