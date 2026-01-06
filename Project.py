import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", page_icon="🎓", layout="centered")

# 2. CSS pentru Design DARK (Fără imagine, fundal curat)
st.markdown("""
    <style>
    /* Ascunde elementele Streamlit */
    header, footer, #MainMenu {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}

    /* FUNDAL DARK COMPLET */
    .stApp {
        background-color: #0b0e14;
    }

    /* CARDUL CENTRAL DARK */
    .main .block-container {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 40px !important;
        margin-top: 8vh !important;
        box-shadow: 0px 20px 40px rgba(0,0,0,0.6);
        max-width: 420px !important;
        text-align: center;
    }

    /* TITLUL */
    .titlu-neon {
        color: #58a6ff;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    .subtitlu-dark {
        color: #8b949e;
        font-size: 0.95rem;
        margin-bottom: 35px;
    }

    /* BUTOANELE NEGRE (STYLE PREMIUM) */
    .stButton > button {
        width: 100% !important;
        height: 65px !important;
        border-radius: 12px !important;
        margin-bottom: 15px !important;
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: 0.3s;
    }

    .stButton > button:hover {
        border-color: #58a6ff !important;
        color: #58a6ff !important;
        background-color: #161b22 !important;
    }

    /* Butonul de Inapoi */
    .back-btn button {
        height: 45px !important;
        background-color: transparent !important;
        border: none !important;
        color: #8b949e !important;
        font-size: 0.9rem !important;
    }

    /* Stil pentru Input-uri în Dark Mode */
    input {
        background-color: #0d1117 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Initializare Baza de Date
def init_db():
    conn = sqlite3.connect('catalog_dark.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS grades (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)')
    c.execute('CREATE TABLE IF NOT EXISTS absences (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT)')
    conn.commit()
    return conn

conn = init_db()
MATERII = ["Limba Română", "Matematică", "Engleză", "Franceză", "Istorie", "Geografie", "Biologie", "Fizică", "Chimie", "TIC", "Religie", "Ed. Plastică", "Ed. Muzicală", "Ed. Fizică", "Dirigenție"]
CLASE = {"6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"]}

if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- ECRAN START (DARK CARD) ---
if st.session_state.page == 'home':
    st.markdown("<div class='titlu-neon'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitlu-dark'>Selectează modul de autentificare:</div>", unsafe_allow_html=True)
    
    if st.button("👤 Profesor"):
        st.session_state.page = 'login_prof'
        st.rerun()

    if st.button("👨‍👩‍👧 Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("⚙️ Administrator"):
        st.session_state.page = 'login_admin'
        st.rerun()

# --- PAGINI LOGIN ---
elif st.session_state.page == 'login_prof':
    st.markdown("<div class='titlu-neon'>Profesor</div>", unsafe_allow_html=True)
    m_sel = st.selectbox("Materia", MATERII)
    p_p = st.text_input("Parolă", type="password")
    if st.button("Autentificare"):
        if p_p == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": m_sel, "page": "main"})
            st.rerun()
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("← Înapoi"): 
        st.session_state.page = 'home'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# (Continuă cu restul logicilor pentru Părinte/Admin în același stil...)
