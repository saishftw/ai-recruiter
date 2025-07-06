import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from core.matching import weighted_fuzzy_skill_score, weighted_fuzzy_qualification_score
from core.embedding import build_jd_embedding_input
from models.data_models import Skill, JobRoleSchema
from models.mappings import candidate_score_weights

def calculate_skill_score(df: pd.DataFrame, jd: JobRoleSchema, filter: bool = False, threshold: float = 0.25) -> pd.DataFrame:
    jd_skills = jd.skills.copy()
    if jd.technologies:
        for t in jd.technologies:
            jd_skills.append(Skill(skill=t.technology, priority=t.priority, proficiency_level=None))
    
    skill_results = df.apply(
        lambda x: weighted_fuzzy_skill_score(x['candidate_id'], jd_skills, x['all_skills']),
        axis=1
    )
    
    skill_results_df = pd.DataFrame(skill_results.tolist())
    df['skill_score'] = skill_results_df['score']
    df['matched_skills'] = skill_results_df['matched_skills']

    if filter:
        df = df[df['skill_score'] >= threshold]
    return df

def calculate_qualification_score(df: pd.DataFrame, jd: JobRoleSchema, filter: bool = False, threshold: float = 0.2) -> pd.DataFrame:
    if jd.qualifications and jd.qualifications.education:
        qualification_results = df.apply(
            lambda x: weighted_fuzzy_qualification_score(
                x['candidate_id'], 
                jd.qualifications.education,# type: ignore
                {"degrees": x['degree_names_norm'], "fields": x['major_field_of_studies']} 
            ), axis=1)
        qualification_results_df = pd.DataFrame(qualification_results.tolist())
        df['qualification_score'] = qualification_results_df['score']
        df['matched_qualifications'] = qualification_results_df['matched_qualifications']
        if filter:
            df = df[df['qualification_score'] >= threshold]
    else:
        df['qualification_score'] = 0.0
    return df

def calculate_similarity_score(df: pd.DataFrame, jd: JobRoleSchema, model: SentenceTransformer) -> pd.DataFrame:
    jd_text = build_jd_embedding_input(jd)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True).cpu()
    candidate_embeddings = torch.stack([torch.tensor(vec) for vec in df['profile_embedding']])
    similarities = util.cos_sim(candidate_embeddings, jd_embedding).squeeze().cpu().numpy()
    df['similarity_score'] = similarities
    return df

def calculate_total_score(df: pd.DataFrame, jd: JobRoleSchema) -> pd.DataFrame:
    total_score = (
        candidate_score_weights['title_score'] * df['title_score'] +
        candidate_score_weights['skill_score'] * df['skill_score'] +
        candidate_score_weights['similarity_score'] * df['similarity_score']
    )
    if jd.qualifications and jd.qualifications.education:
        total_score += candidate_score_weights['qualification_score'] * df['qualification_score']
    df['total_score'] = total_score
    return df
