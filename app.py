import streamlit as st
import random
import time
import hashlib
import json
import os
from datetime import datetime, timedelta

st.set_page_config(
    page_title="ደራሽ ቢንጎ🍀",
    page_icon="🎯🍀",
    layout="wide"
)

# ===================================================================
# CUSTOM CSS FOR GREEN BACKGROUND AND LARGER CARDS
# ===================================================================

st.markdown("""
<style>
    /* Green Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #1a472a, #2d5a27, #3a7d44, #4caf50);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main content background - glass effect */
    .main-content {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Glass morphism effect */
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    }
    
    /* Motivational quotes */
    .motivation-box {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.12), rgba(255, 165, 0, 0.06));
        border-left: 4px solid #FFD700;
        padding: 12px 18px;
        border-radius: 10px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        background: rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 215, 0, 0.1);
    }
    .motivation-box .quote {
        font-size: 1rem;
        color: #FFD700;
        font-style: italic;
        font-family: 'Noto Sans Ethiopic', Arial, sans-serif;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.1);
    }
    .motivation-box .author {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.8rem;
        margin-top: 3px;
    }
    
    /* Card selection grid - USING HTML/CSS GRID */
    .cards-grid-wrapper {
        max-height: 500px;
        overflow-y: auto;
        padding: 8px;
        margin: 8px 0;
        background: rgba(0, 0, 0, 0.15);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        width: 100%;
    }
    .cards-grid-wrapper::-webkit-scrollbar {
        width: 6px;
    }
    .cards-grid-wrapper::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
    }
    .cards-grid-wrapper::-webkit-scrollbar-thumb {
        background: #FFD700;
        border-radius: 10px;
    }
    
    /* CSS Grid - 10 columns on desktop */
    .cards-grid {
        display: grid !important;
        grid-template-columns: repeat(10, 1fr) !important;
        gap: 5px !important;
        max-width: 100% !important;
        margin: 0 auto !important;
    }
    
    /* Mobile - 5 columns */
    @media (max-width: 768px) {
        .cards-grid {
            grid-template-columns: repeat(5, 1fr) !important;
            gap: 8px !important;
        }
        .cards-grid-wrapper {
            max-height: 500px !important;
        }
        .card-btn {
            font-size: 1rem !important;
            min-height: 45px !important;
            height: 45px !important;
            padding: 8px 4px !important;
            border-radius: 10px !important;
        }
    }
    
    @media (max-width: 480px) {
        .cards-grid {
            grid-template-columns: repeat(4, 1fr) !important;
            gap: 6px !important;
        }
        .cards-grid-wrapper {
            max-height: 450px !important;
        }
        .card-btn {
            font-size: 0.9rem !important;
            min-height: 40px !important;
            height: 40px !important;
            padding: 6px 3px !important;
            border-radius: 8px !important;
        }
    }
    
    @media (max-width: 360px) {
        .cards-grid {
            grid-template-columns: repeat(3, 1fr) !important;
            gap: 5px !important;
        }
        .cards-grid-wrapper {
            max-height: 400px !important;
        }
        .card-btn {
            font-size: 0.8rem !important;
            min-height: 35px !important;
            height: 35px !important;
            padding: 4px 2px !important;
            border-radius: 6px !important;
        }
    }
    
    @media (orientation: landscape) and (max-width: 900px) {
        .cards-grid {
            grid-template-columns: repeat(8, 1fr) !important;
            gap: 4px !important;
        }
        .card-btn {
            font-size: 0.8rem !important;
            min-height: 32px !important;
            height: 32px !important;
            padding: 4px 2px !important;
        }
    }
    
    @media (orientation: landscape) and (max-width: 600px) {
        .cards-grid {
            grid-template-columns: repeat(10, 1fr) !important;
            gap: 3px !important;
        }
        .card-btn {
            font-size: 0.6rem !important;
            min-height: 26px !important;
            height: 26px !important;
            padding: 2px 1px !important;
        }
    }
    
    /* Card buttons */
    .card-btn {
        width: 100% !important;
        padding: 6px 4px !important;
        font-size: 0.9rem !important;
        min-height: 40px !important;
        height: 40px !important;
        line-height: 1.2 !important;
        border-radius: 8px !important;
        margin: 0 !important;
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: bold !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
        overflow: hidden !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
        position: relative !important;
        user-select: none !important;
        -webkit-tap-highlight-color: transparent !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.4);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        font-family: Arial, sans-serif !important;
        box-sizing: border-box !important;
    }
    .card-btn:hover:not(.taken) {
        transform: scale(1.05);
        border-color: #FFD700 !important;
        background: rgba(255, 215, 0, 0.2) !important;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.2) !important;
        z-index: 10;
    }
    .card-btn:active {
        transform: scale(0.95);
    }
    .card-btn.selected {
        border-color: #FFD700 !important;
        background: rgba(255, 215, 0, 0.25) !important;
        color: #FFD700 !important;
        box-shadow: 0 0 35px rgba(255, 215, 0, 0.25) !important;
    }
    .card-btn.taken {
        border-color: rgba(255, 0, 0, 0.2) !important;
        background: rgba(255, 0, 0, 0.15) !important;
        color: rgba(255, 255, 255, 0.3) !important;
        cursor: not-allowed !important;
        opacity: 0.5 !important;
    }
    .card-btn.taken:hover {
        transform: none !important;
        border-color: rgba(255, 0, 0, 0.2) !important;
        background: rgba(255, 0, 0, 0.15) !important;
        box-shadow: none !important;
    }
    .card-btn .tick-mark {
        display: none;
    }
    .card-btn.selected .tick-mark {
        display: inline;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #FFD700, #FFA500);
        border-radius: 10px;
    }
    
    /* Text colors for green theme */
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: #FFFFFF !important;
    }
    
    .stInfo, .stSuccess, .stWarning, .stError {
        background: rgba(0, 0, 0, 0.25) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    .stInfo {
        border-left: 4px solid #2196F3 !important;
    }
    .stSuccess {
        border-left: 4px solid #4CAF50 !important;
    }
    .stWarning {
        border-left: 4px solid #FF9800 !important;
    }
    .stError {
        border-left: 4px solid #F44336 !important;
    }
    
    /* Winner celebration */
    .winner-glow {
        animation: winnerPulse 1s ease-in-out infinite alternate;
    }
    @keyframes winnerPulse {
        0% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.3); }
        100% { box-shadow: 0 0 60px rgba(255, 215, 0, 0.8); }
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1adrfps {
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Timer display */
    .header-timer-container {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 15px;
        padding: 10px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .timer-display {
        color: #FFD700 !important;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
    }
    .timer-label {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Responsive header */
    @media (max-width: 768px) {
        .main-header {
            flex-direction: column !important;
            align-items: center !important;
            text-align: center !important;
        }
        .logo-text h1 {
            font-size: 1.5rem !important;
            color: #FFFFFF !important;
        }
        .header-timer-container {
            width: 100% !important;
            max-width: 300px !important;
        }
        .timer-display {
            font-size: 1.8rem !important;
        }
    }
    
    /* Card display in game */
    .card-container {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* BINGO Board */
    .board-container {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    .board-title {
        color: #FFD700 !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.1);
    }
    .board-number {
        color: #FFFFFF !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    .board-number.called {
        background: rgba(255, 152, 0, 0.25) !important;
        color: #FFD700 !important;
        border-color: #FF9800 !important;
        box-shadow: 0 0 15px rgba(255, 152, 0, 0.15);
    }
    .board-number.last-called {
        background: rgba(229, 57, 53, 0.2) !important;
        color: #FF6B6B !important;
        border-color: #E53935 !important;
        box-shadow: 0 0 20px rgba(229, 57, 53, 0.2);
    }
    .board-stats {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    .board-stats strong {
        color: #FFD700 !important;
    }
    
    /* Called numbers */
    .called-numbers-container {
        background: rgba(0, 0, 0, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px !important;
        padding: 15px !important;
    }
    .called-numbers-header {
        color: #FFD700 !important;
    }
    .called-number {
        background: rgba(255, 215, 0, 0.15) !important;
        color: #FFD700 !important;
        border: 1px solid rgba(255, 215, 0, 0.1);
    }
    .called-number.latest {
        background: rgba(255, 215, 0, 0.3) !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
    }
    
    /* Game status */
    .game-status {
        background: rgba(0, 0, 0, 0.2) !important;
        border-left: 4px solid #FFD700 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin-top: 15px !important;
    }
    .status-message {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Game state indicator */
    .game-state-indicator {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        text-align: center !important;
        font-weight: bold !important;
    }
    .game-state-waiting { border-color: #FF9800 !important; color: #FFB74D !important; }
    .game-state-running { border-color: #4CAF50 !important; color: #81C784 !important; }
    .game-state-finished { border-color: #FFD700 !important; color: #FFD700 !important; }
    
    /* Stat boxes */
    .stat-box {
        background: rgba(0, 0, 0, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
    }
    .stat-value {
        color: #FFD700 !important;
        font-weight: bold !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.1);
    }
    .stat-label {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #1a1a2e !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3) !important;
    }
    
    /* Sidebar user info */
    .user-info {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    .user-details h3 {
        color: #FFFFFF !important;
    }
    .user-balance {
        color: #FFD700 !important;
    }
    
    /* Winner celebration text */
    .winner-name {
        color: #FFFFFF !important;
    }
    .winner-prize {
        color: #FFD700 !important;
    }
    
    /* Logo text */
    .logo-text h1 {
        -webkit-text-fill-color: #FFFFFF !important;
        background: none !important;
        color: #FFFFFF !important;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.1);
    }
    .logo-text p {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Selected cards preview */
    .selected-cards-preview {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 215, 0, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# [REST OF YOUR CODE - KEEP EVERYTHING THE SAME]
# ===================================================================

# ... (Keep all your existing code here including:
# - AUDIO FUNCTIONS
# - SESSION STATE INITIALIZATION
# - GAME CONSTANTS
# - MOTIVATIONAL QUOTES
# - LOCAL FILE STORAGE
# - AUTHENTICATION
# - ADMIN PANEL
# - ALL 201 BINGO CARDS
# - ENHANCED WINNER DETECTION
# - GAME FUNCTIONS
# - DISPLAY FUNCTIONS
# )

# ===================================================================
# CARD SELECTION FUNCTION - USING HTML GRID INSTEAD OF st.columns
# ===================================================================

def render_card_selection():
    """Render card selection grid using HTML/CSS grid"""
    
    remaining = st.session_state.card_selection_time
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    time_str = f"{minutes:01d}:{seconds:02d}"
    
    if remaining <= 10:
        color = "#E53935"
    elif remaining <= 30:
        color = "#FF9800"
    else:
        color = "#FFD700"
    
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:15px;flex-wrap:wrap;background:rgba(0,0,0,0.15);padding:8px 15px;border-radius:12px;border:1px solid rgba(255,255,255,0.08);">
        <span style="display:inline-block;padding:8px 20px;background:rgba(0,0,0,0.15);border-radius:8px;border:2px solid {color};font-size:1.3rem;font-weight:bold;color:{color};font-family:monospace;text-shadow:0 0 20px rgba(255,215,0,0.1);">
            ⏱️ {time_str}
        </span>
        <span style="display:inline-block;padding:6px 15px;background:linear-gradient(135deg,#2E7D32,#1B5E20);border-radius:8px;font-size:0.9rem;font-weight:bold;color:#FFD700;">
            Select Card
        </span>
        <span style="display:inline-block;padding:6px 15px;background:rgba(0,0,0,0.15);border-radius:8px;border:1px solid rgba(255,255,255,0.06);font-size:0.8rem;color:rgba(255,255,255,0.5);">
            Selected: {len(st.session_state.clicked_numbers)}/2
        </span>
        <span style="display:inline-block;padding:6px 15px;background:rgba(255,215,0,0.08);border-radius:8px;border:1px solid rgba(255,215,0,0.08);font-size:0.8rem;color:#FFD700;">
            💰 {balance} ETB
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.card_selection_time <= 10:
        st.warning(f"⚠️ Only {int(st.session_state.card_selection_time)} seconds left!")
    elif st.session_state.card_selection_time <= 30:
        st.info(f"⏱️ {int(st.session_state.card_selection_time)} seconds remaining...")
    
    # Build HTML grid with clickable cards
    html = '<div class="cards-grid-wrapper"><div class="cards-grid">'
    
    for i in range(1, 202):
        is_clicked = i in st.session_state.clicked_numbers
        is_taken = i in st.session_state.taken_cards
        
        if is_clicked:
            html += f'<div class="card-btn selected" onclick="handleCardClick({i})" style="cursor:pointer;">✓ {i}</div>'
        elif is_taken:
            html += f'<div class="card-btn taken" style="cursor:not-allowed;">{i}</div>'
        else:
            html += f'<div class="card-btn" onclick="handleCardClick({i})" style="cursor:pointer;">{i}</div>'
    
    html += '</div></div>'
    
    # Add JavaScript for card selection
    html += """
    <script>
        function handleCardClick(cardId) {
            fetch(window.location.pathname + '?toggle=' + cardId, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(function(response) {
                location.reload();
            }).catch(function() {
                location.reload();
            });
        }
    </script>
    """
    
    st.markdown(html, unsafe_allow_html=True)
    
    # Handle card selection via query params
    if 'toggle' in st.query_params:
        card_id = int(st.query_params['toggle'])
        
        if card_id in st.session_state.clicked_numbers:
            # Deselect
            st.session_state.clicked_numbers.remove(card_id)
            if card_id in st.session_state.taken_cards:
                st.session_state.taken_cards.remove(card_id)
            if st.session_state.selected_card == card_id:
                st.session_state.selected_card = None
        else:
            # Select
            if len(st.session_state.clicked_numbers) < 2 and card_id not in st.session_state.taken_cards:
                st.session_state.clicked_numbers.add(card_id)
                st.session_state.taken_cards.append(card_id)
        
        st.query_params.clear()
        st.rerun()
    
    if len(st.session_state.clicked_numbers) >= 2:
        st.success("✅ Maximum 2 cards selected! Waiting for timer...")
    else:
        st.info("👆 Click a card to select it (max 2 cards)")
    
    progress = 1 - (st.session_state.card_selection_time / 60)
    st.progress(progress)
    st.caption(f"⏱️ Auto-join in {int(st.session_state.card_selection_time)}s")

# ===================================================================
# MAIN APP
# ===================================================================

# Display motivational quote
quote = get_random_quote()
st.markdown(f"""
<div class="motivation-box">
    <div class="quote">"{quote['am']}"</div>
    <div class="author">{quote['en']} — {quote['author']}</div>
</div>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align:center;padding:10px 0;margin-bottom:10px;">
    <h1 style="font-family:'Orbitron',sans-serif;font-weight:900;font-size:2.2rem;background:linear-gradient(135deg,#FFD700,#FFA500,#FFD700);background-size:300% 300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3s ease-in-out infinite;letter-spacing:6px;margin:0;text-shadow:0 0 40px rgba(255,215,0,0.1);">
        🎯 ደራሽ ቢንጎ
    </h1>
    <p style="color:rgba(255,255,255,0.6);font-size:0.9rem;letter-spacing:3px;margin-top:-3px;">
        Derash BINGO 
    </p>
</div>
""", unsafe_allow_html=True)

# ===================================================================
# LOGIN / REGISTER
# ===================================================================

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("🎰 Login")
            if submitted:
                if username and password:
                    load_all_data()
                    success, message = login_user(username, password)
                    if success:
                        st.success(message)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(message)
    
    with tab2:
        with st.form("register_form"):
            full_name = st.text_input("👤 Full Name", placeholder="Your full name")
            username = st.text_input("👤 Username", placeholder="Choose a username")
            phone = st.text_input("📱 Phone Number", placeholder="09XXXXXXXX (for TeleBirr)")
            password = st.text_input("🔑 Password", type="password", placeholder="Create password (min 6 chars)")
            confirm = st.text_input("✅ Confirm Password", type="password", placeholder="Confirm password")
            submitted = st.form_submit_button("📝 Register")
            if submitted:
                if not full_name or not username or not password:
                    st.error("❌ Please fill all required fields")
                elif password != confirm:
                    st.error("❌ Passwords do not match")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    success, message = register_user(username, password, full_name, phone)
                    if success:
                        st.success(message)
                        st.info("💡 Your balance starts at 0 ETB. Admin can add balance.")
                        st.balloons()
                        load_all_data()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)
    st.stop()

# ===================================================================
# ADMIN PANEL
# ===================================================================

if st.session_state.current_role == "admin":
    admin_panel()
    st.markdown("---")

# ===================================================================
# USER INFO
# ===================================================================

user = st.session_state.user_db.get(st.session_state.current_user, {})
balance = user.get("balance", 0)

st.sidebar.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(255,215,0,0.08),rgba(255,165,0,0.03));padding:1rem;border-radius:12px;border:1px solid rgba(255,215,0,0.1);margin-bottom:15px;">
    <p style="margin:0;font-weight:600;color:#FFD700;">👤 {user.get('name', st.session_state.current_user)}</p>
    <p style="margin:3px 0;color:rgba(255,255,255,0.4);font-size:0.7rem;">📱 {user.get('phone', 'No phone')}</p>
    <p style="margin:5px 0;font-size:1.1rem;font-weight:bold;color:#FFD700;">💰 {balance} ETB</p>
    <p style="margin:3px 0;color:rgba(255,255,255,0.3);font-size:0.7rem;">⭐ {st.session_state.current_role.title()} | 🏆 {user.get('wins', 0)} wins</p>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout", use_container_width=True):
    logout_user()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(f"📋 Selected: {len(st.session_state.clicked_numbers)}/2 cards")

# ===================================================================
# TIMER - ALWAYS RUNNING
# ===================================================================

current_time = time.time()
time_passed = current_time - st.session_state.card_selection_last_update
st.session_state.card_selection_time = max(0, st.session_state.card_selection_time - time_passed)
st.session_state.card_selection_last_update = current_time

# When timer reaches 0, auto-select card and start game
if st.session_state.card_selection_time <= 0 and not st.session_state.game_started:
    st.session_state.card_selection_time = 60
    st.session_state.card_selection_last_update = time.time()
    
    if len(st.session_state.clicked_numbers) > 0 and st.session_state.selected_card is None:
        st.session_state.selected_card = list(st.session_state.clicked_numbers)[0]
        st.session_state.game_started = True
        st.session_state.auto_call_started = False
        st.rerun()

# ===================================================================
# AUTO-CALL NUMBERS
# ===================================================================

# Auto-call numbers every 2 seconds once game is started
if st.session_state.selected_card is not None and st.session_state.game_started:
    if not st.session_state.auto_call_started:
        st.session_state.auto_call_started = True
        st.session_state.last_call_time = time.time()
        if len(st.session_state.called_numbers) < 75:
            available = [i for i in range(1, 76) if i not in st.session_state.called_numbers]
            if available:
                called_num = random.choice(available)
                st.session_state.called_numbers.add(called_num)
                st.session_state.last_called_number = called_num
                st.session_state.auto_called_count += 1
                st.session_state.last_call_time = time.time()
                st.markdown(get_number_sound_js(called_num), unsafe_allow_html=True)
                check_for_winners()
                st.rerun()
    
    if len(st.session_state.called_numbers) < 75 and not st.session_state.winner_declared:
        current_time = time.time()
        if current_time - st.session_state.last_call_time >= 2.0:
            available = [i for i in range(1, 76) if i not in st.session_state.called_numbers]
            if available:
                called_num = random.choice(available)
                st.session_state.called_numbers.add(called_num)
                st.session_state.last_called_number = called_num
                st.session_state.auto_called_count += 1
                st.session_state.last_call_time = current_time
                st.markdown(get_number_sound_js(called_num), unsafe_allow_html=True)
                check_for_winners()
                st.rerun()

# ===================================================================
# GAME LOOP
# ===================================================================

if not st.session_state.selected_card:
    st.markdown("## 📋ካርድዎን ይምረጡ🔥🚀")
    
    # Check if we should auto-select
    if st.session_state.card_selection_time <= 0 and len(st.session_state.clicked_numbers) > 0:
        st.session_state.selected_card = list(st.session_state.clicked_numbers)[0]
        st.session_state.game_started = True
        st.session_state.auto_call_started = False
        st.rerun()
    
    render_card_selection()

# ===================================================================
# GAME PLAYING PHASE
# ===================================================================

else:
    all_player_cards = list(st.session_state.clicked_numbers)
    
    if st.session_state.winner_declared:
        total_prize = len(all_player_cards) * PRIZE_PER_CARD
        prize_per_winner = total_prize // len(st.session_state.winners_list) if st.session_state.winners_list else 0
        
        winning_pattern = ""
        if st.session_state.winners_list:
            pattern_info = st.session_state.winners_list[0].get("pattern", {})
            winning_pattern = pattern_info.get("type", "BINGO!")
        
        st.markdown(get_winner_sound_js(), unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align:center;padding:40px 20px;background:linear-gradient(135deg,rgba(255,215,0,0.08),rgba(255,165,0,0.03));border-radius:20px;border:2px solid #FFD700;margin:15px 0;box-shadow:0 0 50px rgba(255,215,0,0.1);">
            <div style="font-size:3.5rem;color:#FFD700;">🎉</div>
            <div style="font-size:2.5rem;color:#FFD700;margin:8px 0;">🎉 ቢንጎ! የጨዋታዉ አሸናፊ ሆነዋል!!!🎉</div>
            <div style="font-size:1.8rem;color:#FFD700;margin:5px 0;">🎊 እንኳን ደስ አለዎት!!!🎊</div>
            <div style="font-size:1.2rem;color:#FFFFFF;">🏆 {len(st.session_state.winners_list)} Winner(s)!</div>
            <div style="font-size:1rem;color:#4CAF50;">💰 Prize per winner: {prize_per_winner} ETB</div>
            <div style="font-size:0.9rem;color:rgba(255,255,255,0.5);">Total: {len(all_player_cards)} × {PRIZE_PER_CARD} ETB = {total_prize} ETB</div>
            <div style="font-size:1rem;color:#FFD700;margin-top:5px;">🏅 {winning_pattern}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        st.snow()
        
        st.markdown("### 📋🎉የእርስዎ ካርቴላ")
        for card_id in all_player_cards:
            is_winner = False
            winning_pattern_name = None
            for winner in st.session_state.winners_list:
                if winner.get("card_id") == card_id:
                    is_winner = True
                    pattern_info = winner.get("pattern", {})
                    winning_pattern_name = pattern_info.get("type", "BINGO!")
                    break
            display_selected_card(card_id, list(st.session_state.called_numbers), is_winner, winning_pattern_name)
        
        display_master_board()
        
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
            st.session_state.card_selection_last_update = time.time()
            st.session_state.taken_cards = []
            st.rerun()
    else:
        st.markdown(f"""
        <div style="background:rgba(46,125,50,0.1);border:1px solid rgba(255,215,0,0.05);padding:8px 15px;border-radius:10px;text-align:center;margin-bottom:15px;font-size:0.9rem;color:rgba(255,255,255,0.8);">
            🎯 Playing with {len(all_player_cards)} Card(s)
            <span style="margin-left:12px;background:rgba(255,215,0,0.08);padding:2px 10px;border-radius:12px;border:1px solid rgba(255,215,0,0.08);">
                {len(st.session_state.called_numbers)}/75 Called
            </span>
            <span style="margin-left:8px;background:rgba(255,215,0,0.08);padding:2px 10px;border-radius:12px;border:1px solid rgba(255,215,0,0.08);">
                🎯 Auto-calls: {st.session_state.auto_called_count}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        board_col, cards_col = st.columns([2, 1])
        
        with board_col:
            display_master_board()
        
        with cards_col:
            st.markdown("### 📋 Your Cards")
            for card_id in all_player_cards:
                display_selected_card(card_id, list(st.session_state.called_numbers), False)
        
        st.info(f"🎯 Auto-calling every 2 seconds... ({len(st.session_state.called_numbers)}/75)")

# ===================================================================
# FOOTER
# ===================================================================

st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:rgba(255,255,255,0.3);font-size:0.75rem;padding:15px;border-top:1px solid rgba(255,255,255,0.05);">
    🎯 Derash BINGO | 201 Cards | Selected: {len(st.session_state.clicked_numbers)}/2 | Called: {len(st.session_state.called_numbers)}/75
</div>
""", unsafe_allow_html=True)

# Auto-rerun
if st.session_state.selected_card is not None and len(st.session_state.called_numbers) < 75 and not st.session_state.winner_declared:
    time.sleep(0.5)
    st.rerun()
elif st.session_state.selected_card is None:
    time.sleep(0.5)
    st.rerun()
