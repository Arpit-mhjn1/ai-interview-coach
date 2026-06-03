from langchain_core.prompts import PromptTemplate

EVALUATION_TEMPLATE = """
You are an expert technical and behavioral interviewer evaluating a candidate for a {job_role} position.

Evaluate this interview answer:
Question: {question}
Answer: {answer}

Score the answer on these criteria (1-10 each):
1. Relevance: Does it directly address the question?
2. Structure: Is it well-organized (e.g., uses the STAR method if behavioral)?
3. Depth: Does it show sufficient expertise and experience?
4. Communication: Is it clear, professional, and concise?

Provide your evaluation in the following JSON-like structure (but just output plain text that can be easily parsed or read):

Relevance Score: <score>/10
Structure Score: <score>/10
Depth Score: <score>/10
Communication Score: <score>/10
Overall Score: <weighted average score>/10

Improvement Suggestions:
- <suggestion 1>
- <suggestion 2>

Model Answer Snippet:
<Provide a short example of an ideal way to answer this question>
"""

evaluation_prompt = PromptTemplate(
    input_variables=["job_role", "question", "answer"],
    template=EVALUATION_TEMPLATE,
)
