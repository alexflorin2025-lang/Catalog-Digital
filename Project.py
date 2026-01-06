import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS - Ultra Dark, Glassmorphism & Butoane Negre
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                    url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    header, footer, #MainMenu {visibility: hidden !important;}

    .main .block-container {
        background: rgba(10, 10, 10, 0.6) !important;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 30px !important;
        padding: 60px 50px !important;
        max-width: 500px !important;
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.9) !important;
        margin-top: 5vh;
    }

    .logo-text {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
    }

    .subtitle {
        color: #666;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 40px;
    }

    /* BUTOANE NEGRE MODERNE */
    div.stButton > button {
        width: 100% !important;
        height: 60px !important;
        background: #050505 !important;
        color: #ffffff !important;
        border: 1px solid #1b263b !important;
        border-radius: 15px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin-top: 15px;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background: #111111 !important;
        border-color: #ffffff !important;
        transform: translateY(-2px);
    }

    /* Input-uri Ultra Dark */
    input, div[data-baseweb="select"] > div {
        background-color: rgba(0, 0, 0, 0.9) !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
    }

    label p { color: #e0e1dd !important; }

    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(to right, transparent, #333, transparent);
        margin: 30px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica Navigatie
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- ECRAN START ---
if st.session_state.page == 'home':
    st.markdown("<div class='logo-text'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Sistem Securizat de Management</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    if st.button("PROFESOR"):
        st.session_state.page = 'login_profesor'
        st.rerun()
    if st.button("PĂRINTE / ELEV"):
        st.session_state.page = 'login_parinte'
        st.rerun()
    if st.button("DIRECTOARE"):
        st.session_state.page = 'login_directoare'
        st.rerun()

# --- LOGIN PROFESOR (Fix Parola) ---
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='logo-text'>Logare Prof</div>", unsafe_allow_html=True)
    materia = st.selectbox("Alege Materia", ["Matematică", "Română", "Fizică"], key="sel_prof")
    # key="pwd_prof" rezolvă eroarea de input
    parola = st.text_input("Introdu Parola", type="password", key="pwd_prof")
    
    if st.button("AUTENTIFICARE"):
        if parola == "123451":
            st.success("Acces permis!")
        else:
            st.error("Parolă greșită.")
            
    if st.button("← ÎNAPOI"):
        st.session_state.page = 'home'
        st.rerun()

# --- LOGIN PĂRINTE (Fix Parola) ---
elif st.session_state.page == 'login_parinte':
    st.markdown("<div class='logo-text'>Părinte / Elev</div>", unsafe_allow_html=True)
    cod_elev = st.text_input("Cod Identificare Elev", key="id_elev")
    parola_p = st.text_input("Parolă Părinte", type="password", key="pwd_parinte")
    
    if st.button("VEZI SITUAȚIA"):
        st.info("Se încarcă datele...")
        
    if st.button("← ÎNAPOI"):
        st.session_state.page = 'home'
        st.rerun()

# --- LOGIN DIRECTOARE (Fix Parola) ---
elif st.session_state.page == 'login_directoare':
    st.markdown("<div class='logo-text'>Directoare</div>", unsafe_allow_html=True)
    parola_d = st.text_input("Cod Managerial", type="password", key="pwd_dir")
    
    if st.button("ACCES TOTAL"):
        st.warning("Se deschide panoul de control...")
        
    if st.button("← ÎNAPOI"):
        st.session_state.page = 'home'
        st.rerun()
