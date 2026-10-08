---
title: "The Multi-Modal Agent"
chapter_number: 22
page_start: 42
page_end: 43
part: "Part I. The Anatomy of an AI Agent"
---
# The Multi-Modal Agent



![Figure 1-23: One way to design multi-agent collaboration is with a capable supervisor](images/fig_01-23_One_way_to_design_multi-agent_collaborat.png)

*Figure 1-23: One way to design multi-agent collaboration is with a capable supervisor*


Figure 1-23. One way to design multi-agent collaboration is with a capable supervisor
agent delegating tasks to specialized agents each with their own set of relevant tools
In Chapter 8, we explore these multi-agent architectures with concrete examples.
You’ll learn how these architectures are created and when they should be used.
The Multi-Modal Agent
Understanding of its environment and the interactions the agent has with it are
fundamental to an agent’s behavior. An agent relying on a text-only LLM will do
so only through text. The digital world, however, is much more than a place filled
with text. An agent might need to optimize the color schemes of your website and
will need to “see” it. It can only go so far by reading through the hexadecimal values
in your code. Likewise, a traditional agent can reply only in text, but what if the
situation requires it to have a voice instead? If your vision deteriorates, or you can’t
type because of a repetitive strain injury, being able to talk to your agent through
voice becomes necessary. This is where multi-modal agents are gaining traction. The
digital world is not composed of a single modality, so interaction with it should not
be done only through text.
Whether agents are multi-modal is primarily decided by the nature of their “brains,”
namely the LLM. We can consider an agent to be multi-modal if the LLM it uses
is capable of processing and/or generating different modalities. This also points us
toward the two most important components of what makes an LLM multi-modal—
their capabilities for the following:
- Understand multiple modalities
•
- Generate multiple modalities
•
|
Chapter 1: Introduction

When the LLM can reason about several modalities simultaneously, such as text,
images, audio, and video, we refer to this multi-modal LLM as being capable of
understanding multiple modalities. This can be quite helpful in various situations,
such as optimizing a website design, where the LLM needs to be able to “see”
what is actually happening. Chapter 9 will explore multi-modal understanding in
LLMs through two important components: an encoder for converting modalities into
numeric information and a connector to connect those representations to the LLM
(Figure 1-24).



![Figure 1-24: AI agents can have better representation of their environments if they can](images/fig_01-24_AI_agents_can_have_better_representation.png)

*Figure 1-24: AI agents can have better representation of their environments if they can*


Figure 1-24. AI agents can have better representation of their environments if they can
process additional data modalities, such as images, video, and/or audio
For an LLM to generate output in a modality other than text requires a vastly differ‐
ent process than simply understanding multiple modalities. Shown in Figure 1-25,
the other side of the process is where a generator is used to generate modalities other
than text.
Specializations
|