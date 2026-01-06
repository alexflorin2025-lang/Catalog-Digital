import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS Ultra-Dark & Sleek
st.markdown("""
    <style>
    /* Fundal negru mat cu un gradient radial foarte subtil */
    .stApp {
        background: radial-gradient(circle at center, #121212 0%, #050505 100%);
    }

    header, footer, #MainMenu {visibility: hidden !important;}

    /* Containerul central - Dark Glass */
    .main .block-container {
        background: rgba(18, 18, 18, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        padding: 50px 40px !important;
        max-width: 450px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8) !important;
        margin-top: 8vh;
    }

    /* Titlu cu font alb curat */
    .logo-text {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }

    .subtitle {
        color: #666666;
        font-size: 0.95rem;
        margin-bottom: 40px;
    }

    /* INPUT-URI SI SELECTBOX - DARK MODE TOTAL */
    /* Stil pentru etichete (labels) */
    .stSelectbox label, .stTextInput label {
        color: #888888 !important;
        font-size: 0.85rem !important;
        margin-bottom: 8px !important;
    }

    /* Casutele propriu-zise */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #0a0a0a !important;
        border: 1px solid #222222 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }

    /* Efect la click pe casute */
    div[data-baseweb="select"]:focus-within, div[data-baseweb="input"]:focus-within {
        border-color: #444444 !important;
        box-shadow: 0 0 0 1px #444444 !important;
    }

    /* Culoarea textului in casute */
    input, div[data-baseweb="select"] * {
        color: #eeeeee !important;
    }

    /* BUTOANE - Stil Minimalist Alb pe Negru */
    div.stButton > button {
        width: 100% !important;
        height: 52px !important;
        background-color: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        margin-top: 10px;
        transition: all 0.2s ease;
    }
    
    div.stButton > button:hover {
        background-color: #cccccc !important;
        transform: scale(1.01);
    }

    /* Butonul de inapoi (Back) să fie mai subtil */
    div.stButton > button[kind="secondary"] {
        background-color: transparent !important;
        color: #666666 !important;
        border: 1px solid #222222 !important;
    }
    
    div.stButton > button[kind="secondary"]:hover {
        color: #ffffff !important;
        border-color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Structura Pagini
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<div class='logo-text'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Selectați modul de acces</div>", unsafe_allow_html=True)
    
    if st.button("Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("Director"):
        st.session_state.page = 'login_directoare'
        st.rerun()

elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='logo-text'>Login</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Introduceți datele de identificare</div>", unsafe_allow_html=True)
    
    materia = st.selectbox("Materia", ["Matematică", "Română", "Fizică"])
    parola = st.text_input("Parolă", type="password")
    
    if st.button("CONECTARE"):
        if parola == "123451":
            st.success("Acces permis.")
        else:
            st.error("Parolă incorectă.")
            
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
