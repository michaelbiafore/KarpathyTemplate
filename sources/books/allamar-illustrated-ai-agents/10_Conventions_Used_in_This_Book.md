---
title: "Conventions Used in This Book"
chapter_number: 10
page_start: 16
page_end: 16
---
# Conventions Used in This Book

into a full agent. Part 1 closes with Chapter 7 on evaluation: how to judge agents
by their outcomes and their trajectories, and how to think about reliability and
safety, because evaluating an agent means evaluating an entire system, not just a
model.
Part 2: Specialized Agents
In Part 2, we explore how agents specialize. Chapter 8 covers multi-agent sys‐
tems, where several specialized agents collaborate, and the architectures that
orchestrate them. Chapter 9 covers multi-modal agents, which perceive and
generate more than text, letting them see images, watch video, and speak. We end
the book with Chapter 10 on coding agents and the code LLMs that power them,
arguably the most impactful agent use case at the time of this writing, and the
one reshaping the craft of software engineering itself.
Note that each chapter can be read independently, so feel free to skim chapters you
are already familiar with. We have also provided a bibliography and a glossary as
online-only resources in the book repository.
Hardware and Software Requirements
Running LLM-backed agents can be a compute-intensive task, but a strong local
machine is not required for this book. All examples are made to run in Google
Colaboratory, or “Google Colab” for short, which at the time of writing provides
free access to an NVIDIA T4 GPU. Every chapter has a companion notebook in the
book’s repository that opens directly in Colab, and you have the option of running
everything either locally or in the cloud without any additional costs involved.
All code, notebooks, and additional material are available in this book’s repository.
There you will also find the TinyAgent source as the illustrated-agents package, along
with a quick-start guide in the setup folder for installing everything locally if you
prefer to run the examples on your own machine.
API Keys
The code examples in this book run on open source models by default. A few
examples are demonstrated using proprietary models instead; for those, you will need
to create an account and an API key with the relevant provider. We have strived to
include only proprietary examples that can run on free tiers. Note that these free tiers
often have rate limits which may change over time.
Conventions Used in This Book
The following typographical conventions are used in this book:
xiv
|
Preface