---
title: "Summary"
chapter_number: 145
page_start: 395
page_end: 396
part: "Part II. Specialized Agents"
---
# Summary

image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")

# Run Agent with Image Data
agent.run(
 "Which animal is on the cover of 'Hands-On Large Language Models'?",
 image_data=image_data
)
Which gives:
"The animal on the cover of 'Hands-On Large Language Models' is a **kangaroo**."
That is correct! All that was needed to use its multi-modal capabilities was to process
the image in the chat template, which was handled by the inference engine for us.
What We Built
TinyAgent/
├── agent.py ← Updated (The Agent processes images)
├── evaluator.py
├── llm.py
├── memory.py ← Updated (Track images in the messages)
├── planning.py
├── toolbox.py
├── tools.py
└── trajectory.py
Summary
In this chapter, we explored how LLMs can develop multi-modal understanding.
We first covered various techniques for encoding different modalities, with a focus
on images (ViT/CLIP), audio (wav2vec 2.0, Whisper, CLAP), and videos (ViViT,
TimeSformer, “just CLIP”). These techniques were typically Transformer models,
further demonstrating the power of this fundamental technique. We also discovered
ImageBind, an encoding technique for processing many different modalities (images,
audio, videos, thermal, IMU, depth) at once.
We then explored how these multi-modal encoding techniques could be connected
to pre-trained LLMs. With a projection-based connector, the output of the encoding
technique was directly projected to the LLM using an MLP. With a query-based
connector, the output of the encoding technique was thoroughly processed using a
Transformer model combined with an MLP. Lastly, with a fusion-based connector,
additional cross-attention blocks were added to the pre-trained LLM that could be
trained.
In the next and final chapter, we cover how a specialized type of agent can be created,
namely the coding agent.
Summary
|