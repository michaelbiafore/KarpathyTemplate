---
title: "Audio"
chapter_number: 136
page_start: 360
page_end: 365
part: "Part II. Specialized Agents"
---
# Audio

Contrastive learning is an exceptionally powerful technique. By having the model
learn what is and isn’t similar, it creates accurate semantic representations of the
input. As we’ll explore later in this chapter, CLIP is a very popular image encoder
for MLLMs because the image embeddings have already had “exposure” to the textual
modality.
Audio
To encode audio into embeddings, many different methods exist that make use of the
Transformer architecture, which are in part inspired by the image and text encoders.
wav2vec 2.0
One of the first more successful methods for encoding audio is called wav2vec 2.0.3
This technique samples overlapping (strided) parts of the audio input as a way to
create tokens similar to the text and image examples (Figure 9-16).



![Figure 9-16: The tokenizer in wav2vec 2.0 mimics a regular tokenizer by cutting up the](images/fig_09-16_The_tokenizer_in_wav2vec_20_mimics_a_reg.png)

*Figure 9-16: The tokenizer in wav2vec 2.0 mimics a regular tokenizer by cutting up the*


Figure 9-16. The tokenizer in wav2vec 2.0 mimics a regular tokenizer by cutting up the
input into overlapping pieces, called strided waveforms
Those strided parts are then processed using a convolutional neural network (CNN)
to create features (embeddings). They are finally passed to a regular Transformer
encoder to create contextualized features (Figure 9-17).
3 Baevski, Alexei et al. 2020. “wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representa‐
tions,” Advances in Neural Information Processing Systems, 33: 12449-12460.
|
Chapter 9: Multi-Modal Understanding



![Figure 9-17: Sound processing and understanding in the wav2vec 2.0](images/fig_09-17_Sound_processing_and_understanding_in_th.png)

*Figure 9-17: Sound processing and understanding in the wav2vec 2.0*


Figure 9-17. Sound processing and understanding in the wav2vec 2.0
The training procedure consists of three important steps (Figure 9-18):
Masked language modeling
Randomly masks part of the input for the Transformer to predict
Quantized embeddings
Creates a codebook (vocabulary) of quantized embeddings to reduce the number
of embeddings to represent
Contrastive learning
Updates the model to produce embeddings close to similar inputs and further
away from dissimilar inputs
Encoding Modalities
|



![Figure 9-18: The training process of wav2vec 2.0 using contrastive learning](images/fig_09-18_The_training_process_of_wav2vec_20_using.png)

*Figure 9-18: The training process of wav2vec 2.0 using contrastive learning*


Figure 9-18. The training process of wav2vec 2.0 using contrastive learning
As we’ve seen before (and will see much more of), contrastive learning is an amazing
technique for learning representations and creating embeddings. A popular extension
to this technique is HuBERT, which replaces the quantization step with a clustering
algorithm to create a set of features for the contrastive learning task.4
Whisper
A popular model for encoding audio in LLMs is Whisper. Whisper is used for
automatic speech recognition (ASR) and has an encoder-decoder architecture to
represent the audio (encoder) and to generate a transcription (decoder).5
The architecture is quite straightforward. To represent the audio, it is converted to
a spectrogram, which is an image of sound that shows how the pitch and loudness
of a given sound change over time (Figure 9-19). Features are extracted using convo‐
lutional layers and passed to the encoder-decoder model for contextual processing.
4 Hsu, Wei-Ning et al. 2021. “HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction
of Hidden Units,” IEEE/ACM Transactions on Audio, Speech, and Language Processing, 29: 3451-3460.
5 Radford, Alec et al. 2023. “Robust Speech Recognition via Large-Scale Weak Supervision,” International
Conference on Machine Learning. PMLR.
|
Chapter 9: Multi-Modal Understanding



![Figure 9-19: Sound processing and understanding in the Whisper architecture](images/fig_09-19_Sound_processing_and_understanding_in_th.png)

*Figure 9-19: Sound processing and understanding in the Whisper architecture*


Figure 9-19. Sound processing and understanding in the Whisper architecture
The model is trained on different tasks, such as multilingual speech recognition and
translation. Each task has its own tokens, such as “TRANSCRIBE” for transcription
and “TRANSLATE” for translation tasks, so the decoder understands which task
should be executed. Additional tokens are added for language, if there is speech, time
tokens, etc.
When Whisper is used in MLLMs, typically only the Encoder is used since it serves
to create the audio representations. Instead, the LLM can handle the generative part
(Figure 9-20).
Encoding Modalities
|



![Figure 9-20: How the sound encoder fits into the multi-modal understanding process](images/fig_09-20_How_the_sound_encoder_fits_into_the_mult.png)

*Figure 9-20: How the sound encoder fits into the multi-modal understanding process*


Figure 9-20. How the sound encoder fits into the multi-modal understanding process
Like CLIP, Whisper is a popular audio encoder for MLLMs since the audio embed‐
dings have already had “exposure” to the textual modality.
CLAP
With the performance of CLIP for images, it’s not surprising that other modalities
would follow. Contrastive Language-Audio Pre-training (CLAP) is based on CLIP but
processes audio inputs instead of images.6
The audio waveforms in CLAP (Figure 9-21) are processed in one of two ways, given
a chunk duration d (e.g., 10 seconds):
- If the audio is less than 10 seconds, repeat the input, then pad it with zero values.
•
6 Wu, Yusong et al. 2023. “Large-Scale Contrastive Language-Audio Pretraining with Feature Fusion and
Keyword-to-Caption Augmentation,” ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech
and Signal Processing (ICASSP), IEEE.
|
Chapter 9: Multi-Modal Understanding

- If the audio is more than 10 seconds, the entire input is downsampled to 10
•
seconds. Then, three slices of 10 seconds are randomly sampled.



![Figure 9-21: Sound processing and training process of CLAP](images/fig_09-21_Sound_processing_and_training_process_of.png)

*Figure 9-21: Sound processing and training process of CLAP*


Figure 9-21. Sound processing and training process of CLAP
The authors tested several audio encoders and found that the Hierarchical Token
Semantic-Audio Transformer (HTS-AT) worked best. HTS-AT converts the audio
into a spectrogram and extracts patches from it to generate “tokens,” much like the
image examples we explored.7
The large token/patch embeddings are processed by several hierarchical Transformer
models to downscale the embeddings (Figure 9-22).
7 Chen, Ke et al. 2022. “HTS-AT: A Hierarchical Token-Semantic Audio Transformer for Sound Classification
and Detection,” ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing
(ICASSP), IEEE.
Encoding Modalities
|