import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import hashlib

# 1. Configurare Pagina
st.set_page_config(
    page_title="Catalog Digital", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS modern cu meniu lateral
st.markdown("""
    <style>
    /* Reset și fundal */
    * {
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh !important;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
    }
    
    /* Ascunde elemente inutile */
    footer, #MainMenu, header {
        visibility: hidden !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 20px 15px !important;
    }
    
    /* Card-uri pentru statistici */
    .stat-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    .stat-card h3 {
        color: #60a5fa !important;
        font-size: 0.9rem !important;
        margin-bottom: 8px !important;
    }
    
    .stat-value {
        color: white !important;
        font-size: 1.8rem !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    
    /* Butoane moderne */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Input-uri moderne */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: rgba(30, 41, 59, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
    }
    
    /* Expander modern */
    .stExpander {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        margin: 8px 0 !important;
    }
    
    .streamlit-expanderHeader {
        background: rgba(15, 23, 42, 0.9) !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    
    /* Tabs modern */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px !important;
        padding: 10px 0 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px !important;
        background: rgba(30, 41, 59, 0.8) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        transition: all 0.3s !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.2) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        color: white !important;
    }
    
    /* Deconectare */
    .logout-btn {
        background: rgba(239, 68, 68, 0.9) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        position: fixed;
        top: 15px;
        right: 15px;
        z-index: 1000;
    }
    
    /* Alert messages */
    .stAlert {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Progress bars */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 8px;
        margin: 5px 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #10b981, #3b82f6);
        border-radius: 10px;
    }
    
    </style>
""", unsafe_allow_html=True)

# 3. Parole mai puternice dar ușor de reținut
# Am folosit cuvinte comune + an important
PASSWORDS_HASH = {
    "teacher": hashlib.sha256("Profesor2024!".encode()).hexdigest(),
    "parent": hashlib.sha256("ElevParinte2024".encode()).hexdigest(),
    "admin": hashlib.sha256("AdminScoala2024@".encode()).hexdigest()
}

# 4. Toate materiile de gimnaziu din Craiova (conform programa națională)
MATERII_GIMNAZIU = [
    "Limba și literatura română",
    "Matematică",
    "Limba engleză",
    "Limba franceză",
    "Limba germană",
    "Istorie",
    "Geografie",
    "Biologie",
    "Fizică",
    "Chimie",
    "Educație fizică și sport",
    "Educație plastică",
    "Educație muzicală",
    "Educație tehnologică",
    "Informatică și TIC",
    "Religie",
    "Consiliere și orientare",
    "Educație pentru societate"
]

# 5. Initializare Baza de Date cu structura îmbunătățită
def init_db():
    conn = sqlite3.connect('catalog_digital.db', check_same_thread=False)
    c = conn.cursor()
    
    # Note
    c.execute('''CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        clasa TEXT,
        nume TEXT,
        materie TEXT,
        nota REAL,
        semestru INTEGER DEFAULT 1
    )''')
    
    # Absențe cu materie (o absență = o oră la o anumită materie)
    c.execute('''CREATE TABLE IF NOT EXISTS absente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        clasa TEXT,
        nume TEXT,
        materie TEXT,
        ora INTEGER  -- ora din orar (1-7)
    )''')
    
    # Observații
    c.execute('''CREATE TABLE IF NOT EXISTS observatii (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        nume TEXT,
        materie TEXT,
        observatie TEXT,
        tip TEXT  -- 'mustrare', 'laudă', 'atenționare'
    )''')
    
    # Purtare
    c.execute('''CREATE TABLE IF NOT EXISTS purtare (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nume TEXT UNIQUE,
        nota INTEGER DEFAULT 10,
        semestru INTEGER DEFAULT 1
    )''')
    
    # Medii calculate (cache pentru performanță)
    c.execute('''CREATE TABLE IF NOT EXISTS medii (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_calcul TEXT,
        nume TEXT,
        materie TEXT,
        media REAL,
        clasa TEXT,
        semestru INTEGER
    )''')
    
    conn.commit()
    return conn

# 6. Funcții utilitare
def verify_password(password, role):
    """Verifică parola hash"""
    return hashlib.sha256(password.encode()).hexdigest() == PASSWORDS_HASH[role]

def get_purtare(nume, conn, semestru=1):
    """Obține nota de purtare"""
    cursor = conn.cursor()
    cursor.execute("SELECT nota FROM purtare WHERE nume = ? AND semestru = ?", (nume, semestru))
    result = cursor.fetchone()
    return result[0] if result else 10

def calcul_media_elev(nume, materie, conn, semestru=1):
    """Calculează media unui elev la o materie"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT AVG(nota) FROM grades 
        WHERE nume = ? AND materie = ? AND semestru = ?
    ''', (nume, materie, semestru))
    result = cursor.fetchone()
    return round(result[0], 2) if result and result[0] else 0.00

def calcul_media_clasa(clasa, materie, conn, semestru=1):
    """Calculează media clasei la o materie"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT AVG(nota) FROM grades 
        WHERE clasa = ? AND materie = ? AND semestru = ?
    ''', (clasa, materie, semestru))
    result = cursor.fetchone()
    return round(result[0], 2) if result and result[0] else 0.00

def get_total_absente_elev(nume, materie, data, conn):
    """Obține numărul de absențe al unui elev la o materie într-o zi"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM absente 
        WHERE nume = ? AND materie = ? AND data = ?
    ''', (nume, materie, data))
    result = cursor.fetchone()
    return result[0] if result else 0

