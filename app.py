# ===================================================================
# ደራሽ ቢንጎ (Derash Bingo) - Complete Bingo Game
# Integrated with School Registration Portal Supabase Backend
# Berhanu Mekonen, PhD, Arba Minch University
# ===================================================================

import streamlit as st
import pandas as pd
import hashlib
import json
import random
import string
import time
import uuid
from datetime import datetime, timedelta
from supabase import create_client, Client

# ===================================================================
# GAME CONFIGURATION
# ===================================================================

CARD_PRICE = 10
PRIZE_PER_CARD = 8
COMMISSION = 2
MAX_CARDS_PER_PLAYER = 2
SELECTION_TIME = 60  # 60 seconds = 1 minute
TOTAL_CARDS = 201
MIN_BALANCE_TO_PLAY = CARD_PRICE

# ===================================================================
# SUPABASE CONNECTION
# ===================================================================

def init_supabase():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["anon_key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Supabase connection error: {e}")
        st.stop()

def get_supabase():
    if "supabase" not in st.session_state:
        st.session_state.supabase = init_supabase()
    return st.session_state.supabase

def init_supabase_admin():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["service_role_key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Admin Supabase connection error: {e}")
        st.stop()

def get_supabase_admin():
    if "supabase_admin" not in st.session_state:
        st.session_state.supabase_admin = init_supabase_admin()
    return st.session_state.supabase_admin

# ===================================================================
# DATABASE FUNCTIONS
# ===================================================================

def load_all_data():
    supabase = get_supabase()
    
    # Users
    res = supabase.table("bingo_users").select("*").execute()
    user_db = {}
    if res.data:
        for u in res.data:
            user_db[u["username"]] = {
                "password": u["password"],
                "balance": u["balance"],
                "role": u["role"],
                "name": u["name"],
                "phone": u.get("phone", "")
            }
    st.session_state.user_db = user_db
    
    # Games
    res = supabase.table("bingo_games").select("*").order("game_id", desc=True).execute()
    st.session_state.games = res.data if res.data else []
    
    # Selected Cards
    res = supabase.table("bingo_selected_cards").select("*").execute()
    st.session_state.selected_cards = res.data if res.data else []
    
    # Winners
    res = supabase.table("bingo_winners").select("*").execute()
    st.session_state.winners = res.data if res.data else []
    
    # Payments
    res = supabase.table("bingo_payments").select("*").execute()
    st.session_state.payments = res.data if res.data else []

def init_game_db():
    if "user_db" not in st.session_state:
        load_all_data()
    
    # Ensure admin exists
    if "admin" not in st.session_state.user_db:
        supabase_admin = get_supabase_admin()
        admin_pw = hash_password("adminbb")
        try:
            supabase_admin.table("bingo_users").insert({
                "username": "admin",
                "password": admin_pw,
                "balance": 1000,
                "role": "admin",
                "name": "Bingo Administrator"
            }).execute()
            load_all_data()
        except Exception as e:
            st.error(f"Could not create admin: {e}")
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "🏠 Home"
    if "selected_cards" not in st.session_state:
        st.session_state.selected_cards = []
    if "notifications" not in st.session_state:
        st.session_state.notifications = []

# ===================================================================
# AUTHENTICATION
# ===================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def login_user(username, password):
    init_game_db()
    if username not in st.session_state.user_db:
        return False, "❌ Username not found."
    user = st.session_state.user_db[username]
    if verify_password(password, user["password"]):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.current_role = user["role"]
        st.session_state.balance = user["balance"]
        return True, "✅ Login successful!"
    return False, "❌ Incorrect password."

def logout_user():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_role = None

def register_user(username, password, name, phone=""):
    init_game_db()
    if username in st.session_state.user_db:
        return False, "❌ Username already exists."
    
    hashed = hash_password(password)
    supabase_admin = get_supabase_admin()
    try:
        supabase_admin.table("bingo_users").insert({
            "username": username,
            "password": hashed,
            "balance": 0,
            "role": "player",
            "name": name,
            "phone": phone
        }).execute()
        load_all_data()
        return True, "✅ Registration successful!"
    except Exception as e:
        return False, f"❌ Registration failed: {e}"

