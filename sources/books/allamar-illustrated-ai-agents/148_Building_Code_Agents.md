---
title: "Building Code Agents"
chapter_number: 148
page_start: 400
page_end: 400
part: "Part II. Specialized Agents"
---
# Building Code Agents

Building Code Agents
The first thing that comes to a lot of readers’ minds when they read “code agents” is
Cursor-like software engineering agents. And while that’s one of the main categories,
let’s actually start with a use case that can serve a much larger group of users, those
who are not programmers.
Code Agents to Serve Non-Coders
Code agents open the door for non-coders to wield powerful code tools they did
not have access to before. Data analysis is a great example of this. Let’s expand on a
request to a code agent to make a certain plot, as we can see in Figure 10-3.



![Figure 10-3: An agent generating a plot by writing code to retrieve data and using](images/fig_10-03_An_agent_generating_a_plot_by_writing_co.png)

*Figure 10-3: An agent generating a plot by writing code to retrieve data and using*


Figure 10-3. An agent generating a plot by writing code to retrieve data and using
libraries to render the visual
When we ask the agent to plot a figure, the main behaviors we expect from it are the
following:
1. Data retrieval
The agent will need to decide what tool to use to retrieve the data we need to plot.
On the simpler side, this can be a web search tool. But this can also require the
agent to generate code to retrieve that data:
A) You hand the agent the file (for example, a spreadsheet)
A simple tool to use here is a Python sandbox environment that we pass the
exact file to. Here, the agent will need to write code to read and manipulate
the data in data manipulation libraries like pandas or polars.
|
Chapter 10: Code Agents and Code LLMs