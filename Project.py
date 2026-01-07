

import streamlit as st import sqlite3 import pandas as pd from datetime import datetime, date, timedelta import hashlib # 1. Configurare Pagina st.set_page_config( page_title="Catalog Digital", page_icon="🎓", layout="wide", initial_sidebar_state="expanded" ) # 2. C

pasted

This is my code can you  adjust a little because the app has  bugs

21:19
I'll analyze your code and fix the bugs. Here are the main issues I found and their solutions:

Catalog Digital - Bug Fixes
Code 
Continue

21:22
I've identified and fixed several critical bugs in your code:

Main Bugs Fixed:
Session State Initialization - Added proper individual initialization for each session variable to prevent KeyError exceptions
Date Object Conversion - Fixed the date_input issue by converting the string date back to a date object
Database Error Handling - Added try-except blocks for IntegrityError when inserting duplicate entries
Float Conversion - Fixed nota_noua default value by converting to float for the number_input
Database Connection - Used @st.cache_resource for database initialization to prevent connection issues
Logout Function - Improved the logout to properly clear all session state keys
SQL Query Date Filtering - Fixed date comparison in SQL queries to use proper date strings
The code should now run without errors. The main improvements ensure:

No more KeyError exceptions
Proper date handling throughout the app
Better database error handling
Smoother state management during navigation
Test the app and let me know if you encounter any other issues!

