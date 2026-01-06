import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", page_icon="🎓", layout="centered")

# 2. CSS - Mirror Gradient, Butoane Negre & No Scroll
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { height: 100vh !important; overflow: hidden !important; background-color: #000; }
    .stApp { background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format"); background-size: cover; background-position: center; }
    header, footer, #MainMenu {visibility: hidden !important;}

    /* Card Gradient Oglindă */
    [data-testid="stVerticalBlock"] > div:has(div.stButton), .stExpander {
        background: linear-gradient(to bottom, rgba(60,85,120,0.4), rgba(5,15,30,0.98) 50%, rgba(60,85,120,0.4)) !important;
        backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 20px !important;
    }
    div.stButton > button { width: 100% !important; background-color: #000 !important; color: #fff !important; height: 42px !important; border-radius: 10px !important; border: 1px solid #333 !important; font-weight: 700 !important; }
    input, div[data-baseweb="select"] > div { background-color: rgba(0,0,0,0.8) !important; color: white !important; border: 1px solid #444 !important; }
    h1, h2, h3, label p, .stMarkdown { color: white !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initializare Baza de Date
def init_db():
    conn = sqlite3.connect('attendance_web.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS grades (dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)')
    c.execute('CREATE TABLE IF NOT EXISTS absences (dt TEXT, cl TEXT, name TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT)') # Tabel mesaje
    c.execute('CREATE TABLE IF NOT EXISTS conduct (name TEXT, val INT)') # Tabel purtare
    conn.commit()
    return conn

conn = init_db()

# 4. Date Elevi
CLASE = {
    "6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"],
    "7A": ["Ionescu Maria", "Popescu Dan"]
}

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1>🎓 Catalog Digital</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Profesor", "Părinte", "Directoare"])
    
    with tab1:
        materia = st.selectbox("Materia", ["Informatică", "Matematică", "Română"], key="m_p")
        p_prof = st.text_input("Parolă", type="password", key="pw_p")
        if st.button("LOGARE PROF"):
            if p_prof == "123451":
                st.session_state.update({"logged_in": True, "role": "teacher", "materia": materia})
                st.rerun()
    with tab2:
        nume_p = st.selectbox("Alege Elevul (Părinte)", CLASE["6B"] + CLASE["7A"], key="n_p")
        if st.button("LOGARE PĂRINTE"):
            st.session_state.update({"logged_in": True, "role": "parent", "nume_elev": nume_p})
            st.rerun()
    with tab3:
        p_dir = st.text_input("Cod Managerial", type="password", key="pw_d")
        if st.button("LOGARE DIRECTOARE"):
            if p_dir == "admin":
                st.session_state.update({"logged_in": True, "role": "admin"})
                st.rerun()

else:
    if st.sidebar.button("DECONECTARE"):
        st.session_state.logged_in = False
        st.rerun()

    # --- INTERFAȚA PROFESOR ---
    if st.session_state.role == "teacher":
        st.markdown(f"### 📚 {st.session_state.materia}")
        cl_sel = st.selectbox("Clasa", list(CLASE.keys()))
        for elev in CLASE[cl_sel]:
            with st.expander(f"👤 {elev}"):
                c1, c2, c3 = st.columns(3)
                with c1: 
                    nota = st.number_input("Notă", 1, 10, 10, key=f"n_{elev}")
                    if st.button("Pune Nota", key=f"bn_{elev}"):
                        conn.execute("INSERT INTO grades VALUES (?,?,?,?,?)", (datetime.now().strftime("%d-%m"), cl_sel, elev, st.session_state.materia, nota))
                        conn.commit()
                        st.toast("Notă salvată!")
                with c2:
                    if st.button("Absent", key=f"ba_{elev}"):
                        conn.execute("INSERT INTO absences VALUES (?,?,?)", (datetime.now().strftime("%d-%m"), cl_sel, elev))
                        conn.commit()
                        st.toast("Absență!")
                with c3:
                    if st.button("Mesaj/Mustrare", key=f"bm_{elev}"):
                        conn.execute("INSERT INTO messages VALUES (?,?)", (elev, "Observatie disciplina"))
                        conn.commit()
                        st.toast("Mesaj trimis!")

    # --- INTERFAȚA PĂRINTE ---
    elif st.session_state.role == "parent":
        st.markdown(f"### 👋 Situație: {st.session_state.nume_elev}")
        
        # Afișare Note
        st.write("**Notele tale:**")
        g = pd.read_sql(f"SELECT dt, sub, val FROM grades WHERE name='{st.session_state.nume_elev}'", conn)
        st.dataframe(g, use_container_width=True)
        
        # Afișare Absențe
        abs_count = len(pd.read_sql(f"SELECT * FROM absences WHERE name='{st.session_state.nume_elev}'", conn))
        st.warning(f"Total Absențe: {abs_count}")
        
        # Nota la Purtare
        purtare = pd.read_sql(f"SELECT val FROM conduct WHERE name='{st.session_state.nume_elev}'", conn)
        nota_p = purtare['val'].iloc[0] if not purtare.empty else 10
        st.info(f"Notă Purtare: {nota_p}")

    # --- INTERFAȚA DIRECTOARE ---
    elif st.session_state.role == "admin":
        st.markdown("### 🏛️ Panou Managerial")
        elev_sel = st.selectbox("Verifică Elev", CLASE["6B"] + CLASE["7A"])
        
        # Calcul Purtare Automată
        msgs = pd.read_sql(f"SELECT count(*) as total FROM messages WHERE name='{elev_sel}'", conn)['total'].iloc[0]
        nota_purtare = 10 - (msgs // 3) # La fiecare 3 mesaje scade 1 punct
        
        conn.execute("DELETE FROM conduct WHERE name=?", (elev_sel,))
        conn.execute("INSERT INTO conduct VALUES (?,?)", (elev_sel, nota_purtare))
        conn.commit()

        st.error(f"Mesaje de la profesori: {msgs}")
        st.success(f"Nota la purtare calculată: {nota_purtare}")
        
        if st.button("Vezi Raport Complet"):
            st.write(pd.read_sql(f"SELECT * FROM grades WHERE name='{elev_sel}'", conn))
