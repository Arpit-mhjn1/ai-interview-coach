import streamlit as st
import os
from config import APP_TITLE, PAGE_ICON, DEFAULT_ROLES, get_llm
from utils.resume_parser import parse_resume, extract_key_info
from utils.question_generator import generate_questions
from utils.answer_evaluator import evaluate_answer
from utils.speech_to_text import transcribe_audio_bytes
from utils.answer_coach import generate_star_guidance, get_coach_chat_response
from utils.ui_components import render_js_hero_header, render_js_interview_timer, render_js_radar_chart

# --- Page Config ---
st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="wide", initial_sidebar_state="auto")

# --- Mobile & Responsive & Global Theme Styling ---
st.markdown("""
<style>
    /* Global App Background matching Hero Banner (#0f172a Deep Slate / Indigo) */
    .stApp {
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    /* Ensure clean typography contrast */
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #f8fafc;
    }
    /* Aesthetic Tab Bar matching Hero Banner */
    div[data-baseweb="tab-list"] {
        background-color: rgba(30, 27, 75, 0.45) !important;
        border-radius: 12px;
        padding: 6px;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    div[data-baseweb="tab"] {
        color: #c7d2fe !important;
        font-weight: 600 !important;
    }
    div[aria-selected="true"] {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.35), rgba(99, 102, 241, 0.35)) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    /* Sidebar matching deep indigo aesthetic */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid rgba(139, 92, 246, 0.2);
    }

    /* Mobile & Tablet Layout Optimization */
    @media screen and (max-width: 768px) {
        .block-container {
            padding-top: 1.5rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            padding-bottom: 3rem !important;
        }
        /* Make primary buttons full-width and touch-friendly on mobile */
        div.stButton > button {
            width: 100% !important;
            min-height: 46px !important;
            font-size: 16px !important;
            border-radius: 10px !important;
        }
        /* Ensure font size >= 16px on inputs so iOS Safari does not auto-zoom */
        input, textarea, select {
            font-size: 16px !important;
        }
        /* Enable smooth horizontal scrolling for Streamlit tabs on mobile */
        div[data-baseweb="tab-list"] {
            gap: 4px;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            flex-wrap: nowrap !important;
        }
        div[data-baseweb="tab"] {
            padding: 8px 12px !important;
            font-size: 14px !important;
            white-space: nowrap !important;
        }
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
if 'coach_guidance' not in st.session_state:
    st.session_state.coach_guidance = {} # {question_idx: guidance_markdown}
if 'coach_chat_history' not in st.session_state:
    st.session_state.coach_chat_history = [] # list of {role, content}
if 'target_role' not in st.session_state:
    st.session_state.target_role = "Software Engineer"

# --- Sidebar Configuration ---
with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.markdown("### Info")
    st.info("Using Groq Llama 3 for ultra-fast, free generation.")

# --- Main App Logic ---
render_js_hero_header()
st.markdown("") # spacing

# Tab navigation to simulate steps
tab1, tab2, tab3, tab4, tab5 = st.tabs(["1. Setup", "2. Interview", "3. 🤖 Coach", "4. Feedback", "5. Report"])

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
        st.session_state.target_role = final_role
        
        job_description = st.text_area("Job Description (Optional)", placeholder="Paste the job description here to tailor the questions even more.")
        
        focus_style = st.selectbox(
            "Interview Focus Category",
            [
                "Dynamic & Balanced (Variety of behavioral, technical, & curveball)",
                "Deep Technical & System Architecture Probe",
                "Resume Project Deep-Dive (Line-by-Line Probe)",
                "Challenging Edge-Case & Curveball Scenarios",
                "Leadership & Behavioral (STAR Oriented)"
            ]
        )
        difficulty_level = st.selectbox(
            "Difficulty Rigor",
            [
                "Standard / Realistic",
                "Challenging / Senior Level",
                "High-Pressure FAANG Bar-Raiser"
            ]
        )
        num_qs = st.slider("Number of Questions", min_value=3, max_value=10, value=5)

    if st.button("Generate Interview Questions", type="primary"):
        if not st.session_state.resume_text:
            st.warning("Please upload a resume first.")
        elif not final_role:
            st.warning("Please specify a job role.")
        else:
            try:
                llm = get_llm()
                with st.spinner("Generating tailored, non-repetitive questions..."):
                    questions = generate_questions(
                        llm=llm,
                        job_role=final_role,
                        resume_summary=st.session_state.resume_text[:8000],
                        job_description=job_description,
                        num_questions=num_qs,
                        focus_style=focus_style,
                        difficulty_level=difficulty_level
                    )
                    st.session_state.questions = questions
                    # Reset interview state
                    st.session_state.answers = {}
                    st.session_state.evaluations = {}
                    st.session_state.current_question_idx = 0
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
            render_js_interview_timer()
            st.markdown(f"### Question {q_idx + 1} of {len(st.session_state.questions)}")
            st.info(st.session_state.questions[q_idx])
            
            # --- AI Coach Prep Section ---
            with st.expander("💡 Need Help Preparing Your Answer? Ask Your AI Coach"):
                st.markdown("Get custom STAR talking points tailored to your uploaded resume for this question.")
                if st.button("✨ Generate Personalized STAR Talking Points", key=f"coach_btn_{q_idx}"):
                    try:
                        llm = get_llm()
                        with st.spinner("Analyzing your resume and drafting STAR strategy..."):
                            guidance = generate_star_guidance(
                                llm=llm,
                                job_role=st.session_state.target_role,
                                question=st.session_state.questions[q_idx],
                                resume_summary=st.session_state.resume_text[:6000]
                            )
                            st.session_state.coach_guidance[q_idx] = guidance
                    except Exception as e:
                        st.error(f"Error generating coach guidance: {str(e)}")
                        
                if q_idx in st.session_state.coach_guidance:
                    st.markdown(st.session_state.coach_guidance[q_idx])
            
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
                                job_role=st.session_state.target_role,
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
    st.header("Step 3: 🤖 Personalized AI Prep Coach ('Coach Alex')")
    st.write("Chat with your personal AI mentor! Ask for help brainstorming answers, structuring your background, negotiating salary, or overcoming interview anxiety.")
    
    if not st.session_state.resume_text:
        st.warning("⚠️ For the most personalized advice, please upload your resume in Step 1!")
    
    # Display chat messages from history
    for message in st.session_state.coach_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Accept user input
    if prompt := st.chat_input("Ask Coach Alex anything (e.g., 'How do I explain my employment gap based on my resume?')..."):
        st.session_state.coach_chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Coach Alex is thinking..."):
                try:
                    llm = get_llm()
                    response = get_coach_chat_response(
                        llm=llm,
                        chat_history=st.session_state.coach_chat_history,
                        job_role=st.session_state.target_role,
                        resume_summary=st.session_state.resume_text[:6000]
                    )
                    st.markdown(response)
                    st.session_state.coach_chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error communicating with Coach Alex: {str(e)}")
    
    if st.session_state.coach_chat_history:
        st.markdown("---")
        if st.button("🗑️ Clear Coach Chat"):
            st.session_state.coach_chat_history = []
            st.rerun()


with tab4:
    st.header("Step 4: Instant Feedback")
    
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


with tab5:
    st.header("Step 5: Final Report")
    
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
        render_js_radar_chart(st.session_state.evaluations)
        
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
