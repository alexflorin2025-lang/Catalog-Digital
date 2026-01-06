import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital Pro", page_icon="🎓", layout="centered")

# 2. Interfață Vizuală (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stExpander"] { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; margin-bottom: 10px; }
    div.stButton > button { border-radius: 8px; height: 45px; font-weight: bold; background-color: #21262d; color: #58a6ff; border: 1px solid #30363d; }
    .absent-btn button { background-color: #da3633 !important; color: white !important; }
    .warning-btn button { background-color: #f1e05a !important; color: black !important; }
    .director-btn button { background-color: #8957e5 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza de Date
def init_db():
    conn = sqlite3.connect('catalog_final.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS grades (dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)')
    c.execute('CREATE TABLE IF NOT EXISTS absences (dt TEXT, cl TEXT, name TEXT, sub TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS warnings (dt TEXT, name TEXT, reason TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS conduct (name TEXT, score INT DEFAULT 10)')
    conn.commit()
    return conn

conn = init_db()

# 4. Configurare
MATERII = ["Limba Română", "Matematică", "Engleză", "Istorie", "Geografie", "Biologie", "Fizică", "Chimie", "TIC", "Ed. Fizică", "Dirigenție"]
CLASE = {
    "6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"],
    "7A": ["Ionescu Maria", "Popescu Dan"]
}

# Funcție pentru verificare purtare (3 observații = -1 punct)
def update_conduct_auto(nume):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM warnings WHERE name = ?", (nume,))
    count = c.fetchone()[0]
    if count > 0 and count % 3 == 0:
        c.execute("SELECT score FROM conduct WHERE name = ?", (nume,))
        res = c.fetchone()
        current_score = res[0] if res else 10
        new_score = max(1, current_score - 1)
        c.execute("INSERT OR REPLACE INTO conduct (name, score) VALUES (?, ?)", (nume, new_score))
        conn.commit()
        return True
    return False

# 5. Logica Autentificare
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🎓 Catalog Digital</h1>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["🔒 PROFESOR", "👑 DIRECTOR", "👤 PĂRINTE"])
    
    with t1:
        m_sel = st.selectbox("Materia", MATERII)
        p_p = st.text_input("Parolă Profesor", type="password", key="p_prof")
        if st.button("CONECTARE PROFESOR"):
            if p_p == "123451":
                st.session_state.update({"logged_in": True, "role": "teacher", "materia": m_sel})
                st.rerun()
    
    with t2:
        p_dir = st.text_input("Parolă Director", type="password", key="p_dir")
        if st.button("CONECTARE DIRECTOR"):
            if p_dir == "admin123":
                st.session_state.update({"logged_in": True, "role": "director"})
                st.rerun()
                
    with t3:
        c_p = st.selectbox("Clasa", list(CLASE.keys()))
        n_p = st.selectbox("Nume Elev", CLASE[c_p])
        pw_p = st.text_input("Parolă Acces", type="password", key="p_par")
        if st.button("CONECTARE PĂRINTE"):
            if pw_p == f"{n_p}123":
                st.session_state.update({"logged_in": True, "role": "parent", "nume_elev": n_p})
                st.rerun()

else:
    # 6. Interfață PROFESOR
    if st.session_state.role == "teacher":
        st.title(f"📚 {st.session_state.materia}")
        cl_sel = st.selectbox("Clasa", list(CLASE.keys()))
        for e in CLASE[cl_sel]:
            with st.expander(f"👤 {e}"):
                d_sel = st.date_input("Data", datetime.now(), key=f"d_{e}").strftime("%d-%m-%Y")
                cols = st.columns(5)
                for i in range(1, 11):
                    with cols[(i-1)%5]:
                        if st.button(str(i), key=f"n{i}_{e}"):
                            conn.execute("INSERT INTO grades VALUES (?,?,?,?,?)", (d_sel, cl_sel, e, st.session_state.materia, i))
                            conn.commit()
                            st.toast(f"Nota {i} salvată!")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("<div class='absent-btn'>", unsafe_allow_html=True)
                    if st.button(f"🔴 ABSENT", key=f"ab_{e}", use_container_width=True):
                        conn.execute("INSERT INTO absences VALUES (?,?,?,?)", (d_sel, cl_sel, e, st.session_state.materia))
                        conn.commit()
                    st.markdown("</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown("<div class='warning-btn'>", unsafe_allow_html=True)
                    if st.button(f"⚠️ OBSERVAȚIE", key=f"warn_{e}", use_container_width=True):
                        conn.execute("INSERT INTO warnings VALUES (?,?,?)", (d_sel, e, "Comportament neadecvat"))
                        conn.commit()
                        if update_conduct_auto(e):
                            st.error("Scădere automată a notei la purtare (3 observații)!")
                        else:
                            st.warning("Observație adăugată!")
                    st.markdown("</div>", unsafe_allow_html=True)

    # 7. Interfață DIRECTOR
    elif st.session_state.role == "director":
        st.title("👑 Panou Director")
        cl_dir = st.selectbox("Alege Clasa", list(CLASE.keys()))
        for e in CLASE[cl_dir]:
            c_score = pd.read_sql_query(f"SELECT score FROM conduct WHERE name = '{e}'", conn)
            score = c_score['score'].iloc[0] if not c_score.empty else 10
            
            with st.expander(f"Elev: {e} | Notă Purtare: {score}"):
                st.markdown("<div class='director-btn'>", unsafe_allow_html=True)
                if st.button(f"📉 SCADE PURTAREA LUI {e}", key=f"dec_{e}", use_container_width=True):
                    new_s = max(1, score - 1)
                    conn.execute("INSERT OR REPLACE INTO conduct (name, score) VALUES (?, ?)", (e, new_s))
                    conn.commit()
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    # 8. Interfață PĂRINTE
    else:
        st.title(f"📱 Elev: {st.session_state.nume_elev}")
        c_score = pd.read_sql_query(f"SELECT score FROM conduct WHERE name = '{st.session_state.nume_elev}'", conn)
        score = c_score['score'].iloc[0] if not c_score.empty else 10
        st.metric("Nota la Purtare", score)
        
        tab1, tab2, tab3 = st.tabs(["📊 Note", "📍 Absențe", "⚠️ Observații"])
        with tab1:
            st.table(pd.read_sql_query(f"SELECT dt, sub, val FROM grades WHERE name='{st.session_state.nume_elev}'", conn))
        with tab2:
            st.table(pd.read_sql_query(f"SELECT dt, sub FROM absences WHERE name='{st.session_state.nume_elev}'", conn))
        with tab3:
            st.table(pd.read_sql_query(f"SELECT dt, reason FROM warnings WHERE name='{st.session_state.nume_elev}'", conn))

    if st.sidebar.button("🚪 DECONECTARE"):
        st.session_state.logged_in = False
        st.rerun()
