import streamlit as st

# 1. Configurare Pagina - Layout Centered (cel mai sigur pentru mobil)
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS PREMIUM - Fără chenare, doar elemente flotante
st.markdown("""
    <style>
    /* ASCUNDEM TOT CE E IN PLUS */
    header, footer, #MainMenu {visibility: hidden !important;}
    
    /* FUNDAL NEGRU PUR (AMOLED) */
    .stApp {
        background-color: #000000 !important;
    }

    /* ELIMINĂM ORICE CHENAR SAU BACKGROUND LA CONTAINER */
    .main .block-container {
        background-color: transparent !important; /* Fara fundal la cutie */
        border: none !important; /* Fara bordura */
        box_shadow: none !important; /* Fara umbra */
        padding-top: 60px !important;
        max-width: 550px !important;
    }

    /* TITLU STIL "NOUL CATALOG" */
    .logo-text {
        text-align: center;
        color: #fff;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }
    
    .accent-blue {
        color: #2E9AFE; /* Albastru specific aplicatiilor scolare moderne */
    }
    
    .subtitlu {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 50px;
        font-weight: 400;
    }

    /* BUTOANE "GHOST" PREMIUM */
    /* Fara fundal, doar contur fin care se aprinde */
    div.stButton > button {
        width: 100% !important;
        height: 75px !important;
        background-color: #111 !important; /* Foarte inchis, aproape negru */
        color: white !important;
        border: 1px solid #333 !important; /* Contur subtil */
        border-radius: 12px !important; /* Rotunjire medie ca la Apple */
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        margin-bottom: 20px !important;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify_content: center;
    }
    
    /* Efect Hover - Se face albastru */
    div.stButton > button:hover {
        border-color: #2E9AFE !important;
        color: #2E9AFE !important;
        background-color: #000 !important;
        transform: scale(1.02);
    }

    /* INPUT-URI CURATE */
    input {
        background-color: #111 !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        height: 55px !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #111 !important;
        border-color: #333 !important;
        color: white !important;
        border-radius: 10px !important;
    }
    
    label { color: #888 !important; font-size: 0.9rem !important; }

    /* Linie decorativa subtila */
    .separator {
        height: 1px;
        background: linear-gradient(90deg, transparent, #333, transparent);
        margin: 40px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica Aplicatiei
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- ECRAN START (Stil Noul Catalog) ---
if st.session_state.page == 'home':
    # Titlu cu accent albastru
    st.markdown("<div class='logo-text'>Catalog <span class='accent-blue'>Digital</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitlu'>Platformă de management școlar</div>", unsafe_allow_html=True)
    
    st.write("") # Spatiu
    
    # Butoane curate
    if st.button("👨‍🏫  Profesor"):
        st.session_state.page = 'login_profesor'
        st.rerun()

    if st.button("👨‍👩‍👧  Părinte / Elev"):
        st.session_state.page = 'login_parinte'
        st.rerun()

    if st.button("🔒  Director"):
        st.session_state.page = 'login_Director'
        st.rerun()
        
    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#444; font-size:0.8rem;'>v2.0 Secure System</p>", unsafe_allow_html=True)

# --- LOGIN PROFESOR (Minimalist) ---
elif st.session_state.page == 'login_profesor':
    st.markdown("<div class='logo-text'>Autentificare</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitlu'>Acces cadru didactic</div>", unsafe_allow_html=True)
    
    st.write("")
    materia = st.selectbox("Disciplină", ["Limba Română", "Matematică", "Engleză", "Istorie"])
    
    st.write("")
    parola = st.text_input("Parolă", type="password")
    
    st.write("<br>", unsafe_allow_html=True)
    
    # Butonul de conectare il facem putin diferit (plin) prin CSS inline (hack) sau il lasam standard
    if st.button("Acces în Catalog"):
        if parola == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia, "page": "main"})
            st.rerun()
        else:
            st.error("Date incorecte")
            
    if st.button("← Anulează"):
        st.session_state.page = 'home'
        st.rerun()

# --- CONTINUT DUPA LOGIN ---
elif st.session_state.get('logged_in'):
    st.markdown(f"<div class='logo-text'>{st.session_state.materia}</div>", unsafe_allow_html=True)
    st.success("Bine ai venit!")
    if st.button("Ieșire"):
        st.session_state.clear()
        st.rerun()

