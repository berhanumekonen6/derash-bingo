# ===================================================================
# ደራሽ ቢንጎ (Derash Bingo) - Complete Automatic Bingo Game
# FIXED: Correctly parsing Supabase data
# ===================================================================

import streamlit as st
import pandas as pd
import hashlib
import json
import random
import time
import traceback
from datetime import datetime, timedelta
from supabase import create_client

# ===================================================================
# GAME CONFIGURATION
# ===================================================================

CARD_PRICE = 10
PRIZE_PER_CARD = 8
COMMISSION = 2
MAX_CARDS_PER_PLAYER = 2
SELECTION_TIME = 60
TOTAL_CARDS = 201

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
    
    # Users - FIXED: Properly parse the response
    try:
        res = supabase.table("bingo_users").select("*").execute()
        user_db = {}
        
        # Debug: Print the raw response
        print(f"Raw response: {res}")
        print(f"Data: {res.data}")
        
        if res.data:
            # The data is a list of dictionaries, each representing a row
            for u in res.data:
                username = u.get("username")
                if username:
                    user_db[username] = {
                        "password": u.get("password", ""),
                        "balance": float(u.get("balance", 0)),
                        "role": u.get("role", "player"),
                        "name": u.get("name", username),
                        "phone": u.get("phone", ""),
                        "game_played": u.get("game_played", 0)
                    }
                    print(f"Loaded user: {username} -> {user_db[username]}")
        
        st.session_state.user_db = user_db
        st.session_state.user_db_loaded = True
        print(f"✅ Loaded {len(user_db)} users from database")
        print(f"Users: {list(user_db.keys())}")
        
    except Exception as e:
        st.error(f"Error loading users: {e}")
        print(f"Error loading users: {e}")
        traceback.print_exc()
        st.session_state.user_db = {}
        st.session_state.user_db_loaded = False
    
    # Games
    try:
        res = supabase.table("bingo_games").select("*").order("game_id", desc=True).execute()
        st.session_state.games = res.data if res.data else []
    except Exception as e:
        print(f"Error loading games: {e}")
        st.session_state.games = []
    
    # Selected Cards
    try:
        res = supabase.table("bingo_selected_cards").select("*").execute()
        st.session_state.selected_cards = res.data if res.data else []
    except Exception as e:
        print(f"Error loading selected cards: {e}")
        st.session_state.selected_cards = []
    
    # Winners
    try:
        res = supabase.table("bingo_winners").select("*").execute()
        st.session_state.winners = res.data if res.data else []
    except Exception as e:
        print(f"Error loading winners: {e}")
        st.session_state.winners = []

def init_game_db():
    if "user_db" not in st.session_state:
        load_all_data()
    
    # Initialize session variables
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "current_role" not in st.session_state:
        st.session_state.current_role = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "🏠 Game Lobby"
    if "selected_cards" not in st.session_state:
        st.session_state.selected_cards = []
    if "notifications" not in st.session_state:
        st.session_state.notifications = []
    if "balance" not in st.session_state:
        st.session_state.balance = 0
    if "called_numbers" not in st.session_state:
        st.session_state.called_numbers = []
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "winner_declared" not in st.session_state:
        st.session_state.winner_declared = False
    if "countdown_active" not in st.session_state:
        st.session_state.countdown_active = False
    if "countdown_time" not in st.session_state:
        st.session_state.countdown_time = SELECTION_TIME
    if "auto_play" not in st.session_state:
        st.session_state.auto_play = False
    if "selected_temp_cards" not in st.session_state:
        st.session_state.selected_temp_cards = []
    if "cards_data" not in st.session_state:
        st.session_state.cards_data = {}
    if "debug_info" not in st.session_state:
        st.session_state.debug_info = ""