# ===================================================================
# GAME FUNCTIONS
# ===================================================================

def get_current_game():
    """Get the current active game (waiting or running)"""
    for game in st.session_state.games:
        if game["status"] in ["waiting", "running"]:
            return game
    return None

def get_game_by_id(game_id):
    for game in st.session_state.games:
        if game["game_id"] == game_id:
            return game
    return None

def get_taken_cards(game_id):
    """Get all taken card IDs for a game"""
    cards = []
    for sc in st.session_state.selected_cards:
        if sc["game_id"] == game_id:
            cards.append(sc["card_id"])
    return cards

def get_user_cards(game_id, user_id):
    """Get cards selected by a specific user for a game"""
    cards = []
    for sc in st.session_state.selected_cards:
        if sc["game_id"] == game_id and sc["user_id"] == user_id:
            cards.append(sc["card_id"])
    return cards

def get_players(game_id):
    """Get all players in a game with their card counts"""
    players = {}
    for sc in st.session_state.selected_cards:
        if sc["game_id"] == game_id:
            username = sc.get("username", "Unknown")
            if username not in players:
                players[username] = 0
            players[username] += 1
    return players

def generate_card_numbers(card_id):
    """Generate BINGO card numbers based on card ID"""
    columns = {
        'B': list(range(1, 16)),
        'I': list(range(16, 31)),
        'N': list(range(31, 46)),
        'G': list(range(46, 61)),
        'O': list(range(61, 76))
    }
    
    card = []
    column_keys = ['B', 'I', 'N', 'G', 'O']
    
    for col in range(5):
        col_key = column_keys[col]
        available = columns[col_key][:]
        
        # Seed random for reproducibility
        random.seed(card_id * 1000 + col)
        random.shuffle(available)
        
        col_numbers = available[:5]
        
        for row in range(5):
            if col == 2 and row == 2:
                card.append({'value': 'F', 'row': row, 'col': col})
            else:
                card.append({'value': col_numbers[row], 'row': row, 'col': col})
    
    return card

def check_card_for_win(card_numbers, called_numbers):
    """Check if a card has a winning pattern"""
    if not called_numbers:
        return None
    
    called_set = set(called_numbers)
    
    # Create grid
    grid = [[None for _ in range(5)] for _ in range(5)]
    for cell in card_numbers:
        grid[cell['row']][cell['col']] = cell['value']
    
    def is_marked(value):
        if value == 'F':
            return True
        return value in called_set
    
    # Check rows
    for row in range(5):
        if all(is_marked(grid[row][col]) for col in range(5)):
            return {'type': 'row', 'index': row + 1}
    
    # Check columns
    for col in range(5):
        if all(is_marked(grid[row][col]) for row in range(5)):
            return {'type': 'column', 'letter': ['B', 'I', 'N', 'G', 'O'][col]}
    
    # Check main diagonal
    if all(is_marked(grid[i][i]) for i in range(5)):
        return {'type': 'diagonal', 'direction': 'main'}
    
    # Check anti-diagonal
    if all(is_marked(grid[i][4 - i]) for i in range(5)):
        return {'type': 'diagonal', 'direction': 'anti'}
    
    # Check four corners
    corners = [grid[0][0], grid[0][4], grid[4][0], grid[4][4]]
    if all(is_marked(c) for c in corners):
        return {'type': 'four-corners'}
    
    # Check blackout
    if all(is_marked(grid[row][col]) for row in range(5) for col in range(5)):
        return {'type': 'blackout'}
    
    return None

def get_pattern_name(pattern):
    if not pattern:
        return "Unknown"
    if pattern['type'] == 'row':
        return f"Row {pattern['index']}"
    elif pattern['type'] == 'column':
        return f"Column {pattern['letter']}"
    elif pattern['type'] == 'diagonal':
        return f"{pattern['direction'].title()} Diagonal"
    elif pattern['type'] == 'four-corners':
        return "Four Corners"
    elif pattern['type'] == 'blackout':
        return "Blackout"
    return "Unknown"

