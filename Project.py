import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(
    page_title="Catalog Digital", 
    page_icon="🎓", 
    layout="centered"
)

# 2. CSS REPARAT - Rezolvă problema din screenshot
st.markdown("""
    <style>
    /* Sterge elementele inutile Streamlit */
    header, footer, #MainMenu, [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Fundalul principal */
    .stApp {
        background-color: #0e1117;
    }

    /* Fix pentru centrarea si spatiul de sus */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }

    /* Stil pentru titlu sa nu mai fie taiat */
    .titlu-principal {
        text-align: center;
        color: #58a6ff;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px #000000;
    }

    /* Cardurile pentru elevi */
    div[data-testid="stExpander"] { 
        background-color: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 12px; 
    }

    /* Butoane mari si vizibile */
    div.stButton > button { 
        width: 100%;
        border-radius: 10px; 
        height: 50px; 
        font-weight: bold; 
        background-color: #21262d; 
        color: #58a6ff; 
        border: 1px solid #30363d;
        transition: 0.3s;
    }
    
    div.stButton > button:active {
        background-color: #58a6ff !important;
        color: white !important;
    }

    /* Culori specifice */
    .absent-btn button { background-color: #da3633 !important; color: white !important; }
    .warning-btn button { background-color: #f1e05a !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza de date
def init_db():
    conn = sqlite3.connect('catalog_v8.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS grades (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)')
    c.execute('CREATE TABLE IF NOT EXISTS absences (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS warnings (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, name TEXT, reason TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS conduct (name TEXT PRIMARY KEY, score INT DEFAULT 10)')
    conn.commit()
    return conn

conn = init_db()

# 4. Logica de Login
MATERII = ["Limba Română", "Matematică", "Engleză", "Franceză", "Istorie", "Geografie", "Biologie", "Fizică", "Chimie", "TIC", "Religie", "Ed. Plastică", "Ed. Muzicală", "Ed. Fizică", "Dirigenție"]
CLASE = {"6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"]}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<div class='titlu-principal'>🎓 Catalog Digital</div>", unsafe_allow_html=True)
    
    # Selectie rol mai clara pentru mobil
    rol = st.radio("Cine ești?", ["🔒 PROFESOR", "👑 DIRECTOR", "👤 PĂRINTE"], horizontal=True)
    
    st.divider()

    if "PROFESOR" in rol:
        m_sel = st.selectbox("Materia", MATERII)
        p_p = st.text_input("Parolă", type="password")
        if st.button("INTRARE ÎN CATALOG"):
            if p_p == "123451":
                st.session_state.update({"logged_in": True, "role": "teacher", "materia": m_sel})
                st.rerun()
    elif "DIRECTOR" in rol:
        p_dir = st.text_input("Parolă Director", type="password")
        if st.button("ACCES PANOU CONTROL"):
            if p_dir == "admin123":
                st.session_state.update({"logged_in": True, "role": "director"})
                st.rerun()
    else:
        n_p = st.selectbox("Nume Elev", CLASE["6B"])
        pw_p = st.text_input("Parolă Părinte (Nume123)", type="password")
        if st.button("VEZI NOTELE"):
            if pw_p == f"{n_p}123":
                st.session_state.update({"logged_in": True, "role": "parent", "nume_elev": n_p})
                st.rerun()

else:
    # --- Meniu interior după logare ---
    st.markdown(f"<h2 style='color: #58a6ff;'>{st.session_state.role.upper()}</h2>", unsafe_allow_html=True)
    
    if st.session_state.role == "teacher":
        st.info(f"Materia: {st.session_state.materia}")
        for e in CLASE["6B"]:
            with st.expander(f"👤 {e.upper()}"):
                d_sel = st.date_input("Data", datetime.now(), key=f"d_{e}").strftime("%d-%m-%Y")
                
                # Note 1-10
                cols = st.columns(5)
                for i in range(1, 11):
                    with cols[(i-1)%5]:
                        if st.button(str(i), key=f"n{i}_{e}"):
                            conn.execute("INSERT INTO grades (dt, cl, name, sub, val) VALUES (?,?,?,?,?)", (d_sel, "6B", e, st.session_state.materia, i))
                            conn.commit()
                            st.toast(f"Nota {i} salvată!")

                st.markdown("<br>", unsafe_allow_html=True)
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

    if st.sidebar.button("🚪 DECONECTARE"):
        st.session_state.logged_in = False
        st.rerun()
