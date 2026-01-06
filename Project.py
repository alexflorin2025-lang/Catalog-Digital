import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="wide")

# 2. CSS Optimizat pentru a elimina Scroll-ul
st.markdown("""
    <style>
    /* 1. FUNDAL ȘI ELIMINARE SCROLL */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                    url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
        height: 100vh !important;
        overflow: hidden !important; /* ELIMINĂ SCROLL-UL */
    }

    /* 2. CENTRARE VERTICALĂ ȘI ORIZONTALĂ */
    .main {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 100vh !important;
    }

    /* 3. CARDUL CU GRADIENT OGLINDĂ (COMPACT) */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: linear-gradient(
            to bottom, 
            rgba(50, 70, 100, 0.4) 0%,     /* Sus - mai deschis */
            rgba(5, 15, 35, 0.98) 50%,     /* MIJLOC - Albastru Dark */
            rgba(50, 70, 100, 0.4) 100%    /* Jos - mai deschis */
        ) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 25px !important;
        padding: 35px 40px !important; /* Padding redus pentru compactare */
        width: 420px !important;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.9) !important;
        margin: auto !important;
    }

    /* 4. TITLU MAI MIC */
    .catalog-title {
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem; /* Redus de la 2.8 */
        font-weight: 900;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
    }
    
    .catalog-sub {
        color: #8892b0;
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 25px;
    }

    /* 5. BUTOANE NEGRE COMPACTE */
    div.stButton > button {
        width: 100% !important;
        background-color: #000000 !important;
        color: #ffffff !important;
        height: 50px !important; /* Înălțime redusă */
        border-radius: 10px !important;
        border: 1px solid #1a202c !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        margin-bottom: 10px !important;
        transition: 0.3s !important;
    }
    
    div.stButton > button:hover {
        border-color: #ffffff !important;
        transform: scale(1.02) !important;
    }

    /* Ascundere UI Streamlit */
    header, footer, #MainMenu {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# 3. LOGICA
if 'page' not in st.session_state:
    st.session_state.page = 'home'

with st.container():
    if st.session_state.page == 'home':
        st.markdown("<h1 class='catalog-title'>Catalog Digital</h1>", unsafe_allow_html=True)
        st.markdown("<p class='catalog-sub'>Management Educațional</p>", unsafe_allow_html=True)
        
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
        st.markdown("<h1 class='catalog-title'>Logare</h1>", unsafe_allow_html=True)
        st.write("")
        user = st.text_input("Utilizator", key="u_v40")
        parola = st.text_input("Parolă", type="password", key="p_v40")
        if st.button("CONECTARE"):
            st.success("Acces permis")
        if st.button("← ÎNAPOI"):
            st.session_state.page = 'home'
            st.rerun()
