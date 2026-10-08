---
title: "Reward Models"
chapter_number: 42
page_start: 116
page_end: 117
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Reward Models



![Figure 3-18: Modifying proposal distribution (left) is typically achieved by training the](images/fig_03-18_Modifying_proposal_distribution_left_is.png)

*Figure 3-18: Modifying proposal distribution (left) is typically achieved by training the*


Figure 3-18. Modifying proposal distribution (left) is typically achieved by training the
model, which represents learned behavior. Search against verifiers (right) is typically
achieved by generating many outputs, scoring using a reward model (verifier), and
choosing the best output.
Reward Models
Reward models are used to score the LLM-generated reasoning traces and answers.
They can be many things but are generally (fine-tuned) LLMs or rule-based systems.
LLMs can be used to judge the reasoning traces, whereas rule-based systems, like unit
tests, can be used to test the output.
We will explore two types of verifiers for both methods of test-time compute:
- Outcome Reward Model (ORM)
•
- Process Reward Model (PRM)
•
As the name implies, the Outcome Reward Model judges only the outcome of the
LLM and ignores any reasoning steps. As shown in Figure 3-19, the number of
reasoning traces created and their quality is not taken into account when judging the
quality of the final answer.
The Process Reward Model tends to focus on the processes that lead to a given
outcome. In the context of reasoning models, those processes are the reasoning steps
leading to the final answer. Figure 3-20 demonstrates how one or more PRMs can
judge the quality of the reasoning steps. Note that the final answer is not always taken
into account, and that often a mix between a Process Reward Model and Outcome
Reward Model might be preferred.
|
Chapter 3: Reasoning Large Language Models



![Figure 3-19: An ORM judges only the output and not intermediate reasoning steps](images/fig_03-19_An_ORM_judges_only_the_output_and_not_in.png)

*Figure 3-19: An ORM judges only the output and not intermediate reasoning steps*


Figure 3-19. An ORM judges only the output and not intermediate reasoning steps



![Figure 3-20: A PRM judges only the intermediate reasoning steps and not the output](images/fig_03-20_A_PRM_judges_only_the_intermediate_reaso.png)

*Figure 3-20: A PRM judges only the intermediate reasoning steps and not the output*


Figure 3-20. A PRM judges only the intermediate reasoning steps and not the output
To make these reasoning steps a bit more explicit, let’s use the example we saw at
the beginning of this chapter. The question we ask the reasoning LLM is: “I saw 6
flamingos. 2 flew away. 1 hid behind a tree. How many can I see?” As shown in
Figure 3-21, reasoning steps are the intermediate thinking steps of the reasoning
LLM. How many reasoning steps it has will depend on the specific model because
some are more verbose than others.
Note how each Process Reward Model scores a specific part of these reasoning steps
and aggregates the scores. Although it starts out strong, reasoning step 2 makes
a mistake and is scored low by the PRM. However, the very next reasoning step
corrects its mistakes, which is scored highly by the PRM.
Categories of Test-Time Compute
|