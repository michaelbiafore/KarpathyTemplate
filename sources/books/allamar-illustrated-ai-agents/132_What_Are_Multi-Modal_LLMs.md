---
title: "What Are Multi-Modal LLMs?"
chapter_number: 132
page_start: 350
page_end: 352
part: "Part II. Specialized Agents"
---
# What Are Multi-Modal LLMs?

In this chapter, we’ll explore how MLLMs are created and how they can understand
different types of modalities for various use cases.
What Are Multi-Modal LLMs?
MLLMs are LLMs that can process and/or generate more types of inputs (modalities)
than text. Common modalities are text, image, audio, and video inputs (Figure 9-1).



![Figure 9-1: Multi-modal LLMs may process multiple input modalities and/or generate](images/fig_09-01_Multi-modal_LLMs_may_process_multiple_in.png)

*Figure 9-1: Multi-modal LLMs may process multiple input modalities and/or generate*


Figure 9-1. Multi-modal LLMs may process multiple input modalities and/or generate
multiple output modalities
Most MLLMs generally focus on encoding information (input) rather than generating
information (output). It’s a much cheaper operation without necessarily requiring
large architectural changes (Figure 9-2). As such, these input modalities are often
used to guide the textual generation. Consider it contextual information for a given
task.
|
Chapter 9: Multi-Modal Understanding



![Figure 9-2: Most MLLMs focus on encoding information and generate only a single](images/fig_09-02_Most_MLLMs_focus_on_encoding_information.png)

*Figure 9-2: Most MLLMs focus on encoding information and generate only a single*


Figure 9-2. Most MLLMs focus on encoding information and generate only a single
modality (typically text)
Imagine you have an LLM agent that is in charge of building a website. Wouldn’t it
then be nice if the LLM agent could actually “see” the website (Figure 9-3)?



![Figure 9-3: An MLLM processing text and an image for optimizing a website design](images/fig_09-03_An_MLLM_processing_text_and_an_image_for.png)

*Figure 9-3: An MLLM processing text and an image for optimizing a website design*


Figure 9-3. An MLLM processing text and an image for optimizing a website design
What Are Multi-Modal LLMs?
|

There are three main components (with an optional fourth) in creating an MLLM
(Figure 9-4):
Encoder
Encodes a modality (images, audio, etc.) to features (embeddings)
Connector
Converts encoded features so the LLM can use them
LLM
(Pre-trained) model that processes encoded features and generates text
(Optional) Generator
Generates modalities aside from text



![Figure 9-4: Multi-modal understanding typically involves connecting the encoders of](images/fig_09-04_Multi-modal_understanding_typically_invo.png)

*Figure 9-4: Multi-modal understanding typically involves connecting the encoders of*


Figure 9-4. Multi-modal understanding typically involves connecting the encoders of
different modalities to a regular LLM (left), whereas multi-modal generation couples a
generator to the LLM for generating different modalities (right)
As Figure 9-4 suggests, creating an MLLM generally involves separately training a
base LLM and then adding multi-modality to it.
Note that this chapter will focus on multi-modal understanding (input modalities)
instead of multi-modal generation (output modalities). In particular, we’ll cover meth‐
ods of encoding different modalities into features and techniques for converting these
features so that the LLM can process them.
|
Chapter 9: Multi-Modal Understanding