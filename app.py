# ✅ CRITICAL GUARD — if the game should start, do it NOW before rendering the grid
if not st.session_state.game_started:
    _file_taken_check, _, _, _ = load_global_cards()
    _total_now_check = max(len(_file_taken_check), len(st.session_state.clicked_numbers))
    _remaining_check, _gs_check = get_global_remaining_time()
    if _total_now_check >= 3 and _remaining_check <= 0:
        mark_game_started_globally()
        st.session_state.game_started = True
        st.session_state.auto_call_started = False
        if len(st.session_state.clicked_numbers) > 0:
            st.session_state.selected_card = list(st.session_state.clicked_numbers)[0]
        else:
            st.session_state.selected_card = -1
        save_game_state()
        st.rerun()
        return
