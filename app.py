import streamlit as st
import streamlit.components.v1 as components
import random
import time
import hashlib
import json
import math
from datetime import datetime, timedelta, timezone
from supabase import create_client

st.set_page_config(
    page_title="ደራሽ ቢንጎ🍀",
    page_icon="🎯🍀",
    layout="wide"
)

@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SECRET_KEY"]
    return create_client(url, key)

supabase = get_supabase()

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
# CUSTOM CSS  (unchanged from your version)
# ===================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Ethiopic:wght@400;500;700;900&display=swap');

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
    h1, h2, h3, h4, p, label, .stMarkdown, .stText, .stButton > button, input, textarea, select {
        color: #FFFFFF !important;
        font-family: 'Noto Sans Ethiopic', 'Segoe UI', Arial, sans-serif !important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stPasswordInput"] input,
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    .stTextInput input,
    .stPasswordInput input,
    input[type="text"],
    input[type="password"],
    textarea {
        background-color: rgba(0, 0, 0, 0.45) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        caret-color: #FFD700 !important;
        border: 1px solid rgba(255, 215, 0, 0.35) !important;
        border-radius: 10px !important;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stPasswordInput"] input:focus,
    div[data-baseweb="input"] input:focus,
    .stTextInput input:focus,
    .stPasswordInput input:focus,
    input[type="text"]:focus,
    input[type="password"]:focus {
        border: 1px solid #FFD700 !important;
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.25) !important;
        background-color: rgba(0, 0, 0, 0.55) !important;
    }
    div[data-testid="stTextInput"] input::placeholder,
    div[data-testid="stPasswordInput"] input::placeholder,
    .stTextInput input::placeholder,
    .stPasswordInput input::placeholder,
    input::placeholder {
        color: rgba(255, 255, 255, 0.45) !important;
        -webkit-text-fill-color: rgba(255, 255, 255, 0.45) !important;
        opacity: 1 !important;
    }
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    input:-webkit-autofill:active {
        -webkit-text-fill-color: #FFFFFF !important;
        -webkit-box-shadow: 0 0 0 1000px rgba(0, 0, 0, 0.55) inset !important;
        box-shadow: 0 0 0 1000px rgba(0, 0, 0, 0.55) inset !important;
        transition: background-color 5000s ease-in-out 0s;
        caret-color: #FFD700 !important;
    }
    div[data-baseweb="input"],
    div[data-baseweb="base-input"] {
        background-color: rgba(0, 0, 0, 0.45) !important;
        border-radius: 10px !important;
    }
    div[data-testid="stTextInput"] label,
    div[data-testid="stPasswordInput"] label,
    .stTextInput label,
    .stPasswordInput label {
        color: #FFD700 !important;
        font-weight: 600 !important;
    }
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
    div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stFormSubmitButton"] button *,
    .stFormSubmitButton > button,
    .stFormSubmitButton > button *,
    button[kind="formSubmit"],
    button[kind="formSubmit"] *,
    div[data-testid="stForm"] button,
    div[data-testid="stForm"] button * {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #1a1a2e !important;
        -webkit-text-fill-color: #1a1a2e !important;
        font-weight: 900 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 12px !important;
        min-height: 48px !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.25) !important;
        text-shadow: none !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover,
    div[data-testid="stForm"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.35) !important;
    }
    div[data-testid="stFormSubmitButton"] button:active,
    div[data-testid="stForm"] button:active {
        transform: translateY(0px) scale(0.97) !important;
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
    .board-number { width: 22px; height: 22px; font-size: 0.6rem; }
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
        div[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 3px !important; }
        div[data-testid="stHorizontalBlock"] > div { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
        div[data-testid="stHorizontalBlock"] .stButton > button {
            padding: 4px 1px !important; font-size: 11px !important;
            min-height: 42px !important; height: 42px !important;
            line-height: 1.1 !important; border-radius: 6px !important;
        }
    }
    .stButton > button {
        padding: 6px 3px !important; font-size: 13px !important;
        min-height: 44px !important; border-radius: 8px !important;
        font-weight: bold !important;
    }
    div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {
        margin-bottom: 3px !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# AUDIO
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
# SESSION STATE — only transient UI values, NOT game state
# ===================================================================
def init_session_state():
    defaults = {
        'logged_in': False,
        'current_user': None,
        'current_role': None,
        'user_db': {},
        'flash_msg': "",
        'rejected_card_num': None,
        'insufficient_balance_card_num': None,
        'columns_per_row': 6,
        'show_deposit_msg': False,
        'deposit_msg_text': "",
        'admin_celebration_msg': None,
        'bot_apply_flash': None,
        'admin_bot_card_count': 0,
        '_first_render_done': False,
        # local mirrors, purely for display between reads
        '_last_sound_played_for': None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

if "_first_render_done" not in st.session_state:
    st.session_state["_first_render_done"] = False

# ===================================================================
# SUPABASE — GLOBAL GAME STATE  (single source of truth)
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

def _sanitize_row(row):
    if not isinstance(row, dict):
        return _default_state()
    cn = row.get("called_numbers")
    if isinstance(cn, list):
        try:
            unique_cn = []
            seen = set()
            for x in cn:
                xi = int(x)
                if xi not in seen and 1 <= xi <= 75:
                    seen.add(xi)
                    unique_cn.append(xi)
            row["called_numbers"] = unique_cn
        except Exception:
            row["called_numbers"] = []
    try:
        lca = float(row.get("last_called_at") or 0)
    except Exception:
        lca = 0.0
    row["last_called_at"] = lca
    if row.get("game_over") and not row.get("winner_declared"):
        row["game_over"] = False
    return row

def load_state_row(force=True):
    """Always read from DB. Cached only for the lifetime of a single script run
    unless force=True is passed again after a write."""
    now = time.time()
    cached = st.session_state.get("_state_cache")
    cached_at = st.session_state.get("_state_cache_at", 0.0)
    _first_render = st.session_state.get("_first_render_done", False)
    ttl = 1.5 if not _first_render else 0.25
    if (not force) and cached is not None and (now - cached_at) < ttl:
        return cached

    last_err = None
    for attempt in range(3):
        try:
            res = supabase.table("game_state").select("*").eq("id", 1).execute()
            if res.data and len(res.data) > 0:
                row = _sanitize_row(res.data[0])
                st.session_state["_state_cache"] = row
                st.session_state["_state_cache_at"] = time.time()
                return row
            default = _default_state()
            supabase.table("game_state").upsert(default).execute()
            st.session_state["_state_cache"] = default
            st.session_state["_state_cache_at"] = time.time()
            return default
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(0.1)

    if cached is not None:
        return cached
    return _default_state()

def update_state(patch: dict):
    for attempt in range(2):
        try:
            supabase.table("game_state").update(patch).eq("id", 1).execute()
            st.session_state["_state_cache"] = None
            st.session_state["_state_cache_at"] = 0.0
            return True
        except Exception:
            if attempt == 0:
                time.sleep(0.1)
                continue
            return False

# ===================================================================
# GAME CONSTANTS
# ===================================================================
CARD_PRICE = 10
PRIZE_PER_CARD = 8
MAX_CARDS_PER_PLAYER = 2
MIN_CARDS_TO_START = 3
CARD_SELECTION_DURATION = 60
CALL_INTERVAL = 3.0          # seconds between numbers — global, DB-driven
LEADER_TIMEOUT = 4.5         # if leader silent this long, someone else takes over
WINNER_SCREEN_SECONDS = 10   # celebration duration per round

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

def load_single_user(username):
    try:
        res = supabase.table("users").select("*").eq("username", username).execute()
        if res.data and len(res.data) > 0:
            return res.data[0]
    except Exception:
        pass
    return None

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

def update_user_balance(username, new_balance):
    try:
        supabase.table("users").update({"balance": float(new_balance)}).eq("username", username).execute()
        if username in st.session_state.user_db:
            st.session_state.user_db[username]["balance"] = float(new_balance)
        return True
    except Exception:
        return False

# ===================================================================
# GLOBAL STATE ACCESSORS
# ===================================================================
def get_taken_cards_and_owner():
    row = load_state_row()
    taken = list(row.get("taken_cards") or [])
    owner = dict(row.get("card_owner") or {})
    return taken, owner

def get_called_numbers():
    row = load_state_row()
    return set(int(x) for x in (row.get("called_numbers") or []))

def get_last_called_number():
    row = load_state_row()
    return row.get("last_called_number")

def get_winner_state():
    row = load_state_row()
    return (
        row.get("winners_list") or [],
        bool(row.get("winner_declared", False)),
        bool(row.get("game_over", False)),
        bool(row.get("prize_distributed", False)),
    )

def get_game_started():
    row = load_state_row()
    return bool(row.get("game_started", False))

def get_user_cards(username):
    _, owner = get_taken_cards_and_owner()
    if not username:
        return []
    out = []
    for k, v in owner.items():
        if v == username:
            try:
                out.append(int(k))
            except (ValueError, TypeError):
                pass
    return sorted(set(out))

# ===================================================================
# TIMER — computed from DB
# ===================================================================
def get_remaining_seconds():
    row = load_state_row()
    if row.get("game_started", False):
        return 0
    timer_start = float(row.get("timer_start_time") or time.time())
    duration = float(row.get("card_selection_time") or CARD_SELECTION_DURATION)
    remaining = duration - (time.time() - timer_start)
    if remaining <= 0:
        return 0
    return int(math.floor(remaining + 0.001))

def reset_timer(duration=CARD_SELECTION_DURATION):
    update_state({
        "timer_start_time": time.time(),
        "card_selection_time": duration,
        "game_started": False,
    })

def start_game_globally():
    row = load_state_row(force=True)
    update_state({
        "game_started": True,
        "auto_call_started": True,
        "last_call_time": time.time(),
        "last_called_at": 0,
        "last_called_by": None,
    })

# ===================================================================
# CARD SELECTION / DESELECTION  (writes to DB)
# ===================================================================
def select_card_for_user(card_num, current_balance):
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

    ok = update_state({
        "taken_cards": list(taken),
        "card_owner": dict(owner),
    })
    if not ok:
        return False, "error"
    update_user_balance(user, current_balance - CARD_PRICE)
    return True, "selected"

def deselect_card_for_user(card_num, current_balance):
    row = load_state_row(force=True)
    taken = list(row.get("taken_cards") or [])
    owner = dict(row.get("card_owner") or {})
    user = st.session_state.current_user

    if str(card_num) not in owner or owner[str(card_num)] != user:
        return False, "not_owner"
    if card_num in taken:
        taken.remove(card_num)
    owner.pop(str(card_num), None)

    ok = update_state({
        "taken_cards": list(taken),
        "card_owner": dict(owner),
    })
    if not ok:
        return False, "error"
    update_user_balance(user, current_balance + CARD_PRICE)
    return True, "deselected"

# ===================================================================
# BOT CARDS — ADMIN
# ===================================================================
BOT_NAMES = [
    "Bekele", "Alemu", "Aster", "Yednekachew", "Tigist", "Getachew",
    "Meseret", "Dawit", "Hana", "Solomon", "Marta", "Kebede",
    "Selam", "Tesfaye", "Meron", "Abebe", "Hiwot", "Girma",
    "Bethlehem", "Yohannes", "Rahel", "Mulugeta", "Eden", "Fikadu",
    "Tsehay", "Berhanu", "Liya", "Assefa", "Genet", "Wondimu",
    "Sara", "Desta", "Mahlet", "Tewodros", "Kidist", "Bantayehu",
    "Eyerusalem", "Endale", "Mekdes", "Samuel", "Zewditu", "Nardos",
    "Bereket", "Alemitu", "Yonas", "Wubit", "Henok", "Tizita",
    "Melaku", "Netsanet", "Biniam", "Aynalem", "Eyob", "Sindu",
    "Gedion", "Mimi", "Natnael", "Tsedale", "Firaol", "Rediet",
    "Bruk", "Sifen", "Naol", "Hermela", "Yafet", "Lidiya",
    "Ebisa", "Ruth", "Kaleab", "Beza", "Yared", "Eleni",
    "Abel", "Feven", "Mikiyas", "Saron", "Yosef", "Meron",
    "Dagmawi", "Tinsae", "Luel", "Tsion", "Nahom", "Sena",
    "Kaleb", "Bethany", "Ermias", "Ruhama", "Yosef", "Mimi",
    "Andualem", "Mieraf", "Mulu", "Habtamu", "Frehiwot", "Tadesse",
    "Zerihun", "Aregash", "Mulugeta", "Tigabu", "Lulit", "Bonsa",
]

BOT_SUFFIXES = [
    "_b", "_ad", "_x7", "_z9", "_m2", "_k4", "_p5", "_t8",
    "_g3", "_n6", "_r1", "_v0", "_w9", "_y5", "_q7", "_s4",
    "_c8", "_d2", "_e6", "_f3", "_h1", "_j9", "_l0", "_u7",
]

def make_bot_username(base_name, index=0):
    suffix = BOT_SUFFIXES[index % len(BOT_SUFFIXES)]
    return base_name + suffix

def is_bot_username(username):
    if not username:
        return False
    name = str(username)
    return any(name.endswith(sfx) for sfx in BOT_SUFFIXES)

def get_or_create_bot_users(count):
    load_all_data()
    if count > len(BOT_NAMES):
        count = len(BOT_NAMES)
    available_names = list(BOT_NAMES)
    random.shuffle(available_names)
    bot_users = []
    for i in range(count):
        base_name = available_names[i]
        bot_username = make_bot_username(base_name, i)
        if bot_username not in st.session_state.user_db:
            st.session_state.user_db[bot_username] = {
                "password": hashlib.sha256((bot_username + "_secret_" + str(i)).encode()).hexdigest(),
                "balance": 10000.0,
                "role": "player",
                "name": "🤖 " + base_name,
                "phone": "",
                "game_played": 0,
                "wins": 0,
            }
        bot_users.append(bot_username)
    save_local_users(st.session_state.user_db)
    return bot_users

def assign_bot_cards(bot_count):
    if bot_count <= 0:
        return 0, "No bot count selected"
    row = load_state_row(force=True)
    taken = list(row.get("taken_cards") or [])
    owner = dict(row.get("card_owner") or {})
    bot_owned = [k for k, v in owner.items() if is_bot_username(v)]
    for k in bot_owned:
        try:
            cid = int(k)
            if cid in taken:
                taken.remove(cid)
        except (ValueError, TypeError):
            pass
        owner.pop(k, None)
    bot_users = get_or_create_bot_users(bot_count)
    available_cards = [i for i in range(1, 205) if i not in taken]
    random.shuffle(available_cards)
    assigned = 0
    for i, bot_name in enumerate(bot_users):
        if not available_cards:
            break
        card_num = available_cards.pop()
        taken.append(card_num)
        owner[str(card_num)] = bot_name
        assigned += 1
    update_state({
        "taken_cards": list(taken),
        "card_owner": dict(owner),
    })
    return assigned, f"🤖 Assigned {assigned} bot card(s) — visible to all players as 🔴 selected"

def remove_bot_cards():
    row = load_state_row(force=True)
    taken = list(row.get("taken_cards") or [])
    owner = dict(row.get("card_owner") or {})
    bot_cards = [k for k, v in owner.items() if is_bot_username(v)]
    for k in bot_cards:
        try:
            cid = int(k)
            if cid in taken:
                taken.remove(cid)
        except (ValueError, TypeError):
            pass
        owner.pop(k, None)
    update_state({
        "taken_cards": list(taken),
        "card_owner": dict(owner),
    })
    return len(bot_cards)

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
        if value == 'F':
            return True
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

def scan_for_winner():
    """Read DB, scan all taken cards, write winner back if found.
    Returns the winners list (or []) — same result for every caller because it reads DB."""
    row = load_state_row(force=True)
    if row.get("winner_declared", False):
        return row.get("winners_list") or []

    called = set(int(x) for x in (row.get("called_numbers") or []))
    taken = list(row.get("taken_cards") or [])
    owner = dict(row.get("card_owner") or {})
    if not called or not taken:
        return []

    winners_found = []
    for card_id in taken:
        try:
            cid = int(card_id)
        except (ValueError, TypeError):
            continue
        card_data = get_card_data(cid)
        if not card_data:
            continue
        pattern = check_winning_pattern(card_data, called)
        if pattern:
            owner_name = owner.get(str(cid), "Unknown")
            existing = next((w for w in winners_found if w["username"] == owner_name), None)
            if existing:
                existing["cards"].append(cid)
                existing["patterns"].append(pattern['type'])
            else:
                winners_found.append({
                    "username": owner_name,
                    "cards": [cid],
                    "patterns": [pattern['type']],
                    "card_data": card_data
                })

    if winners_found:
        distribute_prizes(winners_found, taken)
        update_state({
            "winners_list": winners_found,
            "winner_declared": True,
            "game_over": True,
            "auto_call_started": False,
            "last_called_by": None,
            "prize_distributed": True,
        })
        return winners_found
    return []

def distribute_prizes(winners, taken_cards):
    total_cards = len(taken_cards) if taken_cards else 0
    total_prize = total_cards * PRIZE_PER_CARD
    prize_per_winner = total_prize // len(winners) if winners else 0
    load_all_data()
    for winner in winners:
        username = winner.get("username")
        if username in st.session_state.user_db:
            cur = float(st.session_state.user_db[username].get("balance", 0))
            st.session_state.user_db[username]["balance"] = cur + prize_per_winner
            st.session_state.user_db[username]["wins"] = int(st.session_state.user_db[username].get("wins", 0)) + 1
            st.session_state.user_db[username]["game_played"] = int(st.session_state.user_db[username].get("game_played", 0)) + 1
    save_all_data()

# ===================================================================
# GLOBAL CALLER ELECTION + CALL
# ===================================================================
def try_global_call():
    """Single caller elected by DB row. Every client tries, but only the one
    that succeeds in writing becomes the leader for this tick."""
    row = load_state_row(force=True)
    if row.get("winner_declared"):
        return None
    if not row.get("game_started"):
        return None

    now = time.time()
    my_user = st.session_state.current_user or "anon"

    last_at = float(row.get("last_called_at") or 0)
    last_by = row.get("last_called_by")

    # Not yet time for the next call — everyone waits
    if last_at > 0 and (now - last_at) < CALL_INTERVAL:
        return None

    # If another user called recently, don't steal the slot
    if last_by and last_by != my_user and last_at > 0 and (now - last_at) < LEADER_TIMEOUT:
        return None

    current_called = set(int(x) for x in (row.get("called_numbers") or []))
    if len(current_called) >= 75:
        update_state({"game_over": True})
        return None

    available = [i for i in range(1, 76) if i not in current_called]
    if not available:
        return None

    called_num = random.choice(available)
    new_called = sorted(current_called | {called_num})

    ok = update_state({
        "called_numbers": new_called,
        "last_called_number": called_num,
        "auto_called_count": len(new_called),
        "last_called_at": now,
        "last_called_by": my_user,
    })
    if not ok:
        return None

    # Immediately check for a winner after this call
    scan_for_winner()
    return called_num

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
    if username == "admin" and password == "admin123":
        admin_row = load_single_user("admin")
        if admin_row is None:
            new_admin = {
                "username": "admin",
                "password": hash_password("admin123"),
                "balance": 0.0, "role": "admin",
                "name": "Admin", "phone": "",
                "game_played": 0, "wins": 0
            }
            try:
                supabase.table("users").upsert(new_admin).execute()
            except Exception:
                pass
            st.session_state.user_db = {"admin": new_admin}
        else:
            admin_row["balance"] = 0.0
            st.session_state.user_db = {"admin": admin_row}
        st.session_state.logged_in = True
        st.session_state.current_user = "admin"
        st.session_state.current_role = "admin"
        return True, "✅ Admin login successful!"

    user = load_single_user(username)
    if not user:
        return False, "❌ Username not found"
    if verify_password(password, user.get("password", "")):
        st.session_state.user_db = {username: user}
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.current_role = user.get("role", "player")
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
    if is_bot_username(username) or username in BOT_NAMES:
        return False, "❌ This username is reserved"
    if load_single_user(username) is not None:
        return False, "❌ Username already exists"
    new_user = {
        "username": username,
        "password": hash_password(password),
        "balance": 0.0, "role": "player",
        "name": name, "phone": phone,
        "game_played": 0, "wins": 0
    }
    try:
        supabase.table("users").upsert(new_user).execute()
    except Exception:
        return False, "❌ Registration failed"
    st.session_state.user_db = {username: new_user}
    return True, "✅ Registration successful! Your balance is 0.00 ETB"

def logout_user():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_role = None

# ===================================================================
# DISPLAY
# ===================================================================
def display_selected_card(card_id, called_numbers=None, is_winner=False, winning_pattern=None):
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

def display_master_board(called_numbers, last_called_number):
    master_board = {
        'B': list(range(1, 16)), 'I': list(range(16, 31)),
        'N': list(range(31, 46)), 'G': list(range(46, 61)),
        'O': list(range(61, 76))
    }
    html = (
        '<style>'
        '.board-container { max-width: 600px; margin: 0 auto; padding: 12px; background: rgba(0,0,0,0.2); border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.08); }'
        '.board-title { text-align: center; font-size: 1.4rem; font-weight: bold; color: #FFD700; margin-bottom: 10px; }'
        '.board-table { width: 100%; border-collapse: collapse; }'
        '.board-table td { border: 1px solid rgba(255,255,255,0.08); padding: 3px 2px; text-align: center; font-size: 0.75rem; font-weight: bold; min-width: 22px; }'
        '.board-table .header-cell { background: linear-gradient(135deg, rgba(46,125,50,0.2), rgba(27,94,32,0.1)); color: #FFD700; font-size: 1.2rem; font-weight: 900; padding: 6px 3px; letter-spacing: 3px; }'
        '.board-number { display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; border-radius: 50%; background: rgba(255,255,255,0.05); color: #FFFFFF; font-weight: bold; font-size: 0.6rem; border: 1px solid rgba(255,255,255,0.06); }'
        '.board-number.called { background: rgba(255, 152, 0, 0.2); color: #FFD700; border-color: #FF9800; }'
        '.board-number.last-called { background: rgba(229, 57, 53, 0.2); color: #FF6B6B; border-color: #E53935; }'
        '.board-stats { text-align: center; margin-top: 10px; font-size: 0.8rem; color: rgba(255,255,255,0.5); padding: 6px; background: rgba(0,0,0,0.15); border-radius: 8px; }'
        '.board-stats strong { color: #FFD700; }'
        '</style>'
        '<div class="board-container">'
        '<div class="board-title">🎯 BINGO Board</div>'
    )
    if last_called_number:
        letter = get_letter_for_number(last_called_number)
        amharic = get_amharic_number(last_called_number)
        html += (
            '<div style="text-align:center;font-size:0.95rem;font-weight:bold;color:#FF6B6B;margin-bottom:8px;">'
            '🎯 Last Called: <span style="background:rgba(229,57,53,0.15);color:#FF6B6B;padding:2px 12px;border-radius:15px;border:1px solid rgba(229,57,53,0.2);">'
            + str(last_called_number) + ' (' + letter + ') - ' + amharic +
            '</span></div>'
        )
    html += '<table class="board-table"><tr>'
    for letter in ['B', 'I', 'N', 'G', 'O']:
        html += '<td class="header-cell">' + letter + '</td>'
    html += '</tr>'
    for row in range(15):
        html += '<tr>'
        for letter in ['B', 'I', 'N', 'G', 'O']:
            num = master_board[letter][row]
            is_called = num in called_numbers
            is_last = num == last_called_number
            if is_last:
                html += '<td><div class="board-number last-called">' + str(num) + '</div></td>'
            elif is_called:
                html += '<td><div class="board-number called">' + str(num) + '</div></td>'
            else:
                html += '<td><div class="board-number">' + str(num) + '</div></td>'
        html += '</tr>'
    html += '</table>'
    html += '<div class="board-stats">📊 Called: <strong>' + str(len(called_numbers)) + '</strong> / 75 numbers</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ===================================================================
# MAIN
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
                        time.sleep(0.6)
                        st.rerun()
                    else:
                        st.error(message)
    st.stop()

# ===================================================================
# ADMIN PANEL (UNCHANGED from previous version — kept compact here)
# ===================================================================
def load_transactions(status_filter=None, tx_type=None):
    try:
        q = supabase.table("transactions").select("*").order("created_at", desc=True)
        if status_filter:
            q = q.eq("status", status_filter)
        if tx_type:
            q = q.eq("type", tx_type)
        res = q.execute()
        return res.data or []
    except Exception:
        return []

def update_transaction(tx_id, patch):
    try:
        supabase.table("transactions").update(patch).eq("id", tx_id).execute()
        return True
    except Exception:
        return False

def approve_transaction(tx):
    username = tx["username"]
    amount = float(tx["amount"])
    tx_type = tx["type"]
    user_row = load_single_user(username)
    if user_row is None:
        st.error(f"❌ User '{username}' not found in database.")
        return False
    current_balance = float(user_row.get("balance", 0))
    if tx_type == "deposit":
        new_balance = current_balance + amount
    else:
        if current_balance < amount:
            st.error(f"❌ Insufficient balance for {username}.")
            return False
        new_balance = current_balance - amount
    if not update_user_balance(username, new_balance):
        st.error("❌ Failed to update user balance.")
        return False
    return update_transaction(tx["id"], {
        "status": "approved",
        "processed_at": datetime.now(timezone.utc).isoformat(),
    })

def reject_transaction(tx, note=""):
    return update_transaction(tx["id"], {
        "status": "rejected",
        "admin_note": note or "Rejected by admin",
        "processed_at": datetime.now(timezone.utc).isoformat(),
    })

BOT_USERNAME_DISPLAY = "@DerashBingoPlayBot"

def admin_panel():
    if st.session_state.get("bot_apply_flash"):
        flash = st.session_state["bot_apply_flash"]
        st.success(flash["msg"])
        st.session_state["bot_apply_flash"] = None
    if st.session_state.get("admin_celebration_msg"):
        msg = st.session_state["admin_celebration_msg"]
        st.success(msg)
        st.session_state["admin_celebration_msg"] = None

    st.markdown("""
    <div class="glass-container">
        <h3 style="color:#FFD700;text-align:center;">🔧 Admin Panel</h3>
        <p style="color:rgba(255,255,255,0.7);text-align:center;">Manage users, deposits & withdrawals.</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
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

    tab_users, tab_bots, tab_deposits, tab_withdrawals, tab_history = st.tabs([
        "👥 Users", "🤖 Bot Cards", "💰 Deposits", "💸 Withdrawals", "📜 History"
    ])

    with tab_users:
        load_all_data()
        users = [u for u in st.session_state.user_db.keys() if u != "admin" and not is_bot_username(u)]
        if not users:
            st.info("No users registered yet.")
        else:
            selected_user = st.selectbox("Select User", users, key="admin_user_select")
            if selected_user:
                ud = st.session_state.user_db.get(selected_user, {})
                st.markdown("""
                <div style="background:linear-gradient(135deg,rgba(255,215,0,0.1),rgba(255,165,0,0.05));padding:1rem;border-radius:12px;border:1px solid rgba(255,215,0,0.15);margin-bottom:15px;">
                    <p style="margin:0;font-weight:600;color:#FFD700;">👤 {}</p>
                    <p style="margin:5px 0;color:rgba(255,255,255,0.7);font-size:0.85rem;">📱 {}</p>
                    <p style="margin:5px 0;font-size:1.2rem;font-weight:bold;color:#FFD700;">💰 {:.2f} ETB</p>
                    <p style="margin:5px 0;color:rgba(255,255,255,0.5);font-size:0.85rem;">🎮 Games: {} | 🏆 Wins: {}</p>
                </div>
                """.format(
                    ud.get('name', selected_user),
                    ud.get('phone', 'N/A'),
                    ud.get('balance', 0),
                    ud.get('game_played', 0),
                    ud.get('wins', 0)
                ), unsafe_allow_html=True)

                custom_amount = st.number_input("Amount (ETB)", min_value=0, step=10, value=100, key="admin_amt")
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("➕ Add", use_container_width=True, key="admin_add"):
                        new_balance = ud.get("balance", 0) + custom_amount
                        st.session_state.user_db[selected_user]["balance"] = new_balance
                        save_local_users(st.session_state.user_db)
                        st.session_state["admin_celebration_msg"] = (
                            "🎉 ለ " + selected_user + " " + f"{custom_amount:.2f}" + " ETB ተጨምሯል!"
                        )
                        st.rerun()
                with c2:
                    if st.button("💰 Set", use_container_width=True, key="admin_set"):
                        st.session_state.user_db[selected_user]["balance"] = custom_amount
                        save_local_users(st.session_state.user_db)
                        st.session_state["admin_celebration_msg"] = (
                            "🎉 የ " + selected_user + " ሂሳብ " + f"{custom_amount:.2f}" + " ETB ሆኖ ተቀናብሯል!"
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
                                "✅ ከ " + selected_user + " " + f"{custom_amount:.2f}" + " ETB ተቀንሷል!"
                            )
                            st.rerun()
                        else:
                            st.warning("⚠️ በቂ ሂሳብ የለም")

    with tab_bots:
        st.markdown("### 🤖 Bot Card Selection")
        st.markdown(
            "<p style='color:rgba(255,255,255,0.7);font-size:0.9rem;'>"
            "Select how many bot cards to auto-assign. Each bot gets 1 card.</p>",
            unsafe_allow_html=True,
        )
        row_b = load_state_row(force=True)
        current_bot_cards = sum(1 for v in (row_b.get("card_owner") or {}).values() if is_bot_username(v))
        total_taken_b = len(row_b.get("taken_cards") or [])
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(33,150,243,0.12),rgba(33,150,243,0.05));
                    padding:14px;border-radius:12px;border:1px solid rgba(33,150,243,0.25);margin-bottom:12px;">
            <p style="margin:0;color:#2196F3;font-weight:bold;font-size:1.05rem;">
                🤖 Active Bot Cards: {}
            </p>
            <p style="margin:5px 0 0 0;color:rgba(255,255,255,0.65);font-size:0.85rem;">
                📊 Total taken cards: {} / 204
            </p>
        </div>
        """.format(current_bot_cards, total_taken_b), unsafe_allow_html=True)
        bot_options = list(range(0, 101, 2))
        default_index = 0
        if current_bot_cards in bot_options:
            default_index = bot_options.index(current_bot_cards)
        st.selectbox("🔢 Select number of bot cards", options=bot_options, index=default_index, key="admin_bot_card_count")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("✅ Apply Bot Cards", use_container_width=True, type="primary", key="admin_apply_bots"):
                selected_bot_count = st.session_state.get("admin_bot_card_count", 0)
                if selected_bot_count == 0:
                    removed = remove_bot_cards()
                    st.session_state["bot_apply_flash"] = {"msg": f"🗑️ Removed {removed} bot card(s)."}
                else:
                    assigned, msg = assign_bot_cards(selected_bot_count)
                    st.session_state["bot_apply_flash"] = {"msg": f"✅ {msg}"}
                st.rerun()
        with col_b2:
            if st.button("🗑️ Remove All Bot Cards", use_container_width=True, key="admin_clear_bots"):
                removed = remove_bot_cards()
                st.session_state["bot_apply_flash"] = {"msg": f"🗑️ Removed {removed} bot card(s)."}
                st.rerun()
        st.markdown("---")
        st.info("💡 Bot cards count toward the 3-card minimum to start the game.")

    with tab_deposits:
        st.markdown("### 💰 Pending Deposit Requests")
        deposits = load_transactions(status_filter="pending", tx_type="deposit")
        if not deposits:
            st.info("✅ No pending deposit requests.")
        else:
            for tx in deposits:
                st.markdown("""
                <div style="background:linear-gradient(135deg,rgba(76,175,80,0.12),rgba(76,175,80,0.05));
                            padding:15px;border-radius:12px;border:1px solid rgba(76,175,80,0.25);margin-bottom:6px;">
                    <p style="margin:0;font-weight:bold;color:#4CAF50;font-size:1.1rem;">
                        💰 {:.2f} ETB — Deposit
                    </p>
                    <p style="margin:5px 0;color:#FFF;">👤 Username: <b>{}</b></p>
                    <p style="margin:5px 0;color:rgba(255,255,255,0.7);font-size:0.85rem;">
                        📱 Telegram: {} (ID: {})
                    </p>
                    <p style="margin:5px 0;color:rgba(255,255,255,0.5);font-size:0.8rem;">
                        📅 {}
                    </p>
                </div>
                """.format(
                    float(tx['amount']),
                    tx['username'],
                    tx.get('telegram_name', 'N/A'),
                    tx.get('telegram_id', ''),
                    tx.get('created_at', '')
                ), unsafe_allow_html=True)
                if tx.get("screenshot_url"):
                    st.caption("🖼 Telegram file_id: `" + str(tx['screenshot_url']) + "`")
                    st.markdown("👉 [Open bot chat to view screenshot](https://t.me/" + BOT_USERNAME_DISPLAY.replace('@','') + ")")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Approve #" + str(tx['id']), key="app_dep_" + str(tx['id']), use_container_width=True):
                        if approve_transaction(tx):
                            st.session_state["admin_celebration_msg"] = (
                                "✅ Deposit #" + str(tx['id']) + " approved!"
                            )
                            st.rerun()
                with col2:
                    if st.button("❌ Reject #" + str(tx['id']), key="rej_dep_" + str(tx['id']), use_container_width=True):
                        if reject_transaction(tx, "Deposit rejected by admin"):
                            st.session_state["admin_celebration_msg"] = (
                                "❌ Deposit #" + str(tx['id']) + " rejected."
                            )
                            st.rerun()
                st.markdown("---")

    with tab_withdrawals:
        st.markdown("### 💸 Pending Withdrawal Requests")
        withdrawals = load_transactions(status_filter="pending", tx_type="withdraw")
        if not withdrawals:
            st.info("✅ No pending withdrawal requests.")
        else:
            for tx in withdrawals:
                user_info = load_single_user(tx["username"]) or {}
                cur_balance = float(user_info.get("balance", 0))
                amount = float(tx["amount"])
                enough = cur_balance >= amount
                color = "#FF9800" if enough else "#F44336"
                st.markdown("""
                <div style="background:linear-gradient(135deg,rgba(255,152,0,0.12),rgba(255,152,0,0.05));
                            padding:15px;border-radius:12px;border:1px solid {c}44;margin-bottom:6px;">
                    <p style="margin:0;font-weight:bold;color:{c};font-size:1.1rem;">
                        💸 {amt:.2f} ETB — Withdrawal
                    </p>
                    <p style="margin:5px 0;color:#FFF;">👤 Username: <b>{u}</b></p>
                    <p style="margin:5px 0;color:rgba(255,255,255,0.6);font-size:0.85rem;">
                        💼 Current balance: <b>{cb:.2f} ETB</b> {suf}
                    </p>
                </div>
                """.format(c=color, amt=amount, u=tx['username'], cb=cur_balance,
                           suf=("✅ sufficient" if enough else "❌ INSUFFICIENT")),
                unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Approve #" + str(tx['id']), key="app_wd_" + str(tx['id']), use_container_width=True):
                        if approve_transaction(tx):
                            st.session_state["admin_celebration_msg"] = (
                                "✅ Withdrawal #" + str(tx['id']) + " approved!"
                            )
                            st.rerun()
                with col2:
                    if st.button("❌ Reject #" + str(tx['id']), key="rej_wd_" + str(tx['id']), use_container_width=True):
                        if reject_transaction(tx, "Withdrawal rejected by admin"):
                            st.session_state["admin_celebration_msg"] = (
                                "❌ Withdrawal #" + str(tx['id']) + " rejected."
                            )
                            st.rerun()
                st.markdown("---")

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
                st.markdown("""
                <div style="background:rgba(0,0,0,0.2);padding:10px 14px;border-radius:10px;
                            border-left:4px solid {tc};margin-bottom:6px;">
                    <p style="margin:0;color:{tc};font-weight:bold;">
                        {ic} {ty} — {amt:.2f} ETB
                    </p>
                    <p style="margin:3px 0;color:rgba(255,255,255,0.75);font-size:0.85rem;">
                        👤 {u} | 📅 {dt}
                    </p>
                </div>
                """.format(tc=tcolor, ic=icon, ty=tx['type'].title(),
                           amt=float(tx['amount']), u=tx['username'],
                           dt=(tx.get('processed_at') or tx.get('created_at',''))),
                unsafe_allow_html=True)

if st.session_state.current_role == "admin":
    admin_panel()
    st.stop()

# ===================================================================
# USER SIDEBAR
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

my_cards = get_user_cards(st.session_state.current_user)
st.sidebar.markdown("---")
st.sidebar.info(f"📋 Selected: {len(my_cards)}/2 cards")

# ===================================================================
# READ GLOBAL STATE FRESH ON EVERY RENDER
# ===================================================================
row = load_state_row(force=True)

taken_cards = list(row.get("taken_cards") or [])
card_owner = dict(row.get("card_owner") or {})
called_numbers = set(int(x) for x in (row.get("called_numbers") or []))
last_called_number = row.get("last_called_number")
game_started = bool(row.get("game_started", False))
winner_declared = bool(row.get("winner_declared", False))
winners_list = row.get("winners_list") or []
game_over = bool(row.get("game_over", False))

# ===================================================================
# WINNER OVERLAY (any player sees it)
# ===================================================================
if winner_declared and game_started:
    st.markdown(get_winner_sound_js(), unsafe_allow_html=True)

    total_prize = len(taken_cards) * PRIZE_PER_CARD
    prize_per_winner = total_prize // len(winners_list) if winners_list else 0

    winning_patterns = []
    winner_names = []
    all_winner_cards = []
    for w in winners_list:
        winning_patterns.extend(w.get("patterns", []))
        winner_names.append(w.get("username", "Unknown"))
        all_winner_cards.extend(w.get("cards", []))
    winning_pattern = ", ".join(winning_patterns) if winning_patterns else "BINGO!"
    winner_names_str = ", ".join(winner_names)

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

    if winners_list:
        wcp = {}
        for w in winners_list:
            for cid in w.get("cards", []):
                wcp[cid] = ", ".join(w.get("patterns", ["BINGO!"]))
        for i in range(0, len(all_winner_cards), 3):
            chunk = all_winner_cards[i:i+3]
            cols = st.columns(len(chunk))
            for idx, cid in enumerate(chunk):
                with cols[idx]:
                    display_selected_card(cid, list(called_numbers), True, wcp.get(cid, "BINGO!"))

    if winners_list:
        st.markdown("### 🏆 አሸናፊዎች 🏆")
        for w in winners_list:
            patterns = ", ".join(w.get("patterns", ["BINGO!"]))
            cards = ", ".join([f"#{c}" for c in w.get("cards", [])])
            st.success(f"🎉 {w.get('username')} - Card(s): {cards} - {patterns} 🎉")

    st.markdown("""
    <div style="text-align:center;margin:25px 0 10px 0;">
        <p style="color:#FFD700;font-size:1.2rem;font-weight:bold;margin:0;">
            ✅ ወደ ካርቴላ ምርጫ ለመመለስ ከታች ያለውን ቁልፍ ይጫኑ
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("🔄 ወደ ካርቴላ ምርጫ ተመለስ (Resume)", use_container_width=True, type="primary", key="global_resume_btn"):
            # Reset for next round — global
            remove_bot_cards()
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
                "timer_start_time": time.time(),
                "card_selection_time": CARD_SELECTION_DURATION,
            })
            st.rerun()

    time.sleep(1.0)
    st.rerun()
    st.stop()

# ===================================================================
# CARD SELECTION PHASE
# ===================================================================
if not game_started:
    remaining = get_remaining_seconds()
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    time_str = f"{minutes:01d}:{seconds:02d}"

    total_selected = len(taken_cards)
    your_cards_count = len(my_cards)
    available = 204 - total_selected
    enough_cards = total_selected >= MIN_CARDS_TO_START
    color = "#FFD700" if enough_cards and remaining > 30 else ("#FF9800" if remaining <= 30 else "#FFD700")

    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.15);padding:12px 15px;border-radius:12px;border:1px solid rgba(255,255,255,0.08);margin-bottom:15px;text-align:center;">
        <div style="font-size:1.6rem;font-weight:bold;color:{color};font-family:monospace;margin-bottom:6px;">⌚ {time_str}</div>
        <div style="font-size:0.9rem;color:#FFFFFF;line-height:1.9;">
            🟢 <b>Your Cards:</b> {your_cards_count}/2 &nbsp;|&nbsp;
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

    if st.session_state.flash_msg:
        st.warning(st.session_state.flash_msg)
        st.session_state.flash_msg = ""

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
            is_mine = card_num in my_cards
            is_taken = card_num in taken_cards and not is_mine
            is_rejected = (rejected == card_num) and not is_mine and not is_taken
            is_insufficient = (insufficient == card_num) and not is_mine and not is_taken
            with cols[col_idx]:
                if is_mine:
                    if st.button(f"✅{card_num}", key=f"card_{card_num}", use_container_width=True, type="primary"):
                        user_balance = st.session_state.user_db.get(st.session_state.current_user, {}).get("balance", 0)
                        ok, reason = deselect_card_for_user(card_num, user_balance)
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
                        ok, reason = select_card_for_user(card_num, user_balance)
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

    # Auto-start when timer hits 0 with >= 3 cards
    if remaining <= 0 and enough_cards and not game_started:
        start_game_globally()
        st.rerun()

    time.sleep(0.5)
    st.rerun()

# ===================================================================
# GAME STARTED PHASE
# ===================================================================
if game_started and not winner_declared:
    st.markdown(f"""
    <div style="background:rgba(46,125,50,0.1);border:1px solid rgba(255,215,0,0.05);padding:8px 15px;border-radius:10px;text-align:center;margin-bottom:15px;font-size:0.9rem;color:rgba(255,255,255,0.8);">
        🎯 Playing with {len(taken_cards)} Card(s) globally
        <span style="margin-left:12px;background:rgba(255,215,0,0.08);padding:2px 10px;border-radius:12px;">
            {len(called_numbers)}/75 Called
        </span>
        <span style="margin-left:8px;background:rgba(76,175,80,0.15);padding:2px 10px;border-radius:12px;color:#4CAF50;">
            ✅ Your Cards: {len(my_cards)}/2
        </span>
    </div>
    """, unsafe_allow_html=True)

    board_col, cards_col = st.columns([2, 1], gap="large")
    with board_col:
        display_master_board(called_numbers, last_called_number)

    with cards_col:
        st.markdown("### 📋🍀 የእርስዎ ካርቴላ/ዎች")
        if my_cards:
            for cid in my_cards:
                display_selected_card(cid, list(called_numbers), False)
        else:
            st.warning("⚠️በዚህ ዙር ጨዋታ ካርቴላ አልመረጡም!")
            st.info("💡ጨዋታዉ ተጀምሯል🍀 ካርቴላ ለመምረጥ ቀጣዩን ዙር ይጠብቁ።")

    # Play sound for the most recent number once per user
    if last_called_number is not None and st.session_state.get("_last_sound_played_for") != last_called_number:
        st.markdown(get_number_sound_js(last_called_number), unsafe_allow_html=True)
        st.session_state["_last_sound_played_for"] = last_called_number

    st.info(f"🎯 Auto-calling every {int(CALL_INTERVAL)} seconds... ({len(called_numbers)}/75)")

    # Every client runs the same auto-call + winner check.
    # try_global_call() elects a single caller via DB row.
    try_global_call()
    scan_for_winner()

    time.sleep(1.0)
    st.rerun()

st.session_state["_first_render_done"] = True
