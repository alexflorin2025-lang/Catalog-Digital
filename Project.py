import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS - Ultra Dark, Mirror Gradient & No Scroll
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh !important;
        overflow: hidden !important;
        background-color: #000;
    }
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format");
        background-size: cover;
        background-position: center;
    }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* CARDUL CENTRAL CU GRADIENT OGLINDĂ */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: linear-gradient(to bottom, rgba(60,85,120,0.4), rgba(5,15,30,0.98) 50%, rgba(60,85,120,0.4)) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 25px;
        width: 340px !important;
        margin: auto;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }

    .catalog-title { color: white; font-size: 1.6rem; font-weight: 800; text-align: center; margin-bottom: 10px; }
    
    /* BUTOANE NEGRE */
    div.stButton > button {
        width: 100% !important;
        background-color: #000 !important;
        color: #fff !important;
        height: 45px;
        border-radius: 10px;
        border: 1px solid #333;
        font-weight: 700;
        margin-top: 5px;
    }
    
    /* INPUTURI */
    input, div[data-baseweb="select"] > div {
        background-color: rgba(0,0,0,0.7) !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    label p { color: #aaa !important; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica de Navigare și Stări
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- LOGICĂ PAGINI ---

# PAGINA PRINCIPALĂ
if st.session_state.page == 'home':
    st.markdown("<div class='catalog-title'>Catalog Digital</div>", unsafe_allow_html=True)
    if st.button("PROFESOR"): st.session_state.page = 'login_profesor'; st.rerun()
    if st.button("PĂRINTE / ELEV"): st.session_state.page = 'login_parinte'; st.rerun()
    if st.button("DIRECTOARE"): st.session_state.page = 'login_directoare'; st.rerun()

# PAGINA LOGIN PROFESOR
elif st.session_state.page == 'login_profesor' and not st.session_state.authenticated:
    st.markdown("<div class='catalog-title'>Logare Prof</div>", unsafe_allow_html=True)
    materia = st.selectbox("Materia", ["Matematică", "Română", "Fizică"], key="sel_prof")
    parola = st.text_input("Parolă", type="password", key="pwd_prof")
    
    if st.button("CONECTARE"):
        if parola == "1234": # Poți schimba parola aici
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")
    if st.button("← ÎNAPOI"): st.session_state.page = 'home'; st.rerun()

# INTERFAȚA PROFESOR (Dupa Logare)
elif st.session_state.page == 'login_profesor' and st.session_state.authenticated:
    st.markdown("<div class='catalog-title'>Panou Profesor</div>", unsafe_allow_html=True)
    
    actiune = st.radio("Ce doriți să introduceți?", ["Notă", "Absență"], key="act_prof")
    st.selectbox("Alege Elevul", ["Popescu Ion", "Ionescu Ana", "Vasile Dan"], key="elev_prof")
    
    if actiune == "Notă":
        st.slider("Selectează Nota", 1, 10, 10, key="nota_val")
        if st.button("SALVEAZĂ NOTA"):
            st.success("Nota a fost pusă!")
    else:
        st.date_input("Data Absenței", key="data_abs")
        if st.button("SALVEAZĂ ABSENȚA"):
            st.warning("Absență înregistrată!")

    if st.button("IEȘIRE (LOGOUT)"):
        st.session_state.authenticated = False
        st.session_state.page = 'home'
        st.rerun()

# PAGINA LOGIN PĂRINTE
elif st.session_state.page == 'login_parinte':
    st.markdown("<div class='catalog-title'>Părinte / Elev</div>", unsafe_allow_html=True)
    st.text_input("Cod ID Elev", key="id_el")
    parola_el = st.text_input("Parolă", type="password", key="pwd_el")
    if st.button("VEZI CATALOG"):
        if parola_el == "elev123": st.info("Se încarcă notele...")
        else: st.error("Parolă incorectă!")
    if st.button("← ÎNAPOI"): st.session_state.page = 'home'; st.rerun()

# PAGINA LOGIN DIRECTOARE
elif st.session_state.page == 'login_directoare':
    st.markdown("<div class='catalog-title'>Directoare</div>", unsafe_allow_html=True)
    pwd_d = st.text_input("Cod Manager", type="password", key="pwd_dir")
    if st.button("ACCES"):
        if pwd_d == "admin": st.success("Acces panou control")
        else: st.error("Cod invalid!")
    if st.button("← ÎNAPOI"): st.session_state.page = 'home'; st.rerun()
