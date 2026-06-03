# AI Interview Coach

A full-stack AI Interview Coach web application built with Python, Streamlit, and LangChain.

## Features
- **Resume Upload**: Parses PDF and DOCX resumes.
- **Job Role Selection**: Tailor questions based on standard or custom roles and job descriptions.
- **AI Question Generation**: Generates relevant behavioral, technical, and situational questions.
- **Answer Evaluation**: Provides scores and feedback on relevance, structure, depth, and communication.
- **Voice Support**: Answer questions using your microphone (uses SpeechRecognition).
- **Final Report**: Overall score and summary.

## Setup Instructions

1. **Clone or Navigate** to the project directory.
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your API keys. You can choose to use Google Gemini (`MODEL_PROVIDER=gemini`) or OpenAI (`MODEL_PROVIDER=openai`).
5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Open the app in your browser (usually `http://localhost:8501`).
2. Go to **Step 1** to upload your resume and enter the target job role.
3. Click "Generate Interview Questions".
4. Go to **Step 2** to answer the questions. You can type your answer or record it using your microphone.
5. Review immediate feedback in **Step 3** and your final report in **Step 4**.

## Figure
[User Interface] (Screenshot 2026-06-03 163624.png)
