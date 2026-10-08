---
title: "Encoding Modalities"
chapter_number: 133
page_start: 353
page_end: 353
part: "Part II. Specialized Agents"
---
# Encoding Modalities

Encoding Modalities
Encoding different modalities is generally a process of converting a given input (text,
image, audio, etc.) to embeddings (Figure 9-5).



![Figure 9-5: Different modalities have different encoders and may produce different](images/fig_09-05_Different_modalities_have_different_enco.png)

*Figure 9-5: Different modalities have different encoders and may produce different*


Figure 9-5. Different modalities have different encoders and may produce different
embeddings
This process is a vital part of the “making LLMs multi-modal” pipeline because the
LLM expects embeddings as input (Figure 9-6).



![Figure 9-6: In the multi-modal understanding pipeline, the encoder is in charge of](images/fig_09-06_In_the_multi-modal_understanding_pipelin.png)

*Figure 9-6: In the multi-modal understanding pipeline, the encoder is in charge of*


Figure 9-6. In the multi-modal understanding pipeline, the encoder is in charge of
converting the input to embeddings
Let’s go over some of the main methods for encoding common modalities, starting
with the backbone of the MLLMs, the LLM.
Encoding Modalities
|