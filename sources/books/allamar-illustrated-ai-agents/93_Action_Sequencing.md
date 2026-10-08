---
title: "Action Sequencing"
chapter_number: 93
page_start: 252
page_end: 269
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Action Sequencing

Action Sequencing
Least-to-most prompting and plan-and-solve prompting decompose a given problem
into subtasks that are solved sequentially. These work great for LLMs, but not yet
for agents, who sequence actions autonomously one after the other. Specifically, after
the agent decides the (sub)goals it needs to achieve, it then determines a sequence of
actions to continuously transition it from its current state to the desired goal state.
This process is called action sequencing and requires not only a careful plan but also
an efficient set of steps for the agent to follow.
For example, a coding agent needs to decide which optimal sequence of actions
should be taken. If it skips over reading the codebase, for instance, then the agent
would be quite inefficient and this could potentially lead to redundancy. To minimize
wasted resources and reduce execution time, there needs to be a well-thought-out
sequence of actions relating to the plan.
In this section, we’ll explore methodologies for sequencing actions, of which impor‐
tant components are CoT-like reasoning and planning the sequence of actions.
We want the agent not only to create a plan but continuously solve each subtask while
updating its current state. This idea is shown in Figure 6-9 and requires more sophis‐
ticated techniques than least-to-most prompting and plan-and-solve prompting.
The idea of these techniques is that agents rely on their LLMs’ reasoning capabilities
to dynamically adjust their plans based on new information as a result of previous
steps. It also explains how agents can act autonomously after having created the initial
plan.



![Figure 6-9: Action sequencing in an agent, where the agent generates thoughts, actions,](images/fig_06-09_Action_sequencing_in_an_agent_where_the.png)

*Figure 6-9: Action sequencing in an agent, where the agent generates thoughts, actions,*


Figure 6-9. Action sequencing in an agent, where the agent generates thoughts, actions,
and observations in an iterative loop
|
Chapter 6: Planning and Reflection

Reason and act with prompting
In previous examples, we explored how reasoning can be enabled with CoT and how
LLMs can take actions (such as with the Toolformer discussed in Chapter 5). This
split between reasoning and acting is shown in Figure 6-10.



![Figure 6-10: Before ReAct, reasoning and acting were treated as separate capabilities](images/fig_06-10_Before_ReAct_reasoning_and_acting_were_t.png)

*Figure 6-10: Before ReAct, reasoning and acting were treated as separate capabilities*


Figure 6-10. Before ReAct, reasoning and acting were treated as separate capabilities
However, having reasoning and acting separate makes it difficult for an agent to iter‐
ate. A common technique for determining an initial plan and continuously updating
its action sequencing is the Reason and Act (ReAct) framework.6 Compared to CoT,
which embeds reasoning within the planning, ReAct decouples reasoning and plan‐
ning. The framework takes inspiration from CoT for reasoning and tool usage for
acting and combines them. As shown in Figure 6-11, this framework interleaves both
reasoning traces and task-specific actions to create an iterative process of thinking
and taking actions. As a result, we get the first truly autonomous systems that drive
AI agents.



![Figure 6-11: ReAct fuses reasoning and acting, allowing the LLM to produce a reasoning](images/fig_06-11_ReAct_fuses_reasoning_and_acting_allowin.png)

*Figure 6-11: ReAct fuses reasoning and acting, allowing the LLM to produce a reasoning*


Figure 6-11. ReAct fuses reasoning and acting, allowing the LLM to produce a reasoning
trace, execute an action, and observe the result
6 Yao, Shunyu et al. 2022. “ReAct: Synergizing Reasoning and Acting in Language Models,” The Eleventh
International Conference on Learning Representations.
Planning
|

The interleaving of reasoning and actions creates a feedback loop in which the model
repeatedly cycles through a thought-action-observation process. In each loop, the
model is asked to separate its textual output into three components:
Thought
A reasoning step about the current situation
Action
A set of actions to execute (e.g., tools)
Observation
A reasoning step about the result of the action
This is achieved by prompting the model to create these three separate entities
(Figure 6-12). Note that few-shot examples of thought, action, and observation cycles
are typically added to make sure that the LLM matches the proposed behavior.



