# ============================================
# INTERFAȚA PROFESOR
# ============================================
if st.session_state.role == "teacher":
    st.markdown("---")
    menu_options = ["📝 Adaugă note/absente/observații", "📊 Vezi note existente", "✏️ Modifică/șterge note", "📅 Calendar anual"]
    selected_menu = st.radio("Alege acțiunea:", menu_options, horizontal=True, key="prof_menu")
    
    clasa = st.selectbox("Selectează clasa", list(CLASE.keys()), key="prof_clasa")
    if clasa != st.session_state.clasa_selectata:
        st.session_state.clasa_selectata = clasa
    
    # Funcție pentru a obține zilele selectate din st.session_state
    def get_selected_days():
        if 'selected_days' not in st.session_state:
            st.session_state.selected_days = {}
        if clasa not in st.session_state.selected_days:
            st.session_state.selected_days[clasa] = {}
        if st.session_state.materie not in st.session_state.selected_days[clasa]:
            st.session_state.selected_days[clasa][st.session_state.materie] = []
        return st.session_state.selected_days[clasa][st.session_state.materie]
    
    # Funcție pentru a adăuga/elimina o zi din lista de zile selectate
    def toggle_day_selection(day_str):
        selected_days = get_selected_days()
        if day_str in selected_days:
            selected_days.remove(day_str)
        else:
            selected_days.append(day_str)
    
    if selected_menu == "📅 Calendar anual":
        st.markdown("### 📅 Calendar anual - Selectare zile")
        
        # Selectare an și lună
        col_year, col_month = st.columns(2)
        with col_year:
            selected_year = st.selectbox("An", [2025, 2026], index=1)
        with col_month:
            months = ["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie", 
                     "Septembrie", "Octombrie", "Noiembrie", "Decembrie"]
            selected_month_name = st.selectbox("Lună", months, index=0)
        
        # Mapare nume lună -> număr
        month_map = {
            "Ianuarie": 1, "Februarie": 2, "Martie": 3, "Aprilie": 4, "Mai": 5, "Iunie": 6,
            "Septembrie": 9, "Octombrie": 10, "Noiembrie": 11, "Decembrie": 12
        }
        selected_month = month_map[selected_month_name]
        
        # Generare calendar pentru luna selectată
        import calendar
        cal = calendar.monthcalendar(selected_year, selected_month)
        
        # Afișare antet cu zilele săptămânii
        days_header = ["Lun", "Mar", "Mie", "Joi", "Vin", "Sâm", "Dum"]
        cols = st.columns(7)
        for i, day in enumerate(days_header):
            with cols[i]:
                st.markdown(f"<div style='text-align: center; font-weight: bold; padding: 5px;'>{day}</div>", 
                           unsafe_allow_html=True)
        
        # Afișare zilele lunii
        today = date.today()
        selected_days = get_selected_days()
        
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if day != 0:
                        day_date = date(selected_year, selected_month, day)
                        day_str = day_date.strftime("%Y-%m-%d")
                        
                        # Verifică dacă este ziua curentă
                        is_today = day_date == today
                        
                        # Verifică dacă este zi selectată
                        is_selected = day_str in selected_days
                        
                        # Determină culoarea de fundal
                        if is_selected:
                            bg_color = "#3b82f6"  # Albastru pentru zilele selectate
                            text_color = "white"
                            border_color = "#2563eb"
                        elif is_today:
                            bg_color = "#22c55e"  # Verde pentru ziua curentă
                            text_color = "white"
                            border_color = "#16a34a"
                        else:
                            bg_color = "#2d3748"  # Gri închis pentru alte zile
                            text_color = "white"
                            border_color = "#4a5568"
                        
                        # Afișează ziua ca buton clicabil
                        if st.button(
                            str(day),
                            key=f"cal_{selected_year}_{selected_month}_{day}",
                            help=f"Selectează/deselectează {day_date.strftime('%d.%m.%Y')}",
                            use_container_width=True
                        ):
                            toggle_day_selection(day_str)
                            st.rerun()
                        
                        # Stilizare vizuală (folosim CSS pentru aspect)
                        st.markdown(f"""
                            <style>
                            [data-testid="stButton"][key="cal_{selected_year}_{selected_month}_{day}"] > button {{
                                background-color: {bg_color} !important;
                                color: {text_color} !important;
                                border: 2px solid {border_color} !important;
                                font-weight: bold !important;
                                transition: all 0.3s !important;
                            }}
                            [data-testid="stButton"][key="cal_{selected_year}_{selected_month}_{day}"] > button:hover {{
                                transform: scale(1.05) !important;
                                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
                            }}
                            </style>
                        """, unsafe_allow_html=True)
        
        # Afișare zile selectate
        st.markdown("---")
        st.markdown("### 📋 Zile selectate pentru această materie și clasă")
        
        if selected_days:
            # Sortează zilele selectate
            selected_days_sorted = sorted(selected_days)
            
            # Afișează zilele selectate în grupuri de 5
            for i in range(0, len(selected_days_sorted), 5):
                cols = st.columns(5)
                days_chunk = selected_days_sorted[i:i+5]
                
                for j, day_str in enumerate(days_chunk):
                    if j < len(cols):
                        with cols[j]:
                            day_date = datetime.strptime(day_str, "%Y-%m-%d")
                            if st.button(
                                f"🗑️ {day_date.strftime('%d.%m')}",
                                key=f"remove_{day_str}",
                                help=f"Deselectează {day_date.strftime('%d.%m.%Y')}",
                                use_container_width=True
                            ):
                                toggle_day_selection(day_str)
                                st.rerun()
            
            # Buton pentru ștergerea tuturor zilelor selectate
            if st.button("🗑️ Șterge toate zilele selectate", type="secondary", use_container_width=True):
                st.session_state.selected_days[clasa][st.session_state.materie] = []
                st.rerun()
        else:
            st.info("Nu ai selectat nicio zi pentru această materie și clasă.")
        
        # Buton pentru a setă data curentă din selecția calendarului
        st.markdown("---")
        st.markdown("### 📅 Sincronizare cu data curentă")
        
        if selected_days:
            col_sync1, col_sync2 = st.columns(2)
            
            with col_sync1:
                day_to_use = st.selectbox(
                    "Selectează o dată pentru a o folosi ca data curentă:",
                    [datetime.strptime(d, "%Y-%m-%d").strftime("%d.%m.%Y") for d in sorted(selected_days)]
                )
            
            with col_sync2:
                st.write("")
                st.write("")
                if st.button("🎯 Setează ca data curentă", use_container_width=True):
                    selected_date_str = datetime.strptime(day_to_use, "%d.%m.%Y").strftime("%Y-%m-%d")
                    st.session_state.selected_date = selected_date_str
                    st.success(f"Data curentă setată la {day_to_use}")
                    st.rerun()
    
    else:
        # Restul codului pentru celelalte meniuri rămâne la fel
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
                <h1 style="font-size: 3rem; margin: 10px 0; color: #3b82f6;">{selected_date.strftime('%d.%m.%Y')}</h1>
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
                is_selected = day_date == selected_date
                
                # Stilul pentru ziua selectată (întotdeauna albastru)
                if is_selected:
                    col.markdown(f"""
                    <div style="text-align: center; background-color: #3b82f6; 
                                color: white; padding: 8px; border-radius: 8px; margin: 2px;
                                box-shadow: 0 4px 6px rgba(59, 130, 246, 0.4);">
                        <div style="font-size: 0.75rem;"><strong>{day_name[:3]}</strong></div>
                        <div style="font-size: 1.2rem; font-weight: bold;">{day_date.day}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Ziua curentă (verde) sau alte zile (gri închis)
                    is_today = day_date == today
                    col.markdown(f"""
                    <div style="text-align: center; background-color: {'#22c55e' if is_today else '#2d3748'}; 
                                color: white; padding: 8px; border-radius: 8px; margin: 2px;
                                cursor: pointer; transition: all 0.3s;">
                        <div style="font-size: 0.75rem;">{day_name[:3]}</div>
                        <div style="font-size: 1.1rem;">{day_date.day}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Buton pentru selectare
                if st.button("✓", key=f"quick_select_{i}", help=f"Selectează {day_date.strftime('%d.%m.%Y')}"):
                    st.session_state.selected_date = day_date.strftime("%Y-%m-%d")
                    st.rerun()
        
        # ... restul codului pentru celelalte meniuri rămâne la fel