File "/mount/src/catalog-digital/Project.py", line 624
                  st.download_button(
                                    ^
SyntaxError: '(' was never closed

21:24
Catalog Digital - Bug Fixes
Code ∙ Version 2 


Want to be notified when Claude responds?



Claude is AI and can make mistakes. Please double-check responses.
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
import hashlib

# 1. Configurare Pagina
st.set_page_config(
    page_title="Catalog Digital", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS modern
st.markdown("""
    <style>
    * { box-sizing: border-box; }
    
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh !important;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
    }
    
    footer, #MainMenu, header { visibility: hidden !important; }
    
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 20px 15px !important;
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stat-value {
        color: white !important;
        font-size: 1.8rem !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
    }
    
    .date-selector {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
    }
    
    .current-selection {
        background: rgba(59, 130, 246, 0.2) !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
    }
    
    .warning-box {
        background: rgba(234, 179, 8, 0.1) !important;
        border: 1px solid rgba(234, 179, 8, 0.3) !important;
        border-radius: 8px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# 3. Parole individuale
PROFESORI = {
    "Popescu Maria": {
        "materie": "Matematică",
        "parola_hash": hashlib.sha256("ProfPopescu2026@".encode()).hexdigest()
    },
    "Ionescu Ion": {
        "materie": "Limba și literatura română",
        "parola_hash": hashlib.sha256("ProfIonescu2026@".encode()).hexdigest()
    },
    "Georgescu Ana": {
        "materie": "Informatică și TIC",
        "parola_hash": hashlib.sha256("ProfGeorgescu2026@".encode()).hexdigest()
    },
    "Marinescu Dan": {
        "materie": "Biologie",
        "parola_hash": hashlib.sha256("ProfMarinescu2026@".encode()).hexdigest()
    }
}

ELEVI = {
    "Albert": "Albert2026#",
    "Alexandru": "Alexandru2026#",
    "Alissa": "Alissa2026#",
    "Andrei G.": "AndreiG2026#",
    "Andrei C.": "AndreiC2026#",
    "Ayan": "Ayan2026#",
    "Beatrice": "Beatrice2026#",
    "Bianca": "Bianca2026#",
    "Bogdan": "Bogdan2026#",
    "David Costea": "David2026#",
    "Eduard": "Eduard2026#",
    "Erika": "Erika2026#",
    "Giulia": "Giulia2026#",
    "Ines": "Ines2026#",
    "Karina": "Karina2026#",
    "Luca": "Luca2026#",
    "Mara": "Mara2026#",
    "Maria": "Maria2026#",
    "Marius": "Marius2026#",
    "Mihnea": "Mihnea2026#",
    "Natalia": "Natalia2026#",
    "Raisa": "Raisa2026#",
    "Rares Andro": "RaresA2026#",
    "Rares Volintiru": "RaresV2026#",
    "Yanis": "Yanis2026#",
    "Ionescu Maria": "IonescuM2026#",
    "Popescu Dan": "PopescuD2026#"
}

PAROLA_DIRECTOARE = hashlib.sha256("Directoare2026@".encode()).hexdigest()

MATERII_GIMNAZIU = [
    "Limba și literatura română", "Matematică", "Limba engleză", "Limba franceză",
    "Limba germană", "Istorie", "Geografie", "Biologie", "Fizică", "Chimie",
    "Educație fizică și sport", "Educație plastică", "Educație muzicală",
    "Educație tehnologică", "Informatică și TIC", "Religie", "Consiliere și orientare"
]

@st.cache_resource
def init_db():
    conn = sqlite3.connect('catalog_2026.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data DATE,
        clasa TEXT,
        nume TEXT,
        materie TEXT,
        nota REAL,
        profesor TEXT,
        UNIQUE(data, nume, materie)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS absente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data DATE,
        clasa TEXT,
        nume TEXT,
        materie TEXT,
        UNIQUE(data, nume, materie)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS observatii (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data DATE,
        nume TEXT,
        materie TEXT,
        observatie TEXT,
        profesor TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS purtare (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nume TEXT UNIQUE,
        nota INTEGER DEFAULT 10,
        semestru INTEGER DEFAULT 1
    )''')
    
    conn.commit()
    return conn

def verify_password(password, role, username=None):
    if role == "teacher" and username:
        return PROFESORI.get(username, {}).get("parola_hash") == hashlib.sha256(password.encode()).hexdigest()
    elif role == "parent" and username:
        return ELEVI.get(username) == password
    elif role == "admin":
        return hashlib.sha256(password.encode()).hexdigest() == PAROLA_DIRECTOARE
    return False

def elev_are_absenta(data_str, nume_elev, materie, conn):
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM absente WHERE data = ? AND nume = ? AND materie = ?', 
                   (data_str, nume_elev, materie))
    return cursor.fetchone() is not None

def get_note_elev(data_str, nume_elev, materie, conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, nota FROM grades WHERE data = ? AND nume = ? AND materie = ?', 
                   (data_str, nume_elev, materie))
    return cursor.fetchall()

def delete_nota(nota_id, conn):
    conn.execute("DELETE FROM grades WHERE id = ?", (nota_id,))
    conn.commit()

def update_nota(nota_id, noua_nota, conn):
    conn.execute("UPDATE grades SET nota = ? WHERE id = ?", (noua_nota, nota_id))
    conn.commit()

def get_media_elev(nume_elev, materie, conn):
    cursor = conn.cursor()
    cursor.execute('SELECT AVG(nota) FROM grades WHERE nume = ? AND materie = ?', 
                   (nume_elev, materie))
    result = cursor.fetchone()
    return round(result[0], 2) if result and result[0] else 0.00

def init_purtare(conn):
    cursor = conn.cursor()
    for elev in ELEVI.keys():
        cursor.execute("INSERT OR IGNORE INTO purtare (nume, nota) VALUES (?, ?)", (elev, 10))
    conn.commit()

conn = init_db()
init_purtare(conn)

CLASE = {
    "6B": [e for e in ELEVI.keys() if e not in ["Ionescu Maria", "Popescu Dan"]],
    "7A": ["Ionescu Maria", "Popescu Dan"]
}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'materie' not in st.session_state:
    st.session_state.materie = None
if 'nume_elev' not in st.session_state:
    st.session_state.nume_elev = None
if 'clasa_selectata' not in st.session_state:
    st.session_state.clasa_selectata = "6B"
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.now().strftime("%Y-%m-%d")

def display_current_selection():
    if st.session_state.role == "teacher":
        st.markdown(f"""
        <div class="current-selection">
            <strong>👨‍🏫 Profesor:</strong> {st.session_state.username}<br>
            <strong>📚 Materie:</strong> {st.session_state.materie}<br>
            <strong>🏫 Clasă:</strong> {st.session_state.clasa_selectata}<br>
            <strong>📅 Data selectată:</strong> {st.session_state.selected_date}
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.role == "parent":
        st.markdown(f"""
        <div class="current-selection">
            <strong>👤 Elev:</strong> {st.session_state.nume_elev}<br>
            <strong>🏫 Clasă:</strong> {st.session_state.clasa_selectata}<br>
            <strong>📅 Data curentă:</strong> {datetime.now().strftime("%d.%m.%Y")}
        </div>
        """, unsafe_allow_html=True)

# LOGIN PAGE
if not st.session_state.logged_in:
    st.markdown("""
    <div style="text-align: center; padding: 30px 0;">
        <h1 style="color: white; font-size: 2.5rem;">🎓 Catalog Digital 2026</h1>
        <p style="color: #94a3b8; font-size: 1.2rem;">Anul școlar 2025-2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("ℹ️ Informații autentificare", expanded=False):
        st.info("""
        **Parole pentru testare (2026):**
        
        **Profesori:**
        - Popescu Maria: ProfPopescu2026@
        - Ionescu Ion: ProfIonescu2026@
        - Georgescu Ana: ProfGeorgescu2026@
        - Marinescu Dan: ProfMarinescu2026@
        
        **Elevi/Părinți:** NumeElev2026# (ex: Albert2026#)
        
        **Directoare:** Directoare2026@
        """)
    
    tab_prof, tab_parinte, tab_directoare = st.tabs(["👨‍🏫 Profesor", "👪 Părinte", "🏛️ Directoare"])
    
    with tab_prof:
        st.subheader("Autentificare Profesor")
        profesor_selectat = st.selectbox("Selectează numele tău", list(PROFESORI.keys()), key="login_profesor")
        parola = st.text_input("Introdu parola ta", type="password", key="parola_prof")
        
        if st.button("Accesează platforma", type="primary", use_container_width=True):
            if parola and verify_password(parola, "teacher", profesor_selectat):
                st.session_state.logged_in = True
                st.session_state.role = "teacher"
                st.session_state.username = profesor_selectat
                st.session_state.materie = PROFESORI[profesor_selectat]["materie"]
                st.success(f"Bine ai venit, profesorule {profesor_selectat}!")
                st.rerun()
            else:
                st.error("Parolă incorectă!")
    
    with tab_parinte:
        st.subheader("Autentificare Părinte")
        all_students = []
        for clasa, studenti in CLASE.items():
            for student in studenti:
                all_students.append(f"{student} ({clasa})")
        
        elev_selectat = st.selectbox("Selectează elevul", sorted(all_students), key="login_elev")
        nume_elev = elev_selectat.split(" (")[0]
        clasa_elev = elev_selectat.split(" (")[1].replace(")", "")
        parola_parinte = st.text_input("Parolă elev/părinte", type="password", key="parola_parinte")
        
        if st.button("Vezi situația elevului", type="primary", use_container_width=True):
            if parola_parinte and verify_password(parola_parinte, "parent", nume_elev):
                st.session_state.logged_in = True
                st.session_state.role = "parent"
                st.session_state.nume_elev = nume_elev
                st.session_state.clasa_selectata = clasa_elev
                st.success(f"Bine ai venit, părinte al lui {nume_elev}!")
                st.rerun()
            else:
                st.error("Parolă incorectă!")
    
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
                st.error("Cod incorect!")

# MAIN PAGE
else:
    col_title, col_logout = st.columns([4, 1])
    
    with col_title:
        if st.session_state.role == "teacher":
            st.markdown(f"<h2>👨‍🏫 Profesor {st.session_state.username}</h2>", unsafe_allow_html=True)
        elif st.session_state.role == "parent":
            st.markdown(f"<h2>👪 Părinte - {st.session_state.nume_elev}</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2>🏛️ Panou Directoare</h2>", unsafe_allow_html=True)
    
    with col_logout:
        if st.button("🚪 Deconectare", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    display_current_selection()
    
    # TEACHER INTERFACE
    if st.session_state.role == "teacher":
        st.markdown("---")
        menu_options = ["📝 Adaugă note/absente", "📊 Vezi note existente", "✏️ Modifică/șterge note"]
        selected_menu = st.radio("Alege acțiunea:", menu_options, horizontal=True, key="prof_menu")
        
        clasa = st.selectbox("Selectează clasa", list(CLASE.keys()), key="prof_clasa")
        if clasa != st.session_state.clasa_selectata:
            st.session_state.clasa_selectata = clasa
        
        st.markdown("### 📅 Selectează data")
        col_cal1, col_cal2 = st.columns([2, 1])
        
        with col_cal1:
            current_date = datetime.strptime(st.session_state.selected_date, "%Y-%m-%d").date()
            selected_date = st.date_input(
                "Alege data",
                value=current_date,
                min_value=date(2025, 9, 1),
                max_value=date(2026, 6, 30),
                key="calendar_date"
            )
            data_str = selected_date.strftime("%Y-%m-%d")
            if data_str != st.session_state.selected_date:
                st.session_state.selected_date = data_str
        
        with col_cal2:
            st.markdown(f"""
            <div class="date-selector">
                <h4>📅 Data selectată:</h4>
                <h3>{selected_date.strftime('%d.%m.%Y')}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("#### 📅 Săptămâna curentă")
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        
        col_cal = st.columns(7)
        days_of_week = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
        
        for i, (day_name, col) in enumerate(zip(days_of_week, col_cal)):
            day_date = start_of_week + timedelta(days=i)
            with col:
                is_today = day_date == today
                is_selected = day_date == selected_date
                
                if is_selected:
                    col.markdown(f"""
                    <div style="text-align: center; background-color: #3b82f6; 
                                color: white; padding: 5px; border-radius: 5px; margin: 2px;">
                        <div><strong>{day_name[:3]}</strong></div>
                        <div><strong>{day_date.day}</strong></div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    col.markdown(f"""
                    <div style="text-align: center; background-color: {'#f0f2f6' if is_today else '#2d3748'}; 
                                color: {'black' if is_today else 'white'}; padding: 5px; border-radius: 5px; margin: 2px;">
                        <div>{day_name[:3]}</div>
                        <div>{day_date.day}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if st.button("✓", key=f"quick_select_{i}", help=f"Selectează {day_date.strftime('%d.%m')}"):
                    st.session_state.selected_date = day_date.strftime("%Y-%m-%d")
                    st.rerun()
        
        search_query = st.text_input("🔍 Caută elev...", key="search_elev")
        elevi_filtrati = [e for e in CLASE[clasa] if search_query.lower() in e.lower()] if search_query else CLASE[clasa]
        
        st.markdown(f"### 👥 Elevi - {len(elevi_filtrati)} total")
        
        if selected_menu == "📝 Adaugă note/absente":
            for elev in elevi_filtrati:
                with st.expander(f"👤 {elev}", expanded=False):
                    are_absenta = elev_are_absenta(data_str, elev, st.session_state.materie, conn)
                    
                    if are_absenta:
                        st.warning(f"⚠️ {elev} are deja absență la {st.session_state.materie} în data de {selected_date.strftime('%d.%m.%Y')}")
                        st.markdown("**Nu se poate adăuga notă când elevul este absent!**")
                        
                        if st.button(f"🗑️ Șterge absența", key=f"del_abs_{elev}", type="secondary"):
                            conn.execute('DELETE FROM absente WHERE data = ? AND nume = ? AND materie = ?',
                                       (data_str, elev, st.session_state.materie))
                            conn.commit()
                            st.success(f"Absența pentru {elev} a fost ștearsă!")
                            st.rerun()
                    else:
                        note_existente = get_note_elev(data_str, elev, st.session_state.materie, conn)
                        
                        if note_existente:
                            st.info(f"📝 {elev} are deja notă în această zi: {note_existente[0][1]}")
                            col_mod, col_del = st.columns(2)
                            
                            with col_mod:
                                nota_noua = st.number_input("Notă nouă", 1.0, 10.0, float(note_existente[0][1]), 0.5, 
                                                          key=f"mod_nota_{elev}")
                                if st.button("✏️ Modifică nota", key=f"mod_btn_{elev}"):
                                    update_nota(note_existente[0][0], nota_noua, conn)
                                    st.success(f"Nota pentru {elev} a fost modificată în {nota_noua}!")
                                    st.rerun()
                            
                            with col_del:
                                if st.button("🗑️ Șterge nota", key=f"del_btn_{elev}", type="secondary"):
                                    delete_nota(note_existente[0][0], conn)
                                    st.success(f"Nota pentru {elev} a fost ștearsă!")
                                    st.rerun()
                        else:
                            col_nota, col_abs = st.columns(2)
                            
                            with col_nota:
                                nota_noua = st.number_input("Notă", 1.0, 10.0, 8.0, 0.5, key=f"nota_{elev}")
                                if st.button("📝 Adaugă notă", key=f"add_nota_{elev}"):
                                    try:
                                        conn.execute('''INSERT INTO grades (data, clasa, nume, materie, nota, profesor) 
                                                       VALUES (?, ?, ?, ?, ?, ?)''',
                                                    (data_str, clasa, elev, st.session_state.materie, nota_noua, st.session_state.username))
                                        conn.commit()
                                        st.success(f"Nota {nota_noua} adăugată pentru {elev}!")
                                        st.rerun()
                                    except sqlite3.IntegrityError:
                                        st.error("Nota există deja pentru această zi!")
                            
                            with col_abs:
                                if st.button("❌ Marchează absent", key=f"abs_{elev}", type="secondary"):
                                    try:
                                        conn.execute('INSERT INTO absente (data, clasa, nume, materie) VALUES (?, ?, ?, ?)',
                                                    (data_str, clasa, elev, st.session_state.materie))
                                        conn.commit()
                                        st.warning(f"{elev} marcat absent!")
                                        st.rerun()
                                    except sqlite3.IntegrityError:
                                        st.error("Absența există deja!")
        
        elif selected_menu == "📊 Vezi note existente":
            st.markdown(f"### 📋 Note existente - {st.session_state.materie}")
            
            col_filtru1, col_filtru2 = st.columns(2)
            with col_filtru1:
                filtru_data = st.selectbox("Filtrează după dată",
                    ["Toate datele", "Azi", "Ultima săptămână", "Ultima lună", "Data specifică"],
                    key="filtru_data")
            
            query = 'SELECT data, nume, nota FROM grades WHERE clasa = ? AND materie = ?'
            params = [clasa, st.session_state.materie]
            
            if filtru_data == "Azi":
                query += " AND data = ?"
                params.append(date.today().strftime("%Y-%m-%d"))
            elif filtru_data == "Ultima săptămână":
                query += " AND data >= ?"
                params.append((date.today() - timedelta(days=7)).strftime("%Y-%m-%d"))
            elif filtru_data == "Ultima lună":
                query += " AND data >= ?"
                params.append((date.today() - timedelta(days=30)).strftime("%Y-%m-%d"))
            elif filtru_data == "Data specifică":
                with col_filtru2:
                    specific_date = st.date_input("Selectează data", value=date.today())
                    query += " AND data = ?"
                    params.append(specific_date.strftime("%Y-%m-%d"))
            
            query += " ORDER BY data DESC, nume"
            note_df = pd.read_sql(query, conn, params=params)
            
            if not note_df.empty:
                note_df['data'] = pd.to_datetime(note_df['data']).dt.strftime('%d.%m.%Y')
                
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("📊 Media clasei", f"{note_df['nota'].mean():.2f}")
                with col_stat2:
                    st.metric("🏆 Nota maximă", f"{note_df['nota'].max():.2f}")
                with col_stat3:
                    st.metric("📉 Nota minimă", f"{note_df['nota'].min():.2f}")
                
                st.dataframe(note_df, use_container_width=True, hide_index=True, height=400)
                
                csv = note_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Exportă notele",
                    data=csv,
                    file_name=f"note_{clasa}_{st.session_state.materie}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("Nu există note înregistrate pentru această clasă și materie.")
        
        elif selected_menu == "✏️ Modifică/șterge note":
            st.markdown("### ✏️ Management note existente")
            
            col_search1, col_search2 = st.columns(2)
            with col_search1:
                search_elev = st.selectbox("Caută după elev", [""] + CLASE[clasa], key="search_note_elev")
            with col_search2:
                search_date = st.date_input("Caută după dată", value=None, key="search_note_date")
            
            query = 'SELECT id, data, nume, nota FROM grades WHERE clasa = ? AND materie = ?'
            params = [clasa, st.session_state.materie]
            
            if search_elev:
                query += " AND nume = ?"
                params.append(search_elev)
            if search_date:
                query += " AND data = ?"
                params.append(search_date.strftime("%Y-%m-%d"))
            
            query += " ORDER BY data DESC"
            note_to_edit = pd.read_sql(query, conn, params=params)
            
            if not note_to_edit.empty:
                st.markdown(f"**Găsite {len(note_to_edit)} note:**")
                
                for _, row in note_to_edit.iterrows():
                    col_edit1, col_edit2, col_edit3, col_edit4 = st.columns([2, 1, 1, 1])
                    
                    with col_edit1:
                        st.write(f"**{row['nume']}** - {row['data']}")
                    with col_edit2:
                        st.metric("Nota", row['nota'], label_visibility="collapsed")
                    with col_edit3:
                        nota_noua = st.number_input("Noua notă", 1.0, 10.0, float(row['nota']), 0.5, 
                                                   key=f"edit_{row['id']}")
                    with col_edit4:
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn

