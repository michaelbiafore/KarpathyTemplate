---
title: "Retrieval-Augmented Generation"
chapter_number: 63
page_start: 165
page_end: 173
part: "Part 2: A Deeper Dive Into Large Language Models"
---
# Retrieval-Augmented Generation

Note how there is only a system role with a summary of the conversation history. As
you continue the conversation, this summary gets updated. As always, if you want to
track the full conversation, you can use the TrajectoryViewer:
from illustrated_agents.utils import TrajectoryViewer
TrajectoryViewer(agent.trajectory)
Although this implementation may seem straightforward, maintaining the conversa‐
tion history can be a difficult task and requires understanding what is important: the
entire history, the recent history, or a summarized variant? For short conversations,
maintaining the entire history would work, but that might not be the case for long
sequences of actions. In Chapter 10, we will touch on customizing this summariza‐
tion process for a specific domain like code generation.
Long-Term Memory
As the conversation history and the number of actions that an agent has taken grows,
so does the need for long-term memory. However, its usefulness is not limited to
conversation history but may also include proprietary or external knowledge. Long-
term memory typically involves maintaining one or more external databases that can
be queried to extract additional information. This can contain information about
previous traces or states of the agent (episodic memory) or information unrelated
to the agent’s behavior but about the context of your application instead (semantic
memory), like your organization’s documents.
Retrieval-Augmented Generation
Arguably, the most common method for giving your agent, or any LLM for that mat‐
ter, long-term memory is Retrieval-Augmented Generation (RAG).4 RAG typically
consists of two stages: ingestion and inference.
In ingestion, your external data, typically unstructured text, is embedded into numer‐
ical representations and stored in a database (Figure 4-14). To create these representa‐
tions, a special variant of an LLM is used, an embedding model, which converts text
into numerical vectors (also called embeddings) that capture the semantic meaning of
the input. This embedding model is trained to create numerical representations such
that words and phrases with similar meaning will have similar representations. This
external database can be considered the long-term memory of the LLM, which can be
queried for relevant information.
4 Lewis, Patrick et al. 2020. “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,” NIPS’20:
Proceedings of the 34th International Conference on Neural Information Processing Systems, 9459-9474.
Long-Term Memory
|



![Figure 4-14: RAG starts with converting the input data into numerical information](images/fig_04-14_RAG_starts_with_converting_the_input_dat.png)

*Figure 4-14: RAG starts with converting the input data into numerical information*


Figure 4-14. RAG starts with converting the input data into numerical information
(called embeddings or vectors) to be stored in a vector database
Inference with RAG consists of four steps. In step 1, the user’s query is embedded
using the same model that was used for embedding the external data. In step 2, the
embedded query is compared to the external database, and the most relevant items in
the database to the query are extracted.
Defining relevancy in RAG systems can mean many things. In our example, it means
the similarity between the query embeddings and the external embeddings. This
similarity can be defined through the embeddings we created, but hybrid systems
are also possible where embeddings are combined with traditional Bag-of-Words-like
approaches.5
In step 3, the relevant items and the user’s query are combined into the prompt. This
step is meant to provide the model with context for the generation step. Essentially,
you tell the LLM that you have contextual information that it can use to derive its
answer. Finally, in step 4, the augmented prompt is used by the model to generate the
output. The added contextual information should generally result in more accurate
and relevant responses, assuming that the contextual information is indeed relevant
and correct. Figure 4-15 illustrates the four steps of inference with RAG.
RAG is often used to minimize hallucination, which refers to the tendency of LLMs
to confidently produce an answer that is actually incorrect. By providing the LLM
with external information (which you assume to be true), the LLM is less likely to
“make up” information.
5 Bag-of-Words is a sparse representation of texts in which the representation consists of the frequency that
each word appears. The result is a sparse matrix where most entries are zero because any single document
contains only a tiny fraction of the total vocabulary.
|
Chapter 4: Memory



