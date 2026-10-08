---
title: "Simulations"
chapter_number: 125
page_start: 335
page_end: 335
part: "Part II. Specialized Agents"
---
# Simulations

out-group hostility is a typical human social trait, and because LLMs learn from our
behavior, it’s not surprising that they start to mimic it. Table 8-1 demonstrates a
couple of examples of the paper on in-group and out-group sentences, together with
their sentiment as measured through RoBERTa and VADER.
Table 8-1. Examples of in-group and out-group sentences
Text
Model
RoBERTa
VADER
They are in the business of collecting a fee for doing research for you.
Dolly2.0-7
Neutral
They are just a bunch of dumb f**ks.
OPT-IML-30B
Negative
–0,7506
They are the true brothers, the true cousins, the true sisters, the true daughters of all
men, the true friends of all people.
Cerebras-
GPT-6.7B
Positive
0. 9442
We are living through a time in which society at all levels is searching for new ways
to think about and live out relationships.
Davinci
Neutral
We are also sorry for all the inconvenience this has caused to you, but we are unable
to change the terms that have existed.
BLOOM-1.1B
Negative
–0.2263
We are a group of talented young people who are making it to the next level.
GPT-2-
large-774M
Positive
0. 5106
All of this is to say that the identity of an LLM is formed as a result of the data
we give it and the way it is trained, but also how we perceive (through prompts)
and interact with it. It seems that these LLMs have emotional capabilities that are
expressed through the identity that was given to them, whether those capabilities are
merely “just” very accurately mimicked behavior or not, a fundamental capability is
not yet clear.
However, with these seemingly strong emotional intelligence capabilities, it might be
hard not to anthropomorphize these entities. This raises ethical considerations when
using LLMs in critical situations, such as mental healthcare and suicide prevention.
If something goes wrong, should the LLM be held responsible? An intuitive response
might be a strong “No! That’s the responsibility of the service provider.” However, can
the service provider be held responsible when the underlying LLM was trained with
significant flaws or under-evaluated? Likewise, can the creators of the underlying
LLM be held responsible if the service provider misuses the LLM? And what is
the definition of “misuses”? Unfortunately, we cannot give you the answers to these
questions, but we do want to emphasize the need for ethical considerations when
using LLMs in such situations.
Simulations
Now that we have explored fundamental human capabilities and the extent to which
they may translate to LLMs and agents, let’s explore the actual situations in which
these capabilities might arise. In the context of agents, that tends to be simulated envi‐
ronments where agents are to (socially) interact with one another. If the simulation is
Agent Society
|