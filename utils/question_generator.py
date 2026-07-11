import random
from prompts.question_prompts import question_generation_prompt

SESSION_THEMES = [
    "Probing architectural trade-offs, scalability bottlenecks, and technical decisions made in past projects",
    "Investigating edge cases, failure recovery, debugging production incidents, and system resilience",
    "Exploring cross-functional collaboration, technical leadership, and navigating engineering disagreements",
    "Deep-dive into code maintainability, testing strategies, clean design patterns, and performance optimization",
    "Focusing on real-world constraints, deadline trade-offs, prioritization, and technical debt management",
    "Evaluating deep mastery of underlying frameworks, data structures, and foundational principles mentioned on the resume",
    "Challenging the candidate on alternative approaches they could have taken on their top resume achievements",
    "Probing security considerations, data integrity, and robustness in systems they built",
    "Examining communication of complex technical concepts to non-technical stakeholders and leadership",
    "Investigating end-to-end system ownership, deployment pipelines, and operational readiness",
    "Focusing on high-impact quantitative outcomes, metrics optimization, and data-driven engineering decisions",
    "Testing problem-solving adaptability under ambiguity and shifting product requirements"
]

def generate_questions(
    llm, 
    job_role: str, 
    resume_summary: str, 
    job_description: str = "", 
    num_questions: int = 5,
    focus_style: str = "Dynamic & Balanced (Variety of behavioral, technical, & curveball)",
    difficulty_level: str = "Standard / Realistic"
):
    """
    Generates tailored, non-repetitive interview questions using the provided LLM and input parameters.
    Returns a list of question strings.
    """
    chain = question_generation_prompt | llm
    
    # Pick a random session inquiry theme to guarantee fresh, non-repetitive questions on every run
    session_theme = random.choice(SESSION_THEMES)
    
    response = chain.invoke({
        "job_role": job_role,
        "resume_summary": resume_summary,
        "job_description": job_description,
        "num_questions": num_questions,
        "focus_style": focus_style,
        "difficulty_level": difficulty_level,
        "session_theme": session_theme
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
        # Fallback if the LLM output bullet points
        elif line.startswith('- ') or line.startswith('* '):
            questions.append(line[2:].strip())
            
    # Fallback if parsing fails to find individual numbered questions
    if not questions:
        questions = [q.strip() for q in content.split('\n\n') if q.strip()]
        
    return questions[:num_questions]
