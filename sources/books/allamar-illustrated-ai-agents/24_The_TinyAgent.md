---
title: "The TinyAgent"
chapter_number: 24
page_start: 44
page_end: 48
part: "Part I. The Anatomy of an AI Agent"
---
# The TinyAgent



![Figure 1-25: Certain multi-modal LLMs can have the capability of generating modalities](images/fig_01-25_Certain_multi-modal_LLMs_can_have_the_ca.png)

*Figure 1-25: Certain multi-modal LLMs can have the capability of generating modalities*


Figure 1-25. Certain multi-modal LLMs can have the capability of generating modalities
other than text
The Coding Agent
Another popular variant of agents is the coding agent. Unlike traditional AI assis‐
tants, where you have a back-and-forth discussing code, a coding agent can actually
run the program in a dedicated environment. Even more, it can read existing codeba‐
ses, generate new functions, fix bugs, and test what it has created. Increasingly, coding
agents are reshaping the nature of software engineering while granting non-software
engineers capabilities that would be beyond their reach had they not had access to
such agents. This has led to the concept of “vibe coding,” where agents are relied on to
build software for non-developers.
Building and using coding agents effectively is the subject of Chapter 10, along with
how the underlying code LLMs are trained to power them. Coding benchmarks such
as SWE-bench, and how agents are scored on them, are covered in Chapter 7.
The TinyAgent
Although “illustrated” is in the name of this book, wouldn’t it be nice to put some of
the principles covered into practice? As you explore various components of AI agents
and slowly build up the theoretical foundation of an agent through visuals, you’ll do
the same in code.
|
Chapter 1: Introduction

Specifically, you’ll build up a TinyAgent one step at a time. Using the foundations
learned in this book, we’ll explore how to convert them into actual Python code.
You can follow along with the notebooks provided in our GitHub repository. There,
you’ll find all code along with bonus content that’s not covered in this book. To be
able to run this code anywhere, we provided several options to install it as a package,
through pip, or uv. This code is what implements the behavior of the TinyAgent and
is typically called the agent harness. There are many different types of harnesses that
you might come across:
Terminal-based
Agents that run directly in the terminal, such as Claude Code, Gemini CLI,
OpenAI Codex CLI, OpenCode, etc.
Code-based
Libraries you write code against to build your own agent, such as LangGraph,
Smolagents, Pydantic AI, etc.
Personal assistant
Persistent agents that retain memory and skills across sessions, such as Open‐
Claw, Hermes Agent, etc.
Hosted
Agents that run in the cloud as a hosted product, such as Replit, v0, Manus, etc.
UI-based
Agents embedded inside a user-friendly interface, such as Antigravity, Cursor,
Windsurf, GitHub Copilot, etc.
Interestingly, while writing this overview of agentic harnesses, it
feels like this list is already becoming outdated. That’s how fast
things can move in this field! So how do you keep up? We believe
that as long as you learn the foundations well, it will be easier
to navigate new releases, frameworks, and models. After all, all of
these harnesses essentially use the same type of agent scaffolding
(LLM, memory, tools, etc.). They just flavor them a bit differently.



![Figure on page 17](images/fig_p017_x95.png)


Note that these harnesses are starting to evolve more into personal assistants. These
harnesses focus on making agents persistent and always on. You can chat with your
agent via any messaging system (such as WhatsApp, Discord, Slack, or even email)
and they can autonomously solve tasks for you. These harnesses tend to give agents
the most autonomy, such as checking your email, calendar, personal files, etc.
Arguably, the most famous example is OpenClaw, which gained an astonishing
300,000 stars on GitHub in only a couple of months after its release. OpenClaw is one
of the first harnesses that allows users to easily create a persistent personal assistant.
The TinyAgent
|

Since then, there have been many different alternatives, such as Hermes Agent, that
gained popularity (Figure 1-26).



![Figure 1-26: The number of stars on GitHub for open source personal assistant harnesses](images/fig_01-26_The_number_of_stars_on_GitHub_for_open_s.png)

*Figure 1-26: The number of stars on GitHub for open source personal assistant harnesses*


Figure 1-26. The number of stars on GitHub for open source personal assistant harnesses
since their release
The harness of the TinyAgent that you’re going to build is mostly code-based and will
have a terminal implementation. We focus on the educational nature of this harness
and decided that the best way to learn is to build an agent from scratch!
We’re not going to use packages that abstract away the complexities but instead
dive deep into them. The TinyAgent will be built with minimal dependencies and
we’ll explain everything you implement along the way. To do so, we make use of
a highly modular and educational structure that focuses on understanding the vital
components of an agent. Figure 1-27 shows some of the components that will be
added to the TinyAgent.
|
Chapter 1: Introduction



![Figure 1-27: A sneak peek into the different modules that we’re going to explore and](images/fig_01-27_A_sneak_peek_into_the_different_modules.png)

*Figure 1-27: A sneak peek into the different modules that we’re going to explore and*


Figure 1-27. A sneak peek into the different modules that we’re going to explore and
you’re going to build
In this chapter, you’ll take your first step!
We start with building the TinyAgent class, which is used as the skeleton on which
we slowly add components in each chapter. This class is meant to remain small and
showcase only the fundamental principles:
class TinyAgent:
 """A minimal, modular, and educational agent framework."""

 def __init__(self):
 self.llm = None # Chapter 2 & 3: Add LLM
 self.memory = None # Chapter 4: Add Memory
 self.tools = None # Chapter 5: Add Tools
 self.planner = None # Chapter 6: Add Planning

 def run(self, task: str) -> str:
 """Run the agent on a task."""
 return self._step(task)

 def _step(self, task: str) -> str:
 """Perform a single step."""
 # Placeholder - will be implemented in later chapters
 return f"Received: {task}"

 def _execute_action(self, action: str) -> str:
 """Execute a tool action."""
 # Placeholder - will be implemented in later chapters
 return f"Executed action: {action}"
The TinyAgent
|

This scaffolding of the agent does not do anything at the moment other than parrot‐
ing what you say. The components are as follows:
run
Run the agent on a given task
_step
Perform a single step, which might include an answer or a tool call (Chapter 2)
_execute_action
Execute a single action using a tool (Chapter 5)
Throughout this chapter, you will be able to run your TinyAgent with the following:
agent = TinyAgent()
agent.run("What is 2 + 2?")
Because this (the LLM) is merely a skeleton without a brain, the agent simply returns
our question:
'Received: What is 2 + 2?'
The code we explore in this book revolves around a single core entity: building your
TinyAgent. Although each chapter is designed to be self-contained, all code across
chapters can be run out of order. However, each chapter builds on your TinyAgent
and evolves it as you progress through the chapter. The result is essentially a package
that you have developed yourself. To track this evolution, at the end of all code
in a chapter, we conclude with a summary of what we built. Reviewing this small
overview will give you a sense of the changes that were made to your TinyAgent.
What We Built
TinyAgent/
 └── agent.py ← New (`TinyAgent` skeleton)
Likewise, as you go through each chapter, your TinyAgent might need some small
updates, such as tracking the state of the agent. We have provided various tools that
allow you to easily view these differences (or “diffs”) in the illustrated-agents package.
We will first explore that in Chapter 2, along with arguably the most important
component of an agent, its brain!
|
Chapter 1: Introduction