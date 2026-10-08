---
title: "Projection-Based Connector"
chapter_number: 140
page_start: 382
page_end: 384
part: "Part II. Specialized Agents"
---
# Projection-Based Connector

Projection-Based Connector
The most straightforward method of aligning the multi-modal embeddings with the
text embeddings that an LLM expects is by simply projecting them. This is typically
done with a single linear layer to convert these non-text embeddings to token embed‐
dings (Figure 9-42).



![Figure 9-42: An example of how a linear projection maps each input image to an output](images/fig_09-42_An_example_of_how_a_linear_projection_ma.png)

*Figure 9-42: An example of how a linear projection maps each input image to an output*


Figure 9-42. An example of how a linear projection maps each input image to an output
embedding
The projection doesn’t always have to be up (from fewer to more values) but can
also be down projected (from more to fewer values) if the non-text embeddings
are smaller than the token embeddings the LLM expects. The resulting projection
of the non-text embeddings is then concatenated with the token embeddings of the
text input. The LLM will treat every embedding as if it were a token embedding
(Figure 9-43).
|
Chapter 9: Multi-Modal Understanding



![Figure 9-43: A projection connector maps each output embedding of the image encoder](images/fig_09-43_A_projection_connector_maps_each_output.png)

*Figure 9-43: A projection connector maps each output embedding of the image encoder*


Figure 9-43. A projection connector maps each output embedding of the image encoder
to what the LLM expects (with respect to count, dimensions, and data distribution)
A great example of this technique is used in Large Language and Vision Assistant
(LLaVA).14 LLaVA is an MLLM that is not only able to process text but also reason
about images. This technique attempts to make Vicuna, a Llama 2 variant that can
process only text, multi-modal.15 The authors of LLaVA chose this model because, at
the time (2023), it had the best instruction-following capabilities.
LLaVA was created in two steps, using the same projection scheme we explored
previously (Figure 9-44):
Step 1: Pre-training for feature alignment
Only the projection layer is trained. The weights of both the ViT and LLM
(Vicuna) are frozen.
Step 2: Fine-tuning end-to-end
Both the projection layer and the LLM are trained. Only the ViT weights are
frozen.
14 Liu, Haotian et al. 2023. “Visual Instruction Tuning,” Advances in Neural Information Processing Systems, 36:
34892-34916.
15 Chiang, Wei-Lin et al. 2023. “Vicuna: An Open-Source Chatbot Impressing GPT-4 with 90%* Chat GPT
Quality,” Blog post, https://lmsys.org/blog/2023-03-30-vicuna.
Connecting Modalities
|



![Figure 9-44: The two-step training process of LLaVA](images/fig_09-44_The_two-step_training_process_of_LLaVA.png)

*Figure 9-44: The two-step training process of LLaVA*


Figure 9-44. The two-step training process of LLaVA
As shown, this projection-based connector needs to be trained (as is the case with all
connectors) to properly project the initial embeddings to what a specific LLM needs,
in this case the Vicuna model.
This training procedure uses text/image pairs to train the MLP and LLM. The first
step is meant to align the type of embeddings to what the Vicuna model expects.
The second step allows the LLM to learn to reason about the text/image pairs. The
resulting model demonstrated, at the time, state-of-the-art multi-modal chat capabil‐
ities for publicly available models. Likewise, this training procedure has made it
relatively straightforward to create a multi-modal LLM. As such, the projection-based
technique, albeit simple in nature, is still used for more recent architectures like
Qwen2.5-VL,16 Phi-4-multimodal,17 and Janus.18 Moreover, this projection can be
used for any modality, not only images.
16 Bai, Shuai et al. 2025. “Qwen2.5-VL Technical Report,” arXiv, 2502.13923.
17 Abouelenin, Abdelrahman et al. 2025. “Phi-4-mini Technical Report: Compact Yet Powerful Multimodal
Language Models via Mixture-of-loras,” arXiv, 2503.01743.
18 Wu, Chengyue et al. 2025. “Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and
Generation,” Proceedings of the Computer Vision and Pattern Recognition Conference.
|
Chapter 9: Multi-Modal Understanding