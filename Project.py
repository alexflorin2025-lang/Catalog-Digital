import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS pentru Centrare Absoluta si Chenar Stil Premium
st.markdown("""
    <style>
    /* Fundal negru pur */
    .stApp { background-color: #000000 !important; }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* ALINIRE LA MIJLOCUL ECRANULUI (Vertical si Orizontal) */
    .stApp > section > div {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
    }

    /* CHENARUL (CARDUL) CENTRAL */
    .main .block-container {
        background-color: #ffffff !important; /* Fundal alb ca in poza NoulCatalog */
        border-radius: 15px !important;
        padding: 40px !important;
        max-width: 400px !important;
        box-shadow: 0px 10px 30px rgba(255, 255, 255, 0.1) !important;
        text-align: center;
    }

    /* TITLU (Numele site-ului in chenar) */
    .titlu-chenar {
        color: #0056b3; /* Albastru profesional */
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .subtitlu-chenar {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 30px;
    }

    /* BUTOANELE DIN INTERIORUL CHENARULUI */
    div.stButton > button {
        width: 100% !important;
        height: 55px !important;
        background-color: #f8f9fa !important; /* Gri foarte deschis */
        color: #333 !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        margin-bottom: 10px !important;
        transition: 0.2s;
    }
    
    div.stButton > button:hover {
        background-color: #e2e6ea !important;
        border-color: #adb5bd !important;
        color: #000 !important;
    }

    /* Ascundere scrollbar inutil */
    body { overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica de navigare
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PAGINA START (CENTRATA IN CHENAR ALB) ---
if st.session_state.page == 'home':
    # Titlu interior
    st.markdown("<div class='titlu-chenar'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitlu-chenar'>alege cum vrei să te autentifici:</div>", unsafe_allow_html=True)
    
    # Butoanele centrate
    if st.button("Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    # Redenumit in Directoare
    if st.button("Directoare"):
        st.session_state.page = 'login_directoare'
        st.rerun()

# --- LOGIN PROFESOR ---
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='titlu-chenar'>Autentificare</div>", unsafe_allow_html=True)
    
    materia = st.selectbox("Materia", ["Limba Română", "Matematică", "Fizică"])
    parola = st.text_input("Parolă", type="password")
    
    if st.button("Conectare"):
        st.success("Acces permis")
        
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
