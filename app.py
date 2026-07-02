import streamlit as st
import os
from config import APP_TITLE, PAGE_ICON, DEFAULT_ROLES, get_llm
from utils.resume_parser import parse_resume, extract_key_info
from utils.question_generator import generate_questions
from utils.answer_evaluator import evaluate_answer
from utils.speech_to_text import transcribe_audio_bytes
from utils.prep_agent import get_prep_guidance

# --- Page Config ---
st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="wide")

# --- Custom Styling (Rich Aesthetics & Glassmorphism) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* App Header & Title */
h1, h2, h3 {
    font-weight: 700 !important;
    background: linear-gradient(135deg, #c084fc 0%, #818cf8 50%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Expander Styling (AI Prep Coach & Others) */
[data-testid="stExpander"] {
    border: 1px solid rgba(168, 85, 247, 0.45) !important;
    border-radius: 16px !important;
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.45) 0%, rgba(15, 23, 42, 0.75) 100%) !important;
    box-shadow: 0 10px 30px -10px rgba(168, 85, 247, 0.35) !important;
    backdrop-filter: blur(14px) !important;
    overflow: hidden !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    margin: 18px 0 !important;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(192, 132, 252, 0.85) !important;
    box-shadow: 0 15px 35px -5px rgba(168, 85, 247, 0.5) !important;
    transform: translateY(-2px);
}

[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    color: #f8fafc !important;
    padding: 16px 20px !important;
    background: rgba(168, 85, 247, 0.18) !important;
    border-bottom: 1px solid rgba(168, 85, 247, 0.25) !important;
}

[data-testid="stExpander"] summary:hover {
    color: #c084fc !important;
}

/* Buttons */
[data-testid="stButton"] button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.3s ease !important;
    border: 1px solid rgba(168, 85, 247, 0.35) !important;
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(99, 102, 241, 0.15) 100%) !important;
    color: #e2e8f0 !important;
}

[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(168, 85, 247, 0.45) !important;
    border-color: #c084fc !important;
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.35) 0%, rgba(99, 102, 241, 0.35) 100%) !important;
    color: #ffffff !important;
}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 12px !important;
    background: rgba(15, 23, 42, 0.7) !important;
    padding: 10px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px) !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    transition: all 0.2s ease !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 15px rgba(168, 85, 247, 0.45) !important;
}

/* Info & Alerts */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid rgba(168, 85, 247, 0.35) !important;
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.5) 0%, rgba(15, 23, 42, 0.85) 100%) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25) !important;
    backdrop-filter: blur(10px) !important;
}

