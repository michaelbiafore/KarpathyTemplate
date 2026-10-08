# The Ontology Pipeline® — A Semantic Knowledge Management Framework

*Jessica Talisman, MLS (May 26, 2025)*

## Introduction

Structured semantic knowledge systems are becoming essential to performant LLMs, yet technologists either dismiss them as mere text labels or reject them as too labor-intensive. The result is over-reliance on public taxonomies (e.g., the Google Product Taxonomy), producing "cookie-cutter" ecosystems that fail to model an organization's unique attributes — a root cause of AI implementation failures. Lacking a formal framework, the work behaves as a black box: investment cannot be scoped and ROI is hard to measure, since benefits surface only indirectly in RAG performance, entity management, and retrieval metrics.

## Enter The Librarians

Library and Information Science already supplies principled methods for turning data into information and, once accessible to humans and machines, into knowledge. Librarians have used ML and AI as cataloging tools for over a decade, offering repeatable methodologies technologists should adopt.

## The Ontology Pipeline®

The pipeline is a sequence of iterative building blocks, each phase preparing the next, with data cleaning folded into semantic engineering.

![Figure on page 1](images/fig_p001_x9.png)

*The six pipeline stages — controlled vocabulary, metadata standards, taxonomy, thesaurus, ontology, knowledge graph — each annotated with its role.*

Codifying the workflow lets organizations estimate investment and gives stakeholders visibility into requirements.

### Controlled Vocabulary

The first block. Data is deduplicated, merged, and defined so synonyms reconcile into a clean, disambiguated list, with a definition for every concept.

![Figure on page 4](images/fig_p004_x28.png)

*NASA's entry for "Mission to Planet Earth," where UF ("Use For") points from the acronym MTPE.*

### Metadata Standards

Metadata standards encode the "aboutness" of assets through schema-based control. Elements are STRUCTURAL (machine readability), DESCRIPTIVE (context), or ADMINISTRATIVE (maintenance, lineage), plus extensions like provenance.

![Figure on page 5](images/fig_p005_x33.png)

*Elements/values diagram with a worked example: TITLE = "Mad Men Season 5," TYPE = article.*

The controlled vocabulary supplies allowable values, enabling entity reconciliation and schema-based validation matrices.

### Taxonomy

Taxonomy transforms the vocabulary into a broad-to-narrow, parent–child hierarchy — useful for ML classification, navigation, tagging.

![Figure on page 6](images/fig_p006_x38.png)

*A nested Adobe Experience Manager tree illustrating parent/child hierarchy.*

Spreadsheet taxonomies become unwieldy and lack machine-readable encoding; Talisman recommends semantic middleware (Graphwise, TopQuadrant), SKOS as an upper ontology, and validation matrices catching recursive loops and relationship clashes. Governing standards: ISO 25964-1/-2, RDF validation, ANSI/NISO Z39.19-2005 (R2010). Design decisions include depth, granularity, localization, vocabulary deprecation, and new-concept intake.

### Thesaurus

A thesaurus matures a taxonomy by adding associative, equivalent, and transverse relations beyond hierarchy, encoded with a mid-level ontology such as SKOS-XL.

![Figure on page 7](images/fig_p007_x55.png)

*A software-framework term list beside BT (broader term), SYN (synonym), and NT (narrower term) relations.*

### Ontology

Ontologies assign classes, properties, relations, and attributes, establishing rule bases and logical reasoning. ==Machines favor ontologies for high-fidelity disambiguation== supporting retrieval, entity management, and RAG. Building one atop messy vocabularies is near impossible.

![Figure on page 8](images/fig_p008_x59.png)

*A subject–predicate–object triple plus a domain illustration linking classes, attributes, axioms, rules, and instances.*

### Knowledge Graph

The synthesis and visualization layer — an assemblage of all prior blocks, queried with SPARQL and SHACL.

![Figure on page 9](images/fig_p009_x63.png)

*A dense radial network of interlinked entity nodes.*

Its layered construction eases troubleshooting of broken logic and provides control planes for scaling; the visualization doubles as an organizational language for teaching and buy-in.

![Figure on page 10](images/fig_p010_x69.png)

*ANSI/NISO spectrum ordering knowledge organization systems by expressiveness: term list, name authority, taxonomy, thesaurus, ontology.*


## Conclusion

A repeatable framework lets organizations project costs, develop value metrics, and secure funding. Its rigorous iteration — cleaning, reconciliation, modeling, testing, enrichment, enforcement, measurement — is exactly what LLMs need, and semantic engineers are best placed to deliver it. Talisman, a 25-year practitioner (Adobe, Amazon), founded Contextually LLC and the Knowledge Graph Academy.
