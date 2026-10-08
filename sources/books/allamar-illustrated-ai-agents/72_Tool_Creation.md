---
title: "Tool Creation"
chapter_number: 72
page_start: 199
page_end: 199
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Tool Creation

Tool Creation
Although tools can come in various forms, they are typically functions that can be
accessed through either an API or some internal code. This can be as complex or
minimal as is required for your application. LLMs, for instance, are not known for
their mathematical capabilities. Let’s create a simple function for multiplying two
values that the LLM can use:
```
def multiply(a: str, b: str) -> float:
 return float(a) * float(b)
```
This function multiplies two values, taking them as strings and converting them to
floats. The reason for this is that LLMs return only text, which will have to be con‐
verted. As such, these tools should be heavily documented and communicated well
to the LLM. In some cases, the docstrings are passed automatically, so it is important
to describe them well. A clear benefit is that it motivates users to focus more on
writing great documentation, which is often not a priority when developing code.
Although this is a rather simplified example, imagine codebases with functions that
span hundreds of lines of code. Documentation is becoming increasingly important,
as it allows the agent to understand which edge cases exist or implementation details
that cannot be easily determined by examining the code.
This tool can be accessed by directly calling multiply(a, b), which is something the
LLM cannot do since it only outputs strings, but it can be done by an automated
system. Note that external API calls may also call tools. Either way, a tool is generally
considered to be some form of function that can be called in various ways. In our
example, the most straightforward method would be to save it in a dictionary so that
we can access the function by a string. In this case, our database is the registry
variable:
registry = {
 "multiply": multiply
}
Creating tools can be a straightforward process, but the LLM should be taken into
account when designing them. It’s a similar process to designing code for people to
use, where you may ask yourself: does the user understand what the tool does? Is it
clear what is being returned? Are the variable names descriptive? Is there documenta‐
tion? This is especially important for LLMs because they often need to be explicitly
told what exists, what doesn’t, and what the tools are capable of.
Let’s start by creating the first iteration of the Tools class that will give your Tiny
Agent access to tools:
from typing import Callable

class Tools:
 """Tool registry for the Agent."""
Tool Usage
|