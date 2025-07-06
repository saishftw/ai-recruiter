from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts.jd_extraction import system_prompt, user_prompt
from models.data_models import JobRoleSchema

load_dotenv('./.env')
client = genai.Client()

def process_jd(jd: str):
    if not jd.strip():
        raise ValueError("No Job description provided")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=user_prompt.format(**{"job_desc": jd}),
            config=types.GenerateContentConfig(
                temperature=0.2,
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=JobRoleSchema,
            )
        )
        if response and response.text:
            output = JobRoleSchema.model_validate_json(response.text)
            return output
        else:
            raise ValueError("response.text is empty")
    except Exception as e:
        raise e

def load_sample_jd(path: str = './jd/sample_jd_01.txt') -> str:
    with open(path, 'r') as file:
        job_desc = file.read()
    return job_desc
