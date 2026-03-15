if st.button(T['btn_create'], type="primary", use_container_width=True):
                with st.spinner("✨ Колдуем..."):
                    try:
                        # 1. Генерируем текст сказки
                        txt = generate_story_text(cn, st.session_state.sel_lang, skills, details, st.session_state.time_val)
                        if not txt:
                            st.error("Ошибка: Текст не создан")
                            st.stop()
                            
                        ttl = txt.split('\n')[0].strip()
                        
                        # 2. Генерируем картинку, только если НЕ выбран режим "Только Аудио"
                        url = None
                        if not use_audio and use_img:
                            url = generate_image(ttl)
                        
                        # 3. ПОДГОТОВКА ДАННЫХ (БЕЗ аудио_base64 для обхода ошибки кэша)
                        clean_story = {
                            "user_email": st.session_state.user_email,
                            "child_name": cn,
                            "title": ttl,
                            "story_text": txt,
                            "image_url": url
                        }
                        
                        # ШАГ 1: Сохраняем основную запись
                        res = save_story(clean_story)
                        
                        # ШАГ 2: Если сохранение успешно, получаем ID и добавляем аудио
                        if res and hasattr(res, 'data') and len(res.data) > 0:
                            new_id = res.data[0]['id']
                            
                            if use_audio:
                                with st.spinner("🔊 Озвучиваем..."):
                                    audio_b64 = get_speech_b64(txt, voice_id)
                                    if audio_b64:
                                        # Используем новую функцию обновления из database.py
                                        update_audio(new_id, audio_b64)
                        
                        # Перезагружаем страницу, чтобы сказка появилась в списке
                        st.rerun()
                        
                    except Exception as e: 
                        st.error(f"Критическая ошибка: {e}")
