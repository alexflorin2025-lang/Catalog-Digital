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
    
    .success-box {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 8px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# 3. TOATE MATERIILE DE GIMNAZIU
MATERII_GIMNAZIU = [
    "Limba și literatura română",
    "Matematică",
    "Limba engleză",
    "Limba franceză",
    "Limba germană",
    "Limba spaniolă",
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
    "Consiliere și orientare"
]

# 4. PROFESORI - câte unul pentru fiecare materie
PROFESORI = {
    "Popescu Maria": {
        "materie": "Matematică",
        "parola_hash": hashlib.sha256("ProfPopescu2026@".encode()).hexdigest()
    },
    "Ionescu Ion": {
        "materie": "Limba și literatura română",
        "parola_hash": hashlib.sha256("ProfIonescu2026@".encode()).hexdigest()
    },
    "Vasilescu Elena": {
        "materie": "Limba engleză",
        "parola_hash": hashlib.sha256("ProfVasilescu2026@".encode()).hexdigest()
    },
    "Dumitrescu Andreea": {
        "materie": "Limba franceză",
        "parola_hash": hashlib.sha256("ProfDumitrescu2026@".encode()).hexdigest()
    },
    "Constantin Mihai": {
        "materie": "Limba germană",
        "parola_hash": hashlib.sha256("ProfConstantin2026@".encode()).hexdigest()
    },
    "Radu Alexandra": {
        "materie": "Limba spaniolă",
        "parola_hash": hashlib.sha256("ProfRadu2026@".encode()).hexdigest()
    },
    "Stanescu Vlad": {
        "materie": "Istorie",
        "parola_hash": hashlib.sha256("ProfStanescu2026@".encode()).hexdigest()
    },
    "Georgescu Ana": {
        "materie": "Geografie",
        "parola_hash": hashlib.sha256("ProfGeorgescu2026@".encode()).hexdigest()
    },
    "Marinescu Dan": {
        "materie": "Biologie",
        "parola_hash": hashlib.sha256("ProfMarinescu2026@".encode()).hexdigest()
    },
    "Popa Cristian": {
        "materie": "Fizică",
        "parola_hash": hashlib.sha256("ProfPopa2026@".encode()).hexdigest()
    },
    "Munteanu Ioana": {
        "materie": "Chimie",
        "parola_hash": hashlib.sha256("ProfMunteanu2026@".encode()).hexdigest()
    },
    "Badea Sorin": {
        "materie": "Educație fizică și sport",
        "parola_hash": hashlib.sha256("ProfBadea2026@".encode()).hexdigest()
    },
    "Ilie Carmen": {
        "materie": "Educație plastică",
        "parola_hash": hashlib.sha256("ProfIlie2026@".encode()).hexdigest()
    },
    "Stoica Gabriel": {
        "materie": "Educație muzicală",
        "parola_hash": hashlib.sha256("ProfStoica2026@".encode()).hexdigest()
    },
    "Nistor Radu": {
        "materie": "Educație tehnologică",
        "parola_hash": hashlib.sha256("ProfNistor2026@".encode()).hexdigest()
    },
    "Tudor Mihaela": {
        "materie": "Informatică și TIC",
        "parola_hash": hashlib.sha256("ProfTudor2026@".encode()).hexdigest()
    },
    "Diaconu Petru": {
        "materie": "Religie",
        "parola_hash": hashlib.sha256("ProfDiaconu2026@".encode()).hexdigest()
    },
    "Serban Laura": {
        "materie": "Consiliere și orientare",
        "parola_hash": hashlib.sha256("ProfSerban2026@".encode()).hexdigest()
    }
}

# 5. ELEVI
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

# 6. Parola directoare
PAROLA_DIRECTOARE = hashlib.sha256("Directoare2026@".encode()).hexdigest()

# 7. Initializare Baza de Date
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
        tip TEXT,
        profesor TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS purtare (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nume TEXT,
        nota INTEGER,
        data_modificare DATE,
        motiv TEXT,
        profesor TEXT
    )''')
    
    conn.commit()
    return conn

# 8. Funcții utilitare
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

def get_nota_purtare_curenta(nume_elev, conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nota FROM purtare 
        WHERE nume = ? 
        ORDER BY data_modificare DESC 
        LIMIT 1
    ''', (nume_elev,))
    result = cursor.fetchone()
    return result[0] if result else 10

