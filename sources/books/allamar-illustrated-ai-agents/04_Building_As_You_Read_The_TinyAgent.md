---
title: "Building As You Read: The TinyAgent"
chapter_number: 4
page_start: 14
page_end: 14
---
# Building As You Read: The TinyAgent

illustrations give a visual identity to the major concepts and processes of agentic
systems. One figure in particular, introduced in Chapter 1, serves as the foundation
of the entire book. It shows the anatomy of an agent, and every subsequent chapter
zooms into one of its components, so that by the end you will have assembled the
complete picture piece by piece.
This book is about agents backed by LLMs. Other kinds of AI agents exist in practice,
but rather than writing “LLM-backed AI agents” at every mention, we simply say AI
agents and trust you to recall which kind we mean.
One more thing before we begin. The figures in this book are all custom made, and
each went through more rounds of sketching, argument, and redrawing than we
care to count before it earned its page. We worked this way because we were not
assembling information for sale; we were making something for you, as carefully as
we knew how. What we hope you do with it is a question we have saved for the
afterword, on the very last page.
Building As You Read: The TinyAgent
Although “illustrated” is in the name of this book, understanding agents benefits
greatly from building one. Alongside the visual journey, you will build a working
agent in Python, one component at a time, which we call the TinyAgent. By the
end of the book, it will reason, remember, use tools, plan, and reflect. The result is
essentially a package you developed yourself, with a genuine understanding of every
line in it.
The code printed in this book is here to teach; the code in the book’s repository is
here to run. While the pages of a book are fixed once printed, the repository is a
living companion that we actively maintain with bug fixes, dependency updates, and
adjustments as the libraries and APIs the examples rely on evolve. When you are
ready to lean in and build, work from the repository rather than typing code from the
page: you will get the current, tested version of every example, along with additional
tutorials and material that did not fit in the book.
Audience
We wrote this book for several audiences at once, and we structured it so that each
gets value from it:
- If you are a developer building agentic systems, the hands-on code and the
TinyAgent you assemble across the chapters will give you a working foundation
you understand down to the last line.
xii
|
Preface