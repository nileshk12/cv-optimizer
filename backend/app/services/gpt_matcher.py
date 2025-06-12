import os
from openai import AzureOpenAI  # ✅ NEW SDK import
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI client using new SDK
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

# Deployment name
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

def gpt_skill_match(resume_text, jd_text):
    """
    Calls Azure OpenAI to extract skills, compare and suggest improvements.
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

Extract:
1. Resume skills.
2. JD skills.
3. Missing skills.
4. Suggestions.

Return valid JSON format only:
{{
  "resume_skills": [...],
  "jd_skills": [...],
  "missing_skills": [...],
  "suggestions": "..."
}}
"""

    response = client.chat.completions.create(
        model=AZURE_DEPLOYMENT_NAME,   # ✅ Correct new syntax
        messages=[
            {"role": "system", "content": "You are a highly skilled recruiter and resume optimization AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content

