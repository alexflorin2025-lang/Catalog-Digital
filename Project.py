import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS - Ultra Dark Blue & Forced Dark Inputs
st.markdown("""
    <style>
    /* Fundalul General */
    .stApp {
        background: radial-gradient(circle at center, #0a192f 0%, #020c1b 100%);
    }

    header, footer, #MainMenu {visibility: hidden !important;}

    /* Cardul Central */
    .main .block-container {
        background: rgba(2, 12, 27, 0.9) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(100, 255, 218, 0.1) !important;
        border-radius: 20px !important;
        padding: 40px 40px !important;
        max-width: 450px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6) !important;
        margin-top: 5vh;
    }

    /* Texte Titluri */
    .logo-text { font-family: 'Inter', sans-serif; font-size: 2.2rem; font-weight: 700; color: #ccd6f6; text-align: center; margin-bottom: 5px; }
    .subtitle { color: #8892b0; font-size: 0.9rem; text-align: center; margin-bottom: 30px; }

    /* FORȚARE CĂSUȚE DARK (Selectbox & Text Input) */
    /* Această parte asigură că fundalul rămâne negru/albastru închis pe orice pagină */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div,
    input {
        background-color: #040d1a !important;
        color: #e6f1ff !important;
        border: 1px solid #112240 !important;
    }
    
    /* Etichetele (Labels) de deasupra căsuțelor */
    label p {
        color: #64ffda !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }

    /* BUTOANE - White Chrome Look */
    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        background-color: #e6f1ff !important;
        color: #0a192f !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        margin-top: 10px;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #64ffda !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(100, 255, 218, 0.3);
    }

    /* Erori și Succes mai stilizate */
    .stAlert {
        background-color: rgba(2, 12, 27, 0.8) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Inițializare Session State
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- LOGICA PAGINILOR ---

# PAGINA: HOME
if st.session_state.page == 'home':
    st.markdown("<div class='logo-text'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Alegeți profilul de utilizator</div>", unsafe_allow_html=True)
    
    if st.button("👨‍🏫 Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()
    if st.button("👨‍👩‍👧‍👦 Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()
    if st.button("👩‍💼 Directoare"):
        st.session_state.page = 'login_directoare'
        st.rerun()

# PAGINA: LOGIN PROFESOR
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='logo-text'>Login Profesor</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Introduceți datele de acces</div>", unsafe_allow_html=True)
    
    materia = st.selectbox("Materia", ["Matematică", "Română", "Fizică", "Informatică"])
    parola = st.text_input("Parolă", type="password", key="pass_prof")
    
    if st.button("CONECTARE"):
        if parola == "123451":
            st.success("Autentificat cu succes!")
        else:
            st.error("Parolă incorectă.")
            
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()

# PAGINA: LOGIN PARINTE
elif st.session_state.page == 'login_parinte':
    st.markdown("<div class='logo-text'>Login Părinte</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Acces note și absențe elev</div>", unsafe_allow_html=True)
    
    nume_elev = st.text_input("Nume Elev")
    cod_acces = st.text_input("Cod Parinte", type="password", key="pass_parinte")
    
    if st.button("VEZI CATALOG"):
        st.info("Sistemul caută datele elevului...")
        
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()

# PAGINA: LOGIN DIRECTOARE
elif st.session_state.page == 'login_directoare':
    st.markdown("<div class='logo-text'>Management</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Acces Administrație</div>", unsafe_allow_html=True)
    
    admin_user = st.text_input("Utilizator Admin")
    admin_pass = st.text_input("Parolă Master", type="password", key="pass_admin")
    
    if st.button("LOGARE ADMIN"):
        if admin_pass == "admin123":
            st.success("Acces panou control.")
        else:
            st.error("Credentiale gresite.")
            
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
