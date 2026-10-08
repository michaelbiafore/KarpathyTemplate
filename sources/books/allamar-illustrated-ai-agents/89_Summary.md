---
title: "Summary"
chapter_number: 89
page_start: 242
page_end: 242
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Summary

Table 5-1. The layers of progressive disclosure and their impact on tokens
Layer File
Activation
Number of tokens
SKILL.md metadata (YAML)
Always loaded
~100
SKILL.md instruction (Markdown)
Loaded when activated Fewer than 5,000
Bundled files (Markdown, scripts, data, etc.) Loaded when needed
As needed
In the book’s GitHub repository, you’ll find an additional notebook that shows how
to give your TinyAgent access to Skills.
Summary
In this chapter, we explored how tool calling gives LLMs the capabilities to interact
with the world. We first covered the fundamentals of tool calling and how LLMs call
tools in practice. We saw that as text-to-text entities, LLMs merely communicate the
intent to call a tool. The act of actually calling the tool falls either to the user or to
external software that automates this process. The flow of calling a tool involved the
tool creation, definition, selection, calling, and output processing.
Then, we explored three methods of having LLMs learn those tool-calling capabil‐
ities. First was in-context learning, where you can define the tool’s schemas and
definition in the prompt for the LLM to follow. Second was SFT, where an LLM is
fine-tuned on specific tool-calling capabilities. We covered Toolformer as one of the
first successful attempts to use SFT for tool calling. Lastly, we covered RL as one of
the most prominent techniques for instilling tool-calling capabilities. Of note were
ToolRL and Search-R1, which both adopt GRPO, a popular RL algorithm used in
DeepSeek-R1.
We then looked at one of the most exciting things in the realm of tool calling,
the MCP. We explored how MCP standardizes the usage of tools, which led to the
widespread use of tools without the need for custom solutions.
We finally looked at Skills, Anthropic’s approach to giving agents the procedural
knowledge they need to operate in your specific context. Where tool definitions tell
an agent what a tool does, Skills tell it how to get a job done—the recipe of steps, con‐
ventions, and references it should follow for a recurring task. Through progressive
disclosure across three layers—metadata, instructions, and bundled resources—Skills
surface this guidance only when the agent decides a Skill is relevant, keeping the
context window lean.
Along the way, your TinyAgent gained both prompt-based and native tool-calling
capabilities, setting the stage for Chapter 6, where it will start choosing and sequenc‐
ing those tools on its own.
|
Chapter 5: Tool Usage, Learning, and Protocols