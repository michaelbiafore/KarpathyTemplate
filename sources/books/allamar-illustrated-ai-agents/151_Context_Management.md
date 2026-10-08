---
title: "Context Management"
chapter_number: 151
page_start: 411
page_end: 416
part: "Part II. Specialized Agents"
---
# Context Management

An example of this is if a user asks of a SQL agent of a fashion ecommerce shop: show
me all outerwear products. In the database the categories listed include jackets, blaz‐
ers, and coats, but not explicit “outerwear.” Recommended resources to dig deeper
into SQL agents include “Large Language Model Enhanced Text-to-SQL Generation:
A Survey” (2024), “The Dawn of Natural Language to SQL: Are We Fully Ready?”
(2024), and “A Survey on Employing Large Language Models for Text-to-SQL Tasks”
(2024). More recently, “Arming Data Agents with Tribal Knowledge” (2026) aug‐
ments a SQL agent with the institutional knowledge of what columns really mean and
how users phrase requests, accumulated from the agent’s own query mistakes instead
of from a hand-built semantic layer.
Those are the main tools that connect a code agent to its environment. Putting them
to work across a long task raises a different challenge: managing everything these
tools and steps pour into the model’s context.
Context Management
As with other agents, when environments grow, we need to get around the con‐
straints of the LLM context window on the one hand, and the latency and cost of
utilizing very long contexts even when they’re available.
Context optimization for the LLM cache
Even though the user asks the agent for just one thing, as agent builders we add a
great deal more to the context. Alongside the usual system and developer prompts,
agent persona, and tool descriptions, a software engineering agent’s context often
includes a section on desired security behaviors and a description of the repository
it’s working in. Many early software engineering agents are invoked against a single
project, as in an IDE operating on one repository, which is why the repository’s
structure ends up in the prompt. Much of this context is static and repeats on every
call as the agent works through a task over many steps.
That repetition is exactly what makes caching pay off. If we organize the context
carefully, we can get dramatic savings in latency and cost, something you’ll see called
kv-caching, prompt-caching, or prefix-caching. The idea, shown in Figure 10-8, was
introduced in Chapter 2.
Building Code Agents
|



![Figure 10-8: Caching lets the model reuse the calculations it has already run over the](images/fig_10-08_Caching_lets_the_model_reuse_the_calcula.png)

*Figure 10-8: Caching lets the model reuse the calculations it has already run over the*


Figure 10-8. Caching lets the model reuse the calculations it has already run over the
input prefix instead of recomputing them at each step. Here the large, fixed prefix (the
system prompt and repository structure) is cached
As Figure 10-9 shows, even the first call to a software engineering agent can run to
tens of thousands of tokens, and parts of it repeat in every subsequent call as the
agent works across multiple, sometimes dozens, of steps.



![Figure 10-9: The context assembled for a software engineering agent’s call](images/fig_10-09_The_context_assembled_for_a_software_eng.png)

*Figure 10-9: The context assembled for a software engineering agent’s call*


Figure 10-9. The context assembled for a software engineering agent’s call
|
Chapter 10: Code Agents and Code LLMs

To show it another way, Figure 10-10 shows the same two steps: the LLM call and
the tool call, but then the next step would be to continue the agent loop and present
the tool response to the LLM again. In this LLM call, instead of processing the entire
input again, and paying for these tokens in both latency and token cost, we can reuse
the cached calculations from the first step and append to them the new parts of the
trajectory.



![Figure 10-10: The growth of the context cache over an agent’s multi-turn loop, where](images/fig_10-10_The_growth_of_the_context_cache_over_an.png)

*Figure 10-10: The growth of the context cache over an agent’s multi-turn loop, where*


Figure 10-10. The growth of the context cache over an agent’s multi-turn loop, where
each action and observation is appended to the prompt
Note that for the cache to work, two things need to happen:
- The cached input needs to remain identical—we can’t even change a single token
in existing methods.
- All the new input needs to be appended to the end of the cached input.
Building Code Agents
|

