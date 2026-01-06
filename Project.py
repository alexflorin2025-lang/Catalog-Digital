import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", page_icon="🎓", layout="centered")

# 2. Stil Vizual - Ultra Dark, Mirror Gradient & No Scroll
st.markdown("""
    <style>
    /* Fundalul paginii cu imaginea de clasă */
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

    /* Cardul Central cu Gradient Oglindă (Albastru Dark la mijloc) */
    [data-testid="stVerticalBlock"] > div:has(div.stButton), .stExpander {
        background: linear-gradient(to bottom, rgba(60,85,120,0.4), rgba(5,15,30,0.98) 50%, rgba(60,85,120,0.4)) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 20px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }

    /* Butoane Negre */
    div.stButton > button {
        width: 100% !important;
        background-color: #000 !important;
        color: #fff !important;
        height: 42px !important;
        border-radius: 10px !important;
        border: 1px solid #333 !important;
        font-weight: 700 !important;
    }
    
    /* Input-uri Ultra Dark */
    input, div[data-baseweb="select"] > div, .stNumberInput input {
        background-color: rgba(0,0,0,0.8) !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    
    h1, h2, h3, label p { color: white !important; text-align: center; }
    .stExpander { margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initializare Baza de Date
def init_db():
    conn = sqlite3.connect('attendance_web.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS grades (dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS absences (dt TEXT, cl TEXT, name TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# 4. Date Elevi
CLASE = {
    "6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"],
    "7A": ["Ionescu Maria", "Popescu Dan"]
}

# 5. Logica de Autentificare
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🎓 Catalog Digital</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Profesor", "Părinte"])
    
    with tab1:
        materia = st.selectbox("Materia", ["Informatică", "Matematică", "Română"], key="sel_m")
        parola = st.text_input("Parolă", type="password", key="p_prof")
        if st.button("CONECTARE"):
            if parola == "123451":
                st.session_state.logged_in = True
                st.session_state.role = "teacher"
                st.session_state.materia = materia
                st.rerun()
            else: st.error("Parolă incorectă!")
                
    with tab2:
        nume_elev = st.text_input("Nume complet elev", key="p_name")
        if st.button("INTRARE PĂRINTE"):
            st.session_state.logged_in = True
            st.session_state.role = "parent"
            st.session_state.nume_elev = nume_elev
            st.rerun()

else:
    # 6. Dashboard Principal (Interfață Profesor/Părinte)
    if st.sidebar.button("DECONECTARE"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "teacher":
        st.markdown(f"### 📚 {st.session_state.materia}", unsafe_allow_html=True)
        clasa_sel = st.selectbox("Clasa", list(CLASE.keys()), key="c_sel")
        search = st.text_input("🔍 Caută elev...", key="s_elev")

        elevi_filtrati = [e for e in CLASE[clasa_sel] if search.lower() in e.lower()]

        # Container cu scroll limitat pentru a nu strica layout-ul
        container_elevi = st.container()
        with container_elevi:
            for elev in elevi_filtrati:
                with st.expander(f"👤 {elev}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        nota = st.number_input(f"Nota", 1, 10, 10, key=f"n_{elev}")
                        if st.button(f"Pune Nota", key=f"btn_n_{elev}"):
                            dt = datetime.now().strftime("%d-%m-%Y")
                            conn.execute("INSERT INTO grades VALUES (?,?,?,?,?)", (dt, clasa_sel, elev, st.session_state.materia, nota))
                            conn.commit()
                            st.toast(f"Nota {nota} salvată!")
                    with col2:
                        if st.button(f"Absent", key=f"abs_{elev}"):
                            dt = datetime.now().strftime("%d-%m-%Y")
                            conn.execute("INSERT INTO absences VALUES (?,?,?)", (dt, clasa_sel, elev))
                            conn.commit()
                            st.toast("Absență salvată!")
    else:
        st.markdown(f"### 👋 Salut, {st.session_state.nume_elev}", unsafe_allow_html=True)
        st.write("Situația ta școlară va apărea aici.")
