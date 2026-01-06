import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# CSS - Deep Blue & Dark Mode (Păstrat conform cerinței)
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #0a192f 0%, #020c1b 100%); }
    header, footer, #MainMenu {visibility: hidden !important;}
    .main .block-container {
        background: rgba(2, 12, 27, 0.8) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(100, 255, 218, 0.1) !important;
        border-radius: 20px !important;
        padding: 50px 40px !important;
        max-width: 450px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5) !important;
        margin-top: 8vh;
    }
    .logo-text { font-family: 'Inter', sans-serif; font-size: 2.5rem; font-weight: 700; color: #ccd6f6; margin-bottom: 5px; text-align: center; }
    .subtitle { color: #8892b0; font-size: 0.95rem; margin-bottom: 40px; text-align: center; }
    
    /* Etichete si Input-uri */
    .stSelectbox label, .stTextInput label { color: #64ffda !important; font-size: 0.8rem !important; letter-spacing: 1px; }
    div[data-baseweb="select"], div[data-baseweb="input"] { background-color: #112240 !important; border: 1px solid #233554 !important; border-radius: 8px !important; }
    input, div[data-baseweb="select"] * { color: #e6f1ff !important; }

    /* Butoane */
    div.stButton > button {
        width: 100% !important; height: 52px !important; background-color: #e6f1ff !important;
        color: #0a192f !important; border-radius: 8px !important; font-weight: 700 !important;
        transition: all 0.3s ease; margin-top: 10px;
    }
    div.stButton > button:hover { background-color: #64ffda !important; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# 2. Inițializare Stări (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'autentificat' not in st.session_state:
    st.session_state.autentificat = False

# 3. Logica de Navigare
if st.session_state.page == 'home':
    st.markdown("<div class='logo-text'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Sistem de Management Școlar</div>", unsafe_allow_html=True)
    
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
    st.markdown("<div class='logo-text'>Conectare</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Acces securizat Profesor</div>", unsafe_allow_html=True)
    
    materia = st.selectbox("Alege Materia", ["Matematică", "Română", "Fizică"])
    parola = st.text_input("Introdu Parola", type="password")
    
    if st.button("ACCESEAZĂ CATALOGUL"):
        if parola == "123451":
            st.session_state.autentificat = True
            st.success("Autentificare reușită!")
            # Aici poți redirecționa către pagina de catalog
            # st.session_state.page = 'catalog_profesor'
            # st.rerun()
        else:
            st.error("Parolă incorectă! Încearcă din nou.")
            
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
