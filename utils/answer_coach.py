from prompts.coach_prompts import star_coach_prompt, chat_coach_system_prompt
from langchain.schema import SystemMessage, HumanMessage, AIMessage

def generate_star_guidance(llm, job_role: str, question: str, resume_summary: str) -> str:
    """
    Generates personalized STAR interview answer guidance for a specific question.
    """
    chain = star_coach_prompt | llm
    
    response = chain.invoke({
        "job_role": job_role,
        "question": question,
        "resume_summary": resume_summary if resume_summary else "No resume uploaded. Provide general STAR guidance."
    })
    
    return response.content if hasattr(response, 'content') else str(response)

def get_coach_chat_response(llm, chat_history: list, job_role: str, resume_summary: str) -> str:
    """
    Handles interactive chat with Coach Alex.
    chat_history is a list of dicts: [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}]
    """
    system_content = chat_coach_system_prompt.format(
        job_role=job_role if job_role else "General Tech Role",
        resume_summary=resume_summary if resume_summary else "No resume uploaded yet."
    )
    
    messages = [SystemMessage(content=system_content)]
    
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
            
    response = llm.invoke(messages)
    return response.content if hasattr(response, 'content') else str(response)
