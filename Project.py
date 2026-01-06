import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS - Deep Blue & Dark Mode
st.markdown("""
    <style>
    /* Fundal Albastru Foarte Închis */
    .stApp {
        background: radial-gradient(circle at center, #0a192f 0%, #020c1b 100%);
    }

    header, footer, #MainMenu {visibility: hidden !important;}

    /* Containerul central - Dark Blue Glass */
    .main .block-container {
        background: rgba(2, 12, 27, 0.8) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(100, 255, 218, 0.1) !important; /* Bordura cu o tenta de cyan foarte fina */
        border-radius: 20px !important;
        padding: 50px 40px !important;
        max-width: 450px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 15px rgba(10, 25, 47, 0.5) !important;
        margin-top: 8vh;
    }

    /* Titlu */
    .logo-text {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #ccd6f6; /* Albastru foarte deschis / alb */
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }

    .subtitle {
        color: #8892b0; /* Gri-albastru */
        font-size: 0.95rem;
        margin-bottom: 40px;
    }

    /* INPUT-URI SI SELECTBOX - DARK BLUE THEME */
    .stSelectbox label, .stTextInput label {
        color: #64ffda !important; /* Cyan (culoare de accent) */
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #112240 !important; /* Albastru mai deschis decat fundalul pentru contrast */
        border: 1px solid #233554 !important;
        border-radius: 8px !important;
    }

    /* Culoarea textului in casute */
    input, div[data-baseweb="select"] * {
        color: #e6f1ff !important;
    }

    /* BUTOANE - White Chrome Look */
    div.stButton > button {
        width: 100% !important;
        height: 52px !important;
        background-color: #e6f1ff !important;
        color: #0a192f !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        margin-top: 10px;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background-color: #64ffda !important; /* Schimbare in cyan la hover */
        box-shadow: 0 0 20px rgba(100, 255, 218, 0.3);
        transform: translateY(-2px);
    }

    /* Butonul de inapoi */
    div.stButton > button[kind="secondary"] {
        background-color: transparent !important;
        color: #8892b0 !important;
        border: 1px solid #233554 !important;
    }
    
    div.stButton > button[kind="secondary"]:hover {
        color: #64ffda !important;
        border-color: #64ffda !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica (Home / Login)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<div class='logo-text'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Sistem de Management Școlar</div>", unsafe_allow_html=True)
    
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
    st.markdown("<div class='logo-text'>Conectare</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Introduceți datele profesorului</div>", unsafe_allow_html=True)
    
    materia = st.selectbox("Alege Materia", ["Matematică", "Română", "Fizică"])
    parola = st.text_input("Introdu Parola", type="password")
    
    if st.button("ACCESEAZĂ CATALOGUL"):
        if parola == "123451":
            st.success("Conectat cu succes!")
        else:
            st.error("Eroare: Parolă incorectă.")
            
    if st.button("← Înapoi", kind="secondary"):
        st.session_state.page = 'home'
        st.rerun()
