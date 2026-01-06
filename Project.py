import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. Design-ul Dark cu Chenar Albastru Vizibil
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden !important;}
    .stApp { background-color: #050505 !important; }
    
    .main .block-container {
        background-color: #121212 !important;
        border: 3px solid #58a6ff !important;
        border-radius: 25px !important;
        padding: 30px !important;
        margin-top: 30px !important;
        max-width: 420px !important;
        box-shadow: 0px 0px 20px rgba(88, 166, 255, 0.3) !important;
    }
    
    .titlu { color: #58a6ff; text-align: center; font-size: 2rem; font-weight: bold; margin-bottom: 20px; }
    
    .stButton > button {
        width: 100% !important;
        height: 60px !important;
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 15px !important;
    }
    /* Stil pentru inputuri sa fie vizibile in Dark Mode */
    input { background-color: #0d1117 !important; color: white !important; border: 1px solid #30363d !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Functie Baza de Date (Ca sa nu pierzi notele)
def init_db():
    conn = sqlite3.connect('catalog_final.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS grades (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)')
    c.execute('CREATE TABLE IF NOT EXISTS absences (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT)')
    conn.commit()
    return conn

conn = init_db()
CLASE = {"6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"]}

# 4. Logica de Navigare
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PAGINA START ---
if st.session_state.page == 'home':
    st.markdown("<div class='titlu'>Catalog Digital</div>", unsafe_allow_html=True)
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
    st.markdown("<div class='titlu'>Profesor</div>", unsafe_allow_html=True)
    materia = st.selectbox("Materia", ["Matematică", "Română", "Engleză", "Istorie"])
    parola = st.text_input("Parolă", type="password")
    if st.button("LOGARE"):
        if parola == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia, "page": "main"})
            st.rerun()
    if st.button("← Înapoi"): st.session_state.page = 'home'; st.rerun()

# --- INTERFATA CATALOG (Dupa logare) ---
elif st.session_state.get('logged_in'):
    st.markdown(f"<div class='titlu'>{st.session_state.materia}</div>", unsafe_allow_html=True)
    
    for elev in CLASE["6B"]:
        with st.expander(f"👤 {elev}"):
            nota = st.slider("Notă", 1, 10, 10, key=f"s_{elev}")
            if st.button(f"Pune Nota {nota}", key=f"b_{elev}"):
                data_azi = datetime.now().strftime("%d-%m-%Y")
                conn.execute("INSERT INTO grades (dt, cl, name, sub, val) VALUES (?,?,?,?,?)", 
                             (data_azi, "6B", elev, st.session_state.materia, nota))
                conn.commit()
                st.toast(f"Nota {nota} salvată pentru {elev}!")
    
    if st.button("🚪 Deconectare"):
        st.session_state.clear()
        st.rerun()
