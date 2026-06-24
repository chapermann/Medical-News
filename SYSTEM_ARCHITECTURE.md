# System Architecture — Medical News

## Overview

Medical News is a distributed biomedical literature surveillance system designed around persistent search engines that continuously monitor scientific databases and deliver only new, relevant evidence.

The system is composed of five core layers:

1. Query Intelligence Layer (DeCS + MeSH + Boolean Builder)
2. Retrieval Layer (PubMed, BVS, SciELO, Europe PMC)
3. Deduplication & Storage Layer (PostgreSQL)
4. AI Curation Layer (GPT-OSS-120B)
5. Delivery Layer (Email, Dashboard, Podcast)

---

# 1. Core Design Principle

The fundamental unit of the system is not the article.

It is the **Search Engine**.

A Search Engine is a persistent, executable scientific query that evolves over time but maintains memory of previously retrieved literature.

---

# 2. System Pipeline

## Step 1 — User Input

User defines:

* Descriptors (DeCS / MeSH / Keywords)
* Boolean logic (AND, OR, NOT)
* Filters (study type, year, language)
* Frequency (daily / weekly)
* Duration (8–24 weeks)

---

## Step 2 — Query Intelligence Layer

Responsible for:

* Mapping DeCS ↔ MeSH
* Expanding synonyms
* Normalizing terminology
* Validating Boolean syntax
* Estimating query complexity
* Suggesting optimization

Output:

Structured PubMed-compatible query.

---

## Step 3 — Retrieval Layer

Execution across:

* PubMed (NCBI E-utilities)
* BVS (DeCS-based search)
* SciELO
* Europe PMC

Each execution is time-bounded and incremental.

Only publications within the defined time window are queried.

---

## Step 4 — Deduplication Layer

Each article is stored using:

* PMID (primary key)
* DOI (secondary key)

Mapping table:

* article ↔ search_engine (many-to-many)

The system ensures that no article is delivered twice for the same engine.

---

## Step 5 — AI Curation Layer

Model: GPT-OSS-120B

Responsibilities:

* Classify study type:

  * RCT
  * Meta-analysis
  * Cohort
  * Systematic review
* Extract structured metadata
* Assign relevance score
* Identify clinical impact level
* Generate summaries
* Build weekly synthesis

AI does NOT perform retrieval.

---

## Step 6 — Delivery Layer

Outputs:

* Email report (weekly/daily)
* Web dashboard
* PDF summary (optional)
* Podcast script (TTS integration)

If no new articles are found:

System sends a "null report" indicating no updates.

---

# 3. Temporal Engine Behavior

Each Search Engine operates as a time-bounded surveillance unit.

Example lifecycle:

* Week 1: high volume of articles
* Week 2–4: moderate novelty
* Week 5–8: sparse or no new data

At each cycle:

* Only newly indexed publications are returned
* Previously seen PMIDs are excluded

---

# 4. System Components

## Backend

* FastAPI (core API)
* Background scheduler (GitHub Actions / cron)
* PubMed integration module

---

## Database

* PostgreSQL (primary store)
* Optional: pgvector (semantic layer in future)

---

## AI Layer

* GPT-OSS-120B (NVIDIA API)
* Prompt-based structured outputs

---

## External APIs

* NCBI E-utilities (PubMed)
* BVS / DeCS API
* Europe PMC API
* SciELO endpoint

---

## Delivery

* SMTP email service
* Web dashboard (React)
* Podcast generator (NotebookLM / TTS engine)

---

# 5. Key Innovation

Unlike traditional alert systems, Medical News introduces:

* Persistent search engines
* Incremental literature discovery
* Deduplicated scientific memory
* Structured AI curation layer
* Time-bounded monitoring cycles

This transforms literature tracking into a continuous scientific intelligence system.

---
