import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS - Mirror Gradient & Ultra Dark Buttons
st.markdown("""
    <style>
    /* Fundal general cinematic cu imaginea de clasa */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.88), rgba(0, 0, 0, 0.88)), 
                    url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    header, footer, #MainMenu {visibility: hidden !important;}

    /* CHENARUL CENTRAL - GRADIENT OGLINDĂ (Deschis -> Albastru Dark -> Deschis) */
    .main .block-container {
        /* Sus: Gri-albastru deschis | Mijloc: Albastru foarte inchis | Jos: Gri-albastru deschis */
        background: linear-gradient(
            to bottom, 
            rgba(40, 55, 75, 0.6) 0%, 
            rgba(5, 12, 25, 0.95) 50%, 
            rgba(40, 55, 75, 0.6) 100%
        ) !important;
        
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 35px !important;
        padding: 60px 50px !important;
        max-width: 500px !important;
        box-shadow: 0 50px 120px rgba(0, 0, 0, 1) !important;
        margin-top: 5vh;
        text-align: center;
    }

    /* Titlu Premium cu Glow */
    .logo-text {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 5px;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
    }

    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 40px;
    }

    /* BUTOANELE TALE NEGRE (DARK) */
    div.stButton > button {
        width: 100% !important;
        height: 60px !important;
        background: #000000 !important; /* Negru pur */
        color: #ffffff !important;
        border: 1px solid #1e293b !important;
        border-radius: 16px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin-top: 15px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    div.stButton > button:hover {
        background: #0a0a0a !important;
        border-color: #ffffff !important; /* Glow la atingere */
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
    }

    /* Input-uri (Fix Vizibilitate) */
    input, div[data-baseweb="select"] > div {
        background-color: rgba(0, 0, 0, 0.8) !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }

    label p { color: #cbd5e1 !important; }

    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent);
        margin: 30px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica Navigatie
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<div class='logo-text'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Platformă Securizată</div>", unsafe_allow_html=True)
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

elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='logo-text'>Acces Prof</div>", unsafe_allow_html=True)
    st.write("")
    materia = st.selectbox("Disciplina", ["Matematică", "Română", "Engleză"], key="prof_v38")
    parola = st.text_input("Parolă", type="password", key="pwd_prof_v38")
    
    if st.button("AUTENTIFICARE"):
        if parola == "123451":
            st.success("Sistem deblocat")
        else:
            st.error("Eroare!")
            
    if st.button("← ÎNAPOI"):
        st.session_state.page = 'home'
        st.rerun()
