# AI Recruiter Pipeline - Project Architecture

## 📁 **core/** - Core Processing Engine
The main processing pipeline containing all core functionality modules.

- **`data.py`** - Data structures and candidate/job data handling
- **`email_generator.py`** - Automated email generation for candidate outreach
- **`embedding.py`** - Text embedding generation using vector models for semantic matching
- **`filtering.py`** - Initial candidate filtering logic
- **`jd_extraction.py`** - Job description parsing and feature extraction
- **`matching.py`** - Core matching algorithms between candidates and job requirements
- **`normalization.py`** - Data normalization and standardization processes
- **`pipeline.py`** - Main pipeline orchestration and workflow management
- **`scoring.py`** - Candidate scoring and ranking algorithms

## 📁 **data/** - Data Storage
Contains structured data files for the application.

- **`df_candidates.pkl`** - Serialized DataFrame containing candidate profiles and CVs
- **`resume_data.csv`** - Raw resume data in CSV format for processing

## 📁 **jd/** - Job Description Management
Handles job description processing and sample outputs.

- **`sample-outputs/`** - Directory containing sample job description processing results
- **`sample_jd_01.txt`** - Sample job description file for testing and development

## 📁 **models/** - Data Models & Configuration
Defines data structures and model configurations.

- **`data_models.py`** - Pydantic models and data classes for candidates, jobs, and results
- **`enums.py`** - Job category definitions and skill importance levels (e.g., required, preferred, nice-to-have)
- **`mappings.py`** - Field mappings and data transformation configurations

## 📁 **prompts/** - AI Prompt Templates
Contains prompt templates for AI operations.

- **`email_generation.py`** - Prompt templates for generating recruitment emails
- **`jd_extraction.py`** - Prompt templates for extracting structured data from job descriptions

## 📁 **tests/** - Test Suite
Unit and integration tests for the pipeline components.

- **`test_eval_pipeline.py`** - Tests for pipeline evaluation and performance metrics
- **`test_matching_pipeline.py`** - Tests for the core matching algorithm functionality

## 📁 **utils/** - Utility Functions
Helper functions and utilities.

- **`parsing.py`** - Text parsing utilities

## 📚 **Main Application Files**
- **`ai_recruiter.ipynb`** - Jupyter notebook for interactive development and testing
- **`main.py`** - Main application entry point and CLI interface

## 🏗️ **System Architecture Overview**

The pipeline follows this general flow:

1. **Data Ingestion** → Load candidate data from CSV/pickle files
2. **Candidate Processing** → Parse and normalize candidate data
4. **Embedding Generation** → Create vector representations of candidate profile for semantic matching
2. **Job Description Processing** → Extract requirements using LLM prompts
5. **Filtering & Matching** → Apply filters and match candidates to jobs
6. **Scoring & Ranking** → Score candidates and rank by relevance
7. **Output Generation** → Generate emails and results for recruiters

## 🔄 **Key Components Integration**

- **Core Pipeline** orchestrates the entire process
- **Models** define data structures used throughout
- **Prompts** provide LLM templates for intelligent text processing
- **Utils** support parsing and data manipulation
- **Tests** ensure pipeline reliability and performance