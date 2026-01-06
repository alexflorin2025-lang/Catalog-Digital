import streamlit as st
import sqlite3
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital Școlar", layout="centered")

# 2. CSS DARK PREMIUM - Interfață lungă și detaliată
st.markdown("""
    <style>
    /* Fundalul general al aplicației */
    .stApp {
        background-color: #0d1117 !important;
    }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* CHENARUL CENTRAL (Cardul) - Mai lung și mai spațios */
    .main .block-container {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 20px;
        padding: 50px 40px !important; /* Padding mai mare sus/jos */
        margin-top: 40px !important;
        box-shadow: 0px 15px 40px rgba(0, 0, 0, 0.6);
        max-width: 480px !important;
    }

    /* TITLUL COMPLET */
    .titlu-complet {
        text-align: center;
        color: #58a6ff;
        font-size: 2.4rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .descriere-subtitlu {
        text-align: center;
        color: #8b949e;
        font-size: 1rem;
        margin-bottom: 40px;
    }

    /* BUTOANELE DE ACCES - Mai înalte și cu text complet */
    .stButton > button {
        width: 100% !important;
        height: 70px !important; /* Înălțime crescută */
        background-color: #21262d !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        margin-bottom: 18px !important;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        border-color: #58a6ff !important;
        background-color: #30363d !important;
        transform: translateY(-2px);
    }

    /* INPUT-URILE DE LOGIN */
    input {
        background-color: #0d1117 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        height: 55px !important;
        margin-bottom: 20px !important;
    }
    
    label { 
        color: #c9d1d9 !important; 
        font-size: 1rem !important;
        margin-left: 5px !important;
    }

    /* Separator vizual */
    .separator {
        border-bottom: 1px solid #30363d;
        margin: 20px 0 30px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica de funcționare
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PAGINA DE START (Sign In Lung) ---
if st.session_state.page == 'home':
    st.markdown("<div class='titlu-complet'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='descriere-subtitlu'>Sistem oficial de gestionare a situației școlare</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
    
    # Butoane cu denumiri complete
    if st.button("Accesează Modul Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("Vizualizare Părinte sau Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("Panou Control Administrator"):
        st.session_state.page = 'login_administrator'
        st.rerun()

# --- PAGINA LOGARE PROFESOR ---
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='titlu-complet'>Autentificare</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#8b949e;'>Introduceți datele pentru a accesa materia</p>", unsafe_allow_html=True)
    
    st.write("")
    materia = st.selectbox("Selectați Disciplina Școlară:", ["Limba și Literatura Română", "Matematică", "Limba Engleză", "Istorie", "Geografie"])
    
    st.write("")
    parola = st.text_input("Introduceți Parola de Acces:", type="password")
    
    st.write("")
    if st.button("CONECTARE ÎN SISTEM"):
        if parola == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia, "page": "main"})
            st.rerun()
        else:
            st.error("Parola introdusă este incorectă. Vă rugăm să reîncercați.")
            
    if st.button("Înapoi la meniul principal"):
        st.session_state.page = 'home'
        st.rerun()

# --- PAGINA DUPĂ LOGARE ---
elif st.session_state.get('logged_in'):
    st.markdown(f"<div class='titlu-complet'>{st.session_state.materia}</div>", unsafe_allow_html=True)
    st.info("Sunteți conectat cu succes la baza de date școlară.")
    if st.button("Deconectare Securizată"):
        st.session_state.clear()
        st.rerun()