![Figure 4-15: The full pipeline of retrieval- (2) augmented (3) generation (4)](images/fig_04-15_The_full_pipeline_of_retrieval-_2_augmen.png)

*Figure 4-15: The full pipeline of retrieval- (2) augmented (3) generation (4)*


Figure 4-15. The full pipeline of retrieval- (2) augmented (3) generation (4)
Let’s explore how we can add RAG to your TinyAgent. The first thing that we need
to start with is choosing an embedding model that can convert your query into an
embedding. The model that we are choosing is called EmbeddingGemma and is
a 308-million-parameter model from Google DeepMind. We create the Embedding
Model class that allows us to easily embed documents:
```
import json
import urllib.request
```


class EmbeddingModel:
 """Generate embeddings."""

 def __init__(
 self,
 model: str,
 base_url: str = "http://localhost:11434/v1",
 ):
 """Initialize the embedding model with the given model."""
 self.model = model
 self.base_url = base_url

 def embed(self, text: str) -> list[float]:
 """Convert text into a numerical vector."""
 # POST to the OpenAI-compatible /embeddings endpoint
 request = urllib.request.Request(
 f"{self.base_url}/embeddings",
 data=json.dumps({"model": self.model, "input": text}).encode(),
 headers={"Content-Type": "application/json"},
 )
 with urllib.request.urlopen(request) as resp:
 response = json.loads(resp.read())

 # Extract and return the embedding
 return response["data"][0]["embedding"]
Long-Term Memory
|

Since Ollama also supports embedding models, we can mimic the same structure as
we did with the LLM.
Let’s try it out with an example. We embed a single sentence like so:
# Initialize EmbeddingGemma
embedding_model = EmbeddingModel(model="embeddinggemma")

# Test the embedding model
output = embedding_model.embed("Dolphins are amazing!")
output
This gives us:
[-0.21747557818889618,
- 0.01567786931991577,
0. 03601466864347458,
- 0.0049857525154948235,
...
0. 027807850390672684,
- 0.005654981359839439,
- 0.02514023706316948,
0. 0022561103105545044,
- 0.001453613629564643]
This model produces 768 values, each between –1 and 1, for a given input. We can
use these values to compare different documents and calculate their similarity. This
is typically calculated as the cosine similarity, which represents the angle between
embeddings. A smaller angle means a higher similarity. The cosine similarity is calcu‐
lated through the dot product of the embeddings and then divided by the product of
their lengths for normalization.
Let’s try it out!
# Create embeddings
embedding_a = embedding_model.embed("I love flamingos.")
embedding_b = embedding_model.embed("Dolphins use echolocation.")
embedding_c = embedding_model.embed("Flamingos are pink birds.")

# Calculate cosine similarity between A and B
dot_ab = sum(x * y for x, y in zip(embedding_a, embedding_b))
norm_a = sum(x * x for x in embedding_a) ** 0.5
norm_b = sum(x * x for x in embedding_b) ** 0.5
similarity_ab = dot_ab / (norm_a * norm_b)

# Calculate cosine similarity between A and C
dot_ac = sum(x * y for x, y in zip(embedding_a, embedding_c))
norm_c = sum(x * x for x in embedding_c) ** 0.5
similarity_ac = dot_ac / (norm_a * norm_c)

print(f"Similarity between A and B: {similarity_ab}")
print(f"Similarity between A and C: {similarity_ac}")
|
Chapter 4: Memory

Which gives us:
"""
Similarity between A and B: 0.3546779285862413
Similarity between A and C: 0.6386974942657335
"""
As expected, the similarity between “I love flamingos” and “Flamingos are pink birds”
is much higher than between “I love flamingos” and “Dolphins use echolocation.” We
can use cosine similarity to perform the comparisons and select the documents that
best suit the user’s query.
As such, the RAGMemory class that we are going to implement has the following steps:
1. Embed all external documents the agent has no direct access to.
1.
2. Embed the user’s query.
2.
3. Compare the embeddings and create a similarity matrix.
3.
4. Return the documents with the highest similarity.
4.
5. Add those documents to the prompt.
5.
This gives us the following class:
from illustrated_agents.chapters.ch4 import Memory