![Figure 6-12: If the model has strong instruction-following capabilities, ReAct can be](images/fig_06-12_If_the_model_has_strong_instruction-foll.png)

*Figure 6-12: If the model has strong instruction-following capabilities, ReAct can be*


Figure 6-12. If the model has strong instruction-following capabilities, ReAct can be
enabled through prompting
This type of prompt is at the core of a ReAct agent and steers the LLM’s behavior
toward cycles of thoughts, actions, and observations (see Figure 6-13). By iterating
over thoughts and observations, the LLM can plan out actions, observe its output,
and adjust accordingly. Then, the LLM will stop whenever it reaches a predefined
goal.
ReAct agents can theoretically go on for hundreds of cycles but need to remember
their previous steps and outcomes to effectively continue when context becomes an
|
Chapter 6: Planning and Reflection

issue. For agents that go on to perform dozens or potentially hundreds of steps, the
memory component becomes vital, especially context engineering, as we discussed in
Chapter 4.



![Figure 6-13: Two cycles of THOUGHT/ACTION/OBSERVATION using the ReAct](images/fig_06-13_Two_cycles_of_THOUGHTACTIONOBSERVATION_u.png)

*Figure 6-13: Two cycles of THOUGHT/ACTION/OBSERVATION using the ReAct*


Figure 6-13. Two cycles of THOUGHT/ACTION/OBSERVATION using the ReAct
framework
To give a bit more intuition about this ReAct flow and the final step in making
your TinyAgent fully autonomous, let’s implement it. For the most part, ReAct
requires careful prompting to nudge the LLM’s behavior toward loops of THOUGHT,
ACTION, and OBSERVATION. To do so, let’s create the ReAct class as the first
planner class to use in your TinyAgent:
```
import re
from illustrated_agents.chapters.ch2 import Response
```

class ReAct:
Planning
|

"""ReAct module."""

 def __init__(self, max_steps: int = 10):
 """Initialize ReAct module.

 Arguments:
 max_steps: Maximum number of ReAct steps to perform.
 """
 self.max_steps = max_steps

 @property
```
 def prompt(self) -> str:
 return """
```
# ReAct (Reason and Act)

You are a ReAct agent that performs exactly ONE step per turn.

## ReAct Format

You use the following format for each step:

THOUGHT: [Your reasoning about what to do next]
ACTION:
{
 "tool": "a_tool_name",
 "kwargs": {"param": "value"},
}

An observation will be provided after each action. You do not generate the
observation yourself.

## ReAct Completion

To provide the final answer to the task, use an action blob with "tool":
"final_answer" tool.
It is the only way to complete the task, else you will be stuck on a loop.
So your final output should look like this:

ACTION:
{
 "tool": "final_answer",
 "kwargs": "insert your final answer here"
}

Use the `final_answer` tool when you are completely done with all subtasks and
have the final answer ready.
You can also use `final_answer` to directly reply to a user's question without
using any other tools.

