import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS - Ultra Compact & Responsive (Mirror Gradient)
st.markdown("""
    <style>
    /* FUNDAL ȘI ELIMINARE SCROLL GENERAL */
    html, body , [data-testid="stAppViewContainer"] {
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                    url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
    }

    header, footer, #MainMenu {visibility: hidden !important;}

    /* CENTRARE CARD */
    [data-testid="stVerticalBlock"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* CARDUL CU GRADIENT OGLINDĂ - DIMENSIUNI MICI */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: linear-gradient(
            to bottom, 
            rgba(50, 70, 100, 0.4) 0%, 
            rgba(5, 15, 35, 0.98) 50%, 
            rgba(50, 70, 100, 0.4) 100%
        ) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 25px 20px !important; /* Padding redus mult */
        width: 90% !important; /* Adaptabil pe mobil */
        max-width: 350px !important; /* Mai îngust */
        margin: auto !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8) !important;
    }

    /* TITLU ȘI SUBTITLU MICI */
    .catalog-title {
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 1.6rem !important; /* Font mic pentru mobil */
        font-weight: 800;
        text-align: center;
        margin-bottom: 2px !important;
    }
    
    .catalog-sub {
        color: #8892b0;
        text-align: center;
        font-size: 0.8rem !important;
        margin-bottom: 20px !important;
    }

    /* BUTOANE NEGRE COMPACTE */
    div.stButton > button {
        width: 100% !important;
        background-color: #000000 !important;
        color: #ffffff !important;
        height: 45px !important; /* Mai scunde */
        border-radius: 10px !important;
        border: 1px solid #1a202c !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 8px !important;
        transition: 0.2s !important;
    }
    
    div.stButton > button:hover {
        border-color: #ffffff !important;
    }

    /* INPUT-URI COMPACTE */
    input {
        height: 40px !important;
        font-size: 0.9rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGICA APLICAȚIEI
if 'page' not in st.session_state:
    st.session_state.page = 'home'

with st.container():
    if st.session_state.page == 'home':
        st.markdown("<div class='catalog-title'>Catalog Digital</div>", unsafe_allow_html=True)
        st.markdown("<div class='catalog-sub'>Management Școlar</div>", unsafe_allow_html=True)
        
        if st.button("PROFESOR"):
            st.session_state.page = 'login_profesor'
            st.rerun()
            
        if st.button("PĂRINTE / ELEV"):
            st.session_state.page = 'login_parinte'
            st.rerun()
            
        if st.button("DIRECTOARE"):
            st.session_state.page = 'login_directoare'
            st.rerun()

    elif st.session_state.page == 'login_profesor':
        st.markdown("<div class='catalog-title'>Logare</div>", unsafe_allow_html=True)
        parola = st.text_input("Parolă", type="password", key="p_mobile")
        if st.button("CONECTARE"):
            st.success("Succes")
        if st.button("← ÎNAPOI"):
            st.session_state.page = 'home'
            st.rerun()
