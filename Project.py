import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. Design Dark Mode cu Chenar Albastru și Input-uri Vizibile
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden !important;}
    .stApp { background-color: #050505 !important; }
    
    /* Chenarul principal */
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
    
    /* BUTOANELE MARI */
    .stButton > button {
        width: 100% !important;
        height: 60px !important;
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 15px !important;
        font-weight: bold !important;
    }

    /* REPARARE INPUT PAROLĂ - Să fie foarte vizibil */
    div[data-baseweb="input"] {
        background-color: #22272e !important;
        border: 2px solid #58a6ff !important;
        border-radius: 10px !important;
    }
    
    input {
        color: white !important;
        font-size: 1.1rem !important;
        padding: 10px !important;
    }

    /* Etichetele text (Materia, Parola) */
    label {
        color: #8b949e !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza de Date
def init_db():
    conn = sqlite3.connect('catalog_v16.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS grades (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)')
    conn.commit()
    return conn

conn = init_db()
CLASE = {"6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"]}

if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- ECRAN START ---
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

# --- PAGINA LOGIN PROFESOR (Reparată) ---
elif st.session_state.page == 'login_prof':
    st.markdown("<div class='titlu'>Logare</div>", unsafe_allow_html=True)
    materia = st.selectbox("Alege Materia:", ["Matematică", "Română", "Engleză", "Istorie"])
    
    # Am adăugat spațiu extra aici
    st.write("")
    parola = st.text_input("Introdu Parola:", type="password", help="Scrie parola aici")
    
    if st.button("CONECTARE"):
        if parola == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia, "page": "main"})
            st.rerun()
        else:
            st.error("Parolă incorectă!")
            
    if st.button("← Înapoi"): 
        st.session_state.page = 'home'
        st.rerun()

# --- INTERFATA DUPA LOGARE ---
elif st.session_state.get('logged_in'):
    st.success(f"Logat ca Prof. de {st.session_state.materia}")
    if st.button("🚪 Deconectare"):
        st.session_state.clear()
        st.rerun()
