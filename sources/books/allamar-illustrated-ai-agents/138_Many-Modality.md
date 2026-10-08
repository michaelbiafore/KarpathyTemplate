---
title: "Many-Modality"
chapter_number: 138
page_start: 376
page_end: 378
part: "Part II. Specialized Agents"
---
# Many-Modality

Many-Modality
In previous examples, modalities are typically encoded in isolation or in pairs with
other modalities. A disadvantage of this approach is that we need different models
for different modalities. The generated embeddings by different models cannot be
compared to one another (Figure 9-36).



![Figure 9-36: Different embeddings will generate different distributions of values and](images/fig_09-36_Different_embeddings_will_generate_diffe.png)

*Figure 9-36: Different embeddings will generate different distributions of values and*


Figure 9-36. Different embeddings will generate different distributions of values and
often have different dimensions
A popular technique for finding a singular embedding space that can hold many
different modalities is called ImageBind.11 This combines contrastive learning with an
interesting idea, namely that a single image can bind different modalities. An image
of a rainy day at the beach can remind us of the sound of waves, the cold touch of mist
on skin, and even evoke a quiet mood.
11 Girdhar, Rohit et al. 2023. “Imagebind: One Embedding Space to Bind Them All,” Proceedings of the
IEEE/CVF Conference on Computer Vision and Pattern Recognition.
|
Chapter 9: Multi-Modal Understanding

As we have seen before, many modalities are actually processed through the lens
of images. Video and audio encoders, for instance, use image encoders as the main
encoder for processing these modalities (Figure 9-37).



![Figure 9-37: Audio and video can be processed as if they were images, which results in](images/fig_09-37_Audio_and_video_can_be_processed_as_if_t.png)

*Figure 9-37: Audio and video can be processed as if they were images, which results in*


Figure 9-37. Audio and video can be processed as if they were images, which results in
the same type of embeddings generated and can therefore be compared
The primary objective of the ImageBind project is to utilize images as the basis for
contrastive learning. As explored before, contrastive learning typically trains on pairs
of data. With ImageBind, one of those modalities will always be related to the visual
modality (images or video).
Encoding Modalities
|

For each pair of modalities, a linear projection is first applied to the original embed‐
dings to make sure that the embeddings of different pairs of modalities are aligned
(Figure 9-38).



![Figure 9-38: How contrastive learning is used to train ImageBind, connecting all modali‐](images/fig_09-38_How_contrastive_learning_is_used_to_trai.png)

*Figure 9-38: How contrastive learning is used to train ImageBind, connecting all modali‐*


Figure 9-38. How contrastive learning is used to train ImageBind, connecting all modali‐
ties together through images
During training, the following pairs were trained:
- (Image, text)
•
- (Image, depth sensor data)
•
- (Image, thermal data)
•
- (Video, inertial measurement unit [IMU; e.g., accelerometer data])
•
- (Video, audio)
•
Interestingly, although there were many unseen pairs of modalities during training,
such as (audio, text), their embeddings were aligned in the embedding space (see
Figure 9-39).
|
Chapter 9: Multi-Modal Understanding