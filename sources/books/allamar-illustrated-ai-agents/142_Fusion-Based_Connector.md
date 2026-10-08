---
title: "Fusion-Based Connector"
chapter_number: 142
page_start: 388
page_end: 390
part: "Part II. Specialized Agents"
---
# Fusion-Based Connector

Fusion-Based Connector
The previous connectors do not change the LLM’s architecture to enable multi-modal
understanding. With a fusion-based connector, extra modules are added to the LLM’s
architecture to enable a deep interaction and fusion between text and non-text
features.
One of the first methods in doing so is called Flamingo.22 This model uses pre-trained
LLMs as their basis and adds trainable cross-attention layers that can process the
input images. More specifically, images are processed with a vision encoder, and its
output is processed through a perceiver resampler. This resampler is a Transformer
model, much like the Q-Former, and maps the image embeddings to a fixed sequence
size. The output of the resampler is fed to the cross-attention layers that were added
to the LLM (Figure 9-48).



![Figure 9-48: The Flamingo fusion-based connector](images/fig_09-48_The_Flamingo_fusion-based_connector.png)

*Figure 9-48: The Flamingo fusion-based connector*


Figure 9-48. The Flamingo fusion-based connector
21 Bai, Jinze et al. 2023. “Qwen-VL: A Frontier large Vision-Language Model with Versatile Abilities,” arXiv,
2308. 12966.
22 Alayrac, Jean-Baptiste et al. 2022. “Flamingo: A Visual Language Model for Few-Shot Learning,” Advances in
Neural Information Processing Systems, 35: 23716-23736.
|
Chapter 9: Multi-Modal Understanding

Only the added cross-attention and perceiver resampler are trained; the pre-trained
vision encoder and LLM are frozen (Figure 9-49).
Let’s explore these two trainable modules in more detail, starting with the perceiver
resampler. The goal of the perceiver resampler is to extract the most important vision
features and output them in a fixed size, much like the Q-Former.



![Figure 9-49: In Flamingo, while the ViT/CLIP module is frozen, the perceiver resampler](images/fig_09-49_In_Flamingo_while_the_ViTCLIP_module_is.png)

*Figure 9-49: In Flamingo, while the ViT/CLIP module is frozen, the perceiver resampler*


Figure 9-49. In Flamingo, while the ViT/CLIP module is frozen, the perceiver resampler
is trained
These learned queries will have the same shape as expected by the LLM, and the fixed
size allows for reduced computation by focusing on only the most important visual
features.
The output embeddings are then passed to the additional cross-attention blocks that
are intertwined with LLM’s regular blocks. In these cross-attention blocks, the LLM
can then attend to both the image and text features.
They are referred to as “gated” cross-attention because they use a special gating
trick, which makes the conditioned model behave identically to the original LLM at
initialization. This is done by multiplying the layer outputs by tanh(α), where α is
a learnable scalar per layer initialized to 0. Since tanh(0) = 0, these layers initially
contribute nothing, preserving the pretrained LLM’s behavior. As training progresses,
Connecting Modalities
|

α learns to open the gate. This initialization strategy enhances training stability and
final performance (Figure 9-50).



![Figure 9-50: A decoder block of Flamingo](images/fig_09-50_A_decoder_block_of_Flamingo.png)

*Figure 9-50: A decoder block of Flamingo*


Figure 9-50. A decoder block of Flamingo
This fusion-based connector needs to adjust the architecture of the original LLM,
which makes it a bit less flexible than any of the previous techniques. However,
by integrating attention into its architecture, there is the potential for improved
performance.
|
Chapter 9: Multi-Modal Understanding