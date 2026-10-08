---
title: "What Is an AI Agent?"
chapter_number: 15
page_start: 24
page_end: 25
part: "Part I. The Anatomy of an AI Agent"
---
# What Is an AI Agent?

the upcoming chapters, where each subsequent chapter will uncover an important
component of an AI agent. You can expect an intuitive, but in-depth journey, of what
makes AI agents so special.
What Is an AI Agent?
The definition of an AI agent is ever-changing as the field progresses and as these
entities grow in complexity. Fortunately, as with most technologies, the fundamentals
of AI agents are static and a great way to build up to more state-of-the-art techniques.
As such, we consider the following definition of AI agents meaningful through both
the fundamentals and new advances in this field:
An agent is anything that can be viewed as perceiving its environment through sensors
and acting upon that environment through actuators.
—Russell & Norvig, Artificial Intelligence: A Modern Approach1
This definition boils down agents to entities that perceive and interact with their
environment. It’s broad enough to consider entities other than LLMs, but at the same
time, it gives us something structured to work with.
We can deconstruct this definition into the following components that lie at the heart
of agents:
Environment
The world the agent interacts with
Sensors
Components of the agent used to observe the environment
Actuators
Tools the agent uses to interact with the environment
Agent program
The “brain” or rules the agent uses to decide how to go from observations to
actions
The interaction of all these components is shown in Figure 1-1.
1 Russell, Stuart and Peter Norvig, Artificial Intelligence: A Modern Approach, 4th ed. (Pearson, 2020).
|
Chapter 1: Introduction



![Figure 1-1: An agent perceives its environment through sensors and acts on it via tools or](images/fig_01-01_An_agent_perceives_its_environment_throu.png)

*Figure 1-1: An agent perceives its environment through sensors and acts on it via tools or*


Figure 1-1. An agent perceives its environment through sensors and acts on it via tools or
actuators
Let’s clarify this terminology by relating it to LLMs.
In practice, the agent program or brain of an LLM-backed agent is a “reasoning” LLM,
a model that is capable of complex thinking. Through additional modules (memory,
tools, and planning), this LLM is capable of interacting with its environment. Here,
the actuators are the tools of the LLM. Some LLMs can interpret more than text, such
as images or sound, and can be considered as the sensors in this system. The last piece
missing from this system is the user, who can be part of the environment. Users often
initiate the interaction by stating a request for the agent to fulfill.
Together, these aspects are what we believe to be truly fundamental to AI agents as we
see them in practice. Figure 1-2 illustrates how all these components are connected.
More importantly, this figure does not just elucidate the principles of agents but also
tells a story: a story of what agents truly are, how they’re created, and how they
behave. The figure serves as the foundation of this book and will be used throughout
to build up the agent.



![Figure 1-2: Agents operate in regular contact with a user and environment, and use](images/fig_01-02_Agents_operate_in_regular_contact_with_a.png)

*Figure 1-2: Agents operate in regular contact with a user and environment, and use*


Figure 1-2. Agents operate in regular contact with a user and environment, and use
reasoning models, memory, tools, and planning to decide their actions
What Is an AI Agent?
|