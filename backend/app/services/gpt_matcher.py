import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI specific configurations
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Your deployment name (model deployment inside Azure OpenAI)
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

def gpt_skill_match(resume_text, jd_text):
    """
    Calls Azure OpenAI GPT model to extract skills, compare, and suggest improvements.
    """
    prompt = f"""
You are an expert AI technical recruiter.

Here is the candidate's resume:
\"\"\"
{resume_text}
\"\"\"

Here is the job description:
\"\"\"
{jd_text}
\"\"\"

Your task:
1. Extract important technical skills from the resume.
2. Extract important skills required from the job description.
3. Identify missing skills.
4. Suggest how the candidate can improve the resume to better match the job.

Return your response ONLY in valid JSON as:
{{
  "resume_skills": [...],
  "jd_skills": [...],
  "missing_skills": [...],
  "suggestions": "your improvement suggestions"
}}
"""

    response = openai.ChatCompletion.create(
        engine=AZURE_DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content

