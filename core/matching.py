import numpy as np
from rapidfuzz import fuzz, process, utils

from core.normalization import normalize_degree
from models.data_models import Education, Skill
from models.mappings import attribute_weight_by_importance


def fuzzy_match(set1: list[str], set2: list[str], scorer=fuzz.token_set_ratio):
    return process.cdist(
        set1, 
        set2, 
        scorer=scorer,
        processor=utils.default_process
    )


def weighted_fuzzy_skill_score(candidate_id: str, jd_skills: list[Skill], candidate_skills: list[str], score_threshold=80):
    if not jd_skills or not candidate_skills:
        return {
            "score": 0.0,
            "matched_skills": []
        }
    
    candidate_score = 0.0
    matched_skills = []

    total_possible_score = sum(attribute_weight_by_importance[s.priority] for s in jd_skills)

    if total_possible_score == 0:
        return {
            "score": 0.0,
            "matched_skills": []
        }

    for jd_skill in jd_skills:
        jd_skill_name = jd_skill.skill.lower().strip()
        jd_weight = attribute_weight_by_importance.get(jd_skill.priority, 0.0)

        # Compare JD skill against all candidate skills
        match_scores = fuzzy_match([jd_skill_name], candidate_skills)
        # best_score = np.max(match_scores)
        scores = match_scores[0]

        best_idx = np.argmax(scores)
        best_score = scores[best_idx]
                
        if best_score >= score_threshold:
            candidate_score += jd_weight

            matched_skill = candidate_skills[best_idx]
            matched_skills.append(matched_skill)
            
            # print matched skills:
            # print("JD Skill: " + jd_skill_name)
            # print("Candidate: " + candidate_id)
            # matched_skills_indices = np.where(match_scores[0] > score_threshold)[0]
            # for idx in matched_skills_indices:
            #     print(f"Skill: {candidate_skills[idx]}, Score: {match_scores[0][idx]}")

            # print("")

    return {
        "score": candidate_score / total_possible_score,
        "matched_skills": list(set(matched_skills))
    }


def weighted_fuzzy_qualification_score(candidate_id: str, jd_qualifications: list[Education] | None, candidate_qualifications, score_threshold=60):
    if not jd_qualifications or not candidate_qualifications:
        return {
            "score": 0.0,
            "matched_qualifications": []
        }

    degree_hierarchy = ["highschool", "diploma", "associate", "bachelor", "master", "phd"]
    def degree_rank(degree):
        try:
            return degree_hierarchy.index(degree)
        except ValueError:
            return -1  # treat unknown as lowest

    matched_qualifications = []
    candidate_score = 0.0
    total_possible_score = sum(attribute_weight_by_importance[s.priority] for s in jd_qualifications)
    if total_possible_score == 0:
        return {
            "score": 0.0,
            "matched_qualifications": []
        }
    
    candidate_degrees = candidate_qualifications["degrees"]
    candidate_fields = candidate_qualifications["fields"]
    candidate_degrees_norm = [normalize_degree(deg) for deg in candidate_degrees]

    for jd_qualification in jd_qualifications:
        jd_degree_norm = normalize_degree(jd_qualification.degree)
        jd_degree_rank = degree_rank(jd_degree_norm)

        # find candidate degrees that meet or exceed the min required degree
        eligible_indices = [
            idx for idx, cand_deg_norm in enumerate(candidate_degrees_norm)
            if degree_rank(cand_deg_norm) >= jd_degree_rank and jd_degree_rank != -1
        ]

        if not eligible_indices:
            continue

        jd_weight = attribute_weight_by_importance.get(jd_qualification.priority, 0.0)

        # Compare JD field against eligible candidate fields
        eligible_fields = [candidate_fields[idx] for idx in eligible_indices]

        if jd_qualification.field:
            match_scores = fuzzy_match([jd_qualification.field], eligible_fields)
            scores = match_scores[0]

            best_idx = np.argmax(scores)
            best_score = scores[best_idx]

            if best_score >= score_threshold:
                candidate_score += jd_weight

                matched_degree = candidate_degrees[eligible_indices[best_idx]]
                matched_field = candidate_fields[eligible_indices[best_idx]]

                matched_qualifications.append(f"{matched_degree} in {matched_field}")

    return {
        "score": candidate_score / total_possible_score,
        "matched_qualifications": matched_qualifications
    }