def update_purtare(nume_elev, nota_noua, motiv, profesor, conn):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO purtare (nume, nota, data_modificare, motiv, profesor) 
        VALUES (?, ?, ?, ?, ?)
    ''', (nume_elev, nota_noua, datetime.now().date().strftime("%Y-%m-%d"), motiv, profesor))
    conn.commit()

def get_observatii_elev(nume_elev, conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT data, materie, observatie, tip, profesor 
        FROM observatii 
        WHERE nume = ? 
        ORDER BY data DESC
    ''', (nume_elev,))
    return cursor.fetchall()

def adauga_observatie(data_str, nume_elev, materie, observatie, tip, profesor, conn):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO observatii (data, nume, materie, observatie, tip, profesor) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data_str, nume_elev, materie, observatie, tip, profesor))
    conn.commit()

# 9. Setup baza de date
conn = init_db()

# 10. Clasele
CLASE = {
    "6B": [e for e in ELEVI.keys() if e not in ["Ionescu Maria", "Popescu Dan"]],
    "7A": ["Ionescu Maria", "Popescu Dan"]
}

# 11. Inițializare session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.materie = None
    st.session_state.nume_elev = None
    st.session_state.clasa_selectata = "6B"
    st.session_state.selected_date = datetime.now().strftime("%Y-%m-%d")

# 12. Funcții pentru afișare
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

# ============================================
# PAGINA DE LOGIN
# ============================================
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
        
        **Profesori:** ProfNumeProfesor2026@ (ex: ProfPopescu2026@)
        
        **Lista profesori și materii:**
        - Popescu Maria - Matematică
        - Ionescu Ion - Limba și literatura română
        - Vasilescu Elena - Limba engleză
        - Dumitrescu Andreea - Limba franceză
        - Constantin Mihai - Limba germană
        - Radu Alexandra - Limba spaniolă
        - Stanescu Vlad - Istorie
        - Georgescu Ana - Geografie
        - Marinescu Dan - Biologie
        - Popa Cristian - Fizică
        - Munteanu Ioana - Chimie
        - Badea Sorin - Educație fizică și sport
        - Ilie Carmen - Educație plastică
        - Stoica Gabriel - Educație muzicală
        - Nistor Radu - Educație tehnologică
        - Tudor Mihaela - Informatică și TIC
        - Diaconu Petru - Religie
        - Serban Laura - Consiliere și orientare
        
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

