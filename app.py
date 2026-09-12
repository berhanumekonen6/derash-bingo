import streamlit as st
import streamlit.components.v1 as components
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
# ✅ VIEWPORT META — FORCES PROPER SCALING ON SMARTPHONES
# ===================================================================
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
""", unsafe_allow_html=True)

# ===================================================================
# CUSTOM CSS FOR GREEN BACKGROUND AND LARGER CARDS
# ===================================================================

st.markdown("""
<style>
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
    .main-content {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
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
    .cards-grid-wrapper::-webkit-scrollbar { width: 6px; }
    .cards-grid-wrapper::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); border-radius: 10px; }
    .cards-grid-wrapper::-webkit-scrollbar-thumb { background: #FFD700; border-radius: 10px; }
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
    .card-btn:active { transform: scale(0.95); }
    .card-btn.selected {
        border-color: #4CAF50 !important;
        background: rgba(76, 175, 80, 0.35) !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 35px rgba(76, 175, 80, 0.3) !important;
        border-width: 3px !important;
    }
    .card-btn.selected:hover {
        border-color: #FF6B6B !important;
        background: rgba(255, 80, 80, 0.3) !important;
        box-shadow: 0 0 35px rgba(255, 80, 80, 0.3) !important;
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
    .winner-card {
        animation: winnerCardPulse 1s ease-in-out infinite alternate !important;
        border: 3px solid #FFD700 !important;
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.25), rgba(255, 165, 0, 0.15)) !important;
        box-shadow: 0 0 50px rgba(255, 215, 0, 0.5) !important;
    }
    @keyframes winnerCardPulse {
        0% { transform: scale(1); box-shadow: 0 0 20px rgba(255, 215, 0, 0.3); }
        100% { transform: scale(1.03); box-shadow: 0 0 70px rgba(255, 215, 0, 0.7); }
    }
    @keyframes emojiFloat {
        0% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
        100% { transform: translateY(0) rotate(0deg); }
    }
    @keyframes celebrationPulse {
        0% { transform: scale(1); box-shadow: 0 0 30px rgba(255,215,0,0.2); }
        100% { transform: scale(1.01); box-shadow: 0 0 60px rgba(255,215,0,0.4); }
    }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #FFD700, #FFA500); border-radius: 10px; }
    h1, h2, h3, h4, p, label, .stMarkdown { color: #FFFFFF !important; }
    .stInfo, .stSuccess, .stWarning, .stError {
        background: rgba(0, 0, 0, 0.25) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    .stInfo { border-left: 4px solid #2196F3 !important; }
    .stSuccess { border-left: 4px solid #4CAF50 !important; }
    .stWarning { border-left: 4px solid #FF9800 !important; }
    .stError { border-left: 4px solid #F44336 !important; }
    .winner-glow { animation: winnerPulse 1s ease-in-out infinite alternate; }
    @keyframes winnerPulse {
        0% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.3); }
        100% { box-shadow: 0 0 60px rgba(255, 215, 0, 0.8); }
    }
    .css-1d391kg, .css-1adrfps {
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    .header-timer-container {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 15px;
        padding: 10px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .timer-display { color: #FFD700 !important; font-weight: bold; text-shadow: 0 0 20px rgba(255, 215, 0, 0.2); }
    .timer-label { color: rgba(255, 255, 255, 0.7) !important; }
    @media (max-width: 768px) {
        .main-header { flex-direction: column !important; align-items: center !important; text-align: center !important; }
        .logo-text h1 { font-size: 1.5rem !important; color: #FFFFFF !important; }
        .header-timer-container { width: 100% !important; max-width: 300px !important; }
        .timer-display { font-size: 1.8rem !important; }
    }
    .card-container {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    .board-container {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    .board-title { color: #FFD700 !important; text-shadow: 0 0 20px rgba(255, 215, 0, 0.1); }
    .board-number { color: #FFFFFF !important; background: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; }
    .board-number.called { background: rgba(255, 152, 0, 0.25) !important; color: #FFD700 !important; border-color: #FF9800 !important; box-shadow: 0 0 15px rgba(255, 152, 0, 0.15); }
    .board-number.last-called { background: rgba(229, 57, 53, 0.2) !important; color: #FF6B6B !important; border-color: #E53935 !important; box-shadow: 0 0 20px rgba(229, 57, 53, 0.2); }
    .board-stats { color: rgba(255, 255, 255, 0.7) !important; }
    .board-stats strong { color: #FFD700 !important; }
    .called-numbers-container { background: rgba(0, 0, 0, 0.15) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-radius: 15px !important; padding: 15px !important; }
    .called-numbers-header { color: #FFD700 !important; }
    .called-number { background: rgba(255, 215, 0, 0.15) !important; color: #FFD700 !important; border: 1px solid rgba(255, 215, 0, 0.1); }
    .called-number.latest { background: rgba(255, 215, 0, 0.3) !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.2); }
    .game-status { background: rgba(0, 0, 0, 0.2) !important; border-left: 4px solid #FFD700 !important; border-radius: 12px !important; padding: 15px !important; margin-top: 15px !important; }
    .status-message { color: rgba(255, 255, 255, 0.9) !important; }
    .game-state-indicator { background: rgba(0, 0, 0, 0.2) !important; border: 2px solid rgba(255, 255, 255, 0.1) !important; color: #FFFFFF !important; border-radius: 10px !important; padding: 10px 20px !important; text-align: center !important; font-weight: bold !important; }
    .game-state-waiting { border-color: #FF9800 !important; color: #FFB74D !important; }
    .game-state-running { border-color: #4CAF50 !important; color: #81C784 !important; }
    .game-state-finished { border-color: #FFD700 !important; color: #FFD700 !important; }
    .stat-box { background: rgba(0, 0, 0, 0.15) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-radius: 12px !important; padding: 10px 20px !important; }
    .stat-value { color: #FFD700 !important; font-weight: bold !important; text-shadow: 0 0 20px rgba(255, 215, 0, 0.1); }
    .stat-label { color: rgba(255, 255, 255, 0.6) !important; }
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
    .user-info { background: rgba(0, 0, 0, 0.2) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; }
    .user-details h3 { color: #FFFFFF !important; }
    .user-balance { color: #FFD700 !important; }
    .winner-name { color: #FFFFFF !important; }
    .winner-prize { color: #FFD700 !important; }
    .logo-text h1 { -webkit-text-fill-color: #FFFFFF !important; background: none !important; color: #FFFFFF !important; text-shadow: 0 0 30px rgba(255, 215, 0, 0.1); }
    .logo-text p { color: rgba(255, 255, 255, 0.6) !important; }
    .selected-cards-preview { background: rgba(0, 0, 0, 0.2) !important; border: 1px solid rgba(255, 215, 0, 0.15) !important; }

    @media (max-width: 768px) {
        .board-table td { padding: 3px 2px; font-size: 0.7rem; min-width: 22px; }
        .board-number { width: 26px; height: 26px; font-size: 0.7rem; }
        .board-table .header-cell { font-size: 1.1rem; padding: 6px 2px; }
        .board-container { padding: 10px !important; margin: 5px 0 !important; }
        .board-title { font-size: 1.3rem !important; }
        .motivation-box { padding: 8px 12px !important; }
        .motivation-box .quote { font-size: 0.85rem !important; }
        h1 { font-size: 1.4rem !important; letter-spacing: 3px !important; }
    }

    @media (max-width: 400px) {
        .board-number { width: 22px; height: 22px; font-size: 0.62rem; }
        .board-table td { padding: 2px 1px !important; }
        .board-table .header-cell { font-size: 0.95rem !important; padding: 4px 1px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# ✅ MOBILE GRID FIX — forces columns to stay horizontal on phones
# ===================================================================
st.markdown("""
<style>
    /* ✅ Force Streamlit columns to stay horizontal on mobile */
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            gap: 3px !important;
        }
        div[data-testid="stHorizontalBlock"] > div {
            min-width: 0 !important;
            flex: 1 1 0 !important;
            width: auto !important;
        }
        div[data-testid="stHorizontalBlock"] .stButton > button {
            padding: 4px 1px !important;
            font-size: 11px !important;
            min-height: 42px !important;
            height: 42px !important;
            line-height: 1.1 !important;
            border-radius: 6px !important;
        }
    }
    /* Compact buttons for the card grid (both mobile & desktop) */
    .stButton > button {
        padding: 6px 3px !important;
        font-size: 13px !important;
        min-height: 44px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    /* Keep card grid container tight */
    div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {
        margin-bottom: 3px !important;
    }
    /* ✅ Rejected card button — shows the "max 2 cards" message */
    .stButton > button[title="ማስጠንቀቂያ"] {
        background: linear-gradient(135deg, #E53935, #B71C1C) !important;
        color: #FFFFFF !important;
        font-size: 9px !important;
        font-weight: bold !important;
        padding: 2px !important;
        line-height: 1.05 !important;
        white-space: normal !important;
        text-align: center !important;
        border: 2px solid #FF6B6B !important;
        animation: shakeWarning 0.5s ease-in-out !important;
    }
    @keyframes shakeWarning {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-3px); }
        75% { transform: translateX(3px); }
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# AUDIO FUNCTIONS
# ===================================================================

def get_number_sound_js(number):
    if 1 <= number <= 15:
        freq = 440
    elif 16 <= number <= 30:
        freq = 523
    elif 31 <= number <= 45:
        freq = 659
    elif 46 <= number <= 60:
        freq = 784
    else:
        freq = 880
    
    return f"""
    <script>
        (function() {{
            try {{
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                oscillator.type = 'sine';
                oscillator.frequency.value = {freq};
                gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                oscillator.start(audioCtx.currentTime);
                oscillator.stop(audioCtx.currentTime + 0.3);
            }} catch(e) {{
                console.log('Audio play failed:', e);
            }}
        }})();
    </script>
    """

def get_winner_sound_js():
    return """
    <script>
        (function() {
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const notes = [523, 659, 784, 1047, 1175, 1319];
                notes.forEach((freq, index) => {
                    const oscillator = audioCtx.createOscillator();
                    const gainNode = audioCtx.createGain();
                    oscillator.type = 'sine';
                    oscillator.frequency.value = freq;
                    gainNode.gain.setValueAtTime(0.25, audioCtx.currentTime + index * 0.12);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + index * 0.12 + 0.25);
                    oscillator.connect(gainNode);
                    gainNode.connect(audioCtx.destination);
                    oscillator.start(audioCtx.currentTime + index * 0.12);
                    oscillator.stop(audioCtx.currentTime + index * 0.12 + 0.25);
                });
            } catch(e) {
                console.log('Audio play failed:', e);
            }
        })();
    </script>
    """

# ===================================================================
# SESSION STATE INITIALIZATION
# ===================================================================

def init_session_state():
    """Initialize all session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'current_role' not in st.session_state:
        st.session_state.current_role = None
    if 'clicked_numbers' not in st.session_state:
        st.session_state.clicked_numbers = set()
    if 'selected_card' not in st.session_state:
        st.session_state.selected_card = None
    if 'called_numbers' not in st.session_state:
        st.session_state.called_numbers = set()
    if 'last_called_number' not in st.session_state:
        st.session_state.last_called_number = None
    if 'auto_called_count' not in st.session_state:
        st.session_state.auto_called_count = 0
    if 'last_call_time' not in st.session_state:
        st.session_state.last_call_time = time.time()
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'auto_call_started' not in st.session_state:
        st.session_state.auto_call_started = False
    if 'card_selection_time' not in st.session_state:
        st.session_state.card_selection_time = 60
    if 'card_selection_last_update' not in st.session_state:
        st.session_state.card_selection_last_update = time.time()
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'winners_list' not in st.session_state:
        st.session_state.winners_list = []
    if 'winner_declared' not in st.session_state:
        st.session_state.winner_declared = False
    if 'user_db' not in st.session_state:
        st.session_state.user_db = {}
    if 'selected_cards' not in st.session_state:
        st.session_state.selected_cards = []
    if 'taken_cards' not in st.session_state:
        st.session_state.taken_cards = []
    if 'game_pot' not in st.session_state:
        st.session_state.game_pot = 0
    if 'prize_distributed' not in st.session_state:
        st.session_state.prize_distributed = False
    if 'all_player_cards' not in st.session_state:
        st.session_state.all_player_cards = {}
    if 'sound_played' not in st.session_state:
        st.session_state.sound_played = False
    if 'card_owner' not in st.session_state:
        st.session_state.card_owner = {}
    if 'columns_per_row' not in st.session_state:
        st.session_state.columns_per_row = 6
    if 'global_synced' not in st.session_state:
        st.session_state.global_synced = False
    if 'timer_start_time' not in st.session_state:
        st.session_state.timer_start_time = time.time()
    if 'celebration_shown' not in st.session_state:
        st.session_state.celebration_shown = False
    if 'show_insufficient_balance_msg' not in st.session_state:
        st.session_state.show_insufficient_balance_msg = False
    if 'show_max_card_msg' not in st.session_state:
        st.session_state.show_max_card_msg = False
    if 'show_card_taken_msg' not in st.session_state:
        st.session_state.show_card_taken_msg = False
    if 'show_register_success_msg' not in st.session_state:
        st.session_state.show_register_success_msg = False
    if 'show_deposit_msg' not in st.session_state:
        st.session_state.show_deposit_msg = False
    if 'deposit_msg_text' not in st.session_state:
        st.session_state.deposit_msg_text = ""
    if 'flash_msg' not in st.session_state:
        st.session_state.flash_msg = ""
    if 'celebration_start_time' not in st.session_state:
        st.session_state.celebration_start_time = None
    if 'auto_return_done' not in st.session_state:
        st.session_state.auto_return_done = False
    # ✅ NEW: Track which specific card was rejected (max 2 limit)
    if 'rejected_card_num' not in st.session_state:
        st.session_state.rejected_card_num = None

init_session_state()

# ===================================================================
# GLOBAL WINNER TRACKING
# ===================================================================

def get_global_winners_file():
    return "bingo_global_winners.json"

def save_global_winners(winners_list, winner_declared, called_numbers, last_called_number, auto_called_count, game_over, prize_distributed):
    try:
        data = {
            "winners_list": winners_list,
            "winner_declared": winner_declared,
            "called_numbers": list(called_numbers) if called_numbers else [],
            "last_called_number": last_called_number,
            "auto_called_count": auto_called_count,
            "game_over": game_over,
            "prize_distributed": prize_distributed,
            "timestamp": time.time()
        }
        with open(get_global_winners_file(), "w") as f:
            json.dump(data, f)
        return True
    except:
        return False

def load_global_winners():
    try:
        if os.path.exists(get_global_winners_file()):
            with open(get_global_winners_file(), "r") as f:
                data = json.load(f)
                return (data.get("winners_list", []),
                        data.get("winner_declared", False),
                        set(data.get("called_numbers", [])),
                        data.get("last_called_number", None),
                        data.get("auto_called_count", 0),
                        data.get("game_over", False),
                        data.get("prize_distributed", False),
                        data.get("timestamp", 0))
    except:
        pass
    return [], False, set(), None, 0, False, False, 0

def clear_global_winners():
    try:
        if os.path.exists(get_global_winners_file()):
            os.remove(get_global_winners_file())
        return True
    except:
        return False

def sync_global_winners():
    winners_list, winner_declared, called_numbers, last_called_number, auto_called_count, game_over, prize_distributed, ts = load_global_winners()
    if winner_declared:
        st.session_state.winners_list = winners_list
        st.session_state.winner_declared = winner_declared
        if called_numbers:
            st.session_state.called_numbers = called_numbers
        if last_called_number:
            st.session_state.last_called_number = last_called_number
        if auto_called_count > 0:
            st.session_state.auto_called_count = auto_called_count
        st.session_state.game_over = game_over
        st.session_state.prize_distributed = prize_distributed
        if st.session_state.celebration_start_time is None and ts > 0:
            st.session_state.celebration_start_time = ts
        return True
    return False

# ===================================================================
# GAME CONSTANTS
# ===================================================================

CARD_PRICE = 10
PRIZE_PER_CARD = 8
CELEBRATION_DURATION = 3
MAX_CARDS_PER_PLAYER = 2

# ===================================================================
# MOTIVATIONAL QUOTES
# ===================================================================

MOTIVATIONAL_QUOTES = [
    {"am": "በቢንጎ ጨዋታ እየተዝናኑ ያሸንፉ! 🎯⚡⚡", "en": "Have fun and win at BINGO!", "author": "ደራሽ ቢንጎ"},
    {"am": "አሁንኑ እድልዎን ይሞክሩ! 💪🎖️", "en": "Try your luck right now!", "author": "ደራሽ ቢንጎ"},
    {"am": "ቢንጎ! ማለት እድለኛ ማለት ነው! 🏆🎖️", "en": "BINGO! means you are lucky!", "author": "ደራሽ ቢንጎ"},
    {"am": "ያሸንፉ ይሸለሙ! 🌟🎖️🚀", "en": "Win and celebrate!", "author": "ደራሽ ቢንጎ"},
    {"am": "መልካም ዕድል ይሁንልዎ! 🍀🎖️🚀", "en": "Good luck to you!", "author": "ደራሽ ቢንጎ"},
    {"am": "ማን ያዉቃል አንድ ቁጥር ሕይወትን ይለውጣል! ✨🎖️🚀", "en": "Who knows, one number can change your life!", "author": "ደራሽ ቢንጎ"},
]

def get_random_quote():
    return random.choice(MOTIVATIONAL_QUOTES)

def get_amharic_number(num):
    amharic_numbers = {
        1: "አንድ", 2: "ሁለት", 3: "ሶስት", 4: "አራት", 5: "አምስት",
        6: "ስድስት", 7: "ሰባት", 8: "ስምንት", 9: "ዘጠኝ", 10: "አስር",
        11: "አስራ አንድ", 12: "አስራ ሁለት", 13: "አስራ ሶስት", 14: "አስራ አራት", 15: "አስራ አምስት",
        16: "አስራ ስድስት", 17: "አስራ ሰባት", 18: "አስራ ስምንት", 19: "አስራ ዘጠኝ", 20: "ሃያ",
        21: "ሃያ አንድ", 22: "ሃያ ሁለት", 23: "ሃያ ሶስት", 24: "ሃያ አራት", 25: "ሃያ አምስት",
        26: "ሃያ ስድስት", 27: "ሃያ ሰባት", 28: "ሃያ ስምንት", 29: "ሃያ ዘጠኝ", 30: "ሰላሳ",
        31: "ሰላሳ አንድ", 32: "ሰላሳ ሁለት", 33: "ሰላሳ ሶስት", 34: "ሰላሳ አራት", 35: "ሰላሳ አምስት",
        36: "ሰላሳ ስድስት", 37: "ሰላሳ ሰባት", 38: "ሰላሳ ስምንት", 39: "ሰላሳ ዘጠኝ", 40: "አርባ",
        41: "አርባ አንድ", 42: "አርባ ሁለት", 43: "አርባ ሶስት", 44: "አርባ አራት", 45: "አርባ አምስት",
        46: "አርባ ስድስት", 47: "አርባ ሰባት", 48: "አርባ ስምንት", 49: "አርባ ዘጠኝ", 50: "ሃምሳ",
        51: "ሃምሳ አንድ", 52: "ሃምሳ ሁለት", 53: "ሃምሳ ሶስት", 54: "ሃምሳ አራት", 55: "ሃምሳ አምስት",
        56: "ሃምሳ ስድስት", 57: "ሃምሳ ሰባት", 58: "ሃምሳ ስምንት", 59: "ሃምሳ ዘጠኝ", 60: "ስድሳ",
        61: "ስድሳ አንድ", 62: "ስድሳ ሁለት", 63: "ስድሳ ሶስት", 64: "ስድሳ አራት", 65: "ስድሳ አምስት",
        66: "ስድሳ ስድስት", 67: "ስድሳ ሰባት", 68: "ስድሳ ስምንት", 69: "ስድሳ ዘጠኝ", 70: "ሰባ",
        71: "ሰባ አንድ", 72: "ሰባ ሁለት", 73: "ሰባ ሶስት", 74: "ሰባ አራት", 75: "ሰባ አምስት"
    }
    return amharic_numbers.get(num, str(num))

def get_letter_for_number(num):
    if 1 <= num <= 15:
        return "ቢ"
    elif 16 <= num <= 30:
        return "አይ"
    elif 31 <= num <= 45:
        return "ኤን"
    elif 46 <= num <= 60:
        return "ጂ"
    else:
        return "ኦ"

# ===================================================================
# LOCAL FILE STORAGE
# ===================================================================

def get_local_users_file():
    return "bingo_users_local.json"

def load_local_users():
    try:
        if os.path.exists(get_local_users_file()):
            with open(get_local_users_file(), "r") as f:
                return json.load(f)
    except:
        pass
    return {}

def save_local_users(users):
    try:
        with open(get_local_users_file(), "w") as f:
            json.dump(users, f, indent=2)
        return True
    except:
        return False

def load_all_data():
    local_users = load_local_users()
    if local_users:
        st.session_state.user_db = local_users
    else:
        st.session_state.user_db = {}

def save_all_data():
    if "user_db" in st.session_state and st.session_state.user_db:
        save_local_users(st.session_state.user_db)

# ===================================================================
# GLOBAL CARD TRACKING
# ===================================================================

def get_global_cards_file():
    return "bingo_global_cards.json"

def load_global_cards():
    try:
        if os.path.exists(get_global_cards_file()):
            with open(get_global_cards_file(), "r") as f:
                data = json.load(f)
                return (data.get("taken_cards", []), 
                        data.get("card_owner", {}), 
                        data.get("timer_start_time", time.time()),
                        data.get("card_selection_time", 60))
    except:
        pass
    return [], {}, time.time(), 60

def save_global_cards(taken_cards, card_owner, timer_start_time=None, card_selection_time=None):
    try:
        data = {
            "taken_cards": taken_cards,
            "card_owner": card_owner
        }
        if timer_start_time is not None:
            data["timer_start_time"] = timer_start_time
        if card_selection_time is not None:
            data["card_selection_time"] = card_selection_time
        with open(get_global_cards_file(), "w") as f:
            json.dump(data, f)
        return True
    except:
        return False

# ===================================================================
# ✅ GLOBAL TIMER — shared across users in the same process
# ===================================================================

@st.cache_resource
def _get_shared_timer_store():
    return {
        "timer_start": time.time(),
        "duration": 60,
        "game_started": False,
    }


def get_global_timer_file():
    return "bingo_global_timer.json"


def load_global_timer():
    store = _get_shared_timer_store()
    return (store.get("timer_start", time.time()),
            store.get("duration", 60),
            store.get("game_started", False))


def save_global_timer(timer_start, duration=60, game_started=False):
    store = _get_shared_timer_store()
    store["timer_start"] = timer_start
    store["duration"] = duration
    store["game_started"] = game_started
    return True


def reset_global_timer(duration=60):
    new_start = time.time()
    save_global_timer(new_start, duration, False)
    return new_start


def mark_game_started_globally():
    timer_start, duration, _ = load_global_timer()
    save_global_timer(timer_start, duration, True)


def get_global_remaining_time():
    """Returns (remaining_seconds, game_started)."""
    timer_start, duration, game_started = load_global_timer()

    if game_started:
        return 0, True

    elapsed = time.time() - timer_start
    remaining = duration - elapsed

    if remaining <= 0:
        file_taken, _, _, _ = load_global_cards()
        total_now = max(len(file_taken), len(st.session_state.clicked_numbers))
        if total_now >= 3:
            return 0, False
        else:
            reset_global_timer(60)
            return 60, False

    return remaining, False

# ===================================================================
# ✅ GLOBAL CALLER LOCK
# ===================================================================

def get_caller_lock_file():
    return "bingo_caller_lock.json"

def load_caller_lock():
    try:
        if os.path.exists(get_caller_lock_file()):
            with open(get_caller_lock_file(), "r") as f:
                return json.load(f)
    except:
        pass
    return {"last_called_at": 0, "last_called_by": None}

def save_caller_lock(last_called_at, last_called_by):
    try:
        with open(get_caller_lock_file(), "w") as f:
            json.dump({
                "last_called_at": last_called_at,
                "last_called_by": last_called_by
            }, f)
        return True
    except:
        return False

def try_global_call():
    lock = load_caller_lock()
    now = time.time()
    last_at = lock.get("last_called_at", 0)

    if now - last_at < 2.0:
        return None

    save_caller_lock(now, st.session_state.current_user)

    load_game_state()
    current_called = set(st.session_state.called_numbers)

    if len(current_called) >= 75:
        return None

    available = [i for i in range(1, 76) if i not in current_called]
    if not available:
        return None

    called_num = random.choice(available)
    st.session_state.called_numbers.add(called_num)
    st.session_state.last_called_number = called_num
    st.session_state.auto_called_count = len(st.session_state.called_numbers)
    save_game_state()

    check_for_winners()

    return called_num

# ===================================================================
# ✅ GAME STATE
# ===================================================================

def get_game_state_file():
    return "bingo_game_state.json"

def save_game_state():
    try:
        data = {
            "called_numbers": list(st.session_state.called_numbers),
            "last_called_number": st.session_state.last_called_number,
            "auto_called_count": st.session_state.auto_called_count,
            "game_started": st.session_state.game_started,
            "auto_call_started": st.session_state.auto_call_started,
            "last_call_time": st.session_state.last_call_time,
            "winner_declared": st.session_state.winner_declared,
            "game_over": st.session_state.game_over,
            "prize_distributed": st.session_state.prize_distributed,
        }
        with open(get_game_state_file(), "w") as f:
            json.dump(data, f)
    except:
        pass

def load_game_state():
    try:
        if os.path.exists(get_game_state_file()):
            with open(get_game_state_file(), "r") as f:
                data = json.load(f)
                st.session_state.called_numbers = set(data.get("called_numbers", []))
                st.session_state.last_called_number = data.get("last_called_number")
                st.session_state.auto_called_count = data.get("auto_called_count", 0)
                st.session_state.auto_call_started = data.get("auto_call_started", False)
                st.session_state.last_call_time = data.get("last_call_time", time.time())
                st.session_state.winner_declared = data.get("winner_declared", False)
                st.session_state.game_over = data.get("game_over", False)
                st.session_state.prize_distributed = data.get("prize_distributed", False)
    except:
        pass

def clear_game_state():
    try:
        if os.path.exists(get_game_state_file()):
            os.remove(get_game_state_file())
        return True
    except:
        return False

# ===================================================================
# ✅ RESET FOR NEXT ROUND
# ===================================================================

def reset_for_next_round():
    clear_global_winners()
    clear_game_state()
    reset_global_timer(60)
    save_global_cards([], {}, time.time(), 60)
    
    try:
        if os.path.exists(get_caller_lock_file()):
            os.remove(get_caller_lock_file())
    except:
        pass
    
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
    st.session_state.celebration_start_time = None
    st.session_state.auto_return_done = False
    st.session_state.rejected_card_num = None
    
    save_game_state()

# ===================================================================
# ✅ SYNC GLOBAL CARDS + STALE-GAME RECOVERY
# ===================================================================

def sync_global_cards():
    global_taken, global_owner, _, _ = load_global_cards()
    
    st.session_state.taken_cards = list(global_taken)
    st.session_state.card_owner = dict(global_owner)
    
    remaining, game_started = get_global_remaining_time()
    st.session_state.card_selection_time = remaining
    if game_started:
        st.session_state.game_started = True
    
    load_game_state()
    
    # ✅ STALE-GAME RECOVERY — only reset on winner or all-called
    called_count = len(st.session_state.called_numbers)
    winner_done = st.session_state.winner_declared
    all_called = called_count >= 75
    
    if winner_done or all_called:
        reset_for_next_round()
        global_taken, global_owner, _, _ = load_global_cards()
        st.session_state.taken_cards = list(global_taken)
        st.session_state.card_owner = dict(global_owner)
        remaining, game_started = get_global_remaining_time()
        st.session_state.card_selection_time = remaining
        if game_started:
            st.session_state.game_started = True
    
    current_user = st.session_state.current_user
    if current_user:
        user_cards = set()
        for card_id_str, owner in global_owner.items():
            if owner == current_user:
                try:
                    user_cards.add(int(card_id_str))
                except (ValueError, TypeError):
                    pass
        st.session_state.clicked_numbers = st.session_state.clicked_numbers | user_cards

# ===================================================================
# ✅ START-THE-GAME CHECK
# ===================================================================

def maybe_start_game():
    """Start the game when BOTH conditions are true:
       1. 3+ cards selected (from file OR this user's own picks)
       2. Shared timer reached 0:00
    """
    if st.session_state.game_started:
        return

    file_taken, _, _, _ = load_global_cards()
    total_now = max(len(file_taken), len(st.session_state.clicked_numbers))
    min_required = 3

    if total_now < min_required:
        return

    remaining, _ = get_global_remaining_time()

    if remaining <= 0:
        mark_game_started_globally()
        st.session_state.game_started = True
        st.session_state.auto_call_started = False
        if len(st.session_state.clicked_numbers) > 0:
            st.session_state.selected_card = list(st.session_state.clicked_numbers)[0]
        else:
            st.session_state.selected_card = -1
        save_game_state()
        st.rerun()

# ===================================================================
# AUTHENTICATION
# ===================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    if not hashed:
        return False
    return hash_password(password) == hashed

def login_user(username, password):
    username = username.strip()
    password = password.strip()
    load_all_data()
    
    if username == "admin" and password == "admin123":
        if username not in st.session_state.user_db:
            user_data = {
                "password": hash_password("admin123"),
                "balance": 0.0,
                "role": "admin",
                "name": "Admin",
                "phone": "",
                "game_played": 0,
                "wins": 0
            }
            st.session_state.user_db[username] = user_data
            save_local_users(st.session_state.user_db)
            load_all_data()
        else:
            st.session_state.user_db["admin"]["balance"] = 0.0
            save_local_users(st.session_state.user_db)
        
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.current_role = "admin"
        load_all_data()
        sync_global_cards()
        if st.session_state.winner_declared or len(st.session_state.called_numbers) >= 75:
            reset_for_next_round()
            sync_global_cards()
        return True, "✅ Admin login successful!"
    
    if username not in st.session_state.user_db:
        return False, "❌ Username not found"
    
    if verify_password(password, st.session_state.user_db[username]["password"]):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.current_role = st.session_state.user_db[username]["role"]
        load_all_data()
        sync_global_cards()
        if st.session_state.winner_declared or len(st.session_state.called_numbers) >= 75:
            reset_for_next_round()
            sync_global_cards()
        return True, "✅ Login successful!"
    return False, "❌ Incorrect password"

def register_user(username, password, name, phone=""):
    username = username.strip()
    password = password.strip()
    name = name.strip()
    
    if len(username) < 2:
        return False, "❌ Username must be at least 2 characters"
    if len(password) < 6:
        return False, "❌ Password must be at least 6 characters"
    
    load_all_data()
    
    if username in st.session_state.user_db:
        return False, "❌ Username already exists"
    
    user_data = {
        "password": hash_password(password),
        "balance": 0.0,
        "role": "player",
        "name": name,
        "phone": phone,
        "game_played": 0,
        "wins": 0
    }
    
    st.session_state.user_db[username] = user_data
    save_local_users(st.session_state.user_db)
    load_all_data()
    
    return True, "✅ Registration successful! Your balance is 0.00 ETB"

def logout_user():
    save_all_data()
    save_game_state()
    save_global_cards(
        st.session_state.taken_cards,
        st.session_state.card_owner,
        st.session_state.timer_start_time,
        st.session_state.card_selection_time
    )
    
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_role = None
    st.session_state.global_synced = False

# ===================================================================
# ADMIN PANEL
# ===================================================================

def admin_panel():
    st.markdown("""
    <div class="glass-container">
        <h3 style="color:#FFD700;text-align:center;">🔧 Admin Panel</h3>
        <p style="color:rgba(255,255,255,0.7);text-align:center;">Manage user balances, view all users.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.show_deposit_msg:
        st.success(st.session_state.deposit_msg_text)
        st.balloons()
        st.session_state.show_deposit_msg = False
        st.session_state.deposit_msg_text = ""
    
    users = list(st.session_state.user_db.keys())
    users = [u for u in users if u != "admin"]
    
    if not users:
        st.info("No users registered yet.")
        return
    
    selected_user = st.selectbox("Select User", users)
    
    if selected_user:
        user_data = st.session_state.user_db.get(selected_user, {})
        current_balance = user_data.get("balance", 0)
        game_played = user_data.get("game_played", 0)
        wins = user_data.get("wins", 0)
        name = user_data.get("name", selected_user)
        phone = user_data.get("phone", "")
        
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(255,215,0,0.1),rgba(255,165,0,0.05));padding:1rem;border-radius:12px;border:1px solid rgba(255,215,0,0.15);margin-bottom:15px;">
            <p style="margin:0;font-weight:600;color:#FFD700;">👤 {name}</p>
            <p style="margin:5px 0;color:rgba(255,255,255,0.7);font-size:0.85rem;">📱 <strong style="color:#FFD700;">{phone if phone else 'Not provided'}</strong></p>
            <p style="margin:5px 0;color:rgba(255,255,255,0.7);font-size:0.85rem;">👤 Username: <strong style="color:#FFD700;">{selected_user}</strong></p>
            <p style="margin:5px 0;font-size:1.2rem;font-weight:bold;color:#FFD700;">💰 Current Balance: {current_balance:.2f} ETB</p>
            <p style="margin:5px 0;color:rgba(255,255,255,0.5);font-size:0.85rem;">🎮 Games Played: {game_played}</p>
            <p style="margin:5px 0;color:rgba(255,255,255,0.5);font-size:0.85rem;">🏆 Wins: {wins}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 💰 Update Balance")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            balance_options = [20, 50, 100, 200, 300, 500, 1000, 1500, 2000, 3000, 5000]
            custom_amount = st.number_input("Custom Amount (ETB)", min_value=0, step=10, value=100)
            
            st.markdown("**Quick Select Amounts:**")
            cols = st.columns(5)
            for i, amount in enumerate(balance_options):
                with cols[i % 5]:
                    if st.button(f"+{amount}", key=f"bal_{amount}_{selected_user}"):
                        if selected_user in st.session_state.user_db:
                            st.session_state.user_db[selected_user]["balance"] = st.session_state.user_db[selected_user].get("balance", 0) + amount
                            save_local_users(st.session_state.user_db)
                            new_bal = st.session_state.user_db[selected_user]['balance']
                            st.session_state.deposit_msg_text = f"💰 ገንዘብ ገብቷል! ✅ {amount} ብር ለ {selected_user} ተጨምሯል! 🎉 አዲስ ቀሪ ሂሳብ: {new_bal:.2f} ብር 💵✨"
                            st.session_state.show_deposit_msg = True
                            st.rerun()
        
        with col2:
            if st.button("➕ Add Balance", type="primary", use_container_width=True):
                if selected_user in st.session_state.user_db:
                    st.session_state.user_db[selected_user]["balance"] = st.session_state.user_db[selected_user].get("balance", 0) + custom_amount
                    save_local_users(st.session_state.user_db)
                    new_bal = st.session_state.user_db[selected_user]['balance']
                    st.session_state.deposit_msg_text = f"💰 ገንዘብ ገብቷል! ✅ {custom_amount} ብር ለ {selected_user} ተጨምሯል! 🎉 አዲስ ቀሪ ሂሳብ: {new_bal:.2f} ብር 💵✨"
                    st.session_state.show_deposit_msg = True
                    st.rerun()
            
            if st.button("💰 Set Balance", type="primary", use_container_width=True):
                if selected_user in st.session_state.user_db:
                    st.session_state.user_db[selected_user]["balance"] = custom_amount
                    save_local_users(st.session_state.user_db)
                    new_bal = st.session_state.user_db[selected_user]['balance']
                    st.session_state.deposit_msg_text = f"💰 ገንዘብ ገብቷል! ✅ የ {selected_user} ቀሪ ሂሳብ ወደ {new_bal:.2f} ብር ተቀይሯል! 🎉💵✨"
                    st.session_state.show_deposit_msg = True
                    st.rerun()
        
        st.markdown("---")
        st.markdown("#### 💸 Deduct Balance")
        
        col3, col4 = st.columns([2, 1])
        
        with col3:
            deduct_options = [10, 20, 50, 100, 200, 500, 1000]
            custom_deduct = st.number_input("Custom Deduct Amount (ETB)", min_value=0, step=10, value=50)
            
            st.markdown("**Quick Deduct Amounts:**")
            deduct_cols = st.columns(5)
            for i, amount in enumerate(deduct_options):
                with deduct_cols[i % 5]:
                    if st.button(f"-{amount}", key=f"deduct_{amount}_{selected_user}"):
                        if selected_user in st.session_state.user_db:
                            current_bal = st.session_state.user_db[selected_user].get("balance", 0)
                            if current_bal >= amount:
                                st.session_state.user_db[selected_user]["balance"] = current_bal - amount
                                save_local_users(st.session_state.user_db)
                                st.success(f"✅ Deducted {amount} ETB from {selected_user}'s balance! New balance: {st.session_state.user_db[selected_user]['balance']:.2f} ETB")
                                st.rerun()
                            else:
                                st.error(f"❌ Insufficient balance! {selected_user} only has {current_bal:.2f} ETB.")
        
        with col4:
            if st.button("➖ Deduct Balance", type="primary", use_container_width=True):
                if selected_user in st.session_state.user_db:
                    current_bal = st.session_state.user_db[selected_user].get("balance", 0)
                    if current_bal >= custom_deduct:
                        st.session_state.user_db[selected_user]["balance"] = current_bal - custom_deduct
                        save_local_users(st.session_state.user_db)
                        st.success(f"✅ Deducted {custom_deduct} ETB from {selected_user}'s balance! New balance: {st.session_state.user_db[selected_user]['balance']:.2f} ETB")
                        st.rerun()
                    else:
                        st.error(f"❌ Insufficient balance! {selected_user} only has {current_bal:.2f} ETB.")
        
        st.markdown("---")
        st.markdown("#### 📊 All Users")
        
        user_list = []
        for username, data in st.session_state.user_db.items():
            if username != "admin":
                user_list.append({
                    "Username": username,
                    "Name": data.get("name", ""),
                    "Phone": data.get("phone", ""),
                    "Balance": data.get("balance", 0),
                    "Games Played": data.get("game_played", 0),
                    "Wins": data.get("wins", 0)
                })
        
        if user_list:
            st.dataframe(user_list, use_container_width=True)

# ===================================================================
# ALL 201 BINGO CARDS - FULL LIST
# ===================================================================

BINGO_CARDS = [
    {"id": 1, "cells": [['15', '16', '39', '59', '66'], ['11', '28', '40', '51', '68'], ['12', '20', 'F', '56', '67'], ['3', '30', '35', '60', '72'], ['10', '24', '37', '53', '64']]},
    {"id": 2, "cells": [['5', '21', '35', '46', '69'], ['15', '20', '42', '51', '70'], ['10', '28', 'F', '47', '67'], ['2', '26', '31', '49', '64'], ['6', '27', '33', '52', '65']]},
    {"id": 3, "cells": [['14', '23', '40', '58', '62'], ['13', '25', '32', '46', '65'], ['3', '28', 'F', '50', '63'], ['6', '30', '44', '54', '66'], ['10', '16', '37', '53', '74']]},
    {"id": 4, "cells": [['1', '19', '41', '49', '72'], ['5', '26', '36', '50', '69'], ['6', '29', 'F', '60', '61'], ['14', '25', '42', '47', '71'], ['2', '24', '45', '54', '65']]},
    {"id": 5, "cells": [['2', '16', '43', '47', '70'], ['4', '23', '32', '58', '73'], ['9', '17', 'F', '51', '74'], ['1', '26', '34', '59', '75'], ['14', '20', '31', '57', '72']]},
    {"id": 6, "cells": [['3', '28', '42', '46', '70'], ['15', '18', '36', '53', '64'], ['14', '20', 'F', '55', '67'], ['6', '21', '45', '57', '73'], ['11', '30', '41', '60', '62']]},
    {"id": 7, "cells": [['15', '28', '39', '58', '65'], ['10', '19', '34', '54', '68'], ['3', '17', 'F', '59', '71'], ['9', '16', '45', '51', '66'], ['14', '24', '36', '49', '64']]},
    {"id": 8, "cells": [['7', '20', '32', '47', '61'], ['13', '19', '36', '53', '67'], ['9', '21', 'F', '57', '66'], ['4', '18', '38', '59', '68'], ['2', '27', '45', '51', '69']]},
    {"id": 9, "cells": [['5', '26', '33', '56', '75'], ['2', '18', '39', '54', '62'], ['1', '29', 'F', '58', '72'], ['9', '22', '44', '57', '68'], ['13', '17', '42', '55', '67']]},
    {"id": 10, "cells": [['1', '20', '34', '58', '75'], ['13', '18', '40', '59', '69'], ['6', '27', 'F', '52', '67'], ['7', '23', '37', '48', '70'], ['2', '29', '44', '57', '73']]},
    {"id": 11, "cells": [['11', '21', '44', '49', '64'], ['4', '28', '34', '55', '62'], ['2', '26', 'F', '47', '71'], ['14', '29', '41', '48', '73'], ['5', '24', '31', '51', '63']]},
    {"id": 12, "cells": [['9', '20', '35', '59', '66'], ['1', '26', '43', '56', '72'], ['6', '16', 'F', '58', '64'], ['12', '22', '41', '49', '61'], ['2', '18', '38', '51', '69']]},
    {"id": 13, "cells": [['11', '16', '45', '60', '73'], ['1', '26', '44', '55', '69'], ['4', '29', 'F', '47', '72'], ['9', '28', '31', '51', '64'], ['14', '23', '40', '59', '68']]},
    {"id": 14, "cells": [['5', '18', '45', '58', '67'], ['1', '27', '42', '50', '65'], ['7', '28', 'F', '54', '64'], ['2', '21', '43', '60', '74'], ['10', '24', '32', '51', '71']]},
    {"id": 15, "cells": [['5', '30', '38', '48', '71'], ['1', '22', '42', '60', '62'], ['2', '18', 'F', '50', '65'], ['3', '29', '33', '46', '75'], ['12', '17', '32', '55', '66']]},
    {"id": 16, "cells": [['7', '23', '45', '55', '62'], ['3', '27', '42', '60', '71'], ['12', '21', 'F', '57', '66'], ['4', '24', '41', '49', '68'], ['13', '17', '44', '50', '75']]},
    {"id": 17, "cells": [['10', '28', '32', '59', '72'], ['3', '27', '40', '47', '63'], ['13', '24', 'F', '57', '71'], ['2', '21', '41', '60', '68'], ['7', '25', '42', '58', '65']]},
    {"id": 18, "cells": [['13', '27', '33', '51', '63'], ['7', '22', '42', '48', '61'], ['10', '25', 'F', '54', '65'], ['8', '16', '43', '52', '72'], ['14', '23', '38', '60', '74']]},
    {"id": 19, "cells": [['1', '22', '39', '51', '62'], ['15', '25', '35', '47', '75'], ['3', '23', 'F', '50', '66'], ['8', '26', '44', '49', '70'], ['4', '28', '38', '53', '67']]},
    {"id": 20, "cells": [['9', '19', '35', '54', '73'], ['8', '23', '43', '57', '61'], ['4', '24', 'F', '58', '68'], ['11', '17', '32', '50', '62'], ['1', '26', '38', '49', '75']]},
    {"id": 21, "cells": [['8', '18', '39', '54', '63'], ['2', '30', '37', '57', '75'], ['13', '29', 'F', '56', '68'], ['15', '27', '31', '49', '67'], ['6', '17', '45', '52', '61']]},
    {"id": 22, "cells": [['6', '26', '44', '55', '62'], ['13', '19', '32', '60', '61'], ['9', '25', 'F', '49', '75'], ['3', '20', '40', '46', '65'], ['8', '27', '31', '56', '71']]},
    {"id": 23, "cells": [['1', '27', '40', '54', '73'], ['4', '17', '33', '46', '68'], ['7', '16', 'F', '48', '63'], ['9', '23', '36', '56', '66'], ['11', '21', '34', '50', '74']]},
    {"id": 24, "cells": [['9', '19', '40', '46', '75'], ['8', '26', '31', '48', '67'], ['1', '24', 'F', '59', '65'], ['7', '20', '39', '49', '70'], ['12', '27', '43', '57', '73']]},
    {"id": 25, "cells": [['3', '23', '40', '53', '75'], ['1', '27', '45', '51', '68'], ['4', '28', 'F', '46', '73'], ['14', '29', '35', '56', '61'], ['9', '30', '41', '52', '74']]},
    {"id": 26, "cells": [['10', '25', '37', '53', '65'], ['14', '29', '38', '58', '69'], ['2', '28', 'F', '56', '68'], ['6', '22', '35', '57', '70'], ['3', '18', '45', '60', '67']]},
    {"id": 27, "cells": [['11', '26', '39', '51', '75'], ['3', '28', '33', '56', '67'], ['10', '24', 'F', '58', '74'], ['7', '18', '45', '53', '69'], ['13', '30', '44', '47', '64']]},
    {"id": 28, "cells": [['8', '17', '42', '52', '74'], ['2', '24', '39', '56', '63'], ['14', '16', 'F', '60', '62'], ['9', '21', '31', '47', '72'], ['15', '18', '35', '54', '70']]},
    {"id": 29, "cells": [['14', '16', '32', '53', '74'], ['15', '21', '34', '59', '65'], ['10', '26', 'F', '55', '66'], ['2', '19', '45', '56', '61'], ['1', '25', '40', '51', '64']]},
    {"id": 30, "cells": [['8', '27', '44', '54', '70'], ['11', '26', '31', '55', '64'], ['9', '19', 'F', '57', '67'], ['6', '23', '41', '49', '62'], ['13', '22', '40', '56', '72']]},
    {"id": 31, "cells": [['3', '27', '31', '46', '71'], ['9', '24', '40', '48', '67'], ['5', '17', 'F', '55', '62'], ['12', '18', '38', '58', '68'], ['4', '25', '36', '54', '73']]},
    {"id": 32, "cells": [['10', '20', '32', '58', '73'], ['15', '28', '34', '56', '61'], ['9', '24', 'F', '50', '75'], ['5', '25', '37', '46', '67'], ['14', '23', '31', '51', '65']]},
    {"id": 33, "cells": [['7', '29', '42', '56', '69'], ['15', '27', '40', '60', '64'], ['1', '18', 'F', '51', '74'], ['4', '16', '38', '57', '67'], ['8', '21', '39', '59', '68']]},
    {"id": 34, "cells": [['4', '17', '31', '46', '70'], ['8', '29', '37', '57', '65'], ['9', '24', 'F', '59', '75'], ['11', '27', '34', '55', '63'], ['3', '22', '36', '48', '73']]},
    {"id": 35, "cells": [['9', '17', '35', '55', '72'], ['14', '24', '45', '52', '68'], ['11', '18', 'F', '48', '66'], ['8', '21', '36', '47', '71'], ['4', '27', '37', '57', '70']]},
    {"id": 36, "cells": [['2', '22', '41', '54', '62'], ['13', '21', '45', '51', '70'], ['15', '30', 'F', '47', '63'], ['4', '26', '39', '50', '75'], ['10', '29', '34', '58', '64']]},
    {"id": 37, "cells": [['1', '21', '32', '54', '65'], ['5', '28', '42', '51', '63'], ['2', '26', 'F', '60', '61'], ['12', '24', '34', '59', '62'], ['15', '17', '43', '57', '72']]},
    {"id": 38, "cells": [['1', '30', '45', '49', '66'], ['9', '24', '42', '56', '69'], ['7', '20', 'F', '52', '74'], ['12', '17', '36', '60', '62'], ['11', '18', '35', '54', '63']]},
    {"id": 39, "cells": [['10', '27', '35', '51', '61'], ['14', '16', '37', '53', '72'], ['1', '25', 'F', '48', '69'], ['11', '26', '41', '58', '70'], ['13', '28', '42', '47', '68']]},
    {"id": 40, "cells": [['14', '17', '34', '54', '63'], ['10', '28', '43', '55', '70'], ['7', '16', 'F', '58', '71'], ['15', '24', '41', '59', '69'], ['6', '29', '36', '57', '64']]},
    {"id": 41, "cells": [['5', '18', '31', '52', '62'], ['10', '21', '43', '56', '66'], ['9', '28', 'F', '59', '69'], ['14', '25', '40', '48', '67'], ['6', '20', '35', '47', '71']]},
    {"id": 42, "cells": [['11', '20', '43', '49', '75'], ['10', '25', '33', '58', '74'], ['15', '17', 'F', '50', '67'], ['13', '21', '42', '52', '71'], ['2', '23', '35', '51', '64']]},
    {"id": 43, "cells": [['15', '18', '44', '54', '69'], ['6', '19', '31', '56', '64'], ['13', '16', 'F', '60', '70'], ['8', '27', '35', '55', '66'], ['7', '29', '38', '57', '72']]},
    {"id": 44, "cells": [['11', '28', '35', '47', '72'], ['4', '26', '45', '48', '73'], ['14', '16', 'F', '54', '71'], ['8', '25', '33', '52', '61'], ['7', '22', '44', '57', '68']]},
    {"id": 45, "cells": [['9', '27', '39', '48', '70'], ['6', '20', '38', '51', '63'], ['7', '19', 'F', '55', '68'], ['11', '22', '35', '46', '74'], ['8', '17', '45', '47', '69']]},
    {"id": 46, "cells": [['5', '17', '43', '47', '74'], ['15', '18', '42', '48', '63'], ['11', '21', 'F', '56', '64'], ['4', '23', '39', '54', '66'], ['2', '25', '33', '49', '65']]},
    {"id": 47, "cells": [['5', '17', '38', '46', '70'], ['6', '20', '43', '51', '75'], ['12', '25', 'F', '56', '61'], ['1', '16', '45', '60', '68'], ['4', '26', '35', '53', '74']]},
    {"id": 48, "cells": [['4', '28', '37', '53', '61'], ['2', '19', '31', '49', '62'], ['7', '16', 'F', '56', '64'], ['14', '26', '39', '52', '74'], ['6', '18', '32', '57', '67']]},
    {"id": 49, "cells": [['1', '21', '34', '52', '67'], ['3', '29', '41', '54', '69'], ['10', '24', 'F', '57', '70'], ['8', '26', '35', '53', '72'], ['6', '19', '31', '58', '64']]},
    {"id": 50, "cells": [['3', '17', '36', '49', '69'], ['10', '30', '40', '52', '62'], ['14', '27', 'F', '58', '66'], ['2', '19', '41', '59', '68'], ['15', '18', '42', '47', '64']]},
    {"id": 51, "cells": [['2', '21', '31', '49', '68'], ['12', '20', '45', '54', '69'], ['10', '27', 'F', '48', '75'], ['9', '16', '40', '46', '61'], ['14', '19', '39', '57', '62']]},
    {"id": 52, "cells": [['10', '22', '36', '59', '74'], ['2', '21', '44', '55', '70'], ['11', '26', 'F', '48', '72'], ['15', '23', '40', '57', '75'], ['14', '18', '31', '58', '66']]},
    {"id": 53, "cells": [['15', '30', '35', '59', '69'], ['5', '21', '45', '51', '71'], ['8', '25', 'F', '46', '67'], ['7', '23', '40', '58', '74'], ['11', '29', '42', '54', '72']]},
    {"id": 54, "cells": [['1', '26', '34', '60', '61'], ['6', '18', '35', '52', '66'], ['4', '24', 'F', '50', '69'], ['15', '29', '32', '48', '63'], ['7', '25', '45', '53', '72']]},
    {"id": 55, "cells": [['12', '24', '45', '51', '65'], ['8', '16', '42', '53', '62'], ['15', '19', 'F', '59', '64'], ['7', '25', '39', '56', '70'], ['14', '20', '32', '48', '74']]},
    {"id": 56, "cells": [['13', '17', '44', '53', '68'], ['3', '30', '45', '56', '66'], ['15', '28', 'F', '55', '73'], ['12', '20', '33', '50', '70'], ['4', '24', '43', '52', '67']]},
    {"id": 57, "cells": [['5', '28', '40', '56', '63'], ['12', '21', '36', '53', '73'], ['14', '16', 'F', '60', '68'], ['15', '25', '44', '58', '66'], ['11', '17', '45', '54', '64']]},
    {"id": 58, "cells": [['1', '16', '32', '58', '74'], ['3', '28', '44', '60', '67'], ['9', '24', 'F', '49', '64'], ['10', '20', '37', '47', '71'], ['13', '19', '39', '46', '61']]},
    {"id": 59, "cells": [['7', '20', '34', '47', '70'], ['2', '24', '43', '55', '73'], ['3', '29', 'F', '46', '62'], ['12', '18', '45', '49', '69'], ['5', '17', '33', '57', '64']]},
    {"id": 60, "cells": [['14', '25', '41', '48', '75'], ['9', '17', '34', '51', '62'], ['1', '30', 'F', '60', '65'], ['13', '28', '38', '49', '73'], ['6', '22', '40', '54', '61']]},
    {"id": 61, "cells": [['11', '26', '38', '60', '71'], ['5', '25', '37', '52', '65'], ['14', '16', 'F', '59', '62'], ['7', '18', '43', '54', '64'], ['9', '28', '41', '46', '74']]},
    {"id": 62, "cells": [['13', '26', '31', '56', '68'], ['8', '27', '43', '59', '70'], ['11', '18', 'F', '53', '73'], ['6', '21', '36', '48', '72'], ['2', '20', '42', '55', '69']]},
    {"id": 63, "cells": [['12', '21', '35', '49', '62'], ['1', '29', '38', '55', '74'], ['15', '22', 'F', '51', '64'], ['5', '28', '33', '50', '65'], ['4', '17', '37', '60', '72']]},
    {"id": 64, "cells": [['15', '24', '38', '58', '64'], ['1', '22', '44', '60', '73'], ['14', '21', 'F', '48', '67'], ['2', '29', '31', '47', '68'], ['4', '23', '41', '56', '61']]},
    {"id": 65, "cells": [['6', '18', '35', '57', '64'], ['10', '28', '32', '52', '62'], ['7', '19', 'F', '48', '63'], ['9', '20', '39', '49', '68'], ['2', '30', '33', '59', '65']]},
    {"id": 66, "cells": [['1', '20', '34', '54', '67'], ['2', '27', '33', '51', '63'], ['14', '21', 'F', '58', '73'], ['3', '28', '42', '46', '70'], ['4', '24', '37', '55', '64']]},
    {"id": 67, "cells": [['13', '28', '38', '58', '71'], ['14', '22', '44', '51', '73'], ['5', '26', 'F', '56', '61'], ['12', '24', '34', '53', '72'], ['8', '17', '40', '52', '62']]},
    {"id": 68, "cells": [['14', '25', '41', '55', '66'], ['7', '28', '38', '59', '65'], ['9', '19', 'F', '53', '61'], ['13', '22', '33', '56', '68'], ['15', '18', '44', '57', '63']]},
    {"id": 69, "cells": [['10', '16', '35', '55', '65'], ['6', '28', '40', '46', '70'], ['2', '17', 'F', '59', '73'], ['15', '29', '36', '47', '75'], ['8', '27', '39', '51', '62']]},
    {"id": 70, "cells": [['15', '30', '36', '50', '70'], ['9', '18', '32', '59', '65'], ['12', '17', 'F', '58', '75'], ['6', '21', '43', '46', '62'], ['4', '23', '38', '48', '69']]},
    {"id": 71, "cells": [['6', '25', '31', '49', '72'], ['4', '22', '43', '53', '61'], ['2', '28', 'F', '57', '69'], ['7', '17', '41', '54', '63'], ['12', '19', '45', '46', '65']]},
    {"id": 72, "cells": [['8', '18', '40', '46', '64'], ['5', '20', '35', '47', '71'], ['6', '27', 'F', '49', '73'], ['10', '19', '42', '55', '65'], ['2', '17', '45', '58', '75']]},
    {"id": 73, "cells": [['6', '28', '37', '48', '72'], ['2', '23', '43', '57', '61'], ['15', '30', 'F', '54', '66'], ['13', '21', '34', '60', '65'], ['7', '27', '35', '46', '63']]},
    {"id": 74, "cells": [['10', '24', '45', '51', '72'], ['14', '21', '36', '53', '67'], ['3', '17', 'F', '49', '62'], ['7', '18', '41', '48', '66'], ['9', '26', '44', '54', '63']]},
    {"id": 75, "cells": [['6', '17', '44', '59', '75'], ['7', '20', '37', '46', '69'], ['4', '29', 'F', '50', '63'], ['3', '23', '41', '49', '71'], ['14', '24', '40', '52', '72']]},
    {"id": 76, "cells": [['4', '19', '39', '48', '62'], ['10', '24', '31', '60', '70'], ['6', '23', 'F', '51', '66'], ['8', '18', '35', '50', '73'], ['2', '27', '41', '47', '61']]},
    {"id": 77, "cells": [['1', '18', '34', '60', '74'], ['7', '27', '35', '56', '61'], ['15', '25', 'F', '55', '68'], ['14', '21', '38', '53', '64'], ['13', '17', '40', '58', '75']]},
    {"id": 78, "cells": [['15', '27', '37', '47', '67'], ['11', '17', '34', '58', '70'], ['1', '30', 'F', '46', '68'], ['8', '24', '39', '50', '62'], ['13', '22', '38', '57', '66']]},
    {"id": 79, "cells": [['4', '26', '39', '57', '72'], ['13', '17', '40', '58', '61'], ['11', '29', 'F', '54', '69'], ['3', '16', '44', '53', '65'], ['8', '18', '45', '46', '62']]},
    {"id": 80, "cells": [['8', '23', '39', '57', '73'], ['4', '27', '37', '56', '66'], ['1', '19', 'F', '51', '65'], ['5', '30', '31', '47', '63'], ['2', '17', '32', '48', '67']]},
    {"id": 81, "cells": [['3', '23', '45', '49', '66'], ['5', '16', '41', '50', '62'], ['14', '19', 'F', '47', '72'], ['9', '20', '44', '51', '73'], ['2', '25', '38', '52', '64']]},
    {"id": 82, "cells": [['14', '16', '36', '54', '63'], ['8', '17', '31', '59', '64'], ['1', '25', 'F', '55', '72'], ['7', '20', '33', '47', '66'], ['2', '18', '41', '58', '61']]},
    {"id": 83, "cells": [['1', '16', '31', '53', '67'], ['3', '20', '34', '57', '73'], ['9', '28', 'F', '49', '63'], ['10', '26', '38', '54', '70'], ['2', '25', '36', '47', '61']]},
    {"id": 84, "cells": [['11', '29', '32', '59', '64'], ['12', '19', '41', '60', '67'], ['13', '28', 'F', '56', '62'], ['10', '24', '39', '46', '75'], ['5', '22', '38', '58', '74']]},
    {"id": 85, "cells": [['13', '28', '31', '51', '62'], ['1', '30', '34', '59', '66'], ['14', '17', 'F', '50', '64'], ['3', '16', '36', '56', '71'], ['4', '29', '40', '47', '61']]},
    {"id": 86, "cells": [['4', '21', '37', '54', '67'], ['13', '27', '44', '57', '61'], ['15', '26', 'F', '46', '71'], ['2', '25', '33', '58', '70'], ['9', '28', '42', '48', '68']]},
    {"id": 87, "cells": [['2', '25', '35', '46', '66'], ['1', '17', '43', '49', '63'], ['15', '29', 'F', '59', '72'], ['14', '20', '33', '58', '62'], ['8', '22', '34', '48', '73']]},
    {"id": 88, "cells": [['13', '19', '43', '55', '64'], ['14', '18', '42', '48', '63'], ['12', '23', 'F', '58', '75'], ['15', '29', '44', '52', '65'], ['7', '27', '40', '57', '73']]},
    {"id": 89, "cells": [['2', '16', '44', '58', '75'], ['5', '26', '40', '56', '65'], ['14', '17', 'F', '54', '61'], ['10', '24', '33', '57', '72'], ['7', '22', '38', '60', '69']]},
    {"id": 90, "cells": [['13', '26', '44', '48', '69'], ['3', '20', '38', '58', '70'], ['5', '17', 'F', '46', '72'], ['12', '22', '32', '56', '62'], ['1', '24', '36', '54', '63']]},
    {"id": 91, "cells": [['5', '29', '41', '59', '72'], ['1', '25', '31', '46', '63'], ['10', '30', 'F', '57', '71'], ['8', '17', '34', '55', '75'], ['6', '28', '32', '47', '74']]},
    {"id": 92, "cells": [['5', '18', '37', '59', '63'], ['9', '27', '38', '57', '70'], ['14', '24', 'F', '52', '66'], ['13', '28', '41', '56', '71'], ['1', '30', '45', '46', '72']]},
    {"id": 93, "cells": [['14', '21', '33', '46', '65'], ['15', '18', '40', '53', '71'], ['13', '16', 'F', '51', '63'], ['7', '23', '34', '48', '75'], ['8', '20', '31', '47', '74']]},
    {"id": 94, "cells": [['1', '19', '39', '58', '67'], ['8', '22', '40', '53', '62'], ['7', '30', 'F', '50', '65'], ['5', '25', '41', '46', '72'], ['2', '17', '38', '56', '64']]},
    {"id": 95, "cells": [['4', '19', '37', '52', '70'], ['6', '24', '43', '60', '65'], ['5', '16', 'F', '56', '75'], ['12', '29', '41', '51', '67'], ['9', '30', '39', '58', '61']]},
    {"id": 96, "cells": [['2', '18', '34', '54', '74'], ['14', '27', '45', '57', '64'], ['11', '21', 'F', '56', '62'], ['13', '19', '33', '48', '61'], ['4', '16', '41', '53', '72']]},
    {"id": 97, "cells": [['2', '29', '45', '47', '66'], ['12', '30', '42', '60', '74'], ['9', '21', 'F', '58', '61'], ['6', '27', '40', '48', '62'], ['15', '23', '34', '57', '65']]},
    {"id": 98, "cells": [['13', '24', '40', '57', '68'], ['15', '20', '45', '50', '64'], ['9', '19', 'F', '60', '67'], ['8', '28', '43', '56', '70'], ['2', '27', '38', '47', '65']]},
    {"id": 99, "cells": [['7', '30', '45', '49', '66'], ['12', '19', '35', '55', '62'], ['3', '23', 'F', '53', '67'], ['10', '25', '36', '50', '65'], ['11', '29', '32', '51', '74']]},
    {"id": 100, "cells": [['15', '27', '31', '54', '73'], ['10', '29', '37', '50', '69'], ['8', '23', 'F', '57', '75'], ['11', '25', '43', '58', '68'], ['4', '24', '38', '46', '74']]},
    {"id": 101, "cells": [['15', '17', '35', '59', '75'], ['9', '22', '43', '54', '74'], ['1', '29', 'F', '51', '64'], ['7', '16', '37', '48', '66'], ['10', '23', '41', '52', '65']]},
    {"id": 102, "cells": [['7', '16', '32', '50', '64'], ['10', '29', '38', '48', '63'], ['13', '22', 'F', '53', '74'], ['12', '18', '44', '56', '70'], ['4', '27', '39', '57', '71']]},
    {"id": 103, "cells": [['3', '23', '41', '58', '62'], ['4', '22', '35', '50', '61'], ['12', '17', 'F', '59', '73'], ['2', '20', '43', '52', '75'], ['8', '27', '44', '51', '67']]},
    {"id": 104, "cells": [['13', '25', '39', '58', '68'], ['9', '19', '42', '46', '67'], ['4', '22', 'F', '52', '75'], ['5', '18', '32', '49', '72'], ['6', '23', '38', '51', '70']]},
    {"id": 105, "cells": [['12', '17', '36', '49', '67'], ['6', '16', '41', '56', '63'], ['4', '22', 'F', '57', '74'], ['5', '20', '39', '60', '62'], ['1', '29', '35', '51', '65']]},
    {"id": 106, "cells": [['15', '16', '43', '54', '61'], ['9', '24', '42', '60', '70'], ['13', '27', 'F', '56', '63'], ['14', '20', '45', '57', '62'], ['10', '18', '35', '53', '72']]},
    {"id": 107, "cells": [['3', '28', '34', '57', '62'], ['14', '30', '40', '52', '68'], ['4', '27', 'F', '49', '65'], ['9', '22', '33', '58', '70'], ['2', '29', '36', '47', '63']]},
    {"id": 108, "cells": [['1', '23', '41', '47', '75'], ['7', '22', '40', '52', '62'], ['3', '16', 'F', '58', '68'], ['2', '18', '43', '50', '67'], ['6', '30', '44', '57', '61']]},
    {"id": 109, "cells": [['15', '27', '36', '47', '70'], ['13', '17', '42', '59', '61'], ['5', '23', 'F', '57', '62'], ['7', '25', '38', '50', '69'], ['6', '26', '35', '52', '72']]},
    {"id": 110, "cells": [['11', '27', '41', '51', '64'], ['13', '30', '34', '55', '74'], ['3', '28', 'F', '54', '66'], ['6', '18', '37', '46', '62'], ['7', '26', '32', '57', '70']]},
    {"id": 111, "cells": [['3', '30', '41', '51', '66'], ['12', '25', '32', '53', '72'], ['8', '20', 'F', '47', '71'], ['13', '24', '39', '60', '74'], ['1', '28', '38', '50', '63']]},
    {"id": 112, "cells": [['12', '24', '41', '50', '68'], ['14', '21', '35', '52', '65'], ['7', '17', 'F', '46', '70'], ['3', '20', '43', '57', '74'], ['1', '29', '33', '48', '62']]},
    {"id": 113, "cells": [['11', '21', '34', '56', '63'], ['12', '23', '32', '53', '69'], ['3', '24', 'F', '54', '71'], ['2', '26', '37', '49', '72'], ['4', '22', '36', '48', '75']]},
    {"id": 114, "cells": [['12', '30', '37', '51', '74'], ['14', '19', '43', '57', '63'], ['7', '28', 'F', '48', '67'], ['13', '22', '31', '46', '62'], ['3', '20', '38', '54', '70']]},
    {"id": 115, "cells": [['2', '19', '39', '50', '70'], ['9', '23', '34', '49', '64'], ['13', '27', 'F', '59', '61'], ['11', '26', '38', '53', '67'], ['14', '28', '44', '54', '63']]},
    {"id": 116, "cells": [['7', '21', '38', '56', '65'], ['15', '26', '34', '52', '75'], ['1', '30', 'F', '50', '71'], ['4', '27', '43', '54', '66'], ['12', '28', '44', '59', '70']]},
    {"id": 117, "cells": [['1', '21', '33', '57', '65'], ['2', '29', '32', '50', '61'], ['9', '25', 'F', '53', '74'], ['6', '28', '34', '55', '75'], ['14', '18', '37', '47', '67']]},
    {"id": 118, "cells": [['1', '22', '31', '47', '67'], ['6', '26', '37', '54', '64'], ['10', '27', 'F', '49', '62'], ['14', '24', '42', '55', '72'], ['5', '18', '34', '59', '71']]},
    {"id": 119, "cells": [['14', '26', '45', '56', '72'], ['12', '29', '42', '55', '62'], ['15', '23', 'F', '48', '73'], ['3', '28', '41', '49', '61'], ['13', '16', '31', '54', '65']]},
    {"id": 120, "cells": [['7', '25', '37', '60', '70'], ['13', '20', '43', '50', '69'], ['4', '18', 'F', '55', '74'], ['5', '26', '40', '48', '67'], ['8', '17', '39', '46', '73']]},
    {"id": 121, "cells": [['11', '27', '38', '51', '63'], ['7', '20', '41', '59', '64'], ['5', '28', 'F', '54', '71'], ['12', '29', '33', '56', '73'], ['8', '25', '40', '55', '69']]},
    {"id": 122, "cells": [['11', '21', '32', '51', '70'], ['6', '28', '44', '60', '74'], ['5', '18', 'F', '57', '63'], ['1', '16', '38', '46', '62'], ['9', '17', '31', '53', '73']]},
    {"id": 123, "cells": [['14', '20', '43', '54', '70'], ['10', '28', '40', '51', '69'], ['6', '21', 'F', '53', '67'], ['8', '18', '35', '50', '74'], ['3', '29', '34', '48', '64']]},
    {"id": 124, "cells": [['6', '20', '38', '50', '66'], ['5', '21', '33', '49', '61'], ['4', '30', 'F', '48', '75'], ['13', '26', '41', '60', '65'], ['15', '19', '36', '56', '63']]},
    {"id": 125, "cells": [['12', '28', '33', '58', '75'], ['1', '25', '39', '60', '66'], ['13', '20', 'F', '48', '61'], ['14', '21', '44', '46', '65'], ['5', '22', '38', '54', '67']]},
    {"id": 126, "cells": [['13', '22', '41', '57', '65'], ['12', '30', '32', '60', '62'], ['6', '24', 'F', '58', '61'], ['1', '16', '44', '50', '63'], ['2', '17', '45', '53', '69']]},
    {"id": 127, "cells": [['13', '26', '43', '60', '65'], ['4', '16', '38', '52', '62'], ['2', '25', 'F', '58', '63'], ['9', '17', '34', '47', '74'], ['5', '27', '41', '46', '68']]},
    {"id": 128, "cells": [['7', '25', '43', '47', '63'], ['11', '16', '32', '58', '61'], ['2', '23', 'F', '55', '71'], ['3', '22', '38', '46', '68'], ['1', '30', '36', '57', '72']]},
    {"id": 129, "cells": [['3', '25', '43', '57', '63'], ['2', '20', '35', '59', '71'], ['13', '23', 'F', '60', '74'], ['10', '29', '38', '49', '73'], ['11', '21', '42', '53', '70']]},
    {"id": 130, "cells": [['5', '18', '31', '56', '75'], ['15', '27', '42', '59', '66'], ['4', '16', 'F', '57', '71'], ['1', '30', '45', '51', '64'], ['2', '28', '43', '53', '67']]},
    {"id": 131, "cells": [['2', '19', '36', '51', '64'], ['14', '29', '37', '46', '70'], ['3', '28', 'F', '55', '68'], ['12', '23', '32', '56', '67'], ['1', '20', '40', '48', '71']]},
    {"id": 132, "cells": [['1', '30', '32', '48', '67'], ['5', '22', '42', '57', '64'], ['6', '17', 'F', '58', '65'], ['7', '24', '43', '46', '73'], ['2', '18', '37', '55', '74']]},
    {"id": 133, "cells": [['14', '28', '37', '55', '73'], ['6', '16', '39', '54', '72'], ['7', '22', 'F', '58', '63'], ['4', '25', '32', '51', '74'], ['10', '23', '40', '52', '61']]},
    {"id": 134, "cells": [['10', '25', '38', '58', '74'], ['9', '24', '41', '49', '69'], ['1', '26', 'F', '48', '66'], ['4', '28', '39', '57', '75'], ['14', '17', '42', '52', '61']]},
    {"id": 135, "cells": [['13', '24', '45', '52', '61'], ['8', '22', '35', '60', '73'], ['7', '17', 'F', '54', '68'], ['9', '27', '42', '59', '63'], ['5', '26', '40', '49', '71']]},
    {"id": 136, "cells": [['15', '30', '40', '47', '72'], ['4', '22', '32', '55', '70'], ['13', '24', 'F', '53', '66'], ['5', '29', '35', '58', '61'], ['2', '17', '31', '51', '71']]},
    {"id": 137, "cells": [['1', '27', '38', '56', '61'], ['7', '19', '43', '53', '70'], ['3', '24', 'F', '52', '65'], ['11', '22', '31', '51', '74'], ['12', '16', '45', '57', '71']]},
    {"id": 138, "cells": [['4', '30', '35', '58', '65'], ['6', '24', '42', '56', '61'], ['1', '27', 'F', '54', '71'], ['10', '16', '39', '55', '64'], ['13', '21', '36', '53', '67']]},
    {"id": 139, "cells": [['11', '29', '45', '47', '75'], ['4', '21', '41', '46', '67'], ['12', '17', 'F', '53', '69'], ['6', '22', '40', '51', '74'], ['14', '19', '44', '60', '62']]},
    {"id": 140, "cells": [['6', '18', '32', '51', '62'], ['8', '21', '43', '57', '65'], ['2', '16', 'F', '49', '71'], ['13', '30', '41', '59', '75'], ['7', '29', '35', '48', '64']]},
    {"id": 141, "cells": [['11', '20', '42', '49', '70'], ['5', '26', '41', '47', '72'], ['6', '18', 'F', '60', '66'], ['4', '21', '45', '57', '63'], ['14', '19', '36', '52', '69']]},
    {"id": 142, "cells": [['13', '23', '44', '60', '69'], ['10', '27', '42', '47', '71'], ['2', '24', 'F', '58', '68'], ['4', '29', '31', '59', '63'], ['12', '25', '45', '55', '65']]},
    {"id": 143, "cells": [['6', '30', '41', '48', '63'], ['13', '20', '37', '53', '66'], ['10', '16', 'F', '57', '73'], ['14', '28', '35', '54', '67'], ['8', '29', '39', '51', '72']]},
    {"id": 144, "cells": [['14', '20', '42', '60', '65'], ['12', '27', '43', '49', '66'], ['15', '21', 'F', '50', '64'], ['4', '17', '41', '55', '67'], ['6', '25', '39', '51', '72']]},
    {"id": 145, "cells": [['15', '30', '33', '56', '69'], ['9', '29', '32', '57', '65'], ['4', '22', 'F', '46', '66'], ['3', '28', '43', '48', '72'], ['14', '16', '39', '52', '67']]},
    {"id": 146, "cells": [['10', '20', '36', '55', '64'], ['2', '19', '39', '58', '67'], ['7', '28', 'F', '54', '63'], ['14', '30', '35', '60', '66'], ['4', '23', '45', '56', '62']]},
    {"id": 147, "cells": [['11', '29', '34', '50', '68'], ['8', '26', '35', '58', '74'], ['12', '27', 'F', '46', '64'], ['2', '30', '42', '49', '73'], ['15', '23', '41', '57', '69']]},
    {"id": 148, "cells": [['14', '20', '38', '53', '74'], ['15', '22', '45', '56', '64'], ['10', '17', 'F', '50', '63'], ['3', '25', '37', '51', '69'], ['6', '29', '35', '59', '61']]},
    {"id": 149, "cells": [['14', '23', '37', '52', '72'], ['15', '27', '40', '54', '63'], ['7', '18', 'F', '47', '75'], ['6', '16', '42', '57', '61'], ['12', '20', '32', '60', '62']]},
    {"id": 150, "cells": [['6', '24', '33', '48', '75'], ['10', '19', '37', '50', '64'], ['7', '28', 'F', '57', '68'], ['13', '17', '43', '58', '72'], ['11', '21', '35', '53', '74']]},
    {"id": 151, "cells": [['3', '19', '42', '56', '71'], ['8', '22', '37', '46', '62'], ['15', '29', 'F', '57', '72'], ['9', '17', '39', '60', '69'], ['1', '18', '40', '59', '64']]},
    {"id": 152, "cells": [['6', '21', '38', '52', '63'], ['11', '24', '37', '55', '72'], ['14', '27', 'F', '49', '61'], ['2', '23', '44', '58', '68'], ['10', '29', '33', '47', '74']]},
    {"id": 153, "cells": [['14', '16', '44', '51', '69'], ['1', '17', '34', '56', '67'], ['7', '29', 'F', '47', '75'], ['4', '30', '41', '54', '65'], ['10', '18', '43', '49', '61']]},
    {"id": 154, "cells": [['10', '30', '35', '53', '67'], ['14', '18', '38', '47', '64'], ['5', '26', 'F', '60', '69'], ['6', '20', '32', '56', '61'], ['15', '27', '39', '48', '65']]},
    {"id": 155, "cells": [['12', '16', '31', '54', '62'], ['9', '23', '41', '56', '73'], ['13', '20', 'F', '60', '61'], ['2', '28', '42', '57', '67'], ['7', '24', '35', '50', '63']]},
    {"id": 156, "cells": [['14', '26', '42', '56', '66'], ['11', '30', '31', '57', '69'], ['1', '18', 'F', '54', '70'], ['8', '29', '34', '52', '71'], ['15', '16', '40', '50', '62']]},
    {"id": 157, "cells": [['6', '24', '40', '58', '62'], ['10', '26', '31', '47', '74'], ['13', '25', 'F', '57', '64'], ['1', '28', '41', '48', '65'], ['14', '29', '35', '53', '73']]},
    {"id": 158, "cells": [['1', '18', '40', '56', '75'], ['15', '17', '42', '54', '64'], ['11', '24', 'F', '60', '70'], ['7', '20', '38', '51', '72'], ['14', '21', '43', '48', '65']]},
    {"id": 159, "cells": [['12', '17', '36', '53', '72'], ['9', '21', '38', '56', '65'], ['4', '26', 'F', '50', '70'], ['10', '18', '40', '59', '67'], ['8', '22', '35', '55', '69']]},
    {"id": 160, "cells": [['3', '25', '33', '56', '69'], ['5', '24', '36', '54', '70'], ['9', '23', 'F', '60', '66'], ['12', '27', '32', '49', '68'], ['10', '18', '43', '46', '73']]},
    {"id": 161, "cells": [['2', '25', '36', '51', '65'], ['9', '16', '42', '59', '61'], ['6', '27', 'F', '50', '62'], ['11', '17', '39', '52', '75'], ['10', '22', '37', '60', '72']]},
    {"id": 162, "cells": [['8', '20', '43', '56', '69'], ['13', '30', '40', '47', '70'], ['14', '29', 'F', '57', '75'], ['2', '25', '34', '60', '61'], ['3', '19', '31', '54', '71']]},
    {"id": 163, "cells": [['12', '19', '37', '53', '61'], ['1', '23', '35', '46', '74'], ['13', '21', 'F', '55', '72'], ['3', '30', '39', '54', '64'], ['15', '20', '31', '58', '75']]},
    {"id": 164, "cells": [['13', '22', '42', '55', '65'], ['15', '30', '32', '52', '72'], ['5', '18', 'F', '54', '75'], ['11', '25', '39', '58', '61'], ['14', '24', '41', '46', '68']]},
    {"id": 165, "cells": [['13', '30', '36', '57', '70'], ['14', '26', '40', '52', '64'], ['12', '22', 'F', '51', '68'], ['10', '18', '37', '47', '66'], ['7', '16', '39', '56', '67']]},
    {"id": 166, "cells": [['1', '19', '41', '47', '74'], ['9', '26', '42', '53', '68'], ['4', '29', 'F', '54', '67'], ['12', '21', '32', '56', '65'], ['8', '18', '45', '49', '70']]},
    {"id": 167, "cells": [['8', '18', '33', '49', '67'], ['5', '24', '31', '55', '66'], ['6', '20', 'F', '59', '72'], ['15', '19', '37', '47', '73'], ['12', '26', '42', '46', '71']]},
    {"id": 168, "cells": [['12', '27', '33', '48', '69'], ['9', '24', '38', '49', '71'], ['11', '16', 'F', '57', '75'], ['7', '18', '31', '46', '61'], ['2', '20', '32', '60', '73']]},
    {"id": 169, "cells": [['13', '18', '34', '52', '75'], ['10', '19', '32', '54', '61'], ['3', '26', 'F', '51', '62'], ['15', '16', '38', '50', '70'], ['12', '21', '37', '48', '66']]},
    {"id": 170, "cells": [['9', '23', '34', '48', '73'], ['5', '22', '35', '55', '72'], ['4', '19', 'F', '50', '67'], ['15', '24', '40', '49', '63'], ['10', '29', '42', '51', '64']]},
    {"id": 171, "cells": [['5', '25', '36', '57', '70'], ['11', '24', '31', '51', '69'], ['9', '29', 'F', '60', '66'], ['12', '30', '39', '48', '72'], ['6', '27', '38', '52', '68']]},
    {"id": 172, "cells": [['11', '20', '43', '59', '70'], ['3', '29', '41', '50', '69'], ['5', '18', 'F', '46', '65'], ['14', '30', '39', '52', '74'], ['15', '24', '40', '47', '64']]},
    {"id": 173, "cells": [['14', '16', '38', '53', '66'], ['15', '30', '31', '60', '61'], ['4', '18', 'F', '56', '68'], ['3', '19', '43', '58', '69'], ['7', '23', '39', '48', '71']]},
    {"id": 174, "cells": [['11', '21', '33', '49', '68'], ['5', '18', '44', '48', '74'], ['13', '17', 'F', '55', '75'], ['3', '26', '38', '57', '71'], ['9', '25', '43', '56', '66']]},
    {"id": 175, "cells": [['10', '17', '43', '52', '62'], ['2', '27', '42', '51', '74'], ['12', '29', 'F', '55', '61'], ['1', '22', '31', '57', '75'], ['8', '21', '45', '46', '70']]},
    {"id": 176, "cells": [['8', '27', '44', '49', '65'], ['6', '20', '40', '51', '63'], ['15', '24', 'F', '60', '68'], ['9', '26', '33', '52', '70'], ['14', '22', '42', '53', '67']]},
    {"id": 177, "cells": [['3', '28', '39', '55', '62'], ['1', '19', '44', '50', '61'], ['15', '18', 'F', '57', '71'], ['9', '16', '40', '52', '75'], ['13', '21', '35', '54', '64']]},
    {"id": 178, "cells": [['6', '28', '37', '60', '61'], ['2', '24', '39', '56', '66'], ['7', '20', 'F', '46', '63'], ['15', '26', '43', '47', '74'], ['4', '19', '34', '48', '65']]},
    {"id": 179, "cells": [['4', '22', '45', '46', '75'], ['5', '27', '33', '49', '65'], ['14', '26', 'F', '58', '63'], ['11', '24', '43', '48', '70'], ['15', '30', '36', '53', '73']]},
    {"id": 180, "cells": [['12', '23', '31', '54', '65'], ['9', '29', '43', '55', '70'], ['2', '18', 'F', '57', '68'], ['15', '21', '39', '56', '64'], ['5', '19', '38', '52', '75']]},
    {"id": 181, "cells": [['9', '24', '44', '53', '68'], ['4', '19', '38', '57', '63'], ['5', '25', 'F', '55', '66'], ['8', '28', '42', '49', '70'], ['13', '21', '35', '59', '62']]},
    {"id": 182, "cells": [['10', '16', '32', '55', '74'], ['4', '29', '42', '46', '67'], ['11', '20', 'F', '50', '70'], ['15', '19', '38', '49', '75'], ['12', '27', '31', '58', '71']]},
    {"id": 183, "cells": [['1', '23', '45', '57', '61'], ['13', '18', '38', '49', '63'], ['15', '26', 'F', '48', '62'], ['2', '19', '39', '58', '70'], ['6', '28', '32', '55', '72']]},
    {"id": 184, "cells": [['10', '22', '32', '54', '68'], ['2', '17', '42', '59', '66'], ['8', '18', 'F', '55', '63'], ['1', '27', '40', '56', '69'], ['15', '30', '43', '49', '71']]},
    {"id": 185, "cells": [['10', '24', '44', '58', '66'], ['5', '22', '43', '46', '69'], ['13', '21', 'F', '54', '75'], ['2', '20', '31', '55', '61'], ['3', '28', '33', '50', '74']]},
    {"id": 186, "cells": [['1', '29', '43', '54', '61'], ['14', '28', '45', '51', '69'], ['9', '25', 'F', '59', '67'], ['5', '23', '33', '58', '63'], ['7', '16', '31', '48', '74']]},
    {"id": 187, "cells": [['12', '26', '36', '48', '71'], ['1', '29', '38', '49', '74'], ['3', '30', 'F', '59', '70'], ['9', '21', '33', '60', '64'], ['11', '18', '40', '52', '67']]},
    {"id": 188, "cells": [['8', '29', '44', '49', '65'], ['13', '21', '41', '58', '71'], ['10', '16', 'F', '53', '69'], ['4', '24', '43', '48', '74'], ['11', '25', '40', '47', '63']]},
    {"id": 189, "cells": [['14', '17', '36', '52', '63'], ['3', '23', '45', '59', '70'], ['13', '28', 'F', '53', '74'], ['15', '24', '41', '56', '67'], ['9', '26', '42', '55', '66']]},
    {"id": 190, "cells": [['7', '26', '40', '47', '65'], ['15', '18', '45', '57', '63'], ['14', '16', 'F', '58', '71'], ['2', '20', '38', '46', '72'], ['8', '28', '32', '56', '64']]},
    {"id": 191, "cells": [['1', '30', '39', '55', '66'], ['7', '27', '45', '60', '74'], ['5', '20', 'F', '58', '69'], ['13', '17', '44', '57', '62'], ['9', '24', '36', '51', '65']]},
    {"id": 192, "cells": [['8', '29', '35', '60', '71'], ['9', '25', '41', '53', '67'], ['14', '20', 'F', '55', '65'], ['2', '19', '42', '51', '68'], ['13', '28', '43', '57', '61']]},
    {"id": 193, "cells": [['14', '29', '44', '53', '65'], ['8', '25', '43', '52', '72'], ['13', '19', 'F', '59', '71'], ['7', '18', '39', '57', '75'], ['3', '23', '36', '50', '69']]},
    {"id": 194, "cells": [['4', '29', '44', '50', '67'], ['15', '26', '35', '49', '75'], ['1', '17', 'F', '57', '63'], ['6', '21', '37', '48', '66'], ['5', '18', '36', '47', '72']]},
    {"id": 195, "cells": [['8', '22', '31', '53', '73'], ['1', '19', '32', '58', '61'], ['11', '27', 'F', '56', '71'], ['10', '24', '40', '47', '68'], ['2', '20', '45', '60', '65']]},
    {"id": 196, "cells": [['4', '16', '38', '49', '74'], ['2', '30', '42', '60', '73'], ['5', '19', 'F', '56', '64'], ['6', '22', '44', '51', '62'], ['8', '25', '39', '54', '70']]},
    {"id": 197, "cells": [['4', '25', '41', '49', '65'], ['5', '24', '39', '51', '61'], ['8', '22', 'F', '54', '73'], ['2', '30', '43', '47', '62'], ['9', '28', '35', '57', '67']]},
    {"id": 198, "cells": [['6', '17', '42', '54', '73'], ['4', '25', '43', '59', '66'], ['5', '30', 'F', '57', '64'], ['13', '29', '45', '58', '67'], ['12', '28', '33', '55', '71']]},
    {"id": 199, "cells": [['10', '29', '40', '57', '61'], ['5', '17', '33', '50', '73'], ['12', '25', 'F', '54', '63'], ['9', '16', '36', '60', '68'], ['2', '21', '31', '59', '71']]},
    {"id": 200, "cells": [['6', '27', '43', '48', '62'], ['2', '26', '45', '54', '70'], ['5', '24', 'F', '47', '74'], ['10', '19', '40', '46', '65'], ['14', '30', '35', '52', '61']]},
    {"id": 201, "cells": [['5', '20', '38', '58', '61'], ['10', '22', '41', '52', '64'], ['2', '19', 'F', '57', '62'], ['12', '23', '36', '51', '63'], ['3', '26', '31', '53', '74']]},
    {"id": 202, "cells": [['9', '22', '36', '60', '69'], ['12', '21', '32', '56', '74'], ['15', '24', 'F', '47', '73'], ['7', '30', '43', '59', '63'], ['1', '16', '33', '52', '67']]},
    {"id": 203, "cells": [['8', '16', '41', '59', '67'], ['6', '26', '34', '58', '65'], ['14', '23', 'F', '57', '62'], ['4', '18', '31', '55', '72'], ['5', '25', '44', '52', '68']]},
    {"id": 204, "cells": [['12', '20', '39', '55', '64'], ['5', '26', '33', '58', '67'], ['6', '17', 'F', '54', '74'], ['3', '29', '40', '57', '71'], ['1', '19', '31', '49', '69']]},
]

# ===================================================================
# ✅ TEMPORARY DUPLICATE CHECK — remove after verifying
# ===================================================================
_seen_cells = {}
_duplicate_ids = []
for _c in BINGO_CARDS:
    _key = str(_c["cells"])
    if _key in _seen_cells:
        _duplicate_ids.append(f"#{_seen_cells[_key]} = #{_c['id']}")
    else:
        _seen_cells[_key] = _c["id"]

if _duplicate_ids:
    st.error(f"⚠️ Duplicate cards: {', '.join(_duplicate_ids)}")
else:
    st.success(f"✅ All cards are unique!")

def get_card(card_id):
    for card in BINGO_CARDS:
        if card["id"] == card_id:
            return card
    return None

def get_card_data(card_id):
    card = get_card(card_id)
    if card:
        return card["cells"]
    return None

# ===================================================================
# WINNER DETECTION
# ===================================================================

def check_winning_pattern(card_data, called_numbers):
    if not called_numbers or not card_data:
        return None
    
    called_set = set(called_numbers)
    
    def is_marked(value):
        if value == 'F':
            return True
        return int(value) in called_set
    
    for row in range(5):
        if all(is_marked(card_data[row][col]) for col in range(5)):
            return {'type': f"Row {row + 1}", 'cells': [card_data[row][col] for col in range(5)]}
    
    for col in range(5):
        if all(is_marked(card_data[row][col]) for row in range(5)):
            letters = ['B', 'I', 'N', 'G', 'O']
            return {'type': f"Column {letters[col]}", 'cells': [card_data[row][col] for row in range(5)]}
    
    if all(is_marked(card_data[i][i]) for i in range(5)):
        return {'type': "Diagonal Main", 'cells': [card_data[i][i] for i in range(5)]}
    if all(is_marked(card_data[i][4 - i]) for i in range(5)):
        return {'type': "Diagonal Anti", 'cells': [card_data[i][4 - i] for i in range(5)]}
    
    large_corners = [card_data[0][0], card_data[0][4], card_data[4][0], card_data[4][4]]
    if all(is_marked(cell) for cell in large_corners):
        return {'type': "Large Corners", 'cells': large_corners}
    
    small_corners = [card_data[1][1], card_data[1][3], card_data[3][1], card_data[3][3]]
    if all(is_marked(cell) for cell in small_corners):
        return {'type': "Small Corners", 'cells': small_corners}
    
    return None

# ===================================================================
# GAME FUNCTIONS
# ===================================================================

def check_for_winners():
    if st.session_state.winner_declared:
        return
    
    called_numbers = list(st.session_state.called_numbers)
    winners_found = []
    
    for card_id in st.session_state.taken_cards:
        card_data = get_card_data(card_id)
        if card_data:
            pattern = check_winning_pattern(card_data, called_numbers)
            if pattern:
                owner = st.session_state.card_owner.get(str(card_id), "Unknown")
                existing_winner = next((w for w in winners_found if w["username"] == owner), None)
                if existing_winner:
                    existing_winner["cards"].append(card_id)
                    existing_winner["patterns"].append(pattern['type'])
                else:
                    winners_found.append({
                        "username": owner,
                        "cards": [card_id],
                        "patterns": [pattern['type']],
                        "card_data": card_data
                    })
    
    if winners_found:
        st.session_state.winners_list = winners_found
        st.session_state.winner_declared = True
        st.session_state.game_over = True
        st.session_state.auto_call_started = False
        st.session_state.celebration_start_time = time.time()
        distribute_prizes(winners_found)
        save_game_state()
        
        save_global_winners(
            winners_found,
            True,
            st.session_state.called_numbers,
            st.session_state.last_called_number,
            st.session_state.auto_called_count,
            True,
            st.session_state.prize_distributed
        )

def distribute_prizes(winners):
    if st.session_state.prize_distributed:
        return
    
    total_cards = len(st.session_state.taken_cards)
    total_prize = total_cards * PRIZE_PER_CARD
    prize_per_winner = total_prize // len(winners) if len(winners) > 0 else 0
    
    for winner in winners:
        username = winner.get("username")
        if username in st.session_state.user_db:
            st.session_state.user_db[username]["balance"] = st.session_state.user_db[username].get("balance", 0) + prize_per_winner
            st.session_state.user_db[username]["wins"] = st.session_state.user_db[username].get("wins", 0) + 1
            st.session_state.user_db[username]["game_played"] = st.session_state.user_db[username].get("game_played", 0) + 1
            save_all_data()
    
    st.session_state.prize_distributed = True
    
    save_global_winners(
        st.session_state.winners_list,
        True,
        st.session_state.called_numbers,
        st.session_state.last_called_number,
        st.session_state.auto_called_count,
        True,
        True
    )

# ===================================================================
# DISPLAY FUNCTIONS
# ===================================================================

def display_selected_card(card_id, called_numbers=None, is_winner=False, winning_pattern=None):
    if not st.session_state.winner_declared:
        sync_global_winners()
    
    if called_numbers is None:
        called_numbers = []
    
    card = get_card(card_id)
    if not card:
        return
    
    cells = card["cells"]
    
    if is_winner:
        border_color = '#FFD700'
        title_color = '#FFD700'
        card_class = 'winner-card'
    else:
        border_color = 'rgba(255,255,255,0.1)'
        title_color = '#FFFFFF'
        card_class = ''
    
    html = f"""
    <div class="{card_class}" style="background:rgba(0,0,0,0.2);border-radius:15px;padding:12px;margin:8px auto;box-shadow:0 4px 12px rgba(0,0,0,0.3);max-width:400px;border:2px solid {border_color};transition:all 0.3s ease;{'animation:winnerPulse 1s ease-in-out infinite alternate;' if is_winner else ''}">
        <div style="text-align:center;color:{title_color};font-size:1rem;font-weight:bold;margin-bottom:8px;text-shadow:0 0 20px rgba(255,215,0,0.1);">
            {'🎊🏆 ' if is_winner else '🎯'} Card #{card_id} { ' 🏆🎊' if is_winner else ''}
        </div>
        <table style="width:100%;border-collapse:collapse;">
            <tr>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:4px 2px;text-align:center;min-width:30px;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.75rem;">B</td>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:4px 2px;text-align:center;min-width:30px;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.75rem;">I</td>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:4px 2px;text-align:center;min-width:30px;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.75rem;">N</td>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:4px 2px;text-align:center;min-width:30px;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.75rem;">G</td>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:4px 2px;text-align:center;min-width:30px;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.75rem;">O</td>
            </tr>
    """
    
    for row_idx in range(5):
        html += '<tr>'
        for col_idx in range(5):
            value = cells[row_idx][col_idx]
            
            if value == 'F':
                html += f'<td style="border:1px solid rgba(255,255,255,0.08);padding:4px 2px;text-align:center;"><div style="display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;background:rgba(255,215,0,0.15);color:#FFD700;font-size:1.1rem;border:2px solid #FFD700;">★</div></td>'
            else:
                num = int(value)
                is_called = num in called_numbers
                style = ''
                if is_called and is_winner:
                    style = 'background:rgba(255,215,0,0.3);color:#FFD700;border-color:#FFD700;animation:winnerPulse 1s ease-in-out infinite alternate;'
                elif is_called:
                    style = 'background:rgba(255,152,0,0.2);color:#FFD700;border-color:#FF9800;transform:scale(1.05);'
                else:
                    style = 'background:rgba(255,255,255,0.05);color:#FFFFFF;border-color:rgba(255,255,255,0.06);'
                
                html += f'<td style="border:1px solid rgba(255,255,255,0.08);padding:4px 2px;text-align:center;"><div style="display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;{style}font-weight:bold;font-size:0.8rem;border:2px solid;">{value}</div></td>'
        html += '</tr>'
    
    html += '</table>'
    
    total_called = sum(1 for row in cells for val in row if val != 'F' and int(val) in called_numbers)
    
    if is_winner and winning_pattern:
        html += f'<div style="text-align:center;color:#FFD700;font-size:0.9rem;margin-top:6px;font-weight:bold;text-shadow:0 0 30px rgba(255,215,0,0.3);">🎉🏆 WINNER! ({winning_pattern}) 🏆🎉</div>'
        html += f'<div style="text-align:center;color:#FFD700;font-size:0.7rem;margin-top:2px;">🎊🍀 እንኳን ደስ አለዎት!!!🍀🎊</div>'
    else:
        html += f'<div style="text-align:center;color:rgba(255,255,255,0.4);font-size:0.65rem;margin-top:4px;">✅ {total_called}/24 called</div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

def display_master_board():
    if not st.session_state.winner_declared:
        sync_global_winners()
    
    master_board = {
        'B': list(range(1, 16)),
        'I': list(range(16, 31)),
        'N': list(range(31, 46)),
        'G': list(range(46, 61)),
        'O': list(range(61, 76))
    }
    
    called_numbers = list(st.session_state.called_numbers)
    
    html = '''
    <style>
        .board-container {
            max-width: 950px;
            margin: 0 auto;
            padding: 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.08);
        }
        .board-title {
            text-align: center;
            font-size: 1.8rem;
            font-weight: bold;
            color: #FFD700;
            margin-bottom: 12px;
            text-shadow: 0 0 30px rgba(255,215,0,0.1);
        }
        .board-table {
            width: 100%;
            border-collapse: collapse;
        }
        .board-table td {
            border: 1px solid rgba(255,255,255,0.08);
            padding: 6px 4px;
            text-align: center;
            font-size: 0.85rem;
            font-weight: bold;
            min-width: 30px;
        }
        .board-table .header-cell {
            background: linear-gradient(135deg, rgba(46,125,50,0.2), rgba(27,94,32,0.1));
            color: #FFD700;
            font-size: 1.5rem;
            font-weight: 900;
            padding: 10px 4px;
            text-align: center;
            border: 1px solid rgba(255,215,0,0.1);
            letter-spacing: 3px;
        }
        .board-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: rgba(255,255,255,0.05);
            color: #FFFFFF;
            font-weight: bold;
            font-size: 0.8rem;
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.3s ease;
        }
        .board-number.called {
            background: rgba(255, 152, 0, 0.2);
            color: #FFD700;
            border-color: #FF9800;
            transform: scale(1.08);
            box-shadow: 0 0 15px rgba(255,152,0,0.15);
        }
        .board-number.last-called {
            background: rgba(229, 57, 53, 0.2);
            color: #FF6B6B;
            border-color: #E53935;
            transform: scale(1.15);
            animation: lastPulse 0.5s ease-in-out;
            box-shadow: 0 0 20px rgba(229,57,53,0.2);
        }
        @keyframes lastPulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.25); }
            100% { transform: scale(1.15); }
        }
        .board-stats {
            text-align: center;
            margin-top: 12px;
            font-size: 0.9rem;
            color: rgba(255,255,255,0.5);
            padding: 8px;
            background: rgba(0,0,0,0.15);
            border-radius: 8px;
        }
        .board-stats strong {
            color: #FFD700;
        }
        @media (max-width: 600px) {
            .board-table td { padding: 3px 2px; font-size: 0.7rem; min-width: 22px; }
            .board-number { width: 26px; height: 26px; font-size: 0.7rem; }
            .board-table .header-cell { font-size: 1.1rem; padding: 6px 2px; }
        }
    </style>
    <div class="board-container">
        <div class="board-title">🎯 BINGO Board</div>
    '''
    
    if st.session_state.last_called_number:
        letter = get_letter_for_number(st.session_state.last_called_number)
        amharic = get_amharic_number(st.session_state.last_called_number)
        html += f'<div style="text-align:center;font-size:1.1rem;font-weight:bold;color:#FF6B6B;margin-bottom:8px;">🎯 Last Called: <span style="background:rgba(229,57,53,0.15);color:#FF6B6B;padding:3px 15px;border-radius:15px;border:1px solid rgba(229,57,53,0.2);">{st.session_state.last_called_number} ({letter}) - {amharic}</span></div>'
    
    html += '<table class="board-table"><tr>'
    for letter in ['B', 'I', 'N', 'G', 'O']:
        html += f'<td class="header-cell">{letter}</td>'
    html += '</tr>'
    
    for row in range(15):
        html += '<tr>'
        for letter in ['B', 'I', 'N', 'G', 'O']:
            num = master_board[letter][row]
            is_called = num in called_numbers
            is_last = num == st.session_state.last_called_number
            
            if is_last:
                html += f'<td><div class="board-number last-called">{num}</div></td>'
            elif is_called:
                html += f'<td><div class="board-number called">{num}</div></td>'
            else:
                html += f'<td><div class="board-number">{num}</div></td>'
        html += '</tr>'
    
    html += '</table>'
    html += f'<div class="board-stats">📊 Called: <strong>{len(called_numbers)}</strong> / 75 numbers</div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ===================================================================
# CARD SELECTION FUNCTION - REAL st.button (NO URL BROWSING)
# ===================================================================

def render_card_selection():
    """Render card selection using real st.button widgets — no URL browsing."""

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

    if st.session_state.current_role == "admin":
        st.warning("⚠️ Admin cannot play the game. Please login as a player to select cards.")
        st.info("💡 Admin can only manage user balances and monitor the game.")
        total_selected = len(st.session_state.taken_cards)
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.2);border:1px solid rgba(255,215,0,0.1);border-radius:12px;padding:15px;margin:10px 0;">
            <h4 style="color:#FFD700;text-align:center;">📊 Game Status</h4>
            <p style="color:rgba(255,255,255,0.8);text-align:center;">
                Total Cards Selected: <strong style="color:#FFD700;">{total_selected}/204</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    if st.session_state.flash_msg:
        st.warning(st.session_state.flash_msg)
        st.session_state.flash_msg = ""

    remaining = st.session_state.card_selection_time
    game_started = st.session_state.game_started

    if game_started:
        st.rerun()
        return

    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    time_str = f"{minutes:01d}:{seconds:02d}"

    user = st.session_state.user_db.get(st.session_state.current_user, {})
    balance = user.get("balance", 0)

    file_taken, _, _, _ = load_global_cards()
    total_selected = max(len(file_taken), len(st.session_state.clicked_numbers))
    your_cards = len(st.session_state.clicked_numbers)
    available = 204 - total_selected
    min_cards_required = 3
    enough_cards = total_selected >= min_cards_required

    if not enough_cards:
        color = "#FF9800"
    elif remaining <= 10:
        color = "#E53935"
    elif remaining <= 30:
        color = "#FF9800"
    else:
        color = "#FFD700"

    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.15);padding:12px 15px;border-radius:12px;border:1px solid rgba(255,255,255,0.08);margin-bottom:15px;text-align:center;">
        <div style="font-size:1.6rem;font-weight:bold;color:{color};font-family:monospace;margin-bottom:6px;">
            ⌚ {time_str}
        </div>
        <div style="font-size:0.9rem;color:#FFFFFF;line-height:1.9;">
            🟢 <b>Your Cards:</b> {your_cards}/2 &nbsp;|&nbsp;
            📊 <b>Global:</b> {total_selected}/204 &nbsp;|&nbsp;
            ⬜ <b>Available:</b> {available}
        </div>
        <div style="font-size:1rem;color:#FFD700;margin-top:6px;font-weight:bold;">
            💰 {balance:.2f} ETB
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not enough_cards:
        st.warning(f"⚠️ Waiting for {min_cards_required - total_selected} more card(s). Game will start when time hits 0:00 AND 3+ cards are selected! 🎯")
    else:
        st.success(f"✅ 3+ cards ready! Game will start when the timer hits 0:00 — {int(remaining)}s remaining 🎯")

    col_options = [4, 5, 6, 7, 8]
    current_value = st.session_state.columns_per_row if st.session_state.columns_per_row in col_options else 6

    selected_cols = st.selectbox(
        f"📊 Cards per row (your view — current: {current_value})",
        options=col_options,
        index=col_options.index(current_value),
        key=f"cards_per_row_select_{st.session_state.current_user}"
    )

    if selected_cols != st.session_state.columns_per_row:
        st.session_state.columns_per_row = selected_cols
        st.rerun()

    cols_per_row = st.session_state.columns_per_row
    clicked = st.session_state.clicked_numbers
    taken = st.session_state.taken_cards
    rejected = st.session_state.rejected_card_num

    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.15);border-radius:12px;padding:8px;border:1px solid rgba(255,255,255,0.08);margin-bottom:8px;">
        <div style="text-align:center;font-size:0.9rem;color:#FFD700;font-weight:bold;">
            🎯 Tap a card to SELECT (10 ETB) or 🟢 green to DESELECT
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ✅ Real st.button grid — forced horizontal on mobile via CSS
    for row_start in range(1, 205, cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            card_num = row_start + col_idx
            if card_num > 204:
                break

            is_mine = card_num in clicked
            is_taken = card_num in taken and not is_mine
            is_rejected = (rejected == card_num) and not is_mine and not is_taken

            with cols[col_idx]:
                if is_mine:
                    # Deselect button — green
                    if st.button(
                        f"✅{card_num}",
                        key=f"card_btn_{card_num}",
                        use_container_width=True,
                        type="primary",
                    ):
                        user_balance = st.session_state.user_db.get(
                            st.session_state.current_user, {}
                        ).get("balance", 0)

                        st.session_state.clicked_numbers.discard(card_num)
                        if card_num in st.session_state.taken_cards:
                            st.session_state.taken_cards.remove(card_num)
                        if str(card_num) in st.session_state.card_owner:
                            del st.session_state.card_owner[str(card_num)]

                        st.session_state.user_db[st.session_state.current_user]["balance"] = user_balance + 10
                        save_all_data()
                        save_global_cards(
                            st.session_state.taken_cards,
                            st.session_state.card_owner,
                            st.session_state.timer_start_time,
                            st.session_state.card_selection_time
                        )
                        # ✅ Clear any rejected-card highlight when a card is deselected
                        st.session_state.rejected_card_num = None
                        st.session_state.flash_msg = f"✅ Card #{card_num} refunded. +10 ETB"
                        st.rerun()

                elif is_taken:
                    # Disabled button — taken by someone else
                    st.button(
                        f"🔴{card_num}",
                        key=f"card_btn_{card_num}",
                        use_container_width=True,
                        disabled=True,
                    )

                elif is_rejected:
                    # ✅ This is the specific card the player tried to select 3rd time.
                    # Show the warning message on the button itself.
                    if st.button(
                        "🚫 2+ አይቻልም 🚫",
                        key=f"card_btn_{card_num}",
                        use_container_width=True,
                    ):
                        # Clicking it again just dismisses the message
                        st.session_state.rejected_card_num = None
                        st.rerun()

                else:
                    # Available — yellow/gold
                    if st.button(
                        f"🟡{card_num}",
                        key=f"card_btn_{card_num}",
                        use_container_width=True,
                    ):
                        user_balance = st.session_state.user_db.get(
                            st.session_state.current_user, {}
                        ).get("balance", 0)
                        has_max = len(st.session_state.clicked_numbers) >= MAX_CARDS_PER_PLAYER

                        if has_max:
                            # ✅ Store the rejected card number so we render the message on that card
                            st.session_state.rejected_card_num = card_num
                            st.session_state.flash_msg = ""
                        elif user_balance < 10:
                            st.session_state.flash_msg = "💰 ሂሳብዎን ይሙሉ! 💰"
                            st.session_state.rejected_card_num = None
                        else:
                            st.session_state.user_db[st.session_state.current_user]["balance"] = user_balance - 10
                            save_all_data()

                            st.session_state.clicked_numbers.add(card_num)
                            if card_num not in st.session_state.taken_cards:
                                st.session_state.taken_cards.append(card_num)
                            st.session_state.card_owner[str(card_num)] = st.session_state.current_user

                            save_global_cards(
                                st.session_state.taken_cards,
                                st.session_state.card_owner,
                                st.session_state.timer_start_time,
                                st.session_state.card_selection_time
                            )
                            st.session_state.rejected_card_num = None
                            st.session_state.flash_msg = f"✅ Card #{card_num} selected! -10 ETB"
                        st.rerun()

    st.markdown(f"""
    <div style="text-align:center;font-size:0.8rem;color:rgba(255,255,255,0.6);margin:8px 0;">
        🟡 Gold = Available &nbsp;|&nbsp; 🟢 Green = Yours &nbsp;|&nbsp; 🔴 Red = Taken by others
    </div>
    """, unsafe_allow_html=True)

    progress = 1 - (remaining / 60) if remaining > 0 else 1
    st.progress(progress)

    if enough_cards:
        st.caption(f"✅ {total_selected} cards selected globally. Starting in {int(remaining)}s... 🎯")
    else:
        st.caption(f"⏸️ Need {min_cards_required - total_selected} more card(s) to start. Timer keeps running... 🃏")

# ===================================================================
# MAIN APP
# ===================================================================

quote = get_random_quote()
st.markdown(f"""
<div class="motivation-box">
    <div class="quote">"{quote['am']}"</div>
    <div class="author">{quote['en']} — {quote['author']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:10px 0;margin-bottom:10px;">
    🎯🍀 <h1 style="font-family:'Orbitron',sans-serif;font-weight:900;font-size:2.2rem;background:linear-gradient(135deg,#FFD700,#FFA500,#FFD700);background-size:300% 300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3s ease-in-out infinite;letter-spacing:6px;margin:0;text-shadow:0 0 40px rgba(255,215,0,0.1);">
        ደራሽ ቢንጎ -Derash BINGO 
    </h1>
    <p style="color:rgba(255,255,255,0.6);font-size:0.9rem;letter-spacing:3px;margin-top:-3px;">
    @2026 
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
                        st.success("🎉🎊🥳 በትክክል ተመዝግበዋል! 🥳🎊🎉")
                        st.balloons()
                        st.snow()
                        st.info("💡 Your balance starts at 0.00 ETB. Admin can add balance.")
                        load_all_data()
                        time.sleep(2)
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

if st.session_state.current_user == "admin":
    balance = 0.0
    if "admin" in st.session_state.user_db:
        st.session_state.user_db["admin"]["balance"] = 0.0
        save_all_data()

st.sidebar.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(255,215,0,0.08),rgba(255,165,0,0.03));padding:1rem;border-radius:12px;border:1px solid rgba(255,215,0,0.1);margin-bottom:15px;">
    <p style="margin:0;font-weight:600;color:#FFD700;">👤 {user.get('name', st.session_state.current_user)}</p>
    <p style="margin:3px 0;color:rgba(255,255,255,0.4);font-size:0.7rem;">📱 {user.get('phone', 'No phone')}</p>
    <p style="margin:5px 0;font-size:1.1rem;font-weight:bold;color:#FFD700;">💰 {balance:.2f} ETB</p>
    <p style="margin:3px 0;color:rgba(255,255,255,0.3);font-size:0.7rem;">⭐ {st.session_state.current_role.title() if st.session_state.current_role else 'Player'} | 🏆 {user.get('wins', 0)} wins</p>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout", use_container_width=True):
    logout_user()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(f"📋 Selected: {len(st.session_state.clicked_numbers)}/2 cards")

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
# ===================================================================

if st.session_state.game_started:
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
