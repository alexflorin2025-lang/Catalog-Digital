import streamlit as st

# 1. Configurare Pagina - Centrat pentru a sta în mijloc
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS PREMIUM - Chenar Central (Card)
st.markdown("""
    <style>
    /* Fundalul general (în afara chenarului) - Negru pur */
    .stApp { background-color: #000000 !important; }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* CHENARUL CENTRAL (Cutia) */
    .main .block-container {
        background-color: #0d1117 !important; /* Gri foarte închis */
        border: 2px solid #1f6feb !important; /* Bordură Albastră Elegantă */
        border-radius: 25px !important; /* Colțuri rotunjite */
        padding: 50px 30px !important;
        margin-top: 40px !important;
        max-width: 480px !important; /* Lățime fixă ca să arate bine centrat */
        box-shadow: 0px 0px 30px rgba(31, 111, 235, 0.15) !important; /* Umbră fină albastră */
    }

    /* TITLUL */
    .titlu-principal {
        text-align: center;
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .subtitlu {
        text-align: center;
        color: #8b949e;
        font-size: 0.9rem;
        margin-bottom: 40px;
    }

    /* BUTOANELE - Centrate și late în interiorul chenarului */
    div.stButton > button {
        width: 100% !important;
        height: 65px !important;
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 15px !important;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        border-color: #1f6feb !important; /* Se face albastru la atingere */
        color: #58a6ff !important;
        background-color: #1f242c !important;
    }

    /* INPUT-URI (pentru login) */
    input, .stSelectbox > div > div {
        background-color: #0d1117 !important;
        color: white !important;
        border: 1px solid #30363d !important;
    }
    
    label { color: #8b949e !important; }
    
    </style>
    """, unsafe_allow_html=True)

# 3. Logica Aplicatiei
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- ECRAN START ---
if st.session_state.page == 'home':
    # Titlul
    st.markdown("<div class='titlu-principal'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitlu'>Alegeți tipul de acces:</div>", unsafe_allow_html=True)
    
    # Butoanele în chenar
    if st.button("👨‍🏫  Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("👨‍👩‍👧  Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    # Aici am modificat: DIRECTOR în loc de Administrator
    if st.button("👔  Director"):
        st.session_state.page = 'login_director'
        st.rerun()

# --- LOGIN PROFESOR ---
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='titlu-principal'>Acces Profesor</div>", unsafe_allow_html=True)
    st.write("")
    
    materia = st.selectbox("Disciplina:", ["Matematică", "Română", "Engleză", "Istorie"])
    st.write("")
    parola = st.text_input("Parola:", type="password")
    
    st.write("<br>", unsafe_allow_html=True)
    
    if st.button("Autentificare"):
        if parola == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia})
            st.rerun()
        else:
            st.error("Parolă greșită!")
            
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()

# --- LOGIN DIRECTOR (Nou) ---
elif st.session_state.page == 'login_director':
    st.markdown("<div class='titlu-principal'>Acces Director</div>", unsafe_allow_html=True)
    st.write("")
    
    parola = st.text_input("Parolă Director:", type="password")
    
    st.write("<br>", unsafe_allow_html=True)
    if st.button("Logare Director"):
        st.success("Bine ați venit, Domnule Director!")
    
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
