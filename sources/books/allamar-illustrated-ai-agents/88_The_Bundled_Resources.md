---
title: "The Bundled Resources"
chapter_number: 88
page_start: 240
page_end: 241
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# The Bundled Resources

The body of the SKILL.md file contains the instructions relevant to its metadata. For
instance, the “meeting_notes” Skill would contain information on how to perform the
summarization of the transcripts and the things to look out for.
This information is only given to the agent when it asks for it. Imagine that it’s a
tool that the agent can call to provide the much-needed context for a given task.
The reason this information is not already given to the agent has to do with context
engineering. Some Skills have very long descriptions and tasks that might not be
relevant for your query. By only accessing the instructions when asked for, the agent
minimizes the amount of information it does not need. The SKILL.md is shown in
Figure 5-33.



![Figure 5-33: The anatomy of the SKILL.md file](images/fig_05-33_The_anatomy_of_the_SKILLmd_file.png)

*Figure 5-33: The anatomy of the SKILL.md file*


Figure 5-33. The anatomy of the SKILL.md file
The Bundled Resources
Skills can get quite large and unwieldy quickly. In our example of “meeting_notes”,
there can be instructions about different types of meetings. A 1:1 with your manager
requires a different structure than a 1:1 with one of your colleagues or a 1:1 with your
employee. The same applies to calls with external partners, team meetings, etc.
Instead of trying to put everything into the SKILL.md file, we can bundle additional
files within the Skills directory and reference them from the SKILL.md file. These
files can be anything and don’t require anything other than that the agent should be
able to access them. Typical files are Python files for executing specific functions and
markdown files for additional instructions. As such, the agent can decide to load this
information when needed but it’s necessary to use the Skill. This additional layer of
activation is shown in Figure 5-34.
|
Chapter 5: Tool Usage, Learning, and Protocols



![Figure 5-34: The agent can choose to run additional files if needed. Those files can](images/fig_05-34_The_agent_can_choose_to_run_additional_f.png)

*Figure 5-34: The agent can choose to run additional files if needed. Those files can*


Figure 5-34. The agent can choose to run additional files if needed. Those files can
provide additional context or act as helper functions.
In the Skill’s directory, only a SKILL.md is needed. However, as context grows and
more information is needed for certain tasks, additional files can be added that the
agent loads only when needed:
meeting_notes/
├── SKILL.md
├── scripts/
│ └── extract_action_items.py
└── formats/
 ├── one_on_one_manager.md
 ├── one_on_one_colleague.md
 ├── one_on_one_report.md
 ├── team_meeting.md
 └── external_call.md
Progressive disclosure in the form of these three layers helps keep the amount of
context used to a minimum, as shown in Table 5-1.
Skills
|