import streamlit as st
import sqlite3
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Scolar Premium v21", layout="centered")

# 2. CSS ULTRA-DARK & LONG - Design extins la maximum
st.markdown("""
    <style>
    /* Fundalul general */
    .stApp {
        background-color: #05070a !important;
    }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* CARDUL CENTRAL - Lungime Maxima */
    .main .block-container {
        background-color: #0d1117 !important;
        border: 2px solid #1f6feb !important;
        border-radius: 30px;
        padding: 80px 50px !important; /* Padding gigant pentru inaltime */
        margin-top: 20px !important;
        margin-bottom: 50px !important;
        box-shadow: 0px 25px 60px rgba(0, 0, 0, 0.8);
        max-width: 550px !important;
    }

    /* TITLUL SI DECORATIUNI */
    .titlu-ultra {
        text-align: center;
        color: #58a6ff;
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 5px;
        text-shadow: 2px 2px 10px rgba(88, 166, 255, 0.3);
    }
    
    .status-bar {
        text-align: center;
        color: #238636;
        font-size: 0.9rem;
        font-weight: bold;
        margin-bottom: 60px;
        letter-spacing: 2px;
    }

    /* BUTOANELE "KING SIZE" CU EMOJI */
    .stButton > button {
        width: 100% !important;
        height: 110px !important; /* Butoane extrem de inalte */
        background-color: #161b22 !important;
        color: white !important;
        border: 2px solid #30363d !important;
        border-radius: 20px !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        margin-bottom: 40px !important; /* Spatiu mare intre butoane */
        box-shadow: 0px 4px 15px rgba(0,0,0,0.4) !important;
        transition: 0.4s ease-in-out;
    }
    
    .stButton > button:hover {
        border-color: #58a6ff !important;
        background-color: #1f242c !important;
        transform: translateY(-5px);
        box-shadow: 0px 10px 25px rgba(88, 166, 255, 0.2) !important;
    }

    /* INPUT-URILE DE LOGIN GIGANT */
    input {
        background-color: #05070a !important;
        color: white !important;
        border: 2px solid #1f6feb !important;
        border-radius: 15px !important;
        height: 70px !important; /* Input mai inalt */
        font-size: 1.2rem !important;
    }
    
    label { 
        color: #f0f6fc !important; 
        font-size: 1.2rem !important;
        margin-bottom: 15px !important;
        display: block;
    }

    /* Linie de design */
    .glow-line {
        height: 2px;
        background: linear-gradient(90deg, transparent, #1f6feb, transparent);
        margin: 40px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica de navigare
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PAGINA DE START (ULTRA-LONG) ---
if st.session_state.page == 'home':
    st.markdown("<div class='titlu-ultra'>🎓 CATALOG</div>", unsafe_allow_html=True)
    st.markdown("<div class='status-bar'>● SISTEM ONLINE ACTIV</div>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align:center; color:#8b949e;'>Bine ați venit în platforma securizată a școlii dumneavoastră. Vă rugăm să selectați o opțiune de mai jos pentru a continua.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)
    
    # Secțiune Butoane Extinse
    if st.button("👨‍🏫 ACCES MODUL PROFESOR"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("👪 MODUL PĂRINTE / ELEV"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("🛡️ ADMINISTRARE UNITATE"):
        st.session_state.page = 'login_administrator'
        st.rerun()

    st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)
    
    # Footer lung pentru a umple ecranul
    st.markdown("<p style='text-align:center; color:#30363d; font-size:0.8rem;'>Securitate SSL 256-bit activată<br>Suport Tehnic: 0800 123 456<br>Platformă optimizată pentru dispozitive mobile</p>", unsafe_allow_html=True)

# --- PAGINA LOGARE (EXTENDED LOGIN) ---
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='titlu-ultra'>🔑 LOGIN</div>", unsafe_allow_html=True)
    st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)
    
    st.write("")
    materia = st.selectbox("📚 Selectați Disciplina:", ["Limba și Literatura Română", "Matematică", "Limba Engleză", "Istorie", "Geografie", "Biologie", "Chimie", "Fizică"])
    
    st.write("<br><br>", unsafe_allow_html=True) # Spatiu extra
    
    parola = st.text_input("🔐 Introduceți Codul Secret:", type="password")
    
    st.write("<br><br>", unsafe_allow_html=True)
    
    if st.button("🚀 AUTENTIFICARE SECURIZATĂ"):
        if parola == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia, "page": "main"})
            st.rerun()
        else:
            st.error("❌ EROARE: Parolă incorectă. Vă rugăm să contactați administratorul dacă ați uitat datele.")
            
    st.write("<br>", unsafe_allow_html=True)
    if st.button("⬅️ ÎNAPOI LA MENIU"):
        st.session_state.page = 'home'
        st.rerun()
