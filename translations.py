import streamlit as st

translations = {
    "en": {
        "Welcome to TalentScout": "Welcome to TalentScout",
        "I am a Recruiter": "I am a Recruiter",
        "I am a Candidate": "I am a Candidate",
        "Logout": "Logout",
        "Full Name": "Full Name",
        "Email": "Email",
        "Phone": "Phone",
        "Years of Experience": "Years of Experience",
        "Desired Position": "Desired Position",
        "Current Location": "Current Location",
        "Technical Skills": "Technical Skills",
        "Start Interview": "Start Interview",
        "Submit": "Submit",
        "Next": "Next",
        "Your Score": "Your Score",
        "Candidate Dashboard": "Candidate Dashboard",
        "Recruiter Dashboard": "Recruiter Dashboard"
    },
    "es": {
        "Welcome to TalentScout": "Bienvenido a TalentScout",
        "I am a Recruiter": "Soy Reclutador",
        "I am a Candidate": "Soy Candidato",
        "Logout": "Cerrar Sesión",
        "Full Name": "Nombre Completo",
        "Email": "Correo Electrónico",
        "Phone": "Teléfono",
        "Years of Experience": "Años de Experiencia",
        "Desired Position": "Puesto Deseado",
        "Current Location": "Ubicación Actual",
        "Technical Skills": "Habilidades Técnicas",
        "Start Interview": "Comenzar Entrevista",
        "Submit": "Enviar",
        "Next": "Siguiente",
        "Your Score": "Tu Puntuación",
        "Candidate Dashboard": "Panel del Candidato",
        "Recruiter Dashboard": "Panel del Reclutador"
    },
    "fr": {
        "Welcome to TalentScout": "Bienvenue sur TalentScout",
        "I am a Recruiter": "Je suis Recruteur",
        "I am a Candidate": "Je suis Candidat",
        "Logout": "Déconnexion",
        "Full Name": "Nom Complet",
        "Email": "Email",
        "Phone": "Téléphone",
        "Years of Experience": "Années d'Expérience",
        "Desired Position": "Poste Souhaité",
        "Current Location": "Localisation Actuelle",
        "Technical Skills": "Compétences Techniques",
        "Start Interview": "Commencer l'Entretien",
        "Submit": "Soumettre",
        "Next": "Suivant",
        "Your Score": "Votre Score",
        "Candidate Dashboard": "Tableau de Bord Candidat",
        "Recruiter Dashboard": "Tableau de Bord Recruteur"
    }
}

def setup_translations():
    st.session_state.translations = translations

def get_text(key):
    lang = st.session_state.language
    return translations[lang].get(key, key)