class RAGMemory(Memory):
 """Long-term Memory with RAG."""

 def __init__(self, embedding_model: EmbeddingModel, documents: list[str]):
 super().__init__()
 self.embedding_model = embedding_model
 self.documents = documents
 self.embeddings = [embedding_model.embed(doc) for doc in documents]

 def add(self, role: str, content: str, **kwargs) -> None:
 # Augment user queries with retrieved context before storing
 if role == "user":
 context = "\n".join(self.search(content))
 content = f"""Context:
{context}

Question: {content}"""
 super().add(role, content, **kwargs)

 def search(self, query: str) -> list[str]:
 """Return the top-k documents most similar to the query."""
 query_embed = self.embedding_model.embed(query)
 scores = [self._cosine(query_embed, embed) for embed in self.embeddings]
 ranked = sorted(
 range(len(scores)), key=lambda i: scores[i], reverse=True
 )
Long-Term Memory
|

return [self.documents[index] for index in ranked[:3]]

 def _cosine(self, a: list[float], b: list[float]) -> float:
 """Calculate cosine similarity between two embeddings.."""
 dot = sum(x * y for x, y in zip(a, b))
 norm = (sum(x * x for x in a) ** 0.5) * (sum(x * x for x in b) ** 0.5)
 return dot / norm
Let’s put this to practice, starting with a set of documents that your TinyAgent has
no direct access to. This is going to be a simple example, but imagine you have
thousands of documents:
from illustrated_agents.chapters.ch4 import TinyAgent

# RAGMemory with external documents
documents = [
 "Sarah works as a marine biologist studying coral reefs.",
 "Sarah lives in Lisbon, Portugal.",
 "Sarah's favorite hobby is rock climbing.",
 "Sarah favorite animal is flamingos.",
 "Sarah speaks fluent Spanish and Portuguese.",
 "Ilse is a software engineer at a renewable energy startup.",
 "Ilse lives in Amsterdam, the Netherlands.",
 "Ilse plays the cello in a local string quartet.",
 "Ilse's favorite author is Brandon Sanderson.",
 "Ilse's favorite animal is dolphins.",
]
memory = RAGMemory(documents=documents, embedding_model=embedding_model)

