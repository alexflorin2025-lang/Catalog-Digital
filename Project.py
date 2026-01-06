import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina (Trebuie sa fie prima comanda Streamlit)
st.set_page_config(page_title="Catalog Digital", page_icon="🎓", layout="centered")

# 2. Stil Vizual (CSS) - Corectat pentru a evita erori
st.markdown("""
    <style>
    .main { background-color: #0f1115; }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3em; 
        background-color: #3b82f6; 
        color: white; 
        font-weight: bold;
    }
    .stExpander { 
        border: 1px solid #27272a; 
        border_radius: 15px; 
        background-color: #1a1d23; 
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
    st.subheader("Autentificare Sistem")
    
    tab1, tab2 = st.tabs(["Profesor", "Părinte"])
    
    with tab1:
        materia = st.selectbox("Materia", ["Informatică", "Matematică", "Română", "Engleză"])
        parola = st.text_input("Parolă Acces", type="password", key="p_prof")
        
        if st.button("CONECTARE PROFESOR"):
            if parola == "123451":
                st.session_state.logged_in = True
                st.session_state.role = "teacher"
                st.session_state.materia = materia
                st.rerun()
            else:
                st.error("Parolă incorectă!")
                
    with tab2:
        st.info("Accesul părinților se face pe baza numelui elevului.")
        nume_elev = st.text_input("Nume complet elev")
        if st.button("CONECTARE PĂRINTE"):
            st.session_state.logged_in = True
            st.session_state.role = "parent"
            st.session_state.nume_elev = nume_elev
            st.rerun()

else:
    # 6. Dashboard Principal
    st.sidebar.title("Meniu Catalog")
    st.sidebar.write(f"Utilizator: **{st.session_state.role.capitalize()}**")
    
    if st.sidebar.button("DECONECTARE"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "teacher":
        st.title(f"📚 Materia: {st.session_state.materia}")
        clasa_sel = st.selectbox("Selectează Clasa", list(CLASE.keys()))
        search = st.text_input("🔍 Caută elev...")

        elevi_filtrati = [e for e in CLASE[clasa_sel] if search.lower() in e.lower()]

        for elev in elevi_filtrati:
            with st.expander(f"👤 {elev}"):
                col1, col2 = st.columns(2)
                with col1:
                    nota = st.number_input(f"Nota", 1, 10, 10, key=f"n_{elev}")
                    if st.button(f"Salvează Nota", key=f"btn_n_{elev}"):
                        dt = datetime.now().strftime("%d-%m-%Y")
                        conn.execute("INSERT INTO grades VALUES (?,?,?,?,?)", 
                                     (dt, clasa_sel, elev, st.session_state.materia, nota))
                        conn.commit()
                        st.success(f"Nota {nota} adăugată!")
                with col2:
                    if st.button(f"Marchează Absent", key=f"abs_{elev}"):
                        dt = datetime.now().strftime("%d-%m-%Y")
                        conn.execute("INSERT INTO absences VALUES (?,?,?)", (dt, clasa_sel, elev))
                        conn.commit()
                        st.warning("Absență înregistrată!")
                        
        st.divider()
        st.subheader("📋 Ultimile note adăugate")
        query = "SELECT dt as Data, name as Elev, sub as Materia, val as Nota FROM grades ORDER BY rowid DESC LIMIT 5"
        df = pd.read_sql_query(query, conn)
        st.dataframe(df, use_container_width=True)

    else:
        st.title(f"👋 Salut, {st.session_state.nume_elev}")
        st.write("Iată situația ta școlară:")
        # Aici se pot adauga detalii specifice pentru parinti
