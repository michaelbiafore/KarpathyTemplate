---
title: "Video"
chapter_number: 137
page_start: 366
page_end: 375
part: "Part II. Specialized Agents"
---
# Video



![Figure 9-22: How sound is processed using HTS-AT](images/fig_09-22_How_sound_is_processed_using_HTS-AT.png)

*Figure 9-22: How sound is processed using HTS-AT*


Figure 9-22. How sound is processed using HTS-AT
Using the text and audio encoders, CLAP then uses contrastive learning based on
audio/text pairs. These are often captions or descriptions of audio samples.
Video
Encoding videos has a significant overlap with encoding images, but with several
(potential) differences. Videos have an additional temporal dimension that needs to
be encoded, namely as a sequence of images. You can also consider adding the audio
and/or subtitles to the encoding process, as those are tightly related (Figure 9-23).
|
Chapter 9: Multi-Modal Understanding



![Figure 9-23: Videos have at least three dimensions to process, depending on whether you](images/fig_09-23_Videos_have_at_least_three_dimensions_to.png)

*Figure 9-23: Videos have at least three dimensions to process, depending on whether you*


Figure 9-23. Videos have at least three dimensions to process, depending on whether you
include other aspects of videos, such as their audio and subtitles
In other words, the main challenge in encoding the video modality is how to model
that temporal dimension. How do we keep track of this sequence of images?
The most basic version is to use a ViT or CLIP-like model, sample a number of
frames, embed, and finally average them (Figure 9-24).



![Figure 9-24: An example of how videos can be processed as sequences of images](images/fig_09-24_An_example_of_how_videos_can_be_processe.png)

*Figure 9-24: An example of how videos can be processed as sequences of images*


Figure 9-24. An example of how videos can be processed as sequences of images
However, this averages away the temporal dimension and prevents the LLM from
understanding how the video started and ended.
Encoding Modalities
|

Are there more sophisticated ways that we can use these ViT/CLIP embeddings? Let’s
find out!
ViViT
An early example of adapting ViT-like models for video is called the Video Vision
Transformer (ViViT).8 This method uses different combinations of Transformer
models for both the spatial information (the image itself) and the temporal informa‐
tion (changes between subsequent images).
To start, the authors consider extracting tokens from videos in two ways. The first is
uniform frame sampling, where frames are sampled and passed through ViT to create
tokens for each patch in each sampled frame (Figure 9-25).



![Figure 9-25: The processing of individual frames in the Video Vision Transformer](images/fig_09-25_The_processing_of_individual_frames_in_t.png)

*Figure 9-25: The processing of individual frames in the Video Vision Transformer*


Figure 9-25. The processing of individual frames in the Video Vision Transformer
(ViViT)
The second method is to create tubelet embeddings. A tubelet is a block of pixels
taken from consecutive frames, forming a 3D patch that captures a part of the image
as well as its changes over time. Instead of passing a single image to a ViT model,
you would now pass non-overlapping tubelets that cover multiple images, producing
tubelet embeddings. In other words, it would span both the spatial and temporal
nature of videos (Figure 9-26).
8 Arnab, Anurag et al. 2021. “ViViT: A Video Vision Transformer,” Proceedings of the IEEE/CVF International
Conference on Computer Vision.
|
Chapter 9: Multi-Modal Understanding



![Figure 9-26: The processing of tubelet embeddings in the Video Vision Transformer](images/fig_09-26_The_processing_of_tubelet_embeddings_in.png)

*Figure 9-26: The processing of tubelet embeddings in the Video Vision Transformer*


Figure 9-26. The processing of tubelet embeddings in the Video Vision Transformer
(ViViT)
The authors of the ViViT paper experimented with several models, but the most
prominent one was to pass either embedding type to a set of Transformer encoders
that primarily process spatial information (Figure 9-27).



![Figure 9-27: An example of how different types of Transformer encoders might be used](images/fig_09-27_An_example_of_how_different_types_of_Tra.png)

*Figure 9-27: An example of how different types of Transformer encoders might be used*


Figure 9-27. An example of how different types of Transformer encoders might be used
to process spatial and temporal information in the Video Vision Transformer (ViViT)
Encoding Modalities
|

It’s interesting to see how every modality attempts to represent the input as some sort
of token.
TimeSformer
The idea of separating temporal and spatial dimensions of video encoding tasks
was also explored in a single Transformer model, namely TimeSformer.9 Like ViViT,
frames are sampled and split up into patches. These patches are not processed at first
like tubelets but instead flattened and passed directly to a Transformer (Figure 9-28).



![Figure 9-28: The processing of frames in a video in the TimeSformer](images/fig_09-28_The_processing_of_frames_in_a_video_in_t.png)

*Figure 9-28: The processing of frames in a video in the TimeSformer*


