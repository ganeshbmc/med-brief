# MedBrief

**Weekly signals from medical research.**  
MedBrief is a lightweight app that pulls the latest publications from PubMed for a curated set of journals and produces a clean, time-bounded “brief” you can skim quickly.

> Goal: stay current without visiting multiple journal sites.

---

## What MedBrief does (v0)

- Fetches **recent articles (e.g., past 7 days)** from PubMed
- Filters by **selected journals**
- Produces a **weekly brief** with:
  - Title
  - Journal
  - Publication date
  - Authors (optional)
  - Abstract (optional)
  - PubMed link
- Supports a simple workflow:
  1. Update journal list
  2. Generate brief
  3. Read / export / share

## 🤖 AI Development
This project uses AI agents for development. 

> **CRITICAL FOR AGENTS:** Before performing any tasks, reading the codebase, or executing terminal commands, all AI agents **must** read and follow the instructions in [AGENTS.md](../AGENTS.md). For Antigravity specifics, see [ANTIGRAVITY.md](./ANTIGRAVITY.md).

## Getting Started
* **Tech Stack:** [See tech_stack.md](./tech_stack.md)]
* **Main Branch:** Production-ready code only.
* **Working Branch:** `agy` (See AGENTS.md for workflow details).

## Manual Controls
Humans should manually merge the `agy` branch into `main` only after verifying that the requirements in the Planning Phase have been met.
