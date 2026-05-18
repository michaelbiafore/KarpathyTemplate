---
title: "Late-Bound Sagas: Why Your Agent Is Not an LLM in a Loop"
source: "https://medium.com/agentspan/late-bound-sagas-why-your-agent-is-not-an-llm-in-a-loop-a8c50731c551"
author:
  - "[[Viren Baraiya]]"
published: 2026-04-13
created: 2026-04-25
description: "More"
tags:
  - "clippings"
---
Here is how a lot of agents are still written today:

```hs
def run_agent(task):
  state = State(task)
  while not state.is_terminal():
    intent = llm.plan(state)
    result = execute_tool(intent.tool)
    state.append(result)
  return state.final_answer()
```

Here is how it *should* be written:

```hs
@agent
def run_agent(task):
  while not done(task):
    intent = yield plan(task)
    result = yield execute(intent)
    task = yield append(task, result)
```

> *The syntax change is small. The runtime boundary is not. In the first version, your process owns execution state. In the second, the runtime does.*

## An agent is a saga that the model writes as it runs.

Not a loop the model sits inside. That distinction — saga vs. loop — is the difference between a demo and a system you can run a business on. It has a name: the **Late-Bound Saga**. The rest of this post is what it is, why you need it, and what your code looks like on the other side.

*I’ve spent the last decade building* [*Conductor*](https://github.com/conductor-oss/conductor)*, the durable-execution runtime we open-sourced in 2016 at Netflix, which today runs long-lived workflows at a lot of companies you’ve heard of. This post is what I’ve learned about how that kind of runtime has to change for agents — and why the shape of the answer is not what the durable-execution lineage has been building for the last ten years.*

## Durability is not continuity

> *My agent runs in a pod. I checkpoint to Postgres after every tool call. If the process dies, Kubernetes brings it back. I have durability. What else is there?*

Your agent calls Stripe to charge a customer $4,000. The call succeeds. Before your code can write the row that says “Stripe call complete,” the pod gets evicted — node pressure, a rolling deploy, an OOM from a context window that grew larger than you planned. Kubernetes restarts the pod. Your agent reads the last checkpoint, which says “about to call Stripe.” It calls Stripe again. You’ve just charged the customer $8,000.

Postgres did its job. Kubernetes did its job. Your checkpoint did its job. You still double-charged the customer.

The bug isn’t that anything failed. Durability means your data survives. Continuity means your program counter survives. The runtime knows which instruction you were about to execute, determines whether the side effect already ran, and avoids executing it again — no matter how many times the process dies between attempting it and recording it.

A pod plus a database gives you the first. To get the second, something other than your application code has to own the instruction pointer. That something is a runtime — a real one, not a library you import from inside a loop you wrote yourself.

## Your demo worked because it was twelve steps long

**A 200-step agent run succeeds 13% of the time.** Not because the model is wrong. Because of math.

*The exact number depends on independence, retries, and step shape. The point is not the precise percentage. The point is that long runs punish naïve control flow.*

Suppose every step succeeds with 99% reliability — optimistic, since it assumes your model never times out, your tools never rate-limit, and your network never blips. A 20-step workflow succeeds 81% of the time. A 50-step workflow, 60%. A 100-step workflow, 36%. A 200-step workflow — what a serious multi-agent task looks like once you count sub-agent calls — succeeds 13% of the time.

Seven out of eight runs fail. Because you stacked enough 99%s on top of each other that the floor fell out from under them. The only tool the loop has to respond is to start over from the beginning, which doubles the token bill and reintroduces the same probability distribution on the retry.

## The LLM should not execute anything

The fix is the strictest possible separation between two planes.

**The LLM plans.** It is a pure function from state to intent, no file handles, no network, no ability to mutate anything. It looks at the world and emits a description of what it would like to happen next. That description is data, not action. The LLM cannot make Stripe calls because the LLM cannot make any calls at all (not that the LLM cannot, but it *must not*).

**The runtime executes.** It receives intents from the planning plane, writes them to a persistent ledger *before* doing anything with them, performs the side effect against the real world, writes the result back, and only then asks the LLM what to do next. The ledger — not process memory — is the source of truth.

When an agent needs to delegate to another agent, it doesn’t call a function. It yields an intent and returns to the pool. The runtime catches the intent, dispatches the work, and wakes the LLM back up only when there’s a result to look at.

> **The LLM proposes; the runtime disposes.**

**An agent runtime has to provide at least four things a loop cannot:**

### a. Intent ledger

Records every proposed action before it executes, so “did this happen?” is answerable from outside the agent’s process.

### b. Effectively-once execution of side effects

A crash between proposing an action and recording its result never causes the action to run twice.

### c. Suspension and resumption across process boundaries

An agent waiting on a human, a webhook, or another agent consumes zero compute and survives infrastructure churn.

### d. Out-of-band signal delivery

Signaling a running or suspended agent, so a supervisor, a human, or another agent can inject new context without killing the workflow.

A Kubernetes pod gives you none of these. A Postgres checkpoint gives you a weak version of the first one and nothing else.

A durable-execution runtime such as Conductor, Temporal, and the rest of the lineage gives you all four. If you’re building a long-lived workflow today, one of these is almost certainly the right substrate. The question this post is about is what changes when the thing producing the steps is not a programmer at commit time but a language model at runtime. That is not a critique of durable execution. It is an argument that durable execution is the right *substrate* for agents, and that agents need a layer on top of it that the existing frameworks weren’t designed to provide.

The interesting question is whether you can have all four properties *and* keep the LLM’s freedom to decide, at runtime, what the workflow even looks like. The answer is the **Late-Bound Saga**.

## The Late-Bound Saga: a workflow the LLM writes one edge at a time

A Late-Bound Saga is a workflow whose execution graph does not exist when the workflow starts. The LLM synthesizes it edge by edge at runtime, and each edge is committed to a durable ledger at the moment it is proposed — *before* it executes. The graph is append-only. The LLM doesn’t traverse a pre-built graph; it extends the graph by one node at a time, with the runtime as witness and executor.

The order matters. Not: *LLM decides → tool executes → write down what happened.* Instead: *LLM decides → write the intent → tool executes → write the result → LLM sees the result.* Four ledger writes per step, bracketing the side effect on both sides. The bracket is the entire game, because it is the only structure that lets a recovering process answer “did this already happen?” without asking the outside world.

The *late-bound* half of the name gives you the dynamism — the LLM decides the workflow as it goes. The *saga* half gives you the durability — every decision is a transaction with a compensation, written down before it runs. **You don’t have to choose between the two. The whole point of the pattern is that you don’t.**

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Xdel0GVjzZTsAAD6g9TF5g.png)