def create_new_game():
    """Create a new BINGO game"""
    supabase_admin = get_supabase_admin()
    selection_end = (datetime.now() + timedelta(seconds=SELECTION_TIME)).isoformat()
    
    try:
        res = supabase_admin.table("bingo_games").insert({
            "status": "waiting",
            "selection_end_time": selection_end,
            "pot": 0,
            "prize": 0,
            "total_prizes": 1,
            "called_numbers": json.dumps([])
        }).execute()
        if res.data:
            load_all_data()
            return res.data[0]
    except Exception as e:
        st.error(f"Failed to create game: {e}")
    return None

def call_number(game_id):
    """Call the next random number"""
    supabase_admin = get_supabase_admin()
    game = get_game_by_id(game_id)
    if not game:
        return None
    
    called = json.loads(game.get("called_numbers", "[]"))
    all_numbers = list(range(1, 76))
    available = [n for n in all_numbers if n not in called]
    
    if not available:
        return None
    
    new_number = random.choice(available)
    called.append(new_number)
    
    try:
        supabase_admin.table("bingo_games").update({
            "called_numbers": json.dumps(called)
        }).eq("game_id", game_id).execute()
        load_all_data()
        return new_number
    except Exception as e:
        st.error(f"Failed to call number: {e}")
        return None

def declare_winner(game_id, winner_id, card_id, pattern):
    """Declare a winner for the game"""
    supabase_admin = get_supabase_admin()
    game = get_game_by_id(game_id)
    if not game:
        return False
    
    # Get user info
    user = None
    for username, data in st.session_state.user_db.items():
        if data.get("username") == winner_id:
            user = data
            break
    
    if not user:
        return False
    
    prize = game.get("pot", 0)
    
    try:
        # Update game status
        supabase_admin.table("bingo_games").update({
            "status": "finished",
            "winner_declared": True,
            "winner_card": card_id,
            "winner_username": winner_id,
            "prize": prize
        }).eq("game_id", game_id).execute()
        
        # Add winner record
        supabase_admin.table("bingo_winners").insert({
            "game_id": game_id,
            "winner_id": winner_id,
            "username": winner_id,
            "card_id": card_id,
            "prize": prize,
            "winning_pattern": json.dumps(pattern)
        }).execute()
        
        # Update winner's balance
        new_balance = user.get("balance", 0) + prize
        supabase_admin.table("bingo_users").update({
            "balance": new_balance
        }).eq("username", winner_id).execute()
        
        load_all_data()
        return True
    except Exception as e:
        st.error(f"Failed to declare winner: {e}")
        return False

def add_balance(username, amount):
    """Add balance to a user's account"""
    supabase_admin = get_supabase_admin()
    try:
        user = st.session_state.user_db.get(username)
        if user:
            new_balance = user.get("balance", 0) + amount
            supabase_admin.table("bingo_users").update({
                "balance": new_balance
            }).eq("username", username).execute()
            load_all_data()
            return True
    except Exception as e:
        st.error(f"Failed to add balance: {e}")
    return False

def join_game(game_id, user_id, card_ids):
    """Join a game with selected cards"""
    supabase_admin = get_supabase_admin()
    
    total_cost = len(card_ids) * CARD_PRICE
    
    # Check balance
    user = st.session_state.user_db.get(user_id)
    if not user or user.get("balance", 0) < total_cost:
        return False, "Insufficient balance"
    
    # Check if user already has cards
    existing = get_user_cards(game_id, user_id)
    if existing:
        return False, "You already have cards in this game"
    
    # Check if cards are available
    taken = get_taken_cards(game_id)
    for card_id in card_ids:
        if card_id in taken:
            return False, f"Card {card_id} is already taken"
    
    try:
        # Deduct balance
        new_balance = user.get("balance", 0) - total_cost
        supabase_admin.table("bingo_users").update({
            "balance": new_balance
        }).eq("username", user_id).execute()
        
        # Add selected cards
        for card_id in card_ids:
            supabase_admin.table("bingo_selected_cards").insert({
                "user_id": user_id,
                "username": user_id,
                "game_id": game_id,
                "card_id": card_id,
                "created_at": datetime.now().isoformat()
            }).execute()
        
        # Update pot
        game = get_game_by_id(game_id)
        if game:
            new_pot = game.get("pot", 0) + (len(card_ids) * PRIZE_PER_CARD)
            supabase_admin.table("bingo_games").update({
                "pot": new_pot
            }).eq("game_id", game_id).execute()
        
        load_all_data()
        return True, f"Successfully joined with {len(card_ids)} card(s)"
    except Exception as e:
        return False, f"Failed to join game: {e}"

