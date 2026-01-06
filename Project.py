import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS - Ultra Dark cu Gradient Vertical în Card
st.markdown("""
    <style>
    /* Fundalul general ramane neschimbat */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.9)), 
                    url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    header, footer, #MainMenu {visibility: hidden !important;}

    /* CHENARUL CENTRAL - Acum are Gradient Vertical */
    .main .block-container {
        /* Gradient de la un gri-albastru foarte inchis (jos) la unul mai deschis (sus) */
        background: linear-gradient(to top, rgba(5, 5, 5, 0.9), rgba(25, 35, 50, 0.7)) !important;
        
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 30px !important;
        padding: 60px 50px !important;
        max-width: 500px !important;
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.9) !important;
        margin-top: 5vh;
    }

    /* Titlu */
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
        color: #8b949e;
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
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent);
        margin: 30px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica Navigatie (cu Keys unice pentru fix parola)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<div class='logo-text'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Portal de Management Educațional</div>", unsafe_allow_html=True)
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
    st.markdown("<div class='logo-text'>Logare Prof</div>", unsafe_allow_html=True)
    materia = st.selectbox("Alege Materia", ["Matematică", "Română", "Fizică"], key="sel_prof_v37")
    parola = st.text_input("Introdu Parola", type="password", key="pwd_prof_v37")
    
    if st.button("AUTENTIFICARE"):
        if parola == "123451":
            st.success("Sistem deblocat!")
        else:
            st.error("Parolă incorectă.")
            
    if st.button("← ÎNAPOI"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'login_directoare':
    st.markdown("<div class='logo-text'>Directoare</div>", unsafe_allow_html=True)
    parola_d = st.text_input("Cod Managerial", type="password", key="pwd_dir_v37")
    
    if st.button("ACCES SISTEM"):
        st.warning("Se verifică autorizația...")
        
    if st.button("← ÎNAPOI"):
        st.session_state.page = 'home'
        st.rerun()
