import streamlit as st
import random
import time
import hashlib
import json
import os
from datetime import datetime, timedelta

st.set_page_config(
    page_title="ደራሽ ቢንጎ",
    page_icon="🎯",
    layout="wide"
)

# ===================================================================
# CUSTOM CSS FOR LIGHT BACKGROUND AND STYLING
# ===================================================================

st.markdown("""
<style>
    /* Light Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa, #e8edf5, #dce3ef);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main content background */
    .main-content {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Glass morphism effect */
    .glass-container {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
    }
    
    /* Motivational quotes */
    .motivation-box {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.08), rgba(255, 165, 0, 0.05));
        border-left: 4px solid #FFD700;
        padding: 12px 18px;
        border-radius: 10px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.6);
    }
    .motivation-box .quote {
        font-size: 1rem;
        color: #1a1a2e;
        font-style: italic;
        font-family: 'Noto Sans Ethiopic', Arial, sans-serif;
    }
    .motivation-box .author {
        color: rgba(0,0,0,0.5);
        font-size: 0.8rem;
        margin-top: 3px;
    }
    
    /* Card selection grid */
    .cards-grid-container {
        max-height: 450px;
        overflow-y: auto;
        padding: 5px;
        margin: 5px 0;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        border: 1px solid rgba(0, 0, 0, 0.08);
    }
    .cards-grid-container::-webkit-scrollbar {
        width: 4px;
    }
    .cards-grid-container::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.05);
        border-radius: 10px;
    }
    .cards-grid-container::-webkit-scrollbar-thumb {
        background: #FFD700;
        border-radius: 10px;
    }
    
    .cards-grid {
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        gap: 3px;
        max-width: 100%;
        margin: 0 auto;
    }
    
    /* Mobile portrait - still 10 columns */
    @media (max-width: 768px) and (orientation: portrait) {
        .cards-grid {
            grid-template-columns: repeat(10, 1fr) !important;
            gap: 2px !important;
        }
        .card-btn {
            font-size: 0.5rem !important;
            min-height: 20px !important;
            height: 20px !important;
            padding: 2px 1px !important;
        }
        .cards-grid-container {
            max-height: 350px !important;
        }
    }
    
    @media (max-width: 480px) and (orientation: portrait) {
        .cards-grid {
            grid-template-columns: repeat(10, 1fr) !important;
            gap: 1.5px !important;
        }
        .card-btn {
            font-size: 0.4rem !important;
            min-height: 16px !important;
            height: 16px !important;
            padding: 1px 1px !important;
            border-radius: 3px !important;
        }
        .cards-grid-container {
            max-height: 300px !important;
        }
    }
    
    @media (max-width: 360px) and (orientation: portrait) {
        .cards-grid {
            grid-template-columns: repeat(10, 1fr) !important;
            gap: 1px !important;
        }
        .card-btn {
            font-size: 0.35rem !important;
            min-height: 14px !important;
            height: 14px !important;
            padding: 1px 0px !important;
            border-radius: 2px !important;
        }
        .card-btn .card-price {
            display: none !important;
        }
        .cards-grid-container {
            max-height: 250px !important;
        }
    }
    
    @media (orientation: landscape) {
        .cards-grid {
            grid-template-columns: repeat(10, 1fr) !important;
            gap: 3px !important;
        }
        .card-btn {
            font-size: 0.55rem !important;
            min-height: 22px !important;
            height: 22px !important;
            padding: 2px 2px !important;
        }
        .cards-grid-container {
            max-height: 350px !important;
        }
    }
    
    /* Card buttons - Light theme */
    .card-btn {
        width: 100% !important;
        padding: 3px 2px !important;
        font-size: 0.6rem !important;
        min-height: 24px !important;
        height: 24px !important;
        line-height: 1 !important;
        border-radius: 4px !important;
        margin: 1px 0 !important;
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: bold !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        background: #ffffff !important;
        color: #1a1a2e !important;
        overflow: hidden !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
        position: relative !important;
    }
    .card-btn:hover {
        transform: scale(1.05);
        border-color: #FFD700 !important;
        background: #fffde7 !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.15) !important;
    }
    .card-btn.selected {
        border-color: #FFD700 !important;
        background: #fff8e1 !important;
        color: #1a1a2e !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2) !important;
    }
    .card-btn.selected .tick-mark {
        display: inline !important;
    }
    .card-btn.taken {
        border-color: rgba(255, 0, 0, 0.2) !important;
        background: #f5f5f5 !important;
        color: #999 !important;
        cursor: not-allowed !important;
        opacity: 0.5 !important;
    }
    .card-btn.taken:hover {
        transform: none !important;
        border-color: rgba(255, 0, 0, 0.2) !important;
        background: #f5f5f5 !important;
        box-shadow: none !important;
    }
    .card-btn .tick-mark {
        display: none;
        position: absolute;
        top: -2px;
        right: -2px;
        font-size: 0.5rem;
        color: #4CAF50;
        background: #ffffff;
        border-radius: 50%;
        padding: 1px 3px;
        border: 1px solid #4CAF50;
        line-height: 1;
    }
    .card-btn .card-price {
        font-size: 0.4rem !important;
        opacity: 0.6;
        margin-top: 1px;
        line-height: 1;
        color: #666;
    }
    
    /* Override Streamlit button styles for card grid */
    .cards-grid .stButton {
        padding: 0 !important;
        margin: 0 !important;
        min-width: 0 !important;
    }
    .cards-grid .stButton button {
        width: 100% !important;
        padding: 3px 2px !important;
        font-size: 0.6rem !important;
        min-height: 24px !important;
        height: 24px !important;
        line-height: 1 !important;
        border-radius: 4px !important;
        margin: 0 !important;
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: bold !important;
        transition: all 0.2s ease !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        background: #ffffff !important;
        color: #1a1a2e !important;
        box-shadow: none !important;
        font-family: Arial, sans-serif !important;
        overflow: hidden !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
        position: relative !important;
    }
    .cards-grid .stButton button:hover {
        transform: scale(1.05);
        border-color: #FFD700 !important;
        background: #fffde7 !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.15) !important;
    }
    .cards-grid .stButton button[kind="secondary"] {
        border-color: #FFD700 !important;
        background: #fff8e1 !important;
        color: #1a1a2e !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2) !important;
    }
    .cards-grid .stButton button:disabled {
        border-color: rgba(255, 0, 0, 0.2) !important;
        background: #f5f5f5 !important;
        color: #999 !important;
        cursor: not-allowed !important;
        opacity: 0.5 !important;
    }
    .cards-grid .stButton button:disabled:hover {
        transform: none !important;
        border-color: rgba(255, 0, 0, 0.2) !important;
        background: #f5f5f5 !important;
        box-shadow: none !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.05);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #FFD700, #FFA500);
        border-radius: 10px;
    }
    
    /* Text colors for light theme */
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: #1a1a2e !important;
    }
    
    .stInfo, .stSuccess, .stWarning, .stError {
        background: rgba(255, 255, 255, 0.8) !important;
        color: #1a1a2e !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
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
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    /* Timer display */
    .header-timer-container {
        background: rgba(255, 255, 255, 0.8) !important;
        border: 2px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 15px;
        padding: 10px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    .timer-display {
        color: #1a1a2e !important;
        font-weight: bold;
    }
    .timer-label {
        color: #666 !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header {
            flex-direction: column !important;
            align-items: center !important;
            text-align: center !important;
        }
        .logo-text h1 {
            font-size: 1.5rem !important;
            color: #1a1a2e !important;
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
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* BINGO Board */
    .board-container {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    }
    .board-title {
        color: #1a1a2e !important;
    }
    .board-number {
        color: #1a1a2e !important;
        background: rgba(0, 0, 0, 0.03) !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
    }
    .board-number.called {
        background: rgba(255, 152, 0, 0.2) !important;
        color: #E65100 !important;
        border-color: #FF9800 !important;
    }
    .board-number.last-called {
        background: rgba(229, 57, 53, 0.15) !important;
        color: #C62828 !important;
        border-color: #E53935 !important;
    }
    
    /* Called numbers */
    .called-numbers-container {
        background: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        border-radius: 15px !important;
        padding: 15px !important;
    }
    .called-numbers-header {
        color: #1a1a2e !important;
    }
    
    /* Game status */
    .game-status {
        background: rgba(255, 255, 255, 0.8) !important;
        border-left: 4px solid #FFD700 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin-top: 15px !important;
    }
    .status-message {
        color: #1a1a2e !important;
    }
    
    /* Game state indicator */
    .game-state-indicator {
        background: rgba(255, 255, 255, 0.8) !important;
        border: 2px solid rgba(0, 0, 0, 0.1) !important;
        color: #1a1a2e !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        text-align: center !important;
        font-weight: bold !important;
    }
    .game-state-waiting { border-color: #FF9800 !important; color: #E65100 !important; }
    .game-state-running { border-color: #4CAF50 !important; color: #2E7D32 !important; }
    .game-state-finished { border-color: #FFD700 !important; color: #F57F17 !important; }
    
    /* Stat boxes */
    .stat-box {
        background: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
    }
    .stat-value {
        color: #1a1a2e !important;
        font-weight: bold !important;
    }
    .stat-label {
        color: #666 !important;
    }
    
    /* Buttons */
    .btn-primary {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #1a1a2e !important;
        border: none !important;
    }
    .btn-success {
        background: linear-gradient(135deg, #4CAF50, #2E7D32) !important;
        color: white !important;
        border: none !important;
    }
    
    /* Winner celebration text */
    .winner-name {
        color: #1a1a2e !important;
    }
    .winner-prize {
        color: #2E7D32 !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# AUDIO FUNCTIONS - Web Audio API for sound effects
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
                const notes = [523, 659, 784, 1047];
                notes.forEach((freq, index) => {
                    const oscillator = audioCtx.createOscillator();
                    const gainNode = audioCtx.createGain();
                    oscillator.type = 'sine';
                    oscillator.frequency.value = freq;
                    gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime + index * 0.15);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + index * 0.15 + 0.2);
                    oscillator.connect(gainNode);
                    gainNode.connect(audioCtx.destination);
                    oscillator.start(audioCtx.currentTime + index * 0.15);
                    oscillator.stop(audioCtx.currentTime + index * 0.15 + 0.2);
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

init_session_state()

# ===================================================================
# GAME CONSTANTS
# ===================================================================

CARD_PRICE = 10
PRIZE_PER_CARD = 8

# ===================================================================
# MOTIVATIONAL QUOTES
# ===================================================================

MOTIVATIONAL_QUOTES = [
    {"am": "የቢንጎ ጨዋታ ዕድል እና ተስፋ ነው! 🎯", "en": "BINGO is a game of luck and hope!", "author": "ደራሽ ቢንጎ"},
    {"am": "እያንዳንዱ ቁጥር ወደ ድል አንድ እርምጃ ነው! 💪", "en": "Every number is a step closer to victory!", "author": "ደራሽ ቢንጎ"},
    {"am": "ቢንጎ! ማለት ድል ማለት ነው! 🏆", "en": "BINGO means victory!", "author": "ደራሽ ቢንጎ"},
    {"am": "በትዕግስት እና በእምነት ያሸንፉ! 🌟", "en": "Win with patience and faith!", "author": "ደራሽ ቢንጎ"},
    {"am": "ዕድላችሁ ይምራላችሁ! 🍀", "en": "May luck be on your side!", "author": "ደራሽ ቢንጎ"},
    {"am": "አንድ ቁጥር ሕይወትን ይለውጣል! ✨", "en": "One number can change everything!", "author": "ደራሽ ቢንጎ"},
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
                "balance": 0,
                "role": "admin",
                "name": "Admin",
                "phone": "",
                "game_played": 0,
                "wins": 0
            }
            st.session_state.user_db[username] = user_data
            save_local_users(st.session_state.user_db)
            load_all_data()
        
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.current_role = "admin"
        return True, "✅ Admin login successful!"
    
    if username not in st.session_state.user_db:
        return False, "❌ Username not found"
    
    if verify_password(password, st.session_state.user_db[username]["password"]):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.current_role = st.session_state.user_db[username]["role"]
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
        "balance": 0,
        "role": "player",
        "name": name,
        "phone": phone,
        "game_played": 0,
        "wins": 0
    }
    
    st.session_state.user_db[username] = user_data
    save_local_users(st.session_state.user_db)
    load_all_data()
    
    return True, "✅ Registration successful!"

def logout_user():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_role = None

# ===================================================================
# ADMIN PANEL
# ===================================================================

def admin_panel():
    """Admin panel for managing user balances"""
    st.markdown("""
    <div class="glass-container">
        <h3 style="color:#1a1a2e;text-align:center;">🔧 Admin Panel</h3>
        <p style="color:#666;text-align:center;">Manage user balances, view all users.</p>
    </div>
    """, unsafe_allow_html=True)
    
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
            <p style="margin:0;font-weight:600;color:#1a1a2e;">👤 {name}</p>
            <p style="margin:5px 0;color:#666;font-size:0.85rem;">📱 <strong style="color:#E65100;">{phone if phone else 'Not provided'}</strong></p>
            <p style="margin:5px 0;color:#666;font-size:0.85rem;">👤 Username: <strong style="color:#E65100;">{selected_user}</strong></p>
            <p style="margin:5px 0;font-size:1.2rem;font-weight:bold;color:#2E7D32;">💰 Current Balance: {current_balance} ETB</p>
            <p style="margin:5px 0;color:#666;font-size:0.85rem;">🎮 Games Played: {game_played}</p>
            <p style="margin:5px 0;color:#666;font-size:0.85rem;">🏆 Wins: {wins}</p>
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
                    if st.button(f"{amount}", key=f"bal_{amount}_{selected_user}"):
                        if selected_user in st.session_state.user_db:
                            st.session_state.user_db[selected_user]["balance"] = st.session_state.user_db[selected_user].get("balance", 0) + amount
                            save_local_users(st.session_state.user_db)
                            st.success(f"✅ Added {amount} ETB to {selected_user}'s balance!")
                            st.rerun()
        
        with col2:
            if st.button("➕ Add Balance", type="primary", use_container_width=True):
                if selected_user in st.session_state.user_db:
                    st.session_state.user_db[selected_user]["balance"] = st.session_state.user_db[selected_user].get("balance", 0) + custom_amount
                    save_local_users(st.session_state.user_db)
                    st.success(f"✅ Added {custom_amount} ETB to {selected_user}'s balance!")
                    st.rerun()
            
            if st.button("💰 Set Balance", type="primary", use_container_width=True):
                if selected_user in st.session_state.user_db:
                    st.session_state.user_db[selected_user]["balance"] = custom_amount
                    save_local_users(st.session_state.user_db)
                    st.success(f"✅ Set {selected_user}'s balance to {custom_amount} ETB!")
                    st.rerun()
        
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
# ALL 201 BINGO CARDS - FULL LIST (abbreviated for space)
# ===================================================================

BINGO_CARDS = [
    {"id": 1, "cells": [['15', '16', '39', '59', '66'], ['11', '28', '40', '51', '68'], ['12', '20', 'F', '56', '67'], ['3', '30', '35', '60', '72'], ['10', '24', '37', '53', '64']]},
    # ... (all 201 cards - keep your existing list)
    {"id": 201, "cells": [['5', '20', '38', '58', '61'], ['10', '22', '41', '52', '64'], ['2', '19', 'F', '57', '62'], ['12', '23', '36', '51', '63'], ['3', '26', '31', '53', '74']]},
]

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
# ENHANCED WINNER DETECTION
# ===================================================================

def check_winning_pattern(card_data, called_numbers):
    """Check rows, columns, diagonals, and corners"""
    if not called_numbers or not card_data:
        return None
    
    called_set = set(called_numbers)
    
    def is_marked(value):
        if value == 'F':
            return True
        return int(value) in called_set
    
    # Check rows
    for row in range(5):
        if all(is_marked(card_data[row][col]) for col in range(5)):
            return {'type': f"Row {row + 1}", 'cells': [card_data[row][col] for col in range(5)]}
    
    # Check columns
    for col in range(5):
        if all(is_marked(card_data[row][col]) for row in range(5)):
            letters = ['B', 'I', 'N', 'G', 'O']
            return {'type': f"Column {letters[col]}", 'cells': [card_data[row][col] for row in range(5)]}
    
    # Check diagonals
    if all(is_marked(card_data[i][i]) for i in range(5)):
        return {'type': "Diagonal Main", 'cells': [card_data[i][i] for i in range(5)]}
    if all(is_marked(card_data[i][4 - i]) for i in range(5)):
        return {'type': "Diagonal Anti", 'cells': [card_data[i][4 - i] for i in range(5)]}
    
    # Check larger corners
    large_corners = [card_data[0][0], card_data[0][4], card_data[4][0], card_data[4][4]]
    if all(is_marked(cell) for cell in large_corners):
        return {'type': "Large Corners", 'cells': large_corners}
    
    # Check smaller corners
    small_corners = [card_data[1][1], card_data[1][3], card_data[3][1], card_data[3][3]]
    if all(is_marked(cell) for cell in small_corners):
        return {'type': "Small Corners", 'cells': small_corners}
    
    return None

# ===================================================================
# GAME FUNCTIONS
# ===================================================================

def check_for_winners():
    """Check all selected cards for winning patterns"""
    if st.session_state.winner_declared:
        return
    
    called_numbers = list(st.session_state.called_numbers)
    winners_found = []
    
    for card_id in st.session_state.clicked_numbers:
        card_data = get_card_data(card_id)
        if card_data:
            pattern = check_winning_pattern(card_data, called_numbers)
            if pattern:
                winners_found.append({
                    "card_id": card_id,
                    "username": st.session_state.current_user,
                    "pattern": pattern,
                    "card_data": card_data
                })
    
    if winners_found:
        st.session_state.winners_list = winners_found
        st.session_state.winner_declared = True
        st.session_state.game_over = True
        distribute_prizes(winners_found)

def distribute_prizes(winners):
    """Distribute prizes to winners"""
    if st.session_state.prize_distributed:
        return
    
    total_prize = len(st.session_state.clicked_numbers) * PRIZE_PER_CARD
    prize_per_winner = total_prize // len(winners) if len(winners) > 0 else 0
    
    for winner in winners:
        username = winner.get("username")
        if username in st.session_state.user_db:
            st.session_state.user_db[username]["balance"] = st.session_state.user_db[username].get("balance", 0) + prize_per_winner
            st.session_state.user_db[username]["wins"] = st.session_state.user_db[username].get("wins", 0) + 1
            st.session_state.user_db[username]["game_played"] = st.session_state.user_db[username].get("game_played", 0) + 1
            save_all_data()
    
    st.session_state.prize_distributed = True

# ===================================================================
# DISPLAY FUNCTIONS
# ===================================================================

def display_selected_card(card_id, called_numbers=None, is_winner=False, winning_pattern=None):
    """Display a BINGO card"""
    if called_numbers is None:
        called_numbers = []
    
    card = get_card(card_id)
    if not card:
        return
    
    cells = card["cells"]
    
    border_color = '#FFD700' if is_winner else 'rgba(0,0,0,0.1)'
    title_color = '#1a1a2e' if is_winner else '#1a1a2e'
    
    html = f"""
    <div style="background:rgba(255,255,255,0.9);border-radius:15px;padding:12px;margin:8px auto;box-shadow:0 4px 12px rgba(0,0,0,0.05);max-width:400px;border:2px solid {border_color};transition:all 0.3s ease;{'animation:winnerPulse 1s ease-in-out infinite alternate;' if is_winner else ''}">
        <div style="text-align:center;color:{title_color};font-size:1rem;font-weight:bold;margin-bottom:8px;">🎯 Card #{card_id}</div>
        <table style="width:100%;border-collapse:collapse;">
            <tr>
                <td style="border:1px solid rgba(0,0,0,0.08);padding:4px 2px;text-align:center;min-width:30px;background:rgba(46,125,50,0.1);color:#1a1a2e;font-weight:bold;font-size:0.75rem;">B</td>
                <td style="border:1px solid rgba(0,0,0,0.08);padding:4px 2px;text-align:center;min-width:30px;background:rgba(46,125,50,0.1);color:#1a1a2e;font-weight:bold;font-size:0.75rem;">I</td>
                <td style="border:1px solid rgba(0,0,0,0.08);padding:4px 2px;text-align:center;min-width:30px;background:rgba(46,125,50,0.1);color:#1a1a2e;font-weight:bold;font-size:0.75rem;">N</td>
                <td style="border:1px solid rgba(0,0,0,0.08);padding:4px 2px;text-align:center;min-width:30px;background:rgba(46,125,50,0.1);color:#1a1a2e;font-weight:bold;font-size:0.75rem;">G</td>
                <td style="border:1px solid rgba(0,0,0,0.08);padding:4px 2px;text-align:center;min-width:30px;background:rgba(46,125,50,0.1);color:#1a1a2e;font-weight:bold;font-size:0.75rem;">O</td>
            </tr>
    """
    
    for row_idx in range(5):
        html += '<tr>'
        for col_idx in range(5):
            value = cells[row_idx][col_idx]
            
            if value == 'F':
                html += f'<td style="border:1px solid rgba(0,0,0,0.08);padding:4px 2px;text-align:center;"><div style="display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;background:rgba(255,215,0,0.15);color:#E65100;font-size:1.1rem;border:2px solid #FFD700;">★</div></td>'
            else:
                num = int(value)
                is_called = num in called_numbers
                style = ''
                if is_called and is_winner:
                    style = 'background:rgba(255,215,0,0.2);color:#1a1a2e;border-color:#FFD700;animation:winnerPulse 1s ease-in-out infinite alternate;'
                elif is_called:
                    style = 'background:rgba(255,152,0,0.15);color:#E65100;border-color:#FF9800;transform:scale(1.05);'
                else:
                    style = 'background:rgba(255,255,255,0.5);color:#1a1a2e;border-color:rgba(0,0,0,0.06);'
                
                html += f'<td style="border:1px solid rgba(0,0,0,0.08);padding:4px 2px;text-align:center;"><div style="display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;{style}font-weight:bold;font-size:0.8rem;border:2px solid;">{value}</div></td>'
        html += '</tr>'
    
    html += '</table>'
    
    total_called = sum(1 for row in cells for val in row if val != 'F' and int(val) in called_numbers)
    
    if is_winner and winning_pattern:
        html += f'<div style="text-align:center;color:#E65100;font-size:0.8rem;margin-top:4px;">🏆 WINNER! ({winning_pattern}) 🏆</div>'
    else:
        html += f'<div style="text-align:center;color:#666;font-size:0.65rem;margin-top:4px;">✅ {total_called}/24 called</div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

def display_master_board():
    """Display the BINGO board"""
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
            background: rgba(255,255,255,0.9);
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            border: 1px solid rgba(0,0,0,0.06);
        }
        .board-title {
            text-align: center;
            font-size: 1.8rem;
            font-weight: bold;
            color: #1a1a2e;
            margin-bottom: 12px;
        }
        .board-table {
            width: 100%;
            border-collapse: collapse;
        }
        .board-table td {
            border: 1px solid rgba(0,0,0,0.08);
            padding: 6px 4px;
            text-align: center;
            font-size: 0.85rem;
            font-weight: bold;
            min-width: 30px;
        }
        .board-table .header-cell {
            background: linear-gradient(135deg, rgba(46,125,50,0.15), rgba(27,94,32,0.08));
            color: #1a1a2e;
            font-size: 1.5rem;
            font-weight: 900;
            padding: 10px 4px;
            text-align: center;
            border: 1px solid rgba(0,0,0,0.1);
            letter-spacing: 3px;
        }
        .board-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: rgba(255,255,255,0.5);
            color: #1a1a2e;
            font-weight: bold;
            font-size: 0.8rem;
            border: 1px solid rgba(0,0,0,0.06);
            transition: all 0.3s ease;
        }
        .board-number.called {
            background: rgba(255, 152, 0, 0.15);
            color: #E65100;
            border-color: #FF9800;
            transform: scale(1.08);
        }
        .board-number.last-called {
            background: rgba(229, 57, 53, 0.12);
            color: #C62828;
            border-color: #E53935;
            transform: scale(1.15);
            animation: lastPulse 0.5s ease-in-out;
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
            color: #666;
            padding: 8px;
            background: rgba(0,0,0,0.02);
            border-radius: 8px;
        }
        .board-stats strong {
            color: #1a1a2e;
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
        html += f'<div style="text-align:center;font-size:1.1rem;font-weight:bold;color:#C62828;margin-bottom:8px;">🎯 Last Called: <span style="background:rgba(229,57,53,0.1);color:#C62828;padding:3px 15px;border-radius:15px;border:1px solid rgba(229,57,53,0.2);">{st.session_state.last_called_number} ({letter}) - {amharic}</span></div>'
    
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
    <h1 style="font-family:'Orbitron',sans-serif;font-weight:900;font-size:2.2rem;background:linear-gradient(135deg,#FFD700,#FFA500,#FFD700);background-size:300% 300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3s ease-in-out infinite;letter-spacing:6px;margin:0;">
        🎯 ደራሽ ቢንጎ
    </h1>
    <p style="color:#666;font-size:0.9rem;letter-spacing:3px;margin-top:-3px;">
        Derash BINGO - 201 Cards
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
    <p style="margin:0;font-weight:600;color:#1a1a2e;">👤 {user.get('name', st.session_state.current_user)}</p>
    <p style="margin:3px 0;color:#666;font-size:0.7rem;">📱 {user.get('phone', 'No phone')}</p>
    <p style="margin:5px 0;font-size:1.1rem;font-weight:bold;color:#2E7D32;">💰 {balance} ETB</p>
    <p style="margin:3px 0;color:#666;font-size:0.7rem;">⭐ {st.session_state.current_role.title()} | 🏆 {user.get('wins', 0)} wins</p>
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
    # Card Selection Phase
    st.markdown("## 📋 Select Your Card (1 - 201)")
    
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
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:15px;flex-wrap:wrap;background:rgba(255,255,255,0.5);padding:8px 15px;border-radius:12px;border:1px solid rgba(0,0,0,0.05);">
        <span style="display:inline-block;padding:8px 20px;background:rgba(255,255,255,0.5);border-radius:8px;border:2px solid {color};font-size:1.3rem;font-weight:bold;color:{color};font-family:monospace;">
            ⏱️ {time_str}
        </span>
        <span style="display:inline-block;padding:6px 15px;background:linear-gradient(135deg,#2E7D32,#1B5E20);border-radius:8px;font-size:0.9rem;font-weight:bold;color:#FFD700;">
            Select Card
        </span>
        <span style="display:inline-block;padding:6px 15px;background:rgba(255,255,255,0.5);border-radius:8px;border:1px solid rgba(0,0,0,0.06);font-size:0.8rem;color:#666;">
            Selected: {len(st.session_state.clicked_numbers)}/2
        </span>
        <span style="display:inline-block;padding:6px 15px;background:rgba(255,215,0,0.05);border-radius:8px;border:1px solid rgba(255,215,0,0.08);font-size:0.8rem;color:#E65100;">
            💰 {balance} ETB
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.card_selection_time <= 10:
        st.warning(f"⚠️ Only {int(st.session_state.card_selection_time)} seconds left!")
    elif st.session_state.card_selection_time <= 30:
        st.info(f"⏱️ {int(st.session_state.card_selection_time)} seconds remaining...")
    
    # Cards grid - scrollable with small rectangles
    st.markdown('<div class="cards-grid-container">', unsafe_allow_html=True)
    st.markdown('<div class="cards-grid">', unsafe_allow_html=True)
    
    # Create grid using columns
    cols = st.columns(10)
    for i in range(1, 202):
        col_idx = (i - 1) % 10
        with cols[col_idx]:
            is_clicked = i in st.session_state.clicked_numbers
            is_taken = i in st.session_state.taken_cards
            is_disabled = (len(st.session_state.clicked_numbers) >= 2 and not is_clicked) or is_taken
            
            if is_taken:
                # Show as taken/locked
                st.markdown(f'<div class="card-btn taken" style="border-color:rgba(255,0,0,0.2);background:#f5f5f5;color:#999;cursor:not-allowed;opacity:0.5;">{i}<span class="tick-mark">🔒</span></div>', unsafe_allow_html=True)
            else:
                if is_clicked:
                    btn_type = "secondary"
                    label = f"✅ {i}"
                    # Add tick mark for selected
                    st.markdown(f'<div class="card-btn selected"><span class="tick-mark">✓</span>{i}</div>', unsafe_allow_html=True)
                    # Use a hidden button for functionality
                    if st.button(
                        "✓",
                        key=f"card_{i}",
                        use_container_width=True,
                        type="secondary"
                    ):
                        st.session_state.clicked_numbers.remove(i)
                        if st.session_state.selected_card == i:
                            st.session_state.selected_card = None
                        st.rerun()
                else:
                    if st.button(
                        str(i),
                        key=f"card_{i}",
                        use_container_width=True,
                        type="primary",
                        disabled=is_disabled
                    ):
                        if len(st.session_state.clicked_numbers) < 2:
                            st.session_state.clicked_numbers.add(i)
                            st.session_state.taken_cards.append(i)
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if len(st.session_state.clicked_numbers) >= 2:
        st.success("✅ Maximum 2 cards selected! Waiting for timer...")
    else:
        st.info("👆 Click a card to select it (max 2 cards)")
    
    progress = 1 - (st.session_state.card_selection_time / 60)
    st.progress(progress)
    st.caption(f"⏱️ Auto-join in {int(st.session_state.card_selection_time)}s")

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
            <div style="font-size:2.5rem;color:#FFD700;margin:8px 0;">🎉 ቢንጎ! 🎉</div>
            <div style="font-size:1.8rem;color:#FFD700;margin:5px 0;">🎊 እንኳን ደስ አለዎት! 🎊</div>
            <div style="font-size:1.2rem;color:#1a1a2e;">🏆 {len(st.session_state.winners_list)} Winner(s)!</div>
            <div style="font-size:1rem;color:#2E7D32;">💰 Prize per winner: {prize_per_winner} ETB</div>
            <div style="font-size:0.9rem;color:#666;">Total: {len(all_player_cards)} × {PRIZE_PER_CARD} ETB = {total_prize} ETB</div>
            <div style="font-size:1rem;color:#E65100;margin-top:5px;">🏅 {winning_pattern}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        st.snow()
        
        st.markdown("### 📋 Your Cards")
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
        <div style="background:rgba(46,125,50,0.05);border:1px solid rgba(0,0,0,0.05);padding:8px 15px;border-radius:10px;text-align:center;margin-bottom:15px;font-size:0.9rem;color:#1a1a2e;">
            🎯 Playing with {len(all_player_cards)} Card(s)
            <span style="margin-left:12px;background:rgba(255,215,0,0.05);padding:2px 10px;border-radius:12px;border:1px solid rgba(255,215,0,0.08);">
                {len(st.session_state.called_numbers)}/75 Called
            </span>
            <span style="margin-left:8px;background:rgba(255,215,0,0.05);padding:2px 10px;border-radius:12px;border:1px solid rgba(255,215,0,0.08);">
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
<div style="text-align:center;color:#999;font-size:0.75rem;padding:15px;border-top:1px solid rgba(0,0,0,0.05);">
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
