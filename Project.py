import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", page_icon="🎓", layout="centered")

# 2. CSS pentru Butoane de Alegere Mari
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden !important;}
    .stApp {background-color: #0e1117;}
    .block-container {padding-top: 2rem !important;}

    /* Titlu */
    .titlu {
        text-align: center; color: #58a6ff; font-size: 2.5rem; font-weight: bold; margin-bottom: 2rem;
    }

    /* Stil Butoane Selectie Rol (Mari) */
    .stButton > button {
        width: 100%; height: 80px !important; font-size: 20px !important;
        border-radius: 15px !important; margin-bottom: 15px !important;
        transition: 0.3s; border: 1px solid #30363d !important;
    }
    
    /* Culori butoane de start */
    div[data-testid="column"]:nth-of-type(1) .stButton button { border-left: 8px solid #58a6ff !important; }
    div[data-testid="column"]:nth-of-type(2) .stButton button { border-left: 8px solid #8957e5 !important; }
    div[data-testid="column"]:nth-of-type(3) .stButton button { border-left: 8px solid #238636 !important; }

    /* Input-uri mai vizibile */
    input { background-color: #161b22 !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initializare Baza de Date
def init_db():
    conn = sqlite3.connect('catalog_v9.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS grades (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)')
    c.execute('CREATE TABLE IF NOT EXISTS absences (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS warnings (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, name TEXT, reason TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS conduct (name TEXT PRIMARY KEY, score INT DEFAULT 10)')
    conn.commit()
    return conn

conn = init_db()
MATERII = ["Limba Română", "Matematică", "Engleză", "Franceză", "Istorie", "Geografie", "Biologie", "Fizică", "Chimie", "TIC", "Religie", "Ed. Plastică", "Ed. Muzicală", "Ed. Fizică", "Dirigenție"]
CLASE = {"6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"]}

# 4. Logica de Navigare (Alegere Rol)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<div class='titlu'>🎓 Catalog Digital</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Alege modul de conectare:</p>", unsafe_allow_html=True)
    
    # 3 Butoane Mari
    if st.button("🔒 MOD PROFESOR"):
        st.session_state.page = 'login_prof'
        st.rerun()
    
    if st.button("👑 MOD DIRECTOR"):
        st.session_state.page = 'login_dir'
        st.rerun()
        
    if st.button("👤 MOD PĂRINTE"):
        st.session_state.page = 'login_parinte'
        st.rerun()

# --- PAGINA LOGIN PROFESOR ---
elif st.session_state.page == 'login_prof':
    st.markdown("### 🔒 Conectare Profesor")
    m_sel = st.selectbox("Alege Materia", MATERII)
    p_p = st.text_input("Parolă", type="password")
    c1, c2 = st.columns(2)
    if c1.button("ÎNAPOI"): st.session_state.page = 'home'; st.rerun()
    if c2.button("CONECTARE"):
        if p_p == "123451":
            st.session_state.update({"logged_in": True, "role": "teacher", "materia": m_sel, "page": "main"})
            st.rerun()

# --- PAGINA LOGIN DIRECTOR ---
elif st.session_state.page == 'login_dir':
    st.markdown("### 👑 Acces Director")
    p_dir = st.text_input("Parolă de Administrare", type="password")
    c1, c2 = st.columns(2)
    if c1.button("ÎNAPOI"): st.session_state.page = 'home'; st.rerun()
    if c2.button("CONECTARE"):
        if p_dir == "admin123":
            st.session_state.update({"logged_in": True, "role": "director", "page": "main"})
            st.rerun()

# --- PAGINA LOGIN PARINTE ---
elif st.session_state.page == 'login_parinte':
    st.markdown("### 👤 Vizualizare Părinte")
    n_p = st.selectbox("Numele Elevului", CLASE["6B"])
    pw_p = st.text_input("Parolă (Nume123)", type="password")
    c1, c2 = st.columns(2)
    if c1.button("ÎNAPOI"): st.session_state.page = 'home'; st.rerun()
    if c2.button("VEZI NOTE"):
        if pw_p == f"{n_p}123":
            st.session_state.update({"logged_in": True, "role": "parent", "nume_elev": n_p, "page": "main"})
            st.rerun()

# --- INTERFATA PRINCIPALA (Dupa Login) ---
if st.session_state.get('logged_in'):
    st.markdown(f"## {st.session_state.role.upper()}")
    if st.session_state.role == "teacher":
        st.write(f"Materia: **{st.session_state.materia}**")
        for e in CLASE["6B"]:
            with st.expander(f"👤 {e.upper()}"):
                d_sel = st.date_input("Data", datetime.now(), key=f"d_{e}").strftime("%d-%m-%Y")
                cols = st.columns(5)
                for i in range(1, 11):
                    with cols[(i-1)%5]:
                        if st.button(str(i), key=f"n{i}_{e}"):
                            conn.execute("INSERT INTO grades (dt, cl, name, sub, val) VALUES (?,?,?,?,?)", (d_sel, "6B", e, st.session_state.materia, i))
                            conn.commit()
                            st.toast("Salvat!")
    
    if st.sidebar.button("🚪 DECONECTARE"):
        st.session_state.clear()
        st.session_state.page = 'home'
        st.rerun()
