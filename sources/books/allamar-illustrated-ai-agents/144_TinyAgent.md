---
title: "TinyAgent"
chapter_number: 144
page_start: 391
page_end: 394
part: "Part II. Specialized Agents"
---
# TinyAgent

Advantages and Disadvantages
Before ending this chapter, it’s worthwhile to go into the advantages and disadvan‐
tages of the connectors we explored thus far (Table 9-1).
Table 9-1. Advantages and disadvantages of connectors
Connectors
Advantages
Disadvantages
Projection-
based
Scalability: It can produce a large number of tokens,
which quickly fills up the LLM’s context window.
Performance: Since it’s decoupled from the LLM and the
model is rather small, it has limited expressive power.
Query-based
Scalability: The fixed number of queries allows
for scaling with large multi-modal inputs (e.g.,
videos).
Performance: Has more expressive power than
projection-based connectors.
Simple: Lightweight to implement.
Computational efficiency: Low latency and few
parameters.
Complexity: Requires relatively complex training
procedures.
Computational efficiency: Due to the larger models, it
adds more latency than a projection-based connector.
Fusion-based
Integration: The integration with the LLM itself
allows it to “see” multi-modal features at every
layer instead of just as a prefix.
Performance: Has more expressive power
than both projection-based and query-based
connectors.
Complexity: Requires changes to the architecture of the
LLM.
Computational efficiency: Requires the LLM to undergo
extensive fine-tuning procedures, more so than the other
connectors.
There are three main axes at which we can view the potential (dis)advantages of
these connectors, namely their performance, computational efficiency, and scalability.
Generally, projection-based connectors are used for simplicity and computational
efficiency because these connectors are lightweight and easy to train. However, they
may quickly fill up the LLM’s context window since the input is not compressed.
Query-based connectors are primarily used for efficiency and scaling because they
keep the input length constant regardless of the image/video resolution. However,
a query-based connector may skip over details as it does not have the fine-grained
representation of projection-based connectors. Finally, fusion-based connectors tend
to perform best because the processing of the multi-modal input is done throughout
the entire model, rather than just as token embeddings. However, they’re the most
complex connectors to implement (requiring changes to the LLM’s architecture) and
are expensive to train.
TinyAgent
Throughout this chapter, we covered how multi-modal models are created using
methods like SFT and RL. The resulting models can process more than text and
typically have either vision or audio understanding. The model that we’ve been using
thus far, Gemma 4 E4B, has both. It can process both images and audio. To do so, it
has two encoders to process those modalities, a vision encoder for processing images
TinyAgent
|

and an audio encoder for processing sound. You can find more about the vision and
audio encoders of Gemma 4 E4B in “A Visual Guide to Gemma 4”:
from illustrated_agents.chapters.ch2 import LLM


# Gemma 4 E4B (with native thinking and tool calling)
llm = LLM(model="gemma4:e4b", think=True)
The vision encoder in Gemma 4 E4B generates a set of embeddings (also called vision
tokens or image tokens) that the LLM can use. In the raw chat template, that tends to
look something like this:
<|image> <|image|><|image|><|image|><|image|><|image|> … <|image|> <image|>
Those are special image tokens used to indicate that a given embedding belongs to an
image. The <|image> and <image|> tokens indicate the start and end, respectively, of
a sequence of image tokens. The <|image|> is a vision token. In Gemma 4 E4B, there
are generally either a maximum of 70, 140, 280, 560, or 1,120 vision tokens. A larger
number of vision tokens means that the input image will be processed at a higher
resolution. If you chose a different model, then it might use a different chat template
and token structure. In practice, however, they all work similarly.
As we saw in Chapter 5, the processing of this chat template is almost always handled
by the inference engine. So there’s no need for us to create templates with potentially
1,120 vision tokens. The OpenAI endpoint that we’ve been using thus far expects the
following format:
[
 {
 "role": "user",
 "content": [
 {
 "type": "image_url",
 "image_url": {
 "url": "https://raw.githubusercontent.com/HandsOnLLM/
 Hands-On-Large-Language-Models/main/images/book_cover.png"
 },
 },
 {"type": "text", "text": "What’s in this image?"},
 ],
 }
]
We now have two fields in the content, one for the image and one for the text itself.
These will be processed in the chat template of the model. Note that in some cases,
the URL needs to be the image itself (in base64) rather than a link to the image. This
depends on the inference engine. Some will attempt to convert the image themselves,
while others can only process the base64 image.
|
Chapter 9: Multi-Modal Understanding

Note how this example showcases the message’s structure that we explored in detail
in Chapter 4, where we covered memory. The messages not only function as the
memory of the model but also as the way we communicate with it. As such, the place
to enable image inputs is in the Memory class!
To do so, we need only a very minor change to the Memory class, and that is to add the
image_url to the messages if there is an input image. Everything else can stay exactly
the same:
from illustrated_agents.chapters.ch4 import Memory


class MultimodalMemory(Memory):
 """Simple memory module to store conversation history."""

 def add(
 self,
 role: str,
 content: str,
 tool_call: dict = None,
 image_data: str = None,
 ):
 """Add a message to memory."""
 # Image
 if image_data:
 is_url = image_data.startswith(("http://", "https://"))
 url = image_data if is_url else f"data:image/png;base64,{image_data}"
 content = [
 {"type": "image_url", "image_url": {"url": url}},
 {"type": "text", "text": content},
 ]

 # Main message
 message = {"role": role, "content": content}

 # Tool call
 if tool_call:
 message["tool_calls"] = [tool_call]

 # Append message to memory
 self.messages.append(message)
Note that we added the option to use either a URL or the base64-encoded image. This
allows for support for different inference engines.
To give the newly created MultimodalMemory the image, we also need to update the
run function of your TinyAgent. We highlighted the code that was updated:
from illustrated_agents.chapters import ch6


class TinyAgent(ch6.TinyAgent):
TinyAgent
|

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
The only changes we made are:
- Add the image_data parameter to the run function.
•
- Add the image_data parameter to self.memory.add.
•
That is all that’s needed to use your model’s image-understanding capabilities! Let’s
try it out with an example. We ask the agent to tell us which animal is on the cover of
the Hands-On Large Language Model book, but we do not provide it with an image:
```
from illustrated_agents.chapters.ch5 import NativeTools
from illustrated_agents.chapters.ch6 import NativeReAct
```

# Multi-modal Agent
agent = TinyAgent(
 llm=llm,
 tools=NativeTools(),
 memory=MultimodalMemory(),
 planner=NativeReAct()
)

# Run Agent
agent.run("Which animal is on the cover of 'Hands-On Large Language Models'?")
Which gives:
"I do not have the ability to view specific commercial book covers or know
which edition you are referring to, as covers can sometimes change!\n\n
If you can provide an image of the book cover, I would be happy to tell you
what animal is featured.\n\nOtherwise, if the cover is highly abstract or
doesn't feature an animal, please let me know!"
It doesn’t know which animal is on the cover. Now, let’s give it the image:
```
import base64
import httpx
```

# Download and encode the image
image_url = "https://raw.githubusercontent.com/HandsOnLLM/
Hands-On-Large-Language-Models/main/images/book_cover.png"
|
Chapter 9: Multi-Modal Understanding