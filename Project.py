import streamlit as st
import sqlite3
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital Scolar v20", layout="centered")

# 2. CSS DARK PREMIUM - Design Lung cu Emoji
st.markdown("""
    <style>
    /* Fundalul general */
    .stApp {
        background-color: #0d1117 !important;
    }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* CARDUL CENTRAL - Extins pe verticala */
    .main .block-container {
        background-color: #161b22 !important;
        border: 2px solid #30363d !important;
        border-radius: 25px;
        padding: 60px 45px !important; /* Padding foarte mare pentru lungime */
        margin-top: 30px !important;
        box-shadow: 0px 20px 50px rgba(0, 0, 0, 0.7);
        max-width: 500px !important;
    }

    /* TITLUL SI SUBTITLUL */
    .titlu-mare {
        text-align: center;
        color: #58a6ff;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 10px;
    }
    
    .subtitlu-text {
        text-align: center;
        color: #8b949e;
        font-size: 1.1rem;
        margin-bottom: 50px;
    }

    /* BUTOANELE MARI CU EMOJI */
    .stButton > button {
        width: 100% !important;
        height: 85px !important; /* Butoane foarte inalte pentru a lungi pagina */
        background-color: #21262d !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 18px !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        margin-bottom: 25px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton > button:hover {
        border-color: #58a6ff !important;
        background-color: #30363d !important;
        transform: scale(1.02);
    }

    /* INPUT-URILE DE LOGIN */
    input {
        background-color: #0d1117 !important;
        color: white !important;
        border: 2px solid #30363d !important;
        border-radius: 12px !important;
        height: 60px !important;
    }
    
    label { 
        color: #f0f6fc !important; 
        font-size: 1.1rem !important;
        margin-bottom: 12px !important;
    }

    /* Spatiere extra intre elemente */
    .spacer {
        height: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica de navigare
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PAGINA DE START (Design Lung cu Emoji) ---
if st.session_state.page == 'home':
    st.markdown("<div class='titlu-mare'>🎓 Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitlu-text'>Bine ați venit! Vă rugăm să alegeți profilul dumneavoastră:</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    
    if st.button("👨‍🏫 Accesează Modul Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("👪 Vizualizare Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("🛡️ Administrare Sistem"):
        st.session_state.page = 'login_administrator'
        st.rerun()

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#30363d;'>v2.0 Build 2026</p>", unsafe_allow_html=True)

# --- PAGINA LOGARE PROFESOR ---
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='titlu-mare'>🔑 Autentificare</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    
    materia = st.selectbox("📚 Selectați Disciplina:", ["Limba și Literatura Română", "Matematică", "Limba Engleză", "Istorie", "Geografie"])
    
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    
    parola = st.text_input("🔐 Introduceți Parola de Acces:", type="password")
    
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    
    if st.button("🚀 CONECTARE ÎN CATALOG"):
        if parola == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia, "page": "main"})
            st.rerun()
        else:
            st.error("❌ Parolă incorectă! Vă rugăm să verificați datele.")
            
    if st.button("⬅️ Înapoi la început"):
        st.session_state.page = 'home'
        st.rerun()

# --- PAGINA DUPĂ LOGARE ---
elif st.session_state.get('logged_in'):
    st.markdown(f"<div class='titlu-mare'>📖 {st.session_state.materia}</div>", unsafe_allow_html=True)
    st.success("✅ Conexiune securizată stabilită.")
    if st.button("🚪 Deconectare Sigură"):
        st.session_state.clear()
        st.rerun()
