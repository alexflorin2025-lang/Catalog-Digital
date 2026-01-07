import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import hashlib

# 1. Configurare Pagina
st.set_page_config(
    page_title="Catalog Digital", 
    page_icon="🎓", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS - Ultra Dark & Mirror Gradient
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #000 !important; 
    }
    .stApp { 
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url("https://images.unsplash.com/photo-1546410531-bb4ffa13a774?q=80&w=2940&auto=format") !important; 
        background-size: cover !important; 
        background-position: center !important; 
        background-attachment: fixed !important;
    }
    footer, #MainMenu {visibility: hidden !important;}
    
    /* Card Central */
    [data-testid="stVerticalBlock"] > div:has(div.stButton), 
    .stExpander {
        background: linear-gradient(to bottom, rgba(60,85,120,0.4), rgba(5,15,30,0.98) 50%, rgba(60,85,120,0.4)) !important;
        backdrop-filter: blur(15px) !important; 
        border: 1px solid rgba(255,255,255,0.15) !important; 
        border-radius: 20px !important;
        padding: 20px !important;
        margin: 10px 0 !important;
    }
    
    div.stButton > button { 
        width: 100% !important; 
        background-color: #000 !important; 
        color: #fff !important; 
        height: 42px !important; 
        border-radius: 10px !important; 
        border: 1px solid #333 !important; 
        font-weight: 700 !important; 
    }
    
    .stButton > button[kind="secondary"] { 
        background-color: #1a0000 !important; 
        color: #ff4b4b !important; 
        border-color: #400 !important; 
    }
    
    input, div[data-baseweb="select"] > div, textarea { 
        background-color: rgba(0,0,0,0.8) !important; 
        color: white !important; 
        border: 1px solid #444 !important; 
        border-radius: 8px !important;
    }
    
    h1, h2, h3, label p { 
        color: white !important; 
        text-align: center !important; 
    }
    
    /* Fix pentru margin-top */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    /* Pentru dark mode */
    .stDataFrame {
        background-color: rgba(0,0,0,0.5) !important;
        color: white !important;
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
    
    # Tabele principale
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
    
    # Inițializare note purtare
    conn.commit()
    return conn

# 5. Funcții utilitare
def verify_password(password, role):
    """Verifică parola hash"""
    return hashlib.sha256(password.encode()).hexdigest() == PASSWORDS[role]

def get_conduct_value(name, conn):
    """Obține nota de purtare pentru un elev"""
    cursor = conn.cursor()
    cursor.execute("SELECT val FROM conduct WHERE name = ?", (name,))
    result = cursor.fetchone()
    return result[0] if result else 10

def setup_initial_conduct(conn, classes):
    """Initializează notele de purtare pentru toți elevii"""
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

# Inițializează purtarea pentru toți elevii
setup_initial_conduct(conn, CLASE)

# 7. State sesiune
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.materia = None
    st.session_state.nume_elev = None
    st.session_state.selected_class = "6B"  # Default class

# --- LOGICA NAVIGARE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='margin-top: 20px;'>🎓 Catalog Digital</h1>", unsafe_allow_html=True)
    
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
        # Combină toți elevii dintre toate clasele
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
    # --- BUTON DECONECTARE COMUN ---
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("🚪 DECONECTARE", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown("---")
    
    # --- INTERFAȚA PROFESOR ---
    if st.session_state.role == "teacher":
        st.markdown(f"### 📚 {st.session_state.materia}")
        
        cl_sel = st.selectbox("Selectează Clasa", list(CLASE.keys()), 
                             key="prof_class_selector")
        
        # Afișează notele existente pentru clasa selectată
        st.subheader(f"Note existente - Clasa {cl_sel}")
        grades_df = pd.read_sql(f"""
            SELECT name as Elev, val as Nota, dt as Data 
            FROM grades 
            WHERE cl = '{cl_sel}' AND sub = '{st.session_state.materia}'
            ORDER BY dt DESC
        """, conn)
        
        if not grades_df.empty:
            st.dataframe(grades_df, use_container_width=True, hide_index=True)
        else:
            st.info("Nu există note înregistrate pentru această clasă.")
        
        st.markdown("---")
        st.subheader("Adaugă note/absente")
        
        # Formular pentru fiecare elev
        for elev in CLASE[cl_sel]:
            with st.expander(f"👤 {elev}", expanded=False):
                col_note, col_abs, col_msg = st.columns(3)
                
                with col_note:
                    nota_v = st.number_input("Notă", 1, 10, 10, 
                                           key=f"n_{cl_sel}_{elev}")
                    if st.button("➕ Adaugă Nota", key=f"btn_n_{cl_sel}_{elev}"):
                        conn.execute("INSERT INTO grades (dt, cl, name, sub, val) VALUES (?,?,?,?,?)", 
                                   (datetime.now().strftime("%d-%m-%Y %H:%M"), 
                                    cl_sel, elev, st.session_state.materia, nota_v))
                        conn.commit()
                        st.success(f"Nota {nota_v} adăugată pentru {elev}")
                        st.rerun()
                
                with col_abs:
                    st.write("")  # Spacing
                    st.write("")  # Spacing
                    if st.button("❌ Marchează Absent", key=f"btn_a_{cl_sel}_{elev}"):
                        conn.execute("INSERT INTO absences (dt, cl, name) VALUES (?,?,?)", 
                                   (datetime.now().strftime("%d-%m-%Y"), cl_sel, elev))
                        conn.commit()
                        st.warning(f"{elev} marcat absent")
                        st.rerun()
                
                with col_msg:
                    motiv = st.text_area("Observație", 
                                       key=f"txt_{cl_sel}_{elev}", 
                                       placeholder="Introdu observația...",
                                       height=80)
                    if st.button("📨 Trimite Observație", key=f"btn_m_{cl_sel}_{elev}"):
                        if motiv.strip():
                            conn.execute("INSERT INTO messages (dt, name, sub, msg) VALUES (?,?,?,?)", 
                                       (datetime.now().strftime("%d-%m-%Y"), 
                                        elev, st.session_state.materia, motiv.strip()))
                            conn.commit()
                            st.info(f"Observație trimisă pentru {elev}")
                            st.rerun()
                        else:
                            st.error("Introdu un text pentru observație!")

    # --- INTERFAȚA PĂRINTE ---
    elif st.session_state.role == "parent":
        elev = st.session_state.nume_elev
        st.markdown(f"### 👋 Elev: {elev}")
        
        # Găsește clasa elevului
        elev_clasa = None
        for clasa, studenti in CLASE.items():
            if elev in studenti:
                elev_clasa = clasa
                break
        
        if elev_clasa:
            st.caption(f"Clasa: {elev_clasa}")
        
        # Notele elevului
        st.subheader("📊 Note")
        grades_df = pd.read_sql(f"""
            SELECT dt as Data, sub as Materia, val as Nota 
            FROM grades 
            WHERE name='{elev}' 
            ORDER BY dt DESC
        """, conn)
        
        if not grades_df.empty:
            # Calcul medie pe materii
            st.dataframe(grades_df, use_container_width=True, hide_index=True)
            
            # Medii pe materii
            st.subheader("📈 Medii pe materii")
            medii = grades_df.groupby('Materia')['Nota'].mean().round(2)
            for materia, medie in medii.items():
                col_m, col_v = st.columns([2, 1])
                col_m.write(f"**{materia}**")
                col_v.metric("Medie", f"{medie}")
        else:
            st.info("Nu există note înregistrate.")
        
        # Absențe
        st.subheader("❌ Absențe")
        abs_df = pd.read_sql(f"""
            SELECT dt as Data 
            FROM absences 
            WHERE name='{elev}' 
            ORDER BY dt DESC
        """, conn)
        
        if not abs_df.empty:
            st.dataframe(abs_df, use_container_width=True, hide_index=True)
            st.warning(f"Total absențe: {len(abs_df)}")
        else:
            st.success("Nu există absențe.")
        
        # Observații
        st.subheader("📝 Observații de la profesori")
        m_df = pd.read_sql(f"""
            SELECT dt as Data, sub as Materia, msg as Observație 
            FROM messages 
            WHERE name='{elev}' 
            ORDER BY dt DESC
        """, conn)
        
        if not m_df.empty:
            for _, row in m_df.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div style="background-color:rgba(255,75,75,0.1); 
                                padding:12px; 
                                border-radius:10px; 
                                border-left:4px solid #ff4b4b;
                                margin:5px 0;">
                        <strong>{row['Data']} - {row['Materia']}</strong><br>
                        {row['Observație']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("Nicio observație înregistrată.")
        
        # Purtare
        st.subheader("⭐ Purtare")
        nota_purtare = get_conduct_value(elev, conn)
        st.metric("Nota de purtare", f"{nota_purtare}/10")

    # --- INTERFAȚA DIRECTOARE ---
    elif st.session_state.role == "admin":
        st.markdown("### 🏛️ Panou de Control Directoare")
        
        tab_stat, tab_elev, tab_clasa = st.tabs(["📊 Statistici", "👤 Management Elev", "🏫 Vizualizare Clasă"])
        
        with tab_stat:
            st.subheader("Statistici generale")
            
            # Total note
            total_grades = pd.read_sql("SELECT COUNT(*) as count FROM grades", conn)['count'].iloc[0]
            total_abs = pd.read_sql("SELECT COUNT(*) as count FROM absences", conn)['count'].iloc[0]
            total_msgs = pd.read_sql("SELECT COUNT(*) as count FROM messages", conn)['count'].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Note", total_grades)
            col2.metric("Total Absențe", total_abs)
            col3.metric("Total Observații", total_msgs)
            
            # Distribuția notelor
            st.subheader("Distribuția notelor")
            dist_df = pd.read_sql("SELECT val, COUNT(*) as count FROM grades GROUP BY val ORDER BY val", conn)
            if not dist_df.empty:
                st.bar_chart(dist_df.set_index('val'))
        
        with tab_elev:
            st.subheader("Management elev individual")
            
            all_students = []
            for students in CLASE.values():
                all_students.extend(students)
            
            e_s = st.selectbox("Selectează elev", sorted(all_students), key="admin_select_student")
            
            if e_s:
                # Scădere manuală purtare
                v_p = get_conduct_value(e_s, conn)
                
                col_p1, col_p2 = st.columns([2, 1])
                with col_p1:
                    noua_p = st.slider("Setează Nota Purtare", 1, 10, int(v_p), 
                                      key=f"slider_{e_s}")
                with col_p2:
                    st.write("")  # Spacing
                    st.write("")  # Spacing
                    if st.button("💾 SALVEAZĂ PURTARE", key=f"save_conduct_{e_s}"):
                        conn.execute("DELETE FROM conduct WHERE name=?", (e_s,))
                        conn.execute("INSERT INTO conduct (name, val) VALUES (?,?)", (e_s, noua_p))
                        conn.commit()
                        st.success(f"Purtare actualizată pentru {e_s}: {noua_p}")
                        st.rerun()
                
                # Vizualizare și ștergere observații
                st.subheader("Observații profesori")
                msgs = pd.read_sql(f"""
                    SELECT id, dt, sub, msg 
                    FROM messages 
                    WHERE name='{e_s}' 
                    ORDER BY dt DESC
                """, conn)
                
                if not msgs.empty:
                    for index, row in msgs.iterrows():
                        with st.container():
                            col_m, col_b = st.columns([4, 1])
                            with col_m:
                                st.markdown(f"""
                                <div style="background-color:rgba(255,165,0,0.1); 
                                            padding:10px; 
                                            border-radius:8px;
                                            margin:5px 0;">
                                    <strong>{row['dt']} - {row['sub']}</strong><br>
                                    {row['msg']}
                                </div>
                                """, unsafe_allow_html=True)
                            with col_b:
                                if st.button("🗑️", key=f"del_msg_{row['id']}"):
                                    conn.execute("DELETE FROM messages WHERE id=?", (row['id'],))
                                    conn.commit()
                                    st.success("Observație ștearsă!")
                                    st.rerun()
                else:
                    st.info("Nu există observații pentru acest elev.")
        
        with tab_clasa:
            st.subheader("Vizualizare clasă")
            
            cl_select = st.selectbox("Selectează clasa", list(CLASE.keys()), key="admin_class_view")
            
            if cl_select:
                # Note pentru toată clasa
                st.write(f"**Note - Clasa {cl_select}**")
                class_grades = pd.read_sql(f"""
                    SELECT name as Elev, sub as Materia, val as Nota, dt as Data
                    FROM grades 
                    WHERE cl = '{cl_select}'
                    ORDER BY name, dt DESC
                """, conn)
                
                if not class_grades.empty:
                    st.dataframe(class_grades, use_container_width=True, hide_index=True)
                    
                    # Export opțional
                    csv = class_grades.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Exportă note (CSV)",
                        data=csv,
                        file_name=f"note_clasa_{cl_select}.csv",
                        mime="text/csv",
                        key="export_grades"
                    )
                else:
                    st.info("Nu există note pentru această clasă.")

# 8. Footer informativ
st.markdown("---")
st.caption("© Catalog Digital v1.0 | Sistem de management școlar")