Figure 9-28. The processing of frames in a video in the TimeSformer
However, instead of applying different Transformers for different dimensions (tempo‐
ral versus spatial), TimeSformer applies attention mechanisms that each focus on a
different aspect, namely time attention and space attention (Figure 9-29). Both forms
of attention work the same as self-attention (which we covered in Chapter 2) but
operate on different groupings of image patches. Time attention creates tubelets to
operate along the time dimension as a way to capture motion patterns. In contrast,
space attention operates on patches created within individual frames to focus on
spatial structures such as object relationships.
9 Bertasius, Gedas et al. 2021. “Is Space-Time Attention All You Need for Video Understanding?” ICML, 2:(3).
|
Chapter 9: Multi-Modal Understanding



![Figure 9-29: The architecture of an encoder block in the TimeSformer](images/fig_09-29_The_architecture_of_an_encoder_block_in.png)

*Figure 9-29: The architecture of an encoder block in the TimeSformer*


Figure 9-29. The architecture of an encoder block in the TimeSformer
These attention mechanisms are called divided space-time attention and allow for
better representations than if only space attention were used or ViT (Figure 9-30).
Note how all these techniques have very similar underlying principles of sampling
frames, creating patch tokens, embedding them, and finally using them as token
embeddings in some variant of a Transformer encoder. Popular examples include
VideoBERT, Frozen in Time, and VideoMae. Covering them all, however, would
make this guide twice as long. Let’s instead explore a more straightforward technique,
“just” CLIP.
Encoding Modalities
|



![Figure 9-30: Annotated figure in the “Is Space-Time Attention All You Need for Video](images/fig_09-30_Annotated_figure_in_the_Is_Space-Time_At.png)

*Figure 9-30: Annotated figure in the “Is Space-Time Attention All You Need for Video*


Figure 9-30. Annotated figure in the “Is Space-Time Attention All You Need for Video
Understanding?” paper
“Just” CLIP
In the previous examples, we saw different ways of adopting the ViT/CLIP embed‐
dings to allow for additional processing and representing the temporal dimension.
The underlying idea is that these will be passed to an LLM through a connector
(which we’ll discuss in a bit). See Figure 9-31.



![Figure 9-31: How videos might be processed in the multi-modal understanding pipeline](images/fig_09-31_How_videos_might_be_processed_in_the_mul.png)

*Figure 9-31: How videos might be processed in the multi-modal understanding pipeline*


Figure 9-31. How videos might be processed in the multi-modal understanding pipeline
|
Chapter 9: Multi-Modal Understanding

However, there is a bit of redundancy here. Note that there are now two Transformer
encoders before the embeddings are passed to the LLM. Instead, we could also skip
the second and have the LLM figure out the temporal dimensions by having the
connector do a bit more processing (Figure 9-32).



![Figure 9-32: How videos might be processed when skipping explicit temporal encoders in](images/fig_09-32_How_videos_might_be_processed_when_skipp.png)

*Figure 9-32: How videos might be processed when skipping explicit temporal encoders in*


Figure 9-32. How videos might be processed when skipping explicit temporal encoders in
the multi-modal understanding pipeline
The underlying idea here is that since decoder LLMs are already good at processing
temporal dimensions in text, the same could be done for videos if each frame (or
patch) is considered as a sequence of tokens.
As such, both text and video can be seen as having similar time-based sequential
natures (Figure 9-33).



![Figure 9-33: When broken down to sequences, video can be seen as a sequence of frames](images/fig_09-33_When_broken_down_to_sequences_video_can.png)

*Figure 9-33: When broken down to sequences, video can be seen as a sequence of frames*


Figure 9-33. When broken down to sequences, video can be seen as a sequence of frames
(video tokens,) much like text can be seen as a sequence of subwords (tokens)
Encoding Modalities
|

As a result, we can pass sample frames from the video, create embeddings for each
image, and then pass them as a sequence (like with text) to the LLM. The connector
can then either add temporal data or simply convert the image embeddings to the
type of embeddings the LLM expects (Figure 9-34).



![Figure 9-34: Videos can be processed by an LLM as a sequence of image embeddings,](images/fig_09-34_Videos_can_be_processed_by_an_LLM_as_a_s.png)

*Figure 9-34: Videos can be processed by an LLM as a sequence of image embeddings,*


Figure 9-34. Videos can be processed by an LLM as a sequence of image embeddings,
much like text is processed as a sequence of text embeddings
These video “tokens” can either be formed as the entire image or as individual image
tokens. A great example is the VideoMamba paper that uses positional embeddings to
“enhance” the image embeddings (Figure 9-35).10
10 Li, Kunchang et al. 2024. “VideoMamba: State Space Model for Efficient Video Understanding,” European
Conference on Computer Vision.
|
Chapter 9: Multi-Modal Understanding

It first adds spatial information to the embeddings (to which part of the frame does an
embedding belong?) and then temporal information (in which order are the frames?).



![Figure 9-35: Positional embeddings used in VideoMamba allow for adding spatial and](images/fig_09-35_Positional_embeddings_used_in_VideoMamba.png)

*Figure 9-35: Positional embeddings used in VideoMamba allow for adding spatial and*


Figure 9-35. Positional embeddings used in VideoMamba allow for adding spatial and
temporal information to image embeddings
For an overview of techniques that adopt video encoders, we recommend checking
out the “Video Understanding with Large Language Models: A Survey” paper.
Encoding Modalities
|