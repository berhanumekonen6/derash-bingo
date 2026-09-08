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
    
    /* Card selection grid wrapper */
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
    
    /* CSS Grid - responsive columns */
    .cards-grid {
        display: grid !important;
        grid-template-columns: repeat(10, 1fr) !important;
        gap: 5px !important;
        max-width: 100% !important;
        margin: 0 auto !important;
    }
    
    /* Mobile - fewer columns for readable numbers */
    @media (max-width: 768px) {
        .cards-grid {
            grid-template-columns: repeat(4, 1fr) !important;
            gap: 6px !important;
        }
        .cards-grid-wrapper {
            max-height: 500px !important;
        }
        .card-btn {
            font-size: 1rem !important;
            min-height: 48px !important;
            height: 48px !important;
            padding: 6px 4px !important;
            border-radius: 10px !important;
            border-width: 2px !important;
        }
    }
    
    @media (max-width: 480px) {
        .cards-grid {
            grid-template-columns: repeat(3, 1fr) !important;
            gap: 5px !important;
        }
        .cards-grid-wrapper {
            max-height: 450px !important;
        }
        .card-btn {
            font-size: 0.95rem !important;
            min-height: 46px !important;
            height: 46px !important;
            padding: 5px 3px !important;
            border-radius: 8px !important;
        }
    }
    
    @media (max-width: 360px) {
        .cards-grid {
            grid-template-columns: repeat(3, 1fr) !important;
            gap: 4px !important;
        }
        .cards-grid-wrapper {
            max-height: 400px !important;
        }
        .card-btn {
            font-size: 0.85rem !important;
            min-height: 42px !important;
            height: 42px !important;
            padding: 4px 2px !important;
            border-radius: 6px !important;
        }
    }
    
    /* Landscape mode for phones */
    @media (orientation: landscape) and (max-height: 600px) {
        .cards-grid {
            grid-template-columns: repeat(6, 1fr) !important;
            gap: 4px !important;
        }
        .card-btn {
            font-size: 0.75rem !important;
            min-height: 32px !important;
            height: 32px !important;
            padding: 3px 2px !important;
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
        border-color: #4CAF50 !important;
        background: rgba(76, 175, 80, 0.35) !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 35px rgba(76, 175, 80, 0.3) !important;
        border-width: 3px !important;
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
    
    /* Winner Card Celebration */
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
    if 'columns_per_row' not in st.session_state:
        st.session_state.columns_per_row = 4
    if 'global_synced' not in st.session_state:
        st.session_state.global_synced = False

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
# GLOBAL CARD TRACKING - SHARED ACROSS ALL USERS
# ===================================================================

def get_global_cards_file():
    return "bingo_global_cards.json"

def load_global_cards():
    """Load globally selected cards from file"""
    try:
        if os.path.exists(get_global_cards_file()):
            with open(get_global_cards_file(), "r") as f:
                data = json.load(f)
                return data.get("taken_cards", []), data.get("card_owner", {})
    except:
        pass
    return [], {}

def save_global_cards(taken_cards, card_owner):
    """Save globally selected cards to file"""
    try:
        with open(get_global_cards_file(), "w") as f:
            json.dump({
                "taken_cards": taken_cards,
                "card_owner": card_owner
            }, f)
        return True
    except:
        return False

def sync_global_cards():
    """Sync session state with global card data"""
    global_taken, global_owner = load_global_cards()
    
    # Update session state with global data
    st.session_state.taken_cards = global_taken
    st.session_state.card_owner = global_owner
    
    # Also sync clicked_numbers for the current user
    current_user = st.session_state.current_user
    if current_user:
        # Get cards owned by current user - compare strings directly since both are strings
        user_cards = [int(card_id) for card_id, owner in global_owner.items() if owner == current_user] if global_owner else []
        st.session_state.clicked_numbers = set(user_cards)

# ===================================================================
# AUTHENTICATION - FIXED: Balance starts at 0.00 ETB
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
        
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.current_role = "admin"
        # Sync global cards after login
        sync_global_cards()
        return True, "✅ Admin login successful!"
    
    if username not in st.session_state.user_db:
        return False, "❌ Username not found"
    
    if verify_password(password, st.session_state.user_db[username]["password"]):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.current_role = st.session_state.user_db[username]["role"]
        # Sync global cards after login
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
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_role = None
    st.session_state.global_synced = False

# ===================================================================
# ADMIN PANEL
# ===================================================================

def admin_panel():
    """Admin panel for managing user balances"""
    st.markdown("""
    <div class="glass-container">
        <h3 style="color:#FFD700;text-align:center;">🔧 Admin Panel</h3>
        <p style="color:rgba(255,255,255,0.7);text-align:center;">Manage user balances, view all users.</p>
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
# ALL 201 BINGO CARDS - FULL LIST (truncated for brevity, keep your full list)
# ===================================================================

BINGO_CARDS = [
    {"id": 1, "cells": [['15', '16', '39', '59', '66'], ['11', '28', '40', '51', '68'], ['12', '20', 'F', '56', '67'], ['3', '30', '35', '60', '72'], ['10', '24', '37', '53', '64']]},
    # ... keep all your 201 cards here ...
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
    
    # TOTAL PRIZE = ALL cards selected by ALL players × 8 ETB
    total_prize = len(st.session_state.taken_cards) * PRIZE_PER_CARD
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
# DISPLAY FUNCTIONS - UPDATED: Winner cards shown with celebration
# ===================================================================

def display_selected_card(card_id, called_numbers=None, is_winner=False, winning_pattern=None):
    """Display a BINGO card with winner celebration"""
    if called_numbers is None:
        called_numbers = []
    
    card = get_card(card_id)
    if not card:
        return
    
    cells = card["cells"]
    
    # Winner card gets special styling
    if is_winner:
        border_color = '#FFD700'
        title_color = '#FFD700'
        card_class = 'winner-card'
        winner_badge = f'🎉🏆 WINNER! ({winning_pattern}) 🏆🎉' if winning_pattern else '🎉🏆 WINNER! 🏆🎉'
    else:
        border_color = 'rgba(255,255,255,0.1)'
        title_color = '#FFFFFF'
        card_class = ''
        winner_badge = ''
    
    html = f"""
    <div class="{card_class}" style="background:rgba(0,0,0,0.2);border-radius:15px;padding:12px;margin:8px auto;box-shadow:0 4px 12px rgba(0,0,0,0.3);max-width:400px;border:2px solid {border_color};transition:all 0.3s ease;{'animation:winnerPulse 1s ease-in-out infinite alternate;' if is_winner else ''}">
        <div style="text-align:center;color:{title_color};font-size:1rem;font-weight:bold;margin-bottom:8px;text-shadow:0 0 20px rgba(255,215,0,0.1);">
            {'🎊 ' if is_winner else '🎯'} Card #{card_id} { '🎊' if is_winner else ''}
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
# CARD SELECTION FUNCTION - GLOBAL BOARD FOR ALL PLAYERS
# ===================================================================

def render_card_selection():
    """Render card selection grid using Streamlit columns - ONE GLOBAL BOARD"""
    
    # Sync with global data first
    if not st.session_state.global_synced:
        sync_global_cards()
        st.session_state.global_synced = True
    
    remaining = st.session_state.card_selection_time
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    time_str = f"{minutes:01d}:{seconds:02d}"
    
    # Get balance from session state
    user = st.session_state.user_db.get(st.session_state.current_user, {})
    balance = user.get("balance", 0)
    
    # === GLOBAL CARD COUNTS - SAME FOR ALL PLAYERS ===
    total_selected = len(st.session_state.taken_cards)  # ALL cards from ALL players
    your_cards = len(st.session_state.clicked_numbers)   # YOUR cards only
    available = 201 - total_selected
    min_cards_required = 3
    enough_cards = total_selected >= min_cards_required
    
    # Determine timer color
    if not enough_cards:
        color = "#FF9800"
    elif remaining <= 10:
        color = "#E53935"
    elif remaining <= 30:
        color = "#FF9800"
    else:
        color = "#FFD700"
    
    timer_display = time_str
    timer_icon = "⏸️" if not enough_cards else "⏱️"
    
    # Column selection dropdown
    col_options = [2, 3, 4, 5, 6, 8, 10]
    st.session_state.columns_per_row = st.selectbox(
        "📊 Cards per row:",
        options=col_options,
        index=col_options.index(4),
        help="Select how many cards to display per row"
    )
    
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:15px;flex-wrap:wrap;background:rgba(0,0,0,0.15);padding:8px 15px;border-radius:12px;border:1px solid rgba(255,255,255,0.08);">
        <span style="display:inline-block;padding:8px 20px;background:rgba(0,0,0,0.15);border-radius:8px;border:2px solid {color};font-size:1.3rem;font-weight:bold;color:{color};font-family:monospace;text-shadow:0 0 20px rgba(255,215,0,0.1);">
            {timer_icon} {timer_display}
        </span>
        <span style="display:inline-block;padding:6px 15px;background:linear-gradient(135deg,#2E7D32,#1B5E20);border-radius:8px;font-size:0.9rem;font-weight:bold;color:#FFD700;">
            Select Card
        </span>
        <span style="display:inline-block;padding:6px 15px;background:rgba(76,175,80,0.2);border-radius:8px;border:1px solid rgba(76,175,80,0.3);font-size:0.8rem;color:#4CAF50;">
            🟢 Your Cards: {your_cards}/2
        </span>
        <span style="display:inline-block;padding:6px 15px;background:rgba(255,215,0,0.15);border-radius:8px;border:2px solid #FFD700;font-size:0.85rem;color:#FFD700;font-weight:bold;">
            📊 Global Board: {total_selected}/201
        </span>
        <span style="display:inline-block;padding:6px 15px;background:rgba(255,255,255,0.05);border-radius:8px;border:1px solid rgba(255,255,255,0.06);font-size:0.8rem;color:rgba(255,255,255,0.5);">
            ⬜ Available: {available}
        </span>
        <span style="display:inline-block;padding:6px 15px;background:rgba(255,215,0,0.08);border-radius:8px;border:1px solid rgba(255,215,0,0.08);font-size:0.8rem;color:#FFD700;">
            💰 {balance:.2f} ETB
        </span>
        <span style="display:inline-block;padding:6px 15px;background:rgba(255,200,0,0.1);border-radius:8px;border:2px solid {'#4CAF50' if enough_cards else '#FF9800'};font-size:0.8rem;color:{'#4CAF50' if enough_cards else '#FF9800'};font-weight:bold;">
            {'✅' if enough_cards else '⚠️'} {total_selected}/{min_cards_required}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Status Messages
    if not enough_cards:
        st.warning(f"⚠️ Need {min_cards_required - total_selected} more card(s) to start the game! 🎯")
        st.info(f"👥 {total_selected} cards selected globally. Keep selecting! 🃏")
    elif remaining <= 10:
        st.warning(f"⚠️ Only {int(remaining)} seconds left! Game will start soon! ⏰")
    elif remaining <= 30:
        st.info(f"⏱️ {int(remaining)} seconds remaining... Game starting soon! 🎯")
    else:
        st.info(f"📝 Select your cards (max 2). {int(remaining)} seconds remaining ⏳")
    
    # Show currently selected cards by you
    if len(st.session_state.clicked_numbers) > 0:
        your_cards_list = sorted(list(st.session_state.clicked_numbers))
        st.success(f"🟢 Your selected cards: {', '.join(map(str, your_cards_list))}")
        st.caption(f"💡 Click a selected card (🟢) to DESELECT it")
    
    # Create grid using selected number of columns
    cols_per_row = st.session_state.columns_per_row
    cols = st.columns(cols_per_row)
    
    for i in range(1, 202):
        col_idx = (i - 1) % cols_per_row
        with cols[col_idx]:
            is_clicked = i in st.session_state.clicked_numbers
            is_taken = i in st.session_state.taken_cards
            is_disabled = (len(st.session_state.clicked_numbers) >= 2 and not is_clicked) or is_taken
            
            if is_clicked:
                btn_type = "secondary"
                label = f"🟢 {i}"
            elif is_disabled:
                btn_type = "secondary"
                label = str(i)
            else:
                btn_type = "primary"
                label = str(i)
            
            if st.button(
                label,
                key=f"card_{i}",
                use_container_width=True,
                type=btn_type,
                disabled=is_disabled
            ):
                if i in st.session_state.clicked_numbers:
                    # DESELECT - Remove your card from global board
                    st.session_state.clicked_numbers.remove(i)
                    if i in st.session_state.taken_cards:
                        st.session_state.taken_cards.remove(i)
                    if str(i) in st.session_state.card_owner:
                        del st.session_state.card_owner[str(i)]
                    if st.session_state.selected_card == i:
                        st.session_state.selected_card = None
                    # Save to global file
                    save_global_cards(st.session_state.taken_cards, st.session_state.card_owner)
                    st.rerun()
                else:
                    # SELECT - Add your card to global board
                    if len(st.session_state.clicked_numbers) < 2 and i not in st.session_state.taken_cards:
                        st.session_state.clicked_numbers.add(i)
                        st.session_state.taken_cards.append(i)
                        st.session_state.card_owner[str(i)] = st.session_state.current_user
                        # Save to global file
                        save_global_cards(st.session_state.taken_cards, st.session_state.card_owner)
                        st.rerun()
    
    if len(st.session_state.clicked_numbers) >= 2:
        st.success("✅ Maximum 2 cards selected! Waiting for other players... ⏳")
    elif len(st.session_state.clicked_numbers) > 0:
        st.info(f"👆 You have {len(st.session_state.clicked_numbers)} card(s) selected. Click a 🟢 green card to DESELECT")
    else:
        st.info("👆 Click a card to select it (max 2 cards)")
    
    progress = 1 - (st.session_state.card_selection_time / 60)
    st.progress(progress)
    
    if enough_cards:
        st.caption(f"✅ {total_selected} cards ready! Game will start in {int(remaining)}s 🎯")
    else:
        st.caption(f"⏸️ Waiting for {min_cards_required - total_selected} more card(s)... {total_selected} selected 🃏")
        
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
    🎯🍀 <h1 style="font-family:'Orbitron',sans-serif;font-weight:900;font-size:2.2rem;background:linear-gradient(135deg,#FFD700,#FFA500,#FFD700);background-size:300% 300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3s ease-in-out infinite;letter-spacing:6px;margin:0;text-shadow:0 0 40px rgba(255,215,0,0.1);">
        ደራሽ ቢንጎ
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
                        st.info("💡 Your balance starts at 0.00 ETB. Admin can add balance.")
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
# USER INFO - UPDATED: Shows balance with 2 decimal places
# ===================================================================

user = st.session_state.user_db.get(st.session_state.current_user, {})
balance = user.get("balance", 0)

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
# TIMER - ALWAYS RUNNING
# ===================================================================

current_time = time.time()
time_passed = current_time - st.session_state.card_selection_last_update
st.session_state.card_selection_time = max(0, st.session_state.card_selection_time - time_passed)
st.session_state.card_selection_last_update = current_time

# When timer reaches 0, check if enough cards are selected
if st.session_state.card_selection_time <= 0 and not st.session_state.game_started:
    total_selected = len(st.session_state.taken_cards)
    min_cards_required = 3
    
    if total_selected >= min_cards_required:
        # ENOUGH CARDS - START THE GAME
        st.session_state.card_selection_time = 60
        st.session_state.card_selection_last_update = time.time()
        
        if len(st.session_state.clicked_numbers) > 0 and st.session_state.selected_card is None:
            st.session_state.selected_card = list(st.session_state.clicked_numbers)[0]
            st.session_state.game_started = True
            st.session_state.auto_call_started = False
            st.rerun()
    else:
        # NOT ENOUGH CARDS - RESET TIMER AND WAIT
        st.session_state.card_selection_time = 30
        st.session_state.card_selection_last_update = time.time()
        st.warning(f"⚠️ Only {total_selected}/3 cards selected. Waiting for more players to join...")
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
    st.markdown("## 📋 ካርድዎን ይምረጡ 🔥🚀")
    
    # Check if we should auto-select
    if st.session_state.card_selection_time <= 0 and len(st.session_state.clicked_numbers) > 0:
        st.session_state.selected_card = list(st.session_state.clicked_numbers)[0]
        st.session_state.game_started = True
        st.session_state.auto_call_started = False
        st.rerun()
    
    render_card_selection()

# ===================================================================
# GAME PLAYING PHASE - UPDATED: Shows winner cards with celebration
# ===================================================================

else:
    all_player_cards = list(st.session_state.clicked_numbers)
    
    if st.session_state.winner_declared:
        total_prize = len(st.session_state.taken_cards) * PRIZE_PER_CARD
        prize_per_winner = total_prize // len(st.session_state.winners_list) if st.session_state.winners_list else 0
        
        winning_pattern = ""
        if st.session_state.winners_list:
            pattern_info = st.session_state.winners_list[0].get("pattern", {})
            winning_pattern = pattern_info.get("type", "BINGO!")
        
        st.markdown(get_winner_sound_js(), unsafe_allow_html=True) 
        
        st.markdown(f"""
        <div style="text-align:center;padding:40px 20px;background:linear-gradient(135deg,rgba(255,215,0,0.15),rgba(255,165,0,0.08));border-radius:20px;border:2px solid #FFD700;margin:15px 0;box-shadow:0 0 60px rgba(255,215,0,0.2);">
            <div style="font-size:4rem;color:#FFD700;">🎉🎊🏆</div>
            <div style="font-size:2.5rem;color:#FFD700;margin:8px 0;text-shadow:0 0 40px rgba(255,215,0,0.3);">🎉 ቢንጎ! የጨዋታዉ አሸናፊ ታዉቋል!!! 🎉</div>
            <div style="font-size:1.8rem;color:#FFD700;margin:5px 0;text-shadow:0 0 30px rgba(255,215,0,0.2);">🎊🍀አሸናፊዉን ለማዎቅ ከታች ይመልከቱ🍀🎊ለቀጣይ መልካም ዕድል!!!🍀🎊</div>
            <div style="font-size:1.2rem;color:#FFFFFF;">🏆 {len(st.session_state.winners_list)} Winner(s)! 🏆</div>
            <div style="font-size:1rem;color:#4CAF50;">💰 Prize per winner: {prize_per_winner:.2f} ETB</div>
            <div style="font-size:0.9rem;color:rgba(255,255,255,0.5);">Total: {len(st.session_state.taken_cards)} × {PRIZE_PER_CARD} ETB = {total_prize} ETB</div>
            <div style="font-size:1rem;color:#FFD700;margin-top:5px;text-shadow:0 0 20px rgba(255,215,0,0.2);">🏅 {winning_pattern}</div>
            <div style="font-size:1.5rem;color:#FFD700;margin-top:10px;">🎊🎊🎊ፈጥንዉ ካርቴላ ይምረጡ!🎊🎊🎊</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        st.snow()
        
        st.markdown("### 🎉🏆 የአሸናፊዎች ካርቴላ 🏆🎉")
        
        # Show all player cards with winner highlighted
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
        
        # Show winning pattern details for all winners
        if st.session_state.winners_list:
            st.markdown("### 🏆 አሸናፊዎች 🏆")
            for idx, winner in enumerate(st.session_state.winners_list, 1):
                pattern_info = winner.get("pattern", {})
                pattern_type = pattern_info.get("type", "BINGO!")
                st.success(f"🎉 Winner {idx}: Card #{winner.get('card_id')} - {pattern_type} 🎉")
        
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
            st.session_state.card_owner = {}
            # Save empty global state
            save_global_cards([], {})
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
            st.markdown("### 📋🍀 የእርስዎ ካርቴላ/ዎች")
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
