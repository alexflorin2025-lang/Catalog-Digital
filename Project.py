import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS PREMIUM - Chenar Albastru Centrat
st.markdown("""
    <style>
    /* Fundal general negru */
    .stApp { background-color: #000000 !important; }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* CHENARUL CENTRAL (Cardul) */
    .main .block-container {
        background-color: #0d1117 !important;
        border: 1px solid #1f6feb !important; /* Bordură subțire albastră */
        border-radius: 20px !important;
        padding: 60px 40px !important;
        margin-top: 50px !important;
        max-width: 450px !important;
        box-shadow: 0px 10px 40px rgba(0, 0, 0, 0.5) !important;
    }

    /* TITLU */
    .titlu-principal {
        text-align: center;
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 40px;
    }

    /* BUTOANELE - Late și centrate în chenar --------->> */
    div.stButton > button {
        width: 100% !important;
        height: 65px !important;
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        margin-bottom: 20px !important;
        transition: 0.3s ease;
    }
    
    div.stButton > button:hover {
        border-color: #58a6ff !important;
        background-color: #1f242c !important;
    }

    /* Stil pentru paginile de login */
    input, .stSelectbox > div > div {
        background-color: #0d1117 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        height: 50px !important;
    }
    
    label { color: #8b949e !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica de navigare
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- ECRAN START ---
if st.session_state.page == 'home':
    st.markdown("<div class='titlu-principal'>Catalog Digital</div>", unsafe_allow_html=True)
    
    # Butoanele centrate în chenar
    if st.button("Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("Director"):
        st.session_state.page = 'login_director'
        st.rerun()

# --- LOGIN PROFESOR ---
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='titlu-principal'>Logare Profesor</div>", unsafe_allow_html=True)
    
    materia = st.selectbox("Selectați Materia:", ["Matematică", "Română", "Engleză", "Istorie"])
    parola = st.text_input("Parolă:", type="password")
    
    st.write("<br>", unsafe_allow_html=True)
    if st.button("Conectare"):
        if parola == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia})
            st.rerun()
        else:
            st.error("Acces refuzat")
            
    if st.button("Înapoi"):
        st.session_state.page = 'home'
        st.rerun()

# --- LOGIN DIRECTOR ---
elif st.session_state.page == 'login_director':
    st.markdown("<div class='titlu-principal'>Logare Director</div>", unsafe_allow_html=True)
    
    parola = st.text_input("Parolă Director:", type="password")
    
    st.write("<br>", unsafe_allow_html=True)
    if st.button("Acces Panou Control"):
        st.success("Sistem autorizat")
    
    if st.button("Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