Could you guess which parts we would now cache for the next LLM call? We see that
in Figure 10-11.



![Figure 10-11: Serving the entire accumulated context from cache to optimize latency and](images/fig_10-11_Serving_the_entire_accumulated_context_f.png)

*Figure 10-11: Serving the entire accumulated context from cache to optimize latency and*


Figure 10-11. Serving the entire accumulated context from cache to optimize latency and
cost
If you guessed the entire input of step 2, then you’re correct. By the third LLM call
(step 5), the entire context accumulated over the earlier steps is served from cache as
a single block, and only the new output is computed. Letting the cache grow to cover
the whole prior trajectory is what maximizes the cache hit rate.
This type of cache management is one of the key design constraints of agents in
general, and code agents in particular.2 Ideally, the cache continues to grow with the
trajectory to maximize the cache hit rate and minimize cost and latency.
2 Ji, Yichao. “Peak.” 2025. “Context Engineering for AI Agents: Lessons from Building Manus” Blog post, https://
oreil.ly/fbw-y.
|
Chapter 10: Code Agents and Code LLMs

The repository map
As we saw in “Context Management,” representing the structure of a repository is
essential context for plenty of software engineering agents. Key components of a
repository map are file and directory structure at some level of resolution and some
additional information about all or a selection of relevant files.
One popular tool to generate a repository map is Gitingest, which can take the URL
of a GitHub repo and generate a repo map that includes the directory list as well as
the contents of short files.
In a blog post, the creators of Aider, one of the early command-line code agents and
a clear precursor to tools like Claude Code, describe a more thoughtful approach
to generating file summaries, which relies on the abstract syntax tree to identify
important parts like class and function signatures, and using these as summaries of
the files. They additionally employ a follow-up step of ranking and filtering for only
the most relevant definitions that are used the most in other parts of the repository.
Figure 10-12 shows an example repo summary listing both the files and some file
descriptions in the style of Aider’s repo map.



![Figure 10-12: In the style of Aider’s map, this summarized repository (a repo map)](images/fig_10-12_In_the_style_of_Aiders_map_this_summariz.png)

*Figure 10-12: In the style of Aider’s map, this summarized repository (a repo map)*


Figure 10-12. In the style of Aider’s map, this summarized repository (a repo map)
captures the directory structure along with previews of the most relevant files
One final repo description method that’s relevant to know, especially when we can
expend additional LLM calls for a certain task, is to use an LLM to summarize key
Building Code Agents
|

or relevant files. You can see such an example employed in the paper “CodeMonkeys:
Scaling Test-Time Compute for Software Engineering.”3 Their efficiency comes from
amortization: because the system already samples many candidate solutions per issue,
it can afford to have an LLM read every file in the repository to find the relevant ones,
spreading that one-time cost across all the downstream samples so it accounts for
only about 15% of the total budget. The identified files are then ranked and trimmed
to fit the context used in later steps.
Context compaction
In Chapter 4, we saw how summarizing the context of a long conversation is one
form of short-term memory that allows us to shrink the context to continue a
conversation. In different specialized agents, the information that is required in that
summary often needs to be optimized for that domain. For code agents, that may
include information on the environment, code style preferences, preferences for
when and how to run tests and when to commit the repository to source control.
Viewed together with what we’ve covered in cache optimization, we may find a
pattern where we can keep different sections of the trajectory more static to optimize
the cache hit rate. In Figure 10-13, we can see one example breakdown of different
sections that change at different frequencies. The static section stays put, the stable
section shifts now and then, and only the dynamic section turns over step to step.
After compaction, the dynamic section shrinks while everything above it can keep
getting served from cache.
If we organize our work properly, after compaction we can find ourselves with
a much more shrunken dynamic section, while the static and stable section can
generally remain intact and cached for more and more steps.
3 Ehrlich, Ryan et al. 2025. “CodeMonkeys: Scaling Test-Time Compute for Software Engineering,” arXiv,
2501. 14723.
|
Chapter 10: Code Agents and Code LLMs