/* Text Areas and Inputs */
[data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input {
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    background: rgba(15, 23, 42, 0.6) !important;
    color: #f8fafc !important;
}

[data-testid="stTextArea"] textarea:focus, [data-testid="stTextInput"] input:focus {
    border-color: #c084fc !important;
    box-shadow: 0 0 12px rgba(168, 85, 247, 0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = {}  # {question_idx: answer_text}
if 'evaluations' not in st.session_state:
    st.session_state.evaluations = {} # {question_idx: evaluation_dict}
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 0
if 'prep_advice' not in st.session_state:
    st.session_state.prep_advice = {} # {question_idx: prep_advice_text}
if 'job_role' not in st.session_state:
    st.session_state.job_role = ""

# --- Sidebar Configuration ---
with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.markdown("### Info")
    st.info("Using Groq Llama 3 for ultra-fast, free generation.")

# --- Main App Logic ---
st.title(f"{PAGE_ICON} {APP_TITLE}")

# Tab navigation to simulate steps
tab1, tab2, tab3, tab4 = st.tabs(["1. Setup Profile", "2. Interview", "3. Feedback", "4. Final Report"])

with tab1:
    st.header("Step 1: Resume & Role Setup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Resume")
        uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
        
        if uploaded_file is not None:
            try:
                with st.spinner("Parsing resume..."):
                    text = parse_resume(uploaded_file)
                    st.session_state.resume_text = text
                st.success("Resume parsed successfully!")
                with st.expander("View Parsed Text"):
                    st.text_area("Parsed Content", st.session_state.resume_text, height=200, disabled=True)
            except Exception as e:
                st.error(f"Error parsing file: {str(e)}")

    with col2:
        st.subheader("Target Job Role")
        selected_role = st.selectbox("Select a Job Role", DEFAULT_ROLES)
        custom_role = ""
        if selected_role == "Custom...":
            custom_role = st.text_input("Enter Custom Job Role")
        
        final_role = custom_role if selected_role == "Custom..." else selected_role
        
        job_description = st.text_area("Job Description (Optional)", placeholder="Paste the job description here to tailor the questions even more.")
        num_qs = st.slider("Number of Questions", min_value=3, max_value=10, value=5)

    if st.button("Generate Interview Questions", type="primary"):
        if not st.session_state.resume_text:
            st.warning("Please upload a resume first.")
        elif not final_role:
            st.warning("Please specify a job role.")
        else:
            try:
                llm = get_llm()
                with st.spinner("Generating tailored questions..."):
                    questions = generate_questions(
                        llm=llm,
                        job_role=final_role,
                        resume_summary=st.session_state.resume_text[:8000], # truncating for safety
                        job_description=job_description,
                        num_questions=num_qs
                    )
                    st.session_state.questions = questions
                    # Reset interview state
                    st.session_state.answers = {}
                    st.session_state.evaluations = {}
                    st.session_state.current_question_idx = 0
                    st.session_state.prep_advice = {}
                    st.session_state.job_role = final_role
                st.success(f"Generated {len(questions)} questions! Head to the 'Interview' tab.")
            except Exception as e:
                st.error(f"Error generating questions: {str(e)}. Make sure your API key is correct.")


with tab2:
    st.header("Step 2: Mock Interview")
    
    if not st.session_state.questions:
        st.info("Please generate questions in the Setup Profile tab first.")
    else:
        q_idx = st.session_state.current_question_idx
        
        if q_idx < len(st.session_state.questions):
            st.progress((q_idx) / len(st.session_state.questions))
            st.markdown(f"### Question {q_idx + 1} of {len(st.session_state.questions)}")
            st.info(st.session_state.questions[q_idx])
            
            # --- Personalized AI Answer Prep Agent ---
            with st.expander("🤖✨ Personal AI Answer Prep Coach — Click for Custom Hints, Resume Points & STAR Outlines!", expanded=False):
                st.markdown("""
                <div style="padding: 14px 18px; background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%); border-radius: 12px; border-left: 4px solid #a855f7; margin-bottom: 18px;">
                    <p style="margin: 0; font-size: 0.98rem; color: #f8fafc; line-height: 1.5;">
                        💡 <b>Your Personal AI Mentor is ready!</b> I have analyzed your resume and target role. Click any button below for instant, one-click tailored advice, or ask me any custom preparation question!
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                prep_col1, prep_col2, prep_col3 = st.columns(3)
                with prep_col1:
                    if st.button("🎯 Suggest Resume Points", key=f"prep_btn1_{q_idx}"):
                        with st.spinner("Coach is analyzing your resume..."):
                            try:
                                llm = get_llm()
                                advice = get_prep_guidance(llm, st.session_state.get('job_role', final_role), st.session_state.resume_text, st.session_state.questions[q_idx], "What specific projects or experiences from my resume should I highlight to answer this question effectively?")
                                st.session_state.prep_advice[q_idx] = f"**🎯 Recommended Resume Talking Points:**\n\n{advice}"
                            except Exception as e:
                                st.error(f"Error getting advice: {e}")
                with prep_col2:
                    if st.button("📐 STAR Method Outline", key=f"prep_btn2_{q_idx}"):
                        with st.spinner("Coach is structuring STAR template..."):
                            try:
                                llm = get_llm()
                                advice = get_prep_guidance(llm, st.session_state.get('job_role', final_role), st.session_state.resume_text, st.session_state.questions[q_idx], "Provide a customized STAR (Situation, Task, Action, Result) template outline specifically tailored for answering this question using my background.")
                                st.session_state.prep_advice[q_idx] = f"**📐 Tailored STAR Method Outline:**\n\n{advice}"
                            except Exception as e:
                                st.error(f"Error getting advice: {e}")
                with prep_col3:
                    if st.button("💡 Key Technical Terms", key=f"prep_btn3_{q_idx}"):
                        with st.spinner("Coach is finding keywords..."):
                            try:
                                llm = get_llm()
                                advice = get_prep_guidance(llm, st.session_state.get('job_role', final_role), st.session_state.resume_text, st.session_state.questions[q_idx], "What key technical keywords, skills, or industry terms should I make sure to mention in my answer to impress the interviewer?")
                                st.session_state.prep_advice[q_idx] = f"**💡 Keywords & Technical Terms to Include:**\n\n{advice}"
                            except Exception as e:
                                st.error(f"Error getting advice: {e}")
                
                custom_prep_query = st.text_input("Or ask your AI Coach any custom question:", placeholder="e.g., How can I start my answer with a strong hook?", key=f"prep_input_{q_idx}")
                if st.button("Ask Coach", key=f"prep_ask_{q_idx}"):
                    if custom_prep_query:
                        with st.spinner("Coach is thinking..."):
                            try:
                                llm = get_llm()
                                advice = get_prep_guidance(llm, st.session_state.get('job_role', final_role), st.session_state.resume_text, st.session_state.questions[q_idx], custom_prep_query)
                                st.session_state.prep_advice[q_idx] = f"**💬 Coach Advice for '{custom_prep_query}':**\n\n{advice}"
                            except Exception as e:
                                st.error(f"Error getting advice: {e}")
                    else:
                        st.warning("Please type a question for the coach first.")
                
                if q_idx in st.session_state.prep_advice:
                    st.markdown("---")
                    st.info(st.session_state.prep_advice[q_idx], icon="✨")
            
            # Answer input methods
            st.write("#### Your Answer")
            
            # Text Input
            text_answer = st.text_area("Type your answer here:", height=150, key=f"text_ans_{q_idx}")
            
            # Voice Input
            st.write("Or use voice input:")
            audio_bytes = st.audio_input("Record your answer", key=f"audio_ans_{q_idx}")
            
            voice_transcription = ""
            if audio_bytes:
                with st.spinner("Transcribing audio..."):
                    voice_transcription = transcribe_audio_bytes(audio_bytes)
                st.success("Audio transcribed!")
                st.text_area("Transcription preview (you can edit this in the text box above if needed)", voice_transcription, height=100)
            
            final_answer = text_answer if text_answer else voice_transcription
            
            if st.button("Submit Answer & Evaluate"):
                if not final_answer:
                    st.warning("Please provide an answer via text or voice before submitting.")
                else:
                    st.session_state.answers[q_idx] = final_answer
                    try:
                        llm = get_llm()
                        with st.spinner("Evaluating your answer..."):
                            evaluation = evaluate_answer(
                                llm=llm,
                                job_role=final_role, # type: ignore (it's in the broader scope, but let's be careful)
                                question=st.session_state.questions[q_idx],
                                answer=final_answer
                            )
                            st.session_state.evaluations[q_idx] = evaluation
                        st.success("Answer evaluated! Check the 'Feedback' tab or proceed to next question.")
                        # Move to next question automatically if evaluated
                        st.session_state.current_question_idx += 1
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error evaluating answer: {str(e)}")
        else:
            st.success("You have completed all questions! Check the 'Final Report' tab.")
            if st.button("Restart Interview"):
                st.session_state.current_question_idx = 0
                st.rerun()


with tab3:
    st.header("Step 3: Instant Feedback")
    
    if not st.session_state.evaluations:
        st.info("Answer some questions to see feedback here.")
    else:
        # Display evaluations for answered questions
        for idx, eval_data in st.session_state.evaluations.items():
            with st.expander(f"Q{idx + 1}: {st.session_state.questions[idx]}", expanded=(idx == len(st.session_state.evaluations)-1)):
                st.markdown("**Your Answer:**")
                st.write(st.session_state.answers[idx])
                
                st.markdown("---")
                st.markdown("**Feedback:**")
                
                # Display scores in columns
                scores = eval_data.get('scores', {})
                cols = st.columns(5)
                cols[0].metric("Overall", f"{scores.get('overall', 'N/A')}/10")
                cols[1].metric("Relevance", f"{scores.get('relevance', 'N/A')}/10")
                cols[2].metric("Structure", f"{scores.get('structure', 'N/A')}/10")
                cols[3].metric("Depth", f"{scores.get('depth', 'N/A')}/10")
                cols[4].metric("Communication", f"{scores.get('communication', 'N/A')}/10")
                
                st.markdown(eval_data.get('raw_feedback', 'No detailed feedback available.'))


with tab4:
    st.header("Step 4: Final Report")
    
    if len(st.session_state.evaluations) < len(st.session_state.questions) or len(st.session_state.questions) == 0:
        st.info("Complete all interview questions to generate the final report.")
    else:
        st.success("Interview Complete! Here is your summary.")
        
        # Calculate overall averages
        total_overall = 0
        valid_scores_count = 0
        for eval_data in st.session_state.evaluations.values():
            score = eval_data.get('scores', {}).get('overall')
            if score is not None:
                total_overall += score
                valid_scores_count += 1
                
        final_average = round(total_overall / valid_scores_count, 1) if valid_scores_count > 0 else 0
        
        st.metric("Final Interview Score", f"{final_average}/10")
        
        if final_average >= 8:
            st.balloons()
            st.markdown("### Outstanding Performance! 🌟")
            st.write("You are well-prepared for this role.")
        elif final_average >= 6:
            st.markdown("### Good Job! 👍")
            st.write("You have a solid foundation, but there is room for improvement in some areas.")
        else:
            st.markdown("### Keep Practicing! 📚")
            st.write("Review the feedback carefully and practice your responses.")
            
        st.markdown("### Overall Recommendations")
        st.write("Review the specific feedback for each question in the 'Feedback' tab. Consider practicing the STAR method for behavioral questions and reviewing core concepts for technical questions.")
        
        # Optionally, we could use the LLM to generate a summary report here
        if st.button("Generate Detailed Summary (AI)"):
            try:
                llm = get_llm()
                all_feedback = "\n\n".join([f"Q: {st.session_state.questions[i]}\nFeedback: {st.session_state.evaluations[i]['raw_feedback']}" for i in range(len(st.session_state.evaluations))])
                summary_prompt = f"Based on the following interview feedback, generate a brief summary highlighting the candidate's top 2 strengths and 2 main areas for improvement.\n\nFeedback:\n{all_feedback}"
                with st.spinner("Generating summary..."):
                    summary_response = llm.invoke(summary_prompt)
                    st.write(summary_response.content)
            except Exception as e:
                st.error(f"Error generating summary: {str(e)}")

# --- Footer ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Built by <b>Arpit Website & App Studio</b></div>", unsafe_allow_html=True)
