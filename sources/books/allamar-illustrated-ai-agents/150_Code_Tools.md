---
title: "Code Tools"
chapter_number: 150
page_start: 401
page_end: 410
part: "Part II. Specialized Agents"
---
# Code Tools

B) The agent has to find the files itself
A more advanced scenario is if the tool is a command line and the agent
needs to write the code to find and retrieve the file (or files) first. Tools like
this would operate on a virtual machine with access to a filesystem. The code
generated here would use command-line tools to search and navigate the
filesystem.
C) The data is in a database
In a scenario like this, the agent can be connected to a SQL tool giving it
access to one or multiple databases. The agent would need to write the SQL
code and send it to the tool to execute to retrieve and transform the required
data.
2. Creating the plot
Once the agent has the data it needs, it will need to write the code to plot it, and
return the resulting plot.
3. Troubleshooting
We cannot assume that everything will go smoothly. Maybe the data is not
available, maybe the query the model wrote contains mistakes or is based on
limited information. So, it’s important to plan for the different possible failure
cases the agent may face. In a lot of cases, if we get an error from the execution
environment and send it back to the LLM, it can recover on the next step. This
is the ReAct loop from Chapter 6 doing its job: the error is just another observa‐
tion, and the model reasons about it and tries a corrected action. However, we
shouldn’t rely on that alone. The more we plan for specific failure cases, the better
the end user experience will be.
Notice that in this example the user doesn’t necessarily see or interact with any of the
code. This is one of the major levers of power for systems like this that dramatically
increase the number of people it can be useful for.
Code Tools
Code tools are a pivotal component in how we tie an LLM to a software system. The
model decides what it wants to do, and the tool carries that action out against a real
environment: running code in a sandbox, executing a shell command, or querying a
database. In Figure 10-4, we see another plotting request, but this time we see how
specific code tools (a SQL tool and a Python execution tool) tie the LLM to the
appropriate environments.
Building Code Agents
|



![Figure 10-4: A code agent resolving a request via a two-step trajectory, employing](images/fig_10-04_A_code_agent_resolving_a_request_via_a_t.png)

*Figure 10-4: A code agent resolving a request via a two-step trajectory, employing*


Figure 10-4. A code agent resolving a request via a two-step trajectory, employing
distinct tools at each step
Let’s look at a few more of the key examples of code tools as these help us understand
the design space for possible code agents.
File manipulation tools
Some of the first tasks a code agent needs to handle are reading, searching, and edit‐
ing files. These can be implemented as distinct tools, each with its own permissions
and checks. This enables the agent to find relevant files, edit them, create new files,
and navigate through filesystems. These tools are often, but not always, wrappers
around command-line tools.
|
Chapter 10: Code Agents and Code LLMs

Common file manipulation tools to give code agents include:
- Read entire file (e.g., cat).
•
- Read a section of a file (to better manage model context when dealing with long
•
files) (e.g., sed, head, tail).
- List files in a directory (e.g., ls).
•
- Pattern-match file names that follow a certain pattern (e.g., glob).
•
- Search the contents of files (e.g., grep).
•
Code interpreter sandbox environment
A code interpreter or sandbox is a code execution environment that is a little more
restricted than a full virtual machine. These restrictions are important from a security
point of view because LLM-generated code is not guaranteed to be safe. An agent
could delete important files, corrupt a system, or share private data with external
third parties. This can happen either through intended malicious attacks (possibly
utilizing prompt injection), or as well-meaning or naive agent actions.
These sandboxes have to be defined with certain limited resources (e.g., in memory,
processor, or disk space). They often are ephemeral so that:
1. A fresh environment is created for each user or session. This makes the initial
state of the sandbox predictable (e.g., in terms of what packages are available, for
example). This also helps ensure the data of user A is separated from the agents
of user B.
2. Data is deleted at the end of the session and there’s no expectation of data
persistence.
For security reasons, these sandboxes are often restricted in terms of which com‐
mands can run, and you can decide whether the code running inside has internet
access. Every such restriction trades convenience for security: it’s tempting to grant
broad access so the agent never gets stuck, but each capability you add widens what a
mistake or an attack can do. We’ll come back to how to navigate that balance when we
cover command-line tools and the principle of least privilege.
Code sandboxes have become a part of commercial services from LLM providers and
agent providers. You may have already used a tool that utilized a code interpreted on
your behalf without you knowing it. Gemini, for example, provides a dedicated code
execution tool that can be accessed via its API. At the time of the writing, this can be
accessed with a command like we see in the following code example.
Building Code Agents
|

