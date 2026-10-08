## Table of Contents

- The Black Box Problem
- Enter the Librarians
- The Six Building Blocks
- Why the Sequence Pays

## The Black Box Problem

Organized semantic knowledge is now essential to performant LLM systems, yet technologists treat it as trivial text labels or as too labor-intensive to fund. The fallback — Talisman names the **Google Product Taxonomy** — models nobody's actual business.

The deeper problem is procedural. Without a framework the work ==functions as a black box==: investment cannot be scoped, and returns resist measurement because benefits are secondary, surfacing in RAG, entity management, and retrieval metrics.

## Enter the Librarians

Library and Information Science already supplies principled methods for turning data into information and, once machine-accessible, knowledge. The **Ontology Pipeline®** codifies decade-old librarian ML workflows so the effort can be scoped, staffed, and sold as a product.

## The Six Building Blocks

Each phase prepares the next, with data cleaning folded into the semantic engineering workflow rather than bolted on ahead.

![Figure on page 1](images/fig_p001_x9.png)
*Figure 1: the six stages in order — controlled vocabulary, metadata standards, taxonomy, thesaurus, ontology, knowledge graph — each annotated with the one job it does for the stage above it.*

### Vocabulary and Metadata

A **controlled vocabulary** comes first: data deduplicated and merged, synonyms reconciled into one disambiguated list, a definition per concept.

![Figure on page 4](images/fig_p004_x28.png)
*Figure 2: NASA's entry for "Mission to Planet Earth" — `UF` ("Use For") binds the acronym MTPE to the preferred term, which is what synonym resolution actually looks like on the page.*

**Metadata standards** encode an asset's "aboutness" through schema-based control, each element `STRUCTURAL`, `DESCRIPTIVE`, or `ADMINISTRATIVE`. The vocabulary supplies their allowable values, enabling entity reconciliation and validation matrices.

### Hierarchy and Relations

A **taxonomy** turns the vocabulary into a broad-to-narrow parent–child hierarchy for ML classification, navigation, and tagging. Skip spreadsheets — no machine-readable semantics; use semantic middleware, `SKOS` as the upper ontology, and validation matrices catching recursive loops, under `ISO 25964-1` and `ANSI/NISO Z39.19`. A **thesaurus** adds associative, equivalent, and transverse relations — `BT`, `NT`, `SYN` — in `SKOS-XL`.

### Logic and Synthesis

An **ontology** assigns classes, properties, relations, and attributes, establishing rule bases for how concepts behave.

![Figure on page 8](images/fig_p008_x59.png)
*Figure 3: the subject–predicate–object triple over a domain of classes, attributes, axioms, rules, and object instances — the layer where logical reasoning finally enters.*

> Machines love ontologies because of their high-fidelity disambiguation and description.

Shortcuts come due here: logic is near-impossible to introduce over data that is not logically structured. The **knowledge graph** then synthesizes all prior blocks, queried via `SPARQL` and `SHACL`; layered construction keeps broken logic troubleshootable and doubles as an organizational language for buy-in.

## Why the Sequence Pays

Taxonomy-stage decisions — depth, granularity, localization, concept intake — propagate everywhere; faulty base logic proliferates upward. Commercially, a repeatable framework lets organizations project costs, prove value, and secure funding for work that clean-data-hungry LLMs demand regardless.
