import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import hashlib

# 1. Configurare Pagina universală
st.set_page_config(
    page_title="Catalog Digital", 
    page_icon="🎓", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS responsive pentru toate dispozitivele
st.markdown("""
    <style>
    /* RESET pentru compatibilitate */
    * {
        box-sizing: border-box;
    }
    
    /* Fundal universal */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364) !important;
        min-height: 100vh !important;
    }
    
    /* Ascunde elementele inutile */
    footer, #MainMenu, header {
        visibility: hidden !important;
    }
    
    /* Header responsive */
    h1, h2, h3 {
        color: white !important;
        text-align: center !important;
        margin: 10px 0 !important;
    }
    
    /* Container principal */
    .main-container {
        max-width: 100% !important;
        padding: 10px !important;
    }
    
    /* Butoane responsive */
    .stButton > button {
        width: 100% !important;
        margin: 5px 0 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    
    /* Input-uri responsive */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 6px !important;
    }
    
    /* Expander responsive */
    .stExpander {
        margin: 5px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    
    /* Tabs responsive */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px !important;
    }
    
    /* Media queries pentru diferite dispozitive */
    @media (max-width: 768px) {
        /* Mobile optimizations */
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.2rem !important; }
        h3 { font-size: 1rem !important; }
        
        .stButton > button {
            height: 40px !important;
            font-size: 0.9rem !important;
        }
        
        .streamlit-expanderHeader {
            font-size: 0.9rem !important;
            padding: 8px 12px !important;
        }
    }
    
    @media (min-width: 769px) {
        /* Desktop optimizations */
        .main-container {
            max-width: 800px !important;
            margin: 0 auto !important;
        }
    }
    
    /* Mesaje de eroare/success */
    .stAlert {
        border-radius: 8px !important;
        margin: 10px 0 !important;
    }
    
    /* Deconectare fixată */
    .logout-btn {
        position: fixed !important;
        top: 10px !important;
        right: 10px !important;
        z-index: 1000 !important;
        width: auto !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# 3. Parole FIXATE - versiunea simplă care sigur merge
PASSWORDS = {
    "teacher": "123",
    "parent": "1234", 
    "admin": "admin"
}

# 4. Initializare Baza de Date - versiune simplă
def init_db():
    conn = sqlite3.connect('catalog_app.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        clasa TEXT,
        nume TEXT,
        materie TEXT,
        nota INTEGER
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS absente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        clasa TEXT,
        nume TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS observatii (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        nume TEXT,
        materie TEXT,
        observatie TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS purtare (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nume TEXT UNIQUE,
        nota INTEGER DEFAULT 10
    )''')
    
    conn.commit()
    return conn

# 5. Funcții utilitare SIMPLE
def check_password(password, role):
    """Verifică parola direct - fără hash pentru simplitate"""
    return password == PASSWORDS[role]

def get_purtare(nume, conn):
    """Obține nota de purtare"""
    cursor = conn.cursor()
    cursor.execute("SELECT nota FROM purtare WHERE nume = ?", (nume,))
    result = cursor.fetchone()
    return result[0] if result else 10

def init_purtare(conn, elevi):
    """Initializează notele de purtare"""
    cursor = conn.cursor()
    for elev in elevi:
        cursor.execute("INSERT OR IGNORE INTO purtare (nume, nota) VALUES (?, ?)", (elev, 10))
    conn.commit()

# 6. Setup baza de date
conn = init_db()

# Datele aplicației
CLASE = {
    "6B": ["Albert", "Alexandru", "Alissa", "Andrei G.", "Andrei C.", "Ayan", 
           "Beatrice", "Bianca", "Bogdan", "David Costea", "Eduard", "Erika", 
           "Giulia", "Ines", "Karina", "Luca", "Mara", "Maria", "Marius", 
           "Mihnea", "Natalia", "Raisa", "Rares Andro", "Rares Volintiru", "Yanis"],
    "7A": ["Ionescu Maria", "Popescu Dan"]
}

# Inițializează purtarea pentru toți elevii
all_students = []
for studenti in CLASE.values():
    all_students.extend(studenti)
init_purtare(conn, all_students)

# 7. Inițializare session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.materie = None
    st.session_state.nume_elev = None
    st.session_state.clasa_selectata = "6B"

# ============================================
# PAGINA DE LOGIN
# ============================================
if not st.session_state.logged_in:
    st.markdown("<h1>🎓 Catalog Digital</h1>", unsafe_allow_html=True)
    
    # Tabs pentru diferite roluri
    tab_prof, tab_parinte, tab_directoare = st.tabs(["Profesor", "Părinte", "Directoare"])
    
    with tab_prof:
        st.subheader("Autentificare Profesor")
        
        # Selectare materie
        materie = st.selectbox(
            "Selectează materia",
            ["Informatică", "Matematică", "Română"],
            key="login_materie"
        )
        
        # Parolă
        parola = st.text_input("Parolă", type="password", key="parola_prof")
        
        # Buton login
        if st.button("Accesează ca Profesor", type="primary", use_container_width=True):
            if parola and check_password(parola, "teacher"):
                st.session_state.logged_in = True
                st.session_state.role = "teacher"
                st.session_state.materie = materie
                st.success("Autentificare reușită!")
                st.rerun()
            else:
                st.error("Parolă incorectă! Încearcă '123'")
    
    with tab_parinte:
        st.subheader("Autentificare Părinte")
        
        # Selectare elev
        elev_selectat = st.selectbox(
            "Selectează elevul",
            sorted(all_students),
            key="login_elev"
        )
        
        # Parolă
        parola_parinte = st.text_input("Parolă părinte", type="password", key="parola_parinte")
        
        # Buton login
        if st.button("Accesează ca Părinte", type="primary", use_container_width=True):
            if parola_parinte and check_password(parola_parinte, "parent"):
                st.session_state.logged_in = True
                st.session_state.role = "parent"
                st.session_state.nume_elev = elev_selectat
                st.success("Autentificare reușită!")
                st.rerun()
            else:
                st.error("Parolă incorectă! Încearcă '1234'")
    
    with tab_directoare:
        st.subheader("Autentificare Directoare")
        
        # Parolă admin
        parola_admin = st.text_input("Cod de acces", type="password", key="parola_admin")
        
        # Buton login
        if st.button("Accesează ca Directoare", type="primary", use_container_width=True):
            if parola_admin and check_password(parola_admin, "admin"):
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.success("Autentificare reușită!")
                st.rerun()
            else:
                st.error("Cod incorect! Încearcă 'admin'")

# ============================================
# PAGINA PRINCIPALĂ (După login)
# ============================================
else:
    # Buton de deconectare
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("🚪 Deconectare", type="secondary"):
        st.session_state.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # ============================================
    # INTERFAȚA PROFESOR
    # ============================================
    if st.session_state.role == "teacher":
        st.markdown(f"<h2>👨‍🏫 Profesor - {st.session_state.materie}</h2>", unsafe_allow_html=True)
        
        # Selectare clasă
        clasa = st.selectbox("Selectează clasa", list(CLASE.keys()), key="prof_clasa")
        st.session_state.clasa_selectata = clasa
        
        # Statistici rapide
        col1, col2, col3 = st.columns(3)
        with col1:
            today = datetime.now().strftime("%Y-%m-%d")
            note_azi = pd.read_sql(
                f"SELECT COUNT(*) FROM grades WHERE data = '{today}' AND materie = ?",
                conn, params=[st.session_state.materie]
            ).iloc[0,0]
            st.metric("📝 Note azi", note_azi)
        
        with col2:
            abs_azi = pd.read_sql(
                f"SELECT COUNT(*) FROM absente WHERE data = '{today}'",
                conn
            ).iloc[0,0]
            st.metric("❌ Absențe azi", abs_azi)
        
        with col3:
            elev_count = len(CLASE[clasa])
            st.metric("👥 Elevi", elev_count)
        
        st.markdown("---")
        
        # Lista elevilor cu acțiuni
        st.markdown(f"### Elevi - Clasa {clasa}")
        
        # Opțiune de căutare
        search_query = st.text_input("🔍 Caută elev...", key="search_elev")
        
        # Filtrare elevi
        if search_query:
            elevi_filtrati = [e for e in CLASE[clasa] if search_query.lower() in e.lower()]
        else:
            elevi_filtrati = CLASE[clasa]
        
        for elev in elevi_filtrati:
            with st.expander(f"👤 {elev}", expanded=False):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    # Adăugare notă
                    nota_noua = st.number_input("Notă", 1, 10, 10, key=f"nota_{elev}")
                    if st.button("Adaugă Nota", key=f"btn_nota_{elev}", use_container_width=True):
                        data_curenta = datetime.now().strftime("%Y-%m-%d %H:%M")
                        conn.execute(
                            "INSERT INTO grades (data, clasa, nume, materie, nota) VALUES (?, ?, ?, ?, ?)",
                            (data_curenta, clasa, elev, st.session_state.materie, nota_noua)
                        )
                        conn.commit()
                        st.success(f"Nota {nota_noua} adăugată pentru {elev}!")
                        st.rerun()
                
                with col_b:
                    # Marcare absent
                    if st.button("Marchează Absent", key=f"btn_absent_{elev}", use_container_width=True):
                        data_curenta = datetime.now().strftime("%Y-%m-%d")
                        conn.execute(
                            "INSERT INTO absente (data, clasa, nume) VALUES (?, ?, ?)",
                            (data_curenta, clasa, elev)
                        )
                        conn.commit()
                        st.warning(f"{elev} marcat absent!")
                        st.rerun()
                
                # Adăugare observație
                observatie = st.text_area("Observație", key=f"obs_{elev}", placeholder="Scrie observația aici...")
                if st.button("Trimite Observație", key=f"btn_obs_{elev}", use_container_width=True):
                    if observatie.strip():
                        data_curenta = datetime.now().strftime("%Y-%m-%d")
                        conn.execute(
                            "INSERT INTO observatii (data, nume, materie, observatie) VALUES (?, ?, ?, ?)",
                            (data_curenta, elev, st.session_state.materie, observatie.strip())
                        )
                        conn.commit()
                        st.info(f"Observație trimisă pentru {elev}!")
                        st.rerun()
                    else:
                        st.error("Te rog scrie o observație!")
    
    # ============================================
    # INTERFAȚA PĂRINTE
    # ============================================
    elif st.session_state.role == "parent":
        elev = st.session_state.nume_elev
        st.markdown(f"<h2>👪 Părinte - {elev}</h2>", unsafe_allow_html=True)
        
        # Statistici rapide
        col_p1, col_p2, col_p3 = st.columns(3)
        
        with col_p1:
            note_total = pd.read_sql(
                "SELECT COUNT(*) FROM grades WHERE nume = ?",
                conn, params=[elev]
            ).iloc[0,0]
            st.metric("📊 Note", note_total)
        
        with col_p2:
            abs_total = pd.read_sql(
                "SELECT COUNT(*) FROM absente WHERE nume = ?",
                conn, params=[elev]
            ).iloc[0,0]
            st.metric("❌ Absențe", abs_total)
        
        with col_p3:
            nota_purtare = get_purtare(elev, conn)
            st.metric("⭐ Purtare", f"{nota_purtare}/10")
        
        st.markdown("---")
        
        # Tabs pentru diferite informații
        tab_note, tab_absente, tab_observatii = st.tabs(["Note", "Absențe", "Observații"])
        
        with tab_note:
            st.markdown("### Notele elevului")
            note_df = pd.read_sql(
                "SELECT data as Data, materie as Materie, nota as Nota FROM grades WHERE nume = ? ORDER BY data DESC",
                conn, params=[elev]
            )
            
            if not note_df.empty:
                st.dataframe(note_df, use_container_width=True, hide_index=True)
                
                # Calcul medie pe materii
                st.markdown("**Medii pe materii:**")
                medii = note_df.groupby('Materie')['Nota'].mean().round(2)
                for materie, medie in medii.items():
                    st.write(f"**{materie}**: {medie}")
            else:
                st.info("Nu există note înregistrate.")
        
        with tab_absente:
            st.markdown("### Absențele elevului")
            abs_df = pd.read_sql(
                "SELECT data as Data FROM absente WHERE nume = ? ORDER BY data DESC",
                conn, params=[elev]
            )
            
            if not abs_df.empty:
                st.dataframe(abs_df, use_container_width=True, hide_index=True)
            else:
                st.success("Nu există absențe înregistrate.")
        
        with tab_observatii:
            st.markdown("### Observații de la profesori")
            obs_df = pd.read_sql(
                "SELECT data as Data, materie as Materie, observatie as Observație FROM observatii WHERE nume = ? ORDER BY data DESC",
                conn, params=[elev]
            )
            
            if not obs_df.empty:
                for _, row in obs_df.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div style="background-color: rgba(255,75,75,0.1); padding: 10px; border-radius: 8px; margin: 5px 0;">
                            <strong>{row['Data']} - {row['Materie']}</strong><br>
                            {row['Observație']}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.success("Nu există observații înregistrate.")
    
    # ============================================
    # INTERFAȚA DIRECTOARE
    # ============================================
    elif st.session_state.role == "admin":
        st.markdown("<h2>🏛️ Panou Directoare</h2>", unsafe_allow_html=True)
        
        # Tabs pentru diferite funcționalități
        tab_statistici, tab_purtare, tab_mesaje = st.tabs(["Statistici", "Purtare", "Mesaje"])
        
        with tab_statistici:
            st.markdown("### Statistici generale")
            
            # Statistici rapide
            col_a1, col_a2, col_a3 = st.columns(3)
            
            with col_a1:
                total_note = pd.read_sql("SELECT COUNT(*) FROM grades", conn).iloc[0,0]
                st.metric("📚 Note totale", total_note)
            
            with col_a2:
                total_absente = pd.read_sql("SELECT COUNT(*) FROM absente", conn).iloc[0,0]
                st.metric("❌ Absențe totale", total_absente)
            
            with col_a3:
                total_obs = pd.read_sql("SELECT COUNT(*) FROM observatii", conn).iloc[0,0]
                st.metric("⚠️ Observații", total_obs)
            
            # Distribuția notelor
            st.markdown("### Distribuția notelor")
            dist_df = pd.read_sql("SELECT nota, COUNT(*) as count FROM grades GROUP BY nota ORDER BY nota", conn)
            if not dist_df.empty:
                st.bar_chart(dist_df.set_index('nota'))
        
        with tab_purtare:
            st.markdown("### Gestionare note de purtare")
            
            # Selectare elev
            elev_selectat = st.selectbox("Selectează elev", sorted(all_students), key="admin_elev")
            
            if elev_selectat:
                # Afișare și modificare notă purtare
                nota_curenta = get_purtare(elev_selectat, conn)
                st.write(f"Nota curentă de purtare: **{nota_curenta}**")
                
                noua_nota = st.slider("Setează noua notă de purtare", 1, 10, nota_curenta, key=f"slider_{elev_selectat}")
                
                if st.button("Salvează nota de purtare", key=f"btn_save_{elev_selectat}", use_container_width=True):
                    conn.execute("DELETE FROM purtare WHERE nume = ?", (elev_selectat,))
                    conn.execute("INSERT INTO purtare (nume, nota) VALUES (?, ?)", (elev_selectat, noua_nota))
                    conn.commit()
                    st.success(f"Nota de purtare actualizată pentru {elev_selectat}: {noua_nota}")
                    st.rerun()
        
        with tab_mesaje:
            st.markdown("### Gestionare observații")
            
            # Afișare toate observațiile
            mesaje_df = pd.read_sql(
                "SELECT id, data, nume, materie, observatie FROM observatii ORDER BY data DESC",
                conn
            )
            
            if not mesaje_df.empty:
                for _, row in mesaje_df.iterrows():
                    with st.container():
                        col_m1, col_m2 = st.columns([4, 1])
                        with col_m1:
                            st.markdown(f"""
                            <div style="background-color: rgba(255,165,0,0.1); padding: 8px; border-radius: 6px; margin: 3px 0;">
                                <strong>{row['data']} - {row['nume']} ({row['materie']})</strong><br>
                                {row['observatie']}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col_m2:
                            if st.button("Șterge", key=f"del_{row['id']}", type="secondary"):
                                conn.execute("DELETE FROM observatii WHERE id = ?", (row['id'],))
                                conn.commit()
                                st.success("Observație ștearsă!")
                                st.rerun()
            else:
                st.info("Nu există observații în sistem.")
    
    # Închide container principal
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<center><small>© 2024 Catalog Digital | Sistem școlar integrat</small></center>", unsafe_allow_html=True)
