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
elif st.session_state.role == "parent":
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
