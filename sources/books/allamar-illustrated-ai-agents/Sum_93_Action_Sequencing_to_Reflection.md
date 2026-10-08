# Action Sequencing to Reflection (Chapters 93-95)

## Action Sequencing

Least-to-most and plan-and-solve prompting decompose a problem into subtasks, but they stop short of what an agent needs: once the agent has picked its subgoals, it must choose an efficient *sequence* of actions that carries it from the current state to the goal state. A coding agent that skips reading the codebase, for example, wastes steps and creates redundancy. Action sequencing is the discipline of producing that sequence and then revising it as new information arrives.

The dominant technique is ReAct (Reason and Act). Before ReAct, reasoning (chain-of-thought) and acting (tool use, e.g. Toolformer) were separate capabilities, which made iteration hard. ReAct interleaves them.

![Figure 6-11: ReAct fuses reasoning and acting, allowing the LLM to produce a reasoning](images/fig_06-11_ReAct_fuses_reasoning_and_acting_allowin.png)

*Figure: One ReAct loop — the LLM emits a reasoning trace, fires an action into the environment, and feeds the resulting observation back into itself.*

Each turn the model is prompted to emit three separated fields: THOUGHT (reasoning about the situation), ACTION (a tool call), and OBSERVATION (reasoning about the result). Few-shot examples are usually added so the format holds.

![Figure 6-13: Two cycles of THOUGHT/ACTION/OBSERVATION using the ReAct](images/fig_06-13_Two_cycles_of_THOUGHTACTIONOBSERVATION_u.png)

*Figure: Two concrete cycles for "create a new feature for my codebase" — cycle 1 reads the repo, cycle 2 asks the user to clarify, each closing with an observation that seeds the next thought.*

The book's TinyAgent gets a `ReAct` planner class holding only three things: `max_steps` (a loop guard), a `.prompt` property describing the format and the `final_answer` completion tool, and a `.parse` regex that splits THOUGHT/ACTION into `Response.reasoning` and `Response.content`. The agent change is almost trivial — the autonomy loop is a `for` loop over `max_steps`. On "(4.6 + 6.685) x 4, minus 3.14" the agent correctly chains add, multiply, subtract and then calls `final_answer` with 42.0. With a model that has native reasoning and tool calling (Gemma 4 E4B), the `NativeReAct` subclass strips the prompt and parser entirely and behaves the same way.

![Figure 6-14: Action sequencing allows the LLM to iteratively work on a problem until it](images/fig_06-14_Action_sequencing_allows_the_LLM_to_iter.png)

*Figure: The complete agent — a reasoning LLM backed by memory (RAG), tools (MCP), and planning (ReAct), cycling action and feedback with the environment until the goal is reached.*

Prompt-based ReAct is brittle and eats context, so two training routes replace it. FireAct generates CoT/ReAct/Reflexion trajectories with GPT-4, reformats them all as ReAct, keeps only the correct ones, and fine-tunes a smaller model (Llama 2, full or LoRA) — outperforming prompted ReAct with no few-shot examples. ETO (Exploration-based Trajectory Optimization) goes further: SFT first (behavior cloning on successful ALFWorld trajectories), then an RL loop.

![Figure 6-17: The two phases of RL in Exploration-based Trajectory Optimization (ETO):](images/fig_06-17_The_two_phases_of_RL_in_Exploration-base.png)

*Figure: ETO alternates an exploration phase that samples the base agent's failed trajectories with a training phase that pairs them against correct ones and applies DPO.*

## Agents That Continuously Improve

Rather than depending solely on training phases or reward models, agents can use self-generated feedback loops to improve while they act. Feedback keeps them out of local minima and points toward better solutions — though not all feedback is equal, and genuine self-improvement is hard for models that are static at inference time.

## Reflection

Environment feedback is reactive ("I did X, the world returned Y"); *reflection* is the internal counterpart, where the LLM criticizes its own output and process, optionally aided by external sources. Both techniques here are prompt-based and easy to implement.

Self-Refine has one model generate an answer, critique it, and revise — acting as its own editor until a step limit or LLM-judged stopping criterion fires.

![Figure 6-18: The main steps of self-refine where the same LLM continuously refines](images/fig_06-18_The_main_steps_of_self-refine_where_the.png)

*Figure: The Self-Refine cycle — the same LLM generates, refines, critiques its refinement, and loops the feedback back in.*

Reflexion is the agentic version, splitting the work across three roles: an Actor LLM (a ReAct agent), an Evaluator LLM that scores the trajectory, and a Self-Reflection LLM that turns trajectory plus score into specific verbal feedback.

![Figure 6-20: The Reflexion process uses separate LLM roles (Actor, Evaluator, Self-](images/fig_06-20_The_Reflexion_process_uses_separate_LLM.png)

*Figure: Reflexion's wiring — short-term memory holds the trajectory, the Evaluator's internal feedback and the environment's external feedback meet in the Self-Reflection LLM, whose reflective text lands in long-term memory for the Actor.*

Related approaches include CRITIC, which revises output using external tools such as search. All remain prompt-level guidance rather than behavior baked into weights, which motivates the fine-tuning techniques that follow.
