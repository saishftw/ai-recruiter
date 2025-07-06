from rapidfuzz import process, fuzz
from models.mappings import degree_norm_map

TERM_TO_CATEGORY = {
    term: category
    for category, terms in degree_norm_map.items()
    for term in terms
}

all_terms = list(TERM_TO_CATEGORY.keys())


def normalize_degree(degree: str, threshold=80):
    # exact match (case-insensitive) first
    degree_lower = degree.lower().strip()
    for term, category in TERM_TO_CATEGORY.items():
        if degree_lower == term.lower():
            return category

    # fallback to fuzzy match
    match, score, _ = process.extractOne(degree, all_terms, scorer=fuzz.partial_ratio)

    if match and score >= threshold:
        return TERM_TO_CATEGORY[match]

    return degree
