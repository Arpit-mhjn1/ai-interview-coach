from prompts.evaluation_prompts import evaluation_prompt
import re

def evaluate_answer(llm, job_role: str, question: str, answer: str):
    """
    Evaluates the candidate's answer and extracts scores and feedback.
    """
    chain = evaluation_prompt | llm
    
    response = chain.invoke({
        "job_role": job_role,
        "question": question,
        "answer": answer
    })
    
    content = response.content if hasattr(response, 'content') else str(response)
    
    # Parse the text to extract scores (Relevance, Structure, Depth, Communication, Overall)
    # We will use simple regex to find patterns like "Relevance Score: 8/10"
    
    def extract_score(pattern, text):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    scores = {
        "relevance": extract_score(r"Relevance(?: Score)?:\s*([\d.]+)", content),
        "structure": extract_score(r"Structure(?: Score)?:\s*([\d.]+)", content),
        "depth": extract_score(r"Depth(?: Score)?:\s*([\d.]+)", content),
        "communication": extract_score(r"Communication(?: Score)?:\s*([\d.]+)", content),
        "overall": extract_score(r"Overall(?: Score)?:\s*([\d.]+)", content),
    }
    
    # If regex fails to find an overall score, calculate a simple average
    if scores["overall"] is None:
        valid_scores = [s for k, s in scores.items() if s is not None and k != "overall"]
        if valid_scores:
            scores["overall"] = round(sum(valid_scores) / len(valid_scores), 1)
        else:
            scores["overall"] = 0.0

    return {
        "raw_feedback": content,
        "scores": scores
    }
