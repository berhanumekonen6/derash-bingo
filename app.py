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
# VIEWPORT META
# ===================================================================
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
""", unsafe_allow_html=True)

# ===================================================================
# CUSTOM CSS
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
    @keyframes winnerPulse {
        0% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.3); }
        100% { box-shadow: 0 0 60px rgba(255, 215, 0, 0.8); }
    }
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
    .logo-text h1 { -webkit-text-fill-color: #FFFFFF !important; background: none !important; color: #FFFFFF !important; text-shadow: 0 0 30px rgba(255, 215, 0, 0.1); }
    .logo-text p { color: rgba(255, 255, 255, 0.6) !important; }

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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
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
    .stButton > button {
        padding: 6px 3px !important;
        font-size: 13px !important;
        min-height: 44px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {
        margin-bottom: 3px !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# AUDIO FUNCTIONS
# ===================================================================
def get_number_sound_js(number):
    if 1 <= number <= 15: freq = 440
    elif 16 <= number <= 30: freq = 523
    elif 31 <= number <= 45: freq = 659
    elif 46 <= number <= 60: freq = 784
    else: freq = 880
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
            }} catch(e) {{ console.log('Audio play failed:', e); }}
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
            } catch(e) { console.log('Audio play failed:', e); }
        })();
    </script>
    """