# ===================================================================
# AUTHENTICATION
# ===================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def login_user(username, password):
    init_game_db()
    
    debug_msg = f"Login attempt for: {username}\n"
    debug_msg += f"Users in DB: {list(st.session_state.user_db.keys())}\n"
    
    if username not in st.session_state.user_db:
        debug_msg += f"❌ Username '{username}' not found in database\n"
        st.session_state.debug_info = debug_msg
        return False, f"❌ Username not found. Available users: {', '.join(list(st.session_state.user_db.keys())[:5])}"
    
    user = st.session_state.user_db[username]
    stored_hash = user["password"]
    computed_hash = hash_password(password)
    
    debug_msg += f"✅ User found: {username}\n"
    debug_msg += f"Stored hash: {stored_hash}\n"
    debug_msg += f"Computed hash: {computed_hash}\n"
    debug_msg += f"Match: {stored_hash == computed_hash}\n"
    
    if verify_password(password, user["password"]):
        debug_msg += "✅ Password verified successfully!\n"
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.current_role = user["role"]
        st.session_state.balance = user["balance"]
        st.session_state.debug_info = debug_msg
        return True, "✅ Login successful!"
    else:
        debug_msg += "❌ Password verification failed\n"
        st.session_state.debug_info = debug_msg
        return False, "❌ Incorrect password."

def logout_user():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_role = None
    st.session_state.game_started = False
    st.session_state.called_numbers = []
    st.session_state.countdown_active = False
    st.session_state.auto_play = False

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
            "balance": 10,
            "role": "player",
            "name": name,
            "phone": phone
        }).execute()
        load_all_data()
        st.session_state.debug_info = f"✅ User {username} registered successfully"
        return True, "✅ Registration successful! Please login."
    except Exception as e:
        error_msg = f"❌ Registration failed: {e}"
        st.session_state.debug_info = error_msg
        return False, error_msg

# ===================================================================
# GAME FUNCTIONS
# ===================================================================

def get_current_game():
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
    cards = []
    for sc in st.session_state.selected_cards:
        if sc["game_id"] == game_id:
            cards.append(sc["card_id"])
    return cards

def get_user_cards(game_id, user_id):
    cards = []
    for sc in st.session_state.selected_cards:
        if sc["game_id"] == game_id and sc["user_id"] == user_id:
            cards.append(sc["card_id"])
    return cards

def get_players(game_id):
    players = {}
    for sc in st.session_state.selected_cards:
        if sc["game_id"] == game_id:
            username = sc.get("username", "Unknown")
            if username not in players:
                players[username] = 0
            players[username] += 1
    return players

def generate_bingo_card_data(card_id):
    columns = {
        'B': list(range(1, 16)),
        'I': list(range(16, 31)),
        'N': list(range(31, 46)),
        'G': list(range(46, 61)),
        'O': list(range(61, 76))
    }
    
    card = []
    column_keys = ['B', 'I', 'N', 'G', 'O']
    
    random.seed(card_id * 1000)
    
    for col in range(5):
        col_key = column_keys[col]
        available = columns[col_key][:]
        random.shuffle(available)
        col_numbers = available[:5]
        
        for row in range(5):
            if col == 2 and row == 2:
                card.append({'value': 'FREE', 'row': row, 'col': col, 'letter': col_key})
            else:
                card.append({'value': col_numbers[row], 'row': row, 'col': col, 'letter': col_key})
    
    return card

def get_card_data(card_id):
    if card_id not in st.session_state.cards_data:
        st.session_state.cards_data[card_id] = generate_bingo_card_data(card_id)
    return st.session_state.cards_data[card_id]

def display_card_grid(card_data):
    grid = [[None for _ in range(5)] for _ in range(5)]
    for cell in card_data:
        grid[cell['row']][cell['col']] = cell['value']
    return grid

