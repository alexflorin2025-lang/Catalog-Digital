import streamlit as st
import sqlite3
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS DARK PREMIUM - Stil modern cu card vizibil
st.markdown("""
    <style>
    /* Fundalul paginii - Gri extrem de închis, nu negru simplu */
    .stApp {
        background-color: #0d1117 !important;
    }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* CHENARUL CENTRAL (Cardul) - Stil Glassmorphism */
    .main .block-container {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 20px;
        padding: 40px !important;
        margin-top: 50px !important;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
        max-width: 450px !important;
    }

    /* TITLUL - Albastru strălucitor */
    .titlu-premium {
        text-align: center;
        color: #58a6ff;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 30px;
    }

    /* BUTOANELE NEGRE CU TEXT ALB */
    .stButton > button {
        width: 100% !important;
        height: 55px !important;
        background-color: #21262d !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        margin-bottom: 12px;
        transition: 0.2s;
    }
    
    .stButton > button:hover {
        border-color: #58a6ff !important;
        background-color: #30363d !important;
    }

    /* CĂSUȚA DE INPUT (PAROLA) - Gri închis cu text alb */
    input {
        background-color: #0d1117 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        height: 45px !important;
    }
    
    /* Textul de deasupra căsuțelor (Materia, Parola) */
    label { 
        color: #8b949e !important; 
        font-size: 0.9rem !important;
        margin-bottom: 8px !important;
    }

    /* Mesaje de eroare mai discrete */
    .stAlert {
        background-color: #2a1215 !important;
        color: #ff7b72 !important;
        border: 1px solid #8e1519 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica de funcționare
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PAGINA DE START ---
if st.session_state.page == 'home':
    st.markdown("<div class='titlu-premium'>Catalog Digital</div>", unsafe_allow_html=True)
    
    if st.button("👤 Profesor"):
        st.session_state.page = 'login_prof'
        st.rerun()
    if st.button("👨‍👩‍👧 Părinte / Elev"):
        st.session_state.page = 'login_par'
        st.rerun()
    if st.button("⚙️ Administrator"):
        st.session_state.page = 'login_admin'
        st.rerun()

# --- PAGINA LOGIN PROFESOR ---
elif st.session_state.page == 'login_prof':
    st.markdown("<div class='titlu-premium'>Logare Prof</div>", unsafe_allow_html=True)
    
    materia = st.selectbox("Materia", ["Limba Română", "Matematică", "Engleză", "Istorie"])
    st.write("") # Spatiu mic
    parola = st.text_input("Introdu Parola", type="password")
    
    st.write("") # Spatiu sub parola
    if st.button("CONECTARE"):
        if parola == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia, "page": "main"})
            st.rerun()
        else:
            st.error("Parolă incorectă!")
            
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()

# --- PAGINA PRINCIPALĂ (DUMMY) ---
elif st.session_state.get('logged_in'):
    st.markdown(f"<div class='titlu-premium'>{st.session_state.materia}</div>", unsafe_allow_html=True)
    st.info("Sistemul de notare este activ.")
    if st.button("🚪 Ieșire"):
        st.session_state.clear()
        st.rerun()
