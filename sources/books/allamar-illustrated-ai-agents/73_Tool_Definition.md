---
title: "Tool Definition"
chapter_number: 73
page_start: 200
page_end: 204
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Tool Definition

def __init__(self, requires_approval: list[str] = []):
 """Initialize and select tools that require approval before execution.
 """
 self.registry = {}
 self.requires_approval = requires_approval

 def add_tool(self, name: str, func: Callable, description: str = "") -> None:
 """Register a tool that the Agent can use.

 Arguments:
 name: The name of the tool.
 func: The function implementing the tool.
 description: A description of the tool.
 """
 self.registry[name] = {"function": func, "description": description}

 @property
 def schemas(self) -> None:
 """Used only for native tool-calling."""
 return None
The class has two functions:
add_tool
Adds a tool to the registry variable as an entry to the dictionary
schemas
Schemas to be used for native tool calling (we’ll cover this later in the chapter)
Note that you can also select which tools require approval from the user before they
can be run. We cover this behavior more extensively in Chapter 10, where we create a
coding agent.
We can then register the tool like so:
# Register tool
tools = Tools()
tools.add_tool(
 name="multiply",
 func=multiply,
 description="Multiplies two numbers: multiply(a: str, b: str)"
)
Tool Definition
After creating the tool, we need to inform the LLM what the tool does; this is called
tool definition. Without communicating to the LLM which tools exist, what they do,
how they are used, and in which context they should be used, the LLM isn’t able to
properly use them.
|
Chapter 5: Tool Usage, Learning, and Protocols

There are several methods by which we can communicate this to the LLM:
Learning
(Specific) tool definition and usage are learned during training.
Prompting
The tool definition is shared with the LLM through structured prompts.
How to use (specific) tools and when they are needed is often learned during the
fine-tuning state of an LLM, where the model learns how to follow instructions and
use tools. This learning stage can be split up into two aspects: we either tune the
model to learn about specific tools or how to use tools in general. Learning about
specific tools can be costly and limit how many tools you can add to the model.
Instead, recent models (such as Qwen3 and DeepSeek-V3.2)4,5 typically focus on their
improved instruction-following capabilities and general tool use. Instead of learning
about specific tools, they learn to recognize definitions of tools in their prompts and
dynamically use them.
Using natural language
As (reasoning) LLMs are becoming easier to steer and dynamically learn to use tools,
we can share the tool definitions through prompts. When you have a small set of
tools the LLM should use, you can share that through the system prompt:
system_prompt = """
...

# Tool Definition
You can use the following tools:

- multiply(a, b): multiplies two numbers
- divide(a, b): divides a by b

# Tool Usage
When you need to use them, write: [function_name(value1, value2)]
...
"""
Note that the definition here isn’t following a standardized procedure. Frankly, this is
something we made up on the spot to show you that an LLM can call a tool any way
you decide. Assuming the model is capable enough of following those instructions,
if it uses TOOL(value1, value2) or perhaps structures like TOOL, value1, value2
it does not matter. The only thing you need is a small piece of code that recognizes
4 Yang, An et al. 2025. “Qwen3 Technical Report,” arXiv, 2505.09388.
5 Liu, Aixin et al. 2025. “DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models,” arXiv,
2512. 02556.
Tool Usage
|

when a tool is being called. This is called a validator or parser and requires the LLM
to closely follow the usage instructions. It can therefore be quite error-prone because
small errors in following the instructions might result in incomplete calls to the tools.
We’ll cover how the LLM actually calls a tool a bit later in this chapter.
Let’s start by extending the Tools class so it can create this system prompt:
class Tools(Tools):
 """Tool registry for the Agent."""

 @property
 def descriptions(self) -> str:
 """Get descriptions of all registered tools."""
 return "\n".join(
 f"`{tool}`: {self.registry[tool]['description']}"
 for tool in self.registry
 )

 @property
```
 def prompt(self) -> str:
 return f"""
```
# Tools

If needed, you can only use the following tools to assist you
in completing tasks:

{self.descriptions}

To use a tool, respond with JSON:
{{"tool": "name", "kwargs": {{"param": "value"}}}}
"""
The updated Tools class now has two additional functions:
description
A description of all registered tools
prompt
The instructions that will be sent to the LLM on how to call the tools
Let’s reregister the tools with the updated class and inspect the prompt:
# Register tool
tools = Tools()
tools.add_tool(
 name="multiply",
 func=multiply,
 description="Multiplies two numbers: multiply(a: str, b: str)"
)

# Show prompt
print(tools.prompt)
|
Chapter 5: Tool Usage, Learning, and Protocols

Which gives us:
"""
# Tools

If needed, you can only use the following tools to assist you
in completing tasks:

`multiply`: Multiplies two numbers: multiply(a: str, b: str)
`get_weather`: Gets weather: get_weather(location: str)

To use a tool, respond with JSON: {"tool": "name", "kwargs": {"param": "value"}}
"""
This is the system prompt that the model will always have access to.
Using structured function calling
Another method of sharing the definition of the tools with the LLM is through
structured function calling. Instead of messing around with the prompts ourselves
and optimizing how we describe and format each tool, we can define each tool in
structured schemas instead. These are typically JSON Schema objects that include the
function’s name, description, and its parameters (types, required fields, ranges, etc.).
An example of such a schema for our multiply tool is the following:
tool_schema = {
 "type": "function",
 "function": {
 "name": "multiply",
 "description": "Multiply two numbers",
 "parameters": {
 "type": "object",
```
 "properties": {
 "a": {
```
 "type": "number",
 "description": "First number"
 },
 "b": {
 "type": "number",
 "description": "Second number"
 }
 },
 "required": [
 "a",
 "b"
 ]
```
 }
 }
}
```
These schemas are often passed as a separate parameter when using external APIs.
OpenAI, for instance, uses the tools parameter where you can send over the JSON
Tool Usage
|

schemas of your tools. That allows the LLM or even the agent to treat it as special
metadata and process it beforehand if necessary. In practice, however, these schemas
are typically processed as if they were “regular” prompts and put into, for example,
the system prompt.
Although we are using structured JSON schemas for communication, the LLM still
has to interpret how to use the tool and when, which makes tool usage a difficult task.
Therefore, the more descriptive and clear the schema, the more likely the LLM will
make the right tool call decisions.
At this point, the user can finally ask their question. Since they have access to the
multiply function, let’s keep the query simple: “What is 5.1 times 7.3?” To illustrate
how this is going to be processed, we make use of the messages structure that we
explored in Chapter 4. This is visualized in Figure 5-6, where the system prompt
contains the definition of our tool.



![Figure 5-6: The system prompt may contain the full JSON schema for the LLM to use](images/fig_05-06_The_system_prompt_may_contain_the_full_J.png)

*Figure 5-6: The system prompt may contain the full JSON schema for the LLM to use*


Figure 5-6. The system prompt may contain the full JSON schema for the LLM to use
Regardless of whether you use a JSON schema or describe the tool, there are several
best practices for defining functions to take into account:
Document your tool
Include extensive descriptions to allow your agent to have a better understanding
of what the tool is capable of.
Minimize the number of tools
Although having many tools expands the capabilities of your agent, it will
become much more difficult to select and use the appropriate tool. Although
there is no gold standard, aim to minimize the number of tools rather than
maximize them. Using fewer than 10 tools is a good start. The next section, tool
selection, becomes more important as the number of tools grows.
Minimize the scope of a tool
Complex tools with many parameters are difficult to use, even for individuals, let
alone an agent. Having a function with dozens of parameters can be difficult to
use, especially for smaller models.
|
Chapter 5: Tool Usage, Learning, and Protocols