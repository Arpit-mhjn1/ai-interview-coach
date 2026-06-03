from langchain_core.prompts import PromptTemplate

QUESTION_GENERATION_TEMPLATE = """
You are an expert interviewer for {job_role} positions.
Based on the candidate's resume: 
{resume_summary}

If the candidate provided a job description, keep it in mind:
{job_description}

Generate {num_questions} interview questions that:
- Include behavioral questions
- Include technical questions relevant to their experience and the role
- Include situational/problem-solving questions

Return your response strictly as a numbered list of questions. Do not include introductory text, just the numbered list.
"""

question_generation_prompt = PromptTemplate(
    input_variables=["job_role", "resume_summary", "job_description", "num_questions"],
    template=QUESTION_GENERATION_TEMPLATE,
)