"""

 def parse(self, response: Response) -> Response:
|
Chapter 6: Planning and Reflection

"""Parse a ReAct formatted response into THOUGHT and ACTION."""
 text = response.content

 # The patterns for each section
 patterns = {
 "THOUGHT": r"THOUGHT:\s*(.+?)(?=ACTION:|OBSERVATION:|$)",
 "ACTION": r"ACTION:\s*(.+?)(?=THOUGHT:|OBSERVATION:|$)",
 }

 # Extract each section using regex
 result = {}
 for key, pattern in patterns.items():
 match = re.search(pattern, text, re.DOTALL)
 result[key] = match.group(1).strip() if match else ""

 # Update Response and extract only the action
 response.content = result["ACTION"]
 response.reasoning = result["THOUGHT"]
 return response
It might seem like a lot, but only three things are happening within this ReAct class:
1. The max_steps parameter is used to decide the maximum number of steps your
1.
TinyAgent will get to perform its autonomous behavior. The agent can still
decide to stop early, but this prevents it from being stuck in a loop.
2. The .prompt property, much like in Tools, is used to provide sufficient context
2.
on how to approach the ReAct behavior. It specifically describes the ReAct
format (## ReAct Format) and how it should provide a final answer (## ReAct
Completion). Note that this ReAct implementation assumes that the actions are
with Tools and not the NativeTools class that we covered in Chapter 5.
3. The .parse function is used to convert the THOUGHT/ACTION description
3.
into separate fields so they can be used as the Response.reasoning and
Response.content fields, respectively. Remember from Chapter 5 that the Tools
class assumes that the tool call is initially in the Response.content field since
Tools uses prompt-based tool calling rather than native tool calling.
Now that we have the ReAct class, let’s implement it in your TinyAgent to create
your autonomous agent. The most important step to create a fully autonomous agent
is…a for-loop! Truly, with the capabilities of agents these days, it all boils down to
iteratively calling an LLM until it decides to stop the loop.
With the ReAct framework, we structure the for-loop into the THOUGHT/ACTION/
OBSERVATION steps to ensure the model has a clear goal and a clear set of steps to
reach it. Implementing this into your TinyAgent will require three main changes:
Planning
|

- Add the ReAct instruction to the system prompt.
•
- Add an autonomy loop to the .run function.
•
- Parse the LLM’s response into THOUGHT/ACTION.
•
The updated TinyAgent is as follows, where we highlighted the code that was added:
```
from illustrated_agents.chapters.ch2 import Response, Trajectory
from illustrated_agents.chapters.ch4 import Memory
from illustrated_agents.chapters.ch5 import Tools
```


class TinyAgent:
 """A minimal, modular, and educational agent framework."""

 def __init__(self, llm: LLM, memory: Memory, tools: Tools, planner: ReAct):
 self.llm = llm
 self.memory = memory
 self.tools = tools
 self.planner = planner

 self.trajectory = Trajectory()

 # Build system prompt with all components
 system_prompt = "You are a helpful assistant.\n\n"
 system_prompt += self.planner.prompt
 system_prompt += self.tools.prompt
 self.memory.add("system", system_prompt)

 def run(self, task: str) -> str:
 """Run the agent on a task."""
 self.memory.add("user", task)
 self.trajectory.initialize(task)

 # *Autonomy* loop
 for step in range(self.planner.max_steps):
 result = self._step()
 if result is not None:
 return result

 return "Max steps reached without completion."

 def _step(self) -> str | None:
 """Perform a single step."""
 # THOUGHT: Generate response and add to memory
 response = self.llm.generate(
 self.memory.get_messages(), tools=self.tools.schemas
 )
 self.memory.add(
 "assistant", response.content, tool_call=response.tool_call
 )
|
Chapter 6: Planning and Reflection

# Tool parsing
 response = self.planner.parse(response)
 response = self.tools.parse(response)

 # ANSWER: Stopping mechanism
 if self.tools.is_done(response):
 self.trajectory.add(response)
 return response.content

 return self._execute_action(response)

 def _execute_action(self, response: Response) -> None:
 """Execute a tool action."""

 # ACTION: execute tools
 result = self.tools.execute(response)

 # OBSERVATION: add tool results to memory and display
 role, observation = self.tools.observation(result)
 self.memory.add(role, observation)
 self.trajectory.add(response, observation)

 return None
We highlighted the sections that were added to indicate how little actually is needed
to go from a tool calling LLM to an autonomous agent.
Let’s try the agent out and ask it to use several tools to answer a given question. We
keep it simple and give it the add, multiply, and subtract tools:
```
from illustrated_agents.chapters.ch2 import LLM
from illustrated_agents.toolbox import add, multiply, subtract
```

# Gemma 3 12B (no native thinking or tool calling)
llm = LLM(model="gemma3:12b")

# Tools
tools = Tools()
tools.add_tool("add", add, "add(a: str, b: str)")
tools.add_tool("subtract", subtract, "subtract(a: str, b: str)")
tools.add_tool("multiply", multiply, "multiply(a: str, b: str)")

# Memory
memory = Memory()

# ReAct
react = ReAct(max_steps=10)

# Create agent
agent = TinyAgent(llm=llm, tools=tools, memory=memory, planner=react)

# Multi-step task with reasoning
agent.run("What is (4.6 + 6.685) x 4, and then subtract 3.14 from the result?")
Planning
|

This gives:
'42.0'
That is correct!
Although this is the correct answer, we’re much more interested in the full trajectory
of the agent. Did it correctly use the tools one at a time and decide to stop when it got
the answer? To find out, let’s print out the trajectory:
print(agent.trajectory.runs)
Which gives:
[
 {
 'query': 'What is (4.6 + 6.685) x 4, and then subtract 3.14
 from the result?',
 'steps': [
 Step(
 thought='First, I need to add 4.6 and 6.685.
 Then, I need to multiply the result by 4.
 Finally, I need to subtract 3.14 from that final result.',
 action={'tool': 'add', 'kwargs': {'a': '4.6', 'b': '6.685'}},
 observation='OBSERVATION: 11.285',
 answer=None,
 metadata=None
 ),
 Step(
 thought="Now that I've added 4.6 and 6.685, which resulted in
11. 285, I need to multiply this by 4.",
 action={
 'tool': 'multiply',
 'kwargs': {'a': '11.285', 'b': '4'},
 },
 observation='OBSERVATION: 45.14',
 answer=None,
 metadata=None
 ),
 Step(
 thought='I have now multiplied 11.285 by 4, obtaining 45.14.
 The final step is to subtract 3.14 from this result.',
```
 action={
 'tool': 'subtract', 'kwargs': {'a': '45.14', 'b': '3.14'}
```
 },
 observation='OBSERVATION: 42.0',
 answer=None,
 metadata=None
 ),
 Step(
 thought="I've completed all the necessary calculations.
 I added 4.6 and 6.685, multiplied the result by 4, and then
 subtracted 3.14. The final answer is 42.0.",
|
Chapter 6: Planning and Reflection

action=None,
 observation=None,
 answer='42.0',
 metadata=None
 )
 ]
 }
 ]
The trajectory shows that the agent took four steps:
add
The agent using the THOUGHT field to already make up a plan to execute, of
which the first was to add values together.
multiply
It reflects on its previous action and continues on with the next.
subtract
It reflects on its previous action and continues on with the next.
Returned the final answer
The agent saw that it calculated all the necessary steps and returned the final with
the final_answer tool.
With the ReAct framework, we have all the major components to create a truly
autonomous system that is capable of independently taking actions:
Reasoning LLM
The agent’s brain that is capable of advanced decision making and planning
Tools
Used to interact with the agent’s environment
Memory
Prevents the LLM from forgetting past actions and observations
Planning
Task decomposition to create plans and frameworks, such as ReAct, to create
autonomous behavior
When all these components are combined in one system, and that system is capable
of running continuously (imagine a while-loop or a for-loop), you have an agent! In
Figure 6-14, we visualize this system with an example of how these main components
could be built.
Planning
|



![Figure 6-14: Action sequencing allows the LLM to iteratively work on a problem until it](images/fig_06-14_Action_sequencing_allows_the_LLM_to_iter.png)

*Figure 6-14: Action sequencing allows the LLM to iteratively work on a problem until it*


Figure 6-14. Action sequencing allows the LLM to iteratively work on a problem until it
solves it
Where tools, as covered in Chapter 5, were all about single-turn processes, ReAct-like
frameworks turn them into multi-turn processes that allow agents to make complete
use of memory, tools, and planning.
Reason and Act with supervised fine-tuning
ReAct-like frameworks have been quite popular for performing action sequencing.
However, much like we explored in the tooling chapter, prompt engineering is only
the first step in steering an LLM’s behavior. Prompt engineering, much like is done
in ReAct, often requires few-shot prompting to get the correct behavior. This can
waste tokens in the context and be difficult to get right. FireAct is one of the first
methodologies to fine-tune an LLM on ReAct trajectories as a way to instill the ReAct
framework into a small LLM.7 The method is quite straightforward and consists of
two steps.
In step 1, an LLM (GPT-4) is used to generate different kinds of trajectories (e.g., CoT
and ReAct) based on questions from several datasets. The idea is that for different
questions, different methodologies might be needed to solve them. A straightforward
question that requires no agentic behavior would need only CoT-like inferencing,
whereas a potential multi-turn question would require a ReAct framework to solve
the problem. In Figure 6-15, you can see how various questions are processed
through different prompt templates (CoT, ReAct, and Reflexion, an extension of
ReAct that also includes feedback into the cycles)8 to generate their respective
7 Chen, Baian et al. 2023. “FireAct: Toward Language Agent Fine-Tuning,” arXiv, 2310.05915.
8 Shinn, Noah et al. 2023. “Reflexion: Language Agents with Verbal Reinforcement Learning,” Advances in
Neural Information Processing Systems, 36: 8634-8652.
|
Chapter 6: Planning and Reflection

trajectories. A trajectory for a question processed with ReAct, for example, would
contain sequences of thoughts, actions, and observations with a final answer.



![Figure 6-15: Supervised fine-tuning applied using ReAct trajectories by keeping only](images/fig_06-15_Supervised_fine-tuning_applied_using_ReA.png)

*Figure 6-15: Supervised fine-tuning applied using ReAct trajectories by keeping only*


Figure 6-15. Supervised fine-tuning applied using ReAct trajectories by keeping only
correct trajectories
These generated trajectories serve as the training data used for fine-tuning a smaller
LM. The trajectories, however, are first converted to all have the same ReAct format.
CoT, for instance, is turned into a one-round ReAct trajectory where the “thought”
is the intermediate reasoning and “action” that returns the answer. Note that it does
not have an observation since there is only one round. After formatting, this data is
then used to fine-tune a smaller model (Llama 2). The authors experimented with
both a full fine-tune as well as fine-tuning only a small part of the entire model
using Low-Rank Adaptation.9 From their experiments, fine-tuning on trajectories
outperformed the prompt-based ReAct framework. Perhaps more importantly, there
was no need to add few-shot examples to create the ReAct cycles, which makes
inference more efficient and prevents needlessly filling up the context.
Reason and Act with reinforcement learning
As we explored in Chapter 5, a limitation of SFT is that the LLM learns to mimic the
example data instead of adapting through experiences. It lacks the ability to explore
the environment, which tends to lead to suboptimal policies. In contrast, RL is a
powerful approach for enabling LLMs to refine their strategies by learning from the
feedback rather than simply mimicking behavior. By receiving rewards for actions
and refining its policy through trial and error, the model is encouraged to actively
explore its environment.
An interesting technique to explore ReAct through the lens of RL is Exploration-
based Trajectory Optimization (ETO).10 Compared to FireAct, ETO uses RL to
9 Hu, Edward J. et al. 2022. “LoRA: Low-Rank Adaptation of Large Language Models,” The Tenth International
Conference on Learning Representations.
10 Song, Yifan et al. 2024. “Trial and Error: Exploration-based Trajectory Optimization for LLM Agents,” arXiv,
2403. 02502.
Planning
|

encourage the LLM to learn and explore trajectories rather than attempt to mimic
behavior. ETO consists of two steps.
In step 1, the authors applied SFT, using ReAct data, on an LLM (Llama-2-7B Chat),11
to create a base agent that has inherent planning capabilities. The datasets used were
tasks that require multi-step planning and actions, such as ALFWorld, a text-based
environment mimicking typical households where agents are to perform specific
tasks, such as “clean a tomato and put it on the countertop” or “examine an alarm clock
with the desk lamp.”
The following is an example directly taken from ALFWorld, complete with actions:
You are in the middle of a room. Looking quickly around you, you see a safe 1,
a shelf 4, a drawer 2, a bed 1, a drawer 1, a shelf 5, a shelf 2, a side[Table 2: *description*],
a shelf 3, a drawer 3, a shelf 1, a side[Table 1: *description*], a desk 1, and a garbagecan 1.

Your task is to: examine an alarmclock with the desklamp.

> go to desk 1
You arrive at loc 8. On the desk 1, you see a pen 1, a bowl 1, a alarmclock 2,
a pencil 2, a pencil 3, a creditcard 3, a book 1, a alarmclock 3, a keychain 3,
and a book 2.

> take alarmclock 2 from desk 1
You pick up the alarmclock 2 from the desk 1.

> go to side[Table 2: *description*]
You arrive at loc 1. On the side[Table 2: *description*], you see a desklamp 1, and
an alarmclock 1.

> use desklamp 1
You won!
As Figure 6-16 shows, the initial model was fine-tuned using successful ReAct trajec‐
tories that include the task and the ReAct trajectory (see previous example). The
authors refer to SFT as behavior cloning, since this technique encourages the LLM
to mimic the behavior shown in the data instead of having it figure out the correct
answer on its own. In this context, SFT is therefore often referred to as imitation
learning.
Step 2 is an iterative process that switches between the exploration and training phases
(see Figure 6-17). During exploration, the base agent interacts with the environment
and attempts to solve the given tasks. From the ReAct trajectories that are generated
in this process, the failed trajectories are sampled. These are then paired with correct
trajectories that were previously collected for these tasks. During the training phase, the
pairs of trajectories are then used to further fine-tune the LLM using an RL algorithm,
11 Touvron, Hugo et al. 2023. “Llama 2: Open Foundation and Fine-tuned Chat Models,” arXiv, 2307.09288.
|
Chapter 6: Planning and Reflection

namely Direct Preference Optimization (DPO).12 During this fine-tuning, the authors
aimed to increase the likelihood of successful trajectories and decrease the likelihood
of failed trajectories. In other words, the agent learns contrastive information from the
failure/success trajectory pairs to update the RL policy.



![Figure 6-16: Supervised fine-tuning allows for mimicking the behavior as shown in the](images/fig_06-16_Supervised_fine-tuning_allows_for_mimick.png)

*Figure 6-16: Supervised fine-tuning allows for mimicking the behavior as shown in the*


Figure 6-16. Supervised fine-tuning allows for mimicking the behavior as shown in the
training data



![Figure 6-17: The two phases of RL in Exploration-based Trajectory Optimization (ETO):](images/fig_06-17_The_two_phases_of_RL_in_Exploration-base.png)

*Figure 6-17: The two phases of RL in Exploration-based Trajectory Optimization (ETO):*


Figure 6-17. The two phases of RL in Exploration-based Trajectory Optimization (ETO):
exploration and optimization
As we have explored several times before, using SFT followed by RL is a strong
learning paradigm for these models. By starting with SFT, the LLM learns the right
type of behaviors and formatting it should use. It gives the foundation it needs to then
explore and improve upon itself by using exploration and exploitation in RL.
12 Rafailov, Rafael et al. 2023. “Direct Preference Optimization: Your Language Model Is Secretly a Reward Model,”
Advances in Neural Information Processing Systems, 36: 53728-53741.
Planning
|

A major benefit of using SFT or RL (or both) is that there is no need for
ReAct via prompting. As covered previously, we used a specific prompting scheme
(THOUGHT/ACTION/OBSERVATION) to create this ReAct-like behavior. This was
possible because LLMs are great at instruction-following, so that we could steer the
model toward this specific behavior. However, it can be quite brittle and takes up a
fair bit of the system prompt. Training a model to do this natively is an answer to this.
Fortunately, we already created many of the needed components to use the native
ReAct capabilities of newer LLMs, Gemma 4 in particular.
The first step to do this is to choose a model that is actually capable of native
reasoning and tool calls. The model we explored in previous chapters is Gemma 4
E4B, so let’s choose that:
from illustrated_agents.chapters.ch2 import LLM

# Gemma 4 E4B (with native thinking and tool calling)
llm = LLM(model="gemma4:e4b", think=True)
We previously implemented loops of:
THOUGHT
A reasoning step about the current situation
ACTION
An action to execute (e.g., a tool)
OBSERVATION
A generated observation (typically the output of a tool)
However, with native tool calling, there is no need for explicit ACTION, and with
native reasoning, there is no need for explicit THOUGHT. We can replace what we
already have for each of them with the following:
THOUGHT
Replace with Response.reasoning and NativeReAct
ACTION
Replace with Response.tool_call and NativeTools
OBSERVATION
Replace with adding the output of a tool to memory using Response.observa
tion, which gives us the tool role
Since we already have NativeTools, we only need to create NativeReAct. In that
class, it essentially removes all behavior from the previously generated ReAct class.
With native tool calling and reasoning, there’s no need for a ReAct-specific prompt
or parsing it into THOUGHT/ACTION/OBSERVATION. Instead, all the behavior it
needs is to define the maximum number of steps:
|
Chapter 6: Planning and Reflection

from illustrated_agents.chapters.ch6 import ReAct

class NativeReAct(ReAct):
 """ReAct using native LLM reasoning instead of text-based parsing."""

 @property
```
 def prompt(self) -> str:
 return ""
```

```
 def parse(self, response):
 return response
```
What is left is a for-loop that uses native tool calling and reasoning each step. The
LLM decides what to use when and will stop only when there is no tool call. Since the
LLM was trained specifically using SFT and RL to perform ReAct, it already knows
how to do this.
This means that the model can choose at every step whether to perform:
Reasoning
As captured in Response.reasoning
Tool calling
As captured in Response.tool_call
Providing a final answer
As captured in Response.content
Because this is all we needed already, let’s demonstrate it with an example:
```
from illustrated_agents.chapters.ch4 import Memory
from illustrated_agents.chapters.ch5 import NativeTools
from illustrated_agents.chapters.ch6 import TinyAgent
from illustrated_agents.toolbox import add, multiply, subtract
```

# Register tools
tools = NativeTools()
tools.add_tool("add", add, "add(a: str, b: str)")
tools.add_tool("subtract", subtract, "subtract(a: str, b: str)")
tools.add_tool("multiply", multiply, "multiply(a: str, b: str)")

# Memory
memory = Memory()

# ReAct
react = NativeReAct(max_steps=10)

# Create agent
agent = TinyAgent(llm=llm, tools=tools, memory=memory, planner=react)

# Multi-step task with reasoning
agent.run("What is (4.6 + 6.685) x 4, and then subtract 3.14 from the result?")
Planning
|

Which gives:
'The result is 42.0.'
As before, the answer is correct. Your TinyAgent now does ReAct natively. To see
what happened behind the scenes, let’s explore the trajectory:
for index, step in enumerate(agent.trajectory.runs[0]["steps"]):
 print(f"-- Step {index+1} ---")
 if step.action:
 print(f"Tool: {step.action}")
 else:
 print(f"Answer: {step.answer}")
Which gives:
[
 {
 'query':
'What is (4.6 + 6.685) x 4, and then subtract 3.14
from the result?',
 'steps': [
 Step(
 thought='1. Calculate `(4.6 + 6.685)`.\n
2. Multiply the result of step 1 by `4`.\n3.
Subtract `3.14` from the result of step 2.
...
Since I cannot execute all steps at once,
I must start with the first step.',
 action={'tool': 'add', 'kwargs': {'a': '4.6', 'b': '6.685'}},
 observation='11.285',
 answer=None,
 metadata=None
 ),
 Step(
 thought='',
 action={
 'tool': 'multiply',
 'kwargs': {'a': '11.285', 'b': '4'}
 },
 observation='45.14',
 answer=None,
 metadata=None
 ),
 Step(
 thought='',
 action={
 'tool': 'subtract',
 'kwargs': {'a': '45.14', 'b': '3.14'}
 },
 observation='42.0',
 answer=None,
 metadata=None
|
Chapter 6: Planning and Reflection

),
 Step(
 thought='...
Since all calculations have been performed and the final result is available,
I can now answer the user\'s question with the final value.',
 action=None,
 observation=None,
 answer='The result is 42.0.',
 metadata={
 'model': 'gemma4:e4b', 'prompt_tokens': 325,
 'completion_tokens': 267
 }
 )
 ]
 }
]
Looking at the steps, you can see something similar to the ReAct loop we had before:
Step 1
Reasoning, tool call (add), and observation
Step 2
Tool call (multiply) and observation
Step 3
Tool call (subtract) and observation
Step 4
Reasoning and answer
Although similar to loops of THOUGHT/OBSERVATION/ACTION, it foregoes rea‐
soning when it calls the tool. Each LLM will have different behavior, but they do
generally boil down to these kinds of loops.
What We Built
TinyAgent/
├── agent.py ← Updated (Autonomy with a for-loop!)
├── llm.py
├── memory.py
├── planning.py ← New (Added the ReAct (Reason and Act) framework)
├── toolbox.py
├── tools.py
└── trajectory.py
The true foundation of your TinyAgent is now complete! By exploring both prompt-
based and native capabilities, you get to see how an agent actually works behind
Planning
|