---
title: "The SKILL.md"
chapter_number: 87
page_start: 239
page_end: 239
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# The SKILL.md

be quite the annoyance. This is where Skills come in. Created by Anthropic, Skills are
a set of instructions, scripts, and resources the agent can use as context to perform a
given task. They contain procedural knowledge, which are step-by-step instructions
that allow the agent to understand how to best approach a task given in your specific
context.
For instance, if you want it to create a presentation, you might need it to first search
the web for relevant information (this is a tool), then summarize this information (it
can do this by itself), and then finally create the slides one at a time (this is also a
tool). This workflow or “recipe” for creating a presentation might therefore include
a set of tools but also instructions on how to use them and in what order. As such,
Skills teach your agent what to do, when to do it, and how.
A Skill revolves around progressive disclosure. This means that the agent starts with
minimal information on what the Skill may provide, and when it is accessed provides
more information on how to execute it. This progression typically follows three layers
of depth:
Layer 1 (always loaded)
Metadata about the Skill (e.g., name and description)
Layer 2 (loaded when activated)
The main Skill instructions
Layer 3 (loaded when needed)
Additional resources to use (e.g., scripts and references)
To explore these layers and the anatomy of a Skill, let’s use an example. Imagine
you have many meetings to keep track of every week and want to convert your
transcripts and rough notes into structured meetings notes with actions items. Your
agent does not know beforehand how you want the notes structured, the context of
the people you’re meeting, etc. A Skill would give the context needed to perform the
task depending on the type of meeting you have. The first thing needed to create a
Skill is the SKILL.md file.
The SKILL.md
Every Skill is required to have a SKILL.md file. The start of this file contains the Skill’s
metadata, namely the name and a short description. For instance, the name of your
Skill could be “meeting_notes” and its description: “Use this skill when you want to
turn meeting transcripts and notes into structured decisions and action items.” When
you first interact with your agent, only this name and description are provided so
that the agent can decide whether it’s worth exploring it in more detail for a given
task. Regardless of how many Skills you add, their names and descriptions are always
shared with the agent (often as a system prompt). This metadata section is formatted
as YAML, so you can clearly separate this metadata from the rest.
Skills
|