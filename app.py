import streamlit as st
from src.generator import compile_quiz_data
from src.database import setup_and_populate_db

# 1. MUST BE FIRST: Set page configurations
st.set_page_config(page_title="Sports Quiz Agent", page_icon="🏆", layout="centered")

# 2. Inject standard custom styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .stTextArea textarea {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Initialize/Warm-up database
@st.cache_resource
def prepare_knowledge_base():
    setup_and_populate_db()

prepare_knowledge_base()

# 4. Main UI Content
st.title("AI-Powered Sports Quiz Generator")
st.write("Generates factually grounded sports quizzes using Gemini, ChromaDB, and Live Web Search.")

st.sidebar.header("Quiz Settings")
sport_choice = st.sidebar.selectbox("Select Sport", ["Cricket", "Football", "Badminton", "Tennis"])
difficulty = st.sidebar.select_slider("Select Difficulty", options=["Easy", "Medium", "Hard"])

if "quiz_output" not in st.session_state:
    st.session_state.quiz_output = None
    st.session_state.quiz_context = None

if st.sidebar.button("Generate Fresh Quiz", use_container_width=True):
    with st.spinner("Fetching facts and querying Gemini..."):
        try:
            quiz_text, context_used = compile_quiz_data(sport_choice, difficulty)
            st.session_state.quiz_output = quiz_text
            st.session_state.quiz_context = context_used
            st.success("Quiz created successfully!")
        except Exception as e:
            st.error(f"Failed to generate quiz: {e}")

if st.session_state.quiz_output:
    st.subheader(f"Current Quiz: {sport_choice} ({difficulty})")
    st.text_area("Generated Quiz", value=st.session_state.quiz_output, height=450)

    with st.expander("Inspect Ground Truth Context"):
        st.code(st.session_state.quiz_context, language="markdown")