# ===================================================================
# ✅ SYNC GLOBAL STATE
# ===================================================================

sync_global_cards()
sync_global_winners()

# ===================================================================
# ✅ START THE GAME — top level, runs every tick
# ===================================================================
maybe_start_game()

# ===================================================================
# 3-SECOND CELEBRATION AUTO-RETURN
# ===================================================================

if st.session_state.winner_declared and st.session_state.celebration_start_time:
    elapsed = time.time() - st.session_state.celebration_start_time
    if elapsed >= CELEBRATION_DURATION:
        reset_for_next_round()
        st.rerun()

# ===================================================================
# GAME LOOP - ADMIN CANNOT PLAY
# ===================================================================

if st.session_state.current_role == "admin":
    st.info("🔧 Admin Mode - You can manage users and monitor the game.")
    
    if st.session_state.game_started:
        display_master_board()
        
        if st.session_state.winner_declared:
            st.markdown("""
            <div style="background:rgba(255,215,0,0.1);border:2px solid #FFD700;border-radius:15px;padding:20px;text-align:center;margin:20px 0;">
                <h3 style="color:#FFD700;">🏆 Game Finished!</h3>
                <p style="color:rgba(255,255,255,0.8);">Next round starting automatically...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.winners_list:
                st.markdown("### 🏆 Winners")
                for idx, winner in enumerate(st.session_state.winners_list, 1):
                    patterns = ", ".join(winner.get("patterns", ["BINGO!"]))
                    cards = ", ".join([f"#{c}" for c in winner.get("cards", [])])
                    st.success(f"🎉 Winner {idx}: {winner.get('username')} - Card(s): {cards} - {patterns}")
    else:
        st.info("⏳ Waiting for game to start... Players are selecting cards.")
        
        file_taken, _, _, _ = load_global_cards()
        total_selected = max(len(file_taken), len(st.session_state.clicked_numbers))
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.2);border:1px solid rgba(255,215,0,0.1);border-radius:12px;padding:15px;margin:10px 0;">
            <h4 style="color:#FFD700;text-align:center;">📊 Card Selection Status</h4>
            <p style="color:rgba(255,255,255,0.8);text-align:center;">
                Total Cards Selected: <strong style="color:#FFD700;">{total_selected}/204</strong>
            </p>
            <p style="color:rgba(255,255,255,0.6);text-align:center;font-size:0.9rem;">
                Need 3 cards to start the game. Currently: {total_selected}/3
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.current_user == "admin":
        if "admin" in st.session_state.user_db:
            st.session_state.user_db["admin"]["balance"] = 0.0
            save_all_data()
    
    st.stop()

# ===================================================================
# ✅ PLAYER DISPLAY — BINARY SWITCH (RENDERS BEFORE AUTO-CALL)
#    game_started == False → card selection
#    game_started == True  → BINGO board + player's own cards ONLY
# ===================================================================

if st.session_state.game_started:
    # ==============================================================
    # ✅ GAME STARTED — BINGO BOARD + PLAYER'S OWN CARDS ONLY
    # ==============================================================
    all_player_cards = list(st.session_state.clicked_numbers)
    
    if st.session_state.winner_declared:
        sync_global_winners()
        
        total_prize = len(st.session_state.taken_cards) * PRIZE_PER_CARD
        prize_per_winner = total_prize // len(st.session_state.winners_list) if st.session_state.winners_list else 0
        
        winning_patterns = []
        winner_names = []
        all_winner_cards = []
        
        for winner in st.session_state.winners_list:
            winning_patterns.extend(winner.get("patterns", []))
            winner_names.append(winner.get("username", "Unknown"))
            all_winner_cards.extend(winner.get("cards", []))
        
        winning_pattern = ", ".join(winning_patterns) if winning_patterns else "BINGO!"
        winner_names_str = ", ".join(winner_names)
        
        st.markdown(get_winner_sound_js(), unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, rgba(255,215,0,0.15), rgba(255,165,0,0.08));
                    border:3px solid #FFD700;
                    border-radius:15px;
                    padding:15px 10px;
                    margin:10px 0;
                    text-align:center;
                    box-shadow: 0 0 40px rgba(255,215,0,0.2);
                    animation: celebrationPulse 0.8s ease-in-out infinite alternate;">
            <div style="font-size:2.5rem;color:#FFD700;letter-spacing:5px;">
                🎉🎊🏆👑🎊🎉
            </div>
            <div style="font-size:1.8rem;color:#FFD700;margin:3px 0;text-shadow:0 0 30px rgba(255,215,0,0.3);">
                🎉 ቢንጎ! አሸናፊዉ ታዉቋል!!! 🎉
            </div>
            <div style="font-size:1.2rem;color:#FFD700;margin:2px 0;text-shadow:0 0 20px rgba(255,215,0,0.2);">
                🎊🍀🥳 ለቀጣይ ጨዋታ መልካም ዕድል!!! 🥳🍀🎊
            </div>
            <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin:5px 0;">
                <span style="font-size:1.8rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite;">🎉</span>
                <span style="font-size:1.8rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.2s;">🎊</span>
                <span style="font-size:1.8rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.4s;">🏆</span>
                <span style="font-size:1.8rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.6s;">👑</span>
                <span style="font-size:1.8rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.8s;">🥳</span>
                <span style="font-size:1.8rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 1s;">🎉</span>
            </div>
            <div style="font-size:1.2rem;color:#FFFFFF;margin:3px 0;">
                🏆 <span style="color:#FFD700;">{winner_names_str}</span> 🏆 
                <span style="color:rgba(255,255,255,0.5);margin:0 5px;">|</span> 
                🏆 {len(st.session_state.winners_list)} Winner(s)! 🏆
            </div>
            <div style="font-size:1.1rem;color:#4CAF50;margin:2px 0;">
                💰 Prize per winner: <strong style="color:#FFD700;">{prize_per_winner:.2f} ETB</strong>
            </div>
            <div style="font-size:1rem;color:#FFD700;margin:3px 0;text-shadow:0 0 15px rgba(255,215,0,0.2);">
                🏅 {winning_pattern}
            </div>
            <div style="font-size:1.1rem;color:#FFD700;margin:5px 0;">
                🎊🎊🎊ፈጥነው ካርቴላ ይምረጡ!!!🎊🎊🎊
            </div>
            <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin:3px 0;">
                <span style="font-size:1.5rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.1s;">👇⭐</span>
                <span style="font-size:1.5rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.3s;">🌟የዚህን ጨዋታ አሸናፊ ካርቴላ ለማየት ከታች ይመልከቱ</span>
                <span style="font-size:1.5rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.5s;">✨</span>
                <span style="font-size:1.5rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.7s;">⭐</span>
                <span style="font-size:1.5rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.9s;">🌟👇</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        st.snow()
        
        st.markdown("### 🎉🏆 የአሸናፊዎች ካርቴላ 🏆🎉")
        
        if st.session_state.winners_list:
            card_cols = st.columns(3)
            card_idx = 0
            
            all_winner_cards = []
            winner_card_patterns = {}
            
            for winner in st.session_state.winners_list:
                for card_id in winner.get("cards", []):
                    all_winner_cards.append(card_id)
                    winner_card_patterns[card_id] = ", ".join(winner.get("patterns", ["BINGO!"]))
            
            for card_id in all_winner_cards:
                with card_cols[card_idx % 3]:
                    winning_pattern_name = winner_card_patterns.get(card_id, "BINGO!")
                    display_selected_card(card_id, list(st.session_state.called_numbers), True, winning_pattern_name)
                    card_idx += 1
        
        if st.session_state.winners_list:
            st.markdown("### 🏆 አሸናፊዎች 🏆")
            for idx, winner in enumerate(st.session_state.winners_list, 1):
                patterns = ", ".join(winner.get("patterns", ["BINGO!"]))
                cards = ", ".join([f"#{c}" for c in winner.get("cards", [])])
                st.success(f"🎉 {winner.get('username')} - Card(s): {cards} - {patterns} 🎉")
        
        if st.button("🔄 New Game", use_container_width=True):
            st.session_state.selected_card = None
            st.session_state.clicked_numbers = set()
            st.session_state.called_numbers = set()
            st.session_state.last_called_number = None
            st.session_state.auto_called_count = 0
            st.session_state.game_started = False
            st.session_state.auto_call_started = False
            st.session_state.winner_declared = False
            st.session_state.game_over = False
            st.session_state.winners_list = []
            st.session_state.prize_distributed = False
            st.session_state.card_selection_time = 60
            st.session_state.timer_start_time = time.time()
            st.session_state.taken_cards = []
            st.session_state.card_owner = {}
            st.session_state.clicked_numbers = set()
            st.session_state.rejected_card_num = None
            
            clear_global_winners()
            save_global_cards([], {}, st.session_state.timer_start_time, 60)
            st.success("🔄 New game started! Select your cards for the next round.")
            time.sleep(0.5)
            st.rerun()
    else:
        # ==========================================================
        # ✅ GAME RUNNING — BINGO BOARD + PLAYER'S OWN CARDS ONLY
        # ==========================================================
        st.markdown(f"""
        <div style="background:rgba(46,125,50,0.1);border:1px solid rgba(255,215,0,0.05);padding:8px 15px;border-radius:10px;text-align:center;margin-bottom:15px;font-size:0.9rem;color:rgba(255,255,255,0.8);">
            🎯 Playing with {len(st.session_state.taken_cards)} Card(s) globally
            <span style="margin-left:12px;background:rgba(255,215,0,0.08);padding:2px 10px;border-radius:12px;border:1px solid rgba(255,215,0,0.08);">
                {len(st.session_state.called_numbers)}/75 Called
            </span>
            <span style="margin-left:8px;background:rgba(255,215,0,0.08);padding:2px 10px;border-radius:12px;border:1px solid rgba(255,215,0,0.08);">
                🎯 Auto-calls: {st.session_state.auto_called_count}
            </span>
            <span style="margin-left:8px;background:rgba(76,175,80,0.15);padding:2px 10px;border-radius:12px;border:1px solid rgba(76,175,80,0.2);color:#4CAF50;">
                ✅ Your Cards: {len(all_player_cards)}/2
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        board_col, cards_col = st.columns([2, 1])
        
        with board_col:
            display_master_board()
        
        with cards_col:
            if all_player_cards:
                st.markdown("### 📋🍀 የእርስዎ ካርቴላ/ዎች")
                for card_id in all_player_cards:
                    narrow_card_col = st.columns([1])[0]
                    with narrow_card_col:
                        display_selected_card(card_id, list(st.session_state.called_numbers), False)
            else:
                st.warning("⚠️በዚህ ዙር ጨዋታ ካርቴላ አልመረጡም!")
                st.info("💡ጨዋታዉ ተጀምሯል🍀 ካርቴላ ለመምረጥ ቀጣዩን ዙር ይጠብቁ።")
        
        st.info(f"🎯 Auto-calling every 2 seconds... ({len(st.session_state.called_numbers)}/75)")

else:
    # ==============================================================
    # ✅ GAME NOT STARTED — SHOW CARD SELECTION ONLY
    # ==============================================================
    if st.session_state.card_selection_time <= 0 and len(st.session_state.taken_cards) >= 3:
        st.session_state.game_started = True
        st.session_state.auto_call_started = False
        
        if len(st.session_state.clicked_numbers) > 0:
            st.session_state.selected_card = list(st.session_state.clicked_numbers)[0]
        else:
            st.warning("⚠️በዚህ ዙር ጨዋታ ካርቴላ አልመረጡም!")
            st.info("💡ጨዋታዉ ተጀምሯል🍀 ካርቴላ ለመምረጥ ቀጣዩን ዙር ይጠብቁ።")
            st.session_state.selected_card = -1
        
        st.rerun()
    
    if not st.session_state.game_started:
        st.markdown("## 📋 ካርድዎን ይምረጡ 🔥🚀")
        render_card_selection()

# ===================================================================
# FOOTER
# ===================================================================

st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:rgba(255,255,255,0.3);font-size:0.75rem;padding:15px;border-top:1px solid rgba(255,255,255,0.05);">
    🎯 Derash BINGO | 204 Cards | Selected: {len(st.session_state.clicked_numbers)}/2 | Called: {len(st.session_state.called_numbers)}/75
</div>
""", unsafe_allow_html=True)

# ===================================================================
# AUTO-CALL NUMBERS — MOVED TO THE END SO BOARD RENDERS FIRST
# ===================================================================

if st.session_state.game_started and not st.session_state.winner_declared:
    just_called = try_global_call()
    load_game_state()

    if just_called is not None:
        st.markdown(get_number_sound_js(just_called), unsafe_allow_html=True)

    time.sleep(0.5)
    st.rerun()

# ===================================================================
# AUTO-RERUN
# ===================================================================
if not st.session_state.game_started:
    maybe_start_game()
    time.sleep(1)
    st.rerun()
