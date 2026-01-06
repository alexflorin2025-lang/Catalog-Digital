import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS pentru Centrare, Chenar Alb și Butoane Late
st.markdown("""
    <style>
    /* Fundalul paginii este negru */
    .stApp { 
        background-color: #000000 !important; 
    }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* FORȚĂM CENTRAREA PE MIJLOCUL ECRANULUI */
    .stApp > section > div {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
    }

    /* CREĂM CHENARUL ALB (CARDUL) */
    /* Aceasta este partea care lipsea în imaginea ta */
    .main .block-container {
        background-color: #ffffff !important; /* FUNDAL ALB */
        border-radius: 15px !important;
        padding: 50px 40px !important;
        max-width: 450px !important; /* Lățimea cardului */
        box-shadow: 0px 20px 40px rgba(0, 0, 0, 0.5) !important;
        text-align: center !important;
        margin: auto !important;
    }

    /* TEXT LOGO */
    .logo-header {
        font-family: 'Segoe UI', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .blue { color: #007bff; }
    .orange { color: #ff9900; }
    .green { color: #28a745; }

    .subtitle {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 35px;
    }

    /* BUTOANELE - Acum sunt LUNGI (--------->>) în interiorul chenarului */
    div.stButton > button {
        width: 100% !important; /* Ocupă toată lățimea chenarului alb */
        height: 55px !important;
        background-color: #f1f3f5 !important;
        color: #333 !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        margin-bottom: 12px !important;
        transition: 0.2s;
    }
    
    div.stButton > button:hover {
        background-color: #e9ecef !important;
        border-color: #007bff !important;
        color: #007bff !important;
    }

    /* Eliminăm spațiile goale de la Streamlit */
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Conținutul aplicației
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    # Logo-ul stilizat ca în poză
    st.markdown("""
        <div class='logo-header'>
            <span class='blue'>Noul</span><span class='orange'>Catalog</span><span class='green'>.ro</span>
        </div>
        <div class='subtitle'>alege cum vrei să te autentifici:</div>
    """, unsafe_allow_html=True)
    
    # Butoanele care acum vor fi centrate și încadrate în alb
    if st.button("Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("Directoare"):
        st.session_state.page = 'login_directoare'
        st.rerun()

# Pagini de Login (păstrează același stil de card)
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='logo-header'><span class='blue'>Autentificare</span></div>", unsafe_allow_html=True)
    st.write("")
    materia = st.selectbox("Materia", ["Matematică", "Română"])
    parola = st.text_input("Parolă", type="password")
    if st.button("CONECTARE"):
        st.success("Succes!")
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
