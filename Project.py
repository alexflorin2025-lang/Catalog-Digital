import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS pentru replicarea stilului NoulCatalog.ro
st.markdown("""
    <style>
    /* Fundal general negru sau imagine (aici am lasat negru pentru claritate) */
    .stApp { 
        background-color: #000000 !important; 
    }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* CENTRARE ABSOLUTĂ A CARDULUI */
    .stApp > section > div {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
    }

    /* CHENARUL (CARDUL) ALB - Ca in poza */
    .main .block-container {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 40px 30px !important;
        max-width: 420px !important;
        box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.4) !important;
        text-align: center;
    }

    /* TEXTUL DE LOGO (NoulCatalog.ro style) */
    .logo-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .logo-blue { color: #007bff; }
    .logo-orange { color: #ff9900; }
    .logo-green { color: #28a745; }

    .instructiuni {
        color: #666;
        font-size: 0.85rem;
        margin-bottom: 30px;
    }

    /* BUTOANELE DREPTUNGHIULARE CURATE --------->> */
    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        background-color: #f8f9fa !important;
        color: #333 !important;
        border: 1px solid #ced4da !important;
        border-radius: 6px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        margin-bottom: 8px !important;
        transition: all 0.2s;
    }
    
    div.stButton > button:hover {
        background-color: #e9ecef !important;
        border-color: #adb5bd !important;
        color: #000 !important;
    }

    /* Stil pentru campurile de login */
    input {
        border-radius: 6px !important;
        border: 1px solid #ced4da !important;
    }
    
    label { 
        text-align: left !important;
        width: 100%;
        display: block;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica de navigare
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- ECRAN START (CARD ALB CENTRAT) ---
if st.session_state.page == 'home':
    # Titlu stilizat
    st.markdown("""
        <div class='logo-text'>
            <span class='logo-blue'>Noul</span><span class='logo-orange'>Catalog</span><span class='logo-green'>.ro</span>
        </div>
        <div class='instructiuni'>alege cum vrei să te autentifici:</div>
    """, unsafe_allow_html=True)
    
    # Butoanele
    if st.button("Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("Directoare"):
        st.session_state.page = 'login_directoare'
        st.rerun()

# --- LOGIN PROFESOR ---
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='logo-text'><span class='logo-blue'>Logare</span> Prof</div>", unsafe_allow_html=True)
    
    st.write("")
    materia = st.selectbox("Materia", ["Limba Română", "Matematică", "Engleză"])
    parola = st.text_input("Introdu Parola", type="password")
    
    st.write("<br>", unsafe_allow_html=True)
    
    if st.button("CONECTARE"):
        if parola == "123451":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Eroare de autentificare")
            
    if st.button("← Înapoi"):
        st.session_state.page = 'home'
        st.rerun()