## What it looks like in motion

The agent’s task: *find the three best candidates for the senior backend role, and schedule first-round interviews with each.*

**Step 1 — the LLM proposes a search.** The runtime asks the LLM for an intent. It proposes:

*search\_candidates(role=”senior backend”, limit=20).*

The runtime writes the intent, executes the search in a worker, writes the twenty results back. One node in the ledger. One edge in the graph.

**Step 2 — the fan-out.** The runtime asks again. The LLM proposes twenty parallel enrich\_candidate calls. The runtime writes twenty pending intents, dispatches twenty workers — possibly in twenty languages on twenty machines — and waits for each to report back. The graph now has twenty-one nodes and twenty edges, none of which existed sixty seconds ago.

**Step 3 — the saga goes to sleep for three days.** The LLM ranks, selects three, and proposes three request\_interview\_slot calls. The runtime dispatches the emails, writes the three pending nodes, and **suspends the entire saga to disk.** The agent’s process exits. There is nothing running. No pod sitting idle burning compute. The saga is a row in a database and a handful of pending webhook subscriptions.

Three days later, a recruiter clicks “accept.”

The webhook fires.

The runtime looks up the saga, writes the result, and asks the LLM for the next intent.

The LLM, which has no idea three days have passed because it has no concept of time, proposes a calendar invite. The saga continues. To the LLM, no time has passed. To your infrastructure bill, no compute was consumed.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*23M6az2xavpF1YLZ07ZAlQ.png)

## Signals are cache invalidation for intent

**Now suppose on day two, a supervisor agent tells the saga to abort.** In the loop model, there is no agent to tell — the process exited days ago.