# Create the Agent and run a query
agent = TinyAgent(llm=llm, memory=memory)
response = agent.run("What is Sarah's favorite animal?")
print(response)
We asked it the question “What is Sarah’s favorite animal?,” which your TinyAgent
can only know if it truly has gotten those documents:
"Sarah's favorite animal is flamingos."
It got it correct! Let’s explore the memory and see what was happening under the
hood:
print(agent.memory.get_messages())
Which gives:
[
 {
 'role': 'user',
 'content': "Context:\nSarah favorite animals are flamingos.\n
 Sarah's favorite hobby is rock climbing.\nIlse's favorite animals
 are dolphins.\n\nQuestion: What is Sarah's favorite animal?"
 },
|
Chapter 4: Memory

{'role': 'assistant', 'content': "Sarah's favorite animal is flamingos."}
]
Note how it retrieved the top three documents as the context? This is both the
advantage and disadvantage of RAG. Although it minimizes the context that you
have to pass to the model, there is no guarantee that the context will always be good
enough. You could, for example, only accept documents that have a minimum degree
of similarity rather than simply getting the top three irrespective of their absolute
scores.
Now that your TinyAgent has memory in different forms, let’s recap what we built in
this chapter.
What We Built
TinyAgent/
├── agent.py ← Updated (Integrated `Memory` into your `TinyAgent`)
├── llm.py ← Updated (Added `EmbeddingModel` to create embeddings)
├── memory.py ← New (Added both short-term and long-term memory)
└── trajectory.py
MemoryBank
An interesting take on RAG for chatbots is MemoryBank, a mechanism that allows
LLMs to recall relevant memories as a long-term mechanism (external database)
rather than a short-term mechanism (conversation history).6 Its experiences through
conversations are stored in a separate database that allows the LLM to retrieve rele‐
vant memories. What sets it apart from regular RAG is that this memory is continu‐
ously updated to selectively preserve memory through an updating mechanism.
This mechanism allows the MemoryBank to forget and reinforce memory inspired
by the Ebbinghaus Forgetting Curve theory, which is a curve demonstrating the pace
at which we tend to forget. The curve is often shown as being exponential, resulting
in a loss of half of what we learn each day. A common way to prevent forgetting
what you learned, for instance when preparing for exams, is to actively recall the
learned information frequently. This is referred to as spaced repetition, which tends
to decrease the pace at which knowledge is forgotten. Figure 4-16 illustrates this
knowledge decay and the effect of spaced repetition on it.
MemoryBank borrows from this theory and frequently updates the long-term mem‐
ory of an LLM based on which pieces of knowledge are (not) accessed. Specifically,
this means that when a memory item is retrieved and used during conversations, it
6 Zhong, Wanjun et al. 2024. “MemoryBank: Enhancing Large Language Models with Long-Term Memory,”
Proceedings of the AAAI Conference on Artificial Intelligence, 38(17).
Long-Term Memory
|

will persist longer in the MemoryBank. However, if the memory item hasn’t been
retrieved for a while, then there is a chance the memory will be removed entirely.



![Figure 4-16: An example of the forgetting curve theory that demonstrates how spaced](images/fig_04-16_An_example_of_the_forgetting_curve_theor.png)

*Figure 4-16: An example of the forgetting curve theory that demonstrates how spaced*


Figure 4-16. An example of the forgetting curve theory that demonstrates how spaced
repetition and retrieval reduces knowledge decay
The authors use a few variants of memory:
Conversation history
Raw multi-turn conversations.
Summaries of past events
These are generated by an LLM based on the conversation history.
User’s portrait
The personality traits and emotions of the user as summarized by the LLM based
on the conversation history.
These forms of memory are used to create the MemoryBank, as shown in Figure 4-17,
and show how an LLM may create the summaries of past events as well as the user’s
portrait.
The summaries and conversation turns are embedded so that they can easily be
retrieved. The user portrait is dynamically updated and always passed as additional
context. Figure 4-18 shows a full overview of this pipeline. When a query is created,
it is embedded, and related conversation turns and summaries are retrieved, together
with the user portrait. When conversation turns are retrieved, their strength is upda‐
ted, making them less likely to be removed from the MemoryBank. The retrieved
context, together with the query, is used as input for the LLM to generate an answer.
This form of memory demonstrates the potential complexity of RAG-like applica‐
tions, where each use case necessitates different types of memories, summarizations,
etc. As such, there are many forms of RAG, such as GraphRAG and Multi-modal
|
Chapter 4: Memory

RAG, that each require its own set of considerations. The RAG examples shown
previously are often referred to as vanilla RAG or naive RAG for their straightforward
implementation.



![Figure 4-17: MemoryBank maintains summaries of past events and information on the](images/fig_04-17_MemoryBank_maintains_summaries_of_past_e.png)

*Figure 4-17: MemoryBank maintains summaries of past events and information on the*


Figure 4-17. MemoryBank maintains summaries of past events and information on the
user generated by an LLM



![Figure 4-18: How MemoryBank is used for RAG](images/fig_04-18_How_MemoryBank_is_used_for_RAG.png)

*Figure 4-18: How MemoryBank is used for RAG*


Figure 4-18. How MemoryBank is used for RAG
Long-Term Memory
|