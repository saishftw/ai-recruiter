import pandas as pd
from core.matching import fuzzy_match

def filter_by_job_title(df: pd.DataFrame, job_title: str, threshold: float = 0.6) -> pd.DataFrame:
    """
    Filters candidates by fuzzy matching their job position against a given job title.
    """
    df = df.copy()
    role_scores = fuzzy_match(df['job_position_name'].tolist(), [job_title])
    df['title_score'] = role_scores[:, 0] / 100
    return df[df['title_score'] >= threshold]
