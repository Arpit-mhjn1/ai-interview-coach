from langchain_core.prompts import PromptTemplate

QUESTION_GENERATION_TEMPLATE = """
You are an elite, highly discerning technical and behavioral interviewer conducting a realistic interview for a {job_role} position.

Candidate Resume Summary:
{resume_summary}

Target Job Description (if provided):
{job_description}

INTERVIEW CONFIGURATION:
- Focus Category / Style: {focus_style}
- Interview Rigor / Difficulty Level: {difficulty_level}
- Session Unique Inquiry Angle: {session_theme}

CRITICAL ANTI-REPETITION & DIVERSITY INSTRUCTIONS:
1. NEVER generate boilerplate or cliché interview questions (e.g., avoid generic questions like "Tell me about yourself", "Tell me about a time you faced a challenge", or "What are your strengths and weaknesses").
2. EVERY question MUST specifically reference concrete details from the candidate's uploaded resume—such as specific project names, technologies, companies, or quantifiable achievements mentioned in their text.
3. Vary the inquiry angles across questions based on the selected Focus Category ({focus_style}) and Difficulty Level ({difficulty_level}).
4. Ensure each question feels fresh, challenging, realistic, and tailored to probe deeper than surface-level claims.

Generate exactly {num_questions} unique interview questions formatted strictly as a numbered list (e.g. 1. Question text...). Do NOT include any introductory or concluding markdown text.
"""

question_generation_prompt = PromptTemplate(
    input_variables=["job_role", "resume_summary", "job_description", "num_questions", "focus_style", "difficulty_level", "session_theme"],
    template=QUESTION_GENERATION_TEMPLATE,
)
