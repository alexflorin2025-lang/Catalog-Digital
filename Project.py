import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. Design DARK PROFESIONAL (Vizibil pe orice ecran)
st.markdown("""
    <style>
    /* Fundal negru total */
    .stApp { background-color: #050505 !important; }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* CHENARUL ALBASTRU (Fixat pentru vizibilitate) */
    .main .block-container {
        background-color: #111111 !important;
        border: 2px solid #007bff !important;
        border-radius: 20px;
        padding: 30px !important;
        margin-top: 50px !important;
        box-shadow: 0px 0px 25px rgba(0, 123, 255, 0.3);
        color: white !important;
    }

    /* TITLU */
    .titlu-catalog {
        text-align: center;
        color: #007bff;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* BUTOANELE DIN CHENAR */
    .stButton > button {
        width: 100% !important;
        height: 60px !important;
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        font-size: 1.2rem !important;
        margin-bottom: 10px;
    }
    
    .stButton > button:hover {
        border-color: #007bff !important;
        color: #007bff !important;
    }

    /* CĂSUȚA DE PAROLĂ (Albă în interior pentru vizibilitate) */
    input {
        background-color: white !important;
        color: black !important;
        border-radius: 8px !important;
        height: 45px !important;
    }
    
    label { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica de funcționare
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PAGINA DE START ---
if st.session_state.page == 'home':
    st.markdown("<div class='titlu-catalog'>Catalog Digital</div>", unsafe_allow_html=True)
    st.write("<p style='text-align:center; color:gray;'>Alege modul de logare:</p>", unsafe_allow_html=True)
    
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
    st.markdown("<div class='titlu-catalog'>Logare Prof</div>", unsafe_allow_html=True)
    materia = st.selectbox("Materia", ["Limba Română", "Matematică", "Engleză", "Istorie"])
    
    # Câmpul de parolă acum e alb și se vede ce scrii
    parola = st.text_input("Introdu Parola", type="password")
    
    if st.button("CONECTARE"):
        if parola == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia, "page": "main"})
            st.rerun()
        else:
            st.error("Parolă greșită!")
            
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()

# --- DUPĂ LOGARE ---
elif st.session_state.get('logged_in'):
    st.markdown(f"<div class='titlu-catalog'>{st.session_state.materia}</div>", unsafe_allow_html=True)
    st.success(f"Ești logat ca Profesor")
    
    if st.button("🚪 Deconectare"):
        st.session_state.clear()
        st.session_state.page = 'home'
        st.rerun()
