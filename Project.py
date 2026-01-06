import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(
    page_title="Catalog Digital", 
    page_icon="🎓", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS EXTREM pentru Full Screen pe Mobil
st.markdown("""
    <style>
    /* Ascunde absolut orice element Streamlit */
    header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    
    /* Elimina marginile si forțează conținutul sus de tot */
    .stApp {
        margin-top: -60px !important;
    }
    
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }

    /* Ajustare pentru ecranele de telefon */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
    }

    .main { background-color: #0e1117; }
    
    /* Butoane mari pentru degete (Nokia G21) */
    div.stButton > button { 
        width: 100%;
        border-radius: 12px; 
        height: 50px; 
        font-weight: bold; 
        background-color: #21262d; 
        color: #58a6ff; 
        border: 1px solid #30363d;
    }

    .absent-btn button { background-color: #da3633 !important; color: white !important; }
    .warning-btn button { background-color: #f1e05a !important; color: black !important; }
    .motiveaza-btn button { background-color: #238636 !important; color: white !important; height: 35px !important;}
    </style>
    """, unsafe_allow_html=True)

# 3. Restul logicii aplicatiei (Baza de date si functii)
def init_db():
    conn = sqlite3.connect('catalog_final_v7.db', check_same_thread=False)
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

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🎓 Catalog Digital</h1>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["🔒 PROF", "👑 DIR", "👤 PAR"])
    with t1:
        m_sel = st.selectbox("Materia", MATERII)
        p_p = st.text_input("Parolă", type="password", key="p_prof")
        if st.button("LOGARE PROFESOR"):
            if p_p == "123451":
                st.session_state.update({"logged_in": True, "role": "teacher", "materia": m_sel})
                st.rerun()
    with t2:
        p_dir = st.text_input("Parolă Director", type="password", key="p_dir")
        if st.button("LOGARE DIRECTOR"):
            if p_dir == "admin123":
                st.session_state.update({"logged_in": True, "role": "director"})
                st.rerun()
    with t3:
        n_p = st.selectbox("Nume Elev", CLASE["6B"])
        pw_p = st.text_input("Parolă Părinte", type="password", key="p_par")
        if st.button("LOGARE PĂRINTE"):
            if pw_p == f"{n_p}123":
                st.session_state.update({"logged_in": True, "role": "parent", "nume_elev": n_p})
                st.rerun()
else:
    # --- Interfața după logare ---
    st.markdown(f"<h3 style='color: #58a6ff;'>Catalog - {st.session_state.role.upper()}</h3>", unsafe_allow_html=True)
    
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
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("<div class='absent-btn'>", unsafe_allow_html=True)
                    if st.button("🔴 ABSENT", key=f"ab_{e}"):
                        conn.execute("INSERT INTO absences (dt, cl, name, sub) VALUES (?,?,?,?)", (d_sel, "6B", e, st.session_state.materia))
                        conn.commit()
                    st.markdown("</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown("<div class='warning-btn'>", unsafe_allow_html=True)
                    if st.button("⚠️ OBS.", key=f"warn_{e}"):
                        conn.execute("INSERT INTO warnings (dt, name, reason) VALUES (?,?,?)", (d_sel, e, "Comportament"))
                        conn.commit()
                    st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.role == "director":
        for e in CLASE["6B"]:
            with st.expander(f"👤 {e}"):
                st.write("Gestionare purtare și note...")

    if st.sidebar.button("🚪 IEȘIRE"):
        st.session_state.logged_in = False
        st.rerun()
