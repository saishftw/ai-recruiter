# AI Recruiting Agent

## Project Overview

This project implements a candidate ranking system that matches job descriptions (JDs) with a dataset of candidate profiles. It uses a combination of fuzzy logic, structured parsing, and semantic search to rank candidates based on how well they align with the role requirements.

The pipeline evaluates each candidate across four dimensions:
- Job title similarity
- Skill match (with priority weighting)
- Qualification match (normalized degree + field matching + priority weighting)
- Semantic profile match (via embeddings)

The system outputs top candidates with a full breakdown of matched attributes and normalized scores.

---

## Candidate Scoring System

This system evaluates and ranks candidates against a given job description (JD) using a multi-step scoring pipeline. It combines fuzzy logic, structured extraction, and semantic search to generate a final score for each candidate.



### Scoring Components

Each candidate is scored based on the following criteria:

- **Job Title Match**  
  Compares the candidate’s current job title with the role specified in the JD using fuzzy string matching.

- **Skill Match**  
  Each skill in the JD is tagged with a priority level. Candidate skills are compared using fuzzy matching, and matches above a set threshold contribute to the skill score based on their importance.

- **Qualification Match**  
  JD-specified degrees and fields of study are normalized and matched against the candidate’s educational background. A valid match requires:
  - A normalized degree type match in the degree hierarchy
  - A field of study match above a defined fuzzy threshold

- **Semantic Profile Match**  
  The candidate’s entire profile is embedded using a sentence transformer and compared to the JD embedding using cosine similarity. This captures alignment in responsibilities, objectives, and experience.


### Skill Matching Logic

- Skills from the JD are structured with priority tags like `essential`, `important`, etc.
- Each candidate skill is compared using fuzzy logic (e.g., token set ratio)
- Matches above a threshold are collected and scored based on their priority

### Qualification Matching Logic

- Degree names are normalized using a fuzzy matcher and mapped to standard categories (e.g., bachelor, master)
- Fields of study are compared using fuzzy similarity
- Matches are scored based on their presence and relevance in the candidate’s qualifications and degree hierarchy

### Semantic Matching

Some attributes like **career objectives** and **responsibilities** are unstructured and cannot be matched using simple fuzzy logic.

To evaluate these:

- The candidate's profile (including responsibilities and objectives) and the job description are embedded using a sentence transformer.
- Cosine similarity is calculated between these embeddings to measure semantic alignment.
- This score reflects how well the candidate's goals and experience match the intent of the role.


### Final Score

Each candidate receives a normalized score for each component. These are combined into a final score that determines their overall suitability for the JD.

The final output includes:
- The candidate’s total score
- Individual component scores (title, skill, qualification, semantic)
- Matched skills and qualifications for transparency

---

## Quick Start

There are two ways to run the pipeline:

### 1. Run via Notebook (Google Colab)
You can explore and visualize the entire scoring process interactively in a Jupyter notebook.

> **[Run on Google Colab](https://your-colab-link-here)**

No setup is required — the notebook handles loading, filtering, scoring, and explanation.

---

### 2. Run via Python CLI (`main.py`)

If you prefer running the pipeline end-to-end via terminal:

```bash
uv venv  # Create virtual environment using uv
uv pip install -r requirements.txt

uv run main.py
```

Outputs the top-ranked candidates along with their scores and matched attributes.

---

## Installation Instructions

### Prerequisites

* Python 3.10+
* [`uv`](https://github.com/astral-sh/uv) (recommended for managing virtual environments and dependencies)

### Using `uv` (recommended)

```bash
uv venv
uv pip install -r requirements.txt
```

### Without `uv`

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

### Run Tests

```bash
pytest tests/
```

---

## Evaluation and Validation

To validate the pipeline, multiple strategies were implemented:

* **Reverse Matching with Synthetic JDs:** 
To validate the pipeline, I generated synthetic job descriptions using an LLM based on individual candidate profiles. The evaluation checks whether the candidate whose profile was used to create the JD ranks among the top 3 results. This reverse matching approach helps verify that the scoring and matching logic correctly identifies highly relevant candidates when the JD is tailored to them.

* **Threshold Tuning:**
  Various score thresholds were tested to balance strictness and candidate retention.

* **Explainability Checks:**
  The top candidates include matched skills and qualifications for transparency and debugging.

---

## File Structure

```
.
├── core/                   # Core logic (scoring, matching, embeddings)
├── data/                   # Candidate dataset CSVs
├── jd/                     # Sample and synthetic JDs
├── tests/                  # Unit tests and eval modules
├── main.py                 # CLI entry point
├── requirements.txt
├── README.md
```