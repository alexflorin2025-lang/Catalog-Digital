import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS pentru Dark, Imagine de Fundal si Butoane Albe
st.markdown("""
    <style>
    /* Imagine de fundal: o clasa cu copii si un catalog, estompata */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        /* Strat intunecat peste imagine pentru lizibilitate */
        background-color: rgba(0, 0, 0, 0.7); 
        background-blend-mode: darken;
    }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* Centrare perfectă a cardului */
    .stApp > section > div {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
    }

    /* CHENARUL CENTRAL - Acum este DARK, nu alb */
    .main .block-container {
        background-color: rgba(20, 20, 20, 0.8) !important; /* Gri inchis, semi-transparent */
        border: 1px solid rgba(255, 255, 255, 0.1) !important; /* Bordura alba subtila */
        border-radius: 15px !important;
        padding: 50px 40px !important;
        max-width: 450px !important;
        box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.7) !important;
        text-align: center !important;
    }

    /* TITLU "Catalog Digital" */
    .logo-text {
        font-family: 'Segoe UI', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        color: #e0e0e0; /* Alb aproape pur */
        margin-bottom: 10px;
    }

    .subtitle {
        color: #aaaaaa; /* Gri deschis */
        font-size: 0.9rem;
        margin-bottom: 35px;
    }

    /* BUTOANE ALBE CU TEXT DARK */
    div.stButton > button {
        width: 100% !important;
        height: 55px !important;
        background-color: #ffffff !important; /* Butoane albe */
        color: #333333 !important; /* Text negru pe buton alb */
        border: 1px solid #cccccc !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 15px !important;
        transition: 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    div.stButton > button:hover {
        background-color: #f0f0f0 !important;
        border-color: #007bff !important;
        color: #007bff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Conținutul aplicației
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<div class='logo-text'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Alegeți profilul pentru autentificare:</div>", unsafe_allow_html=True)
    
    if st.button("Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("Directoare"):
        st.session_state.page = 'login_directoare'
        st.rerun()

# Pagini de Login
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='logo-text'>Autentificare</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Acces Profesor</div>", unsafe_allow_html=True)
    
    materia = st.selectbox("Materia", ["Matematică", "Română"])
    parola = st.text_input("Parolă", type="password")
    
    if st.button("CONECTARE"):
        if parola == "123451":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Eroare de autentificare")
            
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
