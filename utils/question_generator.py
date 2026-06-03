from prompts.question_prompts import question_generation_prompt

def generate_questions(llm, job_role: str, resume_summary: str, job_description: str = "", num_questions: int = 5):
    """
    Generates interview questions using the provided LLM and input parameters.
    Returns a list of question strings.
    """
    chain = question_generation_prompt | llm
    
    response = chain.invoke({
        "job_role": job_role,
        "resume_summary": resume_summary,
        "job_description": job_description,
        "num_questions": num_questions
    })
    
    # Parse the response into a list of strings
    content = response.content if hasattr(response, 'content') else str(response)
    
    # Simple split by newline and filter out empty lines or non-numbered lines
    lines = content.split('\n')
    questions = []
    for line in lines:
        line = line.strip()
        # If the line starts with a number (e.g., "1. What is..."), it's likely a question
        if line and line[0].isdigit():
            questions.append(line)
        # Fallback if the LLM doesn't use numbers but output bullet points
        elif line.startswith('- ') or line.startswith('* '):
            questions.append(line[2:].strip())
            
    # Fallback if parsing fails to find individual questions
    if not questions:
        # Just split by double newline as a fallback block
        questions = [q for q in content.split('\n\n') if q.strip()]
        
    return questions
