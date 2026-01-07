import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import hashlib

# 1. Configurare Pagina
st.set_page_config(
    page_title="Catalog Digital", 
    page_icon="🎓", 
    layout="wide",  # Schimbat la wide pentru mai mult spațiu
    initial_sidebar_state="collapsed"
)

# 2. CSS - Ultra Dark & Mirror Gradient
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #000 !important;
        height: 100vh !important;
    }
    .stApp { 
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format") !important; 
        background-size: cover !important; 
        background-position: center !important;
        background-attachment: fixed !important;
        min-height: 100vh !important;
    }
    footer, #MainMenu {visibility: hidden !important;}
    
    /* Header fix */
    .st-emotion-cache-10trblm {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    
    /* Scroll personalizat */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.3);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(60,85,120,0.8);
        border-radius: 4px;
    }
    
    /* Expander compact */
    .stExpander {
        margin-bottom: 5px !important;
    }
    .streamlit-expanderHeader {
        padding: 0.5rem 1rem !important;
        font-size: 0.9rem !important;
    }
    
    /* Butoane mai mici */
    div.stButton > button { 
        height: 36px !important; 
        font-size: 0.85rem !important;
        margin: 2px 0 !important;
    }
    
    /* Inputuri mai mici */
    .stNumberInput input, .stTextArea textarea {
        padding: 0.25rem 0.5rem !important;
        font-size: 0.9rem !important;
    }
    
    /* Layout compact */
    [data-testid="stExpander"] div[role="button"] p {
        font-size: 0.9rem !important;
    }
    
    /* Deconectare sus dreapta */
    .deconectare-btn {
        position: absolute !important;
        top: 10px !important;
        right: 10px !important;
        z-index: 1000 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# 3. Parole hash
PASSWORDS = {
    "teacher": hashlib.sha256("123".encode()).hexdigest(),
    "parent": hashlib.sha256("1234".encode()).hexdigest(),
    "admin": hashlib.sha256("admin".encode()).hexdigest()
}

# 4. Initializare Baza de Date
def init_db():
    conn = sqlite3.connect('attendance_web.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dt TEXT, 
        cl TEXT, 
        name TEXT, 
        sub TEXT, 
        val INT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS absences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dt TEXT, 
        cl TEXT, 
        name TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        dt TEXT, 
        name TEXT, 
        sub TEXT, 
        msg TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS conduct (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE, 
        val INT DEFAULT 10
    )''')
    
    conn.commit()
    return conn

# 5. Funcții utilitare
def verify_password(password, role):
    return hashlib.sha256(password.encode()).hexdigest() == PASSWORDS[role]

def get_conduct_value(name, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT val FROM conduct WHERE name = ?", (name,))
    result = cursor.fetchone()
    return result[0] if result else 10

def setup_initial_conduct(conn, classes):
    cursor = conn.cursor()
    for class_name, students in classes.items():
        for student in students:
            cursor.execute("INSERT OR IGNORE INTO conduct (name, val) VALUES (?, ?)", (student, 10))
    conn.commit()

# 6. Conexiune BD și setup
conn = init_db()

CLASE = {
    "6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"],
    "7A": ["Ionescu Maria", "Popescu Dan"]
}

setup_initial_conduct(conn, CLASE)

# 7. State sesiune
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.materia = None
    st.session_state.nume_elev = None

# --- LOGICA NAVIGARE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='margin-top: 10px;'>🎓 Catalog Digital</h1>", unsafe_allow_html=True)
    
    t1, t2, t3 = st.tabs(["👨‍🏫 Profesor", "👪 Părinte", "🏛️ Directoare"])
    
    with t1:
        st.subheader("Autentificare Profesor")
        m_sel = st.selectbox("Materia", ["Informatică", "Matematică", "Română"], key="m_p")
        p_p = st.text_input("Parolă", type="password", key="pw_p")
        if st.button("LOGARE PROFESOR", key="btn_prof", use_container_width=True):
            if verify_password(p_p, "teacher"):
                st.session_state.update({
                    "logged_in": True, 
                    "role": "teacher", 
                    "materia": m_sel
                })
                st.rerun()
            else:
                st.error("Parolă incorectă!")
    
    with t2:
        st.subheader("Autentificare Părinte")
        all_students = []
        for students in CLASE.values():
            all_students.extend(students)
        
        n_p = st.selectbox("Elev", sorted(all_students), key="n_p")
        pw_p = st.text_input("Parolă Părinte", type="password", key="pw_par")
        if st.button("LOGARE PĂRINTE", key="btn_parinte", use_container_width=True):
            if verify_password(pw_p, "parent"):
                st.session_state.update({
                    "logged_in": True, 
                    "role": "parent", 
                    "nume_elev": n_p
                })
                st.rerun()
            else:
                st.error("Parolă incorectă!")
    
    with t3:
        st.subheader("Autentificare Directoare")
        pw_d = st.text_input("Cod Admin", type="password", key="pw_d")
        if st.button("LOGARE DIRECTOARE", key="btn_direct", use_container_width=True):
            if verify_password(pw_d, "admin"):
                st.session_state.update({
                    "logged_in": True, 
                    "role": "admin"
                })
                st.rerun()
            else:
                st.error("Cod incorect!")

else:
    # --- HEADER COMPACT cu DECONECTARE ---
    col_title, col_space, col_logout = st.columns([3, 1, 1])
    
    with col_title:
        if st.session_state.role == "teacher":
            st.markdown(f"### 📚 {st.session_state.materia}")
        elif st.session_state.role == "parent":
            st.markdown(f"### 👋 {st.session_state.nume_elev}")
        else:
            st.markdown("### 🏛️ Panou Directoare")
    
    with col_logout:
        st.write("")  # Spacing
        if st.button("🚪 DECONECTARE", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown("---")
    
    # --- INTERFAȚA PROFESOR (OPTIMIZATĂ) ---
    if st.session_state.role == "teacher":
        cl_sel = st.selectbox("Selectează Clasa", list(CLASE.keys()), 
                             key="prof_class_selector", label_visibility="collapsed")
        
        # HEADER COMPACT cu statistici
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            total_note = pd.read_sql(f"""
                SELECT COUNT(*) as count FROM grades 
                WHERE cl = '{cl_sel}' AND sub = '{st.session_state.materia}'
            """, conn)['count'].iloc[0]
            st.metric("Note total", total_note, delta=None)
        
        with col_stats2:
            total_abs = pd.read_sql(f"""
                SELECT COUNT(*) as count FROM absences 
                WHERE cl = '{cl_sel}' AND dt = date('now')
            """, conn)['count'].iloc[0]
            st.metric("Absențe azi", total_abs)
        
        with col_stats3:
            total_obs = pd.read_sql(f"""
                SELECT COUNT(*) as count FROM messages 
                WHERE name IN ({','.join(['?' for _ in CLASE[cl_sel]])})
            """, conn, params=CLASE[cl_sel])['count'].iloc[0]
            st.metric("Observații", total_obs)
        
        st.markdown("---")
        
        # INTERFAȚĂ DUBLUĂ COLUMN pentru mai puțin scrolling
        col_left, col_right = st.columns(2)
        
        # Impartim elevii in două coloane
        students_left = CLASE[cl_sel][:len(CLASE[cl_sel])//2]
        students_right = CLASE[cl_sel][len(CLASE[cl_sel])//2:]
        
        with col_left:
            st.markdown(f"**Elevi (1-{len(students_left)})**")
            for elev in students_left:
                with st.expander(f"👤 {elev}", expanded=False):
                    # Input compact
                    nota_v = st.number_input("Notă", 1, 10, 10, 
                                           key=f"n_{cl_sel}_{elev}")
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("➕ Nota", key=f"bn_{cl_sel}_{elev}", use_container_width=True):
                            conn.execute("INSERT INTO grades (dt, cl, name, sub, val) VALUES (?,?,?,?,?)", 
                                       (datetime.now().strftime("%d-%m-%Y"), 
                                        cl_sel, elev, st.session_state.materia, nota_v))
                            conn.commit()
                            st.success(f"Nota {nota_v} adăugată!")
                            st.rerun()
                    
                    with col_btn2:
                        if st.button("❌ Absent", key=f"ba_{cl_sel}_{elev}", use_container_width=True):
                            conn.execute("INSERT INTO absences (dt, cl, name) VALUES (?,?,?)", 
                                       (datetime.now().strftime("%d-%m-%Y"), cl_sel, elev))
                            conn.commit()
                            st.warning(f"{elev} absent!")
                            st.rerun()
                    
                    motiv = st.text_area("Observație", 
                                       key=f"txt_{cl_sel}_{elev}", 
                                       placeholder="Scrie observație...",
                                       height=60)
                    
                    if st.button("📨 Trimite", key=f"bm_{cl_sel}_{elev}", use_container_width=True):
                        if motiv.strip():
                            conn.execute("INSERT INTO messages (dt, name, sub, msg) VALUES (?,?,?,?)", 
                                       (datetime.now().strftime("%d-%m-%Y"), 
                                        elev, st.session_state.materia, motiv.strip()))
                            conn.commit()
                            st.info("Observație trimisă!")
                            st.rerun()
        
        with col_right:
            st.markdown(f"**Elevi ({len(students_left)+1}-{len(CLASE[cl_sel])})**")
            for elev in students_right:
                with st.expander(f"👤 {elev}", expanded=False):
                    nota_v = st.number_input("Notă", 1, 10, 10, 
                                           key=f"n_r_{cl_sel}_{elev}")
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("➕ Nota", key=f"bn_r_{cl_sel}_{elev}", use_container_width=True):
                            conn.execute("INSERT INTO grades (dt, cl, name, sub, val) VALUES (?,?,?,?,?)", 
                                       (datetime.now().strftime("%d-%m-%Y"), 
                                        cl_sel, elev, st.session_state.materia, nota_v))
                            conn.commit()
                            st.success(f"Nota {nota_v} adăugată!")
                            st.rerun()
                    
                    with col_btn2:
                        if st.button("❌ Absent", key=f"ba_r_{cl_sel}_{elev}", use_container_width=True):
                            conn.execute("INSERT INTO absences (dt, cl, name) VALUES (?,?,?)", 
                                       (datetime.now().strftime("%d-%m-%Y"), cl_sel, elev))
                            conn.commit()
                            st.warning(f"{elev} absent!")
                            st.rerun()
                    
                    motiv = st.text_area("Observație", 
                                       key=f"txt_r_{cl_sel}_{elev}", 
                                       placeholder="Scrie observație...",
                                       height=60)
                    
                    if st.button("📨 Trimite", key=f"bm_r_{cl_sel}_{elev}", use_container_width=True):
                        if motiv.strip():
                            conn.execute("INSERT INTO messages (dt, name, sub, msg) VALUES (?,?,?,?)", 
                                       (datetime.now().strftime("%d-%m-%Y"), 
                                        elev, st.session_state.materia, motiv.strip()))
                            conn.commit()
                            st.info("Observație trimisă!")
                            st.rerun()

    # --- INTERFAȚA PĂRINTE (NEMODIFICATĂ, DOAR COMPACTĂ) ---
    elif st.session_state.role == "parent":
        elev = st.session_state.nume_elev
        
        # Informații compacte
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            nota_purtare = get_conduct_value(elev, conn)
            st.metric("⭐ Purtare", f"{nota_purtare}/10")
        
        with col_info2:
            total_note = pd.read_sql(f"SELECT COUNT(*) FROM grades WHERE name='{elev}'", conn).iloc[0,0]
            st.metric("📊 Note", total_note)
        
        with col_info3:
            total_abs = pd.read_sql(f"SELECT COUNT(*) FROM absences WHERE name='{elev}'", conn).iloc[0,0]
            st.metric("❌ Absențe", total_abs)
        
        st.markdown("---")
        
        # Tabs pentru diferite categorii
        tab_note, tab_absente, tab_obs = st.tabs(["📝 Note", "❌ Absențe", "⚠️ Observații"])
        
        with tab_note:
            grades_df = pd.read_sql(f"""
                SELECT dt as Data, sub as Materia, val as Nota 
                FROM grades 
                WHERE name='{elev}' 
                ORDER BY dt DESC
            """, conn)
            
            if not grades_df.empty:
                st.dataframe(grades_df, use_container_width=True, hide_index=True, height=200)
            else:
                st.info("Nu există note înregistrate.")
        
        with tab_absente:
            abs_df = pd.read_sql(f"""
                SELECT dt as Data 
                FROM absences 
                WHERE name='{elev}' 
                ORDER BY dt DESC
            """, conn)
            
            if not abs_df.empty:
                st.dataframe(abs_df, use_container_width=True, hide_index=True, height=150)
            else:
                st.success("Nu există absențe.")
        
        with tab_obs:
            m_df = pd.read_sql(f"""
                SELECT dt as Data, sub as Materia, msg as Observație 
                FROM messages 
                WHERE name='{elev}' 
                ORDER BY dt DESC
            """, conn)
            
            if not m_df.empty:
                for _, row in m_df.iterrows():
                    st.warning(f"**{row['Data']} - {row['Materia']}**\n{row['Observație']}")
            else:
                st.success("Nicio observație înregistrată.")

    # --- INTERFAȚA DIRECTOARE (COMPACTĂ) ---
    elif st.session_state.role == "admin":
        all_students = []
        for students in CLASE.values():
            all_students.extend(students)
        
        e_s = st.selectbox("Selectează elev", sorted(all_students), key="admin_select_student")
        
        if e_s:
            # Layout compact
            col_set, col_view = st.columns(2)
            
            with col_set:
                st.subheader("⚙️ Setări")
                v_p = get_conduct_value(e_s, conn)
                noua_p = st.slider("Nota purtare", 1, 10, int(v_p), key=f"slider_{e_s}")
                
                if st.button("💾 Salvează purtare", use_container_width=True):
                    conn.execute("DELETE FROM conduct WHERE name=?", (e_s,))
                    conn.execute("INSERT INTO conduct (name, val) VALUES (?,?)", (e_s, noua_p))
                    conn.commit()
                    st.success(f"Purtare actualizată: {noua_p}")
                    st.rerun()
            
            with col_view:
                st.subheader("📨 Observații")
                msgs = pd.read_sql(f"""
                    SELECT id, dt, sub, msg 
                    FROM messages 
                    WHERE name='{elev}' 
                    ORDER BY dt DESC
                """, conn)
                
                if not msgs.empty:
                    for index, row in msgs.iterrows():
                        with st.container():
                            st.caption(f"{row['dt']} - {row['sub']}")
                            st.text(row['msg'])
                            if st.button("🗑️ Șterge", key=f"del_{row['id']}"):
                                conn.execute("DELETE FROM messages WHERE id=?", (row['id'],))
                                conn.commit()
                                st.rerun()
                            st.markdown("---")
                else:
                    st.info("Nu există observații.")
        
        # Buton rapid pentru toate mesajele
        st.markdown("---")
        if st.button("📋 Vezi toate mesajele"):
            all_msgs = pd.read_sql("SELECT name, dt, sub, msg FROM messages ORDER BY dt DESC LIMIT 20", conn)
            if not all_msgs.empty:
                st.dataframe(all_msgs, use_container_width=True, height=250)

# Footer mic
st.markdown("---")
st.caption("© Catalog Digital | Sistem securizat")
