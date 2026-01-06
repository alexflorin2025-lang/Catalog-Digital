import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", page_icon="🎓", layout="centered")

# 2. CSS pentru Card vizibil în Dark Mode
st.markdown("""
    <style>
    /* Ascunde elementele Streamlit */
    header, footer, #MainMenu {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}

    /* FUNDAL NEGRU COMPLET */
    .stApp {
        background-color: #050505 !important;
    }

    /* CARDUL CENTRAL - Acum cu bordură vizibilă */
    .main .block-container {
        background-color: #121212 !important; /* Gri foarte închis */
        border: 2px solid #58a6ff !important; /* BORDURĂ ALBASTRĂ VIZIBILĂ */
        border-radius: 20px !important;
        padding: 40px !important;
        margin-top: 5vh !important;
        box-shadow: 0px 0px 30px rgba(88, 166, 255, 0.2) !important;
        max-width: 400px !important;
        text-align: center;
    }

    /* TITLUL */
    .titlu-neon {
        color: #58a6ff;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 30px;
    }

    /* BUTOANELE */
    .stButton > button {
        width: 100% !important;
        height: 60px !important;
        border-radius: 12px !important;
        margin-bottom: 15px !important;
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        font-size: 1.1rem !important;
        transition: 0.3s;
    }

    /* Efect când apeși pe buton */
    .stButton > button:active {
        background-color: #58a6ff !important;
        border-color: #58a6ff !important;
    }

    /* Stil input-uri */
    input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #58a6ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA APLICATIEI ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<div class='titlu-neon'>Catalog Digital</div>", unsafe_allow_html=True)
    
    if st.button("👤 Profesor"):
        st.session_state.page = 'login_prof'
        st.rerun()

    if st.button("👨‍👩‍👧 Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("⚙️ Administrator"):
        st.session_state.page = 'login_admin'
        st.rerun()

# (Logica pentru paginile de login...)
elif st.session_state.page == 'login_prof':
    st.markdown("<div class='titlu-neon'>Profesor</div>", unsafe_allow_html=True)
    p_p = st.text_input("Parolă", type="password")
    if st.button("Autentificare"):
        if p_p == "123451":
            st.session_state.page = 'main'
            st.rerun()
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