# ===================================================================
# UI COMPONENTS
# ===================================================================

def show_login_page():
    st.markdown("""
    <div style="text-align:center; padding:2rem 0;">
        <div style="font-size:5rem;">🎰</div>
        <h1 style="font-size:3.5rem; margin:0; color:#8B0000;">ደራሽ ቢንጎ</h1>
        <p style="color:#5F6368; font-size:1.2rem;">Derash Bingo - Premium Gaming Experience</p>
        <p style="color:#5F6368; font-size:1rem;">💰 10 ETB per card | Prize: 8 ETB per card</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="Enter username")
                password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
                submitted = st.form_submit_button("🎰 Login to Play", width='stretch')
                if submitted:
                    if username and password:
                        success, message = login_user(username, password)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            with st.form("register_form"):
                full_name = st.text_input("👤 Full Name", placeholder="Your full name")
                username = st.text_input("👤 Username", placeholder="Choose a username")
                phone = st.text_input("📱 Phone Number", placeholder="09XXXXXXXX")
                password = st.text_input("🔑 Password", type="password", placeholder="Create a password")
                confirm = st.text_input("✅ Confirm Password", type="password", placeholder="Confirm password")
                submitted = st.form_submit_button("📝 Register & Play", width='stretch')
                if submitted:
                    if not full_name or not username or not password:
                        st.error("Please fill in all required fields")
                    elif password != confirm:
                        st.error("Passwords do not match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        success, message = register_user(username, password, full_name, phone)
                        if success:
                            st.success(message)
                            st.info("Please login with your new credentials")
                        else:
                            st.error(message)
            st.markdown('</div>', unsafe_allow_html=True)

def show_card_selection(game_id, user_id):
    """Display card selection interface"""
    st.markdown("### 🎯 Select Your Cards")
    st.markdown(f"💰 Card Price: {CARD_PRICE} ETB each | Max: {MAX_CARDS_PER_PLAYER} cards")
    
    user_cards = get_user_cards(game_id, user_id)
    taken = get_taken_cards(game_id)
    
    if user_cards:
        st.success(f"✅ You have {len(user_cards)} card(s) in this game")
        return user_cards
    
    # Show available cards
    st.markdown("#### Available Cards")
    cols = st.columns(5)
    selected = []
    
    available_cards = [i for i in range(1, TOTAL_CARDS + 1) if i not in taken]
    random.shuffle(available_cards)
    display_cards = available_cards[:50]  # Show 50 random available cards
    
    for i, card_id in enumerate(display_cards):
        col = cols[i % 5]
        with col:
            is_selected = card_id in st.session_state.get('temp_selected', [])
            if st.button(
                f"Card {card_id}\n💵 {CARD_PRICE} ETB",
                key=f"card_{card_id}",
                type="primary" if is_selected else "secondary",
                use_container_width=True
            ):
                temp_selected = st.session_state.get('temp_selected', [])
                if card_id in temp_selected:
                    temp_selected.remove(card_id)
                elif len(temp_selected) < MAX_CARDS_PER_PLAYER:
                    temp_selected.append(card_id)
                else:
                    st.warning(f"Maximum {MAX_CARDS_PER_PLAYER} cards allowed")
                st.session_state.temp_selected = temp_selected
                st.rerun()
    
    # Show selection summary
    temp_selected = st.session_state.get('temp_selected', [])
    if temp_selected:
        st.markdown("---")
        st.markdown(f"### 📋 Selected Cards: {len(temp_selected)}")
        st.write(f"Total Cost: {len(temp_selected) * CARD_PRICE} ETB")
        
        if st.button("✅ Join Game", type="primary", width='stretch'):
            success, message = join_game(game_id, user_id, temp_selected)
            if success:
                st.success(message)
                st.session_state.temp_selected = []
                st.rerun()
            else:
                st.error(message)
    
    return user_cards

def show_game_board(game):
    """Display the BINGO game board"""
    game_id = game["game_id"]
    status = game["status"]
    called = json.loads(game.get("called_numbers", "[]"))
    pot = game.get("pot", 0)
    
    # Game status
    status_colors = {
        "waiting": "🟡",
        "running": "🟢",
        "finished": "🔴"
    }
    status_labels = {
        "waiting": "Waiting for Players",
        "running": "Game in Progress",
        "finished": "Game Ended"
    }
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🎮 Status", f"{status_colors.get(status, '⚪')} {status_labels.get(status, status)}")
    col2.metric("💰 Prize Pool", f"{pot} ETB")
    col3.metric("🎯 Numbers Called", f"{len(called)}/75")
    
    # Show timer if waiting
    if status == "waiting":
        selection_end = datetime.fromisoformat(game["selection_end_time"])
        remaining = max(0, int((selection_end - datetime.now()).total_seconds()))
        st.info(f"⏰ Selection ends in: {remaining // 60}:{remaining % 60:02d}")
        
        # Auto-start when timer expires
        if remaining <= 0:
            supabase_admin = get_supabase_admin()
            try:
                supabase_admin.table("bingo_games").update({
                    "status": "running"
                }).eq("game_id", game_id).execute()
                load_all_data()
                st.rerun()
            except:
                pass
    
    # Show BINGO board if game is running
    if status == "running":
        st.markdown("### 🎯 BINGO Board")
        
        # Display called numbers
        if called:
            cols = st.columns(10)
            for i, num in enumerate(called[-20:]):  # Show last 20 called numbers
                col = cols[i % 10]
                col.markdown(f"""
                <div style="background: #8B0000; color: white; 
                            padding: 0.5rem; border-radius: 8px; 
                            text-align: center; font-weight: bold; 
                            margin: 2px;">
                    {num}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No numbers called yet")
        
        # Auto-call numbers every 5 seconds
        if not st.session_state.get('auto_call_running', False):
            st.session_state.auto_call_running = True
            # Call a number every 5 seconds
            if len(called) < 75:
                time.sleep(5)  # Wait 5 seconds
                new_num = call_number(game_id)
                if new_num:
                    st.rerun()
        
        # Check for winners
        players = get_players(game_id)
        for username in players.keys():
            user_cards = get_user_cards(game_id, username)
            for card_id in user_cards:
                card_nums = generate_card_numbers(card_id)
                pattern = check_card_for_win(card_nums, called)
                if pattern:
                    if declare_winner(game_id, username, card_id, pattern):
                        st.balloons()
                        st.success(f"🎉 {username} WINS with {get_pattern_name(pattern)}!")
                        load_all_data()
                        st.rerun()

def show_players_list(game_id):
    """Display list of players in the game"""
    players = get_players(game_id)
    if players:
        st.markdown("### 👥 Players")
        for username, count in players.items():
            st.markdown(f"🎯 {username}: {count} card(s)")
    else:
        st.info("No players yet. Join the game!")

def show_balance():
    if st.session_state.logged_in:
        user = st.session_state.user_db.get(st.session_state.current_user, {})
        balance = user.get("balance", 0)
        st.sidebar.markdown(f"""
        <div style="background:#E8F0FE;padding:1rem;border-radius:12px;margin-bottom:1rem;">
            <p style="margin:0;font-weight:600;color:#1A73E8;">💰 Balance: {balance} ETB</p>
        </div>
        """, unsafe_allow_html=True)
        return balance
    return 0

def show_add_funds():
    """Display add funds interface"""
    st.markdown("### 💰 Add Funds")
    
    with st.form("add_funds"):
        amount = st.number_input("Amount (ETB)", min_value=10, max_value=10000, step=10, value=50)
        phone = st.text_input("📱 Phone Number", placeholder="09XXXXXXXX")
        confirm_code = st.text_input("🔑 Confirmation Code", placeholder="Enter code 2121 for demo")
        
        if st.form_submit_button("💰 Confirm Payment", width='stretch'):
            if confirm_code == "2121":
                if add_balance(st.session_state.current_user, amount):
                    st.success(f"✅ Added {amount} ETB to your account!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add funds")
            else:
                st.error("❌ Invalid confirmation code. Use 2121 for demo.")

# ===================================================================
# MAIN APPLICATION
# ===================================================================

def main():
    st.set_page_config(
        page_title="ደራሽ ቢንጎ - Derash Bingo",
        page_icon="🎰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS
    st.markdown("""
    <style>
        .login-container {
            max-width: 500px;
            margin: 2rem auto;
            padding: 2.5rem;
            background: #FFFFFF !important;
            border: 1px solid #E8EAED;
            border-radius: 16px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        }
        .stButton > button {
            background: linear-gradient(135deg, #8B0000, #CC0000) !important;
            color: white !important;
            border-radius: 30px !important;
            padding: 0.9rem 2.2rem !important;
            font-weight: 600 !important;
            border: none !important;
        }
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 16px rgba(139,0,0,0.35);
        }
        .stButton > button[type="primary"] {
            background: linear-gradient(135deg, #2E7D32, #4CAF50) !important;
        }
        .stButton > button[type="secondary"] {
            background: linear-gradient(135deg, #1A73E8, #4285F4) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    init_game_db()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎰 ደራሽ ቢንጎ")
        st.markdown("---")
        
        if st.session_state.logged_in:
            user = st.session_state.user_db.get(st.session_state.current_user, {})
            name = user.get("name", st.session_state.current_user)
            role = user.get("role", "player")
            balance = user.get("balance", 0)
            
            st.markdown(f"""
            <div style="background:#E8F0FE;padding:1rem;border-radius:12px;margin-bottom:1rem;">
                <p style="margin:0;font-weight:600;color:#1A73E8;">👤 {name}</p>
                <p style="margin:0;font-size:0.85rem;color:#5F6368;">@{st.session_state.current_user}</p>
                <p style="margin:0;font-size:0.85rem;color:#5F6368;">💰 Balance: {balance} ETB</p>
                <p style="margin:0;font-size:0.85rem;color:#5F6368;">🎯 Role: {role.title()}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if role == "admin":
                nav_options = ["👑 Admin Dashboard", "🏠 Game Lobby", "💰 Add Funds", "📊 History"]
            else:
                nav_options = ["🏠 Game Lobby", "💰 Add Funds", "📊 My History"]
            
            selected = st.radio("Navigation", nav_options, index=0)
            st.session_state.current_page = selected
            
            if st.button("🚪 Logout", width='stretch'):
                logout_user()
                st.rerun()
            
            st.markdown("---")
            st.markdown("📌 **Card Price:** 10 ETB")
            st.markdown("🏆 **Prize:** 8 ETB per card")
            st.markdown("⏰ **Selection:** 1 minute")
            st.markdown("🎯 **Max Cards:** 2 per player")
        else:
            st.markdown("👋 Welcome to Derash Bingo!")
            st.markdown("Please login or register to play.")
            if st.button("🔐 Login / Register", width='stretch'):
                st.rerun()
    
    # Main content
    if not st.session_state.logged_in:
        show_login_page()
        return
    
    current_page = st.session_state.get('current_page', '🏠 Game Lobby')
    
    if current_page == "👑 Admin Dashboard" and st.session_state.current_role == "admin":
        st.markdown("### 👑 Admin Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎮 Games", len(st.session_state.games))
        col2.metric("👥 Players", len([u for u in st.session_state.user_db if u != "admin"]))
        col3.metric("💰 Total Pot", sum(g.get("pot", 0) for g in st.session_state.games))
        col4.metric("🏆 Winners", len(st.session_state.winners))
        
        # Game Management
        st.markdown("---")
        st.markdown("#### 🎮 Game Management")
        
        current_game = get_current_game()
        if current_game:
            st.info(f"Current Game: #{current_game['game_id']} - {current_game['status']}")
            if current_game['status'] == "waiting":
                if st.button("⏰ Force Start Game", width='stretch'):
                    supabase_admin = get_supabase_admin()
                    try:
                        supabase_admin.table("bingo_games").update({
                            "status": "running"
                        }).eq("game_id", current_game['game_id']).execute()
                        load_all_data()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to start game: {e}")
            elif current_game['status'] == "running":
                if st.button("🎯 Call Number", width='stretch'):
                    num = call_number(current_game['game_id'])
                    if num:
                        st.success(f"Number {num} called!")
                        st.rerun()
                if st.button("🏁 End Game", width='stretch'):
                    supabase_admin = get_supabase_admin()
                    try:
                        supabase_admin.table("bingo_games").update({
                            "status": "finished"
                        }).eq("game_id", current_game['game_id']).execute()
                        load_all_data()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to end game: {e}")
        else:
            if st.button("🆕 Create New Game", width='stretch'):
                game = create_new_game()
                if game:
                    st.success(f"✅ New game created! Game ID: {game['game_id']}")
                    st.rerun()
        
        # User Management
        st.markdown("---")
        st.markdown("#### 👥 User Management")
        users_df = pd.DataFrame([{
            "Username": u,
            "Name": d.get("name", ""),
            "Balance": d.get("balance", 0),
            "Role": d.get("role", "player")
        } for u, d in st.session_state.user_db.items()])
        st.dataframe(users_df, use_container_width=True)
        
        # Winner History
        st.markdown("---")
        st.markdown("#### 🏆 Winner History")
        if st.session_state.winners:
            winners_df = pd.DataFrame(st.session_state.winners)
            st.dataframe(winners_df, use_container_width=True)
        else:
            st.info("No winners yet")
    
    elif current_page == "🏠 Game Lobby":
        st.markdown("### 🎰 ደራሽ ቢንጎ")
        st.markdown("#### እንኳን ወደ ደራሽ ቢንጎ በደህና መጡ! 🎉")
        
        # Show current game
        current_game = get_current_game()
        
        if not current_game:
            st.info("No active game. Creating a new game...")
            game = create_new_game()
            if game:
                st.rerun()
            return
        
        game_id = current_game["game_id"]
        status = current_game["status"]
        
        # Show game status
        if status == "waiting":
            st.markdown("### 🎯 Game Lobby - Select Your Cards")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                user_cards = show_card_selection(game_id, st.session_state.current_user)
            with col2:
                show_players_list(game_id)
                show_balance()
                
        elif status == "running":
            st.markdown("### 🎯 Game in Progress")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                show_game_board(current_game)
            with col2:
                show_players_list(game_id)
                show_balance()
                
        elif status == "finished":
            st.markdown("### 🏁 Game Finished")
            
            # Show winner
            winner = None
            for w in st.session_state.winners:
                if w["game_id"] == game_id:
                    winner = w
                    break
            
            if winner:
                st.balloons()
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FFD700, #FFA500);
                            padding: 2rem; border-radius: 20px; text-align: center;
                            border: 4px solid #8B0000;">
                    <div style="font-size: 4rem;">🎉🏆🎉</div>
                    <h1 style="color: #8B0000;">Winner!</h1>
                    <h2 style="color: #1a365d;">{winner.get('username', 'Unknown')}</h2>
                    <p style="font-size: 2rem; color: #8B0000;">💰 {winner.get('prize', 0)} ETB</p>
                    <p>Pattern: {get_pattern_name(json.loads(winner.get('winning_pattern', '{}')))}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No winner declared. Game ended.")
            
            if st.button("🆕 New Game", width='stretch'):
                create_new_game()
                st.rerun()
    
    elif current_page == "💰 Add Funds":
        show_add_funds()
    
    elif current_page == "📊 History" or current_page == "📊 My History":
        st.markdown("### 📊 Game History")
        
        if st.session_state.winners:
            st.markdown("#### 🏆 Your Wins")
            my_wins = [w for w in st.session_state.winners if w.get("username") == st.session_state.current_user]
            if my_wins:
                df = pd.DataFrame(my_wins)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("You haven't won any games yet")
        else:
            st.info("No games played yet")

if __name__ == "__main__":
    main()
