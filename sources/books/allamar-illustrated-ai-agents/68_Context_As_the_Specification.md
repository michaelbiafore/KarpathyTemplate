---
title: "Context As the Specification"
chapter_number: 68
page_start: 192
page_end: 192
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Context As the Specification

techniques can be used to remove contexts that are essentially duplicates of one
another.
Context ordering
The order of the context is vital to the performance of your agent. Early research into
the position of important information in prompts found that LLMs have a tendency
to pay more attention to the beginning and end of a prompt.18 As a result, they often
end up losing information in the middle, which is termed the “lost-in-the-middle”
phenomenon. Figure 4-37 nicely illustrates this concept.



![Figure 4-37: An annotated figure of the “lost-in-the-middle” phenomenon from “Lost in](images/fig_04-37_An_annotated_figure_of_the_lost-in-the-m.png)

*Figure 4-37: An annotated figure of the “lost-in-the-middle” phenomenon from “Lost in*


Figure 4-37. An annotated figure of the “lost-in-the-middle” phenomenon from “Lost in
the Middle”
This tendency to focus on the beginning and end of prompts is similar to human
behavior. The serial-position effect states that people generally recall the first (pri‐
macy effect) and last (recency effect) items in a series best, whereas the middle items
are recalled worst.19 Typically, context engineering helps prevent this problem because
it appears with long contexts rather than small ones. It’s interesting to see how much
of LLMs’ behavior follows similar human tendencies.
Context As the Specification
Arguably, one of the most important things about context engineering is that it
requires a shift in mindset. The context that is given to the agent can be seen as
a tool for communication—not just for the agent, but to the people that you work
18 Liu, Nelson F. et al. 2023. “Lost in the Middle: How Language Models Use Long Contexts,” arXiv, 2307.03172.
19 Murdock, Bennet B. Jr. 1962. “The Serial Position Effect of Free Recall,” Journal of Experimental Psychology,
64(5):482.
|
Chapter 4: Memory