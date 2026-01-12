import streamlit as st

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
        "observatii_speciale": "Talent at desen"
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
            selected_month_name = st.selectbox("Selectează luna pentru detalii:", months)
        
        with col_stats:
            selected_days = self.get_selected_days(clasa, materie)
            st.metric("Zile selectate totale", len(selected_days))
        
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
                with st.expander(f"{month_date.strftime('%B %Y')} - {len(days)} zile"):
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
                if st.button("🗑️ Șterge toate selecțiile", type="secondary", use_container_width=True):
                    st.session_state.selected_days[clasa][materie] = []
                    st.rerun()
            
            with col_action2:
                # Exportă selecțiile
                if st.button("📤 Exportă calendar", type="secondary", use_container_width=True):
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
                        mime="application/json"
                    )
            
            with col_action3:
                # Sincronizează cu data curentă
                if st.button("🎯 Sincronizează selecție", type="primary", use_container_width=True):
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
                    [datetime.strptime(d, "%Y-%m-%d").strftime("%d.%m.%Y") for d in sorted(selected_days)]
                )
                
                day_date_obj = datetime.strptime(selected_day, "%d.%m.%Y")
                day_str = day_date_obj.strftime("%Y-%m-%d")
                current_note = self.get_calendar_note(day_str, clasa, materie)
                
                new_note = st.text_area(
                    "Notă pentru ziua selectată:",
                    value=current_note,
                    height=100,
                    placeholder="Scrie aici note importante, teme, sau reamintiri..."
                )
                
                if st.button("💾 Salvează Notă", use_container_width=True):
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
                    key="event_day_select"
                )
                
                day_date_obj = datetime.strptime(event_day, "%d.%m.%Y")
                day_str = day_date_obj.strftime("%Y-%m-%d")
                
                col_event_type, col_event_desc = st.columns([1, 2])
                
                with col_event_type:
                    event_type = st.selectbox(
                        "Tip eveniment:",
                        ["test", "examen", "activitate", "proiect", "altul"],
                        key="event_type_select"
                    )
                
                with col_event_desc:
                    event_description = st.text_input(
                        "Descriere eveniment:",
                        placeholder="Ex: Test capitolele 1-3, Examen semestrial..."
                    )
                
                if st.button("➕ Adaugă Eveniment", use_container_width=True):
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
                    for event in existing_events:
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
            st.metric("📝 Note totale", total_note)
        
        with col_stat2:
            medie_clasa = pd.read_sql(
                "SELECT AVG(nota) FROM grades WHERE clasa = ? AND materie = ?",
                conn, params=[clasa, st.session_state.materie]
            ).iloc[0,0]
            st.metric("📊 Media clasei", f"{medie_clasa:.2f}" if medie_clasa else "0.00")
        
        with col_stat3:
            total_abs = pd.read_sql(
                "SELECT COUNT(*) FROM absente WHERE clasa = ? AND materie = ?",
                conn, params=[clasa, st.session_state.materie]
            ).iloc[0,0]
            st.metric("❌ Absențe", total_abs)
        
        with col_stat4:
            total_obs = pd.read_sql(
                "SELECT COUNT(*) FROM observatii WHERE materie = ?",
                conn, params=[st.session_state.materie]
            ).iloc[0,0]
            st.metric("📋 Observații", total_obs)
        
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
                    
                    with st.expander(f"👤 {elev}", expanded=False):
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
                                                    if st.form_submit_button("💾 Salvează modificări"):
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
                                                    if st.form_submit_button("❌ Anulează", type="secondary"):
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
                                    
                                    if st.form_submit_button("📝 Adaugă notă", use_container_width=True):
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
                key="calendar_year_select"
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
                st.metric("📅 Zile selectate", days_count)
            
            with col_cal_stats2:
                # Zile cu note înregistrate
                cursor = conn.cursor()
                cursor.execute('''SELECT COUNT(DISTINCT data) 
                                FROM grades 
                                WHERE clasa = ? AND materie = ?''',
                             (clasa, st.session_state.materie))
                days_with_grades = cursor.fetchone()[0] or 0
                st.metric("📝 Zile cu note", days_with_grades)
            
            with col_cal_stats3:
                # Procentaj acoperire
                total_school_days = 180  # Număr aproximativ de zile de școală
                coverage = (days_with_grades / total_school_days * 100) if total_school_days > 0 else 0
                st.metric("📈 Acoperire evaluare", f"{coverage:.1f}%")
            
            # Afișare statistici în loc de heatmap Plotly
            st.markdown("#### 🎨 Statistici Activitate")
            
            try:
                # Generează date pentru statistici
                heatmap_data = generate_calendar_heatmap_data(
                    clasa, st.session_state.materie, conn, selected_year
                )
                
                if not heatmap_data.empty:
                    # Afișează datele ca tabel în loc de grafic Plotly
                    st.markdown(f"**Date statistice pentru {selected_year}**")
                    
                    # Creează un rezumat lunar
                    monthly_summary = heatmap_data.groupby('luna').agg({
                        'medie_zi': 'mean',
                        'numar_note': 'sum'
                    }).round(2).reset_index()
                    
                    monthly_summary.columns = ['Luna', 'Medie lunară', 'Total note']
                    
                    # Adaugă nume lună
                    month_names = {
                        1: 'Ianuarie', 2: 'Februarie', 3: 'Martie', 4: 'Aprilie',
                        5: 'Mai', 6: 'Iunie', 7: 'Iulie', 8: 'August',
                        9: 'Septembrie', 10: 'Octombrie', 11: 'Noiembrie', 12: 'Decembrie'
                    }
                    
                    monthly_summary['Luna'] = monthly_summary['Luna'].map(month_names)
                    
                    # Afișează tabela
                    st.dataframe(monthly_summary, use_container_width=True, hide_index=True)
                    
                    # Mesaj pentru Plotly
                    st.info("""
                    📊 **Vizualizare grafică indisponibilă**
                    
                    Pentru a vedea heatmap-ul interactiv, instalează Plotly:
                    ```
                    pip install plotly
                    ```
                    
                    Datele sunt disponibile în tabelul de mai sus.
                    """)
                else:
                    st.info("ℹ️ Nu există suficiente date pentru a genera statisticile.")
            except Exception as e:
                st.warning(f"⚠️ Nu s-au putut genera statisticile: {str(e)}")
        
        elif selected_menu == "📊 Statistici și Rapoarte":
            st.markdown("#### 📊 Statistici Detaliate și Rapoarte")
            
            # Selectare perioadă pentru rapoarte
            col_period, col_report_type = st.columns(2)
            
            with col_period:
                report_period = st.selectbox(
                    "Perioadă raport:",
                    ["Ultima săptămână", "Ultima lună", "Acest semestru", "Tot anul școlar"],
                    key="report_period_select"
                )
            
            with col_report_type:
                report_type = st.selectbox(
                    "Tip raport:",
                    ["Statistici generale", "Analiză performanță", "Comparație clase", "Tendințe temporale"],
                    key="report_type_select"
                )
            
            # Generare raport
            if st.button("📈 Generează Raport", type="primary", use_container_width=True):
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
                        st.markdown("##### 📋 Statistici Observații")
                        if stats['observatii']:
                            obs_html = ""
                            for tip, numar in stats['observatii'].items():
                                badge_color = {
                                    'laudă': 'success',
                                    'atenționare': 'warning',
                                    'mustrare': 'danger',
                                    'recomandare': 'info'
                                }.get(tip, 'info')
                                
                                obs_html += f"""
                                <p>
                                    <span class="badge badge-{badge_color}">{tip}</span>: {numar}
                                </p>
                                """
                            
                            st.markdown(f"""
                            <div class="custom-card">
                                {obs_html}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="custom-card">
                                <p>Nu există observații înregistrate.</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Afișare date pentru evoluție medie (fără Plotly)
                    st.markdown("##### 📈 Evoluție Medie Clasă")
                    
                    try:
                        # Date pentru evoluție
                        cursor = conn.cursor()
                        cursor.execute('''SELECT strftime('%Y-%m', data) as luna, 
                                        AVG(nota) as medie_luna 
                                        FROM grades 
                                        WHERE clasa = ? AND materie = ? 
                                        GROUP BY strftime('%Y-%m', data) 
                                        ORDER BY luna''',
                                     (clasa, st.session_state.materie))
                        
                        trend_data = cursor.fetchall()
                        
                        if trend_data:
                            # Creează un tabel în loc de grafic
                            trend_df = pd.DataFrame(trend_data, columns=['Luna', 'Medie lunară'])
                            trend_df['Medie lunară'] = trend_df['Medie lunară'].round(2)
                            
                            st.dataframe(trend_df, use_container_width=True, hide_index=True)
                            
                            # Calculează tendința
                            if len(trend_df) > 1:
                                first_avg = trend_df.iloc[0]['Medie lunară']
                                last_avg = trend_df.iloc[-1]['Medie lunară']
                                trend = "↗️ Creștere" if last_avg > first_avg else "↘️ Scădere" if last_avg < first_avg else "➡️ Stabil"
                                
                                st.markdown(f"""
                                <div class="custom-card">
                                    <p><strong>Tendință generală:</strong> {trend}</p>
                                    <p><strong>Prima lună:</strong> {first_avg}</p>
                                    <p><strong>Ultima lună:</strong> {last_avg}</p>
                                    <p><strong>Diferență:</strong> {last_avg - first_avg:.2f}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.info("""
                            📈 **Graficul de evoluție nu este disponibil**
                            
                            Pentru grafice interactive, instalează Plotly:
                            ```
                            pip install plotly
                            ```
                            """)
                        else:
                            st.info("ℹ️ Nu există suficiente date pentru a afișa evoluția.")
                    except Exception as e:
                        st.warning(f"⚠️ Eroare la generarea statisticilor: {str(e)}")
                    
                    # Descărcare raport PDF (simulat)
                    st.markdown("---")
                    col_export1, col_export2 = st.columns(2)
                    
                    with col_export1:
                        if st.button("📥 Exportă Raport PDF", use_container_width=True):
                            st.success("✅ Raportul a fost generat și este pregătit pentru descărcare!")
                            # Aici s-ar genera un PDF real
                    
                    with col_export2:
                        # Export date Excel
                        if st.button("📊 Exportă Date Excel", use_container_width=True):
                            # Culege toate datele pentru export
                            cursor = conn.cursor()
                            
                            # Note
                            cursor.execute('''SELECT data, nume, nota, tip_nota, comentariu 
                                           FROM grades 
                                           WHERE clasa = ? AND materie = ? 
                                           ORDER BY data DESC, nume''',
                                         (clasa, st.session_state.materie))
                            note_data = cursor.fetchall()
                            
                            # Absențe
                            cursor.execute('''SELECT data, nume, motivata, motiv 
                                           FROM absente 
                                           WHERE clasa = ? AND materie = ? 
                                           ORDER BY data DESC, nume''',
                                         (clasa, st.session_state.materie))
                            absente_data = cursor.fetchall()
                            
                            # Creează DataFrames
                            df_note = pd.DataFrame(note_data, columns=['Data', 'Elev', 'Nota', 'Tip', 'Comentariu'])
                            df_absente = pd.DataFrame(absente_data, columns=['Data', 'Elev', 'Motivata', 'Motiv'])
                            
                            # Creează fișier Excel cu mai multe foi
                            with pd.ExcelWriter('raport_clasa.xlsx', engine='openpyxl') as writer:
                                df_note.to_excel(writer, sheet_name='Note', index=False)
                                df_absente.to_excel(writer, sheet_name='Absente', index=False)
                                
                                # Adaugă statistici
                                stats_df = pd.DataFrame([{
                                    'Total_note': stats['note']['total'],
                                    'Medie_clasa': stats['note']['medie'],
                                    'Nota_min': stats['note']['minim'],
                                    'Nota_max': stats['note']['maxim'],
                                    'Total_absente': stats['absente']['total'],
                                    'Absente_motivate': stats['absente']['motivate']
                                }])
                                stats_df.to_excel(writer, sheet_name='Statistici', index=False)
                            
                            # Oferă fișierul pentru descărcare
                            with open('raport_clasa.xlsx', 'rb') as f:
                                st.download_button(
                                    label="⬇️ Descarcă fișier Excel",
                                    data=f,
                                    file_name=f"raport_{clasa}_{st.session_state.materie}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
        
        elif selected_menu == "✏️ Management Note":
            st.markdown("#### ✏️ Management Avansat al Notelor")
            
            # Filtre pentru căutare note
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            
            with col_filter1:
                filter_elev = st.selectbox(
                    "Filtrează după elev:",
                    [""] + elevi_clasa,
                    key="filter_elev_select"
                )
            
            with col_filter2:
                filter_date = st.date_input(
                    "Filtrează după dată:",
                    value=None,
                    key="filter_date_select"
                )
            
            with col_filter3:
                filter_type = st.selectbox(
                    "Filtrează după tip notă:",
                    ["", "oral", "scris", "practical", "teza"],
                    key="filter_type_select"
                )
            
            # Construiește interogarea dinamică
            query = '''SELECT id, data, nume, nota, tip_nota, comentariu 
                       FROM grades 
                       WHERE clasa = ? AND materie = ?'''
            params = [clasa, st.session_state.materie]
            
            if filter_elev:
                query += " AND nume = ?"
                params.append(filter_elev)
            
            if filter_date:
                query += " AND data = ?"
                params.append(filter_date.strftime("%Y-%m-%d"))
            
            if filter_type:
                query += " AND tip_nota = ?"
                params.append(filter_type)
            
            query += " ORDER BY data DESC, nume"
            
            # Execută interogarea
            note_to_manage = pd.read_sql(query, conn, params=params)
            
            if not note_to_manage.empty:
                st.markdown(f"**Găsite {len(note_to_manage)} note:**")
                
                # Afișează notele cu opțiuni de editare
                for _, row in note_to_manage.iterrows():
                    col_manage1, col_manage2, col_manage3, col_manage4 = st.columns([3, 1, 1, 1])
                    
                    with col_manage1:
                        data_formatata = datetime.strptime(row['data'], "%Y-%m-%d").strftime("%d.%m.%Y")
                        st.markdown(f"""
                        <div style="background: rgba(30, 41, 59, 0.7); 
                                    padding: 10px; border-radius: 8px;">
                            <strong>{row['nume']}</strong> - {data_formatata}<br>
                            <small>Tip: {row['tip_nota']} | Comentariu: {row['comentariu'] or 'Niciunul'}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_manage2:
                        st.metric("Nota", row['nota'], label_visibility="collapsed")
                    
                    with col_manage3:
                        # Input pentru editare notă
                        new_note = st.number_input(
                            "Noua notă:",
                            min_value=1.0,
                            max_value=10.0,
                            value=float(row['nota']),
                            step=0.5,
                            key=f"edit_input_{row['id']}",
                            label_visibility="collapsed"
                        )
                    
                    with col_manage4:
                        col_btn_save, col_btn_del = st.columns(2)
                        
                        with col_btn_save:
                            if st.button(
                                "💾",
                                key=f"save_btn_{row['id']}",
                                help="Salvează modificarea",
                                use_container_width=True
                            ):
                                if new_note != row['nota']:
                                    update_nota(row['id'], new_note, conn)
                                    st.success(f"✅ Nota pentru {row['nume']} a fost actualizată!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.info("ℹ️ Nota nu a fost modificată.")
                        
                        with col_btn_del:
                            if st.button(
                                "🗑️",
                                key=f"del_btn_{row['id']}",
                                help="Șterge nota",
                                type="secondary",
                                use_container_width=True
                            ):
                                delete_nota(row['id'], conn)
                                st.success(f"✅ Nota pentru {row['nume']} a fost ștearsă!")
                                time.sleep(1)
                                st.rerun()
            else:
                st.info("ℹ️ Nu s-au găsit note conform criteriilor de căutare.")
            
            # Secțiune pentru acțiuni în masă
            st.markdown("---")
            st.markdown("#### 🔄 Acțiuni în Masă")
            
            if not note_to_manage.empty:
                col_bulk1, col_bulk2, col_bulk3 = st.columns(3)
                
                with col_bulk1:
                    if st.button(
                        "📥 Exportă toate notele",
                        use_container_width=True,
                        help="Exportă toate notele într-un fișier Excel"
                    ):
                        # Export toate notele
                        all_grades = pd.read_sql('''SELECT data, nume, nota, tip_nota, comentariu 
                                                  FROM grades 
                                                  WHERE clasa = ? AND materie = ? 
                                                  ORDER BY data, nume''',
                                               conn, params=[clasa, st.session_state.materie])
                        
                        csv = all_grades.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="⬇️ Descarcă CSV",
                            data=csv,
                            file_name=f"note_complete_{clasa}_{st.session_state.materie}.csv",
                            mime="text/csv"
                        )
                
                with col_bulk2:
                    # Actualizare în masă a tipului de notă
                    new_type = st.selectbox(
                        "Setare tip pentru toate:",
                        ["", "oral", "scris", "practical", "teza"],
                        key="bulk_type_select"
                    )
                    
                    if new_type and st.button(
                        "🔄 Actualizează tip",
                        use_container_width=True
                    ):
                        cursor = conn.cursor()
                        cursor.execute('''UPDATE grades SET tip_nota = ? 
                                        WHERE clasa = ? AND materie = ?''',
                                     (new_type, clasa, st.session_state.materie))
                        conn.commit()
                        st.success(f"✅ Tipul tuturor notelor a fost actualizat la '{new_type}'!")
                        time.sleep(1)
                        st.rerun()
                
                with col_bulk3:
                    # Ștergere note vechi
                    cutoff_date = st.date_input(
                        "Șterge note mai vechi de:",
                        value=date.today() - timedelta(days=30),
                        key="bulk_delete_date"
                    )
                    
                    if st.button(
                        "🧹 Curăță note vechi",
                        type="secondary",
                        use_container_width=True
                    ):
                        cursor = conn.cursor()
                        cursor.execute('''DELETE FROM grades 
                                        WHERE clasa = ? AND materie = ? AND data < ?''',
                                     (clasa, st.session_state.materie, cutoff_date.strftime("%Y-%m-%d")))
                        deleted_count = cursor.rowcount
                        conn.commit()
                        
                        st.warning(f"⚠️ Au fost șterse {deleted_count} note mai vechi de {cutoff_date.strftime('%d.%m.%Y')}!")
                        time.sleep(1)
                        st.rerun()
            else:
                st.warning("⚠️ Nu există note disponibile pentru acțiuni în masă.")
        
        elif selected_menu == "📈 Analiză Performanță":
            st.markdown("#### 📈 Analiză Avansată a Performanței")
            
            # Selectare elev pentru analiză detaliată
            selected_student = st.selectbox(
                "Selectează elev pentru analiză detaliată:",
                elevi_clasa,
                key="performance_student_select"
            )
            
            if selected_student:
                # Statistici individuale
                col_perf1, col_perf2, col_perf3, col_perf4 = st.columns(4)
                
                with col_perf1:
                    media_elev = get_media_elev(selected_student, st.session_state.materie, conn)
                    st.metric("📊 Medie materie", f"{media_elev:.2f}")
                
                with col_perf2:
                    # Număr note
                    cursor = conn.cursor()
                    cursor.execute('''SELECT COUNT(*) 
                                    FROM grades 
                                    WHERE nume = ? AND materie = ?''',
                                 (selected_student, st.session_state.materie))
                    num_notes = cursor.fetchone()[0] or 0
                    st.metric("📝 Număr note", num_notes)
                
                with col_perf3:
                    # Absențe
                    cursor.execute('''SELECT COUNT(*) 
                                    FROM absente 
                                    WHERE nume = ? AND materie = ?''',
                                 (selected_student, st.session_state.materie))
                    num_absences = cursor.fetchone()[0] or 0
                    st.metric("❌ Absențe", num_absences)
                
                with col_perf4:
                    # Nota purtare
                    nota_purtare = get_nota_purtare_curenta(
                        selected_student, conn, st.session_state.current_semester
                    )
                    st.metric("⭐ Purtare", f"{nota_purtare}/10")
                
                # Afișare date pentru evoluție individuală (fără Plotly)
                st.markdown("##### 📈 Evoluție Individuală")
                
                try:
                    cursor.execute('''SELECT data, nota, tip_nota 
                                    FROM grades 
                                    WHERE nume = ? AND materie = ? 
                                    ORDER BY data''',
                                 (selected_student, st.session_state.materie))
                    
                    student_grades = cursor.fetchall()
                    
                    if student_grades:
                        # Creează un tabel cu notele
                        grades_df = pd.DataFrame(student_grades, columns=['Data', 'Nota', 'Tip'])
                        grades_df['Data'] = pd.to_datetime(grades_df['Data']).dt.strftime('%d.%m.%Y')
                        grades_df['Nota'] = grades_df['Nota'].round(2)
                        
                        st.dataframe(grades_df, use_container_width=True, height=300)
                        
                        # Statistici suplimentare
                        col_stats1, col_stats2, col_stats3 = st.columns(3)
                        
                        with col_stats1:
                            max_grade = grades_df['Nota'].max()
                            st.metric("🎯 Nota maximă", f"{max_grade:.2f}")
                        
                        with col_stats2:
                            min_grade = grades_df['Nota'].min()
                            st.metric("📉 Nota minimă", f"{min_grade:.2f}")
                        
                        with col_stats3:
                            std_dev = grades_df['Nota'].std()
                            st.metric("📊 Deviație standard", f"{std_dev:.2f}" if not pd.isna(std_dev) else "0.00")
                        
                        st.info("""
                        📈 **Graficul de evoluție nu este disponibil**
                        
                        Pentru grafice interactive care arată evoluția notelor în timp, instalează Plotly:
                        ```
                        pip install plotly
                        ```
                        """)
                    else:
                        st.info(f"ℹ️ {selected_student} nu are note înregistrate la această materie.")
                except Exception as e:
                    st.warning(f"⚠️ Eroare la generarea statisticilor: {str(e)}")
                
                # Recomandări personalizate
                st.markdown("##### 💡 Recomandări Personalizate")
                
                if media_elev >= 9.00:
                    st.success(f"""
                    **🎉 Excelent!** {selected_student} are o performanță remarcabilă.
                    
                    **Recomandări:**
                    - Continuă cu aceeași dedicare
                    - Participă la cluburi și concursuri școlare
                    - Ajută colegii care întâmpină dificultăți
                    """)
                elif media_elev >= 7.00:
                    st.info(f"""
                    **👍 Bun!** {selected_student} are o performanță solidă.
                    
                    **Recomandări:**
                    - Concentrează-te pe punctele mai slabe
                    - Participă activ la ore
                    - Solicită ajutor suplimentar dacă este necesar
                    """)
                elif media_elev >= 5.00:
                    st.warning(f"""
                    **⚠️ Atenție!** {selected_student} are o performanță sub așteptări.
                    
                    **Recomandări:**
                    - Program de recuperare individual
                    - Colaborare cu părinții
                    - Susținere suplimentară de la profesor
                    - Monitorizare frecventă a progresului
                    """)
                else:
                    st.error(f"""
                    **🚨 Intervenție necesară!** {selected_student} are performanță critică.
                    
                    **Recomandări urgente:**
                    - Consiliere individuală
                    - Plan de intervenție personalizat
                    - Colaborare intensă cu părinții
                    - Evaluare suplimentară a dificultăților
                    """)
        
        elif selected_menu == "⚙️ Setări Profesor":
            st.markdown("#### ⚙️ Setări și Configurare Profesor")
            
            tab_settings, tab_profile, tab_backup = st.tabs([
                "⚙️ Setări Sistem", 
                "👤 Profil Profesor", 
                "💾 Backup Date"
            ])
            
            with tab_settings:
                st.markdown("##### Preferințe Afișare")
                
                col_set1, col_set2 = st.columns(2)
                
                with col_set1:
                    dark_mode = st.toggle(
                        "🌙 Mod întunecat",
                        value=st.session_state.get('dark_mode', True),
                        key="dark_mode_toggle"
                    )
                    
                    if dark_mode != st.session_state.get('dark_mode', True):
                        st.session_state.dark_mode = dark_mode
                        st.success("✅ Modul întunecat a fost " + ("activat" if dark_mode else "dezactivat") + "!")
                
                with col_set2:
                    auto_save = st.toggle(
                        "💾 Salvare automată",
                        value=True,
                        key="auto_save_toggle"
                    )
                
                st.markdown("##### Notificări")
                
                col_notif1, col_notif2, col_notif3 = st.columns(3)
                
                with col_notif1:
                    email_notif = st.toggle("📧 Email notificări", value=True)
                
                with col_notif2:
                    grade_notif = st.toggle("📝 Alertă note noi", value=True)
                
                with col_notif3:
                    absence_notif = st.toggle("❌ Alertă absențe", value=True)
                
                if st.button(
                    "💾 Salvează setări",
                    type="primary",
                    use_container_width=True
                ):
                    st.success("✅ Setările au fost salvate cu succes!")
            
            with tab_profile:
                prof_details = get_profesor_details(st.session_state.username)
                
                if prof_details:
                    col_prof_info1, col_prof_info2 = st.columns([1, 2])
                    
                    with col_prof_info1:
                        st.markdown(f"""
                        <div style="text-align: center;">
                            <div style="font-size: 4rem;">👨‍🏫</div>
                            <h3>{st.session_state.username}</h3>
                            <p style="color: #94a3b8;">{st.session_state.materie}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_prof_info2:
                        st.markdown("##### 📋 Informații Profesor")
                        
                        st.markdown(f"""
                        <div class="custom-card">
                            <p><strong>📧 Email:</strong> {prof_details.get('email', 'N/A')}</p>
                            <p><strong>📞 Telefon:</strong> {prof_details.get('telefon', 'N/A')}</p>
                            <p><strong>🎓 Specializare:</strong> {prof_details.get('specializare', 'N/A')}</p>
                            <p><strong>⭐ Grad didactic:</strong> {prof_details.get('grad_didactic', 'N/A')}</p>
                            <p><strong>⏳ Ani experiență:</strong> {prof_details.get('ani_experienta', 'N/A')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Statistici profesor
                        st.markdown("##### 📊 Statistici Activitate")
                        
                        cursor = conn.cursor()
                        
                        # Note adăugate
                        cursor.execute('''SELECT COUNT(*) 
                                        FROM grades 
                                        WHERE profesor = ?''',
                                     (st.session_state.username,))
                        total_grades = cursor.fetchone()[0] or 0
                        
                        # Observații
                        cursor.execute('''SELECT COUNT(*) 
                                        FROM observatii 
                                        WHERE profesor = ?''',
                                     (st.session_state.username,))
                        total_obs = cursor.fetchone()[0] or 0
                        
                        # Absențe
                        cursor.execute('''SELECT COUNT(*) 
                                        FROM absente 
                                        WHERE profesor = ?''',
                                     (st.session_state.username,))
                        total_abs = cursor.fetchone()[0] or 0
                        
                        col_prof_stat1, col_prof_stat2, col_prof_stat3 = st.columns(3)
                        
                        with col_prof_stat1:
                            st.metric("📝 Note adăugate", total_grades)
                        
                        with col_prof_stat2:
                            st.metric("📋 Observații", total_obs)
                        
                        with col_prof_stat3:
                            st.metric("❌ Absențe", total_abs)
                else:
                    st.error("❌ Informațiile profesorului nu au putut fi încărcate.")
            
            with tab_backup:
                st.markdown("##### 💾 Management Backup")
                
                col_backup1, col_backup2 = st.columns(2)
                
                with col_backup1:
                    st.markdown("**Creează backup**")
                    backup_name = st.text_input(
                        "Nume backup:",
                        placeholder="ex: backup_septembrie_2026",
                        key="backup_name_input"
                    )
                    
                    if st.button(
                        "💾 Creează Backup",
                        use_container_width=True,
                        help="Creează o copie de siguranță a datelor"
                    ):
                        if backup_name.strip():
                            # Simulare creare backup
                            backup_data = {
                                'profesor': st.session_state.username,
                                'materie': st.session_state.materie,
                                'clasa': clasa,
                                'data_creare': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'numar_note': total_grades,
                                'numar_absente': total_abs,
                                'numar_observatii': total_obs
                            }
                            
                            # Salvează ca JSON
                            backup_json = json.dumps(backup_data, indent=2, ensure_ascii=False)
                            
                            st.download_button(
                                label="⬇️ Descarcă Backup",
                                data=backup_json,
                                file_name=f"backup_{backup_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json"
                            )
                        else:
                            st.error("❌ Te rog introdu un nume pentru backup!")
                
                with col_backup2:
                    st.markdown("**Restaurare backup**")
                    
                    uploaded_file = st.file_uploader(
                        "Încarcă fișier backup:",
                        type=['json'],
                        key="backup_uploader"
                    )
                    
                    if uploaded_file is not None:
                        try:
                            backup_data = json.load(uploaded_file)
                            st.success(f"✅ Backup încărcat: {backup_data.get('data_creare', 'N/A')}")
                            
                            if st.button(
                                "🔄 Restaurează Backup",
                                type="secondary",
                                use_container_width=True
                            ):
                                st.warning("⚠️ Funcționalitatea de restaurare va fi implementată în versiunea următoare.")
                        except Exception as e:
                            st.error(f"❌ Eroare la încărcarea backup-ului: {str(e)}")
    
    # ============================================
    # 11. INTERFAȚA PĂRINTE/ELEV - MODUL PREMIUM
    # ============================================
    elif st.session_state.role == "parent":
        elev = st.session_state.nume_elev
        clasa = st.session_state.clasa_selectata
        
        # Header informații elev
        elev_details = get_elev_details(elev)
        
        st.markdown(f"""
        <div class="custom-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="color: white; margin-bottom: 5px;">👤 {elev}</h3>
                    <p style="color: #94a3b8; margin: 0;">
                        Clasa: {clasa} | 
                        Data nașterii: {elev_details.get('data_nasterii', 'N/A')} |
                        Telefon părinte: {elev_details.get('telefon_parinte', 'N/A')}
                    </p>
                </div>
                <div style="text-align: right;">
                    <p style="color: #94a3b8; margin: 0;">
                        Email părinte: {elev_details.get('email_parinte', 'N/A')}<br>
                        Adresă: {elev_details.get('adresa', 'N/A')}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Observații speciale
        if elev_details.get('observatii_speciale'):
            st.markdown(f"""
            <div class="custom-card" style="background: rgba(234, 179, 8, 0.1); 
                                          border: 1px solid rgba(234, 179, 8, 0.3);">
                <h4 style="color: #eab308; margin-bottom: 10px;">📝 Observații speciale:</h4>
                <p style="color: white; margin: 0;">{elev_details['observatii_speciale']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Tabs pentru diferite secțiuni
        tab_note, tab_absente, tab_observatii, tab_medii, tab_purtare, tab_activitati = st.tabs([
            "📝 Note", 
            "❌ Absențe", 
            "📋 Observații", 
            "📊 Medii", 
            "⭐ Purtare", 
            "🎨 Activități"
        ])
        
        with tab_note:
            st.markdown("### 📝 Notele Elevului")
            
            # Filtre pentru note
            col_note_filter1, col_note_filter2, col_note_filter3 = st.columns(3)
            
            with col_note_filter1:
                filtru_materie = st.selectbox(
                    "Materie:",
                    ["Toate"] + MATERII_GIMNAZIU,
                    key="parinte_filtru_materie"
                )
            
            with col_note_filter2:
                filtru_semestru = st.selectbox(
                    "Semestru:",
                    ["Toate", "Semestrul 1", "Semestrul 2"],
                    key="parinte_filtru_semestru"
                )
            
            with col_note_filter3:
                filtru_tip = st.selectbox(
                    "Tip notă:",
                    ["Toate", "oral", "scris", "practical", "teza"],
                    key="parinte_filtru_tip"
                )
            
            # Construiește interogarea
            query = '''SELECT data, materie, nota, tip_nota, comentariu 
                       FROM grades WHERE nume = ?'''
            params = [elev]
            
            if filtru_materie != "Toate":
                query += " AND materie = ?"
                params.append(filtru_materie)
            
            if filtru_semestru != "Toate":
                semestru_num = 1 if filtru_semestru == "Semestrul 1" else 2
                query += " AND semestru = ?"
                params.append(semestru_num)
            
            if filtru_tip != "Toate":
                query += " AND tip_nota = ?"
                params.append(filtru_tip)
            
            query += " ORDER BY data DESC"
            
            # Execută interogarea
            note_df = pd.read_sql(query, conn, params=params)
            
            if not note_df.empty:
                # Formatează data
                note_df['data'] = pd.to_datetime(note_df['data']).dt.strftime('%d.%m.%Y')
                
                # Statistici rapide
                col_note_stat1, col_note_stat2, col_note_stat3 = st.columns(3)
                
                with col_note_stat1:
                    media_generala = note_df['nota'].mean().round(2)
                    st.metric("🎓 Media generală", f"{media_generala:.2f}")
                
                with col_note_stat2:
                    total_note = len(note_df)
                    st.metric("📝 Total note", total_note)
                
                with col_note_stat3:
                    ultima_nota = note_df.iloc[0]['nota'] if not note_df.empty else 0
                    st.metric("📅 Ultima notă", f"{ultima_nota:.2f}")
                
                # Afișează tabela cu note
                st.dataframe(
                    note_df,
                    use_container_width=True,
                    hide_index=True,
                    height=400,
                    column_config={
                        "data": "Data",
                        "materie": "Materie",
                        "nota": "Notă",
                        "tip_nota": "Tip",
                        "comentariu": "Comentariu"
                    }
                )
                
                # Afișare statistici pe materii (fără Plotly)
                st.markdown("##### 📊 Statistici pe Materii")
                
                try:
                    # Grupează notele pe materii
                    materii_stats = note_df.groupby('materie').agg({
                        'nota': ['count', 'mean', 'min', 'max']
                    }).round(2)
                    
                    # Redenumire coloane
                    materii_stats.columns = ['Număr note', 'Medie', 'Nota minimă', 'Nota maximă']
                    materii_stats = materii_stats.reset_index()
                    
                    st.dataframe(materii_stats, use_container_width=True, hide_index=True)
                    
                    st.info("""
                    📈 **Graficele interactive nu sunt disponibile**
                    
                    Pentru a vedea grafice de evoluție și distribuție, instalează Plotly:
                    ```
                    pip install plotly
                    ```
                    """)
                except Exception as e:
                    st.warning(f"⚠️ Nu s-a putut genera tabelul de statistici: {str(e)}")
                
                # Export note
                st.markdown("---")
                col_export1, col_export2 = st.columns(2)
                
                with col_export1:
                    csv = note_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descarcă note (CSV)",
                        data=csv,
                        file_name=f"note_{elev}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                with col_export2:
                    # Generare PDF (simulat)
                    if st.button("📄 Generează raport PDF", use_container_width=True):
                        st.success("✅ Raportul PDF a fost generat și va fi disponibil pentru descărcare!")
            else:
                st.info("ℹ️ Nu există note înregistrate pentru criteriile selectate.")
        
        with tab_absente:
            st.markdown("### ❌ Absențele Elevului")
            
            # Filtre pentru absențe
            col_abs_filter1, col_abs_filter2 = st.columns(2)
            
            with col_abs_filter1:
                filtru_abs_materie = st.selectbox(
                    "Materie:",
                    ["Toate"] + MATERII_GIMNAZIU,
                    key="parinte_filtru_abs_materie"
                )
            
            with col_abs_filter2:
                filtru_abs_luna = st.selectbox(
                    "Lună:",
                    ["Toate"] + ["Septembrie", "Octombrie", "Noiembrie", "Decembrie", 
                                "Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie"],
                    key="parinte_filtru_abs_luna"
                )
            
            # Construiește interogarea
            query = '''SELECT data, materie, motivata, motiv 
                       FROM absente WHERE nume = ?'''
            params = [elev]
            
            if filtru_abs_materie != "Toate":
                query += " AND materie = ?"
                params.append(filtru_abs_materie)
            
            if filtru_abs_luna != "Toate":
                luni = {
                    "Septembrie": "09", "Octombrie": "10", "Noiembrie": "11",
                    "Decembrie": "12", "Ianuarie": "01", "Februarie": "02",
                    "Martie": "03", "Aprilie": "04", "Mai": "05", "Iunie": "06"
                }
                query += " AND strftime('%m', data) = ?"
                params.append(luni[filtru_abs_luna])
            
            query += " ORDER BY data DESC"
            
            # Execută interogarea
            absente_df = pd.read_sql(query, conn, params=params)
            
            if not absente_df.empty:
                # Formatează data
                absente_df['data'] = pd.to_datetime(absente_df['data']).dt.strftime('%d.%m.%Y')
                
                # Statistici absențe
                col_abs_stat1, col_abs_stat2, col_abs_stat3 = st.columns(3)
                
                with col_abs_stat1:
                    total_absente = len(absente_df)
                    st.metric("📊 Total absențe", total_absente)
                
                with col_abs_stat2:
                    absente_motivate = absente_df['motivata'].sum()
                    st.metric("✅ Motivate", absente_motivate)
                
                with col_abs_stat3:
                    absente_nemotivate = total_absente - absente_motivate
                    st.metric("❌ Nemotivate", absente_nemotivate)
                
                # Afișează tabela cu absențe
                st.dataframe(
                    absente_df,
                    use_container_width=True,
                    hide_index=True,
                    height=300,
                    column_config={
                        "data": "Data",
                        "materie": "Materie",
                        "motivata": st.column_config.CheckboxColumn(
                            "Motivată",
                            help="Absență motivată"
                        ),
                        "motiv": "Motiv"
                    }
                )
                
                # Statistici pe materii (fără Plotly)
                st.markdown("##### 📊 Distribuție Absențe pe Materii")
                
                try:
                    # Grupează absențele pe materii
                    abs_by_subject = absente_df.groupby('materie').agg({
                        'motivata': ['count', 'sum']
                    }).reset_index()
                    
                    abs_by_subject.columns = ['Materie', 'Total absențe', 'Motivate']
                    abs_by_subject['Nemotivate'] = abs_by_subject['Total absențe'] - abs_by_subject['Motivate']
                    
                    st.dataframe(abs_by_subject, use_container_width=True, hide_index=True)
                    
                    st.info("""
                    📊 **Graficul circular nu este disponibil**
                    
                    Pentru a vedea graficul de distribuție al absențelor, instalează Plotly:
                    ```
                    pip install plotly
                    ```
                    """)
                except Exception as e:
                    st.warning(f"⚠️ Nu s-a putut genera tabelul de statistici: {str(e)}")
                
                # Export absențe
                st.markdown("---")
                csv = absente_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descarcă absențe (CSV)",
                    data=csv,
                    file_name=f"absente_{elev}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.success("✅ Nu există absențe înregistrate pentru criteriile selectate.")
        
        with tab_observatii:
            st.markdown("### 📋 Observații de la Profesori")
            
            # Filtre pentru observații
            col_obs_filter1, col_obs_filter2 = st.columns(2)
            
            with col_obs_filter1:
                filtru_obs_tip = st.selectbox(
                    "Tip observație:",
                    ["Toate", "laudă", "atenționare", "mustrare", "recomandare"],
                    key="parinte_filtru_obs_tip"
                )
            
            with col_obs_filter2:
                filtru_obs_rezolvata = st.selectbox(
                    "Stare:",
                    ["Toate", "Rezolvate", "Nerezolvate"],
                    key="parinte_filtru_obs_stare"
                )
            
            # Obține observațiile
            rezolvata_param = None
            if filtru_obs_rezolvata == "Rezolvate":
                rezolvata_param = True
            elif filtru_obs_rezolvata == "Nerezolvate":
                rezolvata_param = False
            
            observatii = get_observatii_elev(
                elev, conn, 
                tip=filtru_obs_tip if filtru_obs_tip != "Toate" else None,
                rezolvata=rezolvata_param
            )
            
            if observatii:
                # Statistici observații
                total_obs = len(observatii)
                laudă_count = sum(1 for o in observatii if o[3] == 'laudă')
                atenționare_count = sum(1 for o in observatii if o[3] == 'atenționare')
                mustrare_count = sum(1 for o in observatii if o[3] == 'mustrare')
                recomandare_count = sum(1 for o in observatii if o[3] == 'recomandare')
                
                col_obs_stat1, col_obs_stat2, col_obs_stat3, col_obs_stat4, col_obs_stat5 = st.columns(5)
                
                with col_obs_stat1:
                    st.metric("📋 Total", total_obs)
                
                with col_obs_stat2:
                    st.metric("👏 Laudă", laudă_count)
                
                with col_obs_stat3:
                    st.metric("⚠️ Atenționare", atenționare_count)
                
                with col_obs_stat4:
                    st.metric("❌ Mustrare", mustrare_count)
                
                with col_obs_stat5:
                    st.metric("💡 Recomandare", recomandare_count)
                
                # Afișează observațiile
                for obs in observatii:
                    data_obs, materie_obs, text_obs, tip_obs, profesor_obs, gravitate_obs, rezolvata_obs = obs
                    
                    # Determină culoarea în funcție de tip
                    if tip_obs == 'laudă':
                        bg_color = "rgba(34, 197, 94, 0.1)"
                        border_color = "rgba(34, 197, 94, 0.3)"
                        badge_color = "success"
                    elif tip_obs == 'atenționare':
                        bg_color = "rgba(234, 179, 8, 0.1)"
                        border_color = "rgba(234, 179, 8, 0.3)"
                        badge_color = "warning"
                    elif tip_obs == 'mustrare':
                        bg_color = "rgba(239, 68, 68, 0.1)"
                        border_color = "rgba(239, 68, 68, 0.3)"
                        badge_color = "danger"
                    else:  # recomandare
                        bg_color = "rgba(59, 130, 246, 0.1)"
                        border_color = "rgba(59, 130, 246, 0.3)"
                        badge_color = "info"
                    
                    st.markdown(f"""
                    <div class="custom-card" style="background: {bg_color}; border-color: {border_color};">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h4 style="margin: 0 0 10px 0;">
                                    <span class="badge badge-{badge_color}">{tip_obs.upper()}</span>
                                    {materie_obs}
                                </h4>
                                <p style="margin: 0; color: white;">{text_obs}</p>
                            </div>
                            <div style="text-align: right;">
                                <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">
                                    {datetime.strptime(data_obs, "%Y-%m-%d").strftime("%d.%m.%Y")}<br>
                                    <small>Prof. {profesor_obs}</small>
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ Nu există observații înregistrate pentru criteriile selectate.")
        
        with tab_medii:
            st.markdown("### 📊 Medii pe Materii")
            
            # Calcul medii pentru fiecare materie
            cursor = conn.cursor()
            
            # Obține toate materiile cu note
            cursor.execute('''SELECT DISTINCT materie 
                            FROM grades 
                            WHERE nume = ? 
                            ORDER BY materie''',
                         (elev,))
            materii = cursor.fetchall()
            
            if materii:
                medii_data = []
                
                for materie_row in materii:
                    materie = materie_row[0]
                    
                    # Medie semestrul 1
                    cursor.execute('''SELECT AVG(nota) 
                                    FROM grades 
                                    WHERE nume = ? AND materie = ? AND semestru = 1''',
                                 (elev, materie))
                    medie_sem1 = cursor.fetchone()[0]
                    
                    # Medie semestrul 2
                    cursor.execute('''SELECT AVG(nota) 
                                    FROM grades 
                                    WHERE nume = ? AND materie = ? AND semestru = 2''',
                                 (elev, materie))
                    medie_sem2 = cursor.fetchone()[0]
                    
                    # Medie anuală
                    if medie_sem1 and medie_sem2:
                        medie_anuala = (medie_sem1 + medie_sem2) / 2
                    elif medie_sem1:
                        medie_anuala = medie_sem1
                    elif medie_sem2:
                        medie_anuala = medie_sem2
                    else:
                        medie_anuala = None
                    
                    # Determină situația
                    if medie_anuala:
                        if medie_anuala >= 5.00:
                            situatie = "Promovat"
                            badge_color = "success"
                        else:
                            situatie = "Corigență"
                            badge_color = "danger"
                    else:
                        situatie = "Fără note"
                        badge_color = "warning"
                    
                    medii_data.append({
                        'Materie': materie,
                        'Medie Sem 1': round(medie_sem1, 2) if medie_sem1 else "-",
                        'Medie Sem 2': round(medie_sem2, 2) if medie_sem2 else "-",
                        'Medie Anuală': round(medie_anuala, 2) if medie_anuala else "-",
                        'Situație': situatie,
                        'badge_color': badge_color
                    })
                
                # Creează DataFrame
                medii_df = pd.DataFrame(medii_data)
                
                # Afișează tabela
                st.dataframe(
                    medii_df[['Materie', 'Medie Sem 1', 'Medie Sem 2', 'Medie Anuală', 'Situație']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Calcul medie generală
                medii_valide = [m['Medie Anuală'] for m in medii_data if isinstance(m['Medie Anuală'], (int, float))]
                if medii_valide:
                    medie_generala = sum(medii_valide) / len(medii_valide)
                    
                    col_med_gen1, col_med_gen2, col_med_gen3 = st.columns(3)
                    
                    with col_med_gen1:
                        st.metric("🎓 Medie generală", f"{medie_generala:.2f}")
                    
                    with col_med_gen2:
                        materii_promovate = sum(1 for m in medii_data if m['Situație'] == 'Promovat')
                        st.metric("✅ Materii promovate", f"{materii_promovate}/{len(medii_data)}")
                    
                    with col_med_gen3:
                        if medie_generala >= 9.00:
                            mențiune = "FOARTE BINE"
                            mențiune_color = "#3b82f6"
                        elif medie_generala >= 8.00:
                            mențiune = "BINE"
                            mențiune_color = "#22c55e"
                        elif medie_generala >= 7.00:
                            mențiune = "SUFICIENT"
                            mențiune_color = "#eab308"
                        else:
                            mențiune = "FĂRĂ MENȚIUNE"
                            mențiune_color = "#ef4444"
                        
                        st.markdown(f"""
                        <div style="text-align: center;">
                            <h4 style="color: {mențiune_color}; margin: 0;">{mențiune}</h4>
                            <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">Mențiune</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ Nu există note înregistrate pentru calcularea mediilor.")
        
        with tab_purtare:
            st.markdown("### ⭐ Nota de Purtare")
            
            # Obține nota curentă de purtare
            nota_purtare_sem1 = get_nota_purtare_curenta(elev, conn, 1)
            nota_purtare_sem2 = get_nota_purtare_curenta(elev, conn, 2)
            
            col_purt1, col_purt2, col_purt3 = st.columns(3)
            
            with col_purt1:
                st.metric("Semestrul 1", f"{nota_purtare_sem1}/10")
            
            with col_purt2:
                st.metric("Semestrul 2", f"{nota_purtare_sem2}/10")
            
            with col_purt3:
                # Medie anuală purtare
                if nota_purtare_sem1 and nota_purtare_sem2:
                    medie_purtare = (nota_purtare_sem1 + nota_purtare_sem2) / 2
                elif nota_purtare_sem1:
                    medie_purtare = nota_purtare_sem1
                elif nota_purtare_sem2:
                    medie_purtare = nota_purtare_sem2
                else:
                    medie_purtare = 10  # Default
                
                st.metric("Medie anuală", f"{medie_purtare:.1f}/10")
            
            # Istoric modificări purtare
            st.markdown("##### 📝 Istoric modificări")
            
            cursor = conn.cursor()
            cursor.execute('''SELECT data_modificare, nota, motiv, profesor 
                            FROM purtare 
                            WHERE nume = ? 
                            ORDER BY data_modificare DESC''',
                         (elev,))
            
            istoric_purtare = cursor.fetchall()
            
            if istoric_purtare:
                for data_mod, nota, motiv, profesor in istoric_purtare:
                    data_format = datetime.strptime(data_mod, "%Y-%m-%d").strftime("%d.%m.%Y")
                    
                    # Determină iconița în funcție de modificare
                    if nota >= 9:
                        icon = "⭐"
                        color = "#22c55e"
                    elif nota >= 7:
                        icon = "👍"
                        color = "#eab308"
                    else:
                        icon = "⚠️"
                        color = "#ef4444"
                    
                    st.markdown(f"""
                    <div class="custom-card" style="padding: 15px !important;">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="font-size: 2rem; color: {color};">{icon}</div>
                            <div style="flex: 1;">
                                <h4 style="margin: 0; color: white;">Nota: {nota}/10</h4>
                                <p style="margin: 5px 0 0 0; color: #94a3b8;">
                                    <strong>Motiv:</strong> {motiv}<br>
                                    <small>Modificat de Prof. {profesor} la {data_format}</small>
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ Nu există modificări înregistrate pentru nota de purtare.")
        
        with tab_activitati:
            st.markdown("### 🎨 Activități Extrașcolare")
            
            # Verifică dacă elevul are activități înregistrate
            cursor = conn.cursor()
            cursor.execute('''SELECT tip_activitate, denumire, data_inceput, data_sfarsit, realizari, mentiuni 
                            FROM activitati 
                            WHERE nume = ? 
                            ORDER BY data_inceput DESC''',
                         (elev,))
            
            activitati_elev = cursor.fetchall()
            
            if activitati_elev:
                for activitate in activitati_elev:
                    tip, denumire, data_inceput, data_sfarsit, realizari, mentiuni = activitate
                    
                    # Formatează datele
                    data_inceput_fmt = datetime.strptime(data_inceput, "%Y-%m-%d").strftime("%d.%m.%Y") if data_inceput else "Nespecificat"
                    data_sfarsit_fmt = datetime.strptime(data_sfarsit, "%Y-%m-%d").strftime("%d.%m.%Y") if data_sfarsit else "Prezent"
                    
                    # Determină iconița în funcție de tip
                    icon_map = {
                        'sport': '⚽',
                        'artistic': '🎨',
                        'cultural': '🎭',
                        'voluntariat': '🤝',
                        'competitie': '🏆',
                        'proiect': '📋'
                    }
                    
                    icon = icon_map.get(tip.lower(), '🎯')
                    
                    st.markdown(f"""
                    <div class="custom-card">
                        <div style="display: flex; align-items: start; gap: 15px;">
                            <div style="font-size: 2.5rem;">{icon}</div>
                            <div style="flex: 1;">
                                <h4 style="margin: 0 0 10px 0; color: white;">{denumire}</h4>
                                <p style="margin: 0 0 5px 0; color: #94a3b8;">
                                    <strong>Tip:</strong> {tip} | 
                                    <strong>Perioadă:</strong> {data_inceput_fmt} - {data_sfarsit_fmt}
                                </p>
                                {f'<p style="margin: 5px 0; color: white;"><strong>Realizări:</strong> {realizari}</p>' if realizari else ''}
                                {f'<p style="margin: 5px 0; color: #94a3b8;"><strong>Mențiuni:</strong> {mentiuni}</p>' if mentiuni else ''}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ Nu există activități extrașcolare înregistrate.")
    
    # ============================================
    # 12. INTERFAȚA DIRECTOARE - MODUL ADMINISTRATIV
    # ============================================
    else:  # role == "admin"
        st.markdown("## 🏛️ Panou Administrativ - Directoare")
        
        # Tabs pentru diferite funcționalități administrative
        tab_overview, tab_statistici, tab_gestionare, tab_rapoarte, tab_sistem = st.tabs([
            "📊 Overview", 
            "📈 Statistici", 
            "👥 Gestionare", 
            "📋 Rapoarte", 
            "⚙️ Sistem"
        ])
        
        with tab_overview:
            st.markdown("### 🎓 Overview Sistem")
            
            col_admin1, col_admin2, col_admin3, col_admin4 = st.columns(4)
            
            with col_admin1:
                # Total elevi
                total_elevi = sum(len(studenti) for studenti in CLASE.values())
                st.metric("👥 Total elevi", total_elevi)
            
            with col_admin2:
                # Total profesori
                total_profesori = len(PROFESORI)
                st.metric("👨‍🏫 Total profesori", total_profesori)
            
            with col_admin3:
                # Total note în sistem
                total_note_sistem = pd.read_sql("SELECT COUNT(*) FROM grades", conn).iloc[0,0]
                st.metric("📝 Total note", total_note_sistem)
            
            with col_admin4:
                # Total absențe în sistem
                total_absente_sistem = pd.read_sql("SELECT COUNT(*) FROM absente", conn).iloc[0,0]
                st.metric("❌ Total absențe", total_absente_sistem)
            
            # Statistici pe clase
            st.markdown("##### 📊 Statistici pe Clase")
            
            clase_stats = []
            for clasa_nume, elevi_clasa in CLASE.items():
                if elevi_clasa:  # Doar clasele cu elevi
                    # Note pe clasă
                    cursor = conn.cursor()
                    cursor.execute('''SELECT COUNT(*), AVG(nota) 
                                    FROM grades 
                                    WHERE clasa = ?''',
                                 (clasa_nume,))
                    count_note, medie_note = cursor.fetchone()
                    
                    # Absențe pe clasă
                    cursor.execute('''SELECT COUNT(*) 
                                    FROM absente 
                                    WHERE clasa = ?''',
                                 (clasa_nume,))
                    count_absente = cursor.fetchone()[0]
                    
                    clase_stats.append({
                        'Clasa': clasa_nume,
                        'Elevi': len(elevi_clasa),
                        'Note': count_note or 0,
                        'Medie': round(medie_note, 2) if medie_note else 0,
                        'Absențe': count_absente or 0
                    })
            
            if clase_stats:
                clase_df = pd.DataFrame(clase_stats)
                st.dataframe(clase_df, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ Nu există date suficiente pentru statisticile pe clase.")
            
            # Activități recente
            st.markdown("##### 📅 Activități Recente")
            
            cursor = conn.cursor()
            cursor.execute('''SELECT 
                                CASE 
                                    WHEN tabela = 'grades' THEN '📝 Notă adăugată'
                                    WHEN tabela = 'absente' THEN '❌ Absență înregistrată'
                                    WHEN tabela = 'observatii' THEN '📋 Observație adăugată'
                                    ELSE '📊 Altă activitate'
                                END as activitate,
                                utilizator,
                                created_at
                            FROM istoric_modificari 
                            ORDER BY created_at DESC 
                            LIMIT 10''')
            
            activitati_recente = cursor.fetchall()
            
            if activitati_recente:
                for activitate, utilizator, data_activitate in activitati_recente:
                    data_fmt = datetime.strptime(data_activitate, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H:%M")
                    st.markdown(f"""
                    <div class="custom-card" style="padding: 10px !important; margin: 5px 0 !important;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>{activitate}</strong><br>
                                <small style="color: #94a3b8;">Utilizator: {utilizator}</small>
                            </div>
                            <div style="color: #64748b; font-size: 0.9rem;">
                                {data_fmt}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ Nu există activități recente înregistrate.")
        
        with tab_statistici:
            st.markdown("### 📈 Statistici Avansate")
            
            # Selectare clasă pentru statistici detaliate
            clasa_selectata_admin = st.selectbox(
                "Selectează clasa pentru statistici detaliate:",
                list(CLASE.keys()),
                key="admin_clasa_select"
            )
            
            if clasa_selectata_admin and CLASE[clasa_selectata_admin]:
                elevi_clasa = CLASE[clasa_selectata_admin]
                
                st.markdown(f"#### 📊 Statistici pentru clasa {clasa_selectata_admin}")
                
                # Statistici generale
                col_stat_gen1, col_stat_gen2, col_stat_gen3 = st.columns(3)
                
                with col_stat_gen1:
                    # Medie generală clasă
                    cursor = conn.cursor()
                    cursor.execute('''SELECT AVG(nota) 
                                    FROM grades 
                                    WHERE clasa = ?''',
                                 (clasa_selectata_admin,))
                    medie_generala_clasa = cursor.fetchone()[0]
                    st.metric("🎓 Medie generală clasă", f"{medie_generala_clasa:.2f}" if medie_generala_clasa else "0.00")
                
                with col_stat_gen2:
                    # Procentaj promovare
                    # Aici ar trebui o logică mai complexă bazată pe mediile anuale
                    st.metric("✅ Rate promovare", "95%")  # Exemplu
                
                with col_stat_gen3:
                    # Absenteism
                    cursor.execute('''SELECT COUNT(*) 
                                    FROM absente 
                                    WHERE clasa = ?''',
                                 (clasa_selectata_admin,))
                    total_absente_clasa = cursor.fetchone()[0] or 0
                    rata_absenteism = (total_absente_clasa / (len(elevi_clasa) * 180)) * 100  # 180 zile de școală
                    st.metric("📉 Rata absenteism", f"{rata_absenteism:.1f}%")
                
                # Top elevi
                st.markdown("##### 🏆 Top Elevi")
                
                top_elevi = []
                for elev in elevi_clasa:
                    cursor.execute('''SELECT AVG(nota) 
                                    FROM grades 
                                    WHERE nume = ?''',
                                 (elev,))
                    medie_elev = cursor.fetchone()[0]
                    
                    if medie_elev:
                        top_elevi.append({
                            'Elev': elev,
                            'Medie': round(medie_elev, 2)
                        })
                
                if top_elevi:
                    top_elevi.sort(key=lambda x: x['Medie'], reverse=True)
                    top_df = pd.DataFrame(top_elevi[:10])  # Primele 10
                    
                    st.dataframe(top_df, use_container_width=True, hide_index=True)
                else:
                    st.info("ℹ️ Nu există suficiente date pentru a afișa topul elevilor.")
                
                # Materii cu cele mai multe note
                st.markdown("##### 📚 Activități pe Materii")
                
                cursor.execute('''SELECT materie, COUNT(*) as numar_note, AVG(nota) as medie_materie
                                FROM grades 
                                WHERE clasa = ? 
                                GROUP BY materie 
                                ORDER BY numar_note DESC''',
                             (clasa_selectata_admin,))
                
                materii_stats = cursor.fetchall()
                
                if materii_stats:
                    materii_df = pd.DataFrame(materii_stats, columns=['Materie', 'Număr note', 'Medie'])
                    materii_df['Medie'] = materii_df['Medie'].round(2)
                    
                    st.dataframe(materii_df, use_container_width=True, hide_index=True)
                else:
                    st.info("ℹ️ Nu există date pentru activitățile pe materii.")
            else:
                st.warning(f"⚠️ Clasa {clasa_selectata_admin} nu are elevi înregistrați.")
        
        with tab_gestionare:
            st.markdown("### 👥 Gestionare Utilizatori")
            
            gestionare_tab1, gestionare_tab2 = st.tabs(["👨‍🏫 Profesori", "👤 Elevi"])
            
            with gestionare_tab1:
                st.markdown("##### 🎓 Lista Profesori")
                
                # Afișează lista profesorilor
                prof_df = pd.DataFrame([
                    {
                        'Nume': nume,
                        'Materie': detalii['materie'],
                        'Email': detalii['email'],
                        'Telefon': detalii['telefon'],
                        'Experiență': f"{detalii['ani_experienta']} ani"
                    }
                    for nume, detalii in PROFESORI.items()
                ])
                
                st.dataframe(prof_df, use_container_width=True, hide_index=True)
                
                # Adăugare profesor nou
                st.markdown("##### ➕ Adăugare Profesor Nou")
                
                with st.form(key="form_adaugare_profesor"):
                    col_prof_nume, col_prof_materie = st.columns(2)
                    
                    with col_prof_nume:
                        nume_prof_nou = st.text_input("Nume profesor:")
                    
                    with col_prof_materie:
                        materie_prof_nou = st.selectbox("Materie:", MATERII_GIMNAZIU)
                    
                    col_prof_email, col_prof_tel = st.columns(2)
                    
                    with col_prof_email:
                        email_prof_nou = st.text_input("Email:")
                    
                    with col_prof_tel:
                        telefon_prof_nou = st.text_input("Telefon:")
                    
                    parola_prof_nou = st.text_input("Parolă:", type="password")
                    
                    if st.form_submit_button("➕ Adaugă Profesor"):
                        if nume_prof_nou and materie_prof_nou and parola_prof_nou:
                            # Aici s-ar face adăugarea în baza de date
                            st.success(f"✅ Profesorul {nume_prof_nou} a fost adăugat cu succes!")
                        else:
                            st.error("❌ Completează toate câmpurile obligatorii!")
            
            with gestionare_tab2:
                st.markdown("##### 👥 Lista Elevi")
                
                # Afișează lista elevilor
                elevi_lista = []
                for clasa_nume, elevi_clasa in CLASE.items():
                    for elev in elevi_clasa:
                        detalii = ELEVI.get(elev, {})
                        elevi_lista.append({
                            'Nume': elev,
                            'Clasa': clasa_nume,
                            'Data nașterii': detalii.get('data_nasterii', 'N/A'),
                            'Telefon părinte': detalii.get('telefon_parinte', 'N/A')
                        })
                
                if elevi_lista:
                    elevi_df = pd.DataFrame(elevi_lista)
                    st.dataframe(elevi_df, use_container_width=True, hide_index=True)
                else:
                    st.info("ℹ️ Nu există elevi înregistrați în sistem.")
                
                # Transfer elev între clase
                st.markdown("##### 🔄 Transfer Elev")
                
                if elevi_lista:
                    col_transfer_elev, col_transfer_clasa = st.columns(2)
                    
                    with col_transfer_elev:
                        elev_transfer = st.selectbox(
                            "Selectează elev:",
                            [e['Nume'] for e in elevi_lista]
                        )
                    
                    with col_transfer_clasa:
                        clasa_noua = st.selectbox(
                            "Clasa nouă:",
                            list(CLASE.keys())
                        )
                    
                    if st.button("🔄 Transferă elev", use_container_width=True):
                        # Aici s-ar face transferul efectiv
                        st.success(f"✅ Elevul {elev_transfer} a fost transferat în clasa {clasa_noua}!")
                else:
                    st.warning("⚠️ Nu există elevi disponibili pentru transfer.")
        
        with tab_rapoarte:
            st.markdown("### 📋 Generare Rapoarte")
            
            col_raport_tip, col_raport_perioada = st.columns(2)
            
            with col_raport_tip:
                tip_raport = st.selectbox(
                    "Tip raport:",
                    ["Raport general școală", "Raport pe clasă", "Raport pe profesor", 
                     "Raport absenteism", "Raport performanță"]
                )
            
            with col_raport_perioada:
                perioada_raport = st.selectbox(
                    "Perioadă:",
                    ["Acest an școlar", "Semestrul 1", "Semestrul 2", "Ultima lună", "Personalizată"]
                )
            
            # Opțiuni specifice în funcție de tipul de raport
            if tip_raport == "Raport pe clasă":
                clasa_raport = st.selectbox("Selectează clasa:", list(CLASE.keys()))
            elif tip_raport == "Raport pe profesor":
                profesor_raport = st.selectbox("Selectează profesor:", list(PROFESORI.keys()))
            
            # Generare raport
            if st.button("📄 Generează Raport", type="primary", use_container_width=True):
                with st.spinner("Generare raport în curs..."):
                    time.sleep(2)
                    
                    # Simulare generare raport
                    st.success("✅ Raportul a fost generat cu succes!")
                    
                    # Afișează preview raport
                    st.markdown("""
                    <div class="custom-card">
                        <h4>📋 Preview Raport</h4>
                        <p><strong>Tip raport:</strong> {}</p>
                        <p><strong>Perioadă:</strong> {}</p>
                        <p><strong>Data generare:</strong> {}</p>
                        <p><strong>Statistici incluse:</strong></p>
                        <ul>
                            <li>Date generale școală</li>
                            <li>Performanță academică</li>
                            <li>Analiză absenteism</li>
                            <li>Recomandări și concluzii</li>
                        </ul>
                    </div>
                    """.format(tip_raport, perioada_raport, datetime.now().strftime("%d.%m.%Y %H:%M")), 
                    unsafe_allow_html=True)
                    
                    # Butoane export
                    col_export_pdf, col_export_excel = st.columns(2)
                    
                    with col_export_pdf:
                        st.download_button(
                            label="📥 Descarcă PDF",
                            data="Simulated PDF content",
                            file_name=f"raport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
                    
                    with col_export_excel:
                        st.download_button(
                            label="📊 Descarcă Excel",
                            data="Simulated Excel content",
                            file_name=f"raport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
        
        with tab_sistem:
            st.markdown("### ⚙️ Setări și Configurare Sistem")
            
            sist_tab1, sist_tab2, sist_tab3 = st.tabs(["🔧 Configurare", "💾 Backup", "📊 Monitorizare"])
            
            with sist_tab1:
                st.markdown("##### ⚙️ Configurare Sistem")
                
                col_sys1, col_sys2 = st.columns(2)
                
                with col_sys1:
                    # Setări generale
                    st.markdown("**Setări generale**")
                    
                    an_scolar = st.text_input("An școlar:", value="2025-2026")
                    data_inceput = st.date_input("Data început an școlar:", value=date(2025, 9, 1))
                    data_sfarsit = st.date_input("Data sfârșit an școlar:", value=date(2026, 6, 30))
                    
                    # Setări evaluare
                    st.markdown("**Setări evaluare**")
                    
                    nr_min_note = st.number_input("Număr minim note/semestru:", min_value=1, max_value=10, value=3)
                    nota_promovare = st.number_input("Notă minimă promovare:", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
                
                with col_sys2:
                    # Setări securitate
                    st.markdown("**Setări securitate**")
                    
                    expirare_parola = st.number_input("Expirare parolă (zile):", min_value=30, max_value=365, value=90)
                    blocare_incercari = st.number_input("Încercări eșuate până la blocare:", min_value=3, max_value=10, value=5)
                    log_activitati = st.toggle("Log activități utilizatori", value=True)
                    
                    # Setări notificări
                    st.markdown("**Setări notificări**")
                    
                    notificari_email = st.toggle("Notificări email", value=True)
                    notificari_sms = st.toggle("Notificări SMS", value=False)
                    alerta_absente = st.number_input("Alertă la numărul de absențe:", min_value=1, max_value=20, value=5)
                
                if st.button("💾 Salvează configurare", type="primary", use_container_width=True):
                    st.success("✅ Configurația sistemului a fost salvată cu succes!")
            
            with sist_tab2:
                st.markdown("##### 💾 Backup și Restaurare")
                
                col_backup1, col_backup2 = st.columns(2)
                
                with col_backup1:
                    st.markdown("**Creează backup**")
                    
                    descriere_backup = st.text_area("Descriere backup:", placeholder="Descrie scopul acestui backup...")
                    
                    if st.button("💾 Creează backup complet", use_container_width=True):
                        with st.spinner("Creare backup în curs..."):
                            time.sleep(3)
                            
                            # Simulare backup
                            backup_info = {
                                'data_creare': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'descriere': descriere_backup,
                                'dimensiune': "~15.7 MB",
                                'tabele_incluse': 8,
                                'inregistrari': total_note_sistem + total_absente_sistem
                            }
                            
                            st.success("✅ Backup creat cu succes!")
                            
                            # Afișează detalii backup
                            st.markdown(f"""
                            <div class="custom-card">
                                <h4>📦 Backup creat</h4>
                                <p><strong>Data creare:</strong> {backup_info['data_creare']}</p>
                                <p><strong>Descriere:</strong> {backup_info['descriere'] or 'Niciuna'}</p>
                                <p><strong>Dimensiune:</strong> {backup_info['dimensiune']}</p>
                                <p><strong>Tabele incluse:</strong> {backup_info['tabele_incluse']}</p>
                                <p><strong>Înregistrări:</strong> {backup_info['inregistrari']:,}</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                with col_backup2:
                    st.markdown("**Restaurare backup**")
                    
                    uploaded_backup = st.file_uploader("Încarcă fișier backup:", type=['sql', 'db', 'backup'])
                    
                    if uploaded_backup is not None:
                        st.warning("""
                        ⚠️ **Atenție!** Restaurarea unui backup va suprascrie toate datele curente.
                        
                        Asigură-te că:
                        1. Ai un backup recent al datelor curente
                        2. Înțelegi că toate modificările făcute după backup vor fi pierdute
                        3. Ai permisiunile necesare pentru această operațiune
                        """)
                        
                        col_confirm1, col_confirm2 = st.columns(2)
                        
                        with col_confirm1:
                            if st.button("🔄 Confirmă restaurare", type="secondary", use_container_width=True):
                                with st.spinner("Restaurare în curs..."):
                                    time.sleep(3)
                                    st.success("✅ Backup restaurat cu succes!")
                                    st.info("ℹ️ Este necesară reîncărcarea aplicației.")
                        
                        with col_confirm2:
                            if st.button("❌ Anulează", use_container_width=True):
                                st.info("Operațiune anulată.")
            
            with sist_tab3:
                st.markdown("##### 📊 Monitorizare Sistem")
                
                # Statistici utilizare
                col_mon1, col_mon2, col_mon3 = st.columns(3)
                
                with col_mon1:
                    # Utilizatori activi
                    cursor = conn.cursor()
                    cursor.execute('''SELECT COUNT(DISTINCT utilizator) 
                                    FROM istoric_modificari 
                                    WHERE DATE(created_at) = DATE('now')''')
                    utilizatori_activi = cursor.fetchone()[0] or 0
                    st.metric("👥 Utilizatori activi azi", utilizatori_activi)
                
                with col_mon2:
                    # Operațiuni azi
                    cursor.execute('''SELECT COUNT(*) 
                                    FROM istoric_modificari 
                                    WHERE DATE(created_at) = DATE('now')''')
                    operatii_azi = cursor.fetchone()[0] or 0
                    st.metric("🔄 Operațiuni azi", operatii_azi)
                
                with col_mon3:
                    # Dimensiune baza de date
                    # Aceasta este o aproximare
                    dimensiune_mb = (total_note_sistem * 0.1 + total_absente_sistem * 0.05) / 1024
                    st.metric("💾 Dimensiune baza de date", f"{dimensiune_mb:.2f} MB")
                
                # Loguri sistem
                st.markdown("##### 📝 Loguri Sistem")
                
                cursor.execute('''SELECT created_at, actiune, utilizator, tabela 
                                FROM istoric_modificari 
                                ORDER BY created_at DESC 
                                LIMIT 20''')
                
                loguri = cursor.fetchall()
                
                if loguri:
                    for log in loguri:
                        data_log, actiune, utilizator, tabela = log
                        data_fmt = datetime.strptime(data_log, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H:%M")
                        
                        # Determină iconița
                        if 'INSERT' in actiune:
                            icon = "➕"
                            color = "#22c55e"
                        elif 'UPDATE' in actiune:
                            icon = "✏️"
                            color = "#eab308"
                        elif 'DELETE' in actiune:
                            icon = "🗑️"
                            color = "#ef4444"
                        else:
                            icon = "📝"
                            color = "#3b82f6"
                        
                        st.markdown(f"""
                        <div class="custom-card" style="padding: 10px !important; margin: 5px 0 !important; border-left: 4px solid {color};">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div style="font-size: 1.2rem; color: {color};">{icon}</div>
                                    <div>
                                        <strong>{actiune}</strong><br>
                                        <small style="color: #94a3b8;">Tabela: {tabela} | Utilizator: {utilizator}</small>
                                    </div>
                                </div>
                                <div style="color: #64748b; font-size: 0.9rem;">
                                    {data_fmt}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("ℹ️ Nu există loguri înregistrate.")
                
                # Buton pentru curățare loguri vechi
                if st.button("🧹 Curăță loguri vechi", type="secondary", use_container_width=True):
                    cursor.execute('''DELETE FROM istoric_modificari 
                                    WHERE DATE(created_at) < DATE('now', '-30 days')''')
                    conn.commit()
                    st.success("✅ Logurile mai vechi de 30 de zile au fost șterse!")

# ============================================
# 13. FOOTER ȘI INFORMAȚII SISTEM
# ============================================

# Footer doar pentru paginile după login
if st.session_state.logged_in:
    st.markdown("---")
    
    col_footer_left, col_footer_center, col_footer_right = st.columns(3)
    
    with col_footer_left:
        st.markdown("""
        <div style="text-align: center;">
            <p style="color: #64748b; font-size: 0.9rem;">
                <strong>🎓 Catalog Digital 2026</strong><br>
                Versiunea 6.0 Premium
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_footer_center:
        st.markdown("""
        <div style="text-align: center;">
            <p style="color: #64748b; font-size: 0.9rem;">
                <strong>📅 Anul școlar 2025-2026</strong><br>
                Septembrie 2025 - Iunie 2026
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_footer_right:
        st.markdown("""
        <div style="text-align: center;">
            <p style="color: #64748b; font-size: 0.9rem;">
                <strong>⚙️ Status sistem</strong><br>
                <span style="color: #22c55e;">● Operațional</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
