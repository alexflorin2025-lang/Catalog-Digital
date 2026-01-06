import streamlit as st

# 1. Configurare Pagina - Revenim la "centered" pentru a avea margini
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS - Design Dark cu Margini de Siguranță
st.markdown("""
    <style>
    /* Fundal general */
    .stApp { background-color: #0d1117 !important; }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* CONTAINERUL PRINCIPAL - Îl facem mai mic pe lățime */
    .main .block-container {
        max-width: 500px !important; /* Limită ca să nu atingă marginile */
        padding-top: 40px !important;
        padding-left: 20px !important; /* Margine stânga */
        padding-right: 20px !important; /* Margine dreapta */
    }

    /* TITLU */
    .titlu-principal {
        text-align: center;
        color: #58a6ff;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 40px;
        text-shadow: 0px 0px 10px rgba(88, 166, 255, 0.2);
    }

    /* BUTOANELE - Se întind MAXIM în interiorul containerului sigur */
    div.stButton > button {
        width: 100% !important; /* Ocupă tot spațiul disponibil */
        height: 85px !important;
        background-color: #161b22 !important;
        color: white !important;
        border: 2px solid #30363d !important;
        border-radius: 18px !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        margin-bottom: 25px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: 0.2s;
    }
    
    div.stButton > button:hover {
        border-color: #58a6ff !important;
        background-color: #1f242c !important;
        transform: translateY(-2px);
    }

    /* Input-uri */
    input {
        background-color: #0d1117 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        height: 55px !important;
    }
    
    label { color: #8b949e !important; font-size: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Interfața
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<div class='titlu-principal'>🎓 Catalog Digital</div>", unsafe_allow_html=True)
    
    st.write("") # Spațiu mic
    
    # Butoanele sunt late, dar nu ating marginea ecranului
    if st.button("👨‍🏫 Acces Modul Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("👪 Acces Părinți / Elevi"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("🛡️ Panou Control Director"):
        st.session_state.page = 'login_administrator'
        st.rerun()

elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='titlu-principal'>🔑 Autentificare</div>", unsafe_allow_html=True)
    
    materia = st.selectbox("Materia:", ["Limba Română", "Matematică", "Engleză", "Istorie"])
    st.write("")
    parola = st.text_input("Parolă:", type="password")
    
    st.write("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Conectare"):
        st.success("Logare reușită!")
        
    if st.button("⬅️ Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
