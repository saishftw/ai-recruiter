from models.data_models import JobRoleSchema


def build_jd_embedding_input(jd_data: JobRoleSchema):
    parts = []

    if jd_data.role:
        parts.append(f"Role: {jd_data.role}")

    if jd_data.responsibilities:
        parts.append("Responsibilities: " + ", ".join(jd_data.responsibilities))

    if jd_data.role_objectives:
        parts.append("Career Objective: " + ", ".join(jd_data.role_objectives))

    if jd_data.skills:
        parts.append("Skills: " + ", ".join([s.skill for s in jd_data.skills]))

    if jd_data.technologies:
        parts.append("Technologies: " + ", ".join([t.technology for t in jd_data.technologies]))

    return " ".join(parts)