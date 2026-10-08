---
title: "Images"
chapter_number: 135
page_start: 357
page_end: 359
part: "Part II. Specialized Agents"
---
# Images

Images
To encode images to embeddings, similar to the process of text encoder, an adapta‐
tion of the Transformer is used, namely the Vision-Transformer (ViT).1
Vision-Transformer
The first step of the ViT is to mimic textual tokens. Instead of actually creating
tokens, ViT creates patches of images where each patch is considered a “word”
(Figure 9-12).



![Figure 9-12: The Vision-Transformer mimics the tokenizer in an LLM by cutting up the](images/fig_09-12_The_Vision-Transformer_mimics_the_tokeni.png)

*Figure 9-12: The Vision-Transformer mimics the tokenizer in an LLM by cutting up the*


Figure 9-12. The Vision-Transformer mimics the tokenizer in an LLM by cutting up the
input into pieces, here called patches
After its “tokenization” process of the input image, it flattens the resulting patches
and applies a projection so that a regular Transformer encoder can process the input
as if it were tokens (Figure 9-13).
1 Dosovitskiy, Alexey. 2020. “An Image Is Worth 16x16 Words: Transformers for Image Recognition at Scale,”
arXiv, 2010.11929.
Encoding Modalities
|



![Figure 9-13: Image processing and understanding in the Vision-Transformer](images/fig_09-13_Image_processing_and_understanding_in_th.png)

*Figure 9-13: Image processing and understanding in the Vision-Transformer*


Figure 9-13. Image processing and understanding in the Vision-Transformer
The resulting embeddings can be used in the same way as regular embeddings, for
classification, clustering, search, etc.
Contrastive Language-Image Pre-training
Although ViT is a great image encoder, the arguably most used image encoder is
actually able to encode both text and images. This method is called Contrastive
Language-Image Pre-training (CLIP).2 CLIP uses ViT together with a regular Trans‐
former encoder to embed both images and text. It then uses contrastive learning
using labeled similar and dissimilar pairs of images and text to align the embeddings
of both modalities (Figure 9-14).
As a result, the encoders are updated such that (Figure 9-15):
- Similar pairs result in embeddings with a high similarity.
•
- Dissimilar pairs result in embeddings with a low similarity.
•
2 Radford, Alec et al. 2021. “Learning Transferable Visual Models from Natural Language Supervision,” Pro‐
ceedings of the 38th International Conference on Machine Learning, 139.
|
Chapter 9: Multi-Modal Understanding



![Figure 9-14: The training process of CLIP through contrastive learning](images/fig_09-14_The_training_process_of_CLIP_through_con.png)

*Figure 9-14: The training process of CLIP through contrastive learning*


Figure 9-14. The training process of CLIP through contrastive learning



![Figure 9-15: Data points that are semantically similar are close to each other in semantic](images/fig_09-15_Data_points_that_are_semantically_simila.png)

*Figure 9-15: Data points that are semantically similar are close to each other in semantic*


Figure 9-15. Data points that are semantically similar are close to each other in semantic
space and vice versa
When trained properly, the embeddings of similar text should be close to one another
(high similarity) while the embeddings of dissimilar text should be further apart (low
similarity).
Encoding Modalities
|