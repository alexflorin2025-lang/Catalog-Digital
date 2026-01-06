import streamlit as st
import sqlite3
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Scolar Oficial v22", layout="centered")

# 2. CSS pentru un ecran LUNG (Vertical)
st.markdown("""
    <style>
    /* Fundalul general */
    .stApp { background-color: #0d1117 !important; }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* CARDUL CENTRAL - LUNGIT */
    .main .block-container {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 25px;
        padding: 100px 45px !important; /* Padding uriaș sus/jos pentru lungime */
        margin-top: 20px !important;
        margin-bottom: 100px !important;
        max-width: 500px !important;
        box-shadow: 0px 20px 50px rgba(0, 0, 0, 0.8);
    }

    /* TITLURI */
    .titlu-principal {
        text-align: center;
        color: #58a6ff;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .status-badge {
        text-align: center;
        color: #238636;
        background: rgba(35, 134, 54, 0.1);
        border: 1px solid #238636;
        border-radius: 20px;
        padding: 5px 15px;
        width: fit-content;
        margin: 0 auto 50px auto;
        font-size: 0.8rem;
    }

    /* TEXTE DE SEPARARE PENTRU LUNGIME */
    .sectiune-text {
        color: #8b949e;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 40px;
        line-height: 1.6;
    }

    /* BUTOANELE - Elegante si distantate */
    .stButton > button {
        width: 100% !important;
        height: 70px !important; /* Inaltime medie, dar cu margini mari */
        background-color: #21262d !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 15px !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        margin-bottom: 45px !important; /* Spatiu mare sub fiecare buton pentru lungime */
        transition: 0.3s;
    }
    
    .stButton > button:hover {
        border-color: #58a6ff !important;
        background-color: #30363d !important;
    }

    /* INPUT-URI */
    input {
        background-color: #0d1117 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        height: 55px !important;
    }

    /* Spatiere extra */
    .spatiu-lung { height: 60px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PAGINA START (LUNGĂ) ---
if st.session_state.page == 'home':
    st.markdown("<div class='titlu-principal'>🎓 Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='status-badge'>● SISTEM ONLINE SECURIZAT</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sectiune-text'>Bine ați venit în platforma școlară. Identificați-vă pentru a accesa datele elevilor și situația școlară curentă.</div>", unsafe_allow_html=True)
    
    # Buton 1
    st.write("---") # Linie de separare
    if st.button("👨‍🏫 Autentificare Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    # Buton 2
    if st.button("👪 Acces Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    # Buton 3
    if st.button("🛡️ Panou Administrator"):
        st.session_state.page = 'login_administrator'
        st.rerun()

    st.markdown("<div class='spatiu-lung'></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#30363d;'>Ministerul Educației - 2026</p>", unsafe_allow_html=True)

# --- PAGINA LOGIN ---
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='titlu-principal'>🔑 Logare</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='spatiu-lung'></div>", unsafe_allow_html=True)
    
    materia = st.selectbox("Selectați Materia Predată:", ["Matematică", "Limba Română", "Fizică", "Istorie"])
    
    st.markdown("<div class='spatiu-lung'></div>", unsafe_allow_html=True)
    
    parola = st.text_input("Introduceți Parola:", type="password")
    
    st.markdown("<div class='spatiu-lung'></div>", unsafe_allow_html=True)
    
    if st.button("🚀 CONECTARE"):
        if parola == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia, "page": "main"})
            st.rerun()
        else:
            st.error("❌ Parolă incorectă!")
            
    if st.button("⬅️ Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
