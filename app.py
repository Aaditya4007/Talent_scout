import streamlit as st
import google.generativeai as genai
from views.candidate import show_candidate_view
from views.recruiter import show_recruiter_view
from database import init_database
from translations import setup_translations, get_text
import os

# Initialize Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API Key not found. Please add it to your environment variables.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# Custom CSS
def load_css():
    st.markdown("""
        <style>
        /* Main styles */
        .stApp {
            font-family: 'Inter', sans-serif;
        }

        /* Headers */
        h1, h2, h3 {
            font-weight: 600 !important;
            color: #111827 !important;
        }

        /* Buttons */
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s;
            border: none;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        /* Forms */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 8px;
            border: 1px solid #E5E7EB;
            padding: 0.75rem;
        }

        /* Metrics */
        .stMetric {
            background-color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        /* Success/Info messages */
        .stSuccess, .stInfo {
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }

        /* Custom role selection */
        .role-button {
            background-color: white;
            padding: 2rem;
            border-radius: 12px;
            border: 2px solid #E5E7EB;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }

        .role-button:hover {
            border-color: #4F46E5;
            transform: translateY(-2px);
        }

        /* Sidebar */
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

# Initialize app state
def init_session_state():
    if "role" not in st.session_state:
        st.session_state.role = None
    if "language" not in st.session_state:
        st.session_state.language = "en"
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}

def main():
    st.set_page_config(
        page_title="TalentScout Technical Interview Assistant",
        page_icon="👨‍💼",
        layout="wide"
    )

    load_css()
    init_session_state()
    init_database()
    setup_translations()

    # Language selector in sidebar with custom styling
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/your-repo/talent-scout-logo.png", width=200)
        st.markdown("---")
        languages = {"en": "🇺🇸 English", "es": "🇪🇸 Español", "fr": "🇫🇷 Français"}
        selected_lang = st.selectbox(
            "🌍 Language/Idioma/Langue",
            options=list(languages.keys()),
            format_func=lambda x: languages[x],
            key="language_selector"
        )

        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()

        if st.session_state.role:
            if st.button("📤 " + get_text("Logout"), key="logout"):
                st.session_state.clear()
                st.rerun()

    # Role selection if not already selected
    if not st.session_state.role:
        st.title("🎯 " + get_text("Welcome to TalentScout"))
        st.markdown("### Choose your role to get started")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
                <div class="role-button" onclick="document.querySelector('#recruiter-button').click()">
                    <h3>👔 Recruiter</h3>
                    <p>Access candidate evaluations and manage interviews</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Select Recruiter", key="recruiter-button", type="primary"):
                st.session_state.role = "recruiter"
                st.rerun()

        with col2:
            st.markdown("""
                <div class="role-button" onclick="document.querySelector('#candidate-button').click()">
                    <h3>👨‍💻 Candidate</h3>
                    <p>Take your technical interview and showcase your skills</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Select Candidate", key="candidate-button", type="primary"):
                st.session_state.role = "candidate"
                st.rerun()
    else:
        # Show appropriate view based on role
        if st.session_state.role == "recruiter":
            show_recruiter_view()
        else:
            show_candidate_view()

if __name__ == "__main__":
    main()