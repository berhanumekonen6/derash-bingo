import streamlit as st
import streamlit.components.v1 as components
import random
import time
import hashlib
import json
import math
from datetime import datetime, timedelta, timezone
from supabase import create_client

@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SECRET_KEY"]
    return create_client(url, key)

supabase = get_supabase()

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
        transition: transform 0.06s ease, box-shadow 0.06s ease, background 0.06s ease !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) scale(0.95) !important;
        box-shadow: 0 2px 8px rgba(255, 215, 0, 0.4) !important;
    }
    .logo-text h1 { -webkit-text-fill-color: #FFFFFF !important; background: none !important; color: #FFFFFF !important; text-shadow: 0 0 30px rgba(255, 215, 0, 0.1); }
    .logo-text p { color: rgba(255, 255, 255, 0.6) !important; }

    .display-card-circle {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        font-weight: bold;
        font-size: 0.52rem;
        box-sizing: border-box;
        line-height: 1;
    }
    @media (max-width: 768px) {
        .display-card-circle { width: 16px; height: 16px; font-size: 0.46rem; }
    }
    @media (max-width: 480px) {
        .display-card-circle { width: 14px; height: 14px; font-size: 0.42rem; }
    }

    .board-number {
        width: 22px;
        height: 22px;
        font-size: 0.6rem;
    }

    @media (max-width: 768px) {
        .board-table td { padding: 2px 1px; font-size: 0.65rem; min-width: 18px; }
        .board-number { width: 18px; height: 18px; font-size: 0.52rem; }
        .board-table .header-cell { font-size: 0.95rem; padding: 4px 1px; }
        .board-container { padding: 8px !important; margin: 4px 0 !important; }
        .board-title { font-size: 1.1rem !important; }
        .motivation-box { padding: 8px 12px !important; }
        .motivation-box .quote { font-size: 0.85rem !important; }
        h1 { font-size: 1.4rem !important; letter-spacing: 3px !important; }
    }
    @media (max-width: 480px) {
        .board-number { width: 16px; height: 16px; font-size: 0.46rem; }
        .board-table td { padding: 1px 0.5px; }
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
        'insufficient_balance_card_num': None,
        'winner_acknowledged': False,
        '_state_cache': None,
        '_state_cache_at': 0.0,
        '_state_err_count': 0,
        'admin_celebration_msg': None,
        '_local_balance': None,
        'winner_screen_shown_at': None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

# ===================================================================
# SUPABASE — GAME STATE
# ===================================================================
def _default_state():
    return {
        "id": 1,
        "called_numbers": [],
        "last_called_number": None,
        "auto_called_count": 0,
        "game_started": False,
        "auto_call_started": False,
        "last_call_time": time.time(),
        "winner_declared": False,
        "game_over": False,
        "prize_distributed": False,
        "winners_list": [],
        "taken_cards": [],
        "card_owner": {},
        "timer_start_time": time.time(),
        "card_selection_time": 60,
        "last_called_at": 0,
        "last_called_by": None,
    }

def load_state_row(force=False):
    now = time.time()
    cached = st.session_state.get("_state_cache")
    cached_at = st.session_state.get("_state_cache_at", 0.0)

    if not force and cached is not None and (now - cached_at) < 0.3:
        return cached

    last_err = None
    for attempt in range(3):
        try:
            res = supabase.table("game_state").select("*").eq("id", 1).execute()
            if res.data and len(res.data) > 0:
                row = res.data[0]
                st.session_state["_state_cache"] = row
                st.session_state["_state_cache_at"] = time.time()
                st.session_state["_state_err_count"] = 0
                return row
            default = _default_state()
            supabase.table("game_state").upsert(default).execute()
            st.session_state["_state_cache"] = default
            st.session_state["_state_cache_at"] = time.time()
            st.session_state["_state_err_count"] = 0
            return default
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(0.2)

    err_count = st.session_state.get("_state_err_count", 0) + 1
    st.session_state["_state_err_count"] = err_count
    if err_count == 3:
        st.warning(f"⚠️ ግንኙነት ችግር — በራስ-ሰር እየተስተካከለ ነው... ({last_err})")

    if cached is not None:
        return cached
    return _default_state()

def update_state(patch: dict):
    for attempt in range(2):
        try:
            supabase.table("game_state").update(patch).eq("id", 1).execute()
            st.session_state["_state_cache"] = None
            st.session_state["_state_cache_at"] = 0.0
            st.session_state["_state_err_count"] = 0
            return True
        except Exception as e:
            if attempt == 0:
                time.sleep(0.15)
                continue
            err_count = st.session_state.get("_state_err_count", 0) + 1
            st.session_state["_state_err_count"] = err_count
            if err_count == 5:
                st.warning(f"⚠️ የማስቀመጥ ችግር — እንደገና ይሞክሩ ({e})")
            return False

# ===================================================================
# GLOBAL WINNER TRACKING
# ===================================================================
def save_global_winners(winners_list, winner_declared, called_numbers, last_called_number, auto_called_count, game_over, prize_distributed):
    update_state({
        "winners_list": winners_list,
        "winner_declared": winner_declared,
        "called_numbers": list(called_numbers) if called_numbers else [],
        "last_called_number": last_called_number,
        "auto_called_count": auto_called_count,
        "game_over": game_over,
        "prize_distributed": prize_distributed,
    })
    return True

def load_global_winners():
    row = load_state_row()
    return (
        row.get("winners_list") or [],
        row.get("winner_declared", False),
        set(row.get("called_numbers") or []),
        row.get("last_called_number"),
        row.get("auto_called_count", 0),
        row.get("game_over", False),
        row.get("prize_distributed", False),
        row.get("last_call_time", 0),
    )

def sync_global_winners():
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
MIN_CARDS_TO_START = 3
CARD_SELECTION_DURATION = 60

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
# SUPABASE — USERS
# ===================================================================
def load_local_users():
    try:
        res = supabase.table("users").select("*").execute()
        return {r["username"]: r for r in (res.data or [])}
    except Exception:
        return {}

def save_local_users(users):
    try:
        for u, d in users.items():
            supabase.table("users").upsert({
                "username": u,
                "password": d.get("password", ""),
                "balance": float(d.get("balance", 0)),
                "role": d.get("role", "player"),
                "name": d.get("name", ""),
                "phone": d.get("phone", ""),
                "game_played": int(d.get("game_played", 0)),
                "wins": int(d.get("wins", 0)),
            }).execute()
        return True
    except Exception:
        return False

def load_all_data():
    st.session_state.user_db = load_local_users()

def save_all_data():
    if "user_db" in st.session_state and st.session_state.user_db:
        save_local_users(st.session_state.user_db)

# ===================================================================
# FAST USER BALANCE UPDATE
# ===================================================================
def update_user_balance(username, new_balance):
    try:
        supabase.table("users").update({"balance": float(new_balance)}).eq("username", username).execute()
        if username in st.session_state.user_db:
            st.session_state.user_db[username]["balance"] = float(new_balance)
        st.session_state["_local_balance"] = float(new_balance)
        return True
    except Exception:
        return False

# ===================================================================
# FAST CARD SELECT
# ===================================================================
def fast_select_card(card_num, current_balance):
    row = load_state_row(force=True)
    taken = list(row.get("taken_cards") or [])
    owner = dict(row.get("card_owner") or {})
    user = st.session_state.current_user

    if str(card_num) in owner and owner[str(card_num)] != user:
        return False, "taken"
    if card_num in taken and owner.get(str(card_num)) != user:
        return False, "taken"
    user_card_count = sum(1 for o in owner.values() if o == user)
    if user_card_count >= MAX_CARDS_PER_PLAYER:
        return False, "max"
    if current_balance < CARD_PRICE:
        return False, "balance"

    if card_num not in taken:
        taken.append(card_num)
    owner[str(card_num)] = user

    update_state({
        "taken_cards": list(taken),
        "card_owner": dict(owner),
    })
    update_user_balance(user, current_balance - CARD_PRICE)

    st.session_state.taken_cards = taken
    st.session_state.card_owner = owner
    st.session_state.clicked_numbers = set(
        int(k) for k, v in owner.items() if v == user
    )
    return True, "selected"

def fast_deselect_card(card_num, current_balance):
    row = load_state_row(force=True)
    taken = list(row.get("taken_cards") or [])
    owner = dict(row.get("card_owner") or {})
    user = st.session_state.current_user

    if str(card_num) not in owner or owner[str(card_num)] != user:
        return False, "not_owner"

    if card_num in taken:
        taken.remove(card_num)
    del owner[str(card_num)]

    update_state({
        "taken_cards": list(taken),
        "card_owner": dict(owner),
    })
    update_user_balance(user, current_balance + CARD_PRICE)

    st.session_state.taken_cards = taken
    st.session_state.card_owner = owner
    st.session_state.clicked_numbers = set(
        int(k) for k, v in owner.items() if v == user
    )
    return True, "deselected"

# ===================================================================
# GLOBAL CARD TRACKING
# ===================================================================
def load_global_cards():
    row = load_state_row()
    return (
        row.get("taken_cards") or [],
        row.get("card_owner") or {},
        row.get("timer_start_time", time.time()),
        row.get("card_selection_time", CARD_SELECTION_DURATION),
    )

def save_global_cards(taken_cards, card_owner, timer_start_time=None, card_selection_time=None):
    patch = {
        "taken_cards": list(taken_cards),
        "card_owner": dict(card_owner),
    }
    if timer_start_time is not None:
        patch["timer_start_time"] = timer_start_time
    if card_selection_time is not None:
        patch["card_selection_time"] = card_selection_time
    update_state(patch)
    return True

# ===================================================================
# GLOBAL TIMER
# ===================================================================
def load_global_timer():
    row = load_state_row()
    return (
        row.get("timer_start_time", time.time()),
        row.get("card_selection_time", CARD_SELECTION_DURATION),
        row.get("game_started", False),
    )

def save_global_timer(timer_start, duration=CARD_SELECTION_DURATION, game_started=False):
    update_state({
        "timer_start_time": timer_start,
        "card_selection_time": duration,
        "game_started": game_started,
    })
    return True

def reset_global_timer(duration=CARD_SELECTION_DURATION):
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
        total_now = len(file_taken)
        if total_now >= MIN_CARDS_TO_START:
            return 0, False
        else:
            reset_global_timer(CARD_SELECTION_DURATION)
            return CARD_SELECTION_DURATION, False

    return int(math.ceil(remaining)), False

# ===================================================================
# GLOBAL START CONDITION
# ===================================================================
def check_global_start_condition():
    row = load_state_row(force=True)
    global_taken = list(row.get("taken_cards") or [])
    global_count = len(global_taken)

    timer_start = row.get("timer_start_time", time.time())
    duration = row.get("card_selection_time", CARD_SELECTION_DURATION)
    game_started = bool(row.get("game_started", False))

    elapsed = time.time() - timer_start
    remaining = duration - elapsed

    if global_count >= MIN_CARDS_TO_START and (remaining <= 0 or game_started):
        return True, global_count, 0
    if game_started and global_count >= MIN_CARDS_TO_START:
        return True, global_count, max(0, int(math.ceil(remaining)))
    return False, global_count, max(0, int(math.ceil(remaining)))

# ===================================================================
# GLOBAL CALLER LOCK
# ===================================================================
def try_global_call():
    row = load_state_row(force=True)
    if row.get("winner_declared"):
        return None

    now = time.time()
    last_at = row.get("last_called_at", 0) or 0
    if now - last_at < 2.0:
        return None

    update_state({"last_called_at": now, "last_called_by": st.session_state.current_user})

    current_called = set(row.get("called_numbers") or [])
    if len(current_called) >= 75:
        return None
    available = [i for i in range(1, 76) if i not in current_called]
    if not available:
        return None

    called_num = random.choice(available)
    current_called.add(called_num)

    update_state({
        "called_numbers": list(current_called),
        "last_called_number": called_num,
        "auto_called_count": len(current_called),
    })

    st.session_state.called_numbers = current_called
    st.session_state.last_called_number = called_num
    st.session_state.auto_called_count = len(current_called)

    check_for_winners(force_fresh=True)
    return called_num

# ===================================================================
# GAME STATE
# ===================================================================
def save_game_state():
    update_state({
        "called_numbers": list(st.session_state.called_numbers),
        "last_called_number": st.session_state.last_called_number,
        "auto_called_count": st.session_state.auto_called_count,
        "game_started": st.session_state.game_started,
        "auto_call_started": st.session_state.auto_call_started,
        "last_call_time": st.session_state.last_call_time,
        "winner_declared": st.session_state.winner_declared,
        "game_over": st.session_state.game_over,
        "prize_distributed": st.session_state.prize_distributed,
    })

def load_game_state():
    row = load_state_row()
    st.session_state.called_numbers = set(row.get("called_numbers") or [])
    st.session_state.last_called_number = row.get("last_called_number")
    st.session_state.auto_called_count = row.get("auto_called_count", 0)
    st.session_state.auto_call_started = row.get("auto_call_started", False)
    st.session_state.last_call_time = row.get("last_call_time", time.time())
    if not st.session_state.winner_declared:
        st.session_state.winner_declared = row.get("winner_declared", False)
    st.session_state.game_over = row.get("game_over", False)
    st.session_state.prize_distributed = row.get("prize_distributed", False)

def clear_game_state():
    update_state({
        "called_numbers": [],
        "last_called_number": None,
        "auto_called_count": 0,
        "game_started": False,
        "auto_call_started": False,
        "winner_declared": False,
        "game_over": False,
        "prize_distributed": False,
    })
    return True

# ===================================================================
# RESET FOR NEXT ROUND
# ===================================================================
def reset_for_next_round():
    update_state({
        "winners_list": [],
        "winner_declared": False,
        "game_over": False,
        "prize_distributed": False,
        "called_numbers": [],
        "last_called_number": None,
        "auto_called_count": 0,
        "game_started": False,
        "auto_call_started": False,
        "last_called_at": 0,
        "last_called_by": None,
        "taken_cards": [],
        "card_owner": {},
        "timer_start_time": time.time(),
        "card_selection_time": CARD_SELECTION_DURATION,
    })

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
    st.session_state.card_selection_time = CARD_SELECTION_DURATION
    st.session_state.timer_start_time = time.time()
    st.session_state.taken_cards = []
    st.session_state.card_owner = {}
    st.session_state.celebration_start_time = None
    st.session_state.rejected_card_num = None
    st.session_state.insufficient_balance_card_num = None
    st.session_state.winner_acknowledged = False
    st.session_state.winner_screen_shown_at = None

# ===================================================================
# SYNC GLOBAL CARDS
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
    
    current_user = st.session_state.current_user
    if current_user:
        user_cards = set()
        for card_id_str, owner in global_owner.items():
            if owner == current_user:
                try:
                    user_cards.add(int(card_id_str))
                except (ValueError, TypeError):
                    pass
        st.session_state.clicked_numbers = user_cards

# ===================================================================
# START-THE-GAME CHECK
# ===================================================================
def maybe_start_game():
    if st.session_state.game_started:
        return
    file_taken, _, _, _ = load_global_cards()
    total_now = len(file_taken)
    if total_now < MIN_CARDS_TO_START:
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
# ADMIN PANEL — WITH DEPOSIT / WITHDRAW APPROVALS
# ===================================================================
BOT_USERNAME_DISPLAY = "@DerashBingoPlayBot"

def load_transactions(status_filter=None, tx_type=None):
    try:
        q = supabase.table("transactions").select("*").order("created_at", desc=True)
        if status_filter:
            q = q.eq("status", status_filter)
        if tx_type:
            q = q.eq("type", tx_type)
        res = q.execute()
        return res.data or []
    except Exception as e:
        st.warning(f"⚠️ Could not load transactions: {e}")
        return []


def update_transaction(tx_id, patch):
    try:
        supabase.table("transactions").update(patch).eq("id", tx_id).execute()
        return True
    except Exception as e:
        st.error(f"⚠️ Update failed: {e}")
        return False


def approve_transaction(tx):
    username = tx["username"]
    amount = float(tx["amount"])
    tx_type = tx["type"]

    load_all_data()
    if username not in st.session_state.user_db:
        st.error(f"❌ User '{username}' not found in database.")
        return False

    current_balance = float(st.session_state.user_db[username].get("balance", 0))

    if tx_type == "deposit":
        new_balance = current_balance + amount
    else:
        if current_balance < amount:
            st.error(
                f"❌ Insufficient balance for {username}. "
                f"Balance: {current_balance:.2f} ETB, Requested: {amount:.2f} ETB"
            )
            return False
        new_balance = current_balance - amount

    if not update_user_balance(username, new_balance):
        st.error("❌ Failed to update user balance.")
        return False

    ok = update_transaction(tx["id"], {
        "status": "approved",
        "processed_at": datetime.now(timezone.utc).isoformat(),
    })
    return ok


def reject_transaction(tx, note=""):
    ok = update_transaction(tx["id"], {
        "status": "rejected",
        "admin_note": note or "Rejected by admin",
        "processed_at": datetime.now(timezone.utc).isoformat(),
    })
    return ok


def admin_panel():
    if st.session_state.get("admin_celebration_msg"):
        msg = st.session_state["admin_celebration_msg"]
        st.success(msg)
        st.balloons()
        st.session_state["admin_celebration_msg"] = None

    st.markdown("""
    <div class="glass-container">
        <h3 style="color:#FFD700;text-align:center;">🔧 Admin Panel</h3>
        <p style="color:rgba(255,255,255,0.7);text-align:center;">Manage users, deposits & withdrawals.</p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # ✅ ADMIN INFO + LOGOUT (sidebar, matching player style)
    # ============================================================
    st.sidebar.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(255,215,0,0.08),rgba(255,165,0,0.03));padding:1rem;border-radius:12px;border:1px solid rgba(255,215,0,0.1);margin-bottom:15px;">
        <p style="margin:0;font-weight:600;color:#FFD700;">👤 Admin</p>
        <p style="margin:3px 0;color:rgba(255,255,255,0.4);font-size:0.7rem;">🔧 Administrator</p>
        <p style="margin:5px 0;font-size:1.1rem;font-weight:bold;color:#FFD700;">⭐ Full Access</p>
        <p style="margin:3px 0;color:rgba(255,255,255,0.3);font-size:0.7rem;">🎯 Derash BINGO Admin Panel</p>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🚪 Logout", use_container_width=True, key="admin_logout_btn"):
        logout_user()
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.info("🔧 Admin Mode — Manage users & transactions")

    tab_users, tab_deposits, tab_withdrawals, tab_history = st.tabs([
        "👥 Users", "💰 Deposits", "💸 Withdrawals", "📜 History"
    ])

    # ============================
    # TAB 1: USERS
    # ============================
    with tab_users:
        load_all_data()
        users = [u for u in st.session_state.user_db.keys() if u != "admin"]
        if not users:
            st.info("No users registered yet.")
        else:
            selected_user = st.selectbox("Select User", users, key="admin_user_select")
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

                custom_amount = st.number_input("Amount (ETB)", min_value=0, step=10, value=100, key="admin_amt")
                c1, c2, c3 = st.columns(3)

                with c1:
                    if st.button("➕ Add", use_container_width=True, key="admin_add"):
                        new_balance = ud.get("balance", 0) + custom_amount
                        st.session_state.user_db[selected_user]["balance"] = new_balance
                        save_local_users(st.session_state.user_db)
                        st.session_state["admin_celebration_msg"] = (
                            f"🎉 ለ {selected_user} {custom_amount:.2f} ETB ተጨምሯል! አዲስ ሂሳብ: {new_balance:.2f} ETB"
                        )
                        st.rerun()

                with c2:
                    if st.button("💰 Set", use_container_width=True, key="admin_set"):
                        st.session_state.user_db[selected_user]["balance"] = custom_amount
                        save_local_users(st.session_state.user_db)
                        st.session_state["admin_celebration_msg"] = (
                            f"🎉 የ {selected_user} ሂሳብ {custom_amount:.2f} ETB ሆኖ ተቀናብሯል!"
                        )
                        st.rerun()

                with c3:
                    if st.button("➖ Deduct", use_container_width=True, key="admin_deduct"):
                        cur = ud.get("balance", 0)
                        if cur >= custom_amount:
                            new_balance = cur - custom_amount
                            st.session_state.user_db[selected_user]["balance"] = new_balance
                            save_local_users(st.session_state.user_db)
                            st.session_state["admin_celebration_msg"] = (
                                f"✅ ከ {selected_user} {custom_amount:.2f} ETB ተቀንሷል! አዲስ ሂሳብ: {new_balance:.2f} ETB"
                            )
                            st.rerun()
                        else:
                            st.warning("⚠️ በቂ ሂሳብ የለም")

            st.markdown("---")
            total_users = len(users)
            total_balance = sum(float(st.session_state.user_db[u].get("balance", 0)) for u in users)
            st.info(f"👥 Users: {total_users} | 💰 Total Balance: {total_balance:.2f} ETB")

    # ============================
    # TAB 2: DEPOSITS
    # ============================
    with tab_deposits:
        st.markdown("### 💰 Pending Deposit Requests")
        deposits = load_transactions(status_filter="pending", tx_type="deposit")

        if not deposits:
            st.info("✅ No pending deposit requests.")
        else:
            for tx in deposits:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,rgba(76,175,80,0.12),rgba(76,175,80,0.05));
                            padding:15px;border-radius:12px;border:1px solid rgba(76,175,80,0.25);margin-bottom:6px;">
                    <p style="margin:0;font-weight:bold;color:#4CAF50;font-size:1.1rem;">
                        💰 {float(tx['amount']):.2f} ETB — Deposit
                    </p>
                    <p style="margin:5px 0;color:#FFF;">👤 Username: <b>{tx['username']}</b></p>
                    <p style="margin:5px 0;color:rgba(255,255,255,0.7);font-size:0.85rem;">
                        📱 Telegram: {tx.get('telegram_name','N/A')} (ID: {tx.get('telegram_id','')})
                    </p>
                    <p style="margin:5px 0;color:rgba(255,255,255,0.5);font-size:0.8rem;">
                        📅 {tx.get('created_at','')}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                if tx.get("screenshot_url"):
                    st.caption(f"🖼 Telegram file_id: `{tx['screenshot_url']}`")
                    st.markdown(
                        f"👉 [Open bot chat to view screenshot](https://t.me/{BOT_USERNAME_DISPLAY.replace('@','')})"
                    )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Approve #{tx['id']}", key=f"app_dep_{tx['id']}", use_container_width=True):
                        if approve_transaction(tx):
                            st.success(f"✅ Deposit #{tx['id']} approved! {tx['username']} +{float(tx['amount']):.2f} ETB")
                            st.balloons()
                            time.sleep(1.2)
                            st.rerun()
                with col2:
                    if st.button(f"❌ Reject #{tx['id']}", key=f"rej_dep_{tx['id']}", use_container_width=True):
                        if reject_transaction(tx, "Deposit rejected by admin"):
                            st.warning(f"❌ Deposit #{tx['id']} rejected.")
                            time.sleep(0.8)
                            st.rerun()
                st.markdown("---")

    # ============================
    # TAB 3: WITHDRAWALS
    # ============================
    with tab_withdrawals:
        st.markdown("### 💸 Pending Withdrawal Requests")
        withdrawals = load_transactions(status_filter="pending", tx_type="withdraw")

        if not withdrawals:
            st.info("✅ No pending withdrawal requests.")
        else:
            for tx in withdrawals:
                load_all_data()
                user_info = st.session_state.user_db.get(tx["username"], {})
                cur_balance = float(user_info.get("balance", 0))
                amount = float(tx["amount"])
                enough = cur_balance >= amount
                color = "#FF9800" if enough else "#F44336"

                st.markdown(f"""
                <div style="background:linear-gradient(135deg,rgba(255,152,0,0.12),rgba(255,152,0,0.05));
                            padding:15px;border-radius:12px;border:1px solid {color}44;margin-bottom:6px;">
                    <p style="margin:0;font-weight:bold;color:{color};font-size:1.1rem;">
                        💸 {amount:.2f} ETB — Withdrawal
                    </p>
                    <p style="margin:5px 0;color:#FFF;">👤 Username: <b>{tx['username']}</b></p>
                    <p style="margin:5px 0;color:rgba(255,255,255,0.7);font-size:0.85rem;">
                        📞 Phone: {tx.get('phone','')} | 📱 TG: {tx.get('telegram_name','')}
                    </p>
                    <p style="margin:5px 0;color:rgba(255,255,255,0.6);font-size:0.85rem;">
                        💼 Current balance: <b>{cur_balance:.2f} ETB</b>
                        {"✅ sufficient" if enough else "❌ INSUFFICIENT"}
                    </p>
                    <p style="margin:5px 0;color:rgba(255,255,255,0.5);font-size:0.8rem;">
                        📅 {tx.get('created_at','')}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Approve #{tx['id']}", key=f"app_wd_{tx['id']}", use_container_width=True):
                        if approve_transaction(tx):
                            st.success(f"✅ Withdrawal #{tx['id']} approved! {tx['username']} -{amount:.2f} ETB")
                            time.sleep(1.0)
                            st.rerun()
                with col2:
                    if st.button(f"❌ Reject #{tx['id']}", key=f"rej_wd_{tx['id']}", use_container_width=True):
                        if reject_transaction(tx, "Withdrawal rejected by admin"):
                            st.warning(f"❌ Withdrawal #{tx['id']} rejected.")
                            time.sleep(0.8)
                            st.rerun()
                st.markdown("---")

    # ============================
    # TAB 4: HISTORY
    # ============================
    with tab_history:
        st.markdown("### 📜 Processed Transactions")
        approved = load_transactions(status_filter="approved")
        rejected = load_transactions(status_filter="rejected")
        history = approved + rejected

        if not history:
            st.info("No processed transactions yet.")
        else:
            for tx in history[:100]:
                icon = "✅" if tx["status"] == "approved" else "❌"
                tcolor = "#4CAF50" if tx["status"] == "approved" else "#F44336"
                st.markdown(f"""
                <div style="background:rgba(0,0,0,0.2);padding:10px 14px;border-radius:10px;
                            border-left:4px solid {tcolor};margin-bottom:6px;">
                    <p style="margin:0;color:{tcolor};font-weight:bold;">
                        {icon} {tx['type'].title()} — {float(tx['amount']):.2f} ETB
                    </p>
                    <p style="margin:3px 0;color:rgba(255,255,255,0.75);font-size:0.85rem;">
                        👤 {tx['username']} | 📅 {tx.get('processed_at') or tx.get('created_at','')}
                    </p>
                    {f'<p style="margin:3px 0;color:rgba(255,255,255,0.5);font-size:0.8rem;">📝 {tx.get("admin_note","")}</p>' if tx.get("admin_note") else ""}
                </div>
                """, unsafe_allow_html=True)

# ===================================================================
# ALL 204 BINGO CARDS
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
def check_for_winners(force_fresh=False):
    if st.session_state.winner_declared and not force_fresh:
        return

    row = load_state_row(force=True)

    db_called = set(row.get("called_numbers") or [])
    session_called = set(st.session_state.called_numbers or set())
    called_numbers = list(db_called if len(db_called) >= len(session_called) else session_called)

    taken_cards = list(row.get("taken_cards") or [])
    if not taken_cards:
        taken_cards = list(st.session_state.taken_cards or [])

    card_owner = dict(row.get("card_owner") or {})
    if not card_owner:
        card_owner = dict(st.session_state.card_owner or {})

    if not called_numbers or not taken_cards:
        return

    winners_found = []
    for card_id in taken_cards:
        card_data = get_card_data(card_id)
        if not card_data:
            continue
        pattern = check_winning_pattern(card_data, called_numbers)
        if pattern:
            owner = card_owner.get(str(card_id), "Unknown")
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
        st.session_state.called_numbers = set(called_numbers)
        st.session_state.taken_cards = taken_cards
        st.session_state.card_owner = card_owner

        st.session_state.winners_list = winners_found
        st.session_state.winner_declared = True
        st.session_state.game_over = True
        st.session_state.auto_call_started = False
        st.session_state.celebration_start_time = time.time()

        distribute_prizes(winners_found)

        update_state({
            "winners_list": winners_found,
            "winner_declared": True,
            "game_over": True,
            "auto_call_started": False,
            "called_numbers": called_numbers,
            "last_called_number": row.get("last_called_number"),
            "auto_called_count": len(called_numbers),
            "prize_distributed": st.session_state.prize_distributed,
        })

def distribute_prizes(winners):
    _, _, _, _, _, _, global_paid, _ = load_global_winners()
    if global_paid:
        st.session_state.prize_distributed = True
        return

    if st.session_state.prize_distributed:
        return

    total_cards = len(st.session_state.taken_cards)
    total_prize = total_cards * PRIZE_PER_CARD
    prize_per_winner = total_prize // len(winners) if len(winners) > 0 else 0

    load_all_data()

    for winner in winners:
        username = winner.get("username")
        if username in st.session_state.user_db:
            st.session_state.user_db[username]["balance"] = \
                float(st.session_state.user_db[username].get("balance", 0)) + prize_per_winner
            st.session_state.user_db[username]["wins"] = \
                int(st.session_state.user_db[username].get("wins", 0)) + 1
            st.session_state.user_db[username]["game_played"] = \
                int(st.session_state.user_db[username].get("game_played", 0)) + 1

    save_all_data()
    st.session_state.prize_distributed = True
    save_global_winners(
        winners, True,
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
    <div class="{card_class}" style="background:rgba(0,0,0,0.2);border-radius:15px;padding:10px;margin:6px auto;box-shadow:0 4px 12px rgba(0,0,0,0.3);max-width:280px;border:2px solid {border_color};{'animation:winnerPulse 1s ease-in-out infinite alternate;' if is_winner else ''}">
        <div style="text-align:center;color:{title_color};font-size:0.9rem;font-weight:bold;margin-bottom:6px;">
            {'🎊🏆 ' if is_winner else '🎯'} Card #{card_id} { ' 🏆🎊' if is_winner else ''}
        </div>
        <table style="width:100%;border-collapse:collapse;">
            <tr>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:3px 2px;text-align:center;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.65rem;">B</td>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:3px 2px;text-align:center;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.65rem;">I</td>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:3px 2px;text-align:center;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.65rem;">N</td>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:3px 2px;text-align:center;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.65rem;">G</td>
                <td style="border:1px solid rgba(255,255,255,0.08);padding:3px 2px;text-align:center;background:rgba(46,125,50,0.2);color:#FFD700;font-weight:bold;font-size:0.65rem;">O</td>
            </tr>
    """
    for row_idx in range(5):
        html += '<tr>'
        for col_idx in range(5):
            value = cells[row_idx][col_idx]
            if value == 'F':
                html += f'<td style="border:1px solid rgba(255,255,255,0.08);padding:3px 2px;text-align:center;"><div class="display-card-circle" style="background:rgba(255,215,0,0.15);color:#FFD700;font-size:0.85rem;border:2px solid #FFD700;">★</div></td>'
            else:
                num = int(value)
                is_called = num in called_numbers
                style = ''
                if is_called and is_winner:
                    style = 'background:rgba(255,215,0,0.3);color:#FFD700;border-color:#FFD700;'
                elif is_called:
                    style = 'background:rgba(255,152,0,0.2);color:#FFD700;border-color:#FF9800;'
                else:
                    style = 'background:rgba(255,255,255,0.05);color:#FFFFFF;border-color:rgba(255,255,255,0.06);'
                html += f'<td style="border:1px solid rgba(255,255,255,0.08);padding:3px 2px;text-align:center;"><div class="display-card-circle" style="{style}border-width:2px;border-style:solid;">{value}</div></td>'
        html += '</tr>'
    html += '</table>'
    total_called = sum(1 for row in cells for val in row if val != 'F' and int(val) in called_numbers)
    if is_winner and winning_pattern:
        html += f'<div style="text-align:center;color:#FFD700;font-size:0.8rem;margin-top:5px;font-weight:bold;">🎉🏆 WINNER! ({winning_pattern}) 🏆🎉</div>'
        html += f'<div style="text-align:center;color:#FFD700;font-size:0.65rem;margin-top:2px;">🎊🍀 እንኳን ደስ አለዎት!!!🍀🎊</div>'
    else:
        html += f'<div style="text-align:center;color:rgba(255,255,255,0.4);font-size:0.6rem;margin-top:3px;">✅ {total_called}/24 called</div>'
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
        .board-container { max-width: 600px; margin: 0 auto; padding: 12px; background: rgba(0,0,0,0.2); border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.08); }
        .board-title { text-align: center; font-size: 1.4rem; font-weight: bold; color: #FFD700; margin-bottom: 10px; }
        .board-table { width: 100%; border-collapse: collapse; }
        .board-table td { border: 1px solid rgba(255,255,255,0.08); padding: 3px 2px; text-align: center; font-size: 0.75rem; font-weight: bold; min-width: 22px; }
        .board-table .header-cell { background: linear-gradient(135deg, rgba(46,125,50,0.2), rgba(27,94,32,0.1)); color: #FFD700; font-size: 1.2rem; font-weight: 900; padding: 6px 3px; letter-spacing: 3px; }
        .board-number { display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; border-radius: 50%; background: rgba(255,255,255,0.05); color: #FFFFFF; font-weight: bold; font-size: 0.6rem; border: 1px solid rgba(255,255,255,0.06); }
        .board-number.called { background: rgba(255, 152, 0, 0.2); color: #FFD700; border-color: #FF9800; }
        .board-number.last-called { background: rgba(229, 57, 53, 0.2); color: #FF6B6B; border-color: #E53935; }
        .board-stats { text-align: center; margin-top: 10px; font-size: 0.8rem; color: rgba(255,255,255,0.5); padding: 6px; background: rgba(0,0,0,0.15); border-radius: 8px; }
        .board-stats strong { color: #FFD700; }
    </style>
    <div class="board-container">
        <div class="board-title">🎯 BINGO Board</div>
    '''
    if st.session_state.last_called_number:
        letter = get_letter_for_number(st.session_state.last_called_number)
        amharic = get_amharic_number(st.session_state.last_called_number)
        html += f'<div style="text-align:center;font-size:0.95rem;font-weight:bold;color:#FF6B6B;margin-bottom:8px;">🎯 Last Called: <span style="background:rgba(229,57,53,0.15);color:#FF6B6B;padding:2px 12px;border-radius:15px;border:1px solid rgba(229,57,53,0.2);">{st.session_state.last_called_number} ({letter}) - {amharic}</span></div>'
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
    if st.session_state.game_started or st.session_state.winner_declared:
        st.rerun()
        return

    if st.session_state.current_role == "admin":
        st.warning("⚠️ Admin cannot play.")
        return

    if st.session_state.flash_msg:
        st.warning(st.session_state.flash_msg)
        st.session_state.flash_msg = ""

    remaining, _ = get_global_remaining_time()
    if remaining <= 0:
        st.rerun()
        return

    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    time_str = f"{minutes:01d}:{seconds:02d}"

    user = st.session_state.user_db.get(st.session_state.current_user, {})
    balance = user.get("balance", 0)

    file_taken, _, _, _ = load_global_cards()
    total_selected = len(file_taken)
    your_cards = len(st.session_state.clicked_numbers)
    available = 204 - total_selected
    enough_cards = total_selected >= MIN_CARDS_TO_START

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
        st.warning(f"⚠️ Waiting for {MIN_CARDS_TO_START - total_selected} more card(s). Game will start when time hits 0:00 AND 3+ cards are selected! 🎯")
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
    insufficient = st.session_state.insufficient_balance_card_num

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
            is_insufficient = (insufficient == card_num) and not is_mine and not is_taken

            with cols[col_idx]:
                if is_mine:
                    if st.button(f"✅{card_num}", key=f"card_{card_num}", use_container_width=True, type="primary"):
                        user_balance = st.session_state.user_db.get(st.session_state.current_user, {}).get("balance", 0)
                        ok, reason = fast_deselect_card(card_num, user_balance)
                        if ok:
                            st.session_state.rejected_card_num = None
                            st.session_state.insufficient_balance_card_num = None
                            st.session_state.flash_msg = f"✅ Card #{card_num} refunded. +10 ETB"
                        st.rerun()
                elif is_taken:
                    st.button(f"🔴{card_num}", key=f"card_{card_num}", use_container_width=True, disabled=True)
                elif is_rejected:
                    if st.button("🚫 2+ አይቻልም 🚫", key=f"card_{card_num}", use_container_width=True):
                        st.session_state.rejected_card_num = None
                        st.rerun()
                elif is_insufficient:
                    if st.button("⚠️💰ሂሳብዎን ይሙሉ💰⚠️", key=f"card_{card_num}", use_container_width=True):
                        st.session_state.insufficient_balance_card_num = None
                        st.rerun()
                else:
                    if st.button(f"🟡{card_num}", key=f"card_{card_num}", use_container_width=True):
                        user_balance = st.session_state.user_db.get(st.session_state.current_user, {}).get("balance", 0)
                        ok, reason = fast_select_card(card_num, user_balance)
                        if ok:
                            st.session_state.rejected_card_num = None
                            st.session_state.insufficient_balance_card_num = None
                            st.session_state.flash_msg = f"✅ Card #{card_num} selected! -10 ETB"
                        else:
                            if reason == "max":
                                st.session_state.rejected_card_num = card_num
                                st.session_state.insufficient_balance_card_num = None
                            elif reason == "balance":
                                st.session_state.insufficient_balance_card_num = card_num
                                st.session_state.rejected_card_num = None
                            else:
                                st.session_state.flash_msg = f"⚠️ Card #{card_num} already taken!"
                        st.rerun()

    st.progress(1 - (remaining / CARD_SELECTION_DURATION) if remaining > 0 else 0)

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
    st.stop()

# ===================================================================
# USER INFO
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
# GLOBAL GATE
# ===================================================================
_show_game, _g_count, _g_remaining = check_global_start_condition()

if not _show_game:
    if (st.session_state.game_started
            or st.session_state.winner_declared
            or st.session_state.winners_list):
        st.session_state.game_started = False
        st.session_state.winner_declared = False
        st.session_state.game_over = False
        st.session_state.winners_list = []
        st.session_state.winner_acknowledged = False
        st.session_state.selected_card = None
        st.session_state.celebration_start_time = None
        st.session_state.prize_distributed = False

# ===================================================================
# SYNC GLOBAL STATE
# ===================================================================
sync_global_cards()
sync_global_winners()

# ===================================================================
# SESSION SELF-HEAL
# ===================================================================
try:
    _db_row = load_state_row(force=True)
    _db_gs = bool(_db_row.get("game_started", False))
    _db_wd = bool(_db_row.get("winner_declared", False))
    _db_taken = list(_db_row.get("taken_cards") or [])
    _db_called = set(_db_row.get("called_numbers") or [])
    _db_owner = dict(_db_row.get("card_owner") or {})
    _db_winners = _db_row.get("winners_list") or []

    if (not _db_gs) and (not _db_wd):
        if (st.session_state.get("game_started")
                or st.session_state.get("winner_declared")
                or st.session_state.get("winners_list")):
            st.session_state.game_started = False
            st.session_state.winner_declared = False
            st.session_state.game_over = False
            st.session_state.winners_list = []
            st.session_state.called_numbers = set()
            st.session_state.last_called_number = None
            st.session_state.auto_called_count = 0
            st.session_state.auto_call_started = False
            st.session_state.taken_cards = list(_db_taken)
            st.session_state.card_owner = _db_owner
            st.session_state.selected_card = None
            st.session_state.celebration_start_time = None
            st.session_state.prize_distributed = False
            st.session_state.winner_acknowledged = False
            st.session_state.flash_msg = ""
            _cu = st.session_state.current_user
            if _cu:
                _mine = set()
                for _cid_s, _own in _db_owner.items():
                    if _own == _cu:
                        try:
                            _mine.add(int(_cid_s))
                        except (ValueError, TypeError):
                            pass
                st.session_state.clicked_numbers = _mine
            else:
                st.session_state.clicked_numbers = set()
            st.rerun()

    elif _db_gs and not _db_wd:
        st.session_state.game_started = True
        st.session_state.winner_declared = False
        st.session_state.game_over = False
        st.session_state.winners_list = []
        st.session_state.winner_acknowledged = False
        if _db_called:
            st.session_state.called_numbers = _db_called
        st.session_state.taken_cards = _db_taken
        st.session_state.card_owner = _db_owner
        _cu = st.session_state.current_user
        if _cu:
            _mine = set()
            for _cid_s, _own in _db_owner.items():
                if _own == _cu:
                    try:
                        _mine.add(int(_cid_s))
                    except (ValueError, TypeError):
                        pass
            st.session_state.clicked_numbers = _mine

    elif _db_wd:
        if not st.session_state.get("winner_declared"):
            st.session_state.winner_declared = True
            st.session_state.game_started = True
            st.session_state.game_over = True
            st.session_state.winner_acknowledged = False
            if _db_called:
                st.session_state.called_numbers = _db_called
            st.session_state.winners_list = _db_winners
except Exception:
    pass

# ===================================================================
# START THE GAME
# ===================================================================
maybe_start_game()

# ===================================================================
# GLOBAL WINNER OVERLAY
# ===================================================================
if st.session_state.winner_declared and st.session_state.game_started:
    sync_global_winners()
    total_prize = len(st.session_state.taken_cards) * PRIZE_PER_CARD
    prize_per_winner = total_prize // len(st.session_state.winners_list) if st.session_state.winners_list else 0

    # ============================================================
    # ✅ AUTO-RESUME TIMER — 25 seconds countdown
    # ============================================================
    if st.session_state.get("winner_screen_shown_at") is None:
        st.session_state.winner_screen_shown_at = time.time()

    elapsed_w = time.time() - st.session_state.winner_screen_shown_at
    remaining_w = 25 - elapsed_w

    if remaining_w <= 0:
        st.session_state.winner_acknowledged = True
        st.session_state.winner_screen_shown_at = None
        reset_for_next_round()
        st.rerun()

    seconds_left = int(math.ceil(remaining_w))

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
        <div style="font-size:1.2rem;color:#FFD700;margin:10px 0;font-weight:bold;text-shadow:0 0 20px rgba(255,215,0,0.3);">
            🎉🏆ያለዉ ካርቴላ ዉስን ስለሆን ፈጥንው ይምረጡ🏆🎉
        </div>
        <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin:8px 0;">
            <span style="font-size:1.6rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.1s;">👇⭐</span>
            <span style="font-size:1.6rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.7s;">የዚህን ጨዋታ አሸናፊ ካርቴላ ለማየት ከታች ይመልከቱ!</span>
            <span style="font-size:1.6rem;display:inline-block;animation:emojiFloat 2s ease-in-out infinite 0.9s;">🌟👇</span>
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

    st.markdown(f"""
    <div style="text-align:center;margin:25px 0 10px 0;">
        <p style="color:#FFD700;font-size:1.2rem;font-weight:bold;margin:0;">
            ✅ ወደ ካርቴላ ምርጫ ለመመለስ ከታች ያለውን ቁልፍ ይጫኑ
        </p>
        <p style="color:#FF9800;font-size:1rem;font-weight:bold;margin:10px 0 0 0;
                  animation: celebrationPulse 1s ease-in-out infinite alternate;">
            ⏳ በራስ-ሰር ይመለሳል: <span style="font-size:1.5rem;color:#FFD700;">{seconds_left}</span> ሰከንድ
        </p>
        <p style="color:rgba(255,255,255,0.6);font-size:0.85rem;margin:4px 0 0 0;font-style:italic;">
            ⏳ Auto-resume in {seconds_left}s (or click now to resume immediately)
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("🔄 ወደ ካርቴላ ምርጫ ተመለስ (Resume)", use_container_width=True, type="primary", key="global_resume_btn"):
            st.session_state.winner_acknowledged = True
            st.session_state.winner_screen_shown_at = None
            reset_for_next_round()
            st.rerun()

    time.sleep(1)
    st.rerun()
    st.stop()

# ===================================================================
# PLAYER DISPLAY
# ===================================================================
if st.session_state.game_started and _show_game:
    all_player_cards = list(st.session_state.clicked_numbers)

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
        🎯 Playing with {_g_count} Card(s) globally
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
            st.info("💡ጨዋታዉ ተጀምሯል🍀 ካርቴላ ለመምረጥ ቀጣዩን ዙር ይጠብቁ።")
            st.markdown("""
<div style="text-align:center;margin:15px 0 5px 0;">
    <p style="color:#FF9800;font-size:1.1rem;font-weight:bold;margin:0;">
        ⏳ አሸናፊ እስኪታወቅ ይጠብቁ...
    </p>
    <p style="color:rgba(255,255,255,0.7);font-size:0.9rem;margin:6px 0 0 0;">
        🎯 ጨዋታው በመካሄድ ላይ ነው
    </p>
    <p style="color:rgba(255,255,255,0.5);font-size:0.8rem;margin:4px 0 0 0;font-style:italic;">
        ⏳ Waiting for winner to be declared...
    </p>
</div>
""", unsafe_allow_html=True)
            if st.session_state.get("winner_declared", False):
                st.markdown("""
<div style="text-align:center;margin:15px 0 5px 0;">
    <p style="color:#FFD700;font-size:1rem;font-weight:bold;margin:0;">
        ✅ ወደ ካርቴላ ምርጫ ለመመለስ ከታች ያለውን ቁልፍ ይጫኑ
    </p>
</div>
""", unsafe_allow_html=True)
                if st.button("🔄 ወደ ካርቴላ ምርጫ ተመለስ (Resume)", use_container_width=True, type="primary", key="non_player_resume_btn"):
                    reset_for_next_round()
                    st.rerun()

    st.info(f"🎯 Auto-calling every 2 seconds... ({len(st.session_state.called_numbers)}/75)")

else:
    st.session_state.game_started = False
    st.session_state.winner_declared = False
    st.session_state.game_over = False

    st.markdown("## 📋 ካርድዎን ይምረጡ 🔥🚀")
    render_card_selection()
    time.sleep(0.5)
    st.rerun()

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
# AUTO-CALL
# ===================================================================
if st.session_state.game_started and not st.session_state.winner_declared and _show_game:
    _, _gd, _, _, _, _, _, _ = load_global_winners()
    if _gd:
        sync_global_winners()
        st.rerun()
    else:
        sync_global_cards()
        check_for_winners(force_fresh=True)

        if st.session_state.winner_declared:
            st.rerun()

        just_called = try_global_call()
        load_game_state()
        if just_called is not None:
            st.markdown(get_number_sound_js(just_called), unsafe_allow_html=True)
        time.sleep(0.3)
        st.rerun()

# ===================================================================
# AUTO-RERUN
# ===================================================================
if st.session_state.game_started and st.session_state.winner_declared:
    pass
elif not st.session_state.game_started:
    time.sleep(0.5)
    st.rerun()
else:
    time.sleep(0.5)
    st.rerun()
