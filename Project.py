import streamlit as st
import sqlite3
from datetime import datetime

# 1. Configurare Pagina - Layout Wide obligatoriu pentru latime
st.set_page_config(page_title="Catalog Digital Wide", layout="wide")

# 2. CSS pentru butoane si containere ultra-late
st.markdown("""
    <style>
    /* Fundal general dark */
    .stApp { background-color: #0d1117 !important; }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* Containerul principal - Fara limita de latime */
    .main .block-container {
        max-width: 98% !important; 
        padding-top: 2rem !important;
    }

    /* Stilul Cardului care prinde tot ecranul --------->> */
    .wide-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 50px 2% !important;
        width: 100% !important;
        margin-bottom: 20px;
    }

    /* TITLUL */
    .titlu-mare {
        text-align: center;
        color: #58a6ff;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 40px;
    }

    /* BUTOANELE LATE (--------->>) */
    .stButton > button {
        width: 100% !important; /* Ocupa toata latimea ecranului */
        height: 90px !important;
        background-color: #21262d !important;
        color: white !important;
        border: 2px solid #30363d !important;
        border-radius: 15px !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        margin-bottom: 30px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: 0.3s ease;
    }
    
    .stButton > button:hover {
        border-color: #58a6ff !important;
        background-color: #1f242c !important;
        transform: scale(1.01);
    }

    /* Input-uri late pentru pagina de login */
    div[data-baseweb="input"], div[data-baseweb="select"], input {
        width: 100% !important;
        height: 60px !important;
        background-color: #0d1117 !important;
        color: white !important;
        border-radius: 12px !important;
    }

    label { color: #f0f6fc !important; font-size: 1.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica de navigare
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- CONTAINERUL CARE FACE TOTUL LAT ---
with st.container():
    st.markdown('<div class="wide-card">', unsafe_allow_html=True)

    # --- ECRAN START: Profesor, Parinte, Director ---
    if st.session_state.page == 'home':
        st.markdown("<div class='titlu-mare'>🎓 Catalog Digital</div>", unsafe_allow_html=True)
        
        # Butoanele se vor intinde pe toata latimea acum
        if st.button("👨‍🏫 ACCES MODUL PROFESOR"):
            st.session_state.page = 'login_profesor'
            st.rerun()

        if st.button("👪 ACCES PĂRINȚI / ELEVI"):
            st.session_state.page = 'login_parinte'
            st.rerun()

        if st.button("🛡️ PANOU CONTROL DIRECTOR"):
            st.session_state.page = 'login_administrator'
            st.rerun()

    # --- PAGINA LOGIN PROFESOR ---
    elif st.session_state.page == 'login_profesor':
        st.markdown("<div class='titlu-mare'>🔑 Autentificare Profesor</div>", unsafe_allow_html=True)
        
        materia = st.selectbox("Selectați Materia:", ["Limba Română", "Matematică", "Engleză", "Istorie"])
        st.write("")
        parola = st.text_input("Parolă de acces:", type="password")
        
        st.write("<br>", unsafe_allow_html=True)
        if st.button("🚀 CONECTARE"):
            if parola == "123451":
                st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia, "page": "main"})
                st.rerun()
            else:
                st.error("Parolă incorectă!")
                
        if st.button("⬅️ Înapoi la Meniu"):
            st.session_state.page = 'home'
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
