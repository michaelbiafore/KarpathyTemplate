---
title: "Connecting Modalities"
chapter_number: 139
page_start: 379
page_end: 381
part: "Part II. Specialized Agents"
---
# Connecting Modalities



![Figure 9-39: ImageBind demonstrates emergent alignment of modalities despite not](images/fig_09-39_ImageBind_demonstrates_emergent_alignmen.png)

*Figure 9-39: ImageBind demonstrates emergent alignment of modalities despite not*


Figure 9-39. ImageBind demonstrates emergent alignment of modalities despite not
being trained together
This emergent alignment of unseen pairs of modalities showcases how strong this
“binding” factor of images can be.
Connecting Modalities
We explored how representations (embeddings) can be created for many different
modalities. Before we can feed those to the LLM, making it multi-modal, there’s a big
problem with the generated embeddings.
As we explored earlier in this chapter, the encoders for each modality generally create
different embeddings with respect to their size, dimensions, and embedding space
than what the LLM might expect. Likewise, there might be differences in positional
encoding and tokenization schemas. As such, we need a connector that transforms
those embeddings to the same type of embeddings as its token embeddings (see
Figure 9-40).
Connecting Modalities
|



![Figure 9-40: The connector is needed to align different types of encoders to what the](images/fig_09-40_The_connector_is_needed_to_align_differe.png)

*Figure 9-40: The connector is needed to align different types of encoders to what the*


Figure 9-40. The connector is needed to align different types of encoders to what the
LLM expects
There are roughly three types of connectors (Figure 9-41):12,13
Projection-based
A Multi-Layer Perceptron (MLP) to project multi-modal embeddings into an
embedding size compatible with the LLM
Query-based
Leveraging groups of learnable query tokens to extract information in a query-
based manner
12 Cui, Can et al. 2024. “A Survey on Multimodal Large Language Models for Autonomous Driving,” Proceedings
of the IEEE/CVF Winter Conference on Applications of Computer Vision.
13 Caffagni, Davide et al. 2024. “The Revolution of Multimodal Large Language Models: a Survey,” arXiv,
2402. 12451.
|
Chapter 9: Multi-Modal Understanding

Fusion-based
Adding additional (cross-attention) layers in the LLM that can process both text
and other multi-modal embeddings



![Figure 9-41: The three types of connectors: the projection, query, and fusion connectors](images/fig_09-41_The_three_types_of_connectors_the_projec.png)

*Figure 9-41: The three types of connectors: the projection, query, and fusion connectors*


Figure 9-41. The three types of connectors: the projection, query, and fusion connectors
Let’s explore these types, one by one, in more detail!
Connecting Modalities
|