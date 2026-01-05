import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", page_icon="🎓", layout="centered")

# 2. Stil Vizual (CSS)
st.markdown("""
    <style>
    .main { background-color: #0f1115; }
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3em; 
        background-color: #3b82f6; color: white; font-weight: bold;
    }
    .stExpander { 
        border: 1px solid #27272a; border-radius: 15px; background-color: #1a1d23; 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Initializare Baza de Date
def init_db():
    conn = sqlite3.connect('attendance_web.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS grades 
                 (dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS absences 
                 (dt TEXT, cl TEXT, name TEXT)''')
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
    st.title("🎓 Catalog Digital")
    tab1, tab2 = st.tabs(["Profesor", "PĂRINTE"])
    
    with tab1:
        materia = st.selectbox("Materia", ["Informatică", "Matematică", "Română", "Engleză"])
        parola_p = st.text_input("Parolă Profesor", type="password", key="p_prof")
        if st.button("CONECTARE PROFESOR"):
            if parola_p == "123451":
                st.session_state.logged_in = True
                st.session_state.role = "teacher"
                st.session_state.materia = materia
                st.rerun()
            else:
                st.error("Parolă incorectă")
                
    with tab2:
        # Alegerea clasei pentru parinti
        clasa_parinte = st.selectbox("Clasa", list(CLASE.keys()), key="cl_par")
        # Alegerea numelui elevului din clasa selectata
        nume_e = st.selectbox("Nume elev", CLASE[clasa_parinte], key="n_par")
        parola_e = st.text_input("Parolă Părinte", type="password", key="p_par")
        
        if st.button("CONECTARE PĂRINTE"):
            # Parola ramane NumeElev123
            if parola_e == f"{nume_e}123":
                st.session_state.logged_in = True
                st.session_state.role = "parent"
                st.session_state.nume_elev = nume_e
                st.rerun()
            else:
                st.error("Acces refuzat")

else:
    # 6. Dashboard Principal
    st.sidebar.title("Meniu")
    if st.sidebar.button("DECONECTARE"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "teacher":
        st.title(f"📚 {st.session_state.materia}")
        clasa_sel = st.selectbox("Clasa", list(CLASE.keys()))
        search = st.text_input("Căutare")
        elevi_f = [e for e in CLASE[clasa_sel] if search.lower() in e.lower()]

        for elev in elevi_f:
            with st.expander(f"👤 {elev}"):
                c1, c2 = st.columns(2)
                with c1:
                    nota = st.number_input(f"Nota", 1, 10, 10, key=f"n_{elev}")
                    if st.button(f"Salvează", key=f"b_{elev}"):
                        dt = datetime.now().strftime("%d-%m-%Y")
                        conn.execute("INSERT INTO grades VALUES (?,?,?,?,?)", (dt, clasa_sel, elev, st.session_state.materia, nota))
                        conn.commit()
                        st.success("Salvat")
                with c2:
                    if st.button(f"Absent", key=f"a_{elev}"):
                        dt = datetime.now().strftime("%d-%m-%Y")
                        conn.execute("INSERT INTO absences VALUES (?,?,?)", (dt, clasa_sel, elev))
                        conn.commit()
                        st.warning("Înregistrat")

    else:
        st.title(f"Salut, {st.session_state.nume_elev}")
        df_note = pd.read_sql_query(f"SELECT dt as Data, sub as Materia, val as Nota FROM grades WHERE name = '{st.session_state.nume_elev}'", conn)
        if not df_note.empty:
            st.table(df_note)
        else:
            st.info("Fără date")