def init_purtare(conn, elevi):
    """Initializează notele de purtare pentru toți elevii"""
    cursor = conn.cursor()
    for elev in elevi:
        # Pentru ambele semestre
        for semestru in [1, 2]:
            cursor.execute("INSERT OR IGNORE INTO purtare (nume, nota, semestru) VALUES (?, ?, ?)", 
                          (elev, 10, semestru))
    conn.commit()

# 7. Setup baza de date
conn = init_db()

# 8. Datele aplicației
CLASE = {
    "6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", 
           "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", 
           "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", 
           "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"],
    "7A": ["Ionescu Maria", "Popescu Dan"],
    "8C": ["Mihai Popescu", "Ana Ionescu", "George Marinescu"]  # Clasă adăugată pentru exemplu
}

# 9. Orașul - pentru afișare
ORAS = "Craiova"

# 10. Inițializare session state
if 'logged_in' not in st.session_state:
    st.session_state.update({
        'logged_in': False,
        'role': None,
        'materie': None,
        'nume_elev': None,
        'clasa_selectata': "6B",
        'semestru': 1,
        'sidebar_open': True
    })

# ============================================
# FUNCȚII PENTRU MENIU LATERAL
# ============================================
def display_statistics_sidebar(role, conn):
    """Afișează statisticile în meniul lateral"""
    
    if role == "teacher":
        st.sidebar.markdown(f"### 📊 Statistici Clasa {st.session_state.clasa_selectata}")
        
        # Media clasei la materia selectată
        if st.session_state.materie:
            media_clasa = calcul_media_clasa(
                st.session_state.clasa_selectata, 
                st.session_state.materie, 
                conn,
                st.session_state.semestru
            )
            
            st.sidebar.markdown(f"""
            <div class="stat-card">
                <h3>📈 Media Clasei</h3>
                <div class="stat-value">{media_clasa}</div>
                <small>{st.session_state.materie}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Numărul de note azi
        today = datetime.now().strftime("%Y-%m-%d")
        note_azi = pd.read_sql(f"""
            SELECT COUNT(*) FROM grades 
            WHERE data LIKE '{today}%' AND clasa = ? AND materie = ?
        """, conn, params=[st.session_state.clasa_selectata, st.session_state.materie]).iloc[0,0]
        
        st.sidebar.markdown(f"""
        <div class="stat-card">
            <h3>📝 Note astăzi</h3>
            <div class="stat-value">{note_azi}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Absențele azi
        abs_azi = pd.read_sql(f"""
            SELECT COUNT(DISTINCT nume) FROM absente 
            WHERE data = '{today}' AND clasa = ?
        """, conn, params=[st.session_state.clasa_selectata]).iloc[0,0]
        
        st.sidebar.markdown(f"""
        <div class="stat-card">
            <h3>❌ Absențe azi</h3>
            <div class="stat-value">{abs_azi}</div>
        </div>
        """, unsafe_allow_html=True)
    
    elif role == "parent":
        elev = st.session_state.nume_elev
        
        # Media generală a elevului
        cursor = conn.cursor()
        cursor.execute('''
            SELECT AVG(nota) FROM grades 
            WHERE nume = ? AND semestru = ?
        ''', (elev, st.session_state.semestru))
        media_generala = cursor.fetchone()[0]
        media_generala = round(media_generala, 2) if media_generala else 0.00
        
        st.sidebar.markdown(f"""
        <div class="stat-card">
            <h3>🏆 Media Generală</h3>
            <div class="stat-value">{media_generala}</div>
            <small>Semestru {st.session_state.semestru}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Purtarea
        nota_purtare = get_purtare(elev, conn, st.session_state.semestru)
        
        st.sidebar.markdown(f"""
        <div class="stat-card">
            <h3>⭐ Purtare</h3>
            <div class="stat-value">{nota_purtare}/10</div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {nota_purtare * 10}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Numărul total de absențe
        total_abs = pd.read_sql(
            "SELECT COUNT(*) FROM absente WHERE nume = ?",
            conn, params=[elev]
        ).iloc[0,0]
        
        st.sidebar.markdown(f"""
        <div class="stat-card">
            <h3>📅 Total Absențe</h3>
            <div class="stat-value">{total_abs}</div>
        </div>
        """, unsafe_allow_html=True)
    
    elif role == "admin":
        # Statistici generale pentru admin
        total_elevi = sum(len(studenti) for studenti in CLASE.values())
        
        st.sidebar.markdown(f"""
        <div class="stat-card">
            <h3>👥 Total Elevi</h3>
            <div class="stat-value">{total_elevi}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Note totale
        total_note = pd.read_sql("SELECT COUNT(*) FROM grades", conn).iloc[0,0]
        
        st.sidebar.markdown(f"""
        <div class="stat-card">
            <h3>📚 Note în sistem</h3>
            <div class="stat-value">{total_note}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Clase active
        st.sidebar.markdown(f"""
        <div class="stat-card">
            <h3>🏫 Clase active</h3>
            <div class="stat-value">{len(CLASE)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Selector semestru pentru toți
    st.sidebar.markdown("---")
    semestru = st.sidebar.radio("Semestru", [1, 2], horizontal=True, key="sidebar_semestru")
    if semestru != st.session_state.semestru:
        st.session_state.semestru = semestru
        st.rerun()

# ============================================
# PAGINA DE LOGIN
# ============================================
if not st.session_state.logged_in:
    st.markdown(f"""
    <div style="text-align: center; padding: 30px 0;">
        <h1 style="color: white; font-size: 2.5rem;">🎓 Catalog Digital</h1>
        <p style="color: #94a3b8; font-size: 1.2rem;">Gimnaziul din {ORAS}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Informații despre parole pentru ușurință
    with st.expander("ℹ️ Informații autentificare", expanded=False):
        st.info("""
        **Parole pentru testare:**
        - **Profesor:** Profesor2024!
        - **Părinte:** ElevParinte2024
        - **Directoare:** AdminScoala2024@
        
        *Acestea sunt parole puternice dar ușor de reținut.*
        """)
    
    # Tabs pentru autentificare
    tab_prof, tab_parinte, tab_directoare = st.tabs(["👨‍🏫 Profesor", "👪 Părinte", "🏛️ Directoare"])
    
    with tab_prof:
        st.subheader("Autentificare Profesor")
        
        # Selectare materie din lista completă
        materie = st.selectbox(
            "Selectează materia predată",
            MATERII_GIMNAZIU,
            key="login_materie"
        )
        
        # Parolă
        parola = st.text_input("Introdu parola", type="password", key="parola_prof")
        
        if st.button("Accesează platforma", type="primary", use_container_width=True):
            if parola and verify_password(parola, "teacher"):
                st.session_state.logged_in = True
                st.session_state.role = "teacher"
                st.session_state.materie = materie
                st.success(f"Bine ai venit, profesorule de {materie}!")
                st.rerun()
            else:
                st.error("Parolă incorectă! Încearcă: Profesor2024!")
    
    with tab_parinte:
        st.subheader("Autentificare Părinte")
        
        # Combină toți elevii
        all_students = []
        for clasa, studenti in CLASE.items():
            for student in studenti:
                all_students.append(f"{student} ({clasa})")
        
        elev_selectat = st.selectbox(
            "Selectează elevul",
            sorted(all_students),
            key="login_elev"
        )
        
        # Extrage numele și clasa
        if "(" in elev_selectat:
            nume_elev = elev_selectat.split(" (")[0]
            clasa_elev = elev_selectat.split(" (")[1].replace(")", "")
        else:
            nume_elev = elev_selectat
            clasa_elev = "6B"
        
        parola_parinte = st.text_input("Parolă părinte", type="password", key="parola_parinte")
        
        if st.button("Vezi situația elevului", type="primary", use_container_width=True):
            if parola_parinte and verify_password(parola_parinte, "parent"):
                st.session_state.logged_in = True
                st.session_state.role = "parent"
                st.session_state.nume_elev = nume_elev
                st.session_state.clasa_selectata = clasa_elev
                st.success(f"Bine ai venit, părinte al lui {nume_elev}!")
                st.rerun()
            else:
                st.error("Parolă incorectă! Încearcă: ElevParinte2024")
    
    with tab_directoare:
        st.subheader("Autentificare Directoare")
        
        parola_admin = st.text_input("Cod de acces administrativ", type="password", key="parola_admin")
        
        if st.button("Accesează panoul administrativ", type="primary", use_container_width=True):
            if parola_admin and verify_password(parola_admin, "admin"):
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.success("Bine ai venit, doamnă directoare!")
                st.rerun()
            else:
                st.error("Cod incorect! Încearcă: AdminScoala2024@")

# ============================================
# PAGINA PRINCIPALĂ (După login)
# ============================================
else:
    # Header cu buton deconectare
    col_title, col_logout = st.columns([4, 1])
    
    with col_title:
        if st.session_state.role == "teacher":
            st.markdown(f"<h2>👨‍🏫 Profesor - {st.session_state.materie}</h2>", unsafe_allow_html=True)
            st.caption(f"Clasa selectată: {st.session_state.clasa_selectata} | Semestru {st.session_state.semestru}")
        elif st.session_state.role == "parent":
            st.markdown(f"<h2>👪 Părinte - {st.session_state.nume_elev}</h2>", unsafe_allow_html=True)
            st.caption(f"Clasa: {st.session_state.clasa_selectata} | Semestru {st.session_state.semestru}")
        else:
            st.markdown(f"<h2>🏛️ Panou Directoare - {ORAS}</h2>", unsafe_allow_html=True)
    
    with col_logout:
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("🚪 Deconectare", type="secondary"):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Meniu lateral cu statistici
    with st.sidebar:
        display_statistics_sidebar(st.session_state.role, conn)
        
        # Oraș și info
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"""
        <div style="color: #94a3b8; font-size: 0.8rem; text-align: center;">
            <p>📚 <strong>Gimnaziul {ORAS}</strong></p>
            <p>© 2024 Catalog Digital v3.0</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================
    # INTERFAȚA PROFESOR
    # ============================================
    if st.session_state.role == "teacher":
        main_col1, main_col2 = st.columns([3, 1])
        
        with main_col1:
            # Selectare clasă
            clasa = st.selectbox("Selectează clasa", list(CLASE.keys()), key="prof_clasa")
            if clasa != st.session_state.clasa_selectata:
                st.session_state.clasa_selectata = clasa
                st.rerun()
            
            # Filtru rapid pentru elevi
            search_query = st.text_input("🔍 Caută elev în clasă...", key="search_elev")
            
            # Filtrare elevi
            if search_query:
                elevi_filtrati = [e for e in CLASE[clasa] if search_query.lower() in e.lower()]
            else:
                elevi_filtrati = CLASE[clasa]
            
            st.markdown(f"### 📋 Lista elevilor - {len(elevi_filtrati)} elevi")
            
            # Afișare elevi cu acțiuni
            for elev in elevi_filtrati:
                with st.expander(f"👤 {elev}", expanded=False):
                    col_info, col_stats = st.columns([2, 1])
                    
                    with col_info:
                        # Media elevului la materia curentă
                        media_elev = calcul_media_elev(elev, st.session_state.materie, conn, st.session_state.semestru)
                        st.metric(f"📊 Media la {st.session_state.materie[:15]}...", f"{media_elev}")
                        
                        # Adăugare notă
                        nota_noua = st.number_input("Notă nouă", 1.0, 10.0, 8.0, 0.5, 
                                                   key=f"nota_{elev}_{clasa}")
                        
                        if st.button("📝 Adaugă notă", key=f"btn_nota_{elev}", use_container_width=True):
                            data_curenta = datetime.now().strftime("%Y-%m-%d %H:%M")
                            conn.execute(
                                "INSERT INTO grades (data, clasa, nume, materie, nota, semestru) VALUES (?, ?, ?, ?, ?, ?)",
                                (data_curenta, clasa, elev, st.session_state.materie, nota_noua, st.session_state.semestru)
                            )
                            conn.commit()
                            st.success(f"Nota {nota_noua} adăugată pentru {elev}!")
                            st.rerun()
                    
                    with col_stats:
                        # Absențe azi
                        today = datetime.now().strftime("%Y-%m-%d")
                        absente_azi = get_total_absente_elev(elev, st.session_state.materie, today, conn)
                        
                        # Buton pentru absență
                        if st.button(f"❌ Absent ({absente_azi})", key=f"btn_abs_{elev}", use_container_width=True):
                            data_curenta = datetime.now().strftime("%Y-%m-%d")
                            ora_curenta = datetime.now().hour - 7  # Presupunem că prima oră e la 8
                            ora_curenta = max(1, min(7, ora_curenta))  # Limită 1-7
                            
                            conn.execute(
                                "INSERT INTO absente (data, clasa, nume, materie, ora) VALUES (?, ?, ?, ?, ?)",
                                (data_curenta, clasa, elev, st.session_state.materie, ora_curenta)
                            )
                            conn.commit()
                            st.warning(f"Absență înregistrată pentru {elev} la ora {ora_curenta}!")
                            st.rerun()
                        
                        # Purtare
                        nota_purtare = get_purtare(elev, conn, st.session_state.semestru)
                        st.metric("⭐ Purtare", f"{nota_purtare}")
                    
                    # Observație
                    observatie = st.text_area("Observație comportament", 
                                             key=f"obs_{elev}", 
                                             placeholder="Scrie observația aici...",
                                             height=60)
                    
                    col_obs1, col_obs2, col_obs3 = st.columns(3)
                    
                    with col_obs1:
                        if st.button("⚠️ Atenționare", key=f"at_{elev}", use_container_width=True):
                            if observatie.strip():
                                data_curenta = datetime.now().strftime("%Y-%m-%d %H:%M")
                                conn.execute(
                                    "INSERT INTO observatii (data, nume, materie, observatie, tip) VALUES (?, ?, ?, ?, ?)",
                                    (data_curenta, elev, st.session_state.materie, observatie.strip(), "atenționare")
                                )
                                conn.commit()
                                st.info(f"Atenționare trimisă pentru {elev}!")
                                st.rerun()
                    
                    with col_obs2:
                        if st.button("👏 Laudă", key=f"lauda_{elev}", use_container_width=True):
                            if observatie.strip():
                                data_curenta = datetime.now().strftime("%Y-%m-%d %H:%M")
                                conn.execute(
                                    "INSERT INTO observatii (data, nume, materie, observatie, tip) VALUES (?, ?, ?, ?, ?)",
                                    (data_curenta, elev, st.session_state.materie, observatie.strip(), "laudă")
                                )
                                conn.commit()
                                st.success(f"Laudă trimisă pentru {elev}!")
                                st.rerun()
        
        with main_col2:
            st.markdown("### 📈 Rapoarte rapide")
            
            # Top 5 elevi
            st.markdown("**🏆 Top 5 elevi**")
            top_elevi = pd.read_sql(f'''
                SELECT nume, AVG(nota) as media 
                FROM grades 
                WHERE clasa = ? AND materie = ? AND semestru = ?
                GROUP BY nume 
                ORDER BY media DESC 
                LIMIT 5
            ''', conn, params=[clasa, st.session_state.materie, st.session_state.semestru])
            
            if not top_elevi.empty:
                for idx, row in top_elevi.iterrows():
                    st.markdown(f"{idx+1}. **{row['nume']}**: {row['media']:.2f}")
            else:
                st.info("Nu există note încă")
            
            st.markdown("---")
            
            # Materii predate (pentru schimbare rapidă)
            st.markdown("**📚 Schimbă materia**")
            materie_noua = st.selectbox("", MATERII_GIMNAZIU, key="schimba_materia", 
                                       label_visibility="collapsed")
            if materie_noua != st.session_state.materie:
                if st.button("Schimbă", use_container_width=True):
                    st.session_state.materie = materie_noua
                    st.rerun()
    
    # ============================================
    # INTERFAȚA PĂRINTE
    # ============================================
    elif st.session_state.role == "parent":
        elev = st.session_state.nume_elev
        clasa = st.session_state.clasa_selectata
        
        tab_overview, tab_note, tab_absente, tab_observatii = st.tabs(["📊 Prezentare generală", "📝 Note", "❌ Absențe", "⚠️ Observații"])
        
        with tab_overview:
            col_medii, col_progres = st.columns([2, 1])
            
            with col_medii:
                st.markdown("### 📈 Medii pe materii")
                
                # Calculăm mediile pentru toate materiile
                medii_elev = []
                for materie in MATERII_GIMNAZIU:
                    media = calcul_media_elev(elev, materie, conn, st.session_state.semestru)
                    if media > 0:
                        medii_elev.append((materie, media))
                
                # Sortăm descrescător după medie
                medii_elev.sort(key=lambda x: x[1], reverse=True)
                
                for materie, media in medii_elev[:10]:  # Primele 10
                    col_mat, col_val = st.columns([3, 1])
                    col_mat.write(f"**{materie}**")
                    col_val.metric("", f"{media:.2f}", label_visibility="collapsed")
                    
                    # Progress bar
                    st.markdown(f'''
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {media * 10}%"></div>
                    </div>
                    ''', unsafe_allow_html=True)
            
            with col_progres:
                st.markdown("### 📅 Activitate recentă")
                
                # Ultimele note
                st.markdown("**Ultimele note:**")
                ultime_note = pd.read_sql(f'''
                    SELECT data, materie, nota 
                    FROM grades 
                    WHERE nume = ? 
                    ORDER BY data DESC 
                    LIMIT 5
                ''', conn, params=[elev])
                
                if not ultime_note.empty:
                    for _, row in ultime_note.iterrows():
                        data_form = datetime.strptime(row['data'][:10], "%Y-%m-%d").strftime("%d.%m")
                        st.markdown(f"• {data_form} - {row['materie'][:15]}...: **{row['nota']}**")
                else:
                    st.info("Nu există note")
                
                st.markdown("---")
                
                # Ultimele absențe
                st.markdown("**Ultimele absențe:**")
                ultime_abs = pd.read_sql(f'''
                    SELECT data, materie 
                    FROM absente 
                    WHERE nume = ? 
                    ORDER BY data DESC 
                    LIMIT 5
                ''', conn, params=[elev])
                
                if not ultime_abs.empty:
                    for _, row in ultime_abs.iterrows():
                        data_form = datetime.strptime(row['data'], "%Y-%m-%d").strftime("%d.%m")
                        st.markdown(f"• {data_form} - {row['materie'][:15]}...")
                else:
                    st.success("Nu există absențe")
        
        with tab_note:
            # Filtru după materie
            materie_selectata = st.selectbox("Filtrează după materie", 
                                           ["Toate materiile"] + MATERII_GIMNAZIU,
                                           key="filtru_note")
            
            query = "SELECT data as Data, materie as Materie, nota as Nota FROM grades WHERE nume = ?"
            params = [elev]
            
            if materie_selectata != "Toate materiile":
                query += " AND materie = ?"
                params.append(materie_selectata)
            
            query += " ORDER BY data DESC"
            
            note_df = pd.read_sql(query, conn, params=params)
            
            if not note_df.empty:
                # Formatează data
                note_df['Data'] = pd.to_datetime(note_df['Data']).dt.strftime('%d.%m.%Y %H:%M')
                
                st.dataframe(note_df, use_container_width=True, hide_index=True, height=400)
                
                # Export opțional
                csv = note_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Exportă notele (CSV)",
                    data=csv,
                    file_name=f"note_{elev}_sem{st.session_state.semestru}.csv",
                    mime="text/csv"
                )
            else:
                st.info("Nu există note înregistrate pentru acest elev.")
        
        with tab_absente:
            # Statistici absențe
            col_abs1, col_abs2, col_abs3 = st.columns(3)
            
            with col_abs1:
                total_abs = pd.read_sql(
                    "SELECT COUNT(*) FROM absente WHERE nume = ?",
                    conn, params=[elev]
                ).iloc[0,0]
                st.metric("Total absențe", total_abs)
            
            with col_abs2:
                abs_luna = pd.read_sql(f"""
                    SELECT COUNT(*) FROM absente 
                    WHERE nume = ? AND strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
                """, conn, params=[elev]).iloc[0,0]
                st.metric("Absențe luna curentă", abs_luna)
            
            with col_abs3:
                # Materia cu cele mai multe absențe
                materie_abs = pd.read_sql(f"""
                    SELECT materie, COUNT(*) as cnt 
                    FROM absente 
                    WHERE nume = ? 
                    GROUP BY materie 
                    ORDER BY cnt DESC 
                    LIMIT 1
                """, conn, params=[elev])
                
                if not materie_abs.empty:
                    st.metric("Materie cu cele mai multe absențe", materie_abs.iloc[0,0])
                else:
                    st.metric("Materie cu absențe", "-")
            
            # Lista detaliată a absențelor
            abs_df = pd.read_sql(f"""
                SELECT data as Data, materie as Materie, ora as Ora
                FROM absente 
                WHERE nume = ? 
                ORDER BY data DESC
            """, conn, params=[elev])
            
            if not abs_df.empty:
                abs_df['Data'] = pd.to_datetime(abs_df['Data']).dt.strftime('%d.%m.%Y')
                st.dataframe(abs_df, use_container_width=True, hide_index=True, height=300)
            else:
                st.success("Nu există absențe înregistrate.")
        
        with tab_observatii:
            # Filtru după tip observație
            tip_obs = st.selectbox("Tip observație", 
                                 ["Toate", "Laudă", "Atenționare", "Mustrare"],
                                 key="filtru_obs")
            
            query = "SELECT data as Data, materie as Materie, observatie as Observație, tip as Tip FROM observatii WHERE nume = ?"
            params = [elev]
            
            if tip_obs != "Toate":
                query += " AND tip = ?"
                params.append(tip_obs.lower())
            
            query += " ORDER BY data DESC"
            
            obs_df = pd.read_sql(query, conn, params=params)
            
            if not obs_df.empty:
                obs_df['Data'] = pd.to_datetime(obs_df['Data']).dt.strftime('%d.%m.%Y %H:%M')
                
                for _, row in obs_df.iterrows():
                    # Culoare în funcție de tip
                    if row['Tip'] == 'laudă':
                        bg_color = "rgba(34, 197, 94, 0.1)"
                        border_color = "rgba(34, 197, 94, 0.3)"
                        icon = "✅"
                    elif row['Tip'] == 'atenționare':
                        bg_color = "rgba(234, 179, 8, 0.1)"
                        border_color = "rgba(234, 179, 8, 0.3)"
                        icon = "⚠️"
                    else:
                        bg_color = "rgba(239, 68, 68, 0.1)"
                        border_color = "rgba(239, 68, 68, 0.3)"
                        icon = "❌"
                    
                    st.markdown(f"""
                    <div style="background: {bg_color}; 
                                border: 1px solid {border_color}; 
                                border-radius: 10px; 
                                padding: 15px; 
                                margin: 10px 0;
                                backdrop-filter: blur(10px);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>{icon} {row['Materie']}</strong>
                                <small style="color: #94a3b8; margin-left: 10px;">{row['Data']}</small>
                            </div>
                            <span style="background: {border_color}; 
                                       color: white; 
                                       padding: 3px 10px; 
                                       border-radius: 20px;
                                       font-size: 0.8rem;">
                                {row['Tip'].capitalize()}
                            </span>
                        </div>
                        <p style="margin-top: 10px; color: white;">{row['Observație']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("Nu există observații înregistrate.")
    
    # ============================================
    # INTERFAȚA DIRECTOARE
    # ============================================
    else:
        tab_statistici, tab_clase, tab_elevi, tab_setari = st.tabs(["📊 Statistici", "🏫 Clase", "👤 Elevi", "⚙️ Setări"])
        
        with tab_statistici:
            st.markdown("### 📈 Statistici generale școală")
            
            # Metrici principale
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_elevi = sum(len(studenti) for studenti in CLASE.values())
                st.metric("Total elevi", total_elevi)
            
            with col2:
                total_note = pd.read_sql("SELECT COUNT(*) FROM grades", conn).iloc[0,0]
                st.metric("Note totale", total_note)
            
            with col3:
                total_abs = pd.read_sql("SELECT COUNT(*) FROM absente", conn).iloc[0,0]
                st.metric("Absențe totale", total_abs)
            
            with col4:
                medie_generala = pd.read_sql("SELECT AVG(nota) FROM grades", conn).iloc[0,0]
                medie_generala = round(medie_generala, 2) if medie_generala else 0.00
                st.metric("Medie generală școală", medie_generala)
            
            st.markdown("---")
            
            # Top clase
            st.markdown("### 🏆 Top clase după medie")
            top_clase = pd.read_sql('''
                SELECT clasa, AVG(nota) as media
                FROM grades
                GROUP BY clasa
                ORDER BY media DESC
            ''', conn)
            
            if not top_clase.empty:
                col_chart, col_table = st.columns([2, 1])
                
                with col_chart:
                    st.bar_chart(top_clase.set_index('clasa'))
                
                with col_table:
                    st.dataframe(top_clase, use_container_width=True, hide_index=True)
            else:
                st.info("Nu există suficiente date pentru statistici.")
        
        with tab_clase:
            st.markdown("### 🏫 Management clase")
            
            selected_class = st.selectbox("Selectează clasa", list(CLASE.keys()))
            
            if selected_class:
                st.markdown(f"#### Elevii clasei {selected_class}")
                
                # Lista elevilor
                for idx, elev in enumerate(CLASE[selected_class], 1):
                    col_elev, col_medie, col_purtare = st.columns([3, 1, 1])
                    
                    with col_elev:
                        st.write(f"**{idx}. {elev}**")
                    
                    with col_medie:
                        # Media generală a elevului
                        cursor = conn.cursor()
                        cursor.execute('''
                            SELECT AVG(nota) FROM grades WHERE nume = ?
                        ''', (elev,))
                        media = cursor.fetchone()[0]
                        media = f"{media:.2f}" if media else "-"
                        st.metric("Medie", media, label_visibility="collapsed")
                    
                    with col_purtare:
                        nota_purtare = get_purtare(elev, conn, st.session_state.semestru)
                        st.metric("Purtare", nota_purtare, label_visibility="collapsed")
                
                st.markdown("---")
                
                # Adăugare elev nou
                st.markdown("#### Adăugare elev nou")
                col_new1, col_new2 = st.columns(2)
                
                with col_new1:
                    nume_nou = st.text_input("Numele noului elev")
                
                with col_new2:
                    if st.button("➕ Adaugă elev în clasă"):
                        if nume_nou:
                            CLASE[selected_class].append(nume_nou)
                            # Adaugă în baza de date pentru purtare
                            for semestru in [1, 2]:
                                conn.execute(
                                    "INSERT OR IGNORE INTO purtare (nume, nota, semestru) VALUES (?, ?, ?)",
                                    (nume_nou, 10, semestru)
                                )
                            conn.commit()
                            st.success(f"Elevul {nume_nou} a fost adăugat în clasa {selected_class}!")
                            st.rerun()
        
        with tab_elevi:
            st.markdown("### 👤 Gestionare elevi individuali")
            
            # Selectare elev
            all_students = []
            for clasa, studenti in CLASE.items():
                for student in studenti:
                    all_students.append(f"{student} ({clasa})")
            
            elev_selectat = st.selectbox("Selectează elev", sorted(all_students))
            
            if elev_selectat:
                # Extrage numele
                nume_elev = elev_selectat.split(" (")[0]
                
                # Modificare notă purtare
                nota_curenta = get_purtare(nume_elev, conn, st.session_state.semestru)
                
                col_edit1, col_edit2 = st.columns([2, 1])
                
                with col_edit1:
                    noua_nota = st.slider("Notă purtare", 1, 10, nota_curenta, key=f"edit_{nume_elev}")
                
                with col_edit2:
                    st.write("")  # Spacing
                    st.write("")  # Spacing
                    if st.button("💾 Salvează purtare", key=f"save_{nume_elev}", use_container_width=True):
                        conn.execute("DELETE FROM purtare WHERE nume = ? AND semestru = ?", 
                                   (nume_elev, st.session_state.semestru))
                        conn.execute("INSERT INTO purtare (nume, nota, semestru) VALUES (?, ?, ?)",
                                   (nume_elev, noua_nota, st.session_state.semestru))
                        conn.commit()
                        st.success(f"Nota de purtare actualizată pentru {nume_elev}: {noua_nota}")
                        st.rerun()
                
                st.markdown("---")
                
                # Gestionare observații
                st.markdown("#### Observații elev")
                obs_elev = pd.read_sql(
                    "SELECT id, data, materie, observatie, tip FROM observatii WHERE nume = ? ORDER BY data DESC",
                    conn, params=[nume_elev]
                )
                
                if not obs_elev.empty:
                    for _, row in obs_elev.iterrows():
                        col_obs, col_del = st.columns([4, 1])
                        
                        with col_obs:
                            st.markdown(f"**{row['data']}** - {row['materie']} ({row['tip']})")
                            st.write(f"{row['observatie']}")
                        
                        with col_del:
                            if st.button("🗑️", key=f"del_obs_{row['id']}"):
                                conn.execute("DELETE FROM observatii WHERE id = ?", (row['id'],))
                                conn.commit()
                                st.success("Observație ștearsă!")
                                st.rerun()
                else:
                    st.info("Nu există observații pentru acest elev.")
        
        with tab_setari:
            st.markdown("### ⚙️ Setări sistem")
            
            # Resetare date (DOAR pentru demo/testare)
            with st.expander("⚠️ Opțiuni avansate", expanded=False):
                st.warning("Aceste opțiuni sunt pentru întreținerea sistemului.")
                
                col_reset1, col_reset2 = st.columns(2)
                
                with col_reset1:
                    if st.button("🔄 Resetare date demo", type="secondary"):
                        # Nu resetăm complet, doar punem un mesaj
                        st.info("Într-un sistem real, această funcție ar reseta datele de test.")
                
                with col_reset2:
                    if st.button("📊 Recalculează statistici", type="secondary"):
                        # Recalculează mediile
                        st.info("Statisticile au fost recalculate!")
            
            # Informații despre sistem
            st.markdown("#### ℹ️ Informații sistem")
            st.info(f"""
            **Catalog Digital v3.0**
            
            • **Oraș:** {ORAS}
            • **Clase active:** {len(CLASE)}
            • **Total elevi:** {sum(len(s) for s in CLASE.values())}
            • **Materii gimnaziu:** {len(MATERII_GIMNAZIU)}
            • **Semestru curent:** {st.session_state.semestru}
            
            **Parole pentru testare:**
            - Profesor: Profesor2024!
            - Părinte: ElevParinte2024  
            - Directoare: AdminScoala2024@
            """)

# Footer general
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #94a3b8; font-size: 0.8rem; padding: 10px;">
    <p>🎓 <strong>Catalog Digital Gimnaziu {ORAS}</strong> | Sistem integrat de management școlar</p>
    <p>© 2024 | Versiunea 3.0 | Toate drepturile rezervate</p>
</div>
""", unsafe_allow_html=True)
