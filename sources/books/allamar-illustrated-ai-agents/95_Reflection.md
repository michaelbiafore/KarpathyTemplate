---
title: "Reflection"
chapter_number: 95
page_start: 270
page_end: 273
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Reflection

the curtain. If we had jumped directly into native capabilities, much of the behavior
would have seemed like a closed box.
Agents That Continuously Improve
As AI agents evolve, instead of relying on training phases or reward models for
improvement, these systems start relying on self-generated feedback loops to con‐
tinuously improve their performance as they act. Feedback prevents agents from
ending up in local minima and provides valuable information on potentially better
solutions to pursue. In practice, not all feedback is equivalent, and continuous self-
improvement is tricky to pursue for LLMs that are fundamentally static when they
act. In this section, we explore methods for AI agents to reflect on their behavior and
pursue self-improvement as they act with their environment(s).
Reflection
The feedback that an agent gets from its environment is typically different from
process feedback. The environment gives feedback based on an action: “When I do
X (action), the environment gives back Y (feedback).” Feedback, as covered in this
section, is often referred to as “reflection” to demonstrate that it is typically an
internal process where the LLM should be critical of its own output and processes.
After all, reflecting on past behavior helps us learn from prior failings. Reflection,
however, can also be in tandem with external sources to supply feedback.
The techniques covered in this section are all based on prompting techniques and are
therefore relatively straightforward to implement.
Self-Refine
An elegant approach to feedback is Self-Refine,13 a prompting framework where the
LLM provides feedback and refines its own results. The approach is quite straightfor‐
ward and lets an LLM iteratively improve its answer by acting as its own editor. The
idea was inspired by how people draft and revise their solutions.
In this framework, the LLM generates an initial answer and then proceeds to critique
its own output (feedback). Based on that reflection step, the LLM refines its answer
and incorporates the necessary change (refine). This cycle repeats until a stopping
criterion has been reached, such as the number of steps or an LLM-guided stopping
mechanism. This cycle between feedback and refine is shown in Figure 6-18.
13 Madaan, Aman et al. 2023. “Self-Refine: Iterative Refinement with Self-Feedback,” Advances in Neural Infor‐
mation Processing Systems, 36: 46534-46594.
|
Chapter 6: Planning and Reflection



![Figure 6-18: The main steps of self-refine where the same LLM continuously refines](images/fig_06-18_The_main_steps_of_self-refine_where_the.png)

*Figure 6-18: The main steps of self-refine where the same LLM continuously refines*


Figure 6-18. The main steps of self-refine where the same LLM continuously refines
generated output
The same LLM generates the initial output, the refined output, and feedback, hence
the name Self-Refine. Figure 6-19 illustrates an example from the paper where, after
an initial output, an iterative loop is generated of first feedback and then a refined
output.



![Figure 6-19: An example from the Self-Refine paper where an LLM starts from a given](images/fig_06-19_An_example_from_the_Self-Refine_paper_wh.png)

*Figure 6-19: An example from the Self-Refine paper where an LLM starts from a given*


Figure 6-19. An example from the Self-Refine paper where an LLM starts from a given
generated output and continuously updates and refines it
As you might have noted, this framework was built around LLMs refining and
improving their own outputs, but no mention is given of an agentic system. Next,
let’s explore how ReAct can use similar feedback mechanisms to improve agentic
trajectories.
Agents That Continuously Improve
|

Reflexion
A more involved but quite successful attempt at instilling reflective behavior in agents
is Reflexion,14 a prompting framework where agents verbally reflect on previous tasks
through internal and external feedback. The authors used three entities within this
framework:
Actor LLM
A ReAct LLM in charge of executing actions based on observations and trajec‐
tory data. This can be considered the main “brain” of the agent.
Evaluator LLM
An LLM that assesses the quality of the current trajectory and output generated
by the Actor LLM.
Self-Reflection LLM
This LLM generates more nuanced and specific feedback based on the full trajec‐
tory, including the output of the Evaluator LLM.
As shown in Figure 6-20, the Actor LLM is based on a ReAct agent and will convert
the initial task into actions and interact with the environment. The resulting observa‐
tions are saved in the full trajectory for which the Evaluator LLM rewards a score
that reflects the performance of the Actor LLM given the task. The Evaluator LLM
is essentially asked, “How well did the Actor LLM do?” and produces a scalar reward.
The current trajectory, including the reward, is given to the Self-Reflection LLM to
analyze the trajectory and produce a reflective summary for the Actor LLM to use.
This process continues until the Evaluator LLM deems the answer of the Actor LLM
to be correct.
These three LLMs are vital to provide the actions (Actor), the stopping mechanism
(Evaluator), and the reflective feedback (Self-Reflector). They are tied together by
the different forms of memory, where the trajectory is saved in short-term memory
(conversation memory) and the reflective experiences based on the trajectories within
the long-term memory.
14 Shinn, Noah et al. 2023. “Reflexion: Language Agents with Verbal Reinforcement Learning,” Advances in
Neural Information Processing Systems, 36: 8634-8652.
|
Chapter 6: Planning and Reflection



![Figure 6-20: The Reflexion process uses separate LLM roles (Actor, Evaluator, Self-](images/fig_06-20_The_Reflexion_process_uses_separate_LLM.png)

*Figure 6-20: The Reflexion process uses separate LLM roles (Actor, Evaluator, Self-*


Figure 6-20. The Reflexion process uses separate LLM roles (Actor, Evaluator, Self-
Reflection) to iteratively refine actions
Together, these components allow Reflexion agents to verbally reflect on trajectory
observations, which are maintained in episodic memory to promote improved deci‐
sion making in subsequent trials.
Self-Refine and Reflexion are common techniques to easily create agents that have
some reflective capabilities. Many other prompt-based techniques exist that attempt
something similar, such as CRITIC,15 which starts with an initial output and revises
it through the use of external tools, like search, to get more information. As such,
feedback is an important component of agents that can reflect, and as the Reflexion
framework shows, feedback can come from many places, including both itself and its
environment.
However, like all prompt-based techniques we have explored thus far, they only
guide the agent toward behavior that we previously described without instilling that
behavior into its parameters. Let’s explore techniques that allow reflective behavior to
be a part of an agent’s nature through fine-tuning the model.
15 Gou, Zhibin et al. 2023. “CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing,”
arXiv, 2305.11738.
Agents That Continuously Improve
|