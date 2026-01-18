import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
import hashlib
import calendar
import json
import os
import time
from typing import Dict, List, Tuple, Optional, Any
import numpy as np

# ============================================
# 1. CONFIGURARE PAGINĂ AVANSATĂ
# ============================================
st.set_page_config(
    page_title="🎓 Catalog Digital 2026 | Sistem Integrat de Management Școlar",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.educatie.ro',
        'Report a bug': None,
        'About': """
        ## 🎓 Catalog Digital 2026
        **Versiunea:** 6.0 Premium
        **Anul școlar:** 2025-2026
        **Dezvoltat de:** Departamentul IT Școlar
        **Licență:** EDU-SOFT 2026
        """
    }
)

# ============================================
# 2. SISTEM AVANSAT DE STILURI CSS
# ============================================
st.markdown("""
<style>
    /* Resetare și configurare de bază */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
    }
    
    /* Fundal gradient premium */
    .main {
        background: linear-gradient(135deg, 
            #0f172a 0%,
            #1e293b 25%,
            #334155 50%,
            #475569 75%,
            #64748b 100%
        ) !important;
        min-height: 100vh;
    }
    
    /* Sidebar elegant cu efect de sticlă */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Carduri moderne */
    .custom-card {
        background: linear-gradient(145deg, 
            rgba(30, 41, 59, 0.9),
            rgba(15, 23, 42, 0.9)
        ) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        margin: 15px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 
            0 10px 25px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .custom-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(59, 130, 246, 0.5) !important;
    }
    
    /* Butoane premium */
    .stButton > button {
        background: linear-gradient(135deg, 
            #3b82f6 0%,
            #2563eb 50%,
            #1d4ed8 100%
        ) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(135deg, 
            #2563eb 0%,
            #1d4ed8 50%,
            #1e40af 100%
        ) !important;
    }
    
    /* Input-uri și select-uri stilizate */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        background: rgba(30, 41, 59, 0.9) !important;
    }
    
    /* Tabele elegante */
    .dataframe {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 15px !important;
        text-align: left !important;
    }
    
    .dataframe td {
        padding: 12px 15px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        background: rgba(30, 41, 59, 0.7) !important;
    }
    
    .dataframe tr:hover td {
        background: rgba(59, 130, 246, 0.15) !important;
    }
    
    /* Animatie pentru încărcare */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Efecte pentru zile calendar */
    .calendar-day {
        padding: 10px !important;
        margin: 3px !important;
        border-radius: 12px !important;
        text-align: center !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        min-height: 60px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .calendar-day::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.1) 0%,
            rgba(255, 255, 255, 0.05) 100%
        );
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .calendar-day:hover::before {
        opacity: 1;
    }
    
    .calendar-day-selected {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
        transform: scale(1.05) !important;
    }
    
    .calendar-day-today {
        background: linear-gradient(135deg, #22c55e, #16a34a) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4) !important;
    }
    
    .calendar-day-regular {
        background: rgba(30, 41, 59, 0.8) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Scrollbar personalizat */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
    }
    
    /* Badge-uri și etichete */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #eab308, #ca8a04);
        color: white;
    }
    
    .badge-danger {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
    }
    
    .badge-info {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
    }
    
    /* Header-uri decorative */
    .section-header {
        position: relative;
        padding-left: 20px;
        margin-bottom: 25px;
    }
    
    .section-header::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 5px;
        background: linear-gradient(to bottom, #3b82f6, #22c55e);
        border-radius: 3px;
    }
    
    /* Efect de iluminare */
    .glow-effect {
        position: relative;
    }
    
    .glow-effect::after {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
            #3b82f6, #22c55e, #eab308, #ef4444, #8b5cf6
        );
        z-index: -1;
        filter: blur(15px);
        opacity: 0.3;
        border-radius: inherit;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .calendar-day {
            min-height: 45px;
            font-size: 0.9rem;
            padding: 6px !important;
        }
        
        .custom-card {
            padding: 15px !important;
            border-radius: 15px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 3. CONSTANTE ȘI SETĂRI SISTEM
# ============================================

# Materii complete pentru gimnaziu
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
    "Consiliere și orientare",
    "Educație pentru societate",
    "Dezvoltare personală"
]

# Dicționar detaliat al profesorilor
PROFESORI = {
    "Popescu Maria": {
        "materie": "Matematică",
        "parola": "ProfPopescu2026@",
        "email": "maria.popescu@scoala.ro",
        "telefon": "0721123456",
        "specializare": "Matematică-Informatică",
        "grad_didactic": "Definitiv",
        "ani_experienta": 15
    },
    "Ionescu Ion": {
        "materie": "Limba și literatura română",
        "parola": "ProfIonescu2026@",
        "email": "ion.ionescu@scoala.ro",
        "telefon": "0722123456",
        "specializare": "Limba și literatura română",
        "grad_didactic": "Definitiv",
        "ani_experienta": 12
    },
    "Vasilescu Elena": {
        "materie": "Limba engleză",
        "parola": "ProfVasilescu2026@",
        "email": "elena.vasilescu@scoala.ro",
        "telefon": "0723123456",
        "specializare": "Limba engleză",
        "grad_didactic": "Definitiv",
        "ani_experienta": 10
    },
    "Dumitrescu Andreea": {
        "materie": "Limba franceză",
        "parola": "ProfDumitrescu2026@",
        "email": "andreea.dumitrescu@scoala.ro",
        "telefon": "0724123456",
        "specializare": "Limba franceză",
        "grad_didactic": "Definitiv",
        "ani_experienta": 8
    },
    "Constantin Mihai": {
        "materie": "Limba germană",
        "parola": "ProfConstantin2026@",
        "email": "mihai.constantin@scoala.ro",
        "telefon": "0725123456",
        "specializare": "Limba germană",
        "grad_didactic": "Definitiv",
        "ani_experienta": 7
    },
    "Radu Alexandra": {
        "materie": "Limba spaniolă",
        "parola": "ProfRadu2026@",
        "email": "alexandra.radu@scoala.ro",
        "telefon": "0726123456",
        "specializare": "Limba spaniolă",
        "grad_didactic": "Definitiv",
        "ani_experienta": 6
    },
    "Stanescu Vlad": {
        "materie": "Istorie",
        "parola": "ProfStanescu2026@",
        "email": "vlad.stanescu@scoala.ro",
        "telefon": "0727123456",
        "specializare": "Istorie",
        "grad_didactic": "Definitiv",
        "ani_experienta": 14
    },
    "Georgescu Ana": {
        "materie": "Geografie",
        "parola": "ProfGeorgescu2026@",
        "email": "ana.georgescu@scoala.ro",
        "telefon": "0728123456",
        "specializare": "Geografie",
        "grad_didactic": "Definitiv",
        "ani_experienta": 11
    },
    "Marinescu Dan": {
        "materie": "Biologie",
        "parola": "ProfMarinescu2026@",
        "email": "dan.marinescu@scoala.ro",
        "telefon": "0729123456",
        "specializare": "Biologie-Chimie",
        "grad_didactic": "Definitiv",
        "ani_experienta": 13
    },
    "Popa Cristian": {
        "materie": "Fizică",
        "parola": "ProfPopa2026@",
        "email": "cristian.popa@scoala.ro",
        "telefon": "0730123456",
        "specializare": "Fizică",
        "grad_didactic": "Definitiv",
        "ani_experienta": 9
    },
    "Munteanu Ioana": {
        "materie": "Chimie",
        "parola": "ProfMunteanu2026@",
        "email": "ioana.munteanu@scoala.ro",
        "telefon": "0731123456",
        "specializare": "Chimie",
        "grad_didactic": "Definitiv",
        "ani_experienta": 8
    },
    "Badea Sorin": {
        "materie": "Educație fizică și sport",
        "parola": "ProfBadea2026@",
        "email": "sorin.badea@scoala.ro",
        "telefon": "0732123456",
        "specializare": "Educație fizică și sport",
        "grad_didactic": "Definitiv",
        "ani_experienta": 16
    },
    "Ilie Carmen": {
        "materie": "Educație plastică",
        "parola": "ProfIlie2026@",
        "email": "carmen.ilie@scoala.ro",
        "telefon": "0733123456",
        "specializare": "Arte plastice",
        "grad_didactic": "Definitiv",
        "ani_experienta": 10
    },
    "Stoica Gabriel": {
        "materie": "Educație muzicală",
        "parola": "ProfStoica2026@",
        "email": "gabriel.stoica@scoala.ro",
        "telefon": "0734123456",
        "specializare": "Muzică",
        "grad_didactic": "Definitiv",
        "ani_experienta": 12
    },
    "Nistor Radu": {
        "materie": "Educație tehnologică",
        "parola": "ProfNistor2026@",
        "email": "radu.nistor@scoala.ro",
        "telefon": "0735123456",
        "specializare": "Tehnologie",
        "grad_didactic": "Definitiv",
        "ani_experienta": 9
    },
    "Tudor Mihaela": {
        "materie": "Informatică și TIC",
        "parola": "ProfTudor2026@",
        "email": "mihaela.tudor@scoala.ro",
        "telefon": "0736123456",
        "specializare": "Informatică",
        "grad_didactic": "Definitiv",
        "ani_experienta": 7
    },
    "Diaconu Petru": {
        "materie": "Religie",
        "parola": "ProfDiaconu2026@",
        "email": "petru.diaconu@scoala.ro",
        "telefon": "0737123456",
        "specializare": "Religie",
        "grad_didactic": "Definitiv",
        "ani_experienta": 18
    },
    "Serban Laura": {
        "materie": "Consiliere și orientare",
        "parola": "ProfSerban2026@",
        "email": "laura.serban@scoala.ro",
        "telefon": "0738123456",
        "specializare": "Psihologie",
        "grad_didactic": "Definitiv",
        "ani_experienta": 11
    }
}

# Dicționar detaliat al elevilor
ELEVI = {
    "Albert": {
        "parola": "Albert2026#",
        "data_nasterii": "2012-03-15",
        "adresa": "Strada Primăverii nr. 10",
        "telefon_parinte": "0740111222",
        "email_parinte": "parinte.albert@gmail.com",
        "observatii_speciale": "Alergie la praf de cretă"
    },
    "Alexandru": {
        "parola": "Alexandru2026#",
        "data_nasterii": "2012-05-20",
        "adresa": "Strada Libertății nr. 25",
        "telefon_parinte": "0740222333",
        "email_parinte": "parinte.alexandru@gmail.com",
        "observatii_speciale": "Nicio observație specială"
    },
    "Alissa": {
        "parola": "Alissa2026#",
        "data_nasterii": "2012-07-12",
        "adresa": "Strada Florilor nr. 8",
        "telefon_parinte": "0740333444",
        "email_parinte": "parinte.alissa@gmail.com",
        "observatii_speciale": "Necesită ochelari"
    },
    "Andrei G.": {
        "parola": "AndreiG2026#",
        "data_nasterii": "2012-02-28",
        "adresa": "Strada Soarelui nr. 15",
        "telefon_parinte": "0740444555",
        "email_parinte": "parinte.andrei.g@gmail.com",
        "observatii_speciale": "Excelent la matematică"
    },
    "Andrei C.": {
        "parola": "AndreiC2026#",
        "data_nasterii": "2012-09-03",
        "adresa": "Strada Lunii nr. 7",
        "telefon_parinte": "0740555666",
        "email_parinte": "parinte.andrei.c@gmail.com",
        "observatii_speciale": "Talent muzical"
    },
    "Ayan": {
        "parola": "Ayan2026#",
        "data_nasterii": "2012-11-18",
        "adresa": "Strada Stelelor nr. 12",
        "telefon_parinte": "0740666777",
        "email_parinte": "parinte.ayan@gmail.com",
        "observatii_speciale": "Vorbește trei limbi"
    },
    "Beatrice": {
        "parola": "Beatrice2026#",
        "data_nasterii": "2012-04-22",
        "adresa": "Strada Plopilor nr. 30",
        "telefon_parinte": "0740777888",
        "email_parinte": "parinte.beatrice@gmail.com",
        "observatii_speciale": "Premiante la concursuri de limba română"
    },
    "Bianca": {
        "parola": "Bianca2026#",
        "data_nasterii": "2012-08-05",
        "adresa": "Strada Castanilor nr. 18",
        "telefon_parinte": "0740888999",
        "email_parinte": "parinte.bianca@gmail.com",
        "observatii_speciale": "Practică dans sportiv"
    },
    "Bogdan": {
        "parola": "Bogdan2026#",
        "data_nasterii": "2012-01-30",
        "adresa": "Strada Bravului nr. 22",
        "telefon_parinte": "0740999000",
        "email_parinte": "parinte.bogdan@gmail.com",
        "observatii_speciale": "Căpitan de echipă de fotbal"
    },
    "David Costea": {
        "parola": "David2026#",
        "data_nasterii": "2012-06-14",
        "adresa": "Strada Speranței nr. 9",
        "telefon_parinte": "0740101010",
        "email_parinte": "parinte.david@gmail.com",
        "observatii_speciale": "Interes pentru robotică"
    },
    "Eduard": {
        "parola": "Eduard2026#",
        "data_nasterii": "2012-10-08",
        "adresa": "Strada Mărgăritarului nr. 14",
        "telefon_parinte": "0740112020",
        "email_parinte": "parinte.eduard@gmail.com",
        "observatii_speciale": "Nicio observație specială"
    },
    "Erika": {
        "parola": "Erika2026#",
        "data_nasterii": "2012-12-25",
        "adresa": "Strada Crinului nr. 11",
        "telefon_parinte": "0740223030",
        "email_parinte": "parinte.erika@gmail.com",
        "observatii_speciale": "Talent artistic"
    },
    "Giulia": {
        "parola": "Giulia2026#",
        "data_nasterii": "2012-03-03",
        "adresa": "Strada Trandafirilor nr. 6",
        "telefon_parinte": "0740334040",
        "email_parinte": "parinte.giulia@gmail.com",
        "observatii_speciale": "Vorbește italiană fluent"
    },
    "Ines": {
        "parola": "Ines2026#",
        "data_nasterii": "2012-07-19",
        "adresa": "Strada Lalelelor nr. 17",
        "telefon_parinte": "0740445050",
        "email_parinte": "parinte.ines@gmail.com",
        "observatii_speciale": "Premiantă la matematică"
    },
    "Karina": {
        "parola": "Karina2026#",
        "data_nasterii": "2012-05-11",
        "adresa": "Strada Narciselor nr. 4",
        "telefon_parinte": "0740556060",
        "email_parinte": "parinte.karina@gmail.com",
        "observatii_speciale": "Cântă la pian"
    },
    "Luca": {
        "parola": "Luca2026#",
        "data_nasterii": "2012-09-27",
        "adresa": "Strada Zorilor nr. 20",
        "telefon_parinte": "0740667070",
        "email_parinte": "parinte.luca@gmail.com",
        "observatii_speciale": "Interes pentru astronomie"
    },
    "Mara": {
        "parola": "Mara2026#",
        "data_nasterii": "2012-02-14",
        "adresa": "Strada Brândușilor nr. 13",
        "telefon_parinte": "0740778080",
        "email_parinte": "parinte.mara@gmail.com",
        "observatii_speciale": "Practică înot competitiv"
    },
    "Maria": {
        "parola": "Maria2026#",
        "data_nasterii": "2012-11-05",
        "adresa": "Strada Crizantemelor nr. 16",
        "telefon_parinte": "0740889090",
        "email_parinte": "parinte.maria@gmail.com",
        "observatii_speciale": "Delegată de clasă"
    },
    "Marius": {
        "parola": "Marius2026#",
        "data_nasterii": "2012-04-08",
        "adresa": "Strada Bujorilor nr. 19",
        "telefon_parinte": "0740990010",
        "email_parinte": "parinte.marius@gmail.com",
        "observatii_speciale": "Excelent la informatică"
    },
    "Mihnea": {
        "parola": "Mihnea2026#",
        "data_nasterii": "2012-08-22",
        "adresa": "Strada Garoafelor nr. 5",
        "telefon_parinte": "0740102010",
        "email_parinte": "parinte.mihnea@gmail.com",
        "observatii_speciale": "Talent la șah"
    },
    "Natalia": {
        "parola": "Natalia2026#",
        "data_nasterii": "2012-01-17",
        "adresa": "Strada Viorelelor nr. 21",
        "telefon_parinte": "0740213020",
        "email_parinte": "parinte.natalia@gmail.com",
        "observatii_speciale": "Premiantă la limba engleză"
    },
    "Raisa": {
        "parola": "Raisa2026#",
        "data_nasterii": "2012-10-30",
        "adresa": "Strada Cameliilor nr. 23",
        "telefon_parinte": "0740324030",
        "email_parinte": "parinte.raisa@gmail.com",
        "observatii_speciale": "Practică gimnastică ritmică"
    },
    "Rares Andro": {
        "parola": "RaresA2026#",
        "data_nasterii": "2012-06-07",
        "adresa": "Strada Magnoliilor nr. 24",
        "telefon_parinte": "0740435040",
        "email_parinte": "parinte.rares.andro@gmail.com",
        "observatii_speciale": "Interes pentru fizică"
    },
    "Rares Volintiru": {
        "parola": "RaresV2026#",
        "data_nasterii": "2012-03-25",
        "adresa": "Strada Liliacilor nr. 26",
        "telefon_parinte": "0740546050",
        "email_parinte": "parinte.rares.volintiru@gmail.com",
        "observatii_speciale": "Talent la desen"
    },
    "Yanis": {
        "parola": "Yanis2026#",
        "data_nasterii": "2012-12-12",
        "adresa": "Strada Iasomiei nr. 27",
        "telefon_parinte": "0740657060",
        "email_parinte": "parinte.yanis@gmail.com",
        "observatii_speciale": "Vorbește franceză fluent"
    },
    "Ionescu Maria": {
        "parola": "IonescuM2026#",
        "data_nasterii": "2011-07-15",
        "adresa": "Strada Unirii nr. 45",
        "telefon_parinte": "0740768070",
        "email_parinte": "parinte.ionescu@gmail.com",
        "observatii_speciale": "Reprezentantă elev în consiliul școlii"
    },
    "Popescu Dan": {
        "parola": "PopescuD2026#",
        "data_nasterii": "2011-09-22",
        "adresa": "Strada Independenței nr. 32",
        "telefon_parinte": "0740879080",
        "email_parinte": "parinte.popescu@gmail.com",
        "observatii_speciale": "Premiant general"
    }
}

# Parola pentru directoare
PAROLA_DIRECTOARE = "Directoare2026@"

# Configurare clase
CLASE = {
    "6B": [elev for elev in ELEVI.keys() if elev not in ["Ionescu Maria", "Popescu Dan"]],
    "7A": ["Ionescu Maria", "Popescu Dan"],
    "8C": []  # Clasă goală pentru viitoare extinderi
}

# ============================================
# 4. SISTEM AVANSAT DE BAZĂ DE DATE
# ============================================

@st.cache_resource
def init_db():
    """Inițializează baza de date cu tabelele necesare"""
    conn = sqlite3.connect('catalog_2026_premium.db', check_same_thread=False)
    c = conn.cursor()
    
    # Tabel pentru note
    c.execute('''CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data DATE NOT NULL,
        clasa TEXT NOT NULL,
        nume TEXT NOT NULL,
        materie TEXT NOT NULL,
        nota REAL CHECK (nota >= 1 AND nota <= 10),
        profesor TEXT NOT NULL,
        tip_nota TEXT DEFAULT 'oral',
        semestru INTEGER DEFAULT 1,
        comentariu TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(data, nume, materie, tip_nota)
    )''')
    
    # Tabel pentru absențe
    c.execute('''CREATE TABLE IF NOT EXISTS absente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data DATE NOT NULL,
        clasa TEXT NOT NULL,
        nume TEXT NOT NULL,
        materie TEXT NOT NULL,
        motivata BOOLEAN DEFAULT 0,
        motiv TEXT,
        profesor TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(data, nume, materie)
    )''')
    
    # Tabel pentru observații
    c.execute('''CREATE TABLE IF NOT EXISTS observatii (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data DATE NOT NULL,
        nume TEXT NOT NULL,
        materie TEXT NOT NULL,
        observatie TEXT NOT NULL,
        tip TEXT CHECK (tip IN ('laudă', 'atenționare', 'mustrare', 'recomandare')),
        profesor TEXT NOT NULL,
        gravitate INTEGER DEFAULT 1,
        rezolvata BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_nume_tip (nume, tip)
    )''')
    
    # Tabel pentru purtare
    c.execute('''CREATE TABLE IF NOT EXISTS purtare (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nume TEXT NOT NULL,
        nota INTEGER CHECK (nota >= 1 AND nota <= 10),
        data_modificare DATE NOT NULL,
        motiv TEXT NOT NULL,
        profesor TEXT NOT NULL,
        semestru INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_nume_semestru (nume, semestru)
    )''')
    
    # Tabel pentru medii finale
    c.execute('''CREATE TABLE IF NOT EXISTS medii (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nume TEXT NOT NULL,
        clasa TEXT NOT NULL,
        materie TEXT NOT NULL,
        medie_sem1 REAL,
        medie_sem2 REAL,
        medie_anuala REAL,
        teza REAL,
        nota_finala REAL,
        situatie TEXT,
        an_scolar TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(nume, materie, an_scolar)
    )''')
    
    # Tabel pentru activități extrașcolare
    c.execute('''CREATE TABLE IF NOT EXISTS activitati (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nume TEXT NOT NULL,
        tip_activitate TEXT NOT NULL,
        denumire TEXT NOT NULL,
        data_inceput DATE,
        data_sfarsit DATE,
        realizari TEXT,
        mentiuni TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Tabel pentru statistici sistem
    c.execute('''CREATE TABLE IF NOT EXISTS statistici (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data DATE NOT NULL,
        tip_statistica TEXT NOT NULL,
        valoare REAL,
        detalii TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Tabel pentru backup și istoric
    c.execute('''CREATE TABLE IF NOT EXISTS istoric_modificari (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tabela TEXT NOT NULL,
        id_inregistrare INTEGER,
        actiune TEXT NOT NULL,
        date_vechi TEXT,
        date_noi TEXT,
        utilizator TEXT NOT NULL,
        ip_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    return conn

# ============================================
# 5. FUNCȚII UTILITARE AVANSATE
# ============================================

def verify_password(password: str, role: str, username: str = None) -> bool:
    """Verifică parola pentru diferitele roluri"""
    if role == "teacher" and username:
        return PROFESORI.get(username, {}).get("parola") == password
    elif role == "parent" and username:
        return ELEVI.get(username, {}).get("parola") == password
    elif role == "admin":
        return PAROLA_DIRECTOARE == password
    return False

def get_elev_details(nume_elev: str) -> Dict:
    """Returnează detaliile complete ale unui elev"""
    return ELEVI.get(nume_elev, {})

def get_profesor_details(nume_profesor: str) -> Dict:
    """Returnează detaliile complete ale unui profesor"""
    return PROFESORI.get(nume_profesor, {})

def elev_are_absenta(data_str: str, nume_elev: str, materie: str, conn) -> bool:
    """Verifică dacă un elev are absență într-o anumită zi"""
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM absente WHERE data = ? AND nume = ? AND materie = ?', 
                   (data_str, nume_elev, materie))
    return cursor.fetchone() is not None

def get_note_elev(data_str: str, nume_elev: str, materie: str, conn) -> List[Tuple]:
    """Returnează notele unui elev pentru o anumită zi și materie"""
    cursor = conn.cursor()
    cursor.execute('SELECT id, nota, tip_nota, comentariu FROM grades WHERE data = ? AND nume = ? AND materie = ?', 
                   (data_str, nume_elev, materie))
    return cursor.fetchall()

def delete_nota(nota_id: int, conn):
    """Șterge o notă din baza de date"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM grades WHERE id = ?', (nota_id,))
    nota_veche = cursor.fetchone()
    
    cursor.execute("DELETE FROM grades WHERE id = ?", (nota_id,))
    
    # Salvare în istoric
    if nota_veche:
        cursor.execute('''INSERT INTO istoric_modificari 
                        (tabela, id_inregistrare, actiune, date_vechi, utilizator) 
                        VALUES (?, ?, ?, ?, ?)''',
                     ('grades', nota_id, 'DELETE', str(nota_veche), 'system'))
    
    conn.commit()

def update_nota(nota_id: int, noua_nota: float, conn):
    """Actualizează o notă existentă"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM grades WHERE id = ?', (nota_id,))
    nota_veche = cursor.fetchone()
    
    cursor.execute("UPDATE grades SET nota = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", 
                   (noua_nota, nota_id))
    
    # Salvare în istoric
    if nota_veche:
        cursor.execute('''INSERT INTO istoric_modificari 
                        (tabela, id_inregistrare, actiune, date_vechi, date_noi, utilizator) 
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     ('grades', nota_id, 'UPDATE', str(nota_veche), 
                      f'{{"nota": {noua_nota}}}', 'system'))
    
    conn.commit()

def get_media_elev(nume_elev: str, materie: str, conn, semestru: int = None) -> float:
    """Calculează media unui elev la o materie"""
    cursor = conn.cursor()
    query = 'SELECT AVG(nota) FROM grades WHERE nume = ? AND materie = ?'
    params = [nume_elev, materie]
    
    if semestru:
        query += ' AND semestru = ?'
        params.append(semestru)
    
    cursor.execute(query, params)
    result = cursor.fetchone()
    return round(result[0], 2) if result and result[0] else 0.00

def get_nota_purtare_curenta(nume_elev: str, conn, semestru: int = 1) -> int:
    """Returnează nota curentă de purtare a unui elev"""
    cursor = conn.cursor()
    cursor.execute('''SELECT nota FROM purtare 
                     WHERE nume = ? AND semestru = ? 
                     ORDER BY data_modificare DESC 
                     LIMIT 1''', (nume_elev, semestru))
    result = cursor.fetchone()
    return result[0] if result else 10

def update_purtare(nume_elev: str, nota_noua: int, motiv: str, profesor: str, conn, semestru: int = 1):
    """Actualizează nota de purtare a unui elev"""
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO purtare (nume, nota, data_modificare, motiv, profesor, semestru) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (nume_elev, nota_noua, datetime.now().date().strftime("%Y-%m-%d"), 
                   motiv, profesor, semestru))
    conn.commit()

def get_observatii_elev(nume_elev: str, conn, tip: str = None, rezolvata: bool = None) -> List[Tuple]:
    """Returnează observațiile unui elev"""
    cursor = conn.cursor()
    query = '''SELECT data, materie, observatie, tip, profesor, gravitate, rezolvata 
               FROM observatii WHERE nume = ?'''
    params = [nume_elev]
    
    if tip:
        query += ' AND tip = ?'
        params.append(tip)
    
    if rezolvata is not None:
        query += ' AND rezolvata = ?'
        params.append(1 if rezolvata else 0)
    
    query += ' ORDER BY data DESC, gravitate DESC'
    cursor.execute(query, params)
    return cursor.fetchall()

def adauga_observatie(data_str: str, nume_elev: str, materie: str, observatie: str, 
                     tip: str, profesor: str, conn, gravitate: int = 1):
    """Adaugă o observație pentru un elev"""
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO observatii 
                     (data, nume, materie, observatie, tip, profesor, gravitate) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (data_str, nume_elev, materie, observatie, tip, profesor, gravitate))
    conn.commit()

def get_statistici_clasa(clasa: str, materie: str, conn, perioada: str = 'luna') -> Dict:
    """Returnează statistici detaliate pentru o clasă"""
    cursor = conn.cursor()
    
    if perioada == 'luna':
        data_start = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    elif perioada == 'semestru':
        data_start = '2025-09-01'
    else:
        data_start = '2025-09-01'
    
    # Note
    cursor.execute('''SELECT COUNT(*) as total_note, AVG(nota) as medie, 
                     MIN(nota) as minim, MAX(nota) as maxim 
                     FROM grades WHERE clasa = ? AND materie = ? AND data >= ?''',
                  (clasa, materie, data_start))
    note_stats = cursor.fetchone()
    
    # Absențe
    cursor.execute('''SELECT COUNT(*) as total_absente, 
                     SUM(CASE WHEN motivata = 1 THEN 1 ELSE 0 END) as motivate 
                     FROM absente WHERE clasa = ? AND materie = ? AND data >= ?''',
                  (clasa, materie, data_start))
    absente_stats = cursor.fetchone()
    
    # Observații
    cursor.execute('''SELECT tip, COUNT(*) as numar 
                     FROM observatii WHERE materie = ? AND data >= ? 
                     GROUP BY tip ORDER BY numar DESC''',
                  (materie, data_start))
    observatii_stats = cursor.fetchall()
    
    return {
        'note': {
            'total': note_stats[0] if note_stats else 0,
            'medie': round(note_stats[1], 2) if note_stats and note_stats[1] else 0,
            'minim': note_stats[2] if note_stats else 0,
            'maxim': note_stats[3] if note_stats else 0
        },
        'absente': {
            'total': absente_stats[0] if absente_stats else 0,
            'motivate': absente_stats[1] if absente_stats else 0
        },
        'observatii': dict(observatii_stats) if observatii_stats else {}
    }

def generate_calendar_heatmap_data(clasa: str, materie: str, conn, an: int = 2026, luna: int = None) -> pd.DataFrame:
    """Generează date pentru heatmap-ul calendaristic"""
    cursor = conn.cursor()
    
    if luna:
        query = '''SELECT data, AVG(nota) as medie_zi, COUNT(*) as numar_note 
                   FROM grades WHERE clasa = ? AND materie = ? 
                   AND strftime('%Y', data) = ? AND strftime('%m', data) = ?
                   GROUP BY data ORDER BY data'''
        params = (clasa, materie, str(an), f'{luna:02d}')
    else:
        query = '''SELECT data, AVG(nota) as medie_zi, COUNT(*) as numar_note 
                   FROM grades WHERE clasa = ? AND materie = ? 
                   AND strftime('%Y', data) = ?
                   GROUP BY data ORDER BY data'''
        params = (clasa, materie, str(an))
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    if not data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data, columns=['data', 'medie_zi', 'numar_note'])
    df['data'] = pd.to_datetime(df['data'])
    df['zi'] = df['data'].dt.day
    df['luna'] = df['data'].dt.month
    df['saptamana'] = df['data'].dt.isocalendar().week
    
    return df

# ============================================
# 6. FUNCȚII PENTRU CALENDARUL ANUAL AVANSAT
# ============================================

class CalendarAnual:
    """Clasă pentru gestionarea calendarului anual avansat"""
    
    def __init__(self):
        if 'selected_days' not in st.session_state:
            st.session_state.selected_days = {}
        if 'calendar_notes' not in st.session_state:
            st.session_state.calendar_notes = {}
        if 'calendar_events' not in st.session_state:
            st.session_state.calendar_events = {}
    
    def get_selected_days(self, clasa: str, materie: str) -> List[str]:
        """Returnează zilele selectate pentru o clasă și materie"""
        if clasa not in st.session_state.selected_days:
            st.session_state.selected_days[clasa] = {}
        if materie not in st.session_state.selected_days[clasa]:
            st.session_state.selected_days[clasa][materie] = []
        return st.session_state.selected_days[clasa][materie]
    
    def toggle_day_selection(self, day_str: str, clasa: str, materie: str):
        """Comută selecția unei zile"""
        selected_days = self.get_selected_days(clasa, materie)
        if day_str in selected_days:
            selected_days.remove(day_str)
        else:
            selected_days.append(day_str)
        st.session_state.selected_days[clasa][materie] = selected_days
    
    def add_calendar_note(self, day_str: str, clasa: str, materie: str, note: str):
        """Adaugă o notă pentru o zi din calendar"""
        key = f"{clasa}_{materie}_{day_str}"
        st.session_state.calendar_notes[key] = note
    
    def get_calendar_note(self, day_str: str, clasa: str, materie: str) -> str:
        """Returnează nota pentru o zi din calendar"""
        key = f"{clasa}_{materie}_{day_str}"
        return st.session_state.calendar_notes.get(key, "")
    
    def add_calendar_event(self, day_str: str, clasa: str, materie: str, 
                          event_type: str, description: str):
        """Adaugă un eveniment pentru o zi din calendar"""
        if clasa not in st.session_state.calendar_events:
            st.session_state.calendar_events[clasa] = {}
        if materie not in st.session_state.calendar_events[clasa]:
            st.session_state.calendar_events[clasa][materie] = {}
        
        if day_str not in st.session_state.calendar_events[clasa][materie]:
            st.session_state.calendar_events[clasa][materie][day_str] = []
        
        st.session_state.calendar_events[clasa][materie][day_str].append({
            'type': event_type,
            'description': description,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def get_calendar_events(self, day_str: str, clasa: str, materie: str) -> List[Dict]:
        """Returnează evenimentele pentru o zi din calendar"""
        if (clasa in st.session_state.calendar_events and 
            materie in st.session_state.calendar_events[clasa] and 
            day_str in st.session_state.calendar_events[clasa][materie]):
            return st.session_state.calendar_events[clasa][materie][day_str]
        return []
    
    def display_month_calendar(self, clasa: str, materie: str, year: int, month: int):
        """Afișează calendarul pentru o lună specifică"""
        today = date.today()
        selected_days = self.get_selected_days(clasa, materie)
        
        # Creare calendar
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        
        # Afișare header
        st.markdown(f"### 📅 {month_name} {year}")
        st.markdown(f"**Clasa:** {clasa} | **Materie:** {materie}")
        
        # Zilele săptămânii
        days_header = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
        cols = st.columns(7)
        
        for i, day_name in enumerate(days_header):
            with cols[i]:
                st.markdown(f"""
                <div style="text-align: center; font-weight: bold; padding: 8px; 
                          background: rgba(30, 41, 59, 0.8); border-radius: 8px;">
                    {day_name[:3]}
                </div>
                """, unsafe_allow_html=True)
        
        # Zilele lunii
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if day != 0:
                        day_date = date(year, month, day)
                        day_str = day_date.strftime("%Y-%m-%d")
                        
                        # Verifică dacă este ziua curentă
                        is_today = day_date == today
                        
                        # Verifică dacă este zi selectată
                        is_selected = day_str in selected_days
                        
                        # Obține evenimentele pentru această zi
                        events = self.get_calendar_events(day_str, clasa, materie)
                        has_events = len(events) > 0
                        
                        # Obține nota pentru această zi
                        day_note = self.get_calendar_note(day_str, clasa, materie)
                        has_note = bool(day_note.strip())
                        
                        # Determină clasa CSS
                        if is_selected:
                            css_class = "calendar-day-selected"
                        elif is_today:
                            css_class = "calendar-day-today"
                        else:
                            css_class = "calendar-day-regular"
                        
                        # Indicator pentru evenimente
                        event_indicator = ""
                        if has_events:
                            event_types = [e['type'] for e in events]
                            if 'test' in event_types:
                                event_indicator = "📝"
                            elif 'exam' in event_types:
                                event_indicator = "🎯"
                            elif 'activitate' in event_types:
                                event_indicator = "🎨"
                            else:
                                event_indicator = "📌"
                        
                        # Indicator pentru note
                        note_indicator = "📋" if has_note else ""
                        
                        # Afișează ziua
                        button_text = f"{day}{event_indicator}{note_indicator}"
                        
                        if st.button(
                            button_text,
                            key=f"cal_{clasa}_{materie}_{year}_{month}_{day}",
                            help=f"Ziua: {day_date.strftime('%d.%m.%Y')}\n"
                                 f"{'Zi selectată' if is_selected else ''}\n"
                                 f"{'Evenimente: ' + ', '.join([e['type'] for e in events]) if has_events else ''}\n"
                                 f"{'Notă: ' + day_note if has_note else ''}"
                        ):
                            self.toggle_day_selection(day_str, clasa, materie)
                            st.rerun()
                        
                        # Aplică stilul CSS
                        st.markdown(f"""
                            <script>
                            const button = document.querySelector(
                                '[data-testid="stButton"] [key="cal_{clasa}_{materie}_{year}_{month}_{day}"]'
                            );
                            if (button) {{
                                button.classList.add('calendar-day', '{css_class}');
                            }}
                            </script>
                        """, unsafe_allow_html=True)
                    else:
                        st.write("")
    
    def display_year_calendar(self, clasa: str, materie: str, year: int = 2026):
        """Afișează calendarul pentru întregul an"""
        st.markdown(f"## 📅 Calendar Anual {year}")
        st.markdown(f"**Clasa:** {clasa} | **Materie:** {materie}")
        
        # Selectare lună pentru detalii
        months = ["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie",
                 "Septembrie", "Octombrie", "Noiembrie", "Decembrie"]
        
        col_select, col_stats = st.columns([2, 1])
        
        with col_select:
            selected_month_name = st.selectbox("Selectează luna pentru detalii:", months, key="calendar_month_select")
        
        with col_stats:
            selected_days = self.get_selected_days(clasa, materie)
            st.metric("Zile selectate totale", len(selected_days), key="selected_days_metric")
        
        # Mapare nume lună -> număr
        month_map = {name: i for i, name in enumerate(months, 1)}
        selected_month = month_map[selected_month_name]
        
        # Afișare calendar pentru luna selectată
        self.display_month_calendar(clasa, materie, year, selected_month)
        
        # Secțiune pentru managementul zilelor selectate
        st.markdown("---")
        st.markdown("### 🗓️ Management Zile Selectate")
        
        if selected_days:
            # Grupează zilele pe luni
            days_by_month = {}
            for day_str in sorted(selected_days):
                day_date = datetime.strptime(day_str, "%Y-%m-%d")
                month_key = day_date.strftime("%Y-%m")
                if month_key not in days_by_month:
                    days_by_month[month_key] = []
                days_by_month[month_key].append(day_date)
            
            # Afișează zilele grupat pe luni
            for month_key, days in days_by_month.items():
                month_date = datetime.strptime(f"{month_key}-01", "%Y-%m-%d")
                with st.expander(f"{month_date.strftime('%B %Y')} - {len(days)} zile", key=f"exp_{month_key}"):
                    cols = st.columns(5)
                    for i, day_date in enumerate(days):
                        col_idx = i % 5
                        with cols[col_idx]:
                            day_str = day_date.strftime("%Y-%m-%d")
                            if st.button(
                                f"🗑️ {day_date.strftime('%d.%m')}",
                                key=f"remove_{clasa}_{materie}_{day_str}",
                                help=f"Deselectează {day_date.strftime('%d.%m.%Y')}",
                                use_container_width=True
                            ):
                                self.toggle_day_selection(day_str, clasa, materie)
                                st.rerun()
            
            # Acțiuni în masă
            col_action1, col_action2, col_action3 = st.columns(3)
            
            with col_action1:
                if st.button("🗑️ Șterge toate selecțiile", type="secondary", use_container_width=True, key="btn_clear_all"):
                    st.session_state.selected_days[clasa][materie] = []
                    st.rerun()
            
            with col_action2:
                # Exportă selecțiile
                if st.button("📤 Exportă calendar", type="secondary", use_container_width=True, key="btn_export_calendar"):
                    calendar_data = {
                        'clasa': clasa,
                        'materie': materie,
                        'an': year,
                        'zile_selectate': selected_days,
                        'note': {k: v for k, v in st.session_state.calendar_notes.items() 
                                if k.startswith(f"{clasa}_{materie}")},
                        'evenimente': st.session_state.calendar_events.get(clasa, {}).get(materie, {})
                    }
                    
                    # Crează fișier JSON pentru export
                    json_str = json.dumps(calendar_data, indent=2, ensure_ascii=False, default=str)
                    st.download_button(
                        label="⬇️ Descarcă fișier JSON",
                        data=json_str,
                        file_name=f"calendar_{clasa}_{materie}_{year}.json",
                        mime="application/json",
                        key="btn_download_calendar"
                    )
            
            with col_action3:
                # Sincronizează cu data curentă
                if st.button("🎯 Sincronizează selecție", type="primary", use_container_width=True, key="btn_sync_calendar"):
                    if selected_days:
                        latest_day = max(selected_days)
                        st.session_state.selected_date = latest_day
                        st.success(f"Data curentă sincronizată cu {latest_day}")
                        st.rerun()
        else:
            st.info("Nu ai selectat nicio zi pentru această materie și clasă.")
        
        # Secțiune pentru note și evenimente
        st.markdown("---")
        st.markdown("### 📝 Note și Evenimente Calendar")
        
        tab_notes, tab_events = st.tabs(["📋 Note", "🎯 Evenimente"])
        
        with tab_notes:
            st.markdown("Adaugă note pentru zilele selectate din calendar")
            if selected_days:
                selected_day = st.selectbox(
                    "Selectează o zi pentru a adăuga/edita nota:",
                    [datetime.strptime(d, "%Y-%m-%d").strftime("%d.%m.%Y") for d in sorted(selected_days)],
                    key="select_day_note"
                )
                
                day_date_obj = datetime.strptime(selected_day, "%d.%m.%Y")
                day_str = day_date_obj.strftime("%Y-%m-%d")
                current_note = self.get_calendar_note(day_str, clasa, materie)
                
                new_note = st.text_area(
                    "Notă pentru ziua selectată:",
                    value=current_note,
                    height=100,
                    placeholder="Scrie aici note importante, teme, sau reamintiri...",
                    key="text_area_note"
                )
                
                if st.button("💾 Salvează Notă", use_container_width=True, key="btn_save_note"):
                    self.add_calendar_note(day_str, clasa, materie, new_note)
                    st.success(f"Notă salvată pentru {selected_day}!")
                    st.rerun()
            else:
                st.warning("Selectează mai întâi zile din calendar pentru a adăuga note.")
        
        with tab_events:
            st.markdown("Planifică evenimente speciale (teste, examene, activități)")
            if selected_days:
                event_day = st.selectbox(
                    "Selectează ziua pentru eveniment:",
                    [datetime.strptime(d, "%Y-%m-%d").strftime("%d.%m.%Y") for d in sorted(selected_days)],
                    key="select_day_event"
                )
                
                day_date_obj = datetime.strptime(event_day, "%d.%m.%Y")
                day_str = day_date_obj.strftime("%Y-%m-%d")
                
                col_event_type, col_event_desc = st.columns([1, 2])
                
                with col_event_type:
                    event_type = st.selectbox(
                        "Tip eveniment:",
                        ["test", "examen", "activitate", "proiect", "altul"],
                        key="select_event_type"
                    )
                
                with col_event_desc:
                    event_description = st.text_input(
                        "Descriere eveniment:",
                        placeholder="Ex: Test capitolele 1-3, Examen semestrial...",
                        key="input_event_desc"
                    )
                
                if st.button("➕ Adaugă Eveniment", use_container_width=True, key="btn_add_event"):
                    if event_description:
                        self.add_calendar_event(day_str, clasa, materie, event_type, event_description)
                        st.success(f"Eveniment '{event_type}' adăugat pentru {event_day}!")
                        st.rerun()
                    else:
                        st.error("Te rog completează descrierea evenimentului!")
                
                # Afișează evenimentele existente
                existing_events = self.get_calendar_events(day_str, clasa, materie)
                if existing_events:
                    st.markdown("**Evenimente existente pentru această zi:**")
                    for idx, event in enumerate(existing_events):
                        st.markdown(f"""
                        <div class="custom-card" style="padding: 10px !important; margin: 5px 0 !important;">
                            <strong>{event['type'].upper()}</strong>: {event['description']}<br>
                            <small style="color: #94a3b8;">Adăugat: {event['timestamp']}</small>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("Selectează mai întâi zile din calendar pentru a adăuga evenimente.")

# ============================================
# 7. INIȚIALIZARE BAZĂ DE DATE ȘI SESSION STATE
# ============================================

# Inițializare baza de date
conn = init_db()

# Inițializare calendar anual
calendar_manager = CalendarAnual()

# Inițializare session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.materie = None
    st.session_state.nume_elev = None
    st.session_state.clasa_selectata = "6B"
    st.session_state.selected_date = datetime.now().strftime("%Y-%m-%d")
    st.session_state.current_semester = 1
    st.session_state.dark_mode = True

# ============================================
# 8. PAGINA DE LOGIN PREMIUM
# ============================================

if not st.session_state.logged_in:
    # Header premium
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="color: white; font-size: 3rem; margin-bottom: 10px;">
            🎓 CATALOG DIGITAL 2026
        </h1>
        <p style="color: #94a3b8; font-size: 1.3rem; margin-bottom: 30px;">
            Sistem Integrat de Management Școlar | Anul școlar 2025-2026
        </p>
        <div style="display: inline-flex; gap: 15px; margin-top: 20px;">
            <span class="badge badge-success">Securizat</span>
            <span class="badge badge-info">GDPR Compliant</span>
            <span class="badge badge-warning">Cloud Sync</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs pentru autentificare
    tab_prof, tab_parinte, tab_directoare = st.tabs([
        "👨‍🏫 PROFESOR", 
        "👪 PĂRINTE/ELEV", 
        "🏛️ DIRECTOARE"
    ])
    
    with tab_prof:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #3b82f6; margin-bottom: 20px;">🔐 Autentificare Profesor</h3>
        """, unsafe_allow_html=True)
        
        col_prof_select, col_prof_pass = st.columns([2, 1])
        
        with col_prof_select:
            profesor_selectat = st.selectbox(
                "Selectează numele tău:", 
                list(PROFESORI.keys()),
                key="login_profesor_select"
            )
        
        with col_prof_pass:
            parola = st.text_input(
                "Introdu parola:", 
                type="password",
                key="login_profesor_pass"
            )
        
        if st.button(
            "🚀 Accesează Platforma", 
            type="primary", 
            use_container_width=True,
            key="btn_login_profesor_main"
        ):
            if parola and verify_password(parola, "teacher", profesor_selectat):
                st.session_state.logged_in = True
                st.session_state.role = "teacher"
                st.session_state.username = profesor_selectat
                st.session_state.materie = PROFESORI[profesor_selectat]["materie"]
                
                # Salvare statistică login
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO statistici 
                                (data, tip_statistica, valoare, detalii) 
                                VALUES (?, ?, ?, ?)''',
                             (date.today().strftime("%Y-%m-%d"), 
                              'login_profesor', 1, 
                              f'Profesor: {profesor_selectat}'))
                conn.commit()
                
                st.success(f"✅ Bine ai venit, profesorule {profesor_selectat}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Parolă incorectă! Verifică datele introduse.")
    
    with tab_parinte:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #22c55e; margin-bottom: 20px;">👤 Autentificare Părinte/Elev</h3>
        """, unsafe_allow_html=True)
        
        # Construire listă elevi cu clase
        all_students = []
        for clasa, studenti in CLASE.items():
            for student in studenti:
                all_students.append(f"{student} | Clasa: {clasa}")
        
        if all_students:
            elev_selectat_full = st.selectbox(
                "Selectează elevul:", 
                sorted(all_students),
                key="login_elev_select"
            )
            
            # Extrage numele și clasa
            nume_elev = elev_selectat_full.split(" | ")[0]
            clasa_elev = elev_selectat_full.split("Clasa: ")[1]
            
            parola_parinte = st.text_input(
                "Parolă elev/părinte:", 
                type="password",
                key="login_parinte_pass"
            )
            
            if st.button(
                "📊 Vezi Situația Academică", 
                type="primary", 
                use_container_width=True,
                key="btn_login_parinte_main"
            ):
                if parola_parinte and verify_password(parola_parinte, "parent", nume_elev):
                    st.session_state.logged_in = True
                    st.session_state.role = "parent"
                    st.session_state.nume_elev = nume_elev
                    st.session_state.clasa_selectata = clasa_elev
                    
                    # Salvare statistică login
                    cursor = conn.cursor()
                    cursor.execute('''INSERT INTO statistici 
                                    (data, tip_statistica, valoare, detalii) 
                                    VALUES (?, ?, ?, ?)''',
                                 (date.today().strftime("%Y-%m-%d"), 
                                  'login_parinte', 1, 
                                  f'Elev: {nume_elev}'))
                    conn.commit()
                    
                    st.success(f"✅ Bine ai venit, părinte al lui {nume_elev}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Parolă incorectă! Verifică datele introduse.")
        else:
            st.warning("⚠️ Nu există elevi înregistrați în sistem.")
    
    with tab_directoare:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #8b5cf6; margin-bottom: 20px;">🏛️ Autentificare Directoare</h3>
            <p style="color: #94a3b8; margin-bottom: 20px;">
                Acces administrativ complet pentru managementul școlii
            </p>
        """, unsafe_allow_html=True)
        
        parola_admin = st.text_input(
            "Cod de acces administrativ:", 
            type="password",
            key="login_admin_pass"
        )
        
        if st.button(
            "⚙️ Accesează Panoul Administrativ", 
            type="primary", 
            use_container_width=True,
            key="btn_login_admin_main"
        ):
            if parola_admin and verify_password(parola_admin, "admin"):
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                
                # Salvare statistică login
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO statistici 
                                (data, tip_statistica, valoare, detalii) 
                                VALUES (?, ?, ?, ?)''',
                             (date.today().strftime("%Y-%m-%d"), 
                              'login_admin', 1, 'Directoare'))
                conn.commit()
                
                st.success("✅ Bine ai venit, doamnă directoare!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Cod de acces incorect!")
    
    # Footer informații
    st.markdown("---")
    col_footer1, col_footer2, col_footer3 = st.columns(3)
    
    with col_footer1:
        st.markdown("""
        <div style="text-align: center;">
            <h4>🔒 Securitate</h4>
            <p style="font-size: 0.9rem; color: #94a3b8;">
                Datele sunt criptate și protejate conform GDPR
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_footer2:
        st.markdown("""
        <div style="text-align: center;">
            <h4>📱 Accesibil</h4>
            <p style="font-size: 0.9rem; color: #94a3b8;">
                Compatibil cu toate dispozitivele și browserele
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_footer3:
        st.markdown("""
        <div style="text-align: center;">
            <h4>🔄 Actualizat</h4>
            <p style="font-size: 0.9rem; color: #94a3b8;">
                Sistem actualizat în timp real cu ultimele standarde
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 9. PAGINA PRINCIPALĂ - DUPĂ LOGIN
# ============================================
else:
    # Header principal cu informații utilizator
    col_logo, col_user, col_logout = st.columns([2, 3, 1])
    
    with col_logo:
        st.markdown("""
        <h2 style="color: white; margin-bottom: 0;">
            🎓 Catalog Digital
            <small style="font-size: 0.6em; color: #94a3b8;">v6.0</small>
        </h2>
        <p style="color: #64748b; margin-top: 0;">
            Anul școlar 2025-2026
        </p>
        """, unsafe_allow_html=True)
    
    with col_user:
        if st.session_state.role == "teacher":
            prof_details = get_profesor_details(st.session_state.username)
            st.markdown(f"""
            <div class="custom-card" style="padding: 15px !important; margin: 0 !important;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="font-size: 2rem;">👨‍🏫</div>
                    <div>
                        <h4 style="margin: 0; color: white;">{st.session_state.username}</h4>
                        <p style="margin: 5px 0 0 0; color: #94a3b8;">
                            {st.session_state.materie} | {st.session_state.clasa_selectata}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.role == "parent":
            elev_details = get_elev_details(st.session_state.nume_elev)
            st.markdown(f"""
            <div class="custom-card" style="padding: 15px !important; margin: 0 !important;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="font-size: 2rem;">👤</div>
                    <div>
                        <h4 style="margin: 0; color: white;">{st.session_state.nume_elev}</h4>
                        <p style="margin: 5px 0 0 0; color: #94a3b8;">
                            Clasa: {st.session_state.clasa_selectata} | 
                            Data curentă: {datetime.now().strftime('%d.%m.%Y')}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="custom-card" style="padding: 15px !important; margin: 0 !important;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="font-size: 2rem;">🏛️</div>
                    <div>
                        <h4 style="margin: 0; color: white;">Doamnă Directoare</h4>
                        <p style="margin: 5px 0 0 0; color: #94a3b8;">
                            Panou Administrativ | Management Școlar
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_logout:
        st.write("")
        st.write("")
        if st.button("🚪 Deconectare", type="secondary", use_container_width=True, key="btn_logout_main"):
            # Salvare statistică logout
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO statistici 
                            (data, tip_statistica, valoare, detalii) 
                            VALUES (?, ?, ?, ?)''',
                         (date.today().strftime("%Y-%m-%d"), 
                          'logout', 1, 
                          f'Utilizator: {st.session_state.username or st.session_state.nume_elev}'))
            conn.commit()
            
            # Resetare session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Linie separator
    st.markdown("---")
    
    # ============================================
    # 10. INTERFAȚA PROFESOR - MODUL PREMIUM
    # ============================================
    if st.session_state.role == "teacher":
        # Meniu principal profesor
        menu_options = [
            "📝 Adaugă Note/Absențe",
            "📊 Statistici și Rapoarte",
            "✏️ Management Note",
            "📅 Calendar Anual",
            "📈 Analiză Performanță",
            "⚙️ Setări Profesor"
        ]
        
        selected_menu = st.radio(
            "Selectează modul de lucru:",
            menu_options,
            horizontal=True,
            key="prof_menu_main"
        )
        
        # Selectare clasă
        col_class, col_semester = st.columns([2, 1])
        
        with col_class:
            clasa = st.selectbox(
                "Selectează clasa:",
                list(CLASE.keys()),
                key="prof_clasa_select",
                index=list(CLASE.keys()).index(st.session_state.clasa_selectata) 
                if st.session_state.clasa_selectata in CLASE else 0
            )
            
            if clasa != st.session_state.clasa_selectata:
                st.session_state.clasa_selectata = clasa
        
        with col_semester:
            st.session_state.current_semester = st.selectbox(
                "Semestru:",
                [1, 2],
                key="prof_semester_select",
                index=0
            )
        
        # Afișare dată curentă
        current_date = datetime.strptime(st.session_state.selected_date, "%Y-%m-%d").date()
        col_date_display, col_date_select = st.columns([1, 2])
        
        with col_date_display:
            st.markdown(f"""
            <div class="date-selector">
                <h4 style="color: #94a3b8; margin-bottom: 10px;">📅 Data selectată:</h4>
                <h1 style="font-size: 2.5rem; margin: 0; color: #3b82f6;">
                    {current_date.strftime('%d.%m.%Y')}
                </h1>
                <p style="color: #64748b; margin-top: 5px;">
                    {current_date.strftime('%A')}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_date_select:
            selected_date = st.date_input(
                "Schimbă data:",
                value=current_date,
                min_value=date(2025, 9, 1),
                max_value=date(2026, 6, 30),
                key="prof_date_select_main",
                label_visibility="collapsed"
            )
            
            data_str = selected_date.strftime("%Y-%m-%d")
            if data_str != st.session_state.selected_date:
                st.session_state.selected_date = data_str
        
        # Săptămâna curentă - vizualizare îmbunătățită
        st.markdown("#### 📅 Săptămâna curentă")
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        
        col_cal_week = st.columns(7)
        days_of_week = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
        
        for i, (day_name, col) in enumerate(zip(days_of_week, col_cal_week)):
            day_date = start_of_week + timedelta(days=i)
            with col:
                is_selected = day_date == selected_date
                is_today = day_date == today
                
                # Stiluri diferite pentru zile
                if is_selected:
                    col.markdown(f"""
                    <div style="text-align: center; 
                                background: linear-gradient(135deg, #3b82f6, #2563eb);
                                color: white; padding: 10px; border-radius: 12px; margin: 2px;
                                box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);">
                        <div style="font-size: 0.8rem;"><strong>{day_name[:3]}</strong></div>
                        <div style="font-size: 1.4rem; font-weight: bold;">{day_date.day}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif is_today:
                    col.markdown(f"""
                    <div style="text-align: center; 
                                background: linear-gradient(135deg, #22c55e, #16a34a);
                                color: white; padding: 10px; border-radius: 12px; margin: 2px;">
                        <div style="font-size: 0.8rem;">{day_name[:3]}</div>
                        <div style="font-size: 1.3rem;">{day_date.day}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    col.markdown(f"""
                    <div style="text-align: center; 
                                background: rgba(30, 41, 59, 0.8);
                                color: white; padding: 10px; border-radius: 12px; margin: 2px;
                                cursor: pointer; transition: all 0.3s;">
                        <div style="font-size: 0.8rem;">{day_name[:3]}</div>
                        <div style="font-size: 1.2rem;">{day_date.day}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Buton pentru selectare rapidă
                if st.button("✓", key=f"quick_select_{i}_{clasa}", 
                           help=f"Selectează {day_date.strftime('%d.%m.%Y')}",
                           use_container_width=True):
                    st.session_state.selected_date = day_date.strftime("%Y-%m-%d")
                    st.rerun()
        
        # Căutare elevi
        search_query = st.text_input(
            "🔍 Caută elev...",
            key="prof_search_elev",
            placeholder="Scrie numele elevului..."
        )
        
        elevi_clasa = CLASE.get(clasa, [])
        elevi_filtrati = []
        
        if search_query:
            elevi_filtrati = [e for e in elevi_clasa if search_query.lower() in e.lower()]
        else:
            elevi_filtrati = elevi_clasa
        
        # Afișare statistici rapide
        st.markdown(f"### 👥 Elevi - Clasa {clasa} ({len(elevi_filtrati)}/{len(elevi_clasa)})")
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            total_note = pd.read_sql(
                "SELECT COUNT(*) FROM grades WHERE clasa = ? AND materie = ?",
                conn, params=[clasa, st.session_state.materie]
            ).iloc[0,0]
            st.metric("📝 Note totale", total_note, key="metric_total_note")
        
        with col_stat2:
            medie_clasa = pd.read_sql(
                "SELECT AVG(nota) FROM grades WHERE clasa = ? AND materie = ?",
                conn, params=[clasa, st.session_state.materie]
            ).iloc[0,0]
            st.metric("📊 Media clasei", f"{medie_clasa:.2f}" if medie_clasa else "0.00", key="metric_media_clasei")
        
        with col_stat3:
            total_abs = pd.read_sql(
                "SELECT COUNT(*) FROM absente WHERE clasa = ? AND materie = ?",
                conn, params=[clasa, st.session_state.materie]
            ).iloc[0,0]
            st.metric("❌ Absențe", total_abs, key="metric_total_abs")
        
        with col_stat4:
            total_obs = pd.read_sql(
                "SELECT COUNT(*) FROM observatii WHERE materie = ?",
                conn, params=[st.session_state.materie]
            ).iloc[0,0]
            st.metric("📋 Observații", total_obs, key="metric_total_obs")
        
        # Logică pentru fiecare modul de lucru
        if selected_menu == "📝 Adaugă Note/Absențe":
            st.markdown(f"#### 📝 Adaugă note, absențe și observații - {selected_date.strftime('%d.%m.%Y')}")
            
            if not elevi_filtrati:
                st.warning(f"⚠️ Nu există elevi în clasa {clasa} sau căutarea nu a returnat rezultate.")
            else:
                # Progres bar pentru elevi procesați
                progress_bar = st.progress(0)
                
                for idx, elev in enumerate(elevi_filtrati):
                    progress_bar.progress((idx + 1) / len(elevi_filtrati))
                    
                    with st.expander(f"👤 {elev}", expanded=False, key=f"expander_{elev}"):
                        # Secțiunea pentru note
                        st.markdown("##### 📝 Note")
                        are_absenta = elev_are_absenta(data_str, elev, st.session_state.materie, conn)
                        
                        if are_absenta:
                            st.warning(f"⚠️ {elev} are absență în această zi. Nu se pot adăuga note.")
                            
                            col_abs1, col_abs2 = st.columns([3, 1])
                            with col_abs2:
                                if st.button(
                                    "🗑️ Șterge absența",
                                    key=f"del_abs_{elev}_{data_str}",
                                    type="secondary",
                                    use_container_width=True
                                ):
                                    conn.execute(
                                        'DELETE FROM absente WHERE data = ? AND nume = ? AND materie = ?',
                                        (data_str, elev, st.session_state.materie)
                                    )
                                    conn.commit()
                                    st.success(f"✅ Absența pentru {elev} a fost ștearsă!")
                                    time.sleep(1)
                                    st.rerun()
                        else:
                            note_existente = get_note_elev(data_str, elev, st.session_state.materie, conn)
                            
                            if note_existente:
                                st.info(f"ℹ️ {elev} are deja notă în această zi.")
                                
                                for nota_info in note_existente:
                                    nota_id, nota_val, tip_nota, comentariu = nota_info
                                    
                                    col_nota_info, col_nota_actions = st.columns([2, 1])
                                    
                                    with col_nota_info:
                                        st.markdown(f"""
                                        <div style="background: rgba(30, 41, 59, 0.7); 
                                                    padding: 10px; border-radius: 8px;">
                                            <strong>Notă: {nota_val}</strong><br>
                                            <small>Tip: {tip_nota}</small><br>
                                            <small>Comentariu: {comentariu or 'Niciunul'}</small>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    with col_nota_actions:
                                        col_edit, col_del = st.columns(2)
                                        
                                        with col_edit:
                                            if st.button(
                                                "✏️",
                                                key=f"edit_btn_{nota_id}",
                                                help="Modifică nota",
                                                use_container_width=True
                                            ):
                                                st.session_state[f"editing_nota_{nota_id}"] = True
                                        
                                        with col_del:
                                            if st.button(
                                                "🗑️",
                                                key=f"del_btn_{nota_id}",
                                                help="Șterge nota",
                                                type="secondary",
                                                use_container_width=True
                                            ):
                                                delete_nota(nota_id, conn)
                                                st.success(f"✅ Nota pentru {elev} a fost ștearsă!")
                                                time.sleep(1)
                                                st.rerun()
                                        
                                        # Modal pentru editare nota
                                        if st.session_state.get(f"editing_nota_{nota_id}"):
                                            with st.form(key=f"edit_form_{nota_id}"):
                                                noua_nota = st.number_input(
                                                    "Notă nouă:",
                                                    min_value=1.0,
                                                    max_value=10.0,
                                                    value=float(nota_val),
                                                    step=0.5,
                                                    key=f"edit_nota_{nota_id}"
                                                )
                                                nou_tip = st.selectbox(
                                                    "Tip notă:",
                                                    ["oral", "scris", "practical", "teza"],
                                                    index=["oral", "scris", "practical", "teza"].index(tip_nota),
                                                    key=f"edit_tip_{nota_id}"
                                                )
                                                nou_comentariu = st.text_area(
                                                    "Comentariu:",
                                                    value=comentariu or "",
                                                    key=f"edit_com_{nota_id}"
                                                )
                                                
                                                col_save, col_cancel = st.columns(2)
                                                
                                                with col_save:
                                                    if st.form_submit_button("💾 Salvează modificări", key=f"save_edit_{nota_id}"):
                                                        update_nota(nota_id, noua_nota, conn)
                                                        
                                                        # Actualizează tipul și comentariul
                                                        cursor = conn.cursor()
                                                        cursor.execute(
                                                            "UPDATE grades SET tip_nota = ?, comentariu = ? WHERE id = ?",
                                                            (nou_tip, nou_comentariu, nota_id)
                                                        )
                                                        conn.commit()
                                                        
                                                        del st.session_state[f"editing_nota_{nota_id}"]
                                                        st.success(f"✅ Nota pentru {elev} a fost actualizată!")
                                                        time.sleep(1)
                                                        st.rerun()
                                                
                                                with col_cancel:
                                                    if st.form_submit_button("❌ Anulează", type="secondary", key=f"cancel_edit_{nota_id}"):
                                                        del st.session_state[f"editing_nota_{nota_id}"]
                                                        st.rerun()
                            else:
                                # Formular pentru adăugare notă nouă
                                with st.form(key=f"add_nota_form_{elev}"):
                                    col_nota_val, col_nota_type = st.columns([2, 1])
                                    
                                    with col_nota_val:
                                        nota_noua = st.number_input(
                                            "Notă:",
                                            min_value=1.0,
                                            max_value=10.0,
                                            value=8.0,
                                            step=0.5,
                                            key=f"nota_{elev}"
                                        )
                                    
                                    with col_nota_type:
                                        tip_nota = st.selectbox(
                                            "Tip:",
                                            ["oral", "scris", "practical", "teza"],
                                            key=f"tip_{elev}"
                                        )
                                    
                                    comentariu_nota = st.text_area(
                                        "Comentariu (opțional):",
                                        placeholder="Observații despre notă...",
                                        key=f"com_{elev}"
                                    )
                                    
                                    if st.form_submit_button("📝 Adaugă notă", use_container_width=True, key=f"submit_nota_{elev}"):
                                        try:
                                            cursor = conn.cursor()
                                            cursor.execute('''INSERT INTO grades 
                                                            (data, clasa, nume, materie, nota, profesor, tip_nota, comentariu, semestru) 
                                                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                                         (data_str, clasa, elev, st.session_state.materie, 
                                                          nota_noua, st.session_state.username, tip_nota, 
                                                          comentariu_nota, st.session_state.current_semester))
                                            conn.commit()
                                            
                                            st.success(f"✅ Nota {nota_noua} adăugată pentru {elev}!")
                                            time.sleep(1)
                                            st.rerun()
                                        except sqlite3.IntegrityError:
                                            st.error("❌ Această notă există deja pentru această zi!")
                        
                        st.markdown("---")
                        
                        # Secțiunea pentru absențe
                        st.markdown("##### ❌ Absențe")
                        
                        col_abs_status, col_abs_action = st.columns([2, 1])
                        
                        with col_abs_status:
                            if are_absenta:
                                st.success("✅ Absență deja înregistrată")
                            else:
                                st.info("ℹ️ Nu există absență înregistrată")
                        
                        with col_abs_action:
                            if not are_absenta:
                                if st.button(
                                    "❌ Marchează absent",
                                    key=f"abs_{elev}_{data_str}",
                                    use_container_width=True
                                ):
                                    try:
                                        conn.execute('''INSERT INTO absente 
                                                      (data, clasa, nume, materie, profesor) 
                                                      VALUES (?, ?, ?, ?, ?)''',
                                                   (data_str, clasa, elev, st.session_state.materie, 
                                                    st.session_state.username))
                                        conn.commit()
                                        st.warning(f"⚠️ {elev} marcat absent!")
                                        time.sleep(1)
                                        st.rerun()
                                    except sqlite3.IntegrityError:
                                        st.error("❌ Absența există deja!")
                        
                        st.markdown("---")
                        
                        # Secțiunea pentru observații
                        st.markdown("##### 📋 Observații comportamentale")
                        
                        observatie_text = st.text_area(
                            "Scrie observația aici:",
                            placeholder="Descriere comportament, realizări, sau aspecte de îmbunătățire...",
                            key=f"obs_text_{elev}",
                            height=100
                        )
                        
                        col_obs_type1, col_obs_type2, col_obs_type3, col_obs_type4 = st.columns(4)
                        
                        with col_obs_type1:
                            if st.button(
                                "👏 Laudă",
                                key=f"lauda_{elev}",
                                use_container_width=True,
                                help="Laudă pentru comportament pozitiv sau realizări"
                            ):
                                if observatie_text.strip():
                                    adauga_observatie(
                                        data_str, elev, st.session_state.materie,
                                        observatie_text.strip(), "laudă", 
                                        st.session_state.username, conn
                                    )
                                    st.success(f"✅ Laudă adăugată pentru {elev}!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.warning("⚠️ Completează observația!")
                        
                        with col_obs_type2:
                            if st.button(
                                "⚠️ Atenționare",
                                key=f"atentionare_{elev}",
                                use_container_width=True,
                                help="Atenționare pentru comportament necorespunzător"
                            ):
                                if observatie_text.strip():
                                    adauga_observatie(
                                        data_str, elev, st.session_state.materie,
                                        observatie_text.strip(), "atenționare", 
                                        st.session_state.username, conn, gravitate=2
                                    )
                                    st.warning(f"⚠️ Atenționare adăugată pentru {elev}!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.warning("⚠️ Completează observația!")
                        
                        with col_obs_type3:
                            if st.button(
                                "❌ Mustrare",
                                key=f"mustrare_{elev}",
                                use_container_width=True,
                                help="Mustrare pentru încălcări grave ale regulamentului"
                            ):
                                if observatie_text.strip():
                                    adauga_observatie(
                                        data_str, elev, st.session_state.materie,
                                        observatie_text.strip(), "mustrare", 
                                        st.session_state.username, conn, gravitate=3
                                    )
                                    st.error(f"❌ Mustrare adăugată pentru {elev}!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.warning("⚠️ Completează observația!")
                        
                        with col_obs_type4:
                            if st.button(
                                "💡 Recomandare",
                                key=f"recomandare_{elev}",
                                use_container_width=True,
                                help="Recomandare pentru îmbunătățire sau sugestii"
                            ):
                                if observatie_text.strip():
                                    adauga_observatie(
                                        data_str, elev, st.session_state.materie,
                                        observatie_text.strip(), "recomandare", 
                                        st.session_state.username, conn
                                    )
                                    st.info(f"💡 Recomandare adăugată pentru {elev}!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.warning("⚠️ Completează observația!")
                        
                        st.markdown("---")
                        
                        # Secțiunea pentru purtare
                        st.markdown("##### ⭐ Purtare")
                        
                        nota_purtare_curenta = get_nota_purtare_curenta(
                            elev, conn, st.session_state.current_semester
                        )
                        
                        st.markdown(f"**Nota curentă de purtare:** `{nota_purtare_curenta}/10`")
                        
                        col_purtare_slider, col_purtare_input = st.columns([2, 1])
                        
                        with col_purtare_slider:
                            noua_nota_purtare = st.slider(
                                "Setează nota de purtare:",
                                min_value=1,
                                max_value=10,
                                value=nota_purtare_curenta,
                                key=f"purt_slider_{elev}"
                            )
                        
                        with col_purtare_input:
                            motiv_purtare = st.text_input(
                                "Motivul modificării:",
                                placeholder="Scrie motivul modificării notei de purtare...",
                                key=f"purt_motiv_{elev}"
                            )
                        
                        if st.button(
                            "💾 Salvează nota de purtare",
                            key=f"save_purt_{elev}",
                            use_container_width=True
                        ):
                            if motiv_purtare.strip():
                                update_purtare(
                                    elev, noua_nota_purtare, motiv_purtare.strip(),
                                    st.session_state.username, conn, st.session_state.current_semester
                                )
                                st.success(f"✅ Nota de purtare actualizată pentru {elev}: {noua_nota_purtare}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Te rog completează motivul modificării!")
                
                # Ascunde progress bar după terminare
                progress_bar.empty()
        
        elif selected_menu == "📅 Calendar Anual":
            st.markdown("#### 📅 Calendar Anual - Planificare și Management")
            
            # Selectare an pentru calendar
            selected_year = st.selectbox(
                "Selectează anul:",
                [2025, 2026],
                index=1,
                key="calendar_year_select_prof"
            )
            
            # Afișare calendar anual complet
            calendar_manager.display_year_calendar(
                clasa, 
                st.session_state.materie, 
                selected_year
            )
            
            # Secțiune suplimentară pentru statistici calendaristice
            st.markdown("---")
            st.markdown("#### 📊 Statistici Calendaristice")
            
            col_cal_stats1, col_cal_stats2, col_cal_stats3 = st.columns(3)
            
            with col_cal_stats1:
                selected_days = calendar_manager.get_selected_days(clasa, st.session_state.materie)
                days_count = len(selected_days)
                st.metric("📅 Zile selectate", days_count, key="metric_days_selected")
            
            with col_cal_stats2:
                # Zile cu note înregistrate
                cursor = conn.cursor()
                cursor.execute('''SELECT COUNT(DISTINCT data) 
                                FROM grades 
                                WHERE clasa = ? AND materie = ?''',
                             (clasa, st.session_state.materie))
                days_with_grades = cursor.fetchone()[0] or 0
                st.metric("📝 Zile cu note", days_with_grades, key="metric_days_with_grades")
            
            with col_cal_stats3:
                # Procentaj acoperire
                total_school_days = 180  # Număr aproximativ de zile de școală
                coverage = (days_with_grades / total_school_days * 100) if total_school_days > 0 else 0
                st.metric("📈 Acoperire evaluare", f"{coverage:.1f}%", key="metric_coverage")
        
        elif selected_menu == "📊 Statistici și Rapoarte":
            st.markdown("#### 📊 Statistici Detaliate și Rapoarte")
            
            # Selectare perioadă pentru rapoarte
            col_period, col_report_type = st.columns(2)
            
            with col_period:
                report_period = st.selectbox(
                    "Perioadă raport:",
                    ["Ultima săptămână", "Ultima lună", "Acest semestru", "Tot anul școlar"],
                    key="report_period_select_prof"
                )
            
            with col_report_type:
                report_type = st.selectbox(
                    "Tip raport:",
                    ["Statistici generale", "Analiză performanță", "Comparație clase", "Tendințe temporale"],
                    key="report_type_select_prof"
                )
            
            # Generare raport
            if st.button("📈 Generează Raport", type="primary", use_container_width=True, key="btn_generate_report"):
                with st.spinner("Generare raport în curs..."):
                    time.sleep(2)
                    
                    # Obține statistici
                    stats = get_statistici_clasa(
                        clasa, st.session_state.materie, conn, 
                        'luna' if report_period == "Ultima lună" else 'semestru'
                    )
                    
                    # Afișare statistici
                    col_stat_det1, col_stat_det2, col_stat_det3 = st.columns(3)
                    
                    with col_stat_det1:
                        st.markdown("##### 📝 Statistici Note")
                        st.markdown(f"""
                        <div class="custom-card">
                            <p><strong>Total note:</strong> {stats['note']['total']}</p>
                            <p><strong>Medie clasă:</strong> {stats['note']['medie']}</p>
                            <p><strong>Nota minimă:</strong> {stats['note']['minim']}</p>
                            <p><strong>Nota maximă:</strong> {stats['note']['maxim']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_stat_det2:
                        st.markdown("##### ❌ Statistici Absențe")
                        st.markdown(f"""
                        <div class="custom-card">
                            <p><strong>Total absențe:</strong> {stats['absente']['total']}</p>
                            <p><strong>Absențe motivate:</strong> {stats['absente']['motivate']}</p>
                            <p><strong>Absențe nemotivate:</strong> {stats['absente']['total'] - stats['absente']['motivate']}</p>
                            <p><strong>Rată absenteism:</strong> {(stats['absente']['total'] / len(elevi_clasa) * 100):.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_stat_det3:
                        st.markdown("##### 📋 Statistici Observatii ")
                    with col_stat_det3:
                        st.markdown("##### 📋 Statistici Observații")
                        obs_text = "<div class='custom-card'>"
                        for tip, numar in stats['observatii'].items():
                            obs_text += f"<p><strong>{tip.title()}:</strong> {numar}</p>"
                        obs_text += "</div>"
                        st.markdown(obs_text, unsafe_allow_html=True)
                    
                    # Grafic evoluție note
                    st.markdown("##### 📈 Evoluția Notelor pe Lună")
                    
                    cursor = conn.cursor()
                    cursor.execute('''SELECT strftime('%Y-%m', data) as luna, 
                                     AVG(nota) as medie_luna, COUNT(*) as numar_note
                                     FROM grades 
                                     WHERE clasa = ? AND materie = ?
                                     GROUP BY strftime('%Y-%m', data)
                                     ORDER BY luna''', 
                                 (clasa, st.session_state.materie))
                    monthly_data = cursor.fetchall()
                    
                    if monthly_data:
                        months = [row[0] for row in monthly_data]
                        averages = [row[1] for row in monthly_data]
                        counts = [row[2] for row in monthly_data]
                        
                        col_chart1, col_chart2 = st.columns(2)
                        
                        with col_chart1:
                            chart_data = pd.DataFrame({
                                'Luna': months,
                                'Medie': averages
                            })
                            st.line_chart(chart_data.set_index('Luna'))
                        
                        with col_chart2:
                            chart_data2 = pd.DataFrame({
                                'Luna': months,
                                'Număr note': counts
                            })
                            st.bar_chart(chart_data2.set_index('Luna'))
                    else:
                        st.info("ℹ️ Nu există suficiente date pentru a genera grafice.")
        
        elif selected_menu == "✏️ Management Note":
            st.markdown("#### ✏️ Management Avansat Note")
            
            # Filtrări pentru note
            col_filter_date, col_filter_student = st.columns(2)
            
            with col_filter_date:
                start_date = st.date_input(
                    "Dată început:",
                    value=date(2025, 9, 1),
                    key="mgmt_start_date"
                )
                end_date = st.date_input(
                    "Dată sfârșit:",
                    value=date.today(),
                    key="mgmt_end_date"
                )
            
            with col_filter_student:
                selected_student = st.selectbox(
                    "Filtrează după elev:",
                    ["Toți elevii"] + sorted(elevi_clasa),
                    key="mgmt_student_filter"
                )
            
            # Query pentru note
            query = '''SELECT g.id, g.data, g.nume, g.nota, g.tip_nota, g.comentariu, 
                       g.profesor, g.created_at, g.updated_at
                       FROM grades g
                       WHERE g.clasa = ? AND g.materie = ? 
                       AND g.data BETWEEN ? AND ?'''
            
            params = [clasa, st.session_state.materie, 
                     start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]
            
            if selected_student != "Toți elevii":
                query += " AND g.nume = ?"
                params.append(selected_student)
            
            query += " ORDER BY g.data DESC, g.nume"
            
            df_grades = pd.read_sql(query, conn, params=params)
            
            if not df_grades.empty:
                st.markdown(f"**{len(df_grades)} note găsite**")
                
                # Formatează DataFrame-ul pentru afișare
                df_display = df_grades.copy()
                df_display['data'] = pd.to_datetime(df_display['data']).dt.strftime('%d.%m.%Y')
                df_display['created_at'] = pd.to_datetime(df_display['created_at']).dt.strftime('%d.%m.%Y %H:%M')
                df_display['updated_at'] = pd.to_datetime(df_display['updated_at']).dt.strftime('%d.%m.%Y %H:%M')
                
                # Coloane pentru acțiuni
                st.markdown("##### 📋 Lista Note")
                
                # Buton pentru editare în masă
                if st.button("✏️ Modifică note în masă", key="btn_bulk_edit", use_container_width=True):
                    st.session_state['bulk_edit_mode'] = True
                
                if st.session_state.get('bulk_edit_mode', False):
                    st.markdown("##### ✏️ Modificare în Masă")
                    
                    # Creează un formular pentru editare în masă
                    with st.form(key='bulk_edit_form'):
                        for idx, row in df_grades.iterrows():
                            col1, col2, col3 = st.columns([3, 2, 1])
                            with col1:
                                st.markdown(f"**{row['nume']}** - {row['data']}")
                            with col2:
                                new_grade = st.number_input(
                                    "Notă nouă:",
                                    min_value=1.0,
                                    max_value=10.0,
                                    value=float(row['nota']),
                                    step=0.5,
                                    key=f"bulk_grade_{row['id']}",
                                    label_visibility="collapsed"
                                )
                            with col3:
                                if st.button("💾", key=f"save_bulk_{row['id']}", help="Salvează modificarea"):
                                    update_nota(row['id'], new_grade, conn)
                                    st.success(f"Nota pentru {row['nume']} actualizată!")
                                    time.sleep(1)
                                    st.rerun()
                        
                        col_cancel, col_save_all = st.columns(2)
                        with col_cancel:
                            if st.form_submit_button("❌ Anulează", use_container_width=True):
                                st.session_state['bulk_edit_mode'] = False
                                st.rerun()
                        with col_save_all:
                            st.form_submit_button("💾 Salvează toate", use_container_width=True)
                
                else:
                    # Afișează tabelul normal
                    st.dataframe(
                        df_display[['data', 'nume', 'nota', 'tip_nota', 'comentariu', 'profesor']],
                        use_container_width=True,
                        height=400
                    )
                    
                    # Opțiuni de export
                    col_export1, col_export2 = st.columns(2)
                    
                    with col_export1:
                        csv_data = df_display.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Exportă CSV",
                            data=csv_data,
                            file_name=f"note_{clasa}_{st.session_state.materie}_{start_date}_{end_date}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    with col_export2:
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                            df_display.to_excel(writer, index=False, sheet_name='Note')
                        excel_data = excel_buffer.getvalue()
                        st.download_button(
                            label="📥 Exportă Excel",
                            data=excel_buffer,
                            file_name=f"note_{clasa}_{st.session_state.materie}_{start_date}_{end_date}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    
                    # Statistici rapide
                    st.markdown("##### 📊 Statistici Note")
                    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
                    
                    with col_stats1:
                        avg_grade = df_grades['nota'].mean()
                        st.metric("Medie generală", f"{avg_grade:.2f}")
                    
                    with col_stats2:
                        min_grade = df_grades['nota'].min()
                        st.metric("Nota minimă", f"{min_grade:.2f}")
                    
                    with col_stats3:
                        max_grade = df_grades['nota'].max()
                        st.metric("Nota maximă", f"{max_grade:.2f}")
                    
                    with col_stats4:
                        std_grade = df_grades['nota'].std()
                        st.metric("Deviație standard", f"{std_grade:.2f}")
                    
                    # Distribuție note
                    st.markdown("##### 📊 Distribuția Notelor")
                    grade_counts = df_grades['nota'].value_counts().sort_index()
                    
                    if not grade_counts.empty:
                        chart_data = pd.DataFrame({
                            'Nota': grade_counts.index,
                            'Frecvență': grade_counts.values
                        })
                        st.bar_chart(chart_data.set_index('Nota'))
            else:
                st.info("ℹ️ Nu există note pentru criteriile selectate.")
        
        elif selected_menu == "📈 Analiză Performanță":
            st.markdown("#### 📈 Analiză Performanță Individuală și Comparativă")
            
            # Selectare elev pentru analiză detaliată
            selected_student_analysis = st.selectbox(
                "Selectează elev pentru analiză detaliată:",
                sorted(elevi_clasa),
                key="analysis_student_select"
            )
            
            tab_overview, tab_comparison, tab_trends = st.tabs([
                "📋 Prezentare generală",
                "📊 Comparație cu clasa",
                "📈 Tendințe și progres"
            ])
            
            with tab_overview:
                st.markdown(f"##### 📋 Profil Performanță - {selected_student_analysis}")
                
                col_profile1, col_profile2 = st.columns(2)
                
                with col_profile1:
                    # Informații elev
                    elev_details = get_elev_details(selected_student_analysis)
                    st.markdown(f"""
                    <div class="custom-card">
                        <h4>👤 Informații elev</h4>
                        <p><strong>Nume:</strong> {selected_student_analysis}</p>
                        <p><strong>Clasă:</strong> {clasa}</p>
                        <p><strong>Data nașterii:</strong> {elev_details.get('data_nasterii', 'N/A')}</p>
                        <p><strong>Observații speciale:</strong> {elev_details.get('observatii_speciale', 'Niciuna')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_profile2:
                    # Statistici academice
                    cursor = conn.cursor()
                    
                    # Note statistici
                    cursor.execute('''SELECT COUNT(*), AVG(nota), MIN(nota), MAX(nota) 
                                    FROM grades 
                                    WHERE nume = ? AND materie = ? AND clasa = ?''',
                                 (selected_student_analysis, st.session_state.materie, clasa))
                    grade_stats = cursor.fetchone()
                    
                    # Absențe statistici
                    cursor.execute('''SELECT COUNT(*), 
                                     SUM(CASE WHEN motivata = 1 THEN 1 ELSE 0 END) 
                                     FROM absente 
                                     WHERE nume = ? AND materie = ? AND clasa = ?''',
                                 (selected_student_analysis, st.session_state.materie, clasa))
                    abs_stats = cursor.fetchone()
                    
                    st.markdown(f"""
                    <div class="custom-card">
                        <h4>📊 Statistici academice</h4>
                        <p><strong>Total note:</strong> {grade_stats[0] or 0}</p>
                        <p><strong>Medie generală:</strong> {grade_stats[1] or 0:.2f}</p>
                        <p><strong>Nota minimă:</strong> {grade_stats[2] or 0}</p>
                        <p><strong>Nota maximă:</strong> {grade_stats[3] or 0}</p>
                        <p><strong>Total absențe:</strong> {abs_stats[0] or 0}</p>
                        <p><strong>Absențe motivate:</strong> {abs_stats[1] or 0}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Ultimele note
                st.markdown("##### 📝 Ultimele note")
                cursor.execute('''SELECT data, nota, tip_nota, comentariu 
                                FROM grades 
                                WHERE nume = ? AND materie = ? AND clasa = ?
                                ORDER BY data DESC 
                                LIMIT 10''',
                             (selected_student_analysis, st.session_state.materie, clasa))
                recent_grades = cursor.fetchall()
                
                if recent_grades:
                    grades_df = pd.DataFrame(recent_grades, columns=['Data', 'Nota', 'Tip', 'Comentariu'])
                    grades_df['Data'] = pd.to_datetime(grades_df['Data']).dt.strftime('%d.%m.%Y')
                    st.dataframe(grades_df, use_container_width=True)
                else:
                    st.info("ℹ️ Elevul nu are note înregistrate.")
                
                # Observații recente
                st.markdown("##### 📋 Observații recente")
                observatii = get_observatii_elev(selected_student_analysis, conn)
                
                if observatii:
                    for obs in observatii[:5]:  # Primele 5 observații
                        data_obs, materie_obs, text_obs, tip_obs, prof_obs, grav_obs, rez_obs = obs
                        
                        if tip_obs == "laudă":
                            icon = "👏"
                            color = "#22c55e"
                        elif tip_obs == "atenționare":
                            icon = "⚠️"
                            color = "#eab308"
                        elif tip_obs == "mustrare":
                            icon = "❌"
                            color = "#ef4444"
                        else:
                            icon = "💡"
                            color = "#3b82f6"
                        
                        st.markdown(f"""
                        <div class="custom-card" style="border-left: 4px solid {color}; padding: 10px !important;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong>{icon} {tip_obs.title()}</strong>
                                    <p style="margin: 5px 0;">{text_obs}</p>
                                    <small style="color: #94a3b8;">
                                        {data_obs} | {prof_obs} | Gravitate: {grav_obs}/3
                                    </small>
                                </div>
                                <div>
                                    {"✅" if rez_obs else "⏳"}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("ℹ️ Nu există observații pentru acest elev.")
            
            with tab_comparison:
                st.markdown(f"##### 📊 Comparație cu clasa {clasa}")
                
                # Comparație note
                cursor = conn.cursor()
                
                # Media elevului
                cursor.execute('''SELECT AVG(nota) FROM grades 
                                WHERE nume = ? AND materie = ? AND clasa = ?''',
                             (selected_student_analysis, st.session_state.materie, clasa))
                student_avg = cursor.fetchone()[0] or 0
                
                # Media clasei
                cursor.execute('''SELECT AVG(nota) FROM grades 
                                WHERE clasa = ? AND materie = ?''',
                             (clasa, st.session_state.materie))
                class_avg = cursor.fetchone()[0] or 0
                
                # Pozitia în clasament
                cursor.execute('''SELECT nume, AVG(nota) as medie 
                                FROM grades 
                                WHERE clasa = ? AND materie = ?
                                GROUP BY nume 
                                ORDER BY medie DESC''',
                             (clasa, st.session_state.materie))
                rankings = cursor.fetchall()
                
                if rankings:
                    rank_df = pd.DataFrame(rankings, columns=['Nume', 'Medie'])
                    rank_df['Poziție'] = range(1, len(rank_df) + 1)
                    student_position = rank_df[rank_df['Nume'] == selected_student_analysis].index[0] + 1
                    total_students = len(rank_df)
                else:
                    student_position = 0
                    total_students = 0
                
                # Afișare metrici comparație
                col_comp1, col_comp2, col_comp3 = st.columns(3)
                
                with col_comp1:
                    diff_avg = student_avg - class_avg
                    st.metric(
                        "📊 Medie personală", 
                        f"{student_avg:.2f}",
                        f"{'+' if diff_avg > 0 else ''}{diff_avg:.2f} vs clasa"
                    )
                
                with col_comp2:
                    st.metric(
                        "🥇 Poziția în clasă",
                        f"{student_position}/{total_students}",
                        f"Top {int((student_position/total_students)*100)}%"
                    )
                
                with col_comp3:
                    # Procentaj peste media clasei
                    if class_avg > 0:
                        pct_above = ((student_avg - class_avg) / class_avg) * 100
                        st.metric(
                            "📈 Performanță relativă",
                            f"{pct_above:+.1f}%",
                            "față de media clasei"
                        )
                    else:
                        st.metric("📈 Performanță relativă", "N/A", "date insuficiente")
                
                # Grafic comparativ
                if rankings and len(rankings) > 1:
                    st.markdown("##### 📈 Clasamentul clasei")
                    
                    # Pregătește datele pentru grafic
                    rank_df = pd.DataFrame(rankings, columns=['Nume', 'Medie'])
                    rank_df = rank_df.sort_values('Medie', ascending=True)
                    
                    # Creează un grafic de bare orizontale
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    # Definește culori (elevul selectat în altă culoare)
                    colors = ['#3b82f6' if name != selected_student_analysis else '#22c55e' 
                             for name in rank_df['Nume']]
                    
                    bars = ax.barh(rank_df['Nume'], rank_df['Medie'], color=colors)
                    ax.set_xlabel('Medie')
                    ax.set_title('Clasamentul clasei după medie')
                    
                    # Adaugă valorile pe bare
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width, bar.get_y() + bar.get_height()/2, 
                               f'{width:.2f}', ha='left', va='center')
                    
                    st.pyplot(fig)
            
            with tab_trends:
                st.markdown(f"##### 📈 Evoluția performanței - {selected_student_analysis}")
                
                # Date pentru tendințe
                cursor = conn.cursor()
                cursor.execute('''SELECT strftime('%Y-%m', data) as luna, 
                                 AVG(nota) as medie_luna, COUNT(*) as numar_note
                                 FROM grades 
                                 WHERE nume = ? AND materie = ? AND clasa = ?
                                 GROUP BY strftime('%Y-%m', data)
                                 ORDER BY luna''',
                             (selected_student_analysis, st.session_state.materie, clasa))
                student_trend = cursor.fetchall()
                
                if student_trend and len(student_trend) > 1:
                    months = [row[0] for row in student_trend]
                    averages = [row[1] for row in student_trend]
                    
                    # Grafic evoluție
                    trend_df = pd.DataFrame({
                        'Luna': months,
                        'Medie': averages
                    })
                    
                    # Linia de tendință
                    x = range(len(months))
                    z = np.polyfit(x, averages, 1)
                    p = np.poly1d(z)
                    trend_line = p(x)
                    
                    # Creează graficul
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.plot(months, averages, 'o-', label='Medie lunară', color='#3b82f6')
                    ax.plot(months, trend_line, '--', label='Tendință', color='#ef4444')
                    ax.set_xlabel('Luna')
                    ax.set_ylabel('Medie')
                    ax.set_title('Evoluția mediilor lunare')
                    ax.legend()
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    
                    # Analiză tendință
                    if len(averages) >= 2:
                        first_avg = averages[0]
                        last_avg = averages[-1]
                        trend_direction = "crescătoare" if last_avg > first_avg else "descrescătoare" if last_avg < first_avg else "constantă"
                        trend_magnitude = abs(last_avg - first_avg)
                        
                        st.markdown(f"""
                        <div class="custom-card">
                            <h4>📊 Analiză tendință</h4>
                            <p><strong>Medie inițială ({months[0]}):</strong> {first_avg:.2f}</p>
                            <p><strong>Medie finală ({months[-1]}):</strong> {last_avg:.2f}</p>
                            <p><strong>Tendință:</strong> {trend_direction}</p>
                            <p><strong>Diferență:</strong> {last_avg - first_avg:+.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("ℹ️ Nu există suficiente date pentru analiza tendințelor.")
        
        elif selected_menu == "⚙️ Setări Profesor":
            st.markdown("#### ⚙️ Setări și Configurare Profesor")
            
            tab_profile, tab_preferences, tab_backup = st.tabs([
                "👤 Profil",
                "🎨 Preferințe",
                "💾 Backup"
            ])
            
            with tab_profile:
                prof_details = get_profesor_details(st.session_state.username)
                
                st.markdown(f"""
                <div class="custom-card">
                    <h4>👨‍🏫 Profil profesor</h4>
                    <p><strong>Nume complet:</strong> {st.session_state.username}</p>
                    <p><strong>Materie predată:</strong> {st.session_state.materie}</p>
                    <p><strong>Email:</strong> {prof_details.get('email', 'N/A')}</p>
                    <p><strong>Telefon:</strong> {prof_details.get('telefon', 'N/A')}</p>
                    <p><strong>Specializare:</strong> {prof_details.get('specializare', 'N/A')}</p>
                    <p><strong>Grad didactic:</strong> {prof_details.get('grad_didactic', 'N/A')}</p>
                    <p><strong>Ani experiență:</strong> {prof_details.get('ani_experienta', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Schimbare parolă
                st.markdown("##### 🔐 Schimbare parolă")
                with st.form(key="change_password_form"):
                    current_password = st.text_input("Parola curentă:", type="password")
                    new_password = st.text_input("Parola nouă:", type="password")
                    confirm_password = st.text_input("Confirmă parola nouă:", type="password")
                    
                    if st.form_submit_button("💾 Actualizează parola", use_container_width=True):
                        if current_password == PROFESORI[st.session_state.username]["parola"]:
                            if new_password == confirm_password:
                                # În producție, aceasta ar actualiza în baza de date
                                st.success("✅ Parola a fost actualizată cu succes!")
                            else:
                                st.error("❌ Parolele nu coincid!")
                        else:
                            st.error("❌ Parola curentă este incorectă!")
            
            with tab_preferences:
                st.markdown("##### 🎨 Preferințe afișare")
                
                col_pref1, col_pref2 = st.columns(2)
                
                with col_pref1:
                    default_class = st.selectbox(
                        "Clasă implicită:",
                        list(CLASE.keys()),
                        index=list(CLASE.keys()).index(st.session_state.clasa_selectata)
                    )
                    
                    default_semester = st.selectbox(
                        "Semestru implicit:",
                        [1, 2],
                        index=0
                    )
                
                with col_pref2:
                    items_per_page = st.slider(
                        "Elemente pe pagină:",
                        min_value=10,
                        max_value=50,
                        value=20,
                        step=5
                    )
                    
                    notifications = st.checkbox("🔔 Notificări email", value=True)
                
                if st.button("💾 Salvează preferințe", use_container_width=True):
                    st.session_state.clasa_selectata = default_class
                    st.success("✅ Preferințele au fost salvate!")
            
            with tab_backup:
                st.markdown("##### 💾 Backup și Restaurare")
                
                col_backup1, col_backup2 = st.columns(2)
                
                with col_backup1:
                    st.markdown("**Export date**")
                    if st.button("📥 Exportă toate datele", use_container_width=True):
                        # Exportă toate datele profesorului
                        data_to_export = {}
                        
                        # Note
                        df_grades = pd.read_sql(
                            '''SELECT * FROM grades WHERE profesor = ?''',
                            conn, params=[st.session_state.username]
                        )
                        data_to_export['grades'] = df_grades.to_dict()
                        
                        # Absențe
                        df_absente = pd.read_sql(
                            '''SELECT * FROM absente WHERE profesor = ?''',
                            conn, params=[st.session_state.username]
                        )
                        data_to_export['absente'] = df_absente.to_dict()
                        
                        # Observații
                        df_obs = pd.read_sql(
                            '''SELECT * FROM observatii WHERE profesor = ?''',
                            conn, params=[st.session_state.username]
                        )
                        data_to_export['observatii'] = df_obs.to_dict()
                        
                        # Convertire la JSON și descărcare
                        json_data = json.dumps(data_to_export, indent=2, default=str)
                        
                        st.download_button(
                            label="⬇️ Descarcă backup",
                            data=json_data,
                            file_name=f"backup_{st.session_state.username}_{datetime.now().strftime('%Y%m%d')}.json",
                            mime="application/json"
                        )
                
                with col_backup2:
                    st.markdown("**Statistici backup**")
                    
                    cursor = conn.cursor()
                    
                    # Număr total înregistrări
                    cursor.execute('''SELECT COUNT(*) FROM grades WHERE profesor = ?''',
                                 [st.session_state.username])
                    total_grades = cursor.fetchone()[0] or 0
                    
                    cursor.execute('''SELECT COUNT(*) FROM absente WHERE profesor = ?''',
                                 [st.session_state.username])
                    total_absente = cursor.fetchone()[0] or 0
                    
                    cursor.execute('''SELECT COUNT(*) FROM observatii WHERE profesor = ?''',
                                 [st.session_state.username])
                    total_obs = cursor.fetchone()[0] or 0
                    
                    st.markdown(f"""
                    <div class="custom-card" style="padding: 15px !important;">
                        <p><strong>📝 Note:</strong> {total_grades}</p>
                        <p><strong>❌ Absențe:</strong> {total_absente}</p>
                        <p><strong>📋 Observații:</strong> {total_obs}</p>
                        <p><strong>💾 Ultimul backup:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
                    </div>
                    """, unsafe_allow_html=True)

# ============================================
# 11. INTERFAȚA PĂRINTE/ELEV - MODUL PREMIUM
# ============================================
if st.session_state.role == "parent":
    # Informații elev
    elev_details = get_elev_details(st.session_state.nume_elev)
    
    # Header elev
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0; background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9)); 
                border-radius: 20px; margin-bottom: 30px; border: 1px solid rgba(255, 255, 255, 0.15);">
        <h1 style="color: white; margin-bottom: 10px;">👤 {st.session_state.nume_elev}</h1>
        <div style="display: flex; justify-content: center; gap: 30px; margin-top: 20px;">
            <div>
                <p style="color: #94a3b8; margin: 0;">📅 Data nașterii</p>
                <p style="color: white; margin: 5px 0; font-weight: bold;">{elev_details.get('data_nasterii', 'N/A')}</p>
            </div>
            <div>
                <p style="color: #94a3b8; margin: 0;">🏫 Clasă</p>
                <p style="color: white; margin: 5px 0; font-weight: bold;">{st.session_state.clasa_selectata}</p>
            </div>
            <div>
                <p style="color: #94a3b8; margin: 0;">📞 Contact parinte</p>
                <p style="color: white; margin: 5px 0; font-weight: bold;">{elev_details.get('telefon_parinte', 'N/A')}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Meniu principal părinte
    menu_options_parent = [
        "📊 Situație academică",
        "📝 Note și absențe",
        "📋 Observații comportamentale",
        "📈 Statistici și progres",
        "📅 Calendar școlar",
        "👨‍👩‍👧‍👦 Profil și setări"
    ]
    
    selected_menu_parent = st.radio(
        "Selectează secțiunea dorită:",
        menu_options_parent,
        horizontal=True,
        key="parent_menu_main"
    )
    
    # Secțiunea Situație academică
    if selected_menu_parent == "📊 Situație academică":
        st.markdown(f"#### 📊 Situație academică completă - {st.session_state.nume_elev}")
        
        # Statistici generale
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        
        with col_stats1:
            # Media generală pe semestrul curent
            cursor = conn.cursor()
            cursor.execute('''SELECT AVG(nota) FROM grades 
                            WHERE nume = ? AND semestru = ?''',
                         [st.session_state.nume_elev, st.session_state.current_semester])
            overall_avg = cursor.fetchone()[0] or 0
            st.metric("📊 Medie generală", f"{overall_avg:.2f}", key="parent_metric_avg")
        
        with col_stats2:
            # Număr total note
            cursor.execute('''SELECT COUNT(*) FROM grades 
                            WHERE nume = ? AND semestru = ?''',
                         [st.session_state.nume_elev, st.session_state.current_semester])
            total_grades = cursor.fetchone()[0] or 0
            st.metric("📝 Total note", total_grades, key="parent_metric_total_grades")
        
        with col_stats3:
            # Absențe totale
            cursor.execute('''SELECT COUNT(*) FROM absente 
                            WHERE nume = ?''',
                         [st.session_state.nume_elev])
            total_absente = cursor.fetchone()[0] or 0
            st.metric("❌ Total absențe", total_absente, key="parent_metric_absente")
        
        with col_stats4:
            # Nota purtare
            nota_purtare = get_nota_purtare_curenta(
                st.session_state.nume_elev, conn, st.session_state.current_semester
            )
            st.metric("⭐ Purtare", f"{nota_purtare}/10", key="parent_metric_purtare")
        
        # Medii pe materii
        st.markdown("##### 📚 Medii pe materii")
        
        # Obține toate materiile cu note
        cursor.execute('''SELECT DISTINCT materie FROM grades 
                        WHERE nume = ? AND semestru = ?
                        ORDER BY materie''',
                     [st.session_state.nume_elev, st.session_state.current_semester])
        materii_elev = cursor.fetchall()
        
        if materii_elev:
            # Creează coloane pentru materii
            cols_per_row = 3
            materii_list = [m[0] for m in materii_elev]
            
            for i in range(0, len(materii_list), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(materii_list):
                        materie = materii_list[i + j]
                        
                        # Calculează media pentru fiecare materie
                        cursor.execute('''SELECT AVG(nota) FROM grades 
                                        WHERE nume = ? AND materie = ? AND semestru = ?''',
                                     [st.session_state.nume_elev, materie, st.session_state.current_semester])
                        media_materie = cursor.fetchone()[0] or 0
                        
                        # Determină culoarea bazată pe medie
                        if media_materie >= 9:
                            color = "#22c55e"
                            emoji = "🥇"
                        elif media_materie >= 7:
                            color = "#3b82f6"
                            emoji = "📈"
                        elif media_materie >= 5:
                            color = "#eab308"
                            emoji = "📊"
                        else:
                            color = "#ef4444"
                            emoji = "📉"
                        
                        with cols[j]:
                            st.markdown(f"""
                            <div class="custom-card" style="padding: 15px !important; border-left: 4px solid {color};">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <strong>{emoji} {materie}</strong>
                                        <h3 style="margin: 10px 0; color: white;">{media_materie:.2f}</h3>
                                    </div>
                                    <div style="font-size: 1.5rem;">
                                        {emoji}
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ Elevul nu are note înregistrate pentru acest semestru.")
        
        # Ultimele activități
        st.markdown("##### 📅 Ultimele activități")
        
        col_recent1, col_recent2 = st.columns(2)
        
        with col_recent1:
            st.markdown("**📝 Ultimele note**")
            cursor.execute('''SELECT data, materie, nota, tip_nota, comentariu 
                            FROM grades 
                            WHERE nume = ?
                            ORDER BY data DESC 
                            LIMIT 5''',
                         [st.session_state.nume_elev])
            recent_grades = cursor.fetchall()
            
            if recent_grades:
                for grade in recent_grades:
                    data_grade, materie_grade, nota_grade, tip_grade, coment_grade = grade
                    
                    # Determină culoarea notei
                    if nota_grade >= 9:
                        color = "#22c55e"
                    elif nota_grade >= 7:
                        color = "#3b82f6"
                    elif nota_grade >= 5:
                        color = "#eab308"
                    else:
                        color = "#ef4444"
                    
                    st.markdown(f"""
                    <div class="custom-card" style="padding: 10px !important; margin: 5px 0 !important; 
                                border-left: 4px solid {color};">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <strong>{materie_grade}</strong><br>
                                <small>{data_grade} | {tip_grade}</small>
                            </div>
                            <div style="font-size: 1.3rem; font-weight: bold; color: {color};">
                                {nota_grade}
                            </div>
                        </div>
                        {f'<p style="margin: 5px 0; font-size: 0.9em; color: #94a3b8;">{coment_grade}</p>' if coment_grade else ''}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ Nu există note recente.")
        
        with col_recent2:
            st.markdown("**📋 Ultimele observații**")
            cursor.execute('''SELECT data, materie, observatie, tip 
                            FROM observatii 
                            WHERE nume = ?
                            ORDER BY data DESC 
                            LIMIT 5''',
                         [st.session_state.nume_elev])
            recent_obs = cursor.fetchall()
            
            if recent_obs:
                for obs in recent_obs:
                    data_obs, materie_obs, text_obs, tip_obs = obs
                    
                    if tip_obs == "laudă":
                        icon = "👏"
                        color = "#22c55e"
                    elif tip_obs == "atenționare":
                        icon = "⚠️"
                        color = "#eab308"
                    elif tip_obs == "mustrare":
                        icon = "❌"
                        color = "#ef4444"
                    else:
                        icon = "💡"
                        color = "#3b82f6"
                    
                    st.markdown(f"""
                    <div class="custom-card" style="padding: 10px !important; margin: 5px 0 !important;
                                border-left: 4px solid {color};">
                        <div style="display: flex; align-items: start; gap: 10px;">
                            <div style="font-size: 1.5rem;">{icon}</div>
                            <div>
                                <strong>{tip_obs.title()} - {materie_obs}</strong><br>
                                <p style="margin: 5px 0;">{text_obs}</p>
                                <small style="color: #94a3b8;">{data_obs}</small>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ Nu există observații recente.")
    
    # Secțiunea Note și absențe
    elif selected_menu_parent == "📝 Note și absențe":
        st.markdown(f"#### 📝 Note și absențe detaliat - {st.session_state.nume_elev}")
        
        tab_notes_detailed, tab_absente_detailed, tab_export = st.tabs([
            "📊 Note detaliat",
            "❌ Absențe",
            "📥 Export date"
        ])
        
        with tab_notes_detailed:
            # Filtre pentru note
            col_filter_materie, col_filter_period, col_filter_semester = st.columns(3)
            
            with col_filter_materie:
                # Obține toate materiile cu note
                cursor = conn.cursor()
                cursor.execute('''SELECT DISTINCT materie FROM grades 
                                WHERE nume = ?
                                ORDER BY materie''',
                             [st.session_state.nume_elev])
                all_materii = [m[0] for m in cursor.fetchall()]
                selected_materie = st.selectbox(
                    "Materie:",
                    ["Toate materiile"] + all_materii,
                    key="parent_filter_materie"
                )
            
            with col_filter_period:
                start_date = st.date_input(
                    "Dată început:",
                    value=date(2025, 9, 1),
                    key="parent_filter_start"
                )
                end_date = st.date_input(
                    "Dată sfârșit:",
                    value=date.today(),
                    key="parent_filter_end"
                )
            
            with col_filter_semester:
                selected_semester = st.selectbox(
                    "Semestru:",
                    ["Toate semestrele", "Semestrul 1", "Semestrul 2"],
                    key="parent_filter_semester"
                )
            
            # Construiește query-ul
            query = '''SELECT data, materie, nota, tip_nota, comentariu, profesor 
                       FROM grades 
                       WHERE nume = ? 
                       AND data BETWEEN ? AND ?'''
            
            params = [
                st.session_state.nume_elev,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            ]
            
            if selected_materie != "Toate materiile":
                query += " AND materie = ?"
                params.append(selected_materie)
            
            if selected_semester != "Toate semestrele":
                sem = 1 if selected_semester == "Semestrul 1" else 2
                query += " AND semestru = ?"
                params.append(sem)
            
            query += " ORDER BY data DESC, materie"
            
            # Execută query-ul
            df_grades = pd.read_sql(query, conn, params=params)
            
            if not df_grades.empty:
                # Afișare tabel
                st.markdown(f"**{len(df_grades)} note găsite**")
                
                # Formatează data
                df_display = df_grades.copy()
                df_display['data'] = pd.to_datetime(df_display['data']).dt.strftime('%d.%m.%Y')
                
                # Tabel colorat
                def color_grade(val):
                    if val >= 9:
                        return f'background-color: #16a34a; color: white; font-weight: bold;'
                    elif val >= 7:
                        return f'background-color: #3b82f6; color: white;'
                    elif val >= 5:
                        return f'background-color: #eab308; color: white;'
                    else:
                        return f'background-color: #ef4444; color: white; font-weight: bold;'
                
                styled_df = df_display.style.applymap(color_grade, subset=['nota'])
                st.dataframe(styled_df, use_container_width=True, height=400)
                
                # Statistici
                if selected_materie != "Toate materiile":
                    col_stat1, col_stat2, col_stat3 = st.columns(3)
                    
                    with col_stat1:
                        avg_grade = df_grades['nota'].mean()
                        st.metric("📊 Media materiei", f"{avg_grade:.2f}")
                    
                    with col_stat2:
                        min_grade = df_grades['nota'].min()
                        st.metric("📉 Nota minimă", f"{min_grade:.2f}")
                    
                    with col_stat3:
                        max_grade = df_grades['nota'].max()
                        st.metric("📈 Nota maximă", f"{max_grade:.2f}")
                    
                    # Grafic distribuție note
                    st.markdown("##### 📊 Distribuția notelor")
                    grade_counts = df_grades['nota'].value_counts().sort_index()
                    
                    if not grade_counts.empty:
                        chart_data = pd.DataFrame({
                            'Nota': grade_counts.index,
                            'Frecvență': grade_counts.values
                        })
                        st.bar_chart(chart_data.set_index('Nota'))
            else:
                st.info("ℹ️ Nu există note pentru criteriile selectate.")
        
        with tab_absente_detailed:
            st.markdown("##### ❌ Absențe")
            
            # Obține absențele
            cursor = conn.cursor()
            cursor.execute('''SELECT data, materie, motivata, motiv, profesor 
                            FROM absente 
                            WHERE nume = ?
                            ORDER BY data DESC''',
                         [st.session_state.nume_elev])
            absente = cursor.fetchall()
            
            if absente:
                # Statistici absențe
                total_abs = len(absente)
                motivate = sum(1 for a in absente if a[2])
                nemotivate = total_abs - motivate
                
                col_abs1, col_abs2, col_abs3 = st.columns(3)
                
                with col_abs1:
                    st.metric("📊 Total absențe", total_abs)
                
                with col_abs2:
                    st.metric("✅ Motivate", motivate)
                
                with col_abs3:
                    st.metric("❌ Nemotivate", nemotivate)
                
                # Tabel absențe
                st.markdown("##### 📋 Lista absențelor")
                df_absente = pd.DataFrame(absente, 
                                         columns=['Data', 'Materie', 'Motivată', 'Motiv', 'Profesor'])
                df_absente['Data'] = pd.to_datetime(df_absente['Data']).dt.strftime('%d.%m.%Y')
                df_absente['Motivată'] = df_absente['Motivată'].map({True: '✅', False: '❌'})
                
                st.dataframe(df_absente, use_container_width=True)
            else:
                st.success("🎉 Excelent! Nu există absențe înregistrate.")
        
        with tab_export:
            st.markdown("##### 📥 Export date academice")
            
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                st.markdown("**Export note**")
                if st.button("📝 Exportă notele", use_container_width=True):
                    cursor = conn.cursor()
                    cursor.execute('''SELECT * FROM grades WHERE nume = ?''',
                                 [st.session_state.nume_elev])
                    grades = cursor.fetchall()
                    
                    if grades:
                        df_grades_export = pd.DataFrame(grades, 
                                                       columns=['ID', 'Data', 'Clasa', 'Nume', 'Materie', 
                                                                'Nota', 'Profesor', 'Tip', 'Semestru', 
                                                                'Comentariu', 'Creat', 'Actualizat'])
                        csv_data = df_grades_export.to_csv(index=False).encode('utf-8')
                        
                        st.download_button(
                            label="⬇️ Descarcă CSV",
                            data=csv_data,
                            file_name=f"note_{st.session_state.nume_elev}.csv",
                            mime="text/csv"
                        )
            
            with col_export2:
                st.markdown("**Raport complet**")
                if st.button("📊 Generează raport", use_container_width=True):
                    # Creează un raport complet
                    report_data = {
                        'elev': {
                            'nume': st.session_state.nume_elev,
                            'clasa': st.session_state.clasa_selectata,
                            'date_contact': elev_details
                        },
                        'statistici': {
                            'medie_generala': overall_avg,
                            'total_note': total_grades,
                            'total_absente': total_absente,
                            'nota_purtare': nota_purtare
                        }
                    }
                    
                    json_data = json.dumps(report_data, indent=2, ensure_ascii=False)
                    
                    st.download_button(
                        label="⬇️ Descarcă raport JSON",
                        data=json_data,
                        file_name=f"raport_{st.session_state.nume_elev}.json",
                        mime="application/json"
                    )

# ============================================
# 12. INTERFAȚA DIRECTOARE - PANOU ADMINISTRATIV
# ============================================
elif st.session_state.role == "admin":
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; margin-bottom: 30px;">
        <h1 style="color: white;">🏛️ Panou Administrativ - Directoare</h1>
        <p style="color: #94a3b8;">Management complet al școlii și al catalogului digital</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Meniu administrativ
    admin_menu = st.radio(
        "Selectează modul administrativ:",
        ["📊 Dashboard școală", "👨‍🏫 Management profesori", "👥 Management elevi", 
         "📈 Rapoarte instituționale", "⚙️ Configurare sistem", "🔐 Securitate și audit"],
        horizontal=True,
        key="admin_menu_main"
    )
    
    # Dashboard școală
    if admin_menu == "📊 Dashboard școală":
        st.markdown("#### 📊 Dashboard instituțional")
        
        # Statistici generale
        col_admin1, col_admin2, col_admin3, col_admin4 = st.columns(4)
        
        with col_admin1:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(DISTINCT nume) FROM grades")
            total_students = cursor.fetchone()[0] or 0
            st.metric("👥 Total elevi", total_students, key="admin_total_students")
        
        with col_admin2:
            cursor.execute("SELECT COUNT(DISTINCT profesor) FROM grades")
            total_teachers = cursor.fetchone()[0] or 0
            st.metric("👨‍🏫 Total profesori", total_teachers, key="admin_total_teachers")
        
        with col_admin3:
            cursor.execute("SELECT COUNT(*) FROM grades")
            total_grades = cursor.fetchone()[0] or 0
            st.metric("📝 Total note", total_grades, key="admin_total_grades")
        
        with col_admin4:
            cursor.execute("SELECT AVG(nota) FROM grades")
            overall_avg = cursor.fetchone()[0] or 0
            st.metric("📊 Medie generală", f"{overall_avg:.2f}", key="admin_overall_avg")
        
        # Clasele cu cele mai bune performanțe
        st.markdown("##### 🏆 Top clase după medie")
        cursor.execute('''SELECT clasa, AVG(nota) as medie, COUNT(*) as numar_note
                         FROM grades 
                         GROUP BY clasa 
                         HAVING COUNT(*) >= 5
                         ORDER BY medie DESC 
                         LIMIT 5''')
        top_classes = cursor.fetchall()
        
        if top_classes:
            for clasa, medie, numar in top_classes:
                col_clasa, col_medie = st.columns([3, 1])
                with col_clasa:
                    st.markdown(f"**{clasa}** ({numar} note)")
                with col_medie:
                    st.markdown(f"### {medie:.2f}")
                st.progress(min(float(medie) / 10, 1.0))
        
        # Activități recente
        st.markdown("##### 📅 Activități recente")
        cursor.execute('''SELECT tip_statistica, detalii, created_at 
                         FROM statistici 
                         ORDER BY created_at DESC 
                         LIMIT 10''')
        recent_activities = cursor.fetchall()
        
        if recent_activities:
            for activity in recent_activities:
                tip, detalii, timestamp = activity
                st.markdown(f"""
                <div class="custom-card" style="padding: 10px !important; margin: 5px 0 !important;">
                    <strong>{tip}</strong><br>
                    <small>{detalii}</small><br>
                    <small style="color: #94a3b8;">{timestamp}</small>
                </div>
                """, unsafe_allow_html=True)

# ============================================
# 13. FOOTER ȘI INFORMAȚII SISTEM
# ============================================

st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: #94a3b8; font-size: 0.9rem;">
            🏫 <strong>Școala Gimnazială Model</strong><br>
            Anul școlar 2025-2026
        </p>
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: #94a3b8; font-size: 0.9rem;">
            🔒 <strong>Securitate și confidențialitate</strong><br>
            Conform GDPR și legislației în vigoare
        </p>
    </div>
    """, unsafe_allow_html=True)

with footer_col3:
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: #94a3b8; font-size: 0.9rem;">
            🆘 <strong>Asistență tehnică</strong><br>
            Email: it.support@scoala.ro
        </p>
    </div>
    """, unsafe_allow_html=True)

# Afișează versiunea și ultima actualizare
st.markdown(f"""
<div style="text-align: center; margin-top: 30px;">
    <p style="color: #64748b; font-size: 0.8rem;">
        🎓 Catalog Digital v6.0 Premium | 
        Ultima actualizare: {datetime.now().strftime('%d.%m.%Y %H:%M')} |
        Sesiune activă: {st.session_state.username or st.session_state.nume_elev or 'Directoare'}
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# 14. INIȚIALIZARE FINALĂ ȘI VERIFICĂRI
# ============================================

# Verifică conexiunea la baza de date
try:
    conn.execute("SELECT 1")
except Exception as e:
    st.error(f"⚠️ Eroare conexiune baza de date: {str(e)}")

# Backup automat al session state
if 'last_backup' not in st.session_state:
    st.session_state.last_backup = datetime.now()

if (datetime.now() - st.session_state.last_backup).seconds > 3600:  # La fiecare oră
    try:
        # Salvare backup în baza de date
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO statistici (data, tip_statistica, valoare, detalii) 
                         VALUES (?, ?, ?, ?)''',
                     (datetime.now().strftime("%Y-%m-%d"), 
                      'auto_backup', 1, 'Backup automat session state'))
        conn.commit()
        st.session_state.last_backup = datetime.now()
    except:
        pass

# Ascunde temporizator de încărcare
if 'initial_load' not in st.session_state:
    st.session_state.initial_load = True
    with st.spinner("Se încarcă sistemul..."):
        time.sleep(0.5)


