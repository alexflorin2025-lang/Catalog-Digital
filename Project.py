import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", page_icon="🎓", layout="centered")

# 2. CSS - Ultra Dark & Mirror Gradient
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { height: 100vh !important; overflow: hidden !important; background-color: #000; }
    .stApp { background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format"); background-size: cover; background-position: center; }
    footer, #MainMenu {visibility: hidden !important;}

    /* Card Central */
    [data-testid="stVerticalBlock"] > div:has(div.stButton), .stExpander {
        background: linear-gradient(to bottom, rgba(60,85,120,0.4), rgba(5,15,30,0.98) 50%, rgba(60,85,120,0.4)) !important;
        backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 20px !important;
    }
    div.stButton > button { width: 100% !important; background-color: #000 !important; color: #fff !important; height: 42px !important; border-radius: 10px !important; border: 1px solid #333 !important; font-weight: 700 !important; }
    .stButton > button[kind="secondary"] { background-color: #1a0000 !important; color: #ff4b4b !important; border-color: #400 !important; }
    input, div[data-baseweb="select"] > div, textarea { background-color: rgba(0,0,0,0.8) !important; color: white !important; border: 1px solid #444 !important; }
    h1, h2, h3, label p { color: white !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initializare Baza de Date (Adăugăm coloană pentru mesaje și note)
def init_db():
    conn = sqlite3.connect('attendance_web.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS grades (dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)')
    c.execute('CREATE TABLE IF NOT EXISTS absences (dt TEXT, cl TEXT, name TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS messages (dt TEXT, name TEXT, sub TEXT, msg TEXT)') # Tabel mesaje detaliat
    c.execute('CREATE TABLE IF NOT EXISTS conduct (name TEXT, val INT)')
    conn.commit()
    return conn

conn = init_db()

CLASE = {
    "6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"],
    "7A": ["Ionescu Maria", "Popescu Dan"]
}

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- LOGICA NAVIGARE ---
if not st.session_state.logged_in:
    st.markdown("<h1>🎓 Catalog Digital</h1>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["Profesor", "Părinte", "Directoare"])
    
    with t1:
        m_sel = st.selectbox("Materia", ["Informatică", "Matematică", "Română"], key="m_p")
        p_p = st.text_input("Parolă", type="password", key="pw_p")
        if st.button("LOGARE PROF"):
            if p_p == "123":
                st.session_state.update({"logged_in": True, "role": "teacher", "materia": m_sel}); st.rerun()
    with t2:
        n_p = st.selectbox("Elev", CLASE["6B"] + CLASE["7A"], key="n_p")
        pw_p = st.text_input("Parolă Părinte", type="password", key="pw_par")
        if st.button("LOGARE PĂRINTE"):
            if pw_p == "1234":
                st.session_state.update({"logged_in": True, "role": "parent", "nume_elev": n_p}); st.rerun()
    with t3:
        pw_d = st.text_input("Cod Admin", type="password", key="pw_d")
        if st.button("LOGARE DIRECTOARE"):
            if pw_d == "admin":
                st.session_state.update({"logged_in": True, "role": "admin"}); st.rerun()

else:
    # --- INTERFAȚA PROFESOR ---
    if st.session_state.role == "teacher":
        st.markdown(f"### 📚 {st.session_state.materia}")
        cl_sel = st.selectbox("Clasa", list(CLASE.keys()))
        for elev in CLASE[cl_sel]:
            with st.expander(f"👤 {elev}"):
                c1, c2 = st.columns(2)
                with c1:
                    nota_v = st.number_input("Notă", 1, 10, 10, key=f"n_{elev}")
                    if st.button("Salvează Nota", key=f"bn_{elev}"):
                        conn.execute("INSERT INTO grades VALUES (?,?,?,?,?)", (datetime.now().strftime("%d-%m"), cl_sel, elev, st.session_state.materia, nota_v))
                        conn.commit(); st.toast("Notă adăugată!")
                with c2:
                    if st.button("Marchează Absent", key=f"ba_{elev}"):
                        conn.execute("INSERT INTO absences VALUES (?,?,?)", (datetime.now().strftime("%d-%m"), cl_sel, elev))
                        conn.commit(); st.toast("Absent!")
                
                # SECȚIUNE MUSTRARE CU TEXT
                st.markdown("---")
                motiv = st.text_area("Motivul mustrării", key=f"txt_{elev}", placeholder="Ex: Deranjarea orei...")
                if st.button("Trimite Mustrare", key=f"bm_{elev}"):
                    if motiv:
                        conn.execute("INSERT INTO messages VALUES (?,?,?,?)", (datetime.now().strftime("%d-%m"), elev, st.session_state.materia, motiv))
                        conn.commit(); st.toast("Mustrare trimisă!")
                    else: st.warning("Scrie motivul mai întâi!")

    # --- INTERFAȚA PĂRINTE ---
    elif st.session_state.role == "parent":
        st.markdown(f"### 👋 Salut, {st.session_state.nume_elev}")
        st.write("**Note:**")
        st.dataframe(pd.read_sql(f"SELECT dt as Data, sub as Materia, val as Nota FROM grades WHERE name='{st.session_state.nume_elev}'", conn), use_container_width=True)
        
        st.write("**Observații Profesori:**")
        m_df = pd.read_sql(f"SELECT dt as Data, sub as Materia, msg as Motiv FROM messages WHERE name='{st.session_state.nume_elev}'", conn)
        if not m_df.empty: st.error(m_df.to_html(index=False), unsafe_allow_html=True)
        else: st.success("Nicio observație.")

    # --- INTERFAȚA DIRECTOARE (SCĂDERE NOTE MANUALĂ) ---
    elif st.session_state.role == "admin":
        st.markdown("### 🏛️ Panou Control Directoare")
        e_s = st.selectbox("Alege Elevul", CLASE["6B"] + CLASE["7A"])
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Observații primite:**")
            msgs = pd.read_sql(f"SELECT dt, sub, msg FROM messages WHERE name='{e_s}'", conn)
            st.write(msgs)
        with col_b:
            purtare_act = pd.read_sql(f"SELECT val FROM conduct WHERE name='{e_s}'", conn)
            val_p = purtare_act['val'].iloc[0] if not purtare_act.empty else 10
            st.subheader(f"Purtare actuală: {val_p}")
            
            noua_nota = st.number_input("Modifică Nota la Purtare", 1, 10, int(val_p))
            if st.button("ACTUALIZEAZĂ NOTA"):
                conn.execute("DELETE FROM conduct WHERE name=?", (e_s,))
                conn.execute("INSERT INTO conduct VALUES (?,?)", (e_s, noua_nota))
                conn.commit(); st.success(f"Nota a fost setată la {noua_nota}!")

    if st.button("DECONECTARE", type="secondary"):
        st.session_state.logged_in = False; st.rerun()
