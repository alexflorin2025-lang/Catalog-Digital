import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="wide")

# 2. CSS FORȚAT pentru Centrare, Fundal și Gradient Oglindă
st.markdown("""
    <style>
    /* 1. FUNDALUL ÎNTREGII PAGINI CU IMAGINEA DE CLASĂ */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), 
                    url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* 2. FORȚĂM TOTUL SĂ STEA LA MIJLOCUL ECRANULUI (ORIZONTAL ȘI VERTICAL) */
    .main {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
    }

    /* 3. CHENARUL CENTRAL (CARDUL) */
    /* Folosim un selector extrem de specific pentru a suprascrie Streamlit */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: linear-gradient(
            to bottom, 
            rgba(60, 80, 110, 0.5) 0%,     /* Mai deschis sus */
            rgba(5, 15, 30, 0.95) 50%,     /* Albastru Dark la MIJLOC */
            rgba(60, 80, 110, 0.5) 100%    /* Mai deschis jos */
        ) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 30px !important;
        padding: 60px 40px !important;
        width: 450px !important;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8) !important;
        margin: auto !important;
    }

    /* 4. TITLU "CATALOG DIGITAL" */
    .catalog-title {
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 2.8rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
    }
    
    .catalog-sub {
        color: #adb5bd;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 40px;
    }

    /* 5. BUTOANELE NEGRE (DOREAI DARK) */
    div.stButton > button {
        width: 100% !important;
        background-color: #000000 !important; /* Negru pur */
        color: #ffffff !important;
        height: 55px !important;
        border-radius: 12px !important;
        border: 1px solid #2d3748 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin-bottom: 15px !important;
        transition: 0.3s !important;
    }
    
    div.stButton > button:hover {
        border-color: #ffffff !important;
        background-color: #111111 !important;
        transform: translateY(-2px) !important;
    }

    /* Ascundere elemente Streamlit */
    header, footer, #MainMenu {visibility: hidden !important;}
    </style>
    """, unsafe_allow_html=True)

# 3. LOGICA APLICAȚIEI
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Folosim un container central pentru a ajuta centrarea
with st.container():
    if st.session_state.page == 'home':
        st.markdown("<h1 class='catalog-title'>Catalog Digital</h1>", unsafe_allow_html=True)
        st.markdown("<p class='catalog-sub'>Portal de Management Educațional</p>", unsafe_allow_html=True)
        
        # Butoanele negre
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
        st.markdown("<h1 class='catalog-title'>Autentificare</h1>", unsafe_allow_html=True)
        parola = st.text_input("Parolă", type="password", key="pwd_p_v39")
        if st.button("CONECTARE"):
            st.success("OK")
        if st.button("← ÎNAPOI"):
            st.session_state.page = 'home'
            st.rerun()