# ============================================
# PAGINA PRINCIPALĂ
# ============================================
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
    
    # ============================================
    # INTERFAȚA PROFESOR
    # ============================================
    if st.session_state.role == "teacher":
        st.markdown("---")
        menu_options = ["📝 Adaugă note/absente/observații", "📊 Vezi note existente", "✏️ Modifică/șterge note"]
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
        
        if selected_menu == "📝 Adaugă note/absente/observații":
            for elev in elevi_filtrati:
                with st.expander(f"👤 {elev}", expanded=False):
                    # ORDINEA NOUĂ: Note, Absențe, Observații, Purtare
                    
                    # 1. NOTE
                    st.markdown("#### 📝 Note")
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
                            col_nota, col_abs_btn = st.columns(2)
                            
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
                            
                            with col_abs_btn:
                                st.write("")  # Spacing
                                st.write("")
                    
                    st.markdown("---")
                    
                    # 2. ABSENȚE
                    st.markdown("#### ❌ Absențe")
                    if not are_absenta:
                        if st.button("❌ Marchează absent", key=f"abs_{elev}", use_container_width=True):
                            try:
                                conn.execute('INSERT INTO absente (data, clasa, nume, materie) VALUES (?, ?, ?, ?)',
                                            (data_str, clasa, elev, st.session_state.materie))
                                conn.commit()
                                st.warning(f"{elev} marcat absent!")
                                st.rerun()
                            except sqlite3.IntegrityError:
                                st.error("Absența există deja!")
                    else:
                        st.success("✅ Absență deja marcată pentru această zi")
                    
                    st.markdown("---")
                    
                    # 3. OBSERVAȚII
                    st.markdown("#### 📋 Observații")
                    observatie = st.text_area("Observație comportamentală", 
                                            placeholder="Scrie observația aici...",
                                            key=f"obs_{elev}",
                                            height=100)
                    
                    col_obs1, col_obs2, col_obs3 = st.columns(3)
                    
                    with col_obs1:
                        if st.button("👏 Laudă", key=f"lauda_{elev}", use_container_width=True):
                            if observatie.strip():
                                adauga_observatie(data_str, elev, st.session_state.materie, 
                                                observatie.strip(), "laudă", st.session_state.username, conn)
                                st.success(f"Laudă adăugată pentru {elev}!")
                                st.rerun()
                            else:
                                st.warning("Completează observația!")
                    
                    with col_obs2:
                        if st.button("⚠️ Atenționare", key=f"atentionare_{elev}", use_container_width=True):
                            if observatie.strip():
                                adauga_observatie(data_str, elev, st.session_state.materie, 
                                                observatie.strip(), "atenționare", st.session_state.username, conn)
                                st.warning(f"Atenționare adăugată pentru {elev}!")
                                st.rerun()
                            else:
                                st.warning("Completează observația!")
                    
                    with col_obs3:
                        if st.button("❌ Mustrare", key=f"mustrare_{elev}", use_container_width=True):
                            if observatie.strip():
                                adauga_observatie(data_str, elev, st.session_state.materie, 
                                                observatie.strip(), "mustrare", st.session_state.username, conn)
                                st.error(f"Mustrare adăugată pentru {elev}!")
                                st.rerun()
                            else:
                                st.warning("Completează observația!")
                    
                    st.markdown("---")
                    
                    # 4. PURTARE
                    st.markdown("#### ⭐ Purtare")
                    nota_purtare_curenta = get_nota_purtare_curenta(elev, conn)
                    st.write(f"**Nota curentă de purtare:** {nota_purtare_curenta}")
                    
                    col_purt1, col_purt2 = st.columns([2, 1])
                    
                    with col_purt1:
                        noua_nota_purtare = st.slider("Setează nota de purtare", 1, 10, nota_purtare_curenta,
                                                    key=f"purt_{elev}")
                        motiv_purtare = st.text_input("Motivul modificării", 
                                                    placeholder="Scrie motivul modificării...",
                                                    key=f"motiv_{elev}")
                    
                    with col_purt2:
                        st.write("")
                        st.write("")
                        if st.button("💾 Salvează purtare", key=f"save_purt_{elev}", use_container_width=True):
                            if motiv_purtare.strip():
                                update_purtare(elev, noua_nota_purtare, motiv_purtare.strip(), 
                                            st.session_state.username, conn)
                                st.success(f"Nota de purtare actualizată pentru {elev}: {noua_nota_purtare}")
                                st.rerun()
                            else:
                                st.error("Te rog completează motivul modificării!")
        
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
                    media = note_df['nota'].mean()
                    st.metric("📊 Media clasei", f"{media:.2f}" if not pd.isna(media) else "0.00")
                with col_stat2:
                    nota_max = note_df['nota'].max()
                    st.metric("🏆 Nota maximă", f"{nota_max:.2f}" if not pd.isna(nota_max) else "0.00")
                with col_stat3:
                    nota_min = note_df['nota'].min()
                    st.metric("📉 Nota minimă", f"{nota_min:.2f}" if not pd.isna(nota_min) else "0.00")
                
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
                        data_formatata = datetime.strptime(row['data'], "%Y-%m-%d").strftime("%d.%m.%Y")
                        st.write(f"**{row['nume']}** - {data_formatata}")
                    with col_edit2:
                        st.metric("Nota", row['nota'], label_visibility="collapsed")
                    with col_edit3:
                        nota_noua = st.number_input("Noua notă", 1.0, 10.0, float(row['nota']), 0.5, 
                                                   key=f"edit_{row['id']}")
                    with col_edit4:
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button("✏️", key=f"save_{row['id']}"):
                                update_nota(row['id'], nota_noua, conn)
                                st.success(f"Nota pentru {row['nume']} a fost actualizată!")
                                st.rerun()
                        with col_btn2:
                            if st.button("🗑️", key=f"delete_{row['id']}", type="secondary"):
                                delete_nota(row['id'], conn)
                                st.success(f"Nota pentru {row['nume']} a fost ștearsă!")
                                st.rerun()
            else:
                st.info("Nu s-au găsit note conform criteriilor de căutare.")
    
    # ============================================
    # INTERFAȚA PĂRINTE (ORDINEA NOUĂ)
    # ============================================
    elif st.session_state.role == "parent":
        elev = st.session_state.nume_elev
        clasa = st.session_state.clasa_selectata
        
        # ORDINEA NOUĂ: Note, Absențe, Observații, Medii, Purtare
        tab_note, tab_absente, tab_observatii, tab_medii, tab_purtare = st.tabs(
            ["📝 Note", "❌ Absențe", "📋 Observații", "📊 Medii", "⭐ Purtare"]
        )
        
        with tab_note:
            st.markdown("### 📝 Notele elevului")
            
            col_filtru1, col_filtru2 = st.columns(2)
            with col_filtru1:
                filtru_materie = st.selectbox("Materie", ["Toate"] + MATERII_GIMNAZIU, key="filtru_materie_parinte")
            
            with col_filtru2:
                filtru_luna = st.selectbox("Lună", 
                    ["Toate", "Septembrie", "Octombrie", "Noiembrie", "Decembrie", "Ianuarie", 
                     "Februarie", "Martie", "Aprilie", "Mai", "Iunie"], key="filtru_luna")
            
            query = 'SELECT data, materie, nota FROM grades WHERE nume = ?'
            params = [elev]
            
            if filtru_materie != "Toate":
                query += " AND materie = ?"
                params.append(filtru_materie)
            
            if filtru_luna != "Toate":
                luni = {
                    "Septembrie": "09", "Octombrie": "10", "Noiembrie": "11",
                    "Decembrie": "12", "Ianuarie": "01", "Februarie": "02",
                    "Martie": "03", "Aprilie": "04", "Mai": "05", "Iunie": "06"
                }
                query += " AND strftime('%m', data) = ?"
                params.append(luni[filtru_luna])
            
            query += " ORDER BY data DESC"
            note_df = pd.read_sql(query, conn, params=params)
            
            if not note_df.empty:
                note_df['data'] = pd.to_datetime(note_df['data']).dt.strftime('%d.%m.%Y')
                
                media_generala = note_df['nota'].mean().round(2)
                st.metric("🎓 Media generală", media_generala)
                
                st.dataframe(note_df, use_container_width=True, hide_index=True, height=300)
            else:
                st.info("Nu există note înregistrate.")
        
        with tab_absente:
            st.markdown("### ❌ Absențele elevului")
            
            absente_df = pd.read_sql('SELECT data, materie FROM absente WHERE nume = ? ORDER BY data DESC', 
                                   conn, params=[elev])
            
            if not absente_df.empty:
                col_abs1, col_abs2, col_abs3 = st.columns(3)
                
                with col_abs1:
                    total_abs = len(absente_df)
                    st.metric("Total absențe", total_abs)
                
                with col_abs2:
                    current_month = datetime.now().strftime("%Y-%m")
                    abs_luna = len(absente_df[absente_df['data'].str.startswith(current_month)])
                    st.metric("Această lună", abs_luna)
                
                with col_abs3:
                    if not absente_df.empty:
                        top_materie = absente_df['materie'].value_counts().index[0]
                        st.metric("Materie frecventă", top_materie[:15])
                
                absente_df['data'] = pd.to_datetime(absente_df['data']).dt.strftime('%d.%m.%Y')
                st.dataframe(absente_df, use_container_width=True, hide_index=True, height=300)
            else:
                st.success("✅ Nu există absențe înregistrate.")
        
        with tab_observatii:
            st.markdown("### 📋 Observații de la profesori")
            
            observatii = get_observatii_elev(elev, conn)
            
            if observatii:
                for obs in observatii:
                    data_obs, materie_obs, text_obs, tip_obs, prof_obs = obs
                    data_formatata = datetime.strptime(data_obs, "%Y-%m-%d").strftime("%d.%m.%Y")
                    
                    if tip_obs == "laudă":
                        st.markdown(f"""
                        <div class="success-box">
                            <strong>👏 Laudă - {data_formatata}</strong><br>
                            <strong>Profesor:</strong> {prof_obs} ({materie_obs})<br>
                            <strong>Observație:</strong> {text_obs}
                        </div>
                        """, unsafe_allow_html=True)
                    elif tip_obs == "mustrare":
                        st.markdown(f"""
                        <div class="warning-box">
                            <strong>❌ Mustrare - {data_formatata}</strong><br>
                            <strong>Profesor:</strong> {prof_obs} ({materie_obs})<br>
                            <strong>Observație:</strong> {text_obs}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="warning-box">
                            <strong>⚠️ Atenționare - {data_formatata}</strong><br>
                            <strong>Profesor:</strong> {prof_obs} ({materie_obs})<br>
                            <strong>Observație:</strong> {text_obs}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.success("✅ Nu există observații înregistrate.")
        
        with tab_medii:
            st.markdown("### 📈 Medii pe materii")
            
            medii_elev = []
            for materie in MATERII_GIMNAZIU:
                media = get_media_elev(elev, materie, conn)
                if media > 0:
                    medii_elev.append((materie, media))
            
            if medii_elev:
                medii_elev.sort(key=lambda x: x[1], reverse=True)
                
                for materie, media in medii_elev:
                    col_mat, col_val = st.columns([3, 1])
                    col_mat.write(f"**{materie}**")
                    col_val.metric("", f"{media:.2f}", label_visibility="collapsed")
                    
                    progres = int((media / 10) * 100)
                    st.progress(progres / 100)
            else:
                st.info("Elevul nu are note înregistrate.")
        
        with tab_purtare:
            st.markdown("### ⭐ Situația purtării")
            
            nota_curenta = get_nota_purtare_curenta(elev, conn)
            st.metric("Nota curentă de purtare", f"{nota_curenta}/10")
            
            istoric_purtare = pd.read_sql('''
                SELECT nota, data_modificare, motiv, profesor 
                FROM purtare 
                WHERE nume = ? 
                ORDER BY data_modificare DESC
            ''', conn, params=[elev])
            
            if not istoric_purtare.empty:
                st.markdown("#### 📊 Istoric modificări purtare")
                istoric_purtare['data_modificare'] = pd.to_datetime(istoric_purtare['data_modificare']).dt.strftime('%d.%m.%Y')
                st.dataframe(istoric_purtare, use_container_width=True, hide_index=True)
            else:
                st.info("Nu există modificări înregistrate pentru purtare.")
    
    # ============================================
    # INTERFAȚA DIRECTOARE
    # ============================================
    else:
        st.markdown("### 🏛️ Panou Administrativ")
        
        tab_statistici, tab_profesori, tab_elevi = st.tabs(["📊 Statistici", "👨‍🏫 Profesori", "👤 Elevi"])
        
        with tab_statistici:
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                total_elevi = sum(len(studenti) for studenti in CLASE.values())
                st.metric("Total elevi", total_elevi)
            
            with col_stat2:
                total_note = pd.read_sql("SELECT COUNT(*) FROM grades", conn).iloc[0,0]
                st.metric("Note totale", total_note)
            
            with col_stat3:
                total_abs = pd.read_sql("SELECT COUNT(*) FROM absente", conn).iloc[0,0]
                st.metric("Absențe totale", total_abs)
            
            st.markdown("---")
            
            st.markdown("#### 📈 Statistici pe clase")
            for clasa_nume, studenti in CLASE.items():
                with st.expander(f"Clasa {clasa_nume} - {len(studenti)} elevi"):
                    note_clasa = pd.read_sql(
                        "SELECT materie, COUNT(*) as nr_note, AVG(nota) as media FROM grades WHERE clasa = ? GROUP BY materie",
                        conn, params=[clasa_nume]
                    )
                    
                    if not note_clasa.empty:
                        note_clasa['media'] = note_clasa['media'].round(2)
                        st.dataframe(note_clasa, use_container_width=True, hide_index=True)
                    else:
                        st.info("Nu există note pentru această clasă.")
        
        with tab_profesori:
            st.markdown("### 👨‍🏫 Lista profesorilor")
            
            for profesor, info in PROFESORI.items():
                col_prof1, col_prof2, col_prof3 = st.columns([2, 1, 1])
                
                with col_prof1:
                    st.write(f"**{profesor}**")
                    st.caption(f"Materie: {info['materie']}")
                
                with col_prof2:
                    nr_note = pd.read_sql("SELECT COUNT(*) FROM grades WHERE profesor = ?",
                                        conn, params=[profesor]).iloc[0,0]
                    st.metric("Note adăugate", nr_note)
                
                with col_prof3:
                    nr_obs = pd.read_sql("SELECT COUNT(*) FROM observatii WHERE profesor = ?",
                                       conn, params=[profesor]).iloc[0,0]
                    st.metric("Observații", nr_obs)
        
        with tab_elevi:
            st.markdown("### 👤 Management elevi")
            
            clasa_admin = st.selectbox("Selectează clasa", list(CLASE.keys()), key="admin_clasa")
            
            for elev in CLASE[clasa_admin]:
                col_elev1, col_elev2, col_elev3, col_elev4 = st.columns([2, 1, 1, 1])
                
                with col_elev1:
                    st.write(f"**{elev}**")
                
                with col_elev2:
                    media_result = pd.read_sql("SELECT AVG(nota) FROM grades WHERE nume = ?",
                                            conn, params=[elev])
                    media = media_result.iloc[0,0]
                    st.metric("Medie", f"{media:.2f}" if media else "-")
                
                with col_elev3:
                    absente = pd.read_sql("SELECT COUNT(*) FROM absente WHERE nume = ?",
                                        conn, params=[elev]).iloc[0,0]
                    st.metric("Absențe", absente)
                
                with col_elev4:
                    nota_purtare = get_nota_purtare_curenta(elev, conn)
                    st.metric("Purtare", nota_purtare)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.8rem; padding: 10px;">
    <p>🎓 <strong>Catalog Digital</strong> | Anul școlar 2025-2026</p>
    <p>© 2026 | Sistem integrat de management școlar | Versiunea 5.0</p>
</div>
""", unsafe_allow_html=True)
