import logging
import pandas as pd
from sentence_transformers import SentenceTransformer
from core.data import process_candidate_data
from core.jd_extraction import process_jd, load_sample_jd
from core.filtering import filter_by_job_title
from core.scoring import (
    calculate_skill_score,
    calculate_qualification_score,
    calculate_similarity_score,
    calculate_total_score,
)

def run_pipeline(
    jd_text: str | None = None,
    resume_csv_path: str = '../data/resume_data.csv',
    jd_file_path: str = '../jd/sample_jd_01.txt',
    embedding_model_name: str = 'all-mpnet-base-v2',
    title_score_threshold: float = 0.4,
    filter_by_skills: bool = False,
    skill_score_threshold: float = 0.25,
    filter_by_qualifications: bool = False,
    qualification_score_threshold: float = 0.2,
    top_n: int = 10,
    df_candidates: pd.DataFrame | None = None
) -> pd.DataFrame:
    """
    Runs the full candidate matching pipeline.
    """
    logging.info("Starting candidate matching pipeline...")

    logging.info(f"Loading embedding model: {embedding_model_name}")
    model = SentenceTransformer(embedding_model_name)

    logging.info("Loading and processing candidate data...")
    if df_candidates is None or df_candidates.empty:
        df_candidates = process_candidate_data(resume_csv_path, model)
    
    logging.info("Loading and processing job description...")
    if jd_text is None:
        jd_text = load_sample_jd(jd_file_path)
    processed_jd = process_jd(jd_text)

    logging.info("Filtering by job title...")
    df_filtered = filter_by_job_title(df_candidates, processed_jd.role, title_score_threshold)

    logging.info("Scoring skills...")
    df_filtered = calculate_skill_score(df_filtered, processed_jd, filter_by_skills, skill_score_threshold)

    logging.info("Scoring and filtering by qualifications...")
    df_filtered = calculate_qualification_score(df_filtered, processed_jd, filter_by_qualifications, qualification_score_threshold)

    logging.info("Scoring by similarity...")
    df_filtered = calculate_similarity_score(df_filtered, processed_jd, model)

    logging.info("Calculating final score...")
    df_scored = calculate_total_score(df_filtered, processed_jd)

    logging.info(f"Sorting and returning top {top_n} candidates.")
    cols_to_display = [
        'candidate_id', 'job_position_name', 'total_score', 'title_score', 'skill_score', 'matched_skills',
        'qualification_score', 'matched_qualifications', 'similarity_score',
    ]
    top_candidates = df_scored.sort_values(by='total_score', ascending=False).head(top_n)
    
    logging.info("Pipeline finished.")
    return top_candidates[cols_to_display].reset_index(drop=True)
