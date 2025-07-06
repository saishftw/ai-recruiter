from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts.email_generation import system_prompt, user_prompt

load_dotenv('./.env')
genai_client = genai.Client()

def generate_email(jd: str, candidate_json_str: str):
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt.format(
                **{"job_desc": jd, "selected_candidate": candidate_json_str}
            ),
            config=types.GenerateContentConfig(
                temperature=0.4,
                system_instruction=system_prompt
            )
        )
        if response and response.text:
            return response.text
        else:
            raise ValueError("response is empty")
    except:
        raise