You don’t need any hosted service to follow this chapter: the TinyAgent we build later
runs on a local open model and executes code on your own machine:
## install in the terminal with:
## pip install google-genai

## requires a Gemini API key from Google AI Studio (free tier, no credit card)
## note: free-tier prompts may be used to improve Google's products,
## so don't send anything sensitive
## set it in your environment, e.g.:
## export GEMINI_API_KEY="..."

```
from google import genai
from google.genai import types
```

# Alternatively, we can pass the API key here. genai.Client(api_key="<api_key>")
client = genai.Client()

system_message = """
You are a personal math tutor. When asked a math question,
write and run code using the code execution tool to answer the question.
"""

prompt = "We sell 5,000 units a month at $29 each, and each unit costs
$14 to make. If we cut the price 10% and that lifts volume 10%, what's the change
in monthly profit?"

# See the latest available models at
https://ai.google.dev/gemini-api/docs/models

resp = client.models.generate_content(
 model="gemini-2.5-flash",
 contents=prompt,
 config=types.GenerateContentConfig(
 system_instruction=system_message,
 tools=[types.Tool(code_execution=types.ToolCodeExecution())],
 ),
)
Inspecting the response object shows the model has written the code:
# Original Scenario
original_units = 5000
original_price = 29
cost_per_unit = 14

original_revenue = original_units * original_price
original_cost_of_goods = original_units * cost_per_unit
original_profit = original_revenue - original_cost_of_goods

print(f'{original_profit=}')

# New Scenario
|
Chapter 10: Code Agents and Code LLMs

price_cut_percentage = 0.10 # 10%
volume_lift_percentage = 0.10 # 10%

new_price = original_price * (1 - price_cut_percentage)
new_units = original_units * (1 + volume_lift_percentage)

new_revenue = new_units * new_price
new_cost_of_goods = new_units * cost_per_unit
new_profit = new_revenue - new_cost_of_goods

print(f'{new_profit=}')

# Change in Profit
change_in_profit = new_profit - original_profit

print(f'{change_in_profit=}')
This leads this execution result to be returned to the model:
original_profit=75000
new_profit=66550.0
change_in_profit=-8450.0
This gives the model the information it needs, so it then produced the response:
[...] Cutting the price 10% and lifting volume 10% would result in
a **decrease of $8,450** in monthly profit.
We can see the two steps of executing such a command in Figure 10-5. It starts with
the model writing the code that calculates the answer and sending it to the tool for
execution. The results of that execution are returned to the model, which can now
proceed to the following step: presenting the final output to the user.
What happens in the background here is that OpenAI creates a container to run this
code and charges us for it. So executing this trajectory carries LLM inference cost
(metered in tokens) and a single container (charged per session).
Building Code Agents
|



![Figure 10-5: The agent-interpreter loop: the LLM writes code, sends it to a code inter‐](images/fig_10-05_The_agent-interpreter_loop_the_LLM_write.png)

*Figure 10-5: The agent-interpreter loop: the LLM writes code, sends it to a code inter‐*


Figure 10-5. The agent-interpreter loop: the LLM writes code, sends it to a code inter‐
preter, and uses the output to determine the next step
There are other options for code execution even if we want to continue using the
same model. We can use hosted sandbox services from other commercial providers.
Examples include Modal, Daytona, E2B, and Together Code Sandbox. These services
provide an SDK or API that receives the code our agent wants to execute, and
they return the code execution result while hiding the complexity of environment
management.
It’s also possible to roll our own code interpreter: by using open source tools such as
Open Interpreter or the E2B repo, we can configure Python sandboxes that execute
the agent’s code in an isolated container we control, which is the right level of effort
when we have specific security or networking requirements that the hosted services
don’t meet.
|
Chapter 10: Code Agents and Code LLMs

