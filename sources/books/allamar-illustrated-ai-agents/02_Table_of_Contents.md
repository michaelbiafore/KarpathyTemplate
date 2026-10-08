---
title: "Table of Contents"
chapter_number: 2
page_start: 7
page_end: 12
---
# Table of Contents

Table of Contents
Preface. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xi
Part I.
The Anatomy of an AI Agent
1. Introduction. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
What Is an AI Agent? 4
Large Language Models 6
Reasoning Large Language Models 7
Augmenting the Large Language Model 10
An Agentic System 16
Specializations 20
Multi-Agent Collaboration 21
The Multi-Modal Agent 22
The Coding Agent 24
The TinyAgent 24
Summary 29
2. Large Language Models. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31
Part 1: What You Should Know About Large Language Models 33
Input and Output Tokens 33
From Language Modeling to Powering Agents 34
The TinyAgent 36
Training a Large Language Model 45
The Transformer Architecture 51
Part 2: A Deeper Dive Into Large Language Models 64
How Self-Attention Works 64
KV-Caching Revisited 68
v

More Efficient Self-Attention 70
Mixture of Experts 73
Summary 80
3. Reasoning Large Language Models. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 83
The Paradigm Shift from Train-Time Compute to Test-Time Compute 86
Train-Time Compute Versus Test-Time Compute 86
Scaling Laws 89
Categories of Test-Time Compute 94
Reward Models 96
Prompt Engineering 98
Search Against Verifiers 102
Self-Consistency 104
Best-of-N Samples 106
Modifying Proposal Distribution 109
Supervised Fine-Tuning 111
Reinforcement Learning 114
Native Reasoning 120
Emerging Directions in Reasoning Research 122
Reasoning in Multi-Modal LLMs 122
Efficient Reasoning 125
Reasoning in Latent Space 127
Summary 130
4. Memory. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 131
Types of Memory 133
Short-Term Memory 135
Conversation Memory 135
Trimming 140
Summarization 142
Long-Term Memory 145
Retrieval-Augmented Generation 145
Agentic Retrieval-Augmented Generation 154
Context Engineering 161
Context Engineering for Multi-Agent Systems 166
Optimizing the Context 166
Context As the Specification 172
Summary 173
5. Tool Usage, Learning, and Protocols. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 175
Tool Usage 177
Tool Creation 179
vi
|
Table of Contents

Tool Definition 180
Tool Selection 185
Tool Calling 186
Tool Output Processing 188
TinyAgent with Tools 191
Tool Learning 195
In-Context Learning 196
Supervised Fine-tuning 197
Reinforcement Learning 201
TinyAgent with Native Tool-Calling Capabilities 206
Model Context Protocol 212
Core Components 215
The MCP Flow 216
Skills 218
The SKILL.md 219
The Bundled Resources 220
Summary 222
6. Planning and Reflection. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 223
Planning 224
Task Decomposition 225
Action Sequencing 232
Agents That Continuously Improve 250
Reflection 250
Self-Improvement 254
Summary 260
7. Evaluating Agents. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 261
Public Benchmarks and Leaderboards 262
Coding and Software Engineering 263
Tool Use 264
Software and Computer-Use Environments 264
Real-World Task Completion 264
Reasoning and Knowledge 265
Other Groups of Benchmarks 265
Reading Benchmark Scores Critically 266
Outcome Evaluation: Did the Agent Get the Right Output? 268
Human Evaluation 268
Automated Evaluation 270
Trajectory Evaluation: Did It Get There the Right Way? 282
Reliability: Does It Succeed Every Time? 283
Measuring Capability with pass@k 283
Table of Contents
|
vii

Measuring Reliability with pass^k 286
Safety: Does It Avoid Harm? 288
Building Your Own Evals 288
Summary 289
Part II.
Specialized Agents
8. Multi-Agent Systems. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 293
The Multi-Agent System 294
Orchestrating Agents 297
Patterns 297
General-Purpose Frameworks for Collaborative Task-Solving Patterns 303
Communication Protocols 307
Agent Society 312
Emotional Intelligence 312
Simulations 315
Interactive Simulacra of Human Behavior 316
Deep Research Agents 321
Toward an AI Co-Scientist 322
Agent Laboratory 323
Summary 327
9. Multi-Modal Understanding. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 329
What Are Multi-Modal LLMs? 330
Encoding Modalities 333
Text 334
Images 337
Audio 340
Video 346
Many-Modality 356
Connecting Modalities 359
Projection-Based Connector 362
Query-Based Connector 365
Fusion-Based Connector 368
Advantages and Disadvantages 371
TinyAgent 371
Summary 375
10. Code Agents and Code LLMs. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 377
Users and Builders of Code Agents and Large Language Models 377
Building Code Agents 380
viii
|
Table of Contents

Code Agents to Serve Non-Coders 380
Code Tools 381
Context Management 391
Code Agents for Software Engineering 397
Task-Specific Workflows 400
Building Code LLMs 410
Summary 414
Afterword. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 417
Index. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 419
Table of Contents
|
ix