def check_winning_pattern(card_data, called_numbers):
    if not called_numbers:
        return None
    
    called_set = set(called_numbers)
    grid = display_card_grid(card_data)
    
    def is_marked(value):
        if value == 'FREE':
            return True
        return value in called_set
    
    for row in range(5):
        if all(is_marked(grid[row][col]) for col in range(5)):
            return {'type': 'row', 'index': row + 1}
    
    for col in range(5):
        if all(is_marked(grid[row][col]) for row in range(5)):
            return {'type': 'column', 'letter': ['B', 'I', 'N', 'G', 'O'][col]}
    
    if all(is_marked(grid[i][i]) for i in range(5)):
        return {'type': 'diagonal', 'direction': 'main'}
    
    if all(is_marked(grid[i][4 - i]) for i in range(5)):
        return {'type': 'diagonal', 'direction': 'anti'}
    
    corners = [grid[0][0], grid[0][4], grid[4][0], grid[4][4]]
    if all(is_marked(c) for c in corners):
        return {'type': 'four-corners'}
    
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
            st.session_state.called_numbers = []
            st.session_state.winner_declared = False
            st.session_state.game_started = False
            st.session_state.countdown_active = True
            st.session_state.countdown_time = SELECTION_TIME
            st.session_state.selected_temp_cards = []
            return res.data[0]
    except Exception as e:
        st.error(f"Failed to create game: {e}")
    return None

def call_next_number(game_id):
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
    st.session_state.called_numbers = called
    
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
    supabase_admin = get_supabase_admin()
    game = get_game_by_id(game_id)
    if not game:
        return False
    
    user = st.session_state.user_db.get(winner_id)
    if not user:
        return False
    
    prize = game.get("pot", 0)
    
    try:
        supabase_admin.table("bingo_games").update({
            "status": "finished",
            "winner_declared": True,
            "winner_card": card_id,
            "winner_username": winner_id,
            "prize": prize
        }).eq("game_id", game_id).execute()
        
        supabase_admin.table("bingo_winners").insert({
            "game_id": game_id,
            "winner_id": winner_id,
            "username": winner_id,
            "card_id": card_id,
            "prize": prize,
            "winning_pattern": json.dumps(pattern)
        }).execute()
        
        new_balance = user.get("balance", 0) + prize
        update_data = {"balance": new_balance}
        if "game_played" in user:
            update_data["game_played"] = user.get("game_played", 0) + 1
        
        supabase_admin.table("bingo_users").update(update_data).eq("username", winner_id).execute()
        
        load_all_data()
        st.session_state.winner_declared = True
        st.session_state.game_started = False
        st.session_state.auto_play = False
        return True
    except Exception as e:
        st.error(f"Failed to declare winner: {e}")
        return False

def add_balance(username, amount):
    supabase_admin = get_supabase_admin()
    try:
        user = st.session_state.user_db.get(username)
        if user:
            new_balance = user.get("balance", 0) + amount
            supabase_admin.table("bingo_users").update({
                "balance": new_balance
            }).eq("username", username).execute()
            load_all_data()
            st.session_state.balance = new_balance
            return True
    except Exception as e:
        st.error(f"Failed to add balance: {e}")
    return False

def join_game(game_id, user_id, card_ids):
    supabase_admin = get_supabase_admin()
    
    total_cost = len(card_ids) * CARD_PRICE
    
    user = st.session_state.user_db.get(user_id)
    if not user or user.get("balance", 0) < total_cost:
        return False, "Insufficient balance"
    
    existing = get_user_cards(game_id, user_id)
    if existing:
        return False, "You already have cards in this game"
    
    taken = get_taken_cards(game_id)
    for card_id in card_ids:
        if card_id in taken:
            return False, f"Card {card_id} is already taken"
    
    try:
        new_balance = user.get("balance", 0) - total_cost
        supabase_admin.table("bingo_users").update({
            "balance": new_balance
        }).eq("username", user_id).execute()
        
        for card_id in card_ids:
            supabase_admin.table("bingo_selected_cards").insert({
                "user_id": user_id,
                "username": user_id,
                "game_id": game_id,
                "card_id": card_id,
                "created_at": datetime.now().isoformat()
            }).execute()
        
        game = get_game_by_id(game_id)
        if game:
            new_pot = game.get("pot", 0) + (len(card_ids) * PRIZE_PER_CARD)
            supabase_admin.table("bingo_games").update({
                "pot": new_pot
            }).eq("game_id", game_id).execute()
        
        load_all_data()
        st.session_state.balance = new_balance
        st.session_state.selected_temp_cards = []
        return True, f"Successfully joined with {len(card_ids)} card(s)"
    except Exception as e:
        return False, f"Failed to join game: {e}"

