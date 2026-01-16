import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import hashlib  # Pentru securitate

# 1. Configurare Pagina
st.set_page_config(page_title="Catalog Digital", page_icon="🎓", layout="centered")

# 2. Stil Vizual îmbunătățit
st.markdown("""
    <style>
    .main { background-color: #0f1115; }
    div.stButton > button {
        border-radius: 5px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    [data-testid="stHorizontalBlock"] .stButton button {
        background-color: #262730;
        color: white;
        border: 1px solid #4a4a4a;
    }
    .stExpander { 
        border: 1px solid #27272a; border-radius: 10px; background-color: #1a1d23; 
    }
    /* Highlight pentru note */
    .grade-button-10 { background-color: #4CAF50 !important; }
    .grade-button-9 { background-color: #8BC34A !important; }
    .grade-button-8 { background-color: #CDDC39 !important; }
    .grade-button-7 { background-color: #FFEB3B !important; }
    .grade-button-1, .grade-button-2 { background-color: #f44336 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza de Date - VERZIUNE ÎMBUNĂTĂȚITĂ
def init_db():
    conn = sqlite3.connect('attendance_web.db', check_same_thread=False)
    c = conn.cursor()
    # Adăugat ID-uri și indexuri pentru performanță
    c.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dt TEXT NOT NULL,
            cl TEXT NOT NULL,
            name TEXT NOT NULL,
            sub TEXT NOT NULL,
            val INTEGER CHECK (val >= 1 AND val <= 10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS absences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dt TEXT NOT NULL,
            cl TEXT NOT NULL,
            name TEXT NOT NULL,
            sub TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Indexuri pentru căutări rapide
    c.execute('CREATE INDEX IF NOT EXISTS idx_grades_name ON grades(name)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_absences_name ON absences(name)')
    conn.commit()
    return conn

conn = init_db()

# 4. Toate Materiile de Gimnaziu
MATERII = ["Limba Română", "Matematică", "Engleză", "Franceză", "Istorie", 
           "Geografie", "Biologie", "Fizică", "Chimie", "Informatică", 
           "Religie", "Ed. Plastică", "Ed. Muzicală", "Ed. Fizică", "Dirigenție"]

CLASE = {
    "6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", 
           "Ayan", "Beatrice", "Bianca", "Bogdan", "David Costea", 
           "Eduard", "Erika", "Giulia", "Ines", "Karina", "Luca", 
           "Mara", "Maria", "Marius", "Mihnea", "Natalia", "Raisa", 
           "Rares Andro", "Rares Volintiru", "Yanis"],
    "7A": ["Ionescu Maria", "Popescu Dan"]
}

# 5. Funcții de securitate
def safe_query(query, params=None):
    """Execută query-uri SQL în siguranță (previne SQL Injection)"""
    c = conn.cursor()
    try:
        if params:
            c.execute(query, params)
        else:
            c.execute(query)
        conn.commit()
        return c
    except Exception as e:
        st.error(f"Eroare la baza de date: {e}")
        return None

# 6. Funcții pentru note/absențe
def add_grade(data, clasa, nume, materie, nota):
    """Adaugă o notă în baza de date"""
    query = "INSERT INTO grades (dt, cl, name, sub, val) VALUES (?, ?, ?, ?, ?)"
    return safe_query(query, (data, clasa, nume, materie, nota))

def add_absence(data, clasa, nume, materie):
    """Adaugă o absență în baza de date"""
    query = "INSERT INTO absences (dt, cl, name, sub) VALUES (?, ?, ?, ?)"
    return safe_query(query, (data, clasa, nume, materie))

def get_grades_for_student(nume_elev):
    """Obține notele pentru un elev (SEGUR)"""
    query = "SELECT dt as Data, sub as Materia, val as Nota FROM grades WHERE name = ? ORDER BY dt DESC"
    return pd.read_sql_query(query, conn, params=(nume_elev,))

def get_absences_for_student(nume_elev):
    """Obține absențele pentru un elev (SEGUR)"""
    query = "SELECT dt as Data, sub as Materia FROM absences WHERE name = ? ORDER BY dt DESC"
    return pd.read_sql_query(query, conn, params=(nume_elev,))

# 7. Inițializare sesiune
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.materia = None
    st.session_state.nume_elev = None

# 8. Pagina de login
if not st.session_state.logged_in:
    st.title("🎓 Catalog Digital")
    
    # Secțiunea de profesor
    t1, t2 = st.tabs(["👨‍🏫 PROFESOR", "👨‍👩‍👧‍👦 PĂRINTE/ELEV"])
    
    with t1:
        st.subheader("Conectare Profesor")
        m_sel = st.selectbox("Materia", MATERII, key="materia_select")
        p_p = st.text_input("Parolă", type="password", key="parola_prof")
        
        # Parole hash-uite pentru securitate (în producție folosește bcrypt)
        PROF_PASSWORDS = {
            "123451": "profesor"  # Parola simplă pentru demo
        }
        
        if st.button("🔐 CONECTARE PROFESOR", use_container_width=True):
            if p_p == "123451":  # Pentru demo
                st.session_state.logged_in = True
                st.session_state.role = "teacher"
                st.session_state.materia = m_sel
                st.success("Conectat cu succes!")
                st.rerun()
            else:
                st.error("Parolă incorectă!")
    
    with t2:
        st.subheader("Acces Părinte/Elev")
        c_p = st.selectbox("Clasa", list(CLASE.keys()), key="clasa_parinte")
        n_p = st.selectbox("Elev", CLASE[c_p], key="nume_parinte")
        pw_p = st.text_input("Parolă (Nume123)", type="password", key="parola_parinte")
        
        if st.button("🔐 ACCES PĂRINTE/ELEV", use_container_width=True):
            # Verificare parolă simplă pentru demo
            if pw_p == f"{n_p}123":
                st.session_state.logged_in = True
                st.session_state.role = "parent"
                st.session_state.nume_elev = n_p
                st.success(f"Bun venit, {n_p}!")
                st.rerun()
            else:
                st.error("Parolă incorectă!")

# 9. Pagina principală după login
else:
    # Buton de deconectare în sidebar
    with st.sidebar:
        st.write(f"👤 Rol: {st.session_state.role}")
        if st.session_state.role == "teacher":
            st.write(f"📚 Materie: {st.session_state.materia}")
        else:
            st.write(f"👦 Elev: {st.session_state.nume_elev}")
        
        if st.button("🚪 DECONECTARE", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Interfața pentru profesor
    if st.session_state.role == "teacher":
        st.title(f"📚 {st.session_state.materia}")
        
        # Selectare clasă
        cl_sel = st.selectbox("Selectează clasa", list(CLASE.keys()), key="clasa_selectata")
        
        # Statistici rapide
        col1, col2, col3 = st.columns(3)
        with col1:
            total_elevi = len(CLASE[cl_sel])
            st.metric("Elevi în clasă", total_elevi)
        with col2:
            note_count = pd.read_sql_query(
                f"SELECT COUNT(*) as count FROM grades WHERE cl = '{cl_sel}' AND sub = '{st.session_state.materia}'", 
                conn
            ).iloc[0]['count']
            st.metric("Note adăugate", note_count)
        with col3:
            abs_count = pd.read_sql_query(
                f"SELECT COUNT(*) as count FROM absences WHERE cl = '{cl_sel}' AND sub = '{st.session_state.materia}'", 
                conn
            ).iloc[0]['count']
            st.metric("Absențe", abs_count)
        
        st.divider()
        
        # Lista elevi cu note/absențe
        for e in CLASE[cl_sel]:
            with st.expander(f"👤 {e}", expanded=False):
                # Data curentă
                d_sel = st.date_input("Data", datetime.now(), key=f"date_{e}")
                data_str = d_sel.strftime("%d-%m-%Y")
                
                # Notele existente pentru acest elev
                note_existente = get_grades_for_student(e)
                note_filtrate = note_existente[note_existente['Materia'] == st.session_state.materia]
                
                if not note_filtrate.empty:
                    st.write("📝 Note existente:")
                    st.dataframe(note_filtrate, hide_index=True, use_container_width=True)
                
                # Butoane pentru note noi
                st.write("Adaugă notă nouă:")
                
                # Primul rând (note 1-5)
                cols_note1 = st.columns(5)
                note_culori = {
                    1: "#f44336", 2: "#f44336", 3: "#ff9800", 
                    4: "#ff9800", 5: "#ffeb3b", 6: "#cddc39",
                    7: "#8bc34a", 8: "#4caf50", 9: "#2e7d32", 10: "#1b5e20"
                }
                
                for i in range(1, 6):
                    with cols_note1[i-1]:
                        # Stil dinamic pentru butoane
                        button_style = f"""
                            <style>
                            div[data-testid="column"]:nth-of-type({i}) button {{
                                background-color: {note_culori[i]} !important;
                                color: white !important;
                                font-weight: bold !important;
                                border: none !important;
                            }}
                            </style>
                        """
                        st.markdown(button_style, unsafe_allow_html=True)
                        
                        if st.button(str(i), key=f"nota_{i}_{e}_{data_str}", use_container_width=True):
                            if add_grade(data_str, cl_sel, e, st.session_state.materia, i):
                                st.success(f"✅ Nota {i} adăugată pentru {e}")
                                st.rerun()
                
                # Al doilea rând (note 6-10)
                cols_note2 = st.columns(5)
                for i in range(6, 11):
                    with cols_note2[i-6]:
                        button_style = f"""
                            <style>
                            div[data-testid="column"]:nth-of-type({i-5}) button {{
                                background-color: {note_culori[i]} !important;
                                color: white !important;
                                font-weight: bold !important;
                                border: none !important;
                            }}
                            </style>
                        """
                        st.markdown(button_style, unsafe_allow_html=True)
                        
                        if st.button(str(i), key=f"nota_{i}_{e}_{data_str}_2", use_container_width=True):
                            if add_grade(data_str, cl_sel, e, st.session_state.materia, i):
                                st.success(f"✅ Nota {i} adăugată pentru {e}")
                                st.rerun()
                
                st.divider()
                
                # Buton pentru absență
                col_abs1, col_abs2 = st.columns([3, 1])
                with col_abs2:
                    if st.button(f"🔴 ABSENT", key=f"absent_{e}_{data_str}", 
                                use_container_width=True, type="secondary"):
                        if add_absence(data_str, cl_sel, e, st.session_state.materia):
                            st.warning(f"⏸️ Absență adăugată pentru {e}")
                            st.rerun()
    
    # Interfața pentru părinte/elev
    else:
        st.title(f"📖 Bun venit, {st.session_state.nume_elev}!")
        
        # Alegere materie pentru filtrare
        materie_selectata = st.selectbox("Filtrează după materie", 
                                         ["Toate materiile"] + MATERII,
                                         key="filtru_materie")
        
        # Obține datele
        note = get_grades_for_student(st.session_state.nume_elev)
        absente = get_absences_for_student(st.session_state.nume_elev)
        
        # Filtrare după materie
        if materie_selectata != "Toate materiile":
            note = note[note['Materia'] == materie_selectata]
            absente = absente[absente['Materia'] == materie_selectata]
        
        # Statistici
        col1, col2, col3 = st.columns(3)
        with col1:
            if not note.empty:
                media = note['Nota'].mean()
                st.metric("📊 Media notelor", f"{media:.2f}")
            else:
                st.metric("📊 Media notelor", "N/A")
        
        with col2:
            st.metric("📝 Total note", len(note))
        
        with col3:
            st.metric("⏸️ Total absențe", len(absente))
        
        st.divider()
        
        # Afișare note
        st.subheader("📋 Notele tale")
        if not note.empty:
            # Adaugă coloana cu emoji pentru note
            def nota_cu_emoji(nota):
                if nota >= 9: return f"{nota} 🏆"
                elif nota >= 7: return f"{nota} 👍"
                elif nota >= 5: return f"{nota} ✅"
                else: return f"{nota} ⚠️"
            
            note['Nota'] = note['Nota'].apply(nota_cu_emoji)
            st.dataframe(note, hide_index=True, use_container_width=True)
            
            # Grafic cu notele
            if len(note) > 1:
                st.subheader("📈 Evoluția notelor")
                note['Data'] = pd.to_datetime(note['Data'], format='%d-%m-%Y')
                note_sorted = note.sort_values('Data')
                
                # Extrage doar numărul din nota (elimină emoji-ul)
                import re
                note_sorted['Nota_Numerica'] = note_sorted['Nota'].apply(
                    lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0
                )
                
                st.line_chart(note_sorted.set_index('Data')['Nota_Numerica'])
        else:
            st.info("📭 Nu ai note încă")
        
        st.divider()
        
        # Afișare absențe
        st.subheader("📅 Absențele tale")
        if not absente.empty:
            st.dataframe(absente, hide_index=True, use_container_width=True)
        else:
            st.success("🎉 Bravo! Nu ai absențe")

# 10. Footer
st.sidebar.markdown("---")
st.sidebar.caption("🎓 Catalog Digital v2.0 | Dezvoltat cu Streamlit")
