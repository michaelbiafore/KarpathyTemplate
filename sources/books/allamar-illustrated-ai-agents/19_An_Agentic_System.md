---
title: "An Agentic System"
chapter_number: 19
page_start: 36
page_end: 39
part: "Part I. The Anatomy of an AI Agent"
---
# An Agentic System



![Figure 1-18: Planning and reflection to update plans are key capabilities for agents](images/fig_01-18_Planning_and_reflection_to_update_plans.png)

*Figure 1-18: Planning and reflection to update plans are key capabilities for agents*


Figure 1-18. Planning and reflection to update plans are key capabilities for agents
tackling more difficult problems
An Agentic System
With all these components, a reasoning LLM augmented with memory, tools, and
planning, we arrive at the next stage of the agent: the way it behaves inside a system.
This covers common use cases, degree of autonomy, ethical considerations, and how
these agents and systems can be evaluated.
Autonomy
The AI agent, as we have defined it thus far, has a fair bit of freedom. It can
choose between tools, decide to update the initial plan, add additional steps, or stop
because it has reached the appropriate response. All of this advanced behavior is the
autonomy that is given to the agent. In practice, not all agents will have complete
autonomy; guardrails are often necessary so that the model does not take potentially
destructive actions (such as deleting important files).
Depending on the AI agent and the system in which it’s integrated, agents can have
varying degrees of autonomy. As shown in Figure 1-19, this autonomy can be partial,
where the model can execute only a single step but has the freedom to choose from
tools, or it can be complete freedom without any guardrails.
Depending on who you ask, a system is more “agentic” the more the LLM has
full control over its actions. However, we believe that as long as the agent exhibits
goal-directed behavior and makes decisions, we can call it an agent. Autonomy exists
on a spectrum, and partial autonomy in orchestrated workflows can still qualify as
agency if the agent acts with some degree of independence. Across all chapters, we’ll
cover both autonomous systems as well as orchestrated workflows.
|
Chapter 1: Introduction



![Figure 1-19: AI agents have more autonomy or agency than a single LLM generation or](images/fig_01-19_AI_agents_have_more_autonomy_or_agency_t.png)

*Figure 1-19: AI agents have more autonomy or agency than a single LLM generation or*


Figure 1-19. AI agents have more autonomy or agency than a single LLM generation or
a fixed pipeline
Agentic applications: What makes them so useful?
Agents’ abilities for autonomous behavior make them especially useful for open-
ended problems where the exact steps required are not known beforehand. The LLM
can reason on how to approach a problem and the number of turns to complete
it. This autonomy and self-driving behavior thrives in environments where the goal
might be clear, but the path to reach it is not.
As such, agents are often used for the following:
Coding
Coding assistants (such as Antigravity, Claude Code, and Codex) are arguably
the most common use case at the time of writing, with companies like Cursor
being valued at tens of billions of dollars. With so much knowledge about code,
agents are capable of writing it themselves and going through the steps of writing
new code but also validating it. This is a use case where the agent truly shines
because the goal is quite clear (a specific feature) and often with pre-defined
requirements (language, frameworks, etc.) to work toward with some degree of
freedom. Problems in the code domain also often benefit from the ability to be
automatically verified, which is a useful property at both training and inference
time.
What Is an AI Agent?
|

Deep research
This is a field where agents are used to perform in-depth analyses on various
topics without much intervention by the user. You can ask an agent to research a
given topic, and it will, autonomously, search for everything related to that topic
on sources such as arXiv, PubMed, and Google Scholar. These agents are not
without flaws, but they’re a great starting point whenever you want to dive into a
new topic, and they’re gaining popularity across platforms.
Automation
Although you wouldn’t use an agent to diagnose patients or handle claims auto‐
matically without any human interaction, there are many useful places where an
agent would have a large impact if designed thoughtfully. Standardization and
automation of processes are great examples. For instance, hospitals across the
world differ in how data is stored (both structured and unstructured). Agents are
capable of searching through various data sources to structure the wide array of
patient data, allowing for easier research in healthcare.
Responsible agent development and usage
As we explore the incredible capabilities of LLMs, it’s important to keep their societal
and ethical implications in mind. This is especially true for agents, which can have a
degree of autonomy that might directly impact the digital or physical world. While
many think the future of agents is fully autonomous systems, others state that fully
autonomous agents should not be developed at all due to the risk of giving away
control.3 The field is currently somewhere in the middle. Agents can be amazing
entities and help optimize many processes, such as coding agents. However, having an
agent diagnose patients without any human intervention is, with the current state of
technology, harmful behavior. As with most things, it’s all about the context in which
agents are used.4
As such, here are key points to consider:
Human in the loop
As agents become more autonomous, there is a greater need for humans in the
loop to authorize, check, and audit the decisions that agents make. This can take
many forms, as will be discussed throughout the book, but typically involves a
human checking either the output or intermediate steps before continuing.
Guardrails
It’s essential to be careful with the level of autonomy we grant agents. Not only
can full autonomy be overkill for the task at hand, but it can often be harmful.
3 Mitchell, Margaret et al. 2025. “Fully Autonomous AI Agents Should Not Be Developed.” arXiv, 2502.02649.
4 Gabriel, Iason et al. 2024. “The Ethics of Advanced AI Assistants.” arXiv,2404.16244.
|
Chapter 1: Introduction

A system with many guardrails is often more effective, as it allows steering the
agent toward expected behaviors and away from undesired ones.
Misinformation
AI agents are still LLMs, which are prone to confidently generating incorrect
information, called hallucinations. Although LLMs are becoming much more
capable, additional checks and balances are needed in systems where correct
information is critical.
Evaluating agents
Responsible agent development brings us to an important component of building any
agent: evaluation. LLMs are already hard to evaluate, usually using benchmarks and
scored text outputs, and agents raise the bar further. They reason over multiple steps,
call tools, and sequences of actions, so a single quality score for the final text rarely
captures whether the agent did its job.
Because an agent acts on its environment instead of producing only text, evaluation
has to look at more than the words the agent generates. One lens is the outcome:
did the task actually get done, such as the message sent or the record updated? The
other is the trajectory: the steps and tool calls the agent took to get there, which can
be judged on efficiency and soundness even when the outcome is correct. Chapter 7
treats these as its two main lenses, outcome evaluation and trajectory evaluation.
Two additional properties get dedicated treatment because they don’t surface in a
single run. Reliability asks whether an agent succeeds every time, not just once,
since its outputs are stochastic. Safety asks whether it avoids harm, whether the risk
comes from a malicious user, from manipulated data the agent reads, or from its own
mistakes on an ordinary task. Taken together, this is why evaluating an agent is much
more than evaluating a model: you are evaluating an entire system.
In Chapter 7 we go deeper on all of this, from reading public benchmarks critically to
building an evaluation suite of your own.
The book is organized in two parts: the first covers a single agent on its own, and
the second covers what happens when agents work with each other and with the
wider world. Together with Chapter 7, Part I will primarily focus on the fundamentals
of a single agent, how it’s built, and how it can be evaluated. Part I is visualized in
Figure 1-20 and will serve as the common thread throughout Chapter 1 to Chapter 7.
What Is an AI Agent?
|