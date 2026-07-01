from prompts.prep_agent_prompts import prep_agent_prompt

def get_prep_guidance(llm, job_role: str, resume_summary: str, question: str, user_request: str) -> str:
    """
    Generates personalized interview preparation advice and hints for a candidate
    before they answer a specific interview question.
    """
    chain = prep_agent_prompt | llm
    
    response = chain.invoke({
        "job_role": job_role,
        "resume_summary": resume_summary if resume_summary else "No resume provided.",
        "question": question,
        "user_request": user_request
    })
    
    content = response.content if hasattr(response, 'content') else str(response)
    return content.strip()
