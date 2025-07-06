from models.enums import ImportanceLevel

attribute_weight_by_importance = {
    ImportanceLevel.ESSENTIAL: 1.0,
    ImportanceLevel.IMPORTANT: 0.7,
    ImportanceLevel.VALUABLE: 0.4,
    ImportanceLevel.SUPPLEMENTARY: 0.2
}

degree_norm_map = {
    "bachelor": [
        "b.e", "be", "b.tech", "btech", "b.sc", "bsc", "b.a", "ba", "b.com", "bcom",
        "bba", "bca", "b.arch", "barch", "b.pharm", "bpharm", "b.ed", "bed", "bfa",
        "b.des", "bdes", "b.lit", "blit", "b.s", "bs", "b.eng", "beng", "b.engg", "bengg",
        "bachelors", "bachelor", "undergraduate", "ug", "licentiate", "bacharelado"
    ],
    "master": [
        "m.e", "me", "m.tech", "mtech", "m.sc", "msc", "m.a", "ma", "m.com", "mcom",
        "mba", "mca", "m.arch", "march", "m.pharm", "mpharm", "m.ed", "med", "mfa",
        "m.des", "mdes", "m.lit", "mlit", "m.s", "ms", "m.eng", "meng", "m.engg", "mengg",
        "masters", "master", "postgraduate", "pg", "post grad", "post-graduate", "magister"
    ],
    "phd": [
        "ph.d", "phd", "d.phil", "dphil", "doctorate", "doctoral", "dr.", "dr",
        "sc.d", "scd", "eng.d", "engd", "edd", "dba"
    ],
    "associate": [
        "associate", "a.a", "aa", "a.s", "as", "a.sc", "asc", "a.a.s", "aas"
    ],
    "diploma": [
        "diploma", "advanced diploma", "postgraduate diploma", "pg diploma", "pgd", "post diploma",
        "polytechnic", "certificate", "post-baccalaureate diploma", "post baccalaureate diploma"
    ],
    "highschool": [
        "high school", "secondary school", "hsc", "ssc", "10th", "12th", "intermediate", "matriculation",
        "matric", "senior secondary", "pre-university", "pu", "pu college", "a-levels", "alevels", "o-levels", "olevels"
    ],
    "other": [
        "postdoc", "post doctoral", "post-doctoral", "post doctorate", "post-doctorate",
        "certificate course", "vocational", "trade school", "training", "bootcamp"
    ]
}

# need to adjust weights after eval
candidate_score_weights = {
    'title_score': 0.25,
    'skill_score': 0.25,
    'qualification_score': 0.05,
    'similarity_score': 0.45
}