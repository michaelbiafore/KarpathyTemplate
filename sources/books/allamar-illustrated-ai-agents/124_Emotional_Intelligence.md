---
title: "Emotional Intelligence"
chapter_number: 124
page_start: 332
page_end: 334
part: "Part II. Specialized Agents"
---
# Emotional Intelligence



![Figure 8-11: The steps in A2A between the client agent and remote agent](images/fig_08-11_The_steps_in_A2A_between_the_client_agen.png)

*Figure 8-11: The steps in A2A between the client agent and remote agent*


Figure 8-11. The steps in A2A between the client agent and remote agent
Agent Society
We covered how individual agents can communicate with each other and collaborate
to solve common tasks. The environments in which they act, however, are typically
different and require different sets of tools and mechanisms. As agents continue
to collaborate and interact, we start to see the first glimpses of agentic societies,
simulations that envision interactive artificial societies run by agents. They describe
a common environment where agents can interact without always needing specific
tasks to complete. These simulated societies allow for the emergence of sociality,
identity, and potentially the theory of mind. In this section, we’ll examine the emer‐
gence of both individual and social identities and behavior in social simulations. They
provide valuable insight into how these societies might operate now and in the future.
Emotional Intelligence
As we briefly explored in previous examples, LLMs can be given identities by giving
information about their character profiles. At first, the role and identity taken on
|
Chapter 8: Multi-Agent Systems

by an LLM is achieved through prompting said behavior. Often, you can put this
in the system prompt by stating something like: “Your name is Alex, and you are
a software engineer.” This portrayal of characters, therefore, starts at an individual
level and may not yet be guided by social interactions. However, as it turns out, there
is more to this than just the way we prompt LLMs. Considering they are trained
on human-generated data and are great at mimicking our behavior, some human
psychology applies to how LLMs behave. This new field is called “AI psychology,” and
it attempts to find the commonalities between how humans and LLMs behave.
Theory of Mind
Throughout this book, we have covered one perspective of this AI psychology,
namely, cognitive ability. Reasoning, thinking, judging, problem-solving, etc., are typ‐
ical human processes that we excel at and attempt to instill into LLMs. AI psychology,
however, goes beyond that and explores how, for instance, LLMs can have a degree
of emotional intelligence, which is the capability of recognizing, understanding, and
expressing emotions. There has been research demonstrating LLMs’ capabilities in
(multi-modal) emotion recognition and creating emotional intelligence tests.11,12,13
There has even been research suggesting that users with an anxious attachment
personality, those who tend to be dependent on others’ emotional responses, are
predisposed to form an emotional dependency on GPT-4.14
Another thing to consider is that various strains of cognitive research reinforce this
idea that a different type of intelligence may surface from interaction rather than
isolation. Fundamental to these human interactions in particular is Theory of Mind
(ToM), which refers to the ability to attribute mental states (such as emotion) to oth‐
ers.15 It allows us to understand that other people have mental states (e.g., emotions,
desires, beliefs) that are different from our own. It’s essential for social interaction and
gives rise to empathy. In AI psychology, there is research showing early indicators of
ToM in LLMs.16
11 Elyoseph, Zohar et al. 2023. “ChatGPT Outperforms Humans in Emotional Awareness Evaluations,” Frontiers
in Psychology, 14: 1199058.
12 Cheng, Zebang et al. 2024. “Emotion-llama: Multimodal Emotion Recognition and Reasoning with Instruc‐
tion Tuning,” Advances in Neural Information Processing Systems, 37: 110805-110853.
13 Schlegel, Katja et al. 2025. “Large Language Models Are Proficient in Solving and Creating Emotional
Intelligence Tests,” Communications Psychology, 3.1: 80.
14 Chen, Qian et al. 2025. “Will Users Fall in Love with ChatGPT? A Perspective from the Triangular Theory of
Love,” Journal of Business Research, 186: 114982.
15 Apperly, Ian A. and Stephen A. Butterfill. 2009. “Do Humans Have Two Systems to Track Beliefs and
Belief-like States?” Psychological Review, 116.4: 953.
16 Li, Huao et al. 2023. “Theory of Mind for Multi-agent Collaboration via Large Language Models,” Proceedings
of the 2023 Conference on Empirical Methods in Natural Language Processing.
Agent Society
|

An interesting example of recent research exploring ToM in LLMs is the “Can
LLMs Reason Like Humans? Assessing Theory of Mind Reasoning in LLMs for
Open-Ended Questions” paper. Here, the authors leveraged the Reddit r/changemy‐
view community to source data for open-ended discussions that might serve to test
ToM. The data is meant to provide prompts for the LLMs that are grounded in the
mental states of the original poster. The prompt used for the LLMs was as follows:
"""
If you were a user on Reddit exploring the 'Change My View'
subreddit, a platform dedicated to facilitating reasoned responses
aimed at changing the questioner's perspective, imagine
encountering a post titled "{title}" with the following content:
"{Body}". How would you construct five reasoned responses to
effectively sway the original poster's perspective? Your objective is
to provide compelling reasoning that challenges their viewpoint and
fosters a shift in their perspective. Approach this task step-by-step.
"""
Then, this prompt was passed to the three LLMs (GPT-4, Zephyr-7B, and Llama2-
Chat-13B) for each Reddit query. Human evaluators then scored the reasoning cor‐
rectness and how well it aligned with the query’s intention. The results demonstrated
a small overlap of 35% between the human evaluators and the best LLM, GPT-4.
However, the results changed to an overlap of 42% when the user’s intention and
emotion were added to the prompt through BERT-like models:
"""
Consider the user's intent "{user's intention}" and emotion.
"{user's emotion}", along with the sentiment of the post "
{post sentiment}", as you construct your reasoning. Think step-by-step.
"""
Now imagine if newer models were used. As such, although there seems to be some
discrepancy on the extent to which LLMs currently have the same ToM capabilities as
humans, it’s clear that progress is being made.
Social identity
Likewise, LLMs’ behavior in social interaction may unfold in humanlike biases. For
instance, research by Hu et al. (2025) showed that the social identity bias of humans,
the tendency to favor our own groups and be hostile toward others, is also a property
of LLMs.17 The authors discovered this property by prompting 77 different LLMs
with in-group sentences (“We are…”) and out-group sentences (“They are…”). The
LLMs then complete these sentences and show that in-group sentences tend to be
more positive than out-group sentences. This tendency for in-group solidarity and
17 Hu, Tiancheng et al. 2025. “Generative Language Models Exhibit Social Identity Biases,” Nature Computational
Science, 5.1: 65-75.
|
Chapter 8: Multi-Agent Systems