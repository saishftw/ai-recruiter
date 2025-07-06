import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from core.matching import (
    fuzzy_match,
    weighted_fuzzy_qualification_score,
    weighted_fuzzy_skill_score,
)
from models.data_models import Education, Skill
from models.enums import ImportanceLevel


def test_title_score():
    jd_title = "Software Engineer"
    candidate_title = "Senior Software Developer"
    scores = fuzzy_match([candidate_title], [jd_title])
    best_score = np.max(scores)

    score = float(best_score)
    assert 60.0 <= score <= 100.0

def test_weighted_skill_score():
    jd_skills = [
        Skill(skill="Python", priority=ImportanceLevel.ESSENTIAL, proficiency_level=None),
        Skill(skill="AWS", priority=ImportanceLevel.IMPORTANT, proficiency_level=None)
    ]
    candidate_skills = ["Python", "Flask", "AWS"]

    results = weighted_fuzzy_skill_score("C001", jd_skills, candidate_skills)
    assert 0.5 < results["score"] <= 1.0


def test_weighted_qualification_score():
    jd_qual = [Education(degree="Bachelor", field="Computer Science", priority=ImportanceLevel.ESSENTIAL)]
    cand_qual = {"degrees": ["Bachelor"], "fields": ["Computer Applications"]}

    results = weighted_fuzzy_qualification_score("C002", jd_qual, cand_qual, score_threshold=60)
    assert results["score"] > 0.0

def test_qualification_higher_degree():
    jd_qual = [Education(degree="Bachelor", field="Computer Science", priority=ImportanceLevel.ESSENTIAL)]
    cand_qual = {"degrees": ["Master"], "fields": ["Computer Science"]}
    results = weighted_fuzzy_qualification_score("C003", jd_qual, cand_qual, score_threshold=60)
    assert results["score"] > 0.0
    assert "Master in Computer Science" in results["matched_qualifications"]


def test_embedding_similarity(model = 'all-mpnet-base-v2'):
    model = SentenceTransformer(model)

    jd_text = "Develop web applications using React and Node.js"
    cand_text = "Built several full-stack apps with React and Node.js"

    jd_emb = model.encode(jd_text, convert_to_tensor=True).cpu()
    cand_emb = model.encode(cand_text, convert_to_tensor=True).cpu()
    
    score = cos_sim(jd_emb, cand_emb).item()
    assert score > 0.5

def test_no_overlap_title():
    jd_title = "Accountant"
    candidate_title = "Software Engineer"
    scores = fuzzy_match([candidate_title], [jd_title])
    best_score = np.max(scores)
    assert float(best_score) < 40.0

def test_no_overlap_skills():
    jd_skills = [
        Skill(skill="Java", priority=ImportanceLevel.ESSENTIAL, proficiency_level=None)
    ]
    candidate_skills = ["Python", "AWS"]
    results = weighted_fuzzy_skill_score("C004", jd_skills, candidate_skills)
    assert results["score"] == 0.0

def test_no_overlap_qualifications():
    jd_qual = [Education(degree="PhD", field="Physics", priority=ImportanceLevel.ESSENTIAL)]
    cand_qual = {"degrees": ["Bachelor"], "fields": ["History"]}
    results = weighted_fuzzy_qualification_score("C005", jd_qual, cand_qual, score_threshold=60)
    assert results["score"] == 0.0

def test_empty_inputs():
    assert fuzzy_match([""], [""])[0][0] == 0.0
    results = weighted_fuzzy_skill_score("C006", [], [])
    assert results["score"] == 0.0
    results = weighted_fuzzy_qualification_score("C007", [], {"degrees": [], "fields": []}, score_threshold=60)
    assert results["score"] == 0.0

def test_partial_match_typo():
    jd_skills = [
        Skill(skill="Python", priority=ImportanceLevel.ESSENTIAL, proficiency_level=None)
    ]
    candidate_skills = ["Pythn"]  # typo
    results = weighted_fuzzy_skill_score("C008", jd_skills, candidate_skills)
    assert results["score"] == 1.0

    jd_title = "Data Scientist"
    candidate_title = "Data Scintist"  # typo
    scores = fuzzy_match([candidate_title], [jd_title])
    assert 80.0 < np.max(scores) < 100.0

def test_importance_level_variations():
    jd_skills = [
        Skill(skill="Python", priority=ImportanceLevel.SUPPLEMENTARY, proficiency_level=None),
        Skill(skill="AWS", priority=ImportanceLevel.IMPORTANT, proficiency_level=None),
        Skill(skill="Docker", priority=ImportanceLevel.ESSENTIAL, proficiency_level=None)
    ]
    candidate_skills = ["Python", "AWS", "Docker"]
    results = weighted_fuzzy_skill_score("C009", jd_skills, candidate_skills)
    assert 0.5 < results["score"] <= 1.0

    jd_qual = [
        Education(degree="Bachelor", field="CS", priority=ImportanceLevel.SUPPLEMENTARY),
        Education(degree="Master", field="CS", priority=ImportanceLevel.IMPORTANT),
        Education(degree="PhD", field="CS", priority=ImportanceLevel.ESSENTIAL)
    ]
    cand_qual = {"degrees": ["PhD", "Master", "Bachelor"], "fields": ["CS", "CS", "CS"]}
    results = weighted_fuzzy_qualification_score("C010", jd_qual, cand_qual, score_threshold=60)
    assert results["score"] > 0.0

def test_embedding_low_similarity(model = 'all-mpnet-base-v2'):
    model = SentenceTransformer(model)
    jd_text = "Develop web applications using React and Node.js"
    cand_text = "Manage financial accounts and prepare tax documents"
    jd_emb = model.encode(jd_text, convert_to_tensor=True).cpu()
    cand_emb = model.encode(cand_text, convert_to_tensor=True).cpu()
    score = cos_sim(jd_emb, cand_emb).item()
    assert score < 0.3
