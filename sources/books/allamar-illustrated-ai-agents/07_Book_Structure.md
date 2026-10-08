---
title: "Book Structure"
chapter_number: 7
page_start: 15
page_end: 15
---
# Book Structure

- If you come from a research or machine learning background, the deeper
sections on model internals, training techniques, and evaluation methodology
connect agent behavior back to how these models are actually made.
- If you are a technical leader, product builder, or curious reader who wants a
rigorous mental model of agents without writing code, the illustrations and
intuition-first explanations carry the full conceptual story on their own. The code
can be skipped without losing the plot, or, fittingly, handed to your coding agent.
Where a chapter serves these audiences differently, we say so up front and tell you
which parts you can skim. Whether you are encountering agents for the first time or
already deploying them in production, we invite you to join us on this journey.
Prerequisites
What you need depends on how you plan to read this book. To follow the conceptual
thread, the illustrations and intuition-first explanations, you need nothing beyond
curiosity: no programming, no mathematics, and no prior exposure to agent frame‐
works. Familiarity with LLMs helps, but Chapters 2 and 3 cover everything about
them that the rest of the book relies on.
To follow the hands-on thread and build the TinyAgent yourself, you will want some
experience programming in Python. The deeper sections on model internals and
training assume familiarity with the fundamentals of machine learning, though even
there the focus is on building intuition rather than deriving equations.
If you are not familiar with Python, LearnPython.org, where you will find many
tutorials on the basics of the language, is a great place to start. And to further ease
the learning process, every example in this book can be run in the browser for free,
without installing anything locally; see “Hardware and Software Requirements” on
page xiv.
Book Structure
The book is divided into two parts:
Part 1: The Anatomy of an AI Agent
In Part 1, we build a single agent from the ground up. Chapter 1 introduces
the field and the core question, “What is an AI agent?,” and presents the figure
that anchors the rest of the book. Chapters 2 and 3 cover the agent’s brain: how
LLMs work (Chapter 2) and how reasoning LLMs extend them with the ability to
think through problems before acting (Chapter 3). We then augment that brain
with memory (Chapter 4) and with tools, including how tool use is standardized
across models through the Model Context Protocol (Chapter 5). Chapter 6 adds
the final ingredient, planning and reflection, which turns an augmented LLM
Preface
|
xiii