# ===================================================================
# SESSION STATE INITIALIZATION
# ===================================================================
def init_session_state():
    defaults = {
        'logged_in': False,
        'current_user': None,
        'current_role': None,
        'clicked_numbers': set(),
        'selected_card': None,
        'called_numbers': set(),
        'last_called_number': None,
        'auto_called_count': 0,
        'last_call_time': time.time(),
        'game_started': False,
        'auto_call_started': False,
        'card_selection_time': 60,
        'card_selection_last_update': time.time(),
        'game_over': False,
        'winners_list': [],
        'winner_declared': False,
        'user_db': {},
        'taken_cards': [],
        'prize_distributed': False,
        'card_owner': {},
        'columns_per_row': 6,
        'timer_start_time': time.time(),
        'show_deposit_msg': False,
        'deposit_msg_text': "",
        'flash_msg': "",
        'celebration_start_time': None,
        'rejected_card_num': None,
        'winner_acknowledged': False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

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
    """✅ Sync winner state — skip if this player already acknowledged."""
    if st.session_state.get("winner_acknowledged", False):
        return False
    
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
    m = {1:"አንድ",2:"ሁለት",3:"ሶስት",4:"አራት",5:"አምስት",6:"ስድስት",7:"ሰባት",8:"ስምንት",9:"ዘጠኝ",10:"አስር",
        11:"አስራ አንድ",12:"አስራ ሁለት",13:"አስራ ሶስት",14:"አስራ አራት",15:"አስራ አምስት",
        16:"አስራ ስድስት",17:"አስራ ሰባት",18:"አስራ ስምንት",19:"አስራ ዘጠኝ",20:"ሃያ",
        21:"ሃያ አንድ",22:"ሃያ ሁለት",23:"ሃያ ሶስት",24:"ሃያ አራት",25:"ሃያ አምስት",
        26:"ሃያ ስድስት",27:"ሃያ ሰባት",28:"ሃያ ስምንት",29:"ሃያ ዘጠኝ",30:"ሰላሳ",
        31:"ሰላሳ አንድ",32:"ሰላሳ ሁለት",33:"ሰላሳ ሶስት",34:"ሰላሳ አራት",35:"ሰላሳ አምስት",
        36:"ሰላሳ ስድስት",37:"ሰላሳ ሰባት",38:"ሰላሳ ስምንት",39:"ሰላሳ ዘጠኝ",40:"አርባ",
        41:"አርባ አንድ",42:"አርባ ሁለት",43:"አርባ ሶስት",44:"አርባ አራት",45:"አርባ አምስት",
        46:"አርባ ስድስት",47:"አርባ ሰባት",48:"አርባ ስምንት",49:"አርባ ዘጠኝ",50:"ሃምሳ",
        51:"ሃምሳ አንድ",52:"ሃምሳ ሁለት",53:"ሃምሳ ሶስት",54:"ሃምሳ አራት",55:"ሃምሳ አምስት",
        56:"ሃምሳ ስድስት",57:"ሃምሳ ሰባት",58:"ሃምሳ ስምንት",59:"ሃምሳ ዘጠኝ",60:"ስድሳ",
        61:"ስድሳ አንድ",62:"ስድሳ ሁለት",63:"ስድሳ ሶስት",64:"ስድሳ አራት",65:"ስድሳ አምስት",
        66:"ስድሳ ስድስት",67:"ስድሳ ሰባት",68:"ስድሳ ስምንት",69:"ስድሳ ዘጠኝ",70:"ሰባ",
        71:"ሰባ አንድ",72:"ሰባ ሁለት",73:"ሰባ ሶስት",74:"ሰባ አራት",75:"ሰባ አምስት"}
    return m.get(num, str(num))

def get_letter_for_number(num):
    if 1 <= num <= 15: return "ቢ"
    elif 16 <= num <= 30: return "አይ"
    elif 31 <= num <= 45: return "ኤን"
    elif 46 <= num <= 60: return "ጂ"
    else: return "ኦ"

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
    st.session_state.user_db = local_users if local_users else {}

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
        data = {"taken_cards": taken_cards, "card_owner": card_owner}
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
# GLOBAL TIMER
# ===================================================================
@st.cache_resource
def _get_shared_timer_store():
    return {"timer_start": time.time(), "duration": 60, "game_started": False}

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
# GLOBAL CALLER LOCK
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
            json.dump({"last_called_at": last_called_at, "last_called_by": last_called_by}, f)
        return True
    except:
        return False

def try_global_call():
    # ✅ STOP calling the moment a winner exists (global or local)
    _, global_winner_done, _, _, _, _, _, _ = load_global_winners()
    if global_winner_done or st.session_state.winner_declared:
        return None

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
# GAME STATE
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
                # ✅ Do NOT overwrite winner_declared here (keep session state clean)
                if not st.session_state.winner_declared:
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
# RESET FOR NEXT ROUND
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
    st.session_state.rejected_card_num = None
    st.session_state.winner_acknowledged = False
    save_game_state()

# ===================================================================
# SYNC GLOBAL CARDS — NO AUTO-RESET (winner state preserved)
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
    
    # ✅ NO AUTO-RESET HERE — reset happens only when a player clicks
    # the Resume button, or when a fresh round begins.
    
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
# START-THE-GAME CHECK
# ===================================================================
def maybe_start_game():
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
    return hash_password(password) == hashed if hashed else False

def login_user(username, password):
    username = username.strip()
    password = password.strip()
    load_all_data()
    
    if username == "admin" and password == "admin123":
        if username not in st.session_state.user_db:
            st.session_state.user_db[username] = {
                "password": hash_password("admin123"),
                "balance": 0.0, "role": "admin",
                "name": "Admin", "phone": "",
                "game_played": 0, "wins": 0
            }
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
        return True, "✅ Admin login successful!"
    
    if username not in st.session_state.user_db:
        return False, "❌ Username not found"
    
    if verify_password(password, st.session_state.user_db[username]["password"]):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.current_role = st.session_state.user_db[username]["role"]
        load_all_data()
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
    st.session_state.user_db[username] = {
        "password": hash_password(password),
        "balance": 0.0, "role": "player",
        "name": name, "phone": phone,
        "game_played": 0, "wins": 0
    }
    save_local_users(st.session_state.user_db)
    load_all_data()
    return True, "✅ Registration successful! Your balance is 0.00 ETB"

def logout_user():
    save_all_data()
    save_game_state()
    save_global_cards(st.session_state.taken_cards, st.session_state.card_owner,
                      st.session_state.timer_start_time, st.session_state.card_selection_time)
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_role = None

# ===================================================================
# ADMIN PANEL (unchanged)
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
    users = [u for u in st.session_state.user_db.keys() if u != "admin"]
    if not users:
        st.info("No users registered yet.")
        return
    selected_user = st.selectbox("Select User", users)
    if selected_user:
        ud = st.session_state.user_db.get(selected_user, {})
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(255,215,0,0.1),rgba(255,165,0,0.05));padding:1rem;border-radius:12px;border:1px solid rgba(255,215,0,0.15);margin-bottom:15px;">
            <p style="margin:0;font-weight:600;color:#FFD700;">👤 {ud.get('name', selected_user)}</p>
            <p style="margin:5px 0;color:rgba(255,255,255,0.7);font-size:0.85rem;">📱 {ud.get('phone', 'N/A')}</p>
            <p style="margin:5px 0;font-size:1.2rem;font-weight:bold;color:#FFD700;">💰 {ud.get('balance', 0):.2f} ETB</p>
            <p style="margin:5px 0;color:rgba(255,255,255,0.5);font-size:0.85rem;">🎮 Games: {ud.get('game_played', 0)} | 🏆 Wins: {ud.get('wins', 0)}</p>
        </div>
        """, unsafe_allow_html=True)
        custom_amount = st.number_input("Amount (ETB)", min_value=0, step=10, value=100)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("➕ Add", use_container_width=True):
                st.session_state.user_db[selected_user]["balance"] = ud.get("balance", 0) + custom_amount
                save_local_users(st.session_state.user_db)
                st.rerun()
        with c2:
            if st.button("💰 Set", use_container_width=True):
                st.session_state.user_db[selected_user]["balance"] = custom_amount
                save_local_users(st.session_state.user_db)
                st.rerun()
        with c3:
            if st.button("➖ Deduct", use_container_width=True):
                cur = ud.get("balance", 0)
                if cur >= custom_amount:
                    st.session_state.user_db[selected_user]["balance"] = cur - custom_amount
                    save_local_users(st.session_state.user_db)
                    st.rerun()

# ===================================================================
# ALL 204 BINGO CARDS — PASTE YOUR EXISTING LIST HERE
# ===================================================================
BINGO_CARDS = [
    {"id": 1, "cells": [['15', '16', '39', '59', '66'], ['11', '28', '40', '51', '68'], ['12', '20', 'F', '56', '67'], ['3', '30', '35', '60', '72'], ['10', '24', '37', '53', '64']]},
    {"id": 2, "cells": [['5', '21', '35', '46', '69'], ['15', '20', '42', '51', '70'], ['10', '28', 'F', '47', '67'], ['2', '26', '31', '49', '64'], ['6', '27', '33', '52', '65']]},
    {"id": 3, "cells": [['14', '23', '40', '58', '62'], ['13', '25', '32', '46', '65'], ['3', '28', 'F', '50', '63'], ['6', '30', '44', '54', '66'], ['10', '16', '37', '53', '74']]},
    {"id": 4, "cells": [['1', '19', '41', '49', '72'], ['5', '26', '36', '50', '69'], ['6', '29', 'F', '60', '61'], ['14', '25', '42', '47', '71'], ['2', '24', '45', '54', '65']]},
    {"id": 5, "cells": [['2', '16', '43', '47', '70'], ['4', '23', '32', '58', '73'], ['9', '17', 'F', '51', '74'], ['1', '26', '34', '59', '75'], ['14', '20', '31', '57', '72']]},
    # ... continue with cards 6 through 204 from your existing file ...
]

# ===================================================================
# WINNER DETECTION
# ===================================================================
def get_card(card_id):
    for card in BINGO_CARDS:
        if card["id"] == card_id:
            return card
    return None

def get_card_data(card_id):
    card = get_card(card_id)
    return card["cells"] if card else None

def check_winning_pattern(card_data, called_numbers):
    if not called_numbers or not card_data:
        return None
    called_set = set(called_numbers)
    def is_marked(value):
        if value == 'F': return True
        return int(value) in called_set
    for row in range(5):
        if all(is_marked(card_data[row][col]) for col in range(5)):
            return {'type': f"Row {row + 1}", 'cells': [card_data[row][col] for col in range(5)]}
    for col in range(5):
        if all(is_marked(card_data[row][col]) for row in range(5)):
            letters = ['B','I','N','G','O']
            return {'type': f"Column {letters[col]}", 'cells': [card_data[row][col] for row in range(5)]}
    if all(is_marked(card_data[i][i]) for i in range(5)):
        return {'type': "Diagonal Main", 'cells': [card_data[i][i] for i in range(5)]}
    if all(is_marked(card_data[i][4 - i]) for i in range(5)):
        return {'type': "Diagonal Anti", 'cells': [card_data[i][4 - i] for i in range(5)]}
    large_corners = [card_data[0][0], card_data[0][4], card_data[4][0], card_data[4][4]]
    if all(is_marked(c) for c in large_corners):
        return {'type': "Large Corners", 'cells': large_corners}
    small_corners = [card_data[1][1], card_data[1][3], card_data[3][1], card_data[3][3]]
    if all(is_marked(c) for c in small_corners):
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
                existing = next((w for w in winners_found if w["username"] == owner), None)
                if existing:
                    existing["cards"].append(card_id)
                    existing["patterns"].append(pattern['type'])
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
            winners_found, True,
            st.session_state.called_numbers,
            st.session_state.last_called_number,
            st.session_state.auto_called_count,
            True, st.session_state.prize_distributed
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
        st.session_state.winners_list, True,
        st.session_state.called_numbers,
        st.session_state.last_called_number,
        st.session_state.auto_called_count,
        True, True
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
    border_color = '#FFD700' if is_winner else 'rgba(255,255,255,0.1)'
    title_color = '#FFD700' if is_winner else '#FFFFFF'
    card_class = 'winner-card' if is_winner else ''
    html = f"""
    <div class="{card_class}" style="background:rgba(0,0,0,0.2);border-radius:15px;padding:12px;margin:8px auto;box-shadow:0 4px 12px rgba(0,0,0,0.3);max-width:400px;border:2px solid {border_color};{'animation:winnerPulse 1s ease-in-out infinite alternate;' if is_winner else ''}">
        <div style="text-align:center;color:{title_color};font-size:1rem;font-weight:bold;margin-bottom:8px;">
            {'🎊🏆 ' if is_winner else '🎯'} Card #{card_id} { ' 🏆🎊' if is_winner else ''}
        </div>
        <table style="width:100%;border-collapse:collapse;">
            <tr>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:4px 2px;text-align:center;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.75rem;">B</td>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:4px 2px;text-align:center;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.75rem;">I</td>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:4px 2px;text-align:center;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.75rem;">N</td>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:4px 2px;text-align:center;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.75rem;">G</td>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:4px 2px;text-align:center;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.75rem;">O</td>
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
        html += f'<div style="text-align:center;color:#FFD700;font-size:0.9rem;margin-top:6px;font-weight:bold;">🎉🏆 WINNER! ({winning_pattern}) 🏆🎉</div>'
        html += f'<div style="text-align:center;color:#FFD700;font-size:0.7rem;margin-top:2px;">🎊🍀 እንኳን ደስ አለዎት!!!🍀🎊</div>'
    else:
        html += f'<div style="text-align:center;color:rgba(255,255,255,0.4);font-size:0.65rem;margin-top:4px;">✅ {total_called}/24 called</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def display_master_board():
    if not st.session_state.winner_declared:
        sync_global_winners()
    master_board = {
        'B': list(range(1, 16)), 'I': list(range(16, 31)),
        'N': list(range(31, 46)), 'G': list(range(46, 61)),
        'O': list(range(61, 76))
    }
    called_numbers = list(st.session_state.called_numbers)
    html = '''
    <style>
        .board-container { max-width: 950px; margin: 0 auto; padding: 20px; background: rgba(0,0,0,0.2); border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.08); }
        .board-title { text-align: center; font-size: 1.8rem; font-weight: bold; color: #FFD700; margin-bottom: 12px; }
        .board-table { width: 100%; border-collapse: collapse; }
        .board-table td { border: 1px solid rgba(255,255,255,0.08); padding: 6px 4px; text-align: center; font-size: 0.85rem; font-weight: bold; min-width: 30px; }
        .board-table .header-cell { background: linear-gradient(135deg, rgba(46,125,50,0.2), rgba(27,94,32,0.1)); color: #FFD700; font-size: 1.5rem; font-weight: 900; padding: 10px 4px; letter-spacing: 3px; }
        .board-number { display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.05); color: #FFFFFF; font-weight: bold; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.06); }
        .board-number.called { background: rgba(255, 152, 0, 0.2); color: #FFD700; border-color: #FF9800; }
        .board-number.last-called { background: rgba(229, 57, 53, 0.2); color: #FF6B6B; border-color: #E53935; }
        .board-stats { text-align: center; margin-top: 12px; font-size: 0.9rem; color: rgba(255,255,255,0.5); padding: 8px; background: rgba(0,0,0,0.15); border-radius: 8px; }
        .board-stats strong { color: #FFD700; }
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
# CARD SELECTION
# ===================================================================
def render_card_selection():
    if not st.session_state.game_started:
        _ft, _, _, _ = load_global_cards()
        _tn = max(len(_ft), len(st.session_state.clicked_numbers))
        _rem, _ = get_global_remaining_time()
        if _tn >= 3 and _rem <= 0:
            mark_game_started_globally()
            st.session_state.game_started = True
            st.session_state.auto_call_started = False
            st.session_state.selected_card = list(st.session_state.clicked_numbers)[0] if len(st.session_state.clicked_numbers) > 0 else -1
            save_game_state()
            st.rerun()
            return

    if st.session_state.current_role == "admin":
        st.warning("⚠️ Admin cannot play.")
        return

    if st.session_state.flash_msg:
        st.warning(st.session_state.flash_msg)
        st.session_state.flash_msg = ""

    remaining = st.session_state.card_selection_time
    if remaining <= 0:
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
    enough_cards = total_selected >= 3

    color = "#FFD700" if enough_cards and remaining > 30 else ("#FF9800" if remaining <= 30 else "#FFD700")

    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.15);padding:12px 15px;border-radius:12px;border:1px solid rgba(255,255,255,0.08);margin-bottom:15px;text-align:center;">
        <div style="font-size:1.6rem;font-weight:bold;color:{color};font-family:monospace;margin-bottom:6px;">⌚ {time_str}</div>
        <div style="font-size:0.9rem;color:#FFFFFF;line-height:1.9;">
            🟢 <b>Your Cards:</b> {your_cards}/2 &nbsp;|&nbsp;
            📊 <b>Global:</b> {total_selected}/204 &nbsp;|&nbsp;
            ⬜ <b>Available:</b> {available}
        </div>
        <div style="font-size:1rem;color:#FFD700;margin-top:6px;font-weight:bold;">💰 {balance:.2f} ETB</div>
    </div>
    """, unsafe_allow_html=True)

    if not enough_cards:
        st.warning(f"⚠️ Waiting for {3 - total_selected} more card(s). Game will start when time hits 0:00 AND 3+ cards are selected! 🎯")
    else:
        st.success(f"✅ 3+ cards ready! Game will start when the timer hits 0:00 — {int(remaining)}s remaining 🎯")

    col_options = [4, 5, 6, 7, 8]
    current_value = st.session_state.columns_per_row if st.session_state.columns_per_row in col_options else 6
    selected_cols = st.selectbox(
        f"📊 Cards per row (current: {current_value})",
        options=col_options,
        index=col_options.index(current_value),
        key=f"cards_per_row_{st.session_state.current_user}"
    )
    if selected_cols != st.session_state.columns_per_row:
        st.session_state.columns_per_row = selected_cols
        st.rerun()

    cols_per_row = st.session_state.columns_per_row
    clicked = st.session_state.clicked_numbers
    taken = st.session_state.taken_cards
    rejected = st.session_state.rejected_card_num

    st.markdown("""
    <div style="background:rgba(0,0,0,0.15);border-radius:12px;padding:8px;border:1px solid rgba(255,255,255,0.08);margin-bottom:8px;">
        <div style="text-align:center;font-size:0.9rem;color:#FFD700;font-weight:bold;">🎯 Tap a card to SELECT (10 ETB)</div>
    </div>
    """, unsafe_allow_html=True)

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
                    if st.button(f"✅{card_num}", key=f"card_{card_num}", use_container_width=True, type="primary"):
                        user_balance = st.session_state.user_db.get(st.session_state.current_user, {}).get("balance", 0)
                        st.session_state.clicked_numbers.discard(card_num)
                        if card_num in st.session_state.taken_cards:
                            st.session_state.taken_cards.remove(card_num)
                        if str(card_num) in st.session_state.card_owner:
                            del st.session_state.card_owner[str(card_num)]
                        st.session_state.user_db[st.session_state.current_user]["balance"] = user_balance + 10
                        save_all_data()
                        save_global_cards(st.session_state.taken_cards, st.session_state.card_owner,
                                          st.session_state.timer_start_time, st.session_state.card_selection_time)
                        st.session_state.rejected_card_num = None
                        st.session_state.flash_msg = f"✅ Card #{card_num} refunded. +10 ETB"
                        st.rerun()
                elif is_taken:
                    st.button(f"🔴{card_num}", key=f"card_{card_num}", use_container_width=True, disabled=True)
                elif is_rejected:
                    if st.button("🚫 2+ አይቻልም 🚫", key=f"card_{card_num}", use_container_width=True):
                        st.session_state.rejected_card_num = None
                        st.rerun()
                else:
                    if st.button(f"🟡{card_num}", key=f"card_{card_num}", use_container_width=True):
                        user_balance = st.session_state.user_db.get(st.session_state.current_user, {}).get("balance", 0)
                        has_max = len(st.session_state.clicked_numbers) >= MAX_CARDS_PER_PLAYER
                        if has_max:
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
                            save_global_cards(st.session_state.taken_cards, st.session_state.card_owner,
                                              st.session_state.timer_start_time, st.session_state.card_selection_time)
                            st.session_state.rejected_card_num = None
                            st.session_state.flash_msg = f"✅ Card #{card_num} selected! -10 ETB"
                        st.rerun()

    st.progress(1 - (remaining / 60) if remaining > 0 else 0)

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
    🎯🍀 <h1 style="font-family:'Orbitron',sans-serif;font-weight:900;font-size:2.2rem;background:linear-gradient(135deg,#FFD700,#FFA500,#FFD700);background-size:300% 300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:6px;margin:0;">
        ደራሽ ቢንጎ -Derash BINGO 
    </h1>
    <p style="color:rgba(255,255,255,0.6);font-size:0.9rem;letter-spacing:3px;margin-top:-3px;">@2026</p>
</div>
""", unsafe_allow_html=True)

# ===================================================================
# LOGIN / REGISTER
# ===================================================================
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    with tab1:
        with st.form("login_form"):
            username = st.text_input("👤 Username")
            password = st.text_input("🔑 Password", type="password")
            submitted = st.form_submit_button("🎰 Login")
            if submitted and username and password:
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
            full_name = st.text_input("👤 Full Name")
            username = st.text_input("👤 Username")
            phone = st.text_input("📱 Phone")
            password = st.text_input("🔑 Password", type="password")
            confirm = st.text_input("✅ Confirm Password", type="password")
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
# SYNC GLOBAL STATE
# ===================================================================
sync_global_cards()
sync_global_winners()

# ===================================================================
# START THE GAME
# ===================================================================
maybe_start_game()

# ===================================================================
# ADMIN VIEW
# ===================================================================
if st.session_state.current_role == "admin":
    st.info("🔧 Admin Mode")
    if st.session_state.game_started:
        display_master_board()
        if st.session_state.winner_declared and st.session_state.winners_list:
            st.markdown("### 🏆 Winners")
            for idx, w in enumerate(st.session_state.winners_list, 1):
                st.success(f"🎉 Winner {idx}: {w.get('username')} - Cards: {w.get('cards')} - {', '.join(w.get('patterns', []))}")
    else:
        st.info("⏳ Waiting for game to start...")
    st.stop()

# ===================================================================
# ✅ PLAYER DISPLAY
# ===================================================================
if st.session_state.game_started:
    all_player_cards = list(st.session_state.clicked_numbers)
    
    # ✅ Always rebuild this player's cards from the shared file
    if st.session_state.current_user:
        _gt, _go, _, _ = load_global_cards()
        _my = []
        for _cid_str, _owner in _go.items():
            if _owner == st.session_state.current_user:
                try:
                    _my.append(int(_cid_str))
                except (ValueError, TypeError):
                    pass
        if _my:
            _my = sorted(set(_my))
            st.session_state.clicked_numbers = set(_my)
            all_player_cards = _my
    
    # ==============================================================
    # ✅ WINNER DECLARED — celebration for EVERY player
    # ==============================================================
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
        <div style="background:linear-gradient(135deg, rgba(255,215,0,0.2), rgba(255,165,0,0.1));
                    border:4px solid #FFD700;border-radius:20px;padding:20px 12px;margin:15px 0;
                    text-align:center;box-shadow: 0 0 60px rgba(255,215,0,0.4);
                    animation: celebrationPulse 0.8s ease-in-out infinite alternate;">
            <div style="font-size:3rem;color:#FFD700;letter-spacing:8px;">🎉🎊🏆👑🎊🎉</div>
            <div style="font-size:2rem;color:#FFD700;margin:8px 0;font-weight:900;">🎉 ቢንጎ! አሸናፊዉ ታዉቋል!!! 🎉</div>
            <div style="font-size:1.3rem;color:#FFD700;margin:6px 0;">🎊🍀🥳 ለቀጣይ ጨዋታ መልካም ዕድል!!! 🥳🍀🎊</div>
            <div style="display:flex;justify-content:center;gap:15px;flex-wrap:wrap;margin:12px 0;">
                <span style="font-size:2rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite;">🎉</span>
                <span style="font-size:2rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.2s;">🎊</span>
                <span style="font-size:2rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.4s;">🏆</span>
                <span style="font-size:2rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.6s;">👑</span>
                <span style="font-size:2rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.8s;">🥳</span>
                <span style="font-size:2rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 1s;">🎉</span>
            </div>
            <div style="font-size:1.4rem;color:#FFFFFF;margin:10px 0;padding:10px;background:rgba(0,0,0,0.25);border-radius:12px;">
                🏆 አሸናፊ: <span style="color:#FFD700;font-weight:900;">{winner_names_str}</span> 🏆
            </div>
            <div style="font-size:1.1rem;color:#4CAF50;margin:6px 0;font-weight:bold;">
                💰 ሽልማት: <strong style="color:#FFD700;">{prize_per_winner:.2f} ETB</strong>
            </div>
            <div style="font-size:1.2rem;color:#FFD700;margin:8px 0;padding:6px;background:rgba(255,215,0,0.1);border-radius:10px;">
                🏅 የድል መንገድ: {winning_pattern}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        st.snow()
        
        st.markdown("""
        <div style="text-align:center;margin:20px 0 15px 0;">
            <h2 style="color:#FFD700;font-size:1.8rem;">🎉🏆 የአሸናፊዎች ካርቴላ 🏆🎉</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.winners_list:
            wcp = {}
            for winner in st.session_state.winners_list:
                for cid in winner.get("cards", []):
                    wcp[cid] = ", ".join(winner.get("patterns", ["BINGO!"]))
            for i in range(0, len(all_winner_cards), 3):
                chunk = all_winner_cards[i:i+3]
                card_cols = st.columns(len(chunk))
                for idx, cid in enumerate(chunk):
                    with card_cols[idx]:
                        display_selected_card(cid, list(st.session_state.called_numbers), True, wcp.get(cid, "BINGO!"))
        
        if st.session_state.winners_list:
            st.markdown("### 🏆 አሸናፊዎች 🏆")
            for idx, winner in enumerate(st.session_state.winners_list, 1):
                patterns = ", ".join(winner.get("patterns", ["BINGO!"]))
                cards = ", ".join([f"#{c}" for c in winner.get("cards", [])])
                st.success(f"🎉 {winner.get('username')} - Card(s): {cards} - {patterns} 🎉")
        
        # ✅ RESUME BUTTON
        st.markdown("""
        <div style="text-align:center;margin:25px 0 10px 0;">
            <p style="color:#FFD700;font-size:1.2rem;font-weight:bold;margin:0;">
                ✅ ወደ ካርቴላ ምርጫ ለመመለስ ከታች ያለውን ቁልፍ ይጫኑ
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            if st.button("🔄 ወደ ካርቴላ ምርጫ ተመለስ (Resume)", use_container_width=True, type="primary", key="resume_btn"):
                st.session_state.winner_acknowledged = True
                reset_for_next_round()
                st.rerun()
    
    # ==============================================================
    # ✅ GAME RUNNING — board + player's own cards
    # ==============================================================
    else:
        # Rebuild from shared file every tick
        if st.session_state.current_user:
            _gt, _go, _, _ = load_global_cards()
            _my = []
            for _cid_str, _owner in _go.items():
                if _owner == st.session_state.current_user:
                    try:
                        _my.append(int(_cid_str))
                    except (ValueError, TypeError):
                        pass
            if _my:
                _my = sorted(set(_my))
                st.session_state.clicked_numbers = set(_my)
                all_player_cards = _my
        
        st.markdown(f"""
        <div style="background:rgba(46,125,50,0.1);border:1px solid rgba(255,215,0,0.05);padding:8px 15px;border-radius:10px;text-align:center;margin-bottom:15px;font-size:0.9rem;color:rgba(255,255,255,0.8);">
            🎯 Playing with {len(st.session_state.taken_cards)} Card(s) globally
            <span style="margin-left:12px;background:rgba(255,215,0,0.08);padding:2px 10px;border-radius:12px;">
                {len(st.session_state.called_numbers)}/75 Called
            </span>
            <span style="margin-left:8px;background:rgba(76,175,80,0.15);padding:2px 10px;border-radius:12px;color:#4CAF50;">
                ✅ Your Cards: {len(all_player_cards)}/2
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        board_col, cards_col = st.columns([2, 1], gap="large")
        with board_col:
            display_master_board()
        with cards_col:
            st.markdown("### 📋🍀 የእርስዎ ካርቴላ/ዎች")
            if all_player_cards:
                for cid in all_player_cards:
                    display_selected_card(cid, list(st.session_state.called_numbers), False)
            else:
                st.warning("⚠️በዚህ ዙር ጨዋታ ካርቴላ አልመረጡም!")
        
        st.info(f"🎯 Auto-calling every 2 seconds... ({len(st.session_state.called_numbers)}/75)")

else:
    if st.session_state.card_selection_time <= 0 and len(st.session_state.taken_cards) >= 3:
        st.session_state.game_started = True
        st.session_state.auto_call_started = False
        st.rerun()
    if not st.session_state.game_started:
        st.markdown("## 📋 ካርድዎን ይምረጡ 🔥🚀")
        render_card_selection()

# ===================================================================
# FOOTER
# ===================================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:rgba(255,255,255,0.3);font-size:0.75rem;padding:15px;">
    🎯 Derash BINGO | 204 Cards | Selected: {len(st.session_state.clicked_numbers)}/2 | Called: {len(st.session_state.called_numbers)}/75
</div>
""", unsafe_allow_html=True)

# ===================================================================
# ✅ AUTO-CALL — stops the moment a winner exists
# ===================================================================
if st.session_state.game_started and not st.session_state.winner_declared:
    _, _gd, _, _, _, _, _, _ = load_global_winners()
    if _gd:
        sync_global_winners()
        st.rerun()
    else:
        just_called = try_global_call()
        load_game_state()
        if just_called is not None:
            st.markdown(get_number_sound_js(just_called), unsafe_allow_html=True)
        time.sleep(0.5)
        st.rerun()

# ===================================================================
# ✅ AUTO-RERUN
# ===================================================================
if st.session_state.game_started and st.session_state.winner_declared:
    pass  # Wait for Resume button
elif not st.session_state.game_started:
    maybe_start_game()
    time.sleep(1)
    st.rerun()
