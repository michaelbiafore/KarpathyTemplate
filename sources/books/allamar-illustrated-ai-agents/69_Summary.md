---
title: "Summary"
chapter_number: 69
page_start: 193
page_end: 194
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Summary

with. More specifically, the context that you give to the agent, including the query,
PLAN.md, REQUIREMENTS.md, codebase, etc., all serve as a tool to communicate
your intention. For example, when you allow a coding agent to fully create a PR on its
own, it does not suffice to go through the code itself to check whether everything is
there. The initial query, PLAN.md, etc., all serve as the initial specification of the PR
and should be tracked as well.
As such, we can view the context of the agent as the specification of your feature.
As agents are becoming more autonomous, it’s important to track the intention of
their behavior through the context that is given. Where we would view prompt
engineering as user-facing, context engineering is a much more developer-oriented
tool and requires careful communication of why the agent is executing certain tasks.
The answer to the “why” starts with the user’s intention.
Think about it like this: how strange it is that we tend to throw away the input to our
function (the LLM) and keep track only of the output! Not only for reproducibility,
but also for communication, it allows you to understand why the agent has chosen
certain tools, executions, and outputs. Moreover, this transparency of intention also
serves as a great tool for debugging your agent.
Context, as the specification, brings about significant potential for domain-specific
industries. The context that you give an agent changes drastically between use cases
and applications. Health care requires a completely different context than law, for
instance. As such, there is not a single framework for context engineering and
instead it requires developers to consider their domain-specific knowledge sources,
like patient data in health care and research papers in academia.
Summary
In this chapter, we explored various methods for giving LLMs and agents memory.
We first covered various techniques for short-term memory, including the conversa‐
tion history and methods for compressing it and keeping it manageable. Short-term
memory is an important, but often underestimated component of enabling memory
in intelligent systems.
Then, we explored long-term memory, including methods for RAG (MemoryBank)
and agentic RAG (A-MEM and Search-o1). These methods are often inspired by
human memory systems and may include techniques for degrading memory or
deciding what’s meant to be important.
Finally, we explored context engineering as the next frontier in memory. Where we
used to engineer our prompts ourselves, the entire context window now requires
careful consideration. We covered why this context is important for agents and
various methods for optimizing it.
Summary
|

The context, being much more than just the user’s prompt, contains all previously
discussed forms of memory and potentially even more, like tools. In Chapter 5, we’ll
explore how tools can further enhance the capabilities of LLMs as an important
component of agents. Moreover, we’ll cover how these tools can be called and the best
practices for doing so. In Chapter 6, we cover planning and reflection capabilities of
agents, where memory plays an important role.
|
Chapter 4: Memory