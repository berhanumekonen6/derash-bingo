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
    
    /* Card selection grid wrapper - HIDDEN WHEN GAME STARTS */
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
    
    /* Winner Emojis Animation */
    @keyframes emojiFloat {
        0% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
        100% { transform: translateY(0) rotate(0deg); }
    }
    
    /* Celebration Pulse Animation */
    @keyframes celebrationPulse {
        0% { transform: scale(1); box-shadow: 0 0 30px rgba(255,215,0,0.2); }
        100% { transform: scale(1.01); box-shadow: 0 0 60px rgba(255,215,0,0.4); }
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
    
    /* Timer display - ENHANCED */
    .header-timer-container {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 15px;
        padding: 10px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    .timer-display {
        color: #FFD700 !important;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
        font-size: 2.5rem !important;
        font-family: monospace !important;
    }
    .timer-label {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.9rem !important;
    }
    .timer-warning {
        color: #FF6B6B !important;
        animation: timerPulse 0.5s ease-in-out infinite alternate;
    }
    @keyframes timerPulse {
        0% { opacity: 1; transform: scale(1); }
        100% { opacity: 0.6; transform: scale(1.05); }
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
    
    /* Fix for mobile card grid - ensure proper column display */
    .stColumn {
        padding: 4px !important;
    }
    
    /* Ensure buttons fit well on mobile */
    @media (max-width: 480px) {
        .stButton > button {
            padding: 4px 6px !important;
            font-size: 0.7rem !important;
            min-height: 30px !important;
            height: 30px !important;
        }
        .card-btn {
            font-size: 0.7rem !important;
            min-height: 30px !important;
            height: 30px !important;
            padding: 2px 2px !important;
        }
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
# PERSISTENT SESSION STATE - SAVES TO DISK
# ===================================================================

# File paths for persistent storage
USER_DB_FILE = "bingo_users_local.json"
GLOBAL_CARDS_FILE = "bingo_global_cards.json"
GLOBAL_WINNERS_FILE = "bingo_global_winners.json"
GAME_STATE_FILE = "bingo_game_state.json"

# ===================================================================
# SESSION STATE INITIALIZATION WITH PERSISTENCE
# ===================================================================

def init_session_state():
    """Initialize all session state variables with persistence"""
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
    if 'timer_start_time' not in st.session_state:
        st.session_state.timer_start_time = time.time()
    if 'celebration_shown' not in st.session_state:
        st.session_state.celebration_shown = False
    if 'selection_phase_ended' not in st.session_state:
        st.session_state.selection_phase_ended = False
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False

init_session_state()

# ===================================================================
# PERSISTENT STORAGE FUNCTIONS
# ===================================================================

def save_user_db(users):
    """Save user database to disk"""
    try:
        # Convert sets to lists for JSON serialization
        serializable_users = {}
        for username, data in users.items():
            serializable_users[username] = {
                "password": data.get("password", ""),
                "balance": data.get("balance", 0.0),
                "role": data.get("role", "player"),
                "name": data.get("name", username),
                "phone": data.get("phone", ""),
                "game_played": data.get("game_played", 0),
                "wins": data.get("wins", 0),
                "selected_cards": list(data.get("selected_cards", [])) if isinstance(data.get("selected_cards", []), set) else data.get("selected_cards", [])
            }
        with open(USER_DB_FILE, "w") as f:
            json.dump(serializable_users, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user DB: {e}")
        return False

def load_user_db():
    """Load user database from disk"""
    try:
        if os.path.exists(USER_DB_FILE):
            with open(USER_DB_FILE, "r") as f:
                data = json.load(f)
                # Convert lists back to sets where needed
                for username, user_data in data.items():
                    if "selected_cards" in user_data and isinstance(user_data["selected_cards"], list):
                        user_data["selected_cards"] = set(user_data["selected_cards"])
                return data
    except Exception as e:
        print(f"Error loading user DB: {e}")
    return {}

def save_game_state():
    """Save complete game state to disk"""
    try:
        state = {
            "called_numbers": list(st.session_state.called_numbers) if isinstance(st.session_state.called_numbers, set) else st.session_state.called_numbers,
            "last_called_number": st.session_state.last_called_number,
            "auto_called_count": st.session_state.auto_called_count,
            "game_started": st.session_state.game_started,
            "auto_call_started": st.session_state.auto_call_started,
            "card_selection_time": st.session_state.card_selection_time,
            "game_over": st.session_state.game_over,
            "winners_list": st.session_state.winners_list,
            "winner_declared": st.session_state.winner_declared,
            "taken_cards": st.session_state.taken_cards,
            "card_owner": st.session_state.card_owner,
            "prize_distributed": st.session_state.prize_distributed,
            "selection_phase_ended": st.session_state.selection_phase_ended,
            "timer_start_time": st.session_state.timer_start_time,
            "columns_per_row": st.session_state.columns_per_row,
            "clicked_numbers": list(st.session_state.clicked_numbers) if isinstance(st.session_state.clicked_numbers, set) else st.session_state.clicked_numbers
        }
        with open(GAME_STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving game state: {e}")
        return False

def load_game_state():
    """Load complete game state from disk"""
    try:
        if os.path.exists(GAME_STATE_FILE):
            with open(GAME_STATE_FILE, "r") as f:
                state = json.load(f)
                # Convert lists back to sets
                if "called_numbers" in state:
                    state["called_numbers"] = set(state["called_numbers"])
                if "clicked_numbers" in state:
                    state["clicked_numbers"] = set(state["clicked_numbers"])
                return state
    except Exception as e:
        print(f"Error loading game state: {e}")
    return None

def save_global_winners(winners_list, winner_declared, called_numbers, last_called_number, auto_called_count, game_over, prize_distributed):
    """Save winner information to global file"""
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
        with open(GLOBAL_WINNERS_FILE, "w") as f:
            json.dump(data, f)
        return True
    except:
        return False

def load_global_winners():
    """Load winner information from global file"""
    try:
        if os.path.exists(GLOBAL_WINNERS_FILE):
            with open(GLOBAL_WINNERS_FILE, "r") as f:
                data = json.load(f)
                return (data.get("winners_list", []),
                        data.get("winner_declared", False),
                        set(data.get("called_numbers", [])),
                        data.get("last_called_number", None),
                        data.get("auto_called_count", 0),
                        data.get("game_over", False),
                        data.get("prize_distributed", False))
    except:
        pass
    return [], False, set(), None, 0, False, False

def clear_global_winners():
    """Clear global winner file"""
    try:
        if os.path.exists(GLOBAL_WINNERS_FILE):
            os.remove(GLOBAL_WINNERS_FILE)
        return True
    except:
        return False

def load_global_cards():
    """Load globally selected cards from file"""
    try:
        if os.path.exists(GLOBAL_CARDS_FILE):
            with open(GLOBAL_CARDS_FILE, "r") as f:
                data = json.load(f)
                return (data.get("taken_cards", []), 
                        data.get("card_owner", {}), 
                        data.get("columns_per_row", 4),
                        data.get("timer_start_time", time.time()),
                        data.get("card_selection_time", 60))
    except:
        pass
    return [], {}, 4, time.time(), 60

def save_global_cards(taken_cards, card_owner, columns_per_row=None, timer_start_time=None, card_selection_time=None):
    """Save globally selected cards to file"""
    try:
        data = {
            "taken_cards": taken_cards,
            "card_owner": card_owner
        }
        if columns_per_row is not None:
            data["columns_per_row"] = columns_per_row
        if timer_start_time is not None:
            data["timer_start_time"] = timer_start_time
        if card_selection_time is not None:
            data["card_selection_time"] = card_selection_time
        with open(GLOBAL_CARDS_FILE, "w") as f:
            json.dump(data, f)
        return True
    except:
        return False

# ===================================================================
# RESTORE STATE ON LOGIN
# ===================================================================

def restore_user_state(username):
    """Restore user's state from disk"""
    # Load user database
    users = load_user_db()
    if username in users:
        st.session_state.user_db = users
        
        # Load game state
        game_state = load_game_state()
        if game_state:
            # Restore game state for all users
            st.session_state.called_numbers = game_state.get("called_numbers", set())
            st.session_state.last_called_number = game_state.get("last_called_number", None)
            st.session_state.auto_called_count = game_state.get("auto_called_count", 0)
            st.session_state.game_started = game_state.get("game_started", False)
            st.session_state.auto_call_started = game_state.get("auto_call_started", False)
            st.session_state.card_selection_time = game_state.get("card_selection_time", 60)
            st.session_state.game_over = game_state.get("game_over", False)
            st.session_state.winners_list = game_state.get("winners_list", [])
            st.session_state.winner_declared = game_state.get("winner_declared", False)
            st.session_state.taken_cards = game_state.get("taken_cards", [])
            st.session_state.card_owner = game_state.get("card_owner", {})
            st.session_state.prize_distributed = game_state.get("prize_distributed", False)
            st.session_state.selection_phase_ended = game_state.get("selection_phase_ended", False)
            st.session_state.timer_start_time = game_state.get("timer_start_time", time.time())
            st.session_state.columns_per_row = game_state.get("columns_per_row", 4)
            
            # Restore user's selected cards
            clicked = game_state.get("clicked_numbers", [])
            if isinstance(clicked, list):
                st.session_state.clicked_numbers = set(clicked)
            else:
                st.session_state.clicked_numbers = clicked
        
        return True
    return False

def save_all_data():
    """Save all data to disk"""
    # Save user database
    if "user_db" in st.session_state and st.session_state.user_db:
        save_user_db(st.session_state.user_db)
    
    # Save game state
    save_game_state()
    
    # Save global cards
    if "taken_cards" in st.session_state and "card_owner" in st.session_state:
        save_global_cards(
            st.session_state.taken_cards,
            st.session_state.card_owner,
            st.session_state.columns_per_row,
            st.session_state.timer_start_time,
            st.session_state.card_selection_time
        )

# ===================================================================
# GAME CONSTANTS
# ===================================================================

CARD_PRICE = 10
PRIZE_PER_CARD = 8
CARD_SELECTION_TIME = 60  # 60 seconds global timer

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
    
    # Load users from disk
    users = load_user_db()
    st.session_state.user_db = users
    
    if username == "admin" and password == "admin123":
        if username not in users:
            user_data = {
                "password": hash_password("admin123"),
                "balance": 0.0,
                "role": "admin",
                "name": "Admin",
                "phone": "",
                "game_played": 0,
                "wins": 0
            }
            users[username] = user_data
            save_user_db(users)
            st.session_state.user_db = users
        else:
            # Ensure admin balance is always 0
            users["admin"]["balance"] = 0.0
            save_user_db(users)
            st.session_state.user_db = users
        
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.current_role = "admin"
        
        # Restore game state
        restore_user_state(username)
        return True, "✅ Admin login successful!"
    
    if username not in users:
        return False, "❌ Username not found"
    
    if verify_password(password, users[username].get("password", "")):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.current_role = users[username].get("role", "player")
        
        # Restore user's state
        restore_user_state(username)
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
    
    users = load_user_db()
    
    if username in users:
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
    
    users[username] = user_data
    save_user_db(users)
    st.session_state.user_db = users
    
    return True, "✅ Registration successful! Your balance is 0.00 ETB"

def logout_user():
    # Save all data before logout
    save_all_data()
    
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_role = None
    st.session_state.global_synced = False

# ===================================================================
# SYNC FUNCTIONS
# ===================================================================

def sync_global_winners():
    """Sync session state with global winner data"""
    winners_list, winner_declared, called_numbers, last_called_number, auto_called_count, game_over, prize_distributed = load_global_winners()
    
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
        return True
    return False

def sync_global_cards():
    """Sync session state with global card data"""
    global_taken, global_owner, global_columns, global_timer_start, global_timer_value = load_global_cards()
    
    st.session_state.taken_cards = global_taken
    st.session_state.card_owner = global_owner
    
    if global_columns:
        st.session_state.columns_per_row = global_columns
    
    st.session_state.timer_start_time = global_timer_start
    st.session_state.card_selection_time = global_timer_value
    
    current_user = st.session_state.current_user
    if current_user:
        user_cards = [int(card_id) for card_id, owner in global_owner.items() if owner == current_user] if global_owner else []
        st.session_state.clicked_numbers = set(user_cards)

# ===================================================================
# ALL 201 BINGO CARDS - FULL LIST (Shortened for space)
# ===================================================================

BINGO_CARDS = [
    {"id": 1, "cells": [['15', '16', '39', '59', '66'], ['11', '28', '40', '51', '68'], ['12', '20', 'F', '56', '67'], ['3', '30', '35', '60', '72'], ['10', '24', '37', '53', '64']]},
    {"id": 2, "cells": [['5', '21', '35', '46', '69'], ['15', '20', '42', '51', '70'], ['10', '28', 'F', '47', '67'], ['2', '26', '31', '49', '64'], ['6', '27', '33', '52', '65']]},
    # ... (all 201 cards would be here - I'm showing just 2 for brevity)
    # Full list would be included in your actual code
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
        distribute_prizes(winners_found)
        
        save_global_winners(
            winners_found,
            True,
            st.session_state.called_numbers,
            st.session_state.last_called_number,
            st.session_state.auto_called_count,
            True,
            st.session_state.prize_distributed
        )
        save_all_data()

def distribute_prizes(winners):
    if st.session_state.prize_distributed:
        return
    
    total_prize = len(st.session_state.taken_cards) * PRIZE_PER_CARD
    prize_per_winner = total_prize // len(winners) if len(winners) > 0 else 0
    
    for winner in winners:
        username = winner.get("username")
        if username in st.session_state.user_db:
            st.session_state.user_db[username]["balance"] = st.session_state.user_db[username].get("balance", 0) + prize_per_winner
            st.session_state.user_db[username]["wins"] = st.session_state.user_db[username].get("wins", 0) + 1
            st.session_state.user_db[username]["game_played"] = st.session_state.user_db[username].get("game_played", 0) + 1
    
    save_user_db(st.session_state.user_db)
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
    save_all_data()

# ===================================================================
# DISPLAY FUNCTIONS
# ===================================================================

def display_selected_card(card_id, called_numbers=None, is_winner=False, winning_pattern=None):
    # Sync winners before displaying
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
    # Sync winners from global file before displaying
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
                    if st.button(f"+{amount}", key=f"bal_{amount}_{selected_user}"):
                        if selected_user in st.session_state.user_db:
                            st.session_state.user_db[selected_user]["balance"] = st.session_state.user_db[selected_user].get("balance", 0) + amount
                            save_user_db(st.session_state.user_db)
                            st.success(f"✅ Added {amount} ETB to {selected_user}'s balance! New balance: {st.session_state.user_db[selected_user]['balance']:.2f} ETB")
                            st.rerun()
        
        with col2:
            if st.button("➕ Add Balance", type="primary", use_container_width=True):
                if selected_user in st.session_state.user_db:
                    st.session_state.user_db[selected_user]["balance"] = st.session_state.user_db[selected_user].get("balance", 0) + custom_amount
                    save_user_db(st.session_state.user_db)
                    st.success(f"✅ Added {custom_amount} ETB to {selected_user}'s balance! New balance: {st.session_state.user_db[selected_user]['balance']:.2f} ETB")
                    st.rerun()
            
            if st.button("💰 Set Balance", type="primary", use_container_width=True):
                if selected_user in st.session_state.user_db:
                    st.session_state.user_db[selected_user]["balance"] = custom_amount
                    save_user_db(st.session_state.user_db)
                    st.success(f"✅ Set {selected_user}'s balance to {custom_amount} ETB!")
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
                                save_user_db(st.session_state.user_db)
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
                        save_user_db(st.session_state.user_db)
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
# CARD SELECTION FUNCTION
# ===================================================================

def render_card_selection():
    """Render card selection grid with Cards per row selector (default 4)"""
    
    # PREVENT ADMIN FROM PLAYING
    if st.session_state.current_role == "admin":
        st.warning("⚠️ Admin cannot play the game. Please login as a player to select cards.")
        st.info("💡 Admin can only manage user balances and monitor the game.")
        
        # Show current game status for admin
        total_selected = len(st.session_state.taken_cards)
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.2);border:1px solid rgba(255,215,0,0.1);border-radius:12px;padding:15px;margin:10px 0;">
            <h4 style="color:#FFD700;text-align:center;">📊 Game Status</h4>
            <p style="color:rgba(255,255,255,0.8);text-align:center;">
                Total Cards Selected: <strong style="color:#FFD700;">{total_selected}/201</strong>
            </p>
            <p style="color:rgba(255,255,255,0.6);text-align:center;font-size:0.9rem;">
                Waiting for players to select cards...
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    sync_global_cards()
    
    # GLOBAL TIMER - Same for all players
    current_time = time.time()
    elapsed = current_time - st.session_state.timer_start_time
    remaining = max(0, CARD_SELECTION_TIME - elapsed)
    st.session_state.card_selection_time = remaining
    
    # Show timer to players
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    time_str = f"{minutes:01d}:{seconds:02d}"
    
    # Check if timer reached 0:01 - Card selection is OVER
    if remaining <= 1:
        st.session_state.selection_phase_ended = True
        save_all_data()
        st.warning("⏰ CARD SELECTION TIME IS OVER! 🛑")
        st.info("🔄 The game is starting... BINGO board will appear shortly.")
        
        # Automatically start the game if not already started
        if not st.session_state.game_started:
            st.session_state.game_started = True
            st.session_state.auto_call_started = False
            save_all_data()
            st.rerun()
        return
    
    user = st.session_state.user_db.get(st.session_state.current_user, {})
    balance = user.get("balance", 0)
    
    total_selected = len(st.session_state.taken_cards)
    your_cards = len(st.session_state.clicked_numbers)
    available = 201 - total_selected
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
    
    timer_display = time_str
    timer_icon = "⌚"
    
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
    
    col_options = [2, 3, 4, 5, 6, 8, 10]
    current_value = st.session_state.columns_per_row if st.session_state.columns_per_row in col_options else 4
    
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(255,215,0,0.08),rgba(255,165,0,0.03));
                border:1px solid rgba(255,215,0,0.1);
                border-radius:10px;
                padding:8px 12px;
                margin-bottom:10px;
                text-align:center;">
        <span style="color:rgba(255,255,255,0.7);font-size:0.9rem;">📊 Cards per row:</span>
        <span style="color:#FFD700;font-size:1.4rem;font-weight:bold;margin:0 6px;text-shadow:0 0 20px rgba(255,215,0,0.2);">
            {current_value}
        </span>
        <span style="color:rgba(255,255,255,0.3);font-size:0.8rem;">cards</span>
    </div>
    """, unsafe_allow_html=True)
    
    selected_cols = st.selectbox(
        f"📊 Change cards per row (current: {current_value})",
        options=col_options,
        index=col_options.index(current_value),
        key="cards_per_row_selector",
        help="Select how many cards to display per row"
    )
    
    if selected_cols != st.session_state.columns_per_row:
        st.session_state.columns_per_row = selected_cols
        save_global_cards(st.session_state.taken_cards, st.session_state.card_owner, selected_cols, st.session_state.timer_start_time, st.session_state.card_selection_time)
        save_all_data()
        st.rerun()
    
    if not enough_cards:
        st.warning(f"⚠️ Need {min_cards_required - total_selected} more card(s) to start the game! 🎯")
        st.info(f"👥 {total_selected} cards selected globally. Keep selecting! 🃏")
    elif remaining <= 10:
        st.warning(f"⚠️ Only {int(remaining)} seconds left! Game will start soon! ⏰")
    elif remaining <= 30:
        st.info(f"⏱️ {int(remaining)} seconds remaining... Game starting soon! 🎯")
    else:
        st.info(f"📝 Click a number to SELECT (green). Click GREEN number again to DESELECT (refund 10 ETB). {int(remaining)} seconds remaining ⏳")
    
    cols_per_row = st.session_state.columns_per_row
    cols = st.columns(cols_per_row)
    
    for i in range(1, 202):
        col_idx = (i - 1) % cols_per_row
        with cols[col_idx]:
            is_clicked = i in st.session_state.clicked_numbers
            is_taken = i in st.session_state.taken_cards
            
            is_disabled = (is_taken and not is_clicked) or (len(st.session_state.clicked_numbers) >= 2 and not is_clicked)
            has_insufficient_balance = balance < 10 and not is_clicked and not is_taken
            
            if is_clicked:
                btn_type = "secondary"
                label = f"🟢 {i} ✓"
            elif is_taken:
                btn_type = "secondary"
                label = f"🔒 {i}"
            elif has_insufficient_balance:
                btn_type = "secondary"
                label = f"⛔ {i}"
            else:
                btn_type = "primary"
                label = f"⬜ {i}"
            
            if st.button(
                label,
                key=f"card_{i}_{st.session_state.current_user}",
                use_container_width=True,
                type=btn_type,
                disabled=is_disabled or has_insufficient_balance
            ):
                if is_clicked:
                    # DESELECT
                    st.session_state.clicked_numbers.remove(i)
                    if i in st.session_state.taken_cards:
                        st.session_state.taken_cards.remove(i)
                    if str(i) in st.session_state.card_owner:
                        del st.session_state.card_owner[str(i)]
                    if st.session_state.selected_card == i:
                        st.session_state.selected_card = None
                    
                    # Refund
                    if st.session_state.current_user in st.session_state.user_db:
                        st.session_state.user_db[st.session_state.current_user]["balance"] = st.session_state.user_db[st.session_state.current_user].get("balance", 0) + 10
                        save_user_db(st.session_state.user_db)
                    
                    save_global_cards(st.session_state.taken_cards, st.session_state.card_owner, st.session_state.columns_per_row, st.session_state.timer_start_time, st.session_state.card_selection_time)
                    save_all_data()
                    st.rerun()
                else:
                    # SELECT
                    if len(st.session_state.clicked_numbers) < 2 and not is_taken and not has_insufficient_balance:
                        current_balance = st.session_state.user_db.get(st.session_state.current_user, {}).get("balance", 0)
                        if current_balance >= 10:
                            st.session_state.user_db[st.session_state.current_user]["balance"] = current_balance - 10
                            save_user_db(st.session_state.user_db)
                            
                            st.session_state.clicked_numbers.add(i)
                            st.session_state.taken_cards.append(i)
                            st.session_state.card_owner[str(i)] = st.session_state.current_user
                            
                            save_global_cards(st.session_state.taken_cards, st.session_state.card_owner, st.session_state.columns_per_row, st.session_state.timer_start_time, st.session_state.card_selection_time)
                            save_all_data()
                            st.rerun()
                        else:
                            st.error("❌ Insufficient balance! You need at least 10 ETB to select a card.")
    
    if len(st.session_state.clicked_numbers) >= 2:
        st.success("✅ Maximum 2 cards selected! Click a 🟢 GREEN card to DESELECT it (refund 10 ETB).")
    elif len(st.session_state.clicked_numbers) > 0:
        st.info(f"👆 You have {len(st.session_state.clicked_numbers)} card(s) selected. Click a 🟢 GREEN card to DESELECT it (refund 10 ETB)")
    else:
        if balance < 10:
            st.warning("⚠️ Insufficient balance! You need at least 10 ETB to select a card.")
        else:
            st.info("👆 Click a number to select it (max 2 cards). Each card costs 10 ETB.")
    
    progress = 1 - (remaining / CARD_SELECTION_TIME) if remaining > 0 else 1
    st.progress(progress)

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

# Ensure admin balance is always 0
if st.session_state.current_user == "admin":
    balance = 0.0
    if "admin" in st.session_state.user_db:
        st.session_state.user_db["admin"]["balance"] = 0.0
        save_user_db(st.session_state.user_db)

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
# GLOBAL TIMER - CHECK IF SELECTION PHASE SHOULD END
# ===================================================================

if not st.session_state.game_started:
    current_time = time.time()
    elapsed = current_time - st.session_state.timer_start_time
    remaining = max(0, CARD_SELECTION_TIME - elapsed)
    st.session_state.card_selection_time = remaining
    
    # At 0:01 or less - card selection is OVER
    if remaining <= 1:
        st.session_state.selection_phase_ended = True
        save_all_data()
        # Start the game automatically
        if not st.session_state.game_started:
            st.session_state.game_started = True
            st.session_state.auto_call_started = False
            save_all_data()
            st.rerun()

# ===================================================================
# SYNC GLOBAL WINNERS
# ===================================================================

if not st.session_state.winner_declared and not st.session_state.game_started:
    if sync_global_winners():
        st.rerun()

if st.session_state.game_started and not st.session_state.winner_declared:
    if sync_global_winners():
        st.rerun()

# ===================================================================
# AUTO-CALL NUMBERS
# ===================================================================

if st.session_state.game_started and not st.session_state.winner_declared:
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
                save_all_data()
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
                save_all_data()
                st.rerun()

# ===================================================================
# GAME LOOP - ADMIN CANNOT PLAY
# ===================================================================

if st.session_state.current_role == "admin":
    st.info("🔧 Admin Mode - You can manage users and monitor the game.")
    
    if st.session_state.game_started:
        display_master_board()
        
        if st.session_state.winner_declared:
            total_prize = len(st.session_state.taken_cards) * PRIZE_PER_CARD
            prize_per_winner = total_prize // len(st.session_state.winners_list) if st.session_state.winners_list else 0
            
            st.markdown("""
            <div style="background:rgba(255,215,0,0.1);border:2px solid #FFD700;border-radius:15px;padding:20px;text-align:center;margin:20px 0;">
                <h3 style="color:#FFD700;">🏆 Game Finished!</h3>
                <p style="color:rgba(255,255,255,0.8);">Check the winners above.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.winners_list:
                st.markdown("### 🏆 Winners")
                for idx, winner in enumerate(st.session_state.winners_list, 1):
                    patterns = ", ".join(winner.get("patterns", ["BINGO!"]))
                    cards = ", ".join([f"#{c}" for c in winner.get("cards", [])])
                    st.success(f"🎉 Winner {idx}: {winner.get('username')} - Card(s): {cards} - {patterns}")
        
        if st.button("🔄 Start New Game", use_container_width=True):
            # COMPLETE RESET FOR NEW GAME
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
            st.session_state.card_selection_time = CARD_SELECTION_TIME
            st.session_state.timer_start_time = time.time()
            st.session_state.taken_cards = []
            st.session_state.card_owner = {}
            st.session_state.clicked_numbers = set()
            st.session_state.selection_phase_ended = False
            
            clear_global_winners()
            save_global_cards([], {}, 4, st.session_state.timer_start_time, CARD_SELECTION_TIME)
            save_all_data()
            
            st.success("🔄 New game started! Select your cards for the next round.")
            time.sleep(0.5)
            st.rerun()
    else:
        st.info("⏳ Waiting for game to start... Players are selecting cards.")
        total_selected = len(st.session_state.taken_cards)
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.2);border:1px solid rgba(255,215,0,0.1);border-radius:12px;padding:15px;margin:10px 0;">
            <h4 style="color:#FFD700;text-align:center;">📊 Card Selection Status</h4>
            <p style="color:rgba(255,255,255,0.8);text-align:center;">
                Total Cards Selected: <strong style="color:#FFD700;">{total_selected}/201</strong>
            </p>
            <p style="color:rgba(255,255,255,0.6);text-align:center;font-size:0.9rem;">
                Need 3 cards to start the game. Currently: {total_selected}/3
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.current_user == "admin":
        if "admin" in st.session_state.user_db:
            st.session_state.user_db["admin"]["balance"] = 0.0
            save_user_db(st.session_state.user_db)
    
    st.stop()

# ===================================================================
# PLAYER GAME LOOP
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
            st.session_state.card_selection_time = CARD_SELECTION_TIME
            st.session_state.timer_start_time = time.time()
            st.session_state.taken_cards = []
            st.session_state.card_owner = {}
            st.session_state.clicked_numbers = set()
            st.session_state.selection_phase_ended = False
            
            clear_global_winners()
            save_global_cards([], {}, 4, st.session_state.timer_start_time, CARD_SELECTION_TIME)
            save_all_data()
            
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
                st.markdown("### 📋🍀 የእርስዎ ካርቴላ")
                for card_id in all_player_cards:
                    display_selected_card(card_id, list(st.session_state.called_numbers), False)
            else:
                st.warning("⚠️ You don't have any cards in this game!")
                st.info("💡 Wait for the next round to select cards.")
        
        st.info(f"🎯 Auto-calling every 2 seconds... ({len(st.session_state.called_numbers)}/75)")

else:
    if not st.session_state.selection_phase_ended:
        current_time = time.time()
        elapsed = current_time - st.session_state.timer_start_time
        remaining = max(0, CARD_SELECTION_TIME - elapsed)
        
        if remaining <= 1:
            st.session_state.selection_phase_ended = True
            st.session_state.game_started = True
            st.session_state.auto_call_started = False
            save_all_data()
            st.rerun()
        
        st.markdown("## 📋 ካርድዎን ይምረጡ 🔥🚀")
        
        if not st.session_state.game_started:
            render_card_selection()
        else:
            st.session_state.selected_card = list(st.session_state.clicked_numbers)[0] if st.session_state.clicked_numbers else -1
            st.rerun()
    else:
        if not st.session_state.game_started:
            st.info("⏳ Card selection phase has ended. The game is starting...")
            st.markdown("""
            <div style="background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.2);border-radius:12px;padding:20px;text-align:center;margin:20px 0;">
                <h3 style="color:#FFD700;">🔄 Game is starting...</h3>
                <p style="color:rgba(255,255,255,0.7);">The BINGO board will appear shortly.</p>
                <div style="font-size:2rem;margin-top:10px;">🎯</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.game_started = True
            st.session_state.auto_call_started = False
            save_all_data()
            time.sleep(0.5)
            st.rerun()
        else:
            st.session_state.selected_card = list(st.session_state.clicked_numbers)[0] if st.session_state.clicked_numbers else -1
            st.rerun()

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
elif st.session_state.selected_card is None and not st.session_state.game_started:
    time.sleep(0.5)
    st.rerun()
