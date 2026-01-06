import streamlit as st

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", layout="centered")

# 2. CSS - Ultra Dark, Glassmorphism & Dark Buttons
st.markdown("""
    <style>
    /* Fundal cu Imagine de Clasă + Overlay Cinematic foarte închis */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                    url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    header, footer, #MainMenu {visibility: hidden !important;}

    /* Containerul central - Glassmorphism */
    .main .block-container {
        background: rgba(10, 10, 10, 0.6) !important;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 30px !important;
        padding: 60px 50px !important;
        max-width: 500px !important;
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.9) !important;
        margin-top: 5vh;
    }

    /* Titlu cu Glow */
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
        color: #666;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 40px;
    }

    /* BUTOANE NEGRE (DARK) --------->> */
    div.stButton > button {
        width: 100% !important;
        height: 60px !important;
        background: #050505 !important; /* Negru intens */
        color: #ffffff !important; /* Text Alb */
        border: 1px solid #1b263b !important; /* Contur discret */
        border-radius: 15px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin-top: 15px;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background: #111111 !important;
        border-color: #ffffff !important; /* Glow alb la contur pe hover */
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
    }

    /* Input-uri */
    input, div[data-baseweb="select"] > div {
        background-color: rgba(0, 0, 0, 0.8) !important;
        color: white !important;
        border: 1px solid #222 !important;
    }

    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(to right, transparent, #333, transparent);
        margin: 30px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logica Navigatie
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<div class='logo-text'>Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Alegeți metoda de autentificare</div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Butoanele acum sunt DARK
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
    st.markdown("<div class='logo-text'>Logare</div>", unsafe_allow_html=True)
    materia = st.selectbox("Materia", ["Matematică", "Română", "Fizică"])
    parola = st.text_input("Cheie Acces", type="password")
    
    if st.button("AUTENTIFICARE"):
        if parola == "123451":
            st.success("Bun venit!")
        else:
            st.error("Acces neautorizat.")
            
    if st.button("← ÎNAPOI"):
        st.session_state.page = 'home'
        st.rerun()
