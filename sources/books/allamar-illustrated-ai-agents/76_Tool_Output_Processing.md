---
title: "Tool Output Processing"
chapter_number: 76
page_start: 208
page_end: 210
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Tool Output Processing

We reinitialize the Tools class and reregister the tool. Then, let’s demonstrate with an
example of how the tool would be executed:
tools = Tools()
tools.add_tool(
 "multiply", multiply, "Multiplies two numbers: multiply(a: str, b: str)"
)
# Fake LLM response
response = Response(
 content='{"tool": "multiply", "kwargs": {"a": "3.1", "b": "6.5"} }'
)
# Parse into a tool call
response = tools.parse(response)
# Execute the tool
tools.execute(response)
Which gives:
20. 150000000000002
Great! The Response object contains the content of the model and parses that into a
tool call. After parsing, the JSON can be used to actually call the tool.
Although regular expressions can be used to extract our tool, they
will not work if the tool call has a very slightly different structure
or if the JSON structure is more complex. Instead, more robust
techniques might be needed to extract the arguments, such as json‐
schema, which is a Python package for validating JSON schemas.



![Figure on page 17](images/fig_p017_x95.png)


Another common technique is to use Pydantic, a Python package
for data validation. It can be used to create data classes where each
piece of data can be validated. It allows you to create JSON schemas
of your tools to feed to the LLM. Likewise, the output of the LLM
can be converted to JSON and validated through Pydantic.
Tool Output Processing
We still need to do something with the output of the tool call. In our example, the
LLM ends with a tool call, which we process and call ourselves. To feed the output
back into the LLM, we can use the messages structure that we explored in Chapter 4.
Specifically, we can add messages with two roles:
assistant
The assistant calls the multiply tool.
|
Chapter 5: Tool Usage, Learning, and Protocols

tool
The output of the tool is returned.
By updating the messages to include this additional information, we’re essentially
informing the LLM that these steps were taken. Calling the tool was done outside
of the LLM’s view, and it therefore has no knowledge of what actually happened. As
such, we pretend as if the LLM executed the tool, while that was actually done by the
user or an automated system. These updated messages are illustrated in Figure 5-10.
The specific tool role is used only by LLMs that were trained specifically to perform
native tool calling (more on that in the section “Tool Learning” on page 195). For
LLMs that were not trained with specific tool-calling tokens, we have to approach it a
bit differently.



![Figure 5-10: An example of the JSON structure used to call tools](images/fig_05-10_An_example_of_the_JSON_structure_used_to.png)

*Figure 5-10: An example of the JSON structure used to call tools*


Figure 5-10. An example of the JSON structure used to call tools
Instead of using the tool role, we can use the user role and act as if we are explicitly
telling the LLM what the output of the tool call was. To do so, let’s update the Tools
```
class to add this behavior:
class Tools(Tools):
```
 """Tool registry for the Agent."""

 def observation(self, result: str) -> tuple[str, str]:
 """Return the observation as a user."""
 return "user", f"OBSERVATION: {result}"

 def is_done(self, response: Response) -> bool:
 """The `TinyAgent`'s stopping mechanism."""
 if not response.tool_call:
 return True
 if response.tool_call["tool"] == "final_answer":
 response.content = response.tool_call.get("kwargs", "")
Tool Usage
|

```
return True
 return False
```
The updated Tools class now has two additional functions:
observation
Returns the output of the tool call
is_done
Stops your TinyAgent if there is no tool call or it calls the final_answer tool. In
Chapter 6, we’ll explore the final_answer tool in more depth when the agent has
to decide how to give back a final answer.
Of note is the observation function, which returns the role (user) and the output
of the tool call as an OBSERVATION tag. This OBSERVATION tells the model
that the user has observed the tool call and gives back its result. The idea is that a
conversation history then looks a bit as shown in Figure 5-11.



![Figure 5-11: An example of how the user role can be used to relay the output of the tool](images/fig_05-11_An_example_of_how_the_user_role_can_be_u.png)

*Figure 5-11: An example of how the user role can be used to relay the output of the tool*


Figure 5-11. An example of how the user role can be used to relay the output of the tool
call back to the LLM
We then feed these messages back into the LLM to create our final answer. Although
the tool has given us the appropriate output, the LLM might want to combine/sum‐
marize answers or present them in a nicer way or according to pre-decided instruc‐
tions. This process, along with the updated output, is presented in Figure 5-12.
|
Chapter 5: Tool Usage, Learning, and Protocols