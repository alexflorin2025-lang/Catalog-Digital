import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS - Centrare Absolută și Fixare Input-uri
st.markdown("""
    <style>
    /* Eliminăm orice posibilitate de scroll */
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                    url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
    }

    header, footer, #MainMenu {visibility: hidden !important;}

    /* Cardul cu Gradient Oglindă (Mirror) */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: linear-gradient(
            to bottom, 
            rgba(60, 85, 120, 0.4) 0%,     /* Sus deschis */
            rgba(5, 15, 30, 0.98) 50%,     /* MIJLOC Albastru Dark */
            rgba(60, 85, 120, 0.4) 100%    /* Jos deschis */
        ) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 20px !important;
        padding: 30px 25px !important;
        width: 320px !important; /* Lățime fixă mică pentru mobil */
        margin: auto !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9) !important;
    }

    .catalog-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 20px;
    }

    /* BUTOANE NEGRE */
    div.stButton > button {
        width: 100% !important;
        background-color: #000000 !important;
        color: #ffffff !important;
        height: 48px !important;
        border-radius: 12px !important;
        border: 1px solid #333 !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }

    /* STILIZARE INPUT PAROLĂ */
    input {
        background-color: rgba(0, 0, 0, 0.7) !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica de Navigare
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PAGINA START ---
if st.session_state.page == 'home':
    st.markdown("<div class='catalog-title'>Catalog Digital</div>", unsafe_allow_html=True)
    
    if st.button("PROFESOR"):
        st.session_state.page = 'login_profesor'
        st.rerun()
    if st.button("PĂRINTE / ELEV"):
        st.session_state.page = 'login_parinte'
        st.rerun()
    if st.button("DIRECTOARE"):
        st.session_state.page = 'login_directoare'
        st.rerun()

# --- LOGIN PROFESOR ---
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='catalog-title'>Logare Prof</div>", unsafe_allow_html=True)
    
    # Folosim chei unice (key) pentru ca input-ul să nu se blocheze
    materia = st.selectbox("Materia", ["Matematică", "Română"], key="sel_p")
    parola = st.text_input("Parolă", type="password", key="pwd_p")
    
    if st.button("CONECTARE"):
        if parola == "123451":
            st.success("Acces permis")
        else:
            st.error("Parolă incorectă")
            
    if st.button("← ÎNAPOI"):
        st.session_state.page = 'home'
        st.rerun()

# --- LOGIN DIRECTOARE ---
elif st.session_state.page == 'login_directoare':
    st.markdown("<div class='catalog-title'>Directoare</div>", unsafe_allow_html=True)
    
    parola_d = st.text_input("Cod Manager", type="password", key="pwd_d")
    
    if st.button("AUTENTIFICARE"):
        st.warning("Verificare...")
        
    if st.button("← ÎNAPOI"):
        st.session_state.page = 'home'
        st.rerun()
