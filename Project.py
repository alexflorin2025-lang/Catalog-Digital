import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", page_icon="🎓", layout="centered")

# 2. CSS pentru "3 Pătrate" care ocupă TOT ECRANUL
st.markdown("""
    <style>
    /* Ascunde elementele Streamlit */
    header, footer, #MainMenu {visibility: hidden !important; height: 0px !important;}
    [data-testid="stHeader"] {display: none !important;}
    
    /* Fundal negru complet */
    .stApp {background-color: #0e1117;}
    
    /* Elimină spațiile goale de sus */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        height: 100vh !important;
    }

    .titlu {
        text-align: center; 
        color: #58a6ff; 
        font-size: 1.8rem; 
        font-weight: bold; 
        margin-bottom: 20px;
    }

    /* CONTAINER BUTOANE MARI (PĂTRATE) */
    .stButton > button {
        width: 100% !important;
        height: 22vh !important; /* Ocupă 22% din înălțimea ecranului fiecare */
        border-radius: 20px !important;
        margin-bottom: 15px !important;
        background-color: #161b22 !important;
        color: white !important;
        border: 2px solid #30363d !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-direction: column !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3) !important;
    }

    /* Culori margini pentru identificare rapidă */
    .prof-btn button { border-left: 10px solid #58a6ff !important; }
    .dir-btn button { border-left: 10px solid #8957e5 !important; }
    .par-btn button { border-left: 10px solid #238636 !important; }
    
    /* Efect la apăsare */
    .stButton > button:active {
        transform: scale(0.98);
        background-color: #1f242c !important;
    }
    
    /* Ascunde sidebar-ul pe mobil */
    [data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# 3. Baza de date
def init_db():
    conn = sqlite3.connect('catalog_v11.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS grades (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)')
    c.execute('CREATE TABLE IF NOT EXISTS absences (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT)')
    conn.commit()
    return conn

conn = init_db()
CLASE = {"6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"]}

if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- ECRAN START ---
if st.session_state.page == 'home':
    st.markdown("<div class='titlu'>Catalog Digital</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='prof-btn'>", unsafe_allow_html=True)
    if st.button("🔒 PROFESOR\n(Note & Absențe)", key="btn_prof"):
        st.session_state.page = 'login_prof'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='dir-btn'>", unsafe_allow_html=True)
    if st.button("👑 DIRECTOR\n(Administrare)", key="btn_dir"):
        st.session_state.page = 'login_dir'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='par-btn'>", unsafe_allow_html=True)
    if st.button("👤 PĂRINTE\n(Vizualizare)", key="btn_par"):
        st.session_state.page = 'login_parinte'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- LOGICA PAGINI LOGIN ---
elif st.session_state.page == 'login_prof':
    st.markdown("### 🔒 Logare Profesor")
    p_p = st.text_input("Parolă", type="password")
    if st.button("CONECTARE"):
        if p_p == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "page": "main"})
            st.rerun()
    if st.button("⬅️ Înapoi"): st.session_state.page = 'home'; st.rerun()

# (Se repetă logica pentru celelalte pagini...)
