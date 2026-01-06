import streamlit as st
import sqlite3
from datetime import datetime

# 1. Configurare Pagina - Am setat layout="wide" pentru latime maxima
st.set_page_config(page_title="Catalog Digital Ultra-Wide", layout="wide")

# 2. CSS pentru Latime Maxima (--------->>)
st.markdown("""
    <style>
    /* Fundal general */
    .stApp { background-color: #0d1117 !important; }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* CONTAINERUL - Acum ocupa toata latimea ecranului */
    .main .block-container {
        max-width: 95% !important; /* SE INTINDE PE TOT ECRANUL --------->> */
        padding-top: 50px !important;
        padding-bottom: 50px !important;
        margin: 0 auto !important;
    }

    /* CARDUL CENTRAL */
    .card-background {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 60px 5% !important;
        width: 100% !important;
    }

    /* TITLURI */
    .titlu-ultra {
        text-align: center;
        color: #58a6ff;
        font-size: clamp(2rem, 8vw, 3.5rem); /* Se adapteaza la ecran */
        font-weight: 800;
        margin-bottom: 10px;
    }
    
    .status-online {
        text-align: center;
        color: #238636;
        font-weight: bold;
        margin-bottom: 60px;
        font-size: 1.1rem;
    }

    /* BUTOANELE ULTRA-LATE (--------->>) */
    .stButton > button {
        width: 100% !important; /* OCUPA TOATA LATIMEA CARDULUI */
        height: 80px !important;
        background-color: #21262d !important;
        color: white !important;
        border: 2px solid #30363d !important;
        border-radius: 15px !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        margin-bottom: 30px !important;
        transition: 0.3s;
    }
    
    .stButton > button:hover {
        border-color: #58a6ff !important;
        background-color: #30363d !important;
        box-shadow: 0px 0px 20px rgba(88, 166, 255, 0.2);
    }

    /* INPUT-URILE (Selectbox si Password) - Acum sunt LATE */
    div[data-baseweb="select"], div[data-baseweb="input"], input {
        width: 100% !important;
        min-height: 60px !important;
        background-color: #0d1117 !important;
        color: white !important;
        border-radius: 12px !important;
        font-size: 1.2rem !important;
    }
    
    label { 
        color: #f0f6fc !important; 
        font-size: 1.3rem !important;
        margin-bottom: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica de navigare
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Folosim un container tip card pentru tot continutul
with st.container():
    st.markdown('<div class="card-background">', unsafe_allow_html=True)
    
    # --- PAGINA START (ULTRA-LATA) ---
    if st.session_state.page == 'home':
        st.markdown("<div class='titlu-ultra'>🎓 Catalog Digital</div>", unsafe_allow_html=True)
        st.markdown("<div class='status-online'>● SISTEM ONLINE SECURIZAT</div>", unsafe_allow_html=True)
        
        # Butoane late
        if st.button("👨‍🏫 Autentificare Modul Profesor"):
            st.session_state.page = 'login_profesor'
            st.rerun()

        if st.button("👪 Vizualizare Părinte / Elev"):
            st.session_state.page = 'login_parinte'
            st.rerun()

        if st.button("🛡️ Administrare Unitate Școlară"):
            st.session_state.page = 'login_administrator'
            st.rerun()

    # --- PAGINA LOGIN ---
    elif st.session_state.page == 'login_profesor':
        st.markdown("<div class='titlu-ultra'>🔑 Logare Securizată</div>", unsafe_allow_html=True)
        
        st.write("<br>", unsafe_allow_html=True)
        materia = st.selectbox("Selectați Disciplina Predată:", ["Matematică", "Limba Română", "Fizică", "Istorie"])
        
        st.write("<br>", unsafe_allow_html=True)
        parola = st.text_input("Introduceți Parola de Acces:", type="password")
        
        st.write("<br>", unsafe_allow_html=True)
        if st.button("🚀 CONECTARE"):
            if parola == "123451":
                st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia, "page": "main"})
                st.rerun()
            else:
                st.error("❌ Parolă incorectă!")
                
        if st.button("⬅️ Înapoi la Meniu"):
            st.session_state.page = 'home'
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
