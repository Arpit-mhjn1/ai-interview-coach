import PyPDF2
import docx
import io

def parse_pdf(file) -> str:
    """Extracts text from a PDF file."""
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def parse_docx(file) -> str:
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        raise Exception(f"Error reading DOCX: {str(e)}")

def parse_resume(file) -> str:
    """Routes the file to the correct parser based on extension."""
    filename = file.name.lower()
    
    if filename.endswith(".pdf"):
        return parse_pdf(file)
    elif filename.endswith(".docx"):
        return parse_docx(file)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")

def extract_key_info(text: str, llm) -> dict:
    """
    Optional: use LLM to extract structured info (skills, experience).
    For now, we just return the raw text to be used in the prompt.
    """
    # A full implementation might ask the LLM to summarize the resume here
    # to save tokens in subsequent calls, but passing raw text or a simple
    # summary is often sufficient if the model context window is large.
    return {
        "raw_text": text,
        "summary": text[:8000] # Simple truncation as a fallback
    }
