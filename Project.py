import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", page_icon="🎓", layout="centered")

# 2. Stil Vizual pentru butoane mari (pătrate)
st.markdown("""
    <style>
    .main { background-color: #0f1115; }
    div.stButton > button {
        border-radius: 5px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    /* Stil pentru butoanele de note să arate ca niște pătrate */
    [data-testid="stHorizontalBlock"] .stButton button {
        background-color: #262730;
        color: white;
        border: 1px solid #4a4a4a;
    }
    .stExpander { 
        border: 1px solid #27272a; border-radius: 10px; background-color: #1a1d23; 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza de Date
def init_db():
    conn = sqlite3.connect('attendance_web.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS grades (dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)')
    c.execute('CREATE TABLE IF NOT EXISTS absences (dt TEXT, cl TEXT, name TEXT, sub TEXT)')
    conn.commit()
    return conn

conn = init_db()

# 4. Toate Materiile de Gimnaziu
MATERII = ["Limba Română", "Matematică", "Engleză", "Franceză", "Istorie", "Geografie", "Biologie", "Fizică", "Chimie", "Informatică", "Religie", "Ed. Plastică", "Ed. Muzicală", "Ed. Fizică", "Dirigenție"]

CLASE = {
    "6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"],
    "7A": ["Ionescu Maria", "Popescu Dan"]
}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🎓 Catalog Digital")
    t1, t2 = st.tabs(["PROFESOR", "PĂRINTE"])
    with t1:
        m_sel = st.selectbox("Materia", MATERII)
        p_p = st.text_input("Parolă", type="password")
        if st.button("CONECTARE"):
            if p_p == "123451":
                st.session_state.update({"logged_in": True, "role": "teacher", "materia": m_sel})
                st.rerun()
    with t2:
        c_p = st.selectbox("Clasa", list(CLASE.keys()), key="cp")
        n_p = st.selectbox("Elev", CLASE[c_p], key="np")
        pw_p = st.text_input("Parolă (Nume123)", type="password", key="pp")
        if st.button("ACCES PĂRINTE"):
            if pw_p == f"{n_p}123":
                st.session_state.update({"logged_in": True, "role": "parent", "nume_elev": n_p})
                st.rerun()
else:
    if st.session_state.role == "teacher":
        st.title(f"📚 {st.session_state.materia}")
        cl_sel = st.selectbox("Clasa", list(CLASE.keys()))
        elevi = [e for e in CLASE[cl_sel]]
        
        for e in elevi:
            with st.expander(f"👤 {e}"):
                # 1. Alegem Data (Fără săgeți)
                d_sel = st.date_input("Data notei/absenței", datetime.now(), key=f"d_{e}").strftime("%d-%m-%Y")
                
                # 2. Butoane Pătratice pentru Note (1-10)
                st.write("Apasă pe notă:")
                cols = st.columns(5) # Primul rând (1-5)
                for i in range(1, 6):
                    if cols[i-1].button(str(i), key=f"n{i}_{e}"):
                        conn.execute("INSERT INTO grades VALUES (?,?,?,?,?)", (d_sel, cl_sel, e, st.session_state.materia, i))
                        conn.commit()
                        st.success(f"Nota {i} salvată!")
                
                cols2 = st.columns(5) # Al doilea rând (6-10)
                for i in range(6, 11):
                    if cols2[i-6].button(str(i), key=f"n{i}_{e}"):
                        conn.execute("INSERT INTO grades VALUES (?,?,?,?,?)", (d_sel, cl_sel, e, st.session_state.materia, i))
                        conn.commit()
                        st.success(f"Nota {i} salvată!")
                
                st.divider()
                # 3. Buton Absență
                if st.button(f"🔴 Pune ABSENT", key=f"ab_{e}"):
                    conn.execute("INSERT INTO absences VALUES (?,?,?,?)", (d_sel, cl_sel, e, st.session_state.materia))
                    conn.commit()
                    st.warning("Absență salvată!")
    else:
        st.title(f"Salut, {st.session_state.nume_elev}")
        note = pd.read_sql_query(f"SELECT dt as Data, sub as Materia, val as Nota FROM grades WHERE name = '{st.session_state.nume_elev}'", conn)
        absente = pd.read_sql_query(f"SELECT dt as Data, sub as Materia FROM absences WHERE name = '{st.session_state.nume_elev}'", conn)
        st.subheader("Notele tale")
        st.table(note)
        st.subheader("Absențele tale")
        st.table(absente)

    if st.sidebar.button("DECONECTARE"):
        st.session_state.logged_in = False
        st.rerun()
