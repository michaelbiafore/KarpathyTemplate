---
title: "Query-Based Connector"
chapter_number: 141
page_start: 385
page_end: 387
part: "Part II. Specialized Agents"
---
# Query-Based Connector

Query-Based Connector
A more involved method of connecting modalities is through a query-based connec‐
tor. This connector is meant to extract relevant features from all non-textual inputs
before feeding them to the LLM (Figure 9-45). These relevant features are generally
referred to as “queries” and are learnable by this connector, commonly referred to as
the Q-Former.



![Figure 9-45: The Q-Former, which maps the input to a fixed set of embeddings, com‐](images/fig_09-45_The_Q-Former_which_maps_the_input_to_a_f.png)

*Figure 9-45: The Q-Former, which maps the input to a fixed set of embeddings, com‐*


Figure 9-45. The Q-Former, which maps the input to a fixed set of embeddings, com‐
pressing the amount of information before feeding it to a projection connector
Instead of projecting all ViT features to the LLM, like the projection-based connector,
the Q-Former creates a fixed number of features that the LLM can process. A major
benefit to this approach is that it learns only the most relevant visual information.
The Q-Former was first introduced in BLIP-2, an MLLM that uses a Transformer
model to process both image features and text features.19 During training, the Trans‐
former model will receive learnable queries, embeddings that get “updated” with
relevant visual and textual information.
19 Li, Junnan et al. 2023. “BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and
Large Language Models,” International Conference on Machine Learning, PMLR.
Connecting Modalities
|

This Transformer model has two modes, one with cross-attention for processing the
images and one without cross-attention to process the text (Figure 9-46).



![Figure 9-46: The two modes of the Q-Former, one for processing the images (left) and](images/fig_09-46_The_two_modes_of_the_Q-Former_one_for_pr.png)

*Figure 9-46: The two modes of the Q-Former, one for processing the images (left) and*


Figure 9-46. The two modes of the Q-Former, one for processing the images (left) and
one for processing the text (right)
Since this Transformer model has two modes, this model can then be trained using
contrastive learning using image/text pairs.
The output embeddings of this model are the learned queries, which contain the
image embeddings’ most relevant information. It’s essentially a way to compress
visual tokens into a smaller number of representation vectors.
There are two stages in this training process. In stage 1, the Q-Former was trained on
three tasks such that the queries can learn to extract the visual representation that is
most informative of the text:
|
Chapter 9: Multi-Modal Understanding

Image-text contrastive learning
Aligns image and text representations by maximizing mutual information
Image-grounded text generation
Trains the Q-Former to generate text conditioned on images
Image-text matching
Binary classification to predict if image-text pairs match
In stage 2, the trained Q-Former is connected to an LLM (OPT)20 to improve the
LLM’s generative capabilities. The output query embeddings are projected through an
MLP to match the LLM’s input dimensions. Then, only the Q-Former and MLP are
trained; the LLM and image encoder are frozen (Figure 9-47).



![Figure 9-47: The two-step process of training the Q-Former](images/fig_09-47_The_two-step_process_of_training_the_Q-F.png)

*Figure 9-47: The two-step process of training the Q-Former*


Figure 9-47. The two-step process of training the Q-Former
This technique was used in Qwen’s first multi-modal LLM, namely Qwen-VL.21 Like
the projection-based connector, this connector can be used for any modality.
20 Zhang, Susan et al. 2022. “OPT: Open Pre-trained Transformer Language Models,” arXiv, 2205.01068.
Connecting Modalities
|