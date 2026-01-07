import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import hashlib

# 1. Configurare Pagina minimală
st.set_page_config(
    page_title="Catalog", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# 2. CSS ULTRA COMPACT pentru Nokia G21
st.markdown("""
<style>
/* RESET COMPLET - FARA MARGINI */
* {
    margin: 0 !important;
    padding: 0 !important;
}

html, body, [data-testid="stAppViewContainer"] {
    height: 100vh !important;
    overflow: hidden !important;
    background: #000 !important;
}

.stApp {
    background: #000 !important;
    padding: 2px !important;
    height: 100vh !important;
}

/* ASCUNDE TOT CE NU E NECESAR */
footer, #MainMenu, .stDeployButton, header {
    display: none !important;
}

/* HEADER MIC */
h1, h2, h3 {
    margin: 2px 0 !important;
    font-size: 1rem !important;
    text-align: center !important;
    color: white !important;
}

/* DECONECTARE MICĂ SUS */
.deconectare-btn {
    position: fixed;
    top: 2px;
    right: 2px;
    z-index: 9999;
    width: 40px !important;
    height: 30px !important;
    padding: 0 !important;
}

/* TABS FOARTE MICI */
.stTabs [data-baseweb="tab-list"] {
    gap: 1px !important;
    padding: 1px !important;
}

.stTabs [data-baseweb="tab"] {
    padding: 2px 4px !important;
    font-size: 0.7rem !important;
    min-width: 60px !important;
}

/* BUTOANE MINI */
div.stButton > button {
    height: 28px !important;
    font-size: 0.7rem !important;
    margin: 1px !important;
    padding: 0 4px !important;
    border-radius: 4px !important;
}

/* EXPANDER MIC - DOAR 1 LINIE CAND E INCHIS */
.stExpander {
    margin: 1px 0 !important;
    border: 1px solid #333 !important;
}

.streamlit-expanderHeader {
    padding: 2px 4px !important;
    font-size: 0.75rem !important;
    height: 28px !important;
    min-height: 28px !important;
}

.streamlit-expanderContent {
    padding: 3px !important;
    font-size: 0.7rem !important;
}

/* INPUT-URI FOARTE MICI */
.stNumberInput input {
    height: 28px !important;
    padding: 0 4px !important;
    font-size: 0.8rem !important;
}

.stTextInput input, .stSelectbox div {
    height: 28px !important;
    font-size: 0.8rem !important;
    padding: 0 4px !important;
}

/* TEXTAREA MICĂ */
textarea {
    height: 40px !important;
    font-size: 0.75rem !important;
    padding: 2px !important;
    margin: 2px 0 !important;
}

/* CONTAINER PRINCIPAL CU SCROLL LIMITAT */
.main-container {
    height: calc(100vh - 60px) !important;
    overflow-y: auto !important;
    padding: 2px !important;
}

/* COLUMN FARA SPATIU */
[data-testid="column"] {
    padding: 0 1px !important;
}

/* SCROLLBAR INVISIBIL */
::-webkit-scrollbar {
    width: 3px !important;
}

/* CARD COMPACT */
.compact-card {
    background: rgba(20, 30, 40, 0.9);
    border-radius: 6px;
    padding: 4px;
    margin: 2px 0;
    border: 1px solid #444;
}

/* INFO MIC */
.stMetric {
    padding: 2px !important;
}

.stMetric label {
    font-size: 0.7rem !important;
}

.stMetric div {
    font-size: 0.9rem !important;
}

/* ASCUNDE LABELE CAND E POSIBIL */
[data-testid="stWidgetLabel"] p {
    font-size: 0.7rem !important;
    margin-bottom: 1px !important;
}

</style>
""", unsafe_allow_html=True)

# 3. Parole simple (hash pentru siguranta)
PASSWORDS = {
    "teacher": hashlib.sha256("123".encode()).hexdigest(),
    "parent": hashlib.sha256("1234".encode()).hexdigest(),
    "admin": hashlib.sha256("admin".encode()).hexdigest()
}

# 4. Baza de date - SUPER SIMPLA
def init_db():
    conn = sqlite3.connect('catalog.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dt TEXT, 
        name TEXT, 
        sub TEXT, 
        val INT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS absences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dt TEXT, 
        name TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        dt TEXT, 
        name TEXT, 
        sub TEXT, 
        msg TEXT
    )''')
    
    conn.commit()
    return conn

# 5. Funcții rapide
def verify_password(password, role):
    return hashlib.sha256(password.encode()).hexdigest() == PASSWORDS[role]

# 6. Setup
conn = init_db()

# Elevi - DOAR NUME, FARA CLASE COMPLICATE
ELEVI_6B = ["Albert", "Alex", "Alissa", "Andrei G", "Andrei C", "Ayan", 
           "Beatrice", "Bianca", "Bogdan", "David", "Eduard", "Erika", 
           "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", 
           "Marius", "Mihnea", "Natalia", "Raisa", "Rares A", "Rares V", "Yanis"]

# 7. State minimal
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# === LOGIN SCREEN SUPER COMPACT ===
if not st.session_state.logged_in:
    st.markdown("<h3>🎓 Catalog</h3>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Prof", "Par", "Dir"])
    
    with tab1:
        materia = st.selectbox("Materia", ["Info", "Mate", "Rom"], key="m", label_visibility="collapsed")
        passw = st.text_input("Parola", type="password", key="p1", label_visibility="collapsed")
        if st.button("Intră", key="b1", use_container_width=True):
            if verify_password(passw, "teacher"):
                st.session_state.update(logged_in=True, role="teacher", materia=materia)
                st.rerun()
    
    with tab2:
        elev = st.selectbox("Elev", ELEVI_6B, key="e", label_visibility="collapsed")
        passw = st.text_input("Parola", type="password", key="p2", label_visibility="collapsed")
        if st.button("Intră", key="b2", use_container_width=True):
            if verify_password(passw, "parent"):
                st.session_state.update(logged_in=True, role="parent", nume_elev=elev)
                st.rerun()
    
    with tab3:
        passw = st.text_input("Cod", type="password", key="p3", label_visibility="collapsed")
        if st.button("Intră", key="b3", use_container_width=True):
            if verify_password(passw, "admin"):
                st.session_state.update(logged_in=True, role="admin")
                st.rerun()

else:
    # === BUTON DECONECTARE MIC ===
    st.markdown('<div class="deconectare-btn">', unsafe_allow_html=True)
    if st.button("❌", help="Ieși", key="exit"):
        st.session_state.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Spacing pentru buton
    st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
    
    # === CONTAINER PRINCIPAL ===
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # === PROFESOR - INTERFAȚĂ TABELARĂ COMPACTĂ ===
    if st.session_state.role == "teacher":
        st.markdown(f"**{st.session_state.materia}**")
        
        # CĂUTARE RAPIDĂ
        search = st.text_input("🔍", placeholder="Nume elev", key="search", label_visibility="collapsed")
        
        # FILTRU ELEVI
        if search:
            elev_list = [e for e in ELEVI_6B if search.lower() in e.lower()]
        else:
            elev_list = ELEVI_6B
        
        # DOAR 8 ELEVI PE PAGINĂ
        PAGE_SIZE = 8
        total_pages = (len(elev_list) + PAGE_SIZE - 1) // PAGE_SIZE
        
        if total_pages > 1:
            page = st.selectbox("Pag", list(range(total_pages)), 
                              format_func=lambda x: f"{x+1}", key="page")
        else:
            page = 0
        
        start_idx = page * PAGE_SIZE
        current_elev = elev_list[start_idx:start_idx + PAGE_SIZE]
        
        # TABEL COMPACT
        for elev in current_elev:
            with st.expander(elev[:12], expanded=False):
                # LINIE 1: NOTĂ
                col1, col2 = st.columns([2, 1])
                with col1:
                    nota = st.number_input("Nota", 1, 10, 10, key=f"n_{elev}", label_visibility="collapsed")
                with col2:
                    if st.button("✓", key=f"add_{elev}"):
                        conn.execute("INSERT INTO grades (dt, name, sub, val) VALUES (?,?,?,?)",
                                   (datetime.now().strftime("%d/%m"), elev, st.session_state.materia, nota))
                        conn.commit()
                        st.rerun()
                
                # LINIE 2: ACTIUNI RAPIDE
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("❌ Abs", key=f"abs_{elev}", use_container_width=True):
                        conn.execute("INSERT INTO absences (dt, name) VALUES (?,?)",
                                   (datetime.now().strftime("%d/%m"), elev))
                        conn.commit()
                        st.rerun()
                
                with col_b:
                    obs = st.text_input("Obs", key=f"obs_{elev}", placeholder="scrie...", label_visibility="collapsed")
                    if obs and st.button("📩", key=f"msg_{elev}"):
                        conn.execute("INSERT INTO messages (dt, name, sub, msg) VALUES (?,?,?,?)",
                                   (datetime.now().strftime("%d/%m"), elev, st.session_state.materia, obs))
                        conn.commit()
                        st.rerun()
        
        # STATISTICI JOS
        st.markdown("---")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            note_azi = pd.read_sql(f"""
                SELECT COUNT(*) FROM grades 
                WHERE sub='{st.session_state.materia}' AND dt=date('now')
            """, conn).iloc[0,0]
            st.metric("Note azi", note_azi)
        
        with col_s2:
            abs_azi = pd.read_sql("SELECT COUNT(*) FROM absences WHERE dt=date('now')", conn).iloc[0,0]
            st.metric("Abs azi", abs_azi)
    
    # === PĂRINTE - DOAR 3 TAB-URI MICI ===
    elif st.session_state.role == "parent":
        elev = st.session_state.nume_elev
        
        # TABS MICI
        t1, t2, t3 = st.tabs(["Note", "Abs", "Obs"])
        
        with t1:
            # NOTE RECENTE (max 5)
            notes = pd.read_sql(f"""
                SELECT sub, val, dt FROM grades 
                WHERE name='{elev}' 
                ORDER BY dt DESC LIMIT 5
            """, conn)
            
            if not notes.empty:
                for _, row in notes.iterrows():
                    st.markdown(f"""
                    <div class='compact-card'>
                        <strong>{row['sub']}</strong>: {row['val']} 
                        <small style='float:right'>{row['dt']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Fără note")
        
        with t2:
            # ABSENȚE RECENTE
            absente = pd.read_sql(f"""
                SELECT dt FROM absences 
                WHERE name='{elev}' 
                ORDER BY dt DESC LIMIT 5
            """, conn)
            
            if not absente.empty:
                for date in absente['dt']:
                    st.markdown(f"• {date}")
            else:
                st.success("Fără absențe")
        
        with t3:
            # OBSERVAȚII RECENTE
            obs = pd.read_sql(f"""
                SELECT sub, msg FROM messages 
                WHERE name='{elev}' 
                ORDER BY dt DESC LIMIT 3
            """, conn)
            
            if not obs.empty:
                for _, row in obs.iterrows():
                    st.warning(f"**{row['sub']}**: {row['msg'][:40]}...")
            else:
                st.success("Fără observații")
    
    # === DIRECTOARE - PANOU SIMPLU ===
    elif st.session_state.role == "admin":
        st.markdown("**Admin**")
        
        # BUTOANE RAPIDE
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Mesaje", use_container_width=True):
                st.session_state.admin_view = "msgs"
        
        with col_b:
            if st.button("Șterge", use_container_width=True, type="secondary"):
                if st.checkbox("Confirmă ștergerea"):
                    conn.execute("DELETE FROM messages WHERE dt < date('now', '-30 days')")
                    conn.commit()
                    st.success("Șters!")
        
        # VIZUALIZARE
        if 'admin_view' not in st.session_state:
            st.session_state.admin_view = "stats"
        
        if st.session_state.admin_view == "msgs":
            msgs = pd.read_sql("SELECT name, msg FROM messages ORDER BY dt DESC LIMIT 5", conn)
            if not msgs.empty:
                for _, row in msgs.iterrows():
                    st.text(f"{row['name']}: {row['msg'][:30]}...")
                    if st.button("🗑️", key=f"del_{row['name']}_{row['msg'][:10]}"):
                        conn.execute("DELETE FROM messages WHERE name=? AND msg LIKE ?",
                                   (row['name'], f"{row['msg'][:10]}%"))
                        conn.commit()
                        st.rerun()
            else:
                st.info("Nu sunt mesaje")
    
    # ÎNCHIDE CONTAINER
    st.markdown('</div>', unsafe_allow_html=True)

# FOOTER MIC
st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
st.caption("<center>v3.0</center>", unsafe_allow_html=True)