In the Late-Bound Saga model, the runtime *is* the inbox. You send a signal to the saga’s ID. The runtime writes the signal, wakes the saga, and asks the LLM what to do. The LLM sees the cancellation, proposes a compensation sequence — 1) withdraw the pending requests, 2) send polite declines, 3) terminate — and the runtime executes each step.

Think of a signal as cache invalidation for intent. The agent’s plan is a cache. The world is the source of truth. When the world changes, the cache has to be invalidated and rebuilt. In a volatile loop you can’t, because the cache *is* the process and the process is blocked on a *requests.get*. In a Late-Bound Saga, the cache is the ledger, the invalidation is a ledger write, and the rebuild is the next call to the LLM.

Same mechanism, every other out-of-band event: a rate limit, a hallucination flagged by an evaluator, a budget cap, a human typing “stop, use staging instead.”

None of these are tool calls. All of them are signals, and a runtime that doesn’t have a signal primitive isn’t a runtime — it’s a job queue with extra steps.

## The runtime model, built into Agentspan

[Agentspan](https://github.com/agentspan-ai/agentspan) sits on top of Conductor, the durable-execution runtime I open-sourced at Netflix in 2016. Conductor treats workers as protocol clients rather than SDK-bound processes, which means your planner can run in Python where the LLM ecosystem lives, your high-throughput data tool can run in Go, your legacy underwriting model can stay in the JVM where it has lived for fifteen years, and none of them have to share a process or a language. [Agentspan](https://github.com/agentspan-ai/agentspan) is the layer that turns that substrate into an agent runtime.

Here is the candidate-search saga, in Agentspan, in the smallest form I can write it:

```hs
from agentspan import agent, tool

@tool
def search_candidates(role: str, limit: int): ...

@tool
def enrich_candidate(candidate_id: str): ...

@tool
def req_interview_slot(candidate_id: str, recruiter_id: str): ...

@agent(model="claude-sonnet-4-6")
def hire_for_role(role: str, recruiter_id: str):
    """
    Find the three best candidates for the given role and
    schedule first-round interviews with each of them.
    """
```

That is the user-level program. The rest of the machinery lives where it belongs: in the runtime. No loop. No state machine. No explicit call to the LLM. When you invoke *hire\_for\_role(“senior backend”, “rec\_42”)*, the runtime starts a saga, calls the LLM with the task and the available tools, writes the proposed intent to the ledger, dispatches the worker, writes the result back, and calls the LLM again. If the process dies, the saga survives. If it waits three days for a recruiter, the runtime suspends it to disk and the wait costs nothing. If a supervisor sends cancel(saga\_id), the runtime delivers it as a signal and the LLM gets a chance to compensate.

> **None of these are features bolted on top of the decorator. They are what the decorator means.**

And because every intent and every result is in the ledger, you also get the thing every senior engineer who has ever debugged a non-deterministic system at 3am actually wants: **distributed tracing for cognition.** Point-in-time state inspection. Deterministic replay from any node. The hardest question in debugging an agent — *what did it know, and when did it know it? —* has an answer, and the answer is a database query.

## The Monday morning experiment

Open the agent you’re building at work. Find the loop. Every agent has one. Answer three questions, on paper, honestly.

**One.** If the process dies in the middle of the third iteration, kill -9, no warning — what happens to any side effect that iteration had already started? Not what *should* happen. What actually happens.

**Two.** If a human or another agent needs to tell this loop to stop and reconsider — “send a message from outside” — how does the message get in? If the answer is “it can’t,” you don’t have signals at all.

**Three.** Six months from now, your agent does something weird at 3:14am on a Tuesday. Where do you go to find out exactly what it saw and exactly what it decided? If the answer is “the logs,” check whether your logs contain the LLM’s full input and output for every step in a form you can replay against a different model. They don’t.

If any of the three made you flinch, the flinch is the thing this post is about. The flinch is the gap between durability and continuity, between a loop and a saga, between an LLM that executes and an LLM that proposes. The runtime is the thing on the other side of the flinch.

An agent is not an LLM in a loop. An agent is a saga the model writes as it runs. The loop was a hack we built while we were waiting to figure out what agents actually were. We’ve figured it out. It’s time to write the runtime.

*Code:* [*github.com/agentspan-ai/agentspan*](https://github.com/agentspan-ai/agentspan)*.*

*Agentspan is open-source and is looking for builders and hackers. Send your PR!*