def get_balance_status(balance):
    if balance >= 2000:
        return "🟢", "Excellent Balance!"
    elif balance > 1000:
        return "🟡", "Good Balance"
    elif balance > 500:
        return "🟠", "Balance Running Low"
    else:
        return "🔴", "Please Add Funds"

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
        with st.form("login_form"):
            st.markdown("#### Login")
            username = st.text_input("👤 Username", placeholder="Enter username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
            
            # Show available users
            if st.session_state.user_db:
                st.info(f"👥 Available users: {', '.join(list(st.session_state.user_db.keys()))}")
            
            submitted = st.form_submit_button("🎰 Login to Play", use_container_width=True)
            
            if submitted:
                if username and password:
                    success, message = login_user(username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                        if st.session_state.debug_info:
                            with st.expander("🔍 Debug Info - Click to expand"):
                                st.code(st.session_state.debug_info, language="text")
    
    with tab2:
        with st.form("register_form"):
            st.markdown("#### Register New Account")
            full_name = st.text_input("👤 Full Name", placeholder="Your full name")
            username = st.text_input("👤 Username", placeholder="Choose a username")
            phone = st.text_input("📱 Phone Number", placeholder="09XXXXXXXX")
            password = st.text_input("🔑 Password", type="password", placeholder="Create a password")
            confirm = st.text_input("✅ Confirm Password", type="password", placeholder="Confirm password")
            submitted = st.form_submit_button("📝 Register & Play", use_container_width=True)
            
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
                        st.info("✅ Please login with your new credentials")
                    else:
                        st.error(message)

def show_bingo_card(card_id, called_numbers):
    card_data = get_card_data(card_id)
    grid = display_card_grid(card_data)
    called_set = set(called_numbers) if called_numbers else set()
    
    html = f"""
    <div style="border: 3px solid #8B0000; border-radius: 10px; padding: 10px; margin: 10px 0; background: white;">
        <div style="text-align: center; font-weight: bold; font-size: 18px; color: #8B0000; margin-bottom: 10px;">
            Card #{card_id}
        </div>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background: #8B0000; color: white;">
                <th style="padding: 8px; border: 1px solid #ddd;">B</th>
                <th style="padding: 8px; border: 1px solid #ddd;">I</th>
                <th style="padding: 8px; border: 1px solid #ddd;">N</th>
                <th style="padding: 8px; border: 1px solid #ddd;">G</th>
                <th style="padding: 8px; border: 1px solid #ddd;">O</th>
            </tr>
    """
    
    for row in range(5):
        html += "<tr>"
        for col in range(5):
            value = grid[row][col]
            is_called = value in called_set or value == 'FREE'
            bg_color = "#4CAF50" if is_called and value != 'FREE' else "#FFC107" if value == 'FREE' else "white"
            color = "white" if is_called else "black"
            html += f"""
            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; 
                       background: {bg_color}; color: {color}; font-weight: bold; font-size: 16px;">
                {value}
            </td>
            """
        html += "</tr>"
    
    html += "</table></div>"
    return html

def show_card_selection(game_id, user_id, is_countdown_active):
    st.markdown("### 🎯 Select Your Cards")
    
    if not is_countdown_active:
        st.warning("⏰ Card selection is closed. Wait for the next game!")
        return
    
    st.markdown(f"💰 Card Price: {CARD_PRICE} ETB each | Max: {MAX_CARDS_PER_PLAYER} cards")
    
    user_cards = get_user_cards(game_id, user_id)
    taken = get_taken_cards(game_id)
    
    if user_cards:
        st.success(f"✅ You have {len(user_cards)} card(s) in this game")
        return
    
    available_cards = [i for i in range(1, TOTAL_CARDS + 1) if i not in taken]
    random.shuffle(available_cards)
    display_cards = available_cards[:50]
    
    st.markdown("#### Available Cards")
    
    cols = st.columns(5)
    for i, card_id in enumerate(display_cards):
        col = cols[i % 5]
        with col:
            is_selected = card_id in st.session_state.selected_temp_cards
            if st.button(
                f"Card {card_id}\n💵 {CARD_PRICE} ETB",
                key=f"card_{card_id}_{game_id}",
                type="primary" if is_selected else "secondary",
                use_container_width=True,
                disabled=not is_countdown_active
            ):
                if card_id in st.session_state.selected_temp_cards:
                    st.session_state.selected_temp_cards.remove(card_id)
                elif len(st.session_state.selected_temp_cards) < MAX_CARDS_PER_PLAYER:
                    st.session_state.selected_temp_cards.append(card_id)
                else:
                    st.warning(f"Maximum {MAX_CARDS_PER_PLAYER} cards allowed")
                st.rerun()
    
    if st.session_state.selected_temp_cards:
        st.markdown("---")
        st.markdown(f"### 📋 Selected Cards: {len(st.session_state.selected_temp_cards)}")
        st.write(f"Total Cost: {len(st.session_state.selected_temp_cards) * CARD_PRICE} ETB")
        
        if st.button("✅ Join Game", type="primary", use_container_width=True, disabled=not is_countdown_active):
            success, message = join_game(game_id, user_id, st.session_state.selected_temp_cards)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

def show_game_board(game):
    game_id = game["game_id"]
    status = game["status"]
    called = json.loads(game.get("called_numbers", "[]"))
    pot = game.get("pot", 0)
    
    st.session_state.called_numbers = called
    
    col1, col2, col3, col4 = st.columns(4)
    
    status_icon = "🟡" if status == "waiting" else "🟢" if status == "running" else "🔴"
    status_label = "Waiting for Players" if status == "waiting" else "Game in Progress" if status == "running" else "Game Ended"
    
    col1.metric("🎮 Status", f"{status_icon} {status_label}")
    col2.metric("💰 Prize Pool", f"{pot} ETB")
    col3.metric("🎯 Numbers Called", f"{len(called)}/75")
    col4.metric("👥 Players", len(get_players(game_id)))
    
    if status == "waiting" and not st.session_state.winner_declared:
        selection_end = datetime.fromisoformat(game["selection_end_time"])
        remaining = max(0, int((selection_end - datetime.now()).total_seconds()))
        st.session_state.countdown_time = remaining
        
        minutes = remaining // 60
        seconds = remaining % 60
        time_color = "#4CAF50" if remaining > 10 else "#FF5722" if remaining > 5 else "#F44336"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1a1a2e, #16213e);
                    border-radius: 15px; margin: 10px 0;">
            <div style="font-size: 3rem; font-weight: bold; color: {time_color};">
                ⏰ {minutes:02d}:{seconds:02d}
            </div>
            <div style="color: white; font-size: 1.2rem;">Time to select cards</div>
        </div>
        """, unsafe_allow_html=True)
        
        if remaining <= 0 and not st.session_state.game_started:
            supabase_admin = get_supabase_admin()
            try:
                supabase_admin.table("bingo_games").update({
                    "status": "running"
                }).eq("game_id", game_id).execute()
                load_all_data()
                st.session_state.game_started = True
                st.session_state.countdown_active = False
                st.rerun()
            except:
                pass
        
        if remaining > 0:
            show_card_selection(game_id, st.session_state.current_user, True)
        else:
            st.warning("⏰ Time's up! Game is starting...")
            st.session_state.countdown_active = False
    
    elif status == "running" and not st.session_state.winner_declared:
        st.session_state.countdown_active = False
        
        st.markdown("### 🎯 BINGO Board")
        
        if called:
            cols = st.columns(15)
            for i, num in enumerate(called):
                col = cols[i % 15]
                if num <= 15:
                    letter = "B"
                    bg = "#FF6B6B"
                elif num <= 30:
                    letter = "I"
                    bg = "#4ECDC4"
                elif num <= 45:
                    letter = "N"
                    bg = "#45B7D1"
                elif num <= 60:
                    letter = "G"
                    bg = "#96CEB4"
                else:
                    letter = "O"
                    bg = "#FFEAA7"
                
                col.markdown(f"""
                <div style="background: {bg}; color: white; padding: 8px; border-radius: 8px; 
                            text-align: center; font-weight: bold; margin: 2px; font-size: 14px;">
                    {letter}{num}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No numbers called yet")
        
        if called:
            last_num = called[-1]
            if last_num <= 15:
                letter = "B"
                bg = "#FF6B6B"
            elif last_num <= 30:
                letter = "I"
                bg = "#4ECDC4"
            elif last_num <= 45:
                letter = "N"
                bg = "#45B7D1"
            elif last_num <= 60:
                letter = "G"
                bg = "#96CEB4"
            else:
                letter = "O"
                bg = "#FFEAA7"
            
            st.markdown(f"""
            <div style="background: {bg}; color: white; padding: 20px; border-radius: 15px; 
                        text-align: center; font-size: 3rem; font-weight: bold; margin: 10px 0;
                        border: 4px solid #8B0000;">
                {letter}{last_num}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 🎮 Game Controls")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎯 Draw Number", type="primary", use_container_width=True):
                num = call_next_number(game_id)
                if num:
                    st.success(f"Number {num} called!")
                    st.rerun()
        
        with col2:
            if st.button("⏯️ Auto-Play" if not st.session_state.auto_play else "⏸️ Pause", use_container_width=True):
                st.session_state.auto_play = not st.session_state.auto_play
                st.rerun()
        
        with col3:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.called_numbers = []
                st.session_state.winner_declared = False
                st.rerun()
        
        if st.session_state.auto_play and len(called) < 75 and not st.session_state.winner_declared:
            time.sleep(4.5)
            num = call_next_number(game_id)
            if num:
                st.rerun()
        
        players = get_players(game_id)
        for username in players.keys():
            user_cards = get_user_cards(game_id, username)
            for card_id in user_cards:
                card_data = get_card_data(card_id)
                pattern = check_winning_pattern(card_data, called)
                if pattern:
                    if declare_winner(game_id, username, card_id, pattern):
                        st.balloons()
                        st.success(f"🎉 {username} WINS with {get_pattern_name(pattern)}!")
                        st.session_state.winner_declared = True
                        st.session_state.auto_play = False
                        load_all_data()
                        st.rerun()
    
    elif status == "finished" or st.session_state.winner_declared:
        st.session_state.countdown_active = False
        st.session_state.auto_play = False
        
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
                <p style="font-size: 1.2rem;">Pattern: {get_pattern_name(json.loads(winner.get('winning_pattern', '{}')))}</p>
                <p style="font-size: 1.2rem;">Card: #{winner.get('card_id', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No winner declared. Game ended.")
        
        if st.button("🆕 Next Game", type="primary", use_container_width=True):
            create_new_game()
            st.rerun()

def show_players_list(game_id):
    players = get_players(game_id)
    if players:
        st.markdown("### 👥 Players")
        for username, count in sorted(players.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"🎯 **{username}**: {count} card(s)")
    else:
        st.info("No players yet. Select cards during countdown!")

def show_user_cards(game_id, user_id):
    user_cards = get_user_cards(game_id, user_id)
    if user_cards:
        st.markdown("### 📋 Your Cards")
        for card_id in user_cards:
            st.markdown(show_bingo_card(card_id, st.session_state.called_numbers), unsafe_allow_html=True)

def show_add_funds():
    st.markdown("### 💰 Add Funds")
    st.markdown("Add funds to your account to play more games.")
    
    with st.form("add_funds"):
        amount = st.number_input("Amount (ETB)", min_value=10, max_value=10000, step=10, value=50)
        phone = st.text_input("📱 Phone Number", placeholder="09XXXXXXXX")
        confirm_code = st.text_input("🔑 Confirmation Code", placeholder="Enter code 2121 for demo")
        
        if st.form_submit_button("💰 Confirm Payment", use_container_width=True):
            if confirm_code == "2121":
                if add_balance(st.session_state.current_user, amount):
                    st.success(f"✅ Added {amount} ETB to your account!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add funds")
            else:
                st.error("❌ Invalid confirmation code. Use 2121 for demo.")

def show_balance_status():
    if st.session_state.logged_in:
        user = st.session_state.user_db.get(st.session_state.current_user, {})
        balance = user.get("balance", 0)
        game_played = user.get("game_played", 0)
        
        status_icon, status_text = get_balance_status(balance)
        
        st.sidebar.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); 
                    padding: 1rem; border-radius: 12px; margin-bottom: 1rem; color: white;">
            <p style="margin: 0; font-weight: 600; font-size: 1.1rem;">👤 {user.get('name', st.session_state.current_user)}</p>
            <p style="margin: 5px 0; font-size: 0.9rem;">@ {st.session_state.current_user}</p>
            <p style="margin: 5px 0; font-size: 1.2rem; font-weight: bold;">💰 {balance} ETB</p>
            <p style="margin: 5px 0; font-size: 0.85rem;">{status_icon} {status_text}</p>
            <p style="margin: 5px 0; font-size: 0.85rem;">🎮 Games Played: {game_played}</p>
            <p style="margin: 5px 0; font-size: 0.85rem;">⭐ Role: {st.session_state.current_role.title()}</p>
        </div>
        """, unsafe_allow_html=True)

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
    
    st.markdown("""
    <style>
        .stButton > button {
            border-radius: 20px !important;
            font-weight: 600 !important;
            border: none !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .stButton > button[type="primary"] {
            background: linear-gradient(135deg, #2E7D32, #4CAF50) !important;
            color: white !important;
        }
        .stSelectbox > div > div {
            background-color: white !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    init_game_db()
    
    with st.sidebar:
        st.markdown("### 🎰 ደራሽ ቢንጎ")
        st.markdown("---")
        
        if st.session_state.logged_in:
            show_balance_status()
            
            role = st.session_state.current_role
            if role == "admin":
                nav_options = ["👑 Admin Dashboard", "🏠 Game Lobby", "💰 Add Funds", "📊 History"]
            else:
                nav_options = ["🏠 Game Lobby", "💰 Add Funds", "📊 My History"]
            
            selected = st.radio("Navigation", nav_options, index=0)
            st.session_state.current_page = selected
            
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
                st.rerun()
            
            st.markdown("---")
            st.markdown("📌 **Card Price:** 10 ETB")
            st.markdown("🏆 **Prize:** 8 ETB per card")
            st.markdown("⏰ **Selection:** 60 seconds")
            st.markdown("🎯 **Max Cards:** 2 per player")
        else:
            st.markdown("👋 Welcome to Derash Bingo!")
            st.markdown("Please login or register to play.")
            if st.button("🔐 Login / Register", use_container_width=True):
                st.rerun()
    
    if not st.session_state.logged_in:
        show_login_page()
        return
    
    current_page = st.session_state.get('current_page', '🏠 Game Lobby')
    
    if current_page == "👑 Admin Dashboard" and st.session_state.current_role == "admin":
        st.markdown("### 👑 Admin Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎮 Total Games", len(st.session_state.games))
        col2.metric("👥 Total Players", len([u for u in st.session_state.user_db if u != "admin"]))
        col3.metric("💰 Total Pot", sum(g.get("pot", 0) for g in st.session_state.games))
        col4.metric("🏆 Total Winners", len(st.session_state.winners))
        
        st.markdown("---")
        st.markdown("#### 🎮 Game Management")
        
        current_game = get_current_game()
        if current_game:
            st.info(f"**Current Game:** #{current_game['game_id']} - Status: {current_game['status']}")
            
            if current_game['status'] == "waiting":
                if st.button("⏰ Force Start Game", use_container_width=True):
                    supabase_admin = get_supabase_admin()
                    try:
                        supabase_admin.table("bingo_games").update({
                            "status": "running"
                        }).eq("game_id", current_game['game_id']).execute()
                        load_all_data()
                        st.session_state.game_started = True
                        st.session_state.countdown_active = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to start game: {e}")
            elif current_game['status'] == "running":
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🎯 Call Number", use_container_width=True):
                        num = call_next_number(current_game['game_id'])
                        if num:
                            st.success(f"Number {num} called!")
                            st.rerun()
                with col2:
                    if st.button("🏁 End Game", use_container_width=True):
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
            if st.button("🆕 Create New Game", type="primary", use_container_width=True):
                game = create_new_game()
                if game:
                    st.success(f"✅ New game created! Game ID: {game['game_id']}")
                    st.rerun()
        
        st.markdown("---")
        st.markdown("#### 👥 User Management")
        users_df = pd.DataFrame([{
            "Username": u,
            "Name": d.get("name", ""),
            "Balance": d.get("balance", 0),
            "Games Played": d.get("game_played", 0),
            "Role": d.get("role", "player")
        } for u, d in st.session_state.user_db.items() if u != "admin"])
        st.dataframe(users_df, use_container_width=True)
        
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
        
        current_game = get_current_game()
        
        if not current_game:
            st.info("No active game. Creating a new game...")
            game = create_new_game()
            if game:
                st.rerun()
            return
        
        game_id = current_game["game_id"]
        status = current_game["status"]
        
        col1, col2 = st.columns([3, 1])
        with col1:
            show_game_board(current_game)
        with col2:
            if status == "waiting":
                show_players_list(game_id)
                st.markdown("---")
                st.markdown("#### ℹ️ How to Play")
                st.markdown("""
                1. Select up to 2 cards
                2. Each card costs 10 ETB
                3. Wait for countdown to end
                4. Game starts automatically
                5. Watch numbers being called
                6. Win by completing a pattern!
                """)
            elif status == "running":
                show_players_list(game_id)
                st.markdown("---")
                show_user_cards(game_id, st.session_state.current_user)
            else:
                show_players_list(game_id)
    
    elif current_page == "💰 Add Funds":
        show_add_funds()
    
    elif current_page in ["📊 History", "📊 My History"]:
        st.markdown("### 📊 Game History")
        
        if st.session_state.winners:
            st.markdown("#### 🏆 Your Wins")
            my_wins = [w for w in st.session_state.winners if w.get("username") == st.session_state.current_user]
            if my_wins:
                df = pd.DataFrame(my_wins)
                df['winning_pattern'] = df['winning_pattern'].apply(lambda x: get_pattern_name(json.loads(x)) if x else "Unknown")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("You haven't won any games yet")
        else:
            st.info("No games played yet")
        
        st.markdown("#### 📈 Your Statistics")
        user = st.session_state.user_db.get(st.session_state.current_user, {})
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 Current Balance", f"{user.get('balance', 0)} ETB")
        with col2:
            st.metric("🎮 Games Played", user.get('game_played', 0))

if __name__ == "__main__":
    main()
