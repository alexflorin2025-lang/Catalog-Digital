import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="wide")

# 2. CSS - Fără texte inutile, doar lățime maximă
st.markdown("""
    <style>
    /* Fundal negru premium */
    .stApp { background-color: #0d1117 !important; }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* Forțăm containerul să folosească TOATĂ lățimea ecranului */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
        padding-top: 5rem !important;
    }

    /* TITLU CURAT */
    .titlu-principal {
        text-align: center;
        color: #58a6ff;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 60px;
    }

    /* FORȚARE BUTOANE LATE --------->> */
    div.stButton > button {
        display: block !important;
        width: 100% !important; /* Lățime totală */
        min-width: 100% !important;
        height: 90px !important; /* Înălțime confortabilă */
        background-color: #161b22 !important;
        color: white !important;
        border: 2px solid #30363d !important;
        border-radius: 15px !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        margin-top: 25px !important;
        transition: 0.2s;
    }
    
    div.stButton > button:hover {
        border-color: #58a6ff !important;
        background-color: #1c2128 !important;
    }

    /* Input-uri și Selectoare la fel de late */
    .stSelectbox, .stTextInput, div[data-baseweb="input"] {
        width: 100% !important;
    }
    
    input {
        background-color: #0d1117 !important;
        color: white !important;
        height: 55px !important;
        border: 1px solid #30363d !important;
    }
    
    label { color: #8b949e !important; font-size: 1.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Interfața
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<div class='titlu-principal'>🎓 Catalog Digital</div>", unsafe_allow_html=True)
    
    # Secțiunea de butoane care se întind pe tot ecranul
    if st.button("👨‍🏫 Acces Modul Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("👪 Acces Părinți / Elevi"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("🛡️ Panou Control Director"):
        st.session_state.page = 'login_administrator'
        st.rerun()

elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='titlu-principal'>🔑 Autentificare</div>", unsafe_allow_html=True)
    
    materia = st.selectbox("Materia:", ["Limba Română", "Matematică", "Engleză", "Istorie"])
    st.write("")
    parola = st.text_input("Parolă:", type="password")
    
    if st.button("🚀 Conectare"):
        st.success("Acces permis!")
        
    if st.button("⬅️ Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
