---
title: "Advantages and Disadvantages"
chapter_number: 143
page_start: 391
page_end: 391
part: "Part II. Specialized Agents"
---
# Advantages and Disadvantages

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