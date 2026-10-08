---
title: "TinyAgent with Native Tool-Calling Capabilities"
chapter_number: 82
page_start: 226
page_end: 231
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# TinyAgent with Native Tool-Calling Capabilities



![Figure 5-24: Training process to create Search-Qwen2.5](images/fig_05-24_Training_process_to_create_Search-Qwen25.png)

*Figure 5-24: Training process to create Search-Qwen2.5*


Figure 5-24. Training process to create Search-Qwen2.5
These kinds of frameworks and methodologies leveraging RL have become increas‐
ingly popular as the reward structure for tool calling is generally quite straightfor‐
ward. It’s trivial to check if a tool has been called correctly and if the correct
arguments have been used (as in ToolRL). Moreover, RL works well for rewards
that are verifiable, such as coding and tool calling. As such, there has been an increase
in models that were trained using RL and additionally adopted tool-based rewards,
such as the strong open source Qwen3 and GPT-OSS models.12,13
TinyAgent with Native Tool-Calling Capabilities
SFT and RL are great techniques for instilling tool-calling behavior into the models
themselves without needing to perform explicit CoT instructions in your prompts.
This process, as illustrated previously, does create a bit of “magic” when running
these tool-calling capabilities with inference engines like Ollama or llama.cpp. This
“magic” we refer to is the conversion of a standard method for calling tools to the
chat template that the specific LLM uses. As we explored previously, some LLMs use
<think> tokens for instance, while others use something like <|think|>. Each LLM is
trained differently, with different tokens, and the inference engine “hides” that from
the user. Although that makes for an easy UX, it doesn’t serve well for the educational
nature of this book. So let’s uncover the “magic”!
12 Yang, An et al. 2025. “Qwen3 Technical Report,” arXiv, 2505.09388.
13 Agarwal, Sandhini et al. 2025. “GPT-OSS-120b & GPT-OSS-20b Model Card,” arXiv, 2508.10925.
|
Chapter 5: Tool Usage, Learning, and Protocols

Most inference engines make use of a standardized format in describing tools, namely
JSON. As we discussed in the section “Tool Definition” on page 180, we can use a
JSON schema to describe a tool and pass it to the LLM for it to use. As such, all we
have to do is use the tool_schema variable we defined in the section “Tool Definition”
on page 180 and pass it along to the OpenAI endpoint. We make use of Gemma 4
E4B, which unlike Gemma 3 12B, was trained specifically to perform tool calling:
```
import json
import urllib.request
```

# Prompt
messages = [{"role": "user", "content": "What is 5.1 times 7.3?"}]

# Prepare the data
body = {
 "model": "gemma4:e4b",
 "messages": messages,
 "stream": False,
 "tools": [tool_schema],
}

# Prepare the request
request = urllib.request.Request(
 "http://localhost:11434/api/chat",
 data=json.dumps(body).encode(),
 headers={"Content-Type": "application/json"},
)

# Call and parse the response
with urllib.request.urlopen(request) as response:
 print(json.loads(response.read())["message"])