Command-line tools
While code interpreters are restricted for security reasons, the next step up is giving
the model more power to access the command line and utilize the powerful tools
it has, granting it more control of a computer or dedicated virtual machine. Models
need this level of access when they have to inspect or change the environment, for
example, to install Python packages that aren’t part of the code interpreter image.
Software engineering agents such as Cursor or Claude Code also tend to require some
command-line access to do their work: configuring environments, running Python
scripts and unit tests, and much more.
Needless to say that granting an LLM unfettered access to the command line can
become a security nightmare quickly. Recent research highlights just how critical
it is to treat the execution environment of coding agents as an adversarial surface
rather than a benign and trusted backend. For example, “RedCode: Risky Code Exe‐
cution and Generation Benchmark for Code Agents” (2024) presents a benchmark of
code prompts that probe agents for dangerous behaviors like file deletion, privilege
escalation, or network misuse. Another work, “SandboxEval: Towards Securing Test
Environment for Untrusted Code” (2025), outlines security-relevant properties such
as:
1. Exposing system, directory, and metadata information
2. Manipulating structures, contents, and privileges of filesystems
3. Initiating external communication and dangerous operations
More recent work moves from the sandbox to the personal-agent systems became
popular in 2026. “Your Agent, Their Asset: A Real-World Safety Analysis of Open‐
Claw” (2026) runs the first real-world safety evaluation of such an agent and finds
that poisoning any single dimension of its persistent state, its capabilities, identity, or
knowledge, raises attack success rates from roughly 25% to 64% to 74%, concluding
the exposure is inherent in the architecture instead of a fixable bug.
These threats are one reason software agents in IDEs ask the user to approve each
command before running it. The developer is the ultimate decision-maker here,
bearing the responsibility of permitting actions case by case. That model works when
the person approving has the expertise to judge each command, as a developer in
an IDE usually does, but it offers little real protection to the non-technical users we
met earlier in the chapter, who can’t evaluate what a given command will do. Threats
could come from a malicious user or from well-intentioned but naive model actions
that cause data loss. The safeguard is therefore mostly the agent builder’s responsi‐
bility, applied at design time: follow the principle of least privilege by granting the
agent only the permissions and data access its task requires, and scope the tasks and
workflows you assign it so that a wrong action stays contained. This is a choice the
builder makes up front, not something the agent decides for itself.
Building Code Agents
|

Computer use tools
Computer use tools are analogous to command-line tools that operate on a virtual
machine, but they can interact with the UI of the operating system and feed screen‐
shots of the UI to the vision-language model operating the computer as a key source
of information. This can be handy for cases when we want the agent to operate
applications like Microsoft Excel, for example, or for cases when the agent is building
UIs and needs to verify how they are actually rendered in a specific browser at a
specific window size (Figure 10-6).



![Figure 10-6: A computer use agent interacting directly with a virtual machine’s browser](images/fig_10-06_A_computer_use_agent_interacting_directl.png)

*Figure 10-6: A computer use agent interacting directly with a virtual machine’s browser*


Figure 10-6. A computer use agent interacting directly with a virtual machine’s browser
to complete tasks
|
Chapter 10: Code Agents and Code LLMs

Code search
Advanced software engineering agents can benefit from more powerful code retrieval
capabilities. One example here is a tool like ast-grep, which can do more useful
pattern matching on code than a tool like grep alone can. Because it operates on the
code abstract syntax tree (AST), rather than raw text, it operates on code structure
instead of surface representation, allowing it to find patterns while ignoring format‐
ting, variable names, and whitespace.
Code semantic search is another way to give a code agent more powerful retrieval
capabilities. By searching using dense embeddings generated by a code-embedding
model, a code agent can ask a query such as “Find me a code snippet that iterates
over a list” and get back the most relevant candidates. One benchmark of note that
measures code retrieval is CoIR (Code Information Retrieval Benchmark),1 which
also maintains a leaderboard comparing the capabilities of various models.
SQL tool
An organization’s most important data is often stored within a database, and one
of the most useful actions an agent can do is to retrieve the relevant data for a
specific task or scenario. While generalist search or web-search tools can retrieve
some types of information, databases are queried via SQL code that code LLMs can
write. Whether the data resides in a single database or across multiple, a coding
agent can leverage the context it has to write exceedingly complex SQL statements to
retrieve data even if it requires more than a single query. These flows are crucial for
tasks such as data analysis or report generation.
The simplest SQL tool is one that takes a query and executes it on a pre-configured
database, as we can see in Figure 10-7.
1 Li, Xiangyang et al. 2024. “CoIR: A Comprehensive Benchmark for Code Information Retrieval Models,”
arXiv, 2407.02883.
Building Code Agents
|



![Figure 10-7: A SQL agent executing a multi-step trajectory to inspect database schema](images/fig_10-07_A_SQL_agent_executing_a_multi-step_traje.png)

*Figure 10-7: A SQL agent executing a multi-step trajectory to inspect database schema*


Figure 10-7. A SQL agent executing a multi-step trajectory to inspect database schema
and query tables sequentially
Managing the context of a SQL tool is its own area of research that taps into estab‐
lished works of schema linking in database research. And while simpler SQL agents
can work by providing a general database schema describing the tables and columns
in the database, more advanced agents can be empowered by a more advanced
semantic layer that identifies the relevant columns but might also be able to index
some of the relevant data inside the tables and the actual language that users tend to
use, which might be different from what’s actually stored inside the database.
|
Chapter 10: Code Agents and Code LLMs