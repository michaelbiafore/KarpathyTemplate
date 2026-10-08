---
title: "Tool Calling"
chapter_number: 75
page_start: 206
page_end: 207
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Tool Calling



![Figure 5-8: An example of Retrieval-Augmented Generation (RAG) for searching and](images/fig_05-08_An_example_of_Retrieval-Augmented_Genera.png)

*Figure 5-8: An example of Retrieval-Augmented Generation (RAG) for searching and*


Figure 5-8. An example of Retrieval-Augmented Generation (RAG) for searching and
retrieving tool definitions
Tool Calling
Next, when the LLM ends its thinking process, it can start creating the tool call. It will
output a string, and if the LLM is capable enough, correctly format the tool call with
the given arguments. This is illustrated in Figure 5-9 with the system prompt that we
defined in the section “Tool Definition” on page 180.



![Figure 5-9: After reasoning, the answer may contain the tool call](images/fig_05-09_After_reasoning_the_answer_may_contain_t.png)

*Figure 5-9: After reasoning, the answer may contain the tool call*


Figure 5-9. After reasoning, the answer may contain the tool call
However, this answer is merely a string and will not execute the tool. In fact, you can
view this output as merely the intention of the LLM to call a tool. Without any help
from the user or additional software, nothing will happen. We will have to extend the
Tools class further with functions that extract and parse the JSON call:
```
import json
from typing import Any
from illustrated_agents.chapters.ch2 import Response
```


class Tools(Tools):
|
Chapter 5: Tool Usage, Learning, and Protocols

"""Tool registry for the Agent."""

 def parse(self, response: Response) -> Response:
 """Parse a JSON tool call from text."""
 text = response.content

 if '"tool":' in text or '"tool:"' in text:
 start, end = text.find("{"), text.rfind("}") + 1
 tool_call = json.loads(text[start:end])

 # Add the parsed tool call to the response
 return Response(
 content=response.content,
 reasoning=response.reasoning,
 tool_call=tool_call,
 )

 return response

 def execute(self, response: Response) -> Any:
 """Run a registered tool.

 Arguments:
 tool_call: A parsed tool call dict with "tool" and "kwargs" keys.
 """
 tool_call = response.tool_call
 name, kwargs = tool_call["tool"], tool_call.get("kwargs", {})

 # Human-in-the-loop: ask before running dangerous tools
 if name in self.registry and name in self.requires_approval:
 response = input(f"Allow {name}? [y/N] ").strip().lower()
 if response not in ("y", "yes"):
 return f"Tool '{name}' was denied by the user."

 # Handle registered tools
 if name in self.registry:
 tool_func = self.registry[name]["function"]
 return tool_func(**kwargs)

 return f"Tool '{name}' not found."
The updated Tools class now has two additional functions:
parse
Parses the string into JSON.
execute
Executes the tool call. Note that we also add a human-in-the-loop that allows you
to approve certain tools before execution. We cover the human-in-the-loop more
extensively in Chapter 10 where we create a coding agent.
Tool Usage
|