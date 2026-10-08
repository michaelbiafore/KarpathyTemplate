---
title: "The TinyAgent"
chapter_number: 29
page_start: 56
page_end: 64
part: "Part 1: What You Should Know About Large Language Models"
---
# The TinyAgent



![Figure 2-6: The LLM responds to a user question by emitting a tool call (web_search](images/fig_02-06_The_LLM_responds_to_a_user_question_by_e.png)

*Figure 2-6: The LLM responds to a user question by emitting a tool call (web_search*


Figure 2-6. The LLM responds to a user question by emitting a tool call (web_search
with a structured query) and executing it before the conversation continues
All of the input text we see in this figure is an example of the text that gets tokenized
and sent to the LLM. And the output text is what the LLM generates one token at a
time.
The TinyAgent
The LLM is the agent’s brain, and it’s the first thing we want to implement in your
TinyAgent. To do so, we will need to consider which LLM to use, as there are hun‐
dreds of options depending on your hardware, use case, and the LLM’s capabilities.
Newer models such as Gemma 4 have been trained to perform native reasoning and
tool calling and have various options for different hardware. However, rather than
only showing an LLM that “just does” reasoning and tool calling, we also want to
show you what it’s like to build the tool calling and reasoning behavior yourself.
We decided to show you both! Throughout the book, we will demonstrate these
capabilities both from a prompt-driven and model-driven perspective. By doing it
yourself through various prompting techniques, you’ll gain insight into how these
newer models have learned to perform reasoning and tool calling natively.
As such, we choose two models to use throughout this book: one that cannot natively
perform any reasoning or tool calling whatsoever (Gemma 3) and one that has
been trained specifically to perform agentic tasks through reasoning and tool calling
(Gemma 4). They both have various sizes, where bigger models tend to be stronger
than smaller models. For Gemma 3, we opt for the 12-billion-parameter model
(Gemma 3 12B), and for Gemma 4, we opt for the smaller model that has effectively 4
billion parameters (Gemma 4 E4B).
|
Chapter 2: Large Language Models

The large language model
Before we start creating the main class for the brain, the LLM, we first explore a
common way of interacting with LLMs, namely through the OpenAI-endpoint. It is a
standardization of LLM inference that includes set fields, parameters, and responses
so that you always get the same standardized format back. OpenAI, with the release
of GPT 3.5 in 2022, set this standard for parsing an LLM’s response.
This endpoint generally contains the following pieces of information:
base_url
The URL of your hosted LLM
api_key
The key for accessing your hosted LLM
model
The name of your LLM
messages
The query to send to your LLM
Before you can use the LLM, you will first have to spin up a server that hosts your
LLM. Don’t worry, this is much easier than it sounds. There are many different
ways to download and host your LLM on your device. Popular options include
Ollama, LMStudio, and llama.cpp. Ollama and LMStudio work well for both devel‐
opers and non-developers, whereas llama.cpp is ideal for developers. Throughout
this book, we’ll assume you use Ollama, which hosts its LLMs locally on http://local
host:11434/v1/. However, you can use any inference engine, both locally and hosted,
as long as it is OpenAI-compatible (which most are).
After installing Ollama, you can download the models like so:
ollama pull gemma4:e4b
ollama pull gemma3:12b
As we covered previously, all LLMs have a specific prompt template that decides
how to format the text that passes through the LLM. Instead of having to look up
what this template is for each model, most inference engines (like Ollama) do this
for you with the messages structure. These messages are a common format for
structuring multiple turns of questions and responses between you (user) and the
LLM (assistant). You can then use the messages structure to talk to the LLM, which
will automatically convert it to the prompt template of the LLM.
We’ll use this structure to call the OpenAI-endpoint, which, in turn, will return a
response. This response can contain multiple answers in parallel but is generally
a single answer. As such, we focus on inspecting its one answer, namely
result["choices"][0]:
Part 1: What You Should Know About Large Language Models
|

```
import json
import urllib.request
```

# Prepare request
data = json.dumps(
 {
 "model": "gemma4:e4b",
 "messages": [{"role": "user", "content": "Hi! How's life?"}]
 }
).encode("utf-8")

# Post request
req = urllib.request.Request(
 url="http://localhost:11434/v1/chat/completions",
 data=data,
 headers={"Content-Type": "application/json"}
)

# Parse response
with urllib.request.urlopen(req) as response:
 result = json.loads(response.read())

# Print response
print(result["choices"][0])
This will give the following output:
{
 'index': 0,
 'message': {
 'role': 'assistant',
 'content': "I\'m doing really well, thank you for asking!



![Figure on page 58](images/fig_p058_x638.png)


\n\n
 How about you? What\'s going on with you today?",
 'reasoning': 'Thinking Process:\n\n1.
 **Analyze the Request:** The user said, "Hi! How\'s life?" This is a
 casual, conversational greeting seeking an update or general positive
 interaction.\n2.
 **Determine the Persona/Role:** I am an AI assistant...'
 },
 'finish_reason': 'stop'
}
Note that we truncated the reasoning a bit to prevent it from being too long for this
book. As we cover in Chapter 3, reasoning significantly improves the response of an
LLM.
Depending on the capabilities of the underlying LLM, it might output more fields
than just the content and reasoning. Some models are capable of returning tool calls,
which get a field of their own. As discussed before, we are not going to use the tool
and reasoning fields immediately. The reason is two-fold and is important for the
philosophy behind understanding what is happening under the hood:
|
Chapter 2: Large Language Models

1. Using the reasoning and tool_calls fields is a bit “magical” and does not teach
1.
you how these are actually created and used. Instead, we’re going to show you
how to do this explicitly through prompting techniques.
2. Some models actually do not support reasoning and tool_calls, but with
2.
proper prompting, can still be used as agents. So instead of blindly relying
on these fields, we want to show you how to nudge the model to do explicit
reasoning and tool calling with prompting.
In Chapter 3 (reasoning) and Chapter 5 (tool calling), we will show you first how
to use these capabilities by leveraging prompting techniques before exploring how a
model does this natively.
After we get the output, we are going to create a Response dataclass where we
will track the content, reasoning, tool_call, and other metadata the model may
provide:
from dataclasses import dataclass

@dataclass
class Response:
 """Structured response from LLM calls."""

 content: str = ""
 reasoning: str | None = None
 tool_call: dict | None = None
 metadata: dict | None = None
For now, we are only interested in using the content of the model, as we want to
show you how to have a non-reasoning model that still shows reasoning behavior. To
do that, we are adding a parameter to the LLM class we’ll be building that can disable
thinking. Lastly, we also track metadata that the backend might provide, such as the
model’s name ("model"), the number of tokens in the prompt ("prompt_tokens"),
and the number of tokens that were generated ("completion_tokens").
In this LLM class, we’re going to query the OpenAI-compatible endpoint directly as we
did before. However, we add a few functionalities to prepare you for later chapters,
such as adding tools/reasoning and extracting them:
```
import json
import urllib.request
```

```
class LLM:
 def __init__(
```
 self,
 model: str,
 base_url: str = "http://localhost:11434/v1",
 api_key: str = "no_key",
 think: bool = False,
Part 1: What You Should Know About Large Language Models
|

):
 """Initialize the LLM with the given model."""
 self.model = model
 self.base_url = base_url
 self.api_key = api_key
 self.think = think

 def generate(
 self, messages: list[dict], tools: list | None = None
 ) -> Response:
 """Generate a response from the LLM given a list of messages."""
 # Build the request body
 body = {
 "model": self.model,
 "messages": messages,
 }

 # Tools and Reasoning
 if tools:
 body["tools"] = tools
 if not self.think:
 body["reasoning_effort"] = "none"

 # POST to the OpenAI-compatible /chat/completions endpoint
 request = urllib.request.Request(
 f"{self.base_url}/chat/completions",
 data=json.dumps(body).encode(),
 headers={
 "Content-Type": "application/json",
 "Authorization": f"Bearer {self.api_key}",
 },
 )
 with urllib.request.urlopen(request) as response:
 data = json.loads(response.read())

 # Extract message, tool_call, and metadata
 message = data["choices"][0]["message"]
 tool_calls = message.get("tool_calls")
 tool_call = tool_calls[0] if tool_calls else None
 metadata = {
 "model": data["model"],
 "prompt_tokens": data["usage"]["prompt_tokens"],
 "completion_tokens": data["usage"]["completion_tokens"],
 }

 # Format as Response dataclass
 return Response(
 content=message.get("content"),
 reasoning=message.get("reasoning"),
 tool_call=tool_call,
 metadata=metadata,
 )
|
Chapter 2: Large Language Models

We also added the option to add tools to your LLM and extract a tool call if it exists.
These options are explored in more detail in Chapter 5. We make sure to have this
now so we do not need to update this class later.
Finally, you can call the LLM with our updated class and extract the response only:
# Re-initialize the LLM with the updated class
llm = LLM(model="gemma4:e4b")

# Generate a `Response` dataclass
response = llm.generate([{"role": "user", "content": "Hi! How's life?"}])
print(response)
This gives you:
Response(
 content="Life is going well, thank you for asking!
 I'm busy processing information and helping users like you, which is always
 interesting. How about I ask you? How's life on your end?



![Figure on page 58](images/fig_p058_x638.png)


",
 reasoning=None,
 tool_call=None,
 metadata={
 "model": "gemma4:e4b",
 "prompt_tokens": 16,
 "completion_tokens": 43,
 },
 )
The Response object is going to be used throughout the TinyAgent so that we can
easily access the output of the LLM. Before integrating it into the agent, let’s first
explore how we can track the state of an agent.
A step and trajectory
Remember that we are creating an agentic harness and a vital component of any
harness, is that you can easily debug what is happening during inference. An agent
might run for several turns at a time and run into an incorrect tool usage. To easily
debug that, we want to keep track of everything the model has done so far. To do so,
we track each Step the agent has taken (including observation from the output of a
tool):
from dataclasses import dataclass

@dataclass
class Step:
 """A single step in an agent's trajectory."""

 thought: str = ""
 action: dict | None = None
 observation: str | None = None
Part 1: What You Should Know About Large Language Models
|

answer: str | None = None
 metadata: dict | None = None
The Step is very much like the Response object with one major difference, the answer
and observation fields. The answer is the final answer of the model and represents
that the agent has reached the end of its turn. The observation is the output of
tool usage. They are consequences of any processing or results we get from the
TinyAgent. Finally, we use the term action to describe a tool call because in Chapter 6
we will explore loops of thought → action → observation that allow for autonomous
behavior.
To reach its final answer, an agent might need various steps and use different actions.
This sequence of steps is called the agent’s trajectory. We likewise track this informa‐
tion as it allows for easily debugging this sequence of steps to identify where and why
an agent might have failed.
The Trajectory that you are going to create is where each Step will be created and
filled with information related to the TinyAgent:
class Trajectory:
 """Records agent execution as a sequence of runs."""
 def __init__(self) -> None:
 self.runs: list[dict] = []

 def initialize(self, query: str) -> None:
 """Register a new run with the given query."""
 self.runs.append({"query": query, "steps": []})

 def add(self, response: Response, observation: str | None = None) -> None:
 """Record a step from a Response, optionally with an observation."""
 # Add THOUGHT
 step = Step(
 thought=response.reasoning or "",
 metadata=response.metadata,
 )

 # Add ACTION/OBSERVATION or ANSWER
 if observation is not None:
 step.action = response.tool_call
 step.observation = observation
 else:
 step.answer = response.content

 self.runs[-1]["steps"].append(step)
Updating your TinyAgent
Finally, you need to update the TinyAgent with only a few lines of code to add this
brain (the LLM) to your agent. Note that we focus on only single-step agents for now,
|
Chapter 2: Large Language Models

without any autonomy. This is behavior that will be added and explored in-depth in
Chapter 6:
class TinyAgent:
 """A minimal, modular, and educational agent framework."""

 def __init__(self, llm: LLM):
 self.llm = llm
 self.memory = None # Chapter 4: Add Memory
 self.tools = None # Chapter 5: Add Tools
 self.planner = None # Chapter 6: Add Planning

 self.trajectory = Trajectory()

 def run(self, task: str) -> str:
 """Run the agent on a task."""
 self.trajectory.initialize(task)
 return self._step(task)

 def _step(self, task: str) -> str:
 """Perform a single step."""
 messages = [{"role": "user", "content": task}]
 response = self.llm.generate(messages)
 self.trajectory.add(response)
 return response.content

 def _execute_action(self, action: str) -> str | None:
 """Execute a tool action."""
 # Placeholder - will be implemented in later chapters
 return f"Executed action: {action}"
Helper Functions
As you progress through the chapters, you might add just a single line of code to Tiny
Agent. That becomes difficult to spot as the number of lines of code in TinyAgent
grows. We prepared a number of helper functions in the illustrated-agents package
that will help you quickly see what (small) changes were made between two versions
of, for example, TinyAgent. These are all added to the notebooks in the associated
GitHub repository and are generally used like so:
from illustrated_agents.chapters.ch2 import tinyagents_diff
tinyagents_diff
Part 1: What You Should Know About Large Language Models
|

Or you can use them to inspect how a given class has changed between two chapters,
even if the chapters are far apart:
```
from illustrated_agents.chapters import ch1, ch6
from illustrated_agents.utils import DiffViewer
```

tinyagents_diff = DiffViewer(
 ch1.TinyAgent, ch6.TinyAgent,
 "Chapter 1 - TinyAgent", "Chapter 6 - TinyAgent"
)
To test if it works, initialize the TinyAgent again with the updated LLM and ask it a
question:
agent = TinyAgent(llm=llm)
response = agent.run("What is 2 + 2?")
print(response)
This gives you:
"2 + 2 is 4."
A straightforward answer—great!
Throughout these chapters we also will be looking at the trajectory quite often to
debug and see if the TinyAgent performed as expected. You can access the full
trajectory with:
print(agent.trajectory.runs)
This gives:
[
 {
 'query': 'What is 2 + 2?',
 'steps': [
 Step(
 thought='',
 action=None,
 observation=None,
 answer='2 + 2 is 4.',
 metadata={
 'model': 'gemma4:e4b', 'prompt_tokens': 17, 'completion_tokens': 9
 }
 )
 ]
 }
]
Your “Agent” is still nothing more than the LLM and has no additional behav‐
ior/capabilities that we can showcase yet. For that, we need to add more modules,
|
Chapter 2: Large Language Models