This gives:
{
 'role': 'assistant',
 'content': '',
 'thinking': "1. **Identify the user's request:**
 The user wants to calculate the product of 5.1 and 7.3.",
 'tool_calls': [
 {
 'id': 'call_0mufz9dn',
```
 'function': {
 'index': 0, 'name': 'multiply', 'arguments': {'a': 5.1, 'b': 7.3}
 }
 }
```
 ]
}
Note how the output “just” outputs the tool call without us having to do anything
special. This is because Ollama handles various things, but two stand out. First, it
Tool Learning
|

communicates to the LLM which tools exist. Second, it converts the LLMs tool call to
this parsed output.
To uncover the “magic,” let’s start from Gemma 4 E4B’s chat template. As shown
in Figure 5-25, it uses several special tokens (e.g., <|turn>) to parse the input and
output of the model.



![Figure 5-25: The chat template of Gemma 4 E4B](images/fig_05-25_The_chat_template_of_Gemma_4_E4B.png)

*Figure 5-25: The chat template of Gemma 4 E4B*


Figure 5-25. The chat template of Gemma 4 E4B
To define a given tool, such as the multiply function we covered previously, it expects
the format as shown in Figure 5-26.



![Figure 5-26: The tool declaration between the <|tool> and <tool|> tokens of the](images/fig_05-26_The_tool_declaration_between_the_tool_an.png)

*Figure 5-26: The tool declaration between the <|tool> and <tool|> tokens of the*


Figure 5-26. The tool declaration between the <|tool> and <tool|> tokens of the
multiply function (the indentation is merely for illustration purposes)
|
Chapter 5: Tool Usage, Learning, and Protocols

Under the hood, inference engines convert the JSON schema we used in tool_schema
to whatever the LLM expects. How this translation is done is up to the inference
provider, but it always needs to convert to whatever the LLM is trained on.
Now, let’s explore how we can use the native tool-calling capabilities of an LLM and
use them in your TinyAgent. Among others, the following needs to be implemented:
Creating a tool_to_schema function
A function for converting a Python function to an OpenAI-compatible JSON
schema
Creating the NativeTools class
A variant of Tools that creates and parses tool calls
Let’s start with the tool_to_schema function. It is a helper function that easily allows
us to convert any given function to a JSON schema by inspecting the function’s name,
docstrings, and parameters:
```
import inspect
from typing import Callable
```

# Convert specific types to string descriptions
TYPE_MAP = {
 str: "string", int: "integer", float: "number",
 bool: "boolean", list: "array", dict: "object"
}

def tool_to_schema(function: Callable) -> dict:
 """Convert a Python function to an OpenAI-style tool schema."""
 signature = inspect.signature(function)

 # Extract meatadata
 properties, required = {}, []
 for name, parameter in signature.parameters.items():
 properties[name] = {"type": TYPE_MAP.get(parameter.annotation, "string")}
 if parameter.default is inspect.Parameter.empty:
 required.append(name)

 # Fill schema
 schema = {
 "type": "function",
 "function": {
 "name": function.__name__,
 "description": inspect.getdoc(function),
 "parameters": {
 "type": "object",
 "properties": properties,
 "required": required,
 },
 },
 }
Tool Learning
|

return schema
You can run it like so:
print(tool_to_schema(multiply))
This gives:
{
 'type': 'function',
 'function': {
 'name': 'multiply',
 'description': 'Multiply two values.',
 'parameters': {
 'type': 'object',
 'properties': {'a': {'type': 'string'}, 'b': {'type': 'string'}},
 'required': ['a', 'b']
```
 }
 }
}
```
This standardized format is OpenAI-compatible, and the inference engine will con‐
vert this to the model’s chat template. Next, let’s make the NativeTools class that
creates this schema and parses the output so it can be used to execute tool calls:
```
import json
from illustrated_agents.chapters.ch2 import Response
from illustrated_agents.chapters.ch5 import Tools
```


class NativeTools(Tools):
 """Tool registry using native function calling."""

 @property
 def schemas(self) -> list[dict]:
 """Return tool functions for native function calling."""
 return [
 tool_to_schema(tool["function"]) for tool in self.registry.values()
 ]

 @property
 def prompt(self) -> str:
 """Empty because we don't need a prompt for native tool calling"""
 return ""

 def parse(self, response: Response) -> Response:
 """Parse a tool call."""
 # If there's no tool call, return the response as is
 if not response.tool_call:
 return response

 # Extract the tool name and arguments from the tool call
 args = response.tool_call["function"]["arguments"]
|
Chapter 5: Tool Usage, Learning, and Protocols

if isinstance(args, str):
 args = json.loads(args)
 tool_call = {
 "tool": response.tool_call["function"]["name"],
 "kwargs": args,
 }

 # Add the parsed tool call to the response
 return Response(
 content=response.content,
 reasoning=response.reasoning,
 tool_call=tool_call,
 )

 def observation(self, result: str) -> tuple[str, str]:
 """Native tool results use the 'tool' role."""
 return "tool", str(result)

 def is_done(self, response: Response) -> bool:
 """No tool call means the `TinyAgent` is done."""
 return not response.tool_call
The NativeTools class follows Tools closely and makes a couple of changes:
schemas
Create an OpenAI-compatible schema in JSON.
prompt
No prompt is needed because that is handled by the inference engine.
parse
Converts the LLM’s tool call into JSON and stores it in the Response class.
observation
The observation is now tracked in the tool role.
Usage is exactly the same as the Tools class. All we need to do is add the tools and
give them to your TinyAgent. Then, we can ask it the same query we did before to see
if it uses a tool:
```
from illustrated_agents.chapters.ch4 import Memory
from illustrated_agents.chapters.ch5 import TinyAgent
```

# Tools
tools = NativeTools()
tools.add_tool("multiply", multiply)

# Memory
memory = Memory()

# Initialize Agent
Tool Learning
|