import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS Modernizat (Premium Dark Theme)
st.markdown("""
    <style>
    /* Fundal cu Gradient Modern și Overlay */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        background-attachment: fixed;
    }

    /* Ascundere elemente Streamlit standard */
    header, footer, #MainMenu {visibility: hidden !important;}

    /* Centrare și Glassmorphism pentru containerul principal */
    .main .block-container {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        padding: 60px 45px !important;
        max-width: 450px !important;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3) !important;
        margin-top: 10vh;
    }

    /* Stil Titlu */
    .logo-text {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(to right, #ffffff, #a5a5a5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    .subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 1rem;
        margin-bottom: 40px;
        font-weight: 400;
    }

    /* Butoane Stilizate (White Gloss) */
    div.stButton > button {
        width: 100% !important;
        height: 55px !important;
        background-color: #ffffff !important;
        color: #1a1a2e !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2);
        background-color: #f8f9fa !important;
        color: #007bff !important;
    }

    /* Stil pentru Input-uri (Selectbox & Password) */
    .stSelectbox label, .stTextInput label {
        color: white !important;
        font-weight: 500 !important;
    }
    
    input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica aplicației (Rămâne neschimbată, dar aplică stilul nou)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<div class='logo-text'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Alegeți profilul pentru autentificare</div>", unsafe_allow_html=True)
    
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
    st.markdown("<div class='subtitle'>Acces securizat pentru profesori</div>", unsafe_allow_html=True)
    
    materia = st.selectbox("Materia", ["Matematică", "Română", "Fizică", "Informatică"])
    parola = st.text_input("Introdu parola", type="password")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Înapoi"):
            st.session_state.page = 'home'
            st.rerun()
    with col2:
        if st.button("CONECTARE"):
            if parola == "123451":
                st.success("Autentificare reușită!")
            else:
                st.error("Parolă incorectă")
