import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Configurare Pagina (Numele si Iconita care apar la instalare)
st.set_page_config(
    page_title="Catalog Digital", 
    page_icon="🎓", 
    layout="centered"
)

# 2. Interfață Vizuală (CSS) - Ascundem Streamlit si infrumusetam aplicatia
st.markdown("""
    <style>
    /* Ascunde elementele de branding Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main { background-color: #0e1117; }
    
    /* Design Carduri Elevi */
    div[data-testid="stExpander"] { 
        background-color: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 12px; 
        margin-bottom: 10px; 
    }
    
    /* Stil Butoane Note (Patrate) */
    div.stButton > button { 
        border-radius: 8px; 
        height: 45px; 
        font-weight: bold; 
        background-color: #21262d; 
        color: #58a6ff; 
        border: 1px solid #30363d; 
    }
    
    /* Culori Butoane Speciale */
    .absent-btn button { background-color: #da3633 !important; color: white !important; border: none !important; }
    .warning-btn button { background-color: #f1e05a !important; color: black !important; border: none !important; }
    .motiveaza-btn button { 
        background-color: #238636 !important; 
        color: white !important; 
        height: 35px !important; 
        font-size: 14px !important; 
        border: none !important;
    }
    .director-btn button { background-color: #8957e5 !important; color: white !important; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initializare Baza de Date
def init_db():
    conn = sqlite3.connect('catalog_v5.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS grades (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT, val INT)')
    c.execute('CREATE TABLE IF NOT EXISTS absences (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, cl TEXT, name TEXT, sub TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS warnings (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, name TEXT, reason TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS conduct (name TEXT PRIMARY KEY, score INT DEFAULT 10)')
    conn.commit()
    return conn

conn = init_db()

# 4. Date Materii si Clase
MATERII = ["Limba Română", "Matematică", "Engleză", "Franceză", "Istorie", "Geografie", "Biologie", "Fizică", "Chimie", "TIC", "Religie", "Ed. Plastică", "Ed. Muzicală", "Ed. Fizică", "Dirigenție"]
CLASE = {
    "6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"],
    "7A": ["Ionescu Maria", "Popescu Dan"]
}

# Functie automata pentru nota la purtare (la 3 observatii scade 1 punct)
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
    # Functie pentru detalii elev (vizibila pentru Profi si Director)
    def show_student_details(e):
        c_score = pd.read_sql_query(f"SELECT score FROM conduct WHERE name = '{e}'", conn)
        score = c_score['score'].iloc[0] if not c_score.empty else 10
        st.write(f"**Nota Purtare:** {score}")
        
        note_e = pd.read_sql_query(f"SELECT sub as Materia, val as Nota, dt as Data FROM grades WHERE name='{e}'", conn)
        if not note_e.empty:
            st.write("Note înregistrate:")
            st.dataframe(note_e, use_container_width=True, hide_index=True)
        
        st.write("**Absențe (Motivare):**")
        abs_e = pd.read_sql_query(f"SELECT id, dt, sub FROM absences WHERE name='{e}'", conn)
        if not abs_e.empty:
            for _, row in abs_e.iterrows():
                col_a, col_b = st.columns([2, 1])
                col_a.write(f"📅 {row['dt']} ({row['sub']})")
                st.markdown("<div class='motiveaza-btn'>", unsafe_allow_html=True)
                if col_b.button("Motivează", key=f"mot_{e}_{row['id']}"):
                    conn.execute("DELETE FROM absences WHERE id = ?", (row['id'],))
                    conn.commit()
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Nicio absență.")

    # 6. Interfață PROFESOR
    if st.session_state.role == "teacher":
        st.markdown("<h2 style='color: #58a6ff;'>Catalog Digital</h2>", unsafe_allow_html=True)
        st.subheader(f"Materia: {st.session_state.materia}")
        cl_sel = st.selectbox("Clasa", list(CLASE.keys()))
        for e in CLASE[cl_sel]:
            with st.expander(f"👤 {e.upper()}"):
                d_sel = st.date_input("Data", datetime.now(), key=f"d_{e}").strftime("%d-%m-%Y")
                
                # Grila Note 1-10
                cols = st.columns(5)
                for i in range(1, 11):
                    with cols[(i-1)%5]:
                        if st.button(str(i), key=f"n{i}_{e}"):
                            conn.execute("INSERT INTO grades (dt, cl, name, sub, val) VALUES (?,?,?,?,?)", (d_sel, cl_sel, e, st.session_state.materia, i))
                            conn.commit()
                            st.toast(f"Nota {i} salvată!")

                # Butoane Actiuni
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("<div class='absent-btn'>", unsafe_allow_width=True)
                    if st.button(f"🔴 ABSENT", key=f"ab_{e}", use_container_width=True):
                        conn.execute("INSERT INTO absences (dt, cl, name, sub) VALUES (?,?,?,?)", (d_sel, cl_sel, e, st.session_state.materia))
                        conn.commit()
                        st.toast("Absență adăugată")
                    st.markdown("</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown("<div class='warning-btn'>", unsafe_allow_html=True)
                    if st.button(f"⚠️ OBS.", key=f"warn_{e}", use_container_width=True):
                        conn.execute("INSERT INTO warnings (dt, name, reason) VALUES (?,?,?)", (d_sel, e, "Comportament"))
                        conn.commit()
                        update_conduct_auto(e)
                        st.toast("Observație adăugată")
                    st.markdown("</div>", unsafe_allow_html=True)
                with c3:
                    if st.button("🗑️ Nota", key=f"del_{e}", use_container_width=True):
                        conn.execute("DELETE FROM grades WHERE id = (SELECT MAX(id) FROM grades WHERE name = ?)", (e,))
                        conn.commit()
                        st.rerun()
                
                st.divider()
                show_student_details(e)

    # 7. Interfață DIRECTOR
    elif st.session_state.role == "director":
        st.markdown("<h2 style='color: #58a6ff;'>Catalog Digital - Director</h2>", unsafe_allow_html=True)
        cl_dir = st.selectbox("Clasa", list(CLASE.keys()))
        for e in CLASE[cl_dir]:
            with st.expander(f"👤 {e.upper()}"):
                show_student_details(e)
                st.markdown("<div class='director-btn'>", unsafe_allow_html=True)
                if st.button(f"📉 SCADE PURTAREA (-1p)", key=f"dec_{e}", use_container_width=True):
                    c_score = pd.read_sql_query(f"SELECT score FROM conduct WHERE name = '{e}'", conn)
                    score = c_score['score'].iloc[0] if not c_score.empty else 10
                    conn.execute("INSERT OR REPLACE INTO conduct (name, score) VALUES (?, ?)", (e, max(1, score - 1)))
                    conn.commit()
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    # 8. Interfață PĂRINTE
    else:
        st.markdown("<h2 style='color: #58a6ff;'>Catalog Digital</h2>", unsafe_allow_html=True)
        st.subheader(f"Elev: {st.session_state.nume_elev}")
        c_score = pd.read_sql_query(f"SELECT score FROM conduct WHERE name = '{st.session_state.nume_elev}'", conn)
        score = c_score['score'].iloc[0] if not c_score.empty else 10
        st.metric("Nota la Purtare", score)
        
        t1, t2, t3 = st.tabs(["📊 Note", "📍 Absențe", "⚠️ Observații"])
        with t1: st.table(pd.read_sql_query(f"SELECT dt as Data, sub as Materia, val as Nota FROM grades WHERE name='{st.session_state.nume_elev}'", conn))
        with t2: st.table(pd.read_sql_query(f"SELECT dt as Data, sub as Materia FROM absences WHERE name='{st.session_state.nume_elev}'", conn))
        with t3: st.table(pd.read_sql_query(f"SELECT dt as Data, reason as Motiv FROM warnings WHERE name='{st.session_state.nume_elev}'", conn))

    if st.sidebar.button("🚪 DECONECTARE"):
        st.session_state.logged_in = False
        st.rerun()
