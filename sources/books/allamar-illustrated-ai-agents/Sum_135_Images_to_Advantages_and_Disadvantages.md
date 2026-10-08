# Encoding and Connecting Modalities (Chapters 135-143)

## Images

Images become embeddings through the Vision Transformer (ViT), which mimics tokenization by cutting the input into patches, each treated as a "word." Patches are flattened, projected, given positional embeddings, and fed to an ordinary Transformer encoder, so outputs behave like text embeddings.

![Figure 9-13: Image processing and understanding in the Vision-Transformer](images/fig_09-13_Image_processing_and_understanding_in_th.png)

*Figure: The ViT pipeline — nine image patches, a shared linear projection, added positional embeddings plus a [CLS] slot, then a Transformer encoder emitting contextualized patch embeddings.*

The more widely used encoder is CLIP, which pairs a ViT with a text Transformer and applies contrastive learning to labeled similar/dissimilar image-text pairs, updating both encoders so matching pairs land close together in one semantic space. That prior "exposure" to text is why CLIP is the default image encoder in multi-modal LLMs (MLLMs).

## Audio

Audio follows the same tokenize-then-Transformer recipe. wav2vec 2.0 samples overlapping strided waveforms, extracts CNN features, and contextualizes them in a Transformer encoder, trained via masked language modeling, quantized codebook embeddings, and contrastive learning (HuBERT swaps quantization for clustering). Whisper instead converts sound to a spectrogram — an image of pitch and loudness over time — and uses an encoder-decoder for ASR, with task tokens (TRANSCRIBE, TRANSLATE, language, timestamps). MLLMs reuse only its encoder. CLAP is CLIP for audio: it pads or downsamples clips to a fixed duration and favors HTS-AT, which patches a spectrogram and downscales hierarchically.

![Figure 9-19: Sound processing and understanding in the Whisper architecture](images/fig_09-19_Sound_processing_and_understanding_in_th.png)

*Figure: Whisper's encoder takes a log-mel spectrogram through two 1D convolutions and self-attention blocks, while the decoder cross-attends to it and emits transcription tokens after language/task/timestamp prefix tokens.*

## Video

Video adds a temporal dimension (plus optional audio and subtitles); naively averaging per-frame CLIP embeddings destroys it. ViViT handles it with uniform frame sampling or tubelet embeddings — 3D patches spanning consecutive frames — fed to separate spatial and temporal Transformers. TimeSformer collapses this into one model via divided space-time attention.

![Figure 9-29: The architecture of an encoder block in the TimeSformer](images/fig_09-29_The_architecture_of_an_encoder_block_in.png)

*Figure: A TimeSformer block applies time attention across tubelets (motion) then space attention within frames (object relationships), each with layer norm and residuals before the FFNN.*

Alternatively, "just" CLIP: skip the temporal encoder and pass sampled frame embeddings to the LLM as a sequence — decoders already model time in text — letting the connector add spatial then temporal position (as VideoMamba does).

## Many-Modality

Separate encoders produce embeddings of different dimensions and distributions that cannot be compared. ImageBind fixes this by making images the binding modality: every training pair has a visual side (image-text, image-depth, image-thermal, video-IMU, video-audio), with a linear projection aligning each pair before the contrastive loss.

![Figure 9-38: How contrastive learning is used to train ImageBind, connecting all modali‐](images/fig_09-38_How_contrastive_learning_is_used_to_trai.png)

*Figure: Image/audio and video/text pairs pass through modality-specific encoders, then per-modality linear projections to a shared fixed dimension, scored by contrastive loss.*

Strikingly, unseen pairs such as (audio, text) emerge aligned anyway — evidence of how strong the image "binding" factor is.

## Connecting Modalities

Encoder outputs differ from what the LLM expects in size, dimension, embedding space, positional encoding, and tokenization. A trained connector bridges the gap.

![Figure 9-41: The three types of connectors: the projection, query, and fusion connectors](images/fig_09-41_The_three_types_of_connectors_the_projec.png)

*Figure: The comparison — an MLP projection, a Q-Former driven by learnable queries, and fusion feeding image K/V into multi-head attention inside the LLM.*

## Projection-Based Connector

A single linear layer (up- or down-projecting) maps non-text embeddings to token embeddings concatenated with the text tokens; the LLM treats them identically.

![Figure 9-43: A projection connector maps each output embedding of the image encoder](images/fig_09-43_A_projection_connector_maps_each_output.png)

*Figure: ViT/CLIP patch embeddings pass through an MLP to match the text embedding layer's output, then both streams enter the LLM side by side.*

LLaVA trained this in two stages — projection alone (ViT and Vicuna frozen), then projection plus LLM — and the pattern persists in Qwen2.5-VL, Phi-4-multimodal, and Janus.

## Query-Based Connector

The Q-Former (from BLIP-2) compresses input into a fixed number of learnable query embeddings, keeping only the most relevant visual detail.

![Figure 9-45: The Q-Former, which maps the input to a fixed set of embeddings, com‐](images/fig_09-45_The_Q-Former_which_maps_the_input_to_a_f.png)

*Figure: Variable-length ViT/CLIP embeddings enter the Q-Former and leave as a fixed set of learned queries, then an MLP converts them for the LLM alongside the text prompt.*

Stage 1 trains the queries on image-text contrastive learning, image-grounded text generation, and image-text matching; stage 2 attaches an MLP to a frozen LLM. Qwen-VL used this.

## Fusion-Based Connector

Flamingo changes the LLM itself, inserting trainable gated cross-attention layers between frozen LM blocks; a Q-Former-like perceiver resampler first compresses vision features to a fixed size.

![Figure 9-48: The Flamingo fusion-based connector](images/fig_09-48_The_Flamingo_fusion-based_connector.png)

*Figure: Frozen ViT/CLIP and Chinchilla blocks (snowflakes) surround the trainable perceiver resampler and gated cross-attention (flames) that inject image features at every layer.*

The gate multiplies layer output by tanh(α), α initialized to 0, so the model starts identical to the original LLM and learns to open the gate — a stability trick.

## Advantages and Disadvantages

Three axes decide: performance, computational efficiency, scalability. Projection is simple, lightweight, and cheap but limited in expressive power, and it floods the context window since input is never compressed. Query-based keeps input length constant regardless of resolution and is more expressive, at the cost of complex training, added latency, and possibly skipped detail. Fusion performs best — multi-modal features are seen at every layer, not just as a prefix — but requires architectural surgery and extensive fine-tuning.
