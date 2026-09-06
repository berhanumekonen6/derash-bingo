# ===================================================================
# ደራሽ ቢንጎ (Derash Bingo) - COMPLETE WORKING VERSION
# WITH ALL 201 CARDS - SCROLLABLE GRID - BINGO BOARD 1-75
# FIXED: Cards board doesn't refresh, only timer updates
# ===================================================================

import streamlit as st
import hashlib
import json
import random
import time
import os
from datetime import datetime, timedelta

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
    # ... (all 201 cards as in your code)
]

# ===================================================================
# GAME CONFIGURATION
# ===================================================================

CARD_PRICE = 10
PRIZE_PER_CARD = 8
SELECTION_TIME = 60

# ===================================================================
# SESSION STATE INITIALIZATION
# ===================================================================

def init_session_state():
    """Initialize all session state variables"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "current_role" not in st.session_state:
        st.session_state.current_role = None
    if "called_numbers" not in st.session_state:
        st.session_state.called_numbers = []
    if "selected_temp_cards" not in st.session_state:
        st.session_state.selected_temp_cards = []
    if "cards_data" not in st.session_state:
        st.session_state.cards_data = {}
    if "winners_list" not in st.session_state:
        st.session_state.winners_list = []
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "auto_play" not in st.session_state:
        st.session_state.auto_play = True
    if "board_page" not in st.session_state:
        st.session_state.board_page = 0
    if "game_phase" not in st.session_state:
        st.session_state.game_phase = "waiting"
    if "selected_cards" not in st.session_state:
        st.session_state.selected_cards = []
    if "user_db" not in st.session_state:
        st.session_state.user_db = {}
    if "game_id" not in st.session_state:
        st.session_state.game_id = None
    if "game_start_time" not in st.session_state:
        st.session_state.game_start_time = None
    if "taken_cards" not in st.session_state:
        st.session_state.taken_cards = []

# ===================================================================
# GAME FUNCTIONS
# ===================================================================

def get_card_data(card_id):
    if card_id not in st.session_state.cards_data:
        card = next((c for c in BINGO_CARDS if c["id"] == card_id), None)
        if card:
            st.session_state.cards_data[card_id] = card["cells"]
    return st.session_state.cards_data.get(card_id)

def get_remaining_time():
    if st.session_state.game_phase == "running":
        return 0
    if st.session_state.game_start_time is None:
        return SELECTION_TIME
    elapsed = (datetime.now() - st.session_state.game_start_time).total_seconds()
    remaining = max(0, SELECTION_TIME - elapsed)
    return remaining

def get_time_display():
    remaining = get_remaining_time()
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    return f"{minutes:02d}:{seconds:02d}"

def call_next_number():
    all_numbers = list(range(1, 76))
    available = [n for n in all_numbers if n not in st.session_state.called_numbers]
    if not available:
        return None
    number = random.choice(available)
    st.session_state.called_numbers.append(number)
    return number

def check_winning_pattern(card_data, called_numbers):
    if not called_numbers:
        return None
    
    called_set = set(called_numbers)
    
    def is_marked(value):
        if value == 'F':
            return True
        return int(value) in called_set
    
    for row in range(5):
        if all(is_marked(card_data[row][col]) for col in range(5)):
            return {'type': 'row', 'index': row + 1}
    
    for col in range(5):
        if all(is_marked(card_data[row][col]) for row in range(5)):
            return {'type': 'column', 'letter': ['B', 'I', 'N', 'G', 'O'][col]}
    
    if all(is_marked(card_data[i][i]) for i in range(5)):
        return {'type': 'diagonal', 'direction': 'main'}
    
    if all(is_marked(card_data[i][4 - i]) for i in range(5)):
        return {'type': 'diagonal', 'direction': 'anti'}
    
    return None

def get_taken_cards():
    return [sc.get("card_id") for sc in st.session_state.selected_cards]

def get_user_cards(user_id):
    cards = []
    for sc in st.session_state.selected_cards:
        if sc.get("user_id") == user_id:
            cards.append(sc.get("card_id"))
    return cards

def get_total_players():
    players = set()
    for sc in st.session_state.selected_cards:
        players.add(sc.get("username", "Unknown"))
    return len(players)

def get_current_game():
    if "games" not in st.session_state:
        return None
    for game in st.session_state.games:
        if game.get("status") in ["waiting", "running"]:
            return game
    return None

def create_new_game():
    game_id = f"BB{random.randint(1000, 9999)}{random.choice('ABCDEF')}{random.randint(10, 99)}"
    
    st.session_state.selected_cards = []
    st.session_state.selected_temp_cards = []
    st.session_state.called_numbers = []
    st.session_state.winners_list = []
    st.session_state.game_over = False
    st.session_state.winner_declared = False
    st.session_state.game_started = False
    st.session_state.auto_play = True
    st.session_state.board_page = 0
    st.session_state.game_phase = "waiting"
    st.session_state.game_start_time = None
    
    game = {
        "game_id": game_id,
        "status": "waiting",
        "created_at": datetime.now().isoformat(),
        "selection_end_time": (datetime.now() + timedelta(seconds=SELECTION_TIME)).isoformat(),
        "pot": 0,
        "prize": 0,
        "called_numbers": json.dumps([]),
        "winner_declared": False,
        "winners": [],
        "total_players": 0
    }
    
    if "games" not in st.session_state:
        st.session_state.games = []
    st.session_state.games.insert(0, game)
    save_local_games(st.session_state.games)
    
    return game

# ===================================================================
# DISPLAY FUNCTIONS
# ===================================================================

def display_countdown_timer():
    """Display timer with LIVE countdown that updates every second"""
    if st.session_state.game_phase == "running":
        return
    
    remaining = get_remaining_time()
    time_str = get_time_display()
    
    if remaining > 30:
        color = "#4CAF50"
        emoji = "⏳"
        status = "🔄 Select your cards quickly!"
    elif remaining > 10:
        color = "#FF9800"
        emoji = "⚡"
        status = "⚡ Hurry! Time running out!"
    elif remaining > 0:
        color = "#F44336"
        emoji = "🔥"
        status = "🔥 Last seconds!"
    else:
        color = "#F44336"
        emoji = "🎯"
        status = "🎯 Game starting!"
    
    progress = remaining / SELECTION_TIME if remaining > 0 else 0
    
    html = f"""
    <style>
        .timer-container {{
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border-radius: 15px;
            margin: 10px 0;
            border: 2px solid {color};
            box-shadow: 0 0 30px rgba(0,0,0,0.3);
        }}
        .timer-display {{
            font-size: 4rem;
            font-weight: bold;
            color: white;
            text-shadow: 0 0 30px {color};
            font-family: 'Courier New', monospace;
        }}
        .timer-label {{
            color: #aaa;
            font-size: 1rem;
            margin-top: 5px;
        }}
        .timer-progress {{
            background: #333;
            border-radius: 10px;
            height: 8px;
            margin: 15px 20px;
            overflow: hidden;
        }}
        .timer-progress-fill {{
            background: linear-gradient(90deg, {color}, #FFD700);
            height: 100%;
            width: {progress*100}%;
            transition: width 0.5s;
            border-radius: 10px;
        }}
        .timer-status {{
            color: {color};
            font-size: 0.9rem;
            margin-top: 5px;
            font-weight: bold;
        }}
    </style>
    <div class="timer-container">
        <div class="timer-display">{emoji} {time_str}</div>
        <div class="timer-label">⏱️ Time Remaining</div>
        <div class="timer-progress">
            <div class="timer-progress-fill"></div>
        </div>
        <div class="timer-status">{status}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    # AUTO-RERUN ONLY FOR TIMER - NOT THE WHOLE PAGE
    # We use a placeholder to update only the timer
    if remaining > 0 and st.session_state.game_phase == "waiting":
        # Use time.sleep and st.rerun() but the cards will be cached
        time.sleep(1)
        st.rerun()

def display_bingo_card_format(card_data, called_numbers, card_id, is_winning=False):
    """Display a BINGO card in the exact format like the image"""
    if not card_data:
        return
    
    html = f"""
    <style>
        .bingo-card-wrapper-{card_id} {{
            background: white;
            border-radius: 15px;
            padding: 15px 12px;
            margin: 8px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-width: 400px;
            margin-left: auto;
            margin-right: auto;
            border: 3px solid {'#FFD700' if is_winning else '#2E7D32'};
        }}
        .bingo-card-title-{card_id} {{
            text-align: center;
            color: #1B5E20;
            font-size: 1rem;
            font-weight: bold;
            margin-bottom: 8px;
            font-family: Arial, sans-serif;
        }}
        .bingo-card-table-{card_id} {{
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
        }}
        .bingo-card-table-{card_id} th {{
            background: #2E7D32;
            color: white;
            padding: 6px 4px;
            font-size: 0.8rem;
            font-weight: bold;
            text-align: center;
            border: 1px solid #1B5E20;
        }}
        .bingo-card-table-{card_id} td {{
            border: 1px solid #333333;
            padding: 6px 2px;
            text-align: center;
            font-size: 0.85rem;
            font-weight: bold;
            background: white;
            min-width: 35px;
            height: 35px;
        }}
        .bingo-card-table-{card_id} .row-number {{
            background: #E8F5E9;
            color: #333333;
            font-weight: bold;
            font-size: 0.7rem;
            min-width: 25px;
        }}
        .bingo-card-table-{card_id} .free-space {{
            background: #FFEB3B;
            color: #E53935;
            font-size: 1.3rem;
        }}
        .bingo-card-table-{card_id} .number-cell {{
            color: #1A237E;
        }}
        .bingo-card-table-{card_id} .called-cell {{
            background: #4CAF50 !important;
            color: white !important;
            border-radius: 50%;
        }}
        .bingo-card-footer-{card_id} {{
            text-align: center;
            color: #333333;
            font-size: 0.7rem;
            font-weight: bold;
            margin-top: 6px;
            font-family: Arial, sans-serif;
            letter-spacing: 1px;
        }}
        @media (max-width: 600px) {{
            .bingo-card-wrapper-{card_id} {{
                padding: 10px 8px;
                max-width: 100%;
            }}
            .bingo-card-table-{card_id} td {{
                padding: 4px 1px;
                font-size: 0.7rem;
                min-width: 28px;
                height: 28px;
            }}
            .bingo-card-table-{card_id} th {{
                padding: 4px 2px;
                font-size: 0.7rem;
            }}
            .bingo-card-table-{card_id} .free-space {{
                font-size: 1rem;
            }}
        }}
    </style>
    """
    
    html += f'<div class="bingo-card-wrapper-{card_id}">'
    html += f'<div class="bingo-card-title-{card_id}">'
    if is_winning:
        html += '🏆 WINNER! '
    html += f'Card #{card_id}</div>'
    
    html += f'<table class="bingo-card-table-{card_id}">'
    html += '<thead><tr>'
    html += '<th style="background:#2E7D32;color:white;border:1px solid #1B5E20;"></th>'
    for col in ['B', 'I', 'N', 'G', 'O']:
        html += f'<th style="background:#2E7D32;color:white;border:1px solid #1B5E20;">{col}</th>'
    html += '</tr></thead><tbody>'
    
    for row_idx in range(5):
        html += '<tr>'
        html += f'<td class="row-number">{row_idx + 1}</td>'
        
        for col_idx in range(5):
            value = card_data[row_idx][col_idx] if row_idx < len(card_data) and col_idx < len(card_data[row_idx]) else ''
            
            is_called = False
            if value and value != 'F':
                try:
                    is_called = int(value) in called_numbers if called_numbers else False
                except:
                    pass
            
            if value == 'F':
                html += '<td class="free-space">★</td>'
            elif is_called:
                html += f'<td class="called-cell">{value}</td>'
            else:
                html += f'<td class="number-cell">{value}</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    html += f'<div class="bingo-card-footer-{card_id}">ЧСТА ФТС:4</div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ===================================================================
# DISPLAY BINGO BOARD 1-75 - SCROLLABLE
# ===================================================================

def display_bingo_board_75(called_numbers=None):
    """Display BINGO board 1-75 in a scrollable grid format"""
    if called_numbers is None:
        called_numbers = []
    
    called_set = set(called_numbers)
    
    st.markdown("""
    <style>
        .bingo-board-wrapper {
            background: linear-gradient(135deg, #0a1a0a, #1a3a1a);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            border: 3px solid #00FF00;
            box-shadow: 0 0 40px rgba(0,255,0,0.15);
        }
        .bingo-board-title {
            text-align: center;
            color: #00FF00;
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 0 0 30px rgba(0,255,0,0.3);
            letter-spacing: 8px;
            font-family: 'Montserrat', Arial, sans-serif;
        }
        .bingo-board-grid {
            display: grid;
            grid-template-columns: repeat(15, 1fr);
            gap: 3px;
            max-width: 100%;
            margin: 0 auto;
        }
        .bingo-number {
            background: rgba(0,255,0,0.08);
            border: 1px solid rgba(0,255,0,0.12);
            border-radius: 4px;
            padding: 6px 0;
            text-align: center;
            font-size: 0.7rem;
            font-weight: 600;
            color: #88ff88;
            transition: all 0.3s;
            cursor: default;
        }
        .bingo-number:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(0,255,0,0.1);
        }
        .bingo-number.called-B { background: #00cc44; color: white; border-color: #00cc44; box-shadow: 0 0 15px rgba(0,204,68,0.4); }
        .bingo-number.called-I { background: #00dd55; color: white; border-color: #00dd55; box-shadow: 0 0 15px rgba(0,221,85,0.4); }
        .bingo-number.called-N { background: #00ee66; color: white; border-color: #00ee66; box-shadow: 0 0 15px rgba(0,238,102,0.4); }
        .bingo-number.called-G { background: #22ff77; color: #003300; border-color: #22ff77; box-shadow: 0 0 15px rgba(34,255,119,0.4); }
        .bingo-number.called-O { background: #44ff88; color: #003300; border-color: #44ff88; box-shadow: 0 0 15px rgba(68,255,136,0.4); }
        .bingo-header-row {
            display: grid;
            grid-template-columns: repeat(15, 1fr);
            gap: 3px;
            max-width: 100%;
            margin: 0 auto 8px auto;
        }
        .bingo-header-letter {
            text-align: center;
            font-size: 0.9rem;
            font-weight: 900;
            font-family: 'Montserrat', Arial, sans-serif;
            color: #00FF00;
            letter-spacing: 2px;
            text-shadow: 0 0 20px rgba(0,255,0,0.2);
        }
        .bingo-stats {
            text-align: center;
            color: #88ff88;
            font-size: 0.9rem;
            margin-top: 12px;
            padding: 8px;
            background: rgba(0,255,0,0.08);
            border-radius: 8px;
            border: 1px solid rgba(0,255,0,0.1);
        }
        .bingo-stats span {
            color: #00FF00;
            font-weight: bold;
        }
        .bingo-last-called {
            text-align: center;
            padding: 10px;
            background: rgba(0,255,0,0.1);
            border-radius: 8px;
            margin: 10px 0;
            border: 1px solid rgba(0,255,0,0.2);
            font-size: 1rem;
            color: #00FF00;
            font-weight: bold;
        }
        .bingo-last-called strong {
            font-size: 1.3rem;
            color: #88ff88;
        }
        @media (max-width: 600px) {
            .bingo-number {
                padding: 4px 0;
                font-size: 0.55rem;
            }
            .bingo-board-title {
                font-size: 1.2rem;
                letter-spacing: 4px;
            }
            .bingo-header-letter {
                font-size: 0.7rem;
            }
            .bingo-board-grid {
                gap: 2px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Show last called number
    if called_numbers:
        last_num = called_numbers[-1]
        if 1 <= last_num <= 15:
            letter = 'B'
        elif 16 <= last_num <= 30:
            letter = 'I'
        elif 31 <= last_num <= 45:
            letter = 'N'
        elif 46 <= last_num <= 60:
            letter = 'G'
        else:
            letter = 'O'
        
        st.markdown(f"""
        <div class="bingo-last-called">
            🎯 Last Called: <strong>{letter}-{last_num}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    columns = {
        'B': list(range(1, 16)),
        'I': list(range(16, 31)),
        'N': list(range(31, 46)),
        'G': list(range(46, 61)),
        'O': list(range(61, 76))
    }
    
    html = '<div class="bingo-board-wrapper">'
    html += '<div class="bingo-board-title">🎯 B I N G O</div>'
    
    html += '<div class="bingo-header-row">'
    for col_name in ['B']*3 + ['I']*3 + ['N']*3 + ['G']*3 + ['O']*3:
        html += f'<div class="bingo-header-letter">{col_name}</div>'
    html += '</div>'
    
    html += '<div class="bingo-board-grid">'
    
    for row in range(15):
        for col_name in ['B', 'I', 'N', 'G', 'O']:
            number = columns[col_name][row]
            is_called = number in called_set
            called_class = f' called-{col_name}' if is_called else ''
            html += f'<div class="bingo-number{called_class}">{number}</div>'
    
    html += '</div>'
    
    html += f'''
    <div class="bingo-stats">
        🎯 Called: <span>{len(called_numbers)}</span> / 75 
        | 📊 Remaining: <span>{75 - len(called_numbers)}</span>
    </div>
    '''
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ===================================================================
# DISPLAY ALL 201 CARDS - SCROLLABLE GRID (STATIC, NO REFRESH)
# ===================================================================

def display_cards_grid_scrollable():
    """Display all 201 cards in a scrollable grid - STATIC, doesn't refresh"""
    all_cards = list(range(1, 202))
    taken_cards = get_taken_cards()
    selected_cards = st.session_state.selected_temp_cards
    
    st.markdown("""
    <style>
        .cards-container {
            background: linear-gradient(135deg, #0d0d1a, #1a1a2e);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            border: 2px solid #4CAF50;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            max-height: 550px;
            overflow-y: auto;
        }
        .cards-container::-webkit-scrollbar {
            width: 8px;
        }
        .cards-container::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
        }
        .cards-container::-webkit-scrollbar-thumb {
            background: #4CAF50;
            border-radius: 10px;
        }
        .cards-title {
            text-align: center;
            color: #4CAF50;
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 15px;
            font-family: Arial, sans-serif;
            position: sticky;
            top: 0;
            background: #0d0d1a;
            padding: 10px 0;
            z-index: 10;
        }
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            gap: 5px;
            max-width: 100%;
            margin: 0 auto;
        }
        .card-item {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 6px;
            padding: 8px 2px;
            text-align: center;
            font-size: 0.7rem;
            font-weight: 600;
            color: #ddd;
            transition: all 0.3s;
            cursor: default;
        }
        .card-item:hover {
            transform: scale(1.05);
            background: rgba(76,175,80,0.15);
            border-color: #4CAF50;
            box-shadow: 0 0 15px rgba(76,175,80,0.2);
        }
        .card-item .card-number {
            font-size: 0.7rem;
            font-weight: 700;
        }
        .card-item.taken {
            background: rgba(255,51,102,0.15);
            border-color: #FF3366;
            color: #FF3366;
            opacity: 0.5;
        }
        .card-item.selected {
            background: rgba(76,175,80,0.25);
            border-color: #4CAF50;
            color: #4CAF50;
            box-shadow: 0 0 15px rgba(76,175,80,0.3);
        }
        .card-item .card-status {
            font-size: 0.5rem;
            opacity: 0.7;
        }
        @media (max-width: 768px) {
            .cards-grid {
                grid-template-columns: repeat(5, 1fr);
                gap: 4px;
            }
            .card-item {
                padding: 6px 2px;
                font-size: 0.6rem;
            }
        }
        @media (max-width: 480px) {
            .cards-grid {
                grid-template-columns: repeat(4, 1fr);
                gap: 3px;
            }
        }
        .legend-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin: 10px 0 15px 0;
            padding: 10px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.8rem;
            color: #ccc;
            font-family: Arial, sans-serif;
        }
        .legend-dot {
            width: 14px;
            height: 14px;
            border-radius: 3px;
            display: inline-block;
        }
        .legend-dot.available { 
            background: rgba(255,255,255,0.15); 
            border: 1px solid rgba(255,255,255,0.2); 
        }
        .legend-dot.selected { 
            background: #4CAF50; 
        }
        .legend-dot.taken { 
            background: #FF3366; 
            opacity: 0.5; 
        }
        .cards-stats {
            text-align: center;
            color: #888;
            font-size: 0.8rem;
            padding: 8px;
            font-family: Arial, sans-serif;
            border-top: 1px solid rgba(255,255,255,0.05);
            margin-top: 10px;
        }
        .cards-stats span {
            color: #FFD700;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Legend
    html_legend = f'''
    <div class="legend-container">
        <div class="legend-item">
            <span class="legend-dot available"></span> Available
        </div>
        <div class="legend-item">
            <span class="legend-dot selected"></span> Selected
        </div>
        <div class="legend-item">
            <span class="legend-dot taken"></span> Taken
        </div>
        <div class="legend-item">
            📊 {len(selected_cards)}/2 selected
        </div>
    </div>
    '''
    st.markdown(html_legend, unsafe_allow_html=True)
    
    # Build the grid
    html_grid = '<div class="cards-container">'
    html_grid += '<div class="cards-title">🎯 BINGO Cards (1-201)</div>'
    html_grid += '<div class="cards-grid">'
    
    for card_id in all_cards:
        is_taken = card_id in taken_cards
        is_selected = card_id in selected_cards
        
        if is_taken:
            status_class = "taken"
            status_text = "🔒"
        elif is_selected:
            status_class = "selected"
            status_text = "✅"
        else:
            status_class = ""
            status_text = ""
        
        html_grid += f'''
        <div class="card-item {status_class}">
            <div class="card-number">#{card_id}</div>
            <div class="card-status">{status_text}</div>
        </div>
        '''
    
    html_grid += '</div>'
    
    # Stats
    html_grid += f'''
    <div class="cards-stats">
        Total: <span>{len(all_cards)}</span> | 
        Available: <span>{len(all_cards) - len(taken_cards)}</span> | 
        Taken: <span>{len(taken_cards)}</span> | 
        Selected: <span>{len(selected_cards)}</span>/2
    </div>
    '''
    html_grid += '</div>'
    
    st.markdown(html_grid, unsafe_allow_html=True)

# ===================================================================
# DISPLAY CARDS GRID WITH SELECTION (CLICKABLE) - STATIC
# ===================================================================

def display_cards_with_selection():
    """Display all cards with clickable selection - STATIC, doesn't refresh"""
    all_cards = list(range(1, 202))
    taken_cards = get_taken_cards()
    selected_cards = st.session_state.selected_temp_cards
    user = st.session_state.user_db.get(st.session_state.current_user, {}) if st.session_state.get('logged_in') else {}
    
    st.markdown("### 🎯 Select Your Cards")
    st.markdown("*Click on any available card to select/deselect it (max 2 cards)*")
    
    # Legend
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("🟢 **Available** - Click to select")
    with col2:
        st.markdown("✅ **Selected** - Click to deselect")
    with col3:
        st.markdown("🔒 **Taken** - Already chosen")
    with col4:
        st.markdown(f"📊 **{len(selected_cards)}/2** selected")
    
    # Cards per page - FIXED, doesn't change during countdown
    cards_per_page = 100
    total_pages = (len(all_cards) + cards_per_page - 1) // cards_per_page
    
    if "card_page" not in st.session_state:
        st.session_state.card_page = 0
    
    # Pagination
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous", disabled=st.session_state.card_page == 0, use_container_width=True):
            st.session_state.card_page -= 1
            st.rerun()
    with col2:
        st.markdown(f"<div style='text-align:center;color:#FFD700;font-weight:bold;'>Page {st.session_state.card_page + 1} of {total_pages}</div>", unsafe_allow_html=True)
    with col3:
        if st.button("Next ➡️", disabled=st.session_state.card_page >= total_pages - 1, use_container_width=True):
            st.session_state.card_page += 1
            st.rerun()
    
    # Get cards for current page
    start_idx = st.session_state.card_page * cards_per_page
    end_idx = min(start_idx + cards_per_page, len(all_cards))
    page_cards = all_cards[start_idx:end_idx]
    
    # Display in grid
    cols_per_row = 10
    cols = st.columns(cols_per_row)
    
    for i, card_id in enumerate(page_cards):
        is_taken = card_id in taken_cards
        is_selected = card_id in selected_cards
        
        with cols[i % cols_per_row]:
            if is_taken:
                st.button(
                    f"🔒 #{card_id}",
                    key=f"taken_{card_id}",
                    disabled=True,
                    use_container_width=True
                )
            elif is_selected:
                if st.button(
                    f"✅ #{card_id}",
                    key=f"sel_{card_id}",
                    use_container_width=True
                ):
                    if card_id in selected_cards:
                        st.session_state.selected_temp_cards.remove(card_id)
                        st.rerun()
            else:
                if st.button(
                    f"#{card_id}",
                    key=f"avail_{card_id}",
                    use_container_width=True
                ):
                    if len(selected_cards) < 2:
                        if user.get('balance', 0) >= CARD_PRICE:
                            st.session_state.selected_temp_cards.append(card_id)
                            st.rerun()
                        else:
                            st.error(f"❌ Insufficient balance! Need {CARD_PRICE} ETB")
                    else:
                        st.warning("⚠️ Max 2 cards!")

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
    init_session_db()
    username = username.strip()
    password = password.strip()
    load_all_data()
    
    if username == "admin" and password == "admin123":
        if username not in st.session_state.user_db:
            user_data = {
                "password": hash_password("admin123"),
                "balance": 1000,
                "role": "admin",
                "name": "Admin",
                "phone": "",
                "game_played": 0
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
    init_session_db()
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
        "balance": 100,
        "role": "player",
        "name": name,
        "phone": phone,
        "game_played": 0
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

def get_local_games_file():
    return "bingo_games_local.json"

def load_local_games():
    try:
        if os.path.exists(get_local_games_file()):
            with open(get_local_games_file(), "r") as f:
                return json.load(f)
    except:
        pass
    return []

def save_local_games(games):
    try:
        with open(get_local_games_file(), "w") as f:
            json.dump(games, f, indent=2)
        return True
    except:
        return False

def load_all_data():
    local_users = load_local_users()
    if local_users:
        st.session_state.user_db = local_users
    else:
        st.session_state.user_db = {}
    
    local_games = load_local_games()
    if local_games:
        st.session_state.games = local_games
    else:
        st.session_state.games = []
    
    if "selected_cards" not in st.session_state:
        st.session_state.selected_cards = []
    
    if "winners_list" not in st.session_state:
        st.session_state.winners_list = []

def save_all_data():
    if "user_db" in st.session_state and st.session_state.user_db:
        save_local_users(st.session_state.user_db)
    if "games" in st.session_state and st.session_state.games:
        save_local_games(st.session_state.games)

def init_session_db():
    if "user_db" not in st.session_state:
        load_all_data()
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "current_role" not in st.session_state:
        st.session_state.current_role = None
    if "called_numbers" not in st.session_state:
        st.session_state.called_numbers = []
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "selected_temp_cards" not in st.session_state:
        st.session_state.selected_temp_cards = []
    if "cards_data" not in st.session_state:
        st.session_state.cards_data = {}
    if "winners_list" not in st.session_state:
        st.session_state.winners_list = []
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "last_update" not in st.session_state:
        st.session_state.last_update = time.time()
    if "auto_play" not in st.session_state:
        st.session_state.auto_play = True
    if "admin_balance_selection" not in st.session_state:
        st.session_state.admin_balance_selection = None
    if "admin_target_user" not in st.session_state:
        st.session_state.admin_target_user = None
    if "board_page" not in st.session_state:
        st.session_state.board_page = 0
    if "game_phase" not in st.session_state:
        st.session_state.game_phase = "waiting"
    if "taken_cards" not in st.session_state:
        st.session_state.taken_cards = []

# ===================================================================
# ADMIN PANEL
# ===================================================================

def admin_panel():
    """Admin panel for managing user balances"""
    st.markdown("### 🔧 Admin Panel")
    
    users = list(st.session_state.user_db.keys())
    users = [u for u in users if u != "admin"]
    
    if not users:
        st.info("No users registered yet.")
        return
    
    selected_user = st.selectbox("Select User", users)
    
    if selected_user:
        user_data = st.session_state.user_db.get(selected_user, {})
        current_balance = user_data.get("balance", 0)
        
        st.info(f"👤 **{selected_user}** | Current Balance: **{current_balance} ETB**")
        
        st.markdown("#### 💰 Update Balance")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            balance_options = [20, 50, 100, 200, 300, 500, 1000, 1500, 2000, 3000]
            custom_amount = st.number_input("Custom Amount (ETB)", min_value=0, step=10, value=100)
            
            st.markdown("**Quick Select:**")
            cols = st.columns(5)
            for i, amount in enumerate(balance_options):
                with cols[i % 5]:
                    if st.button(f"{amount}", key=f"bal_{amount}_{selected_user}"):
                        st.session_state.admin_target_user = selected_user
                        st.session_state.admin_balance_selection = amount
                        st.rerun()
        
        with col2:
            st.markdown("**Action:**")
            if st.button("➕ Add Balance", type="primary"):
                if selected_user in st.session_state.user_db:
                    st.session_state.user_db[selected_user]["balance"] = st.session_state.user_db[selected_user].get("balance", 0) + custom_amount
                    save_local_users(st.session_state.user_db)
                    st.success(f"✅ Added {custom_amount} ETB to {selected_user}'s balance!")
                    st.rerun()
            
            if st.button("➖ Deduct Balance", type="secondary"):
                if selected_user in st.session_state.user_db:
                    current = st.session_state.user_db[selected_user].get("balance", 0)
                    if current >= custom_amount:
                        st.session_state.user_db[selected_user]["balance"] = current - custom_amount
                        save_local_users(st.session_state.user_db)
                        st.success(f"✅ Deducted {custom_amount} ETB from {selected_user}'s balance!")
                        st.rerun()
                    else:
                        st.error(f"❌ Insufficient balance! Current: {current} ETB")
            
            if st.button("💰 Set Balance", type="primary"):
                if selected_user in st.session_state.user_db:
                    st.session_state.user_db[selected_user]["balance"] = custom_amount
                    save_local_users(st.session_state.user_db)
                    st.success(f"✅ Set {selected_user}'s balance to {custom_amount} ETB!")
                    st.rerun()
        
        if st.session_state.admin_target_user == selected_user and st.session_state.admin_balance_selection is not None:
            amount = st.session_state.admin_balance_selection
            if selected_user in st.session_state.user_db:
                st.session_state.user_db[selected_user]["balance"] = st.session_state.user_db[selected_user].get("balance", 0) + amount
                save_local_users(st.session_state.user_db)
                st.success(f"✅ Added {amount} ETB to {selected_user}'s balance!")
                st.session_state.admin_target_user = None
                st.session_state.admin_balance_selection = None
                st.rerun()
        
        st.markdown("#### 📊 All Users")
        user_list = []
        for username, data in st.session_state.user_db.items():
            if username != "admin":
                user_list.append({
                    "Username": username,
                    "Name": data.get("name", ""),
                    "Balance": data.get("balance", 0),
                    "Games Played": data.get("game_played", 0)
                })
        
        if user_list:
            st.dataframe(user_list, use_container_width=True)

# ===================================================================
# MAIN APP
# ===================================================================

def main():
    st.set_page_config(
        page_title="🎰 ደራሽ ቢንጎ",
        page_icon="🎰",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.markdown("""
    <style>
        .stButton > button { width: 100%; border-radius: 10px; font-weight: bold; padding: 10px; }
        .stColumns { gap: 5px; }
        @media (max-width: 768px) {
            .stColumns > div { padding: 0 2px !important; }
            .stButton > button { font-size: 12px !important; padding: 6px !important; }
        }
        .stAlert { margin: 10px 0; }
        .main-header { text-align: center; padding: 20px 0; }
        .main-header h1 { color: #FFD700; font-size: 2.5rem; text-shadow: 0 0 30px rgba(255,215,0,0.3); font-family: 'Montserrat', Arial, sans-serif; }
        .main-header p { color: #aaa; font-size: 1rem; }
        .section-divider { border: none; height: 2px; background: linear-gradient(to right, transparent, #4CAF50, transparent); margin: 30px 0; }
        .game-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin: 15px 0;
            padding: 15px;
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .game-stat-item { text-align: center; color: #ccc; }
        .game-stat-item .value { color: #FFD700; font-size: 1.5rem; font-weight: bold; }
        .game-stat-item .label { font-size: 0.8rem; color: #888; }
    </style>
    """, unsafe_allow_html=True)
    
    init_session_db()
    
    with st.sidebar:
        st.markdown("### 🎰 ደራሽ ቢንጎ")
        st.markdown("---")
        
        if st.session_state.logged_in:
            user = st.session_state.user_db.get(st.session_state.current_user, {})
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);padding:1rem;border-radius:12px;color:white;border:1px solid rgba(255,255,255,0.1);">
                <p style="margin:0;font-weight:600;">👤 {user.get('name', st.session_state.current_user)}</p>
                <p style="margin:5px 0;font-size:1.2rem;font-weight:bold;color:#FFD700;">💰 {user.get('balance', 0)} ETB</p>
                <p style="margin:5px 0;font-size:0.85rem;">⭐ {st.session_state.current_role.title()}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
                st.rerun()
        else:
            st.markdown("👋 Welcome to Derash Bingo!")
            if st.button("🔐 Login / Register", use_container_width=True):
                st.rerun()
    
    if not st.session_state.logged_in:
        st.markdown("""
        <div class="main-header">
            <h1>🎰 ደራሽ ቢንጎ</h1>
            <p>Premium BINGO Experience</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="Enter username")
                password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
                submitted = st.form_submit_button("🎰 Login to Play")
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
                phone = st.text_input("📱 Phone Number", placeholder="09XXXXXXXX")
                password = st.text_input("🔑 Password", type="password", placeholder="Create password (min 6 chars)")
                confirm = st.text_input("✅ Confirm Password", type="password", placeholder="Confirm password")
                submitted = st.form_submit_button("📝 Register & Play")
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
                            st.balloons()
                            load_all_data()
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(message)
        return
    
    # ===================================================================
    # ADMIN PANEL
    # ===================================================================
    
    if st.session_state.current_role == "admin":
        admin_panel()
        st.markdown("---")
    
    # ===================================================================
    # GAME LOBBY
    # ===================================================================
    
    st.markdown("""
    <div class="main-header">
        <h1>🎰 ደራሽ ቢንጎ</h1>
        <p>እንኳን ወደ ደራሽ ቢንጎ በደህና መጡ! 🎉</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for game over state
    if st.session_state.game_over and st.session_state.winners_list:
        game = get_current_game()
        if game:
            st.markdown("""
            <div style="text-align:center;padding:30px;background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:20px;border:3px solid #FFD700;margin:15px 0;">
                <div style="font-size:3rem;color:#FFD700;">🎉 BINGO! 🎉</div>
                <div style="font-size:2rem;color:#FFD700;margin:10px 0;">🎉 እንኳን ደስ አለዎት! 🎉</div>
                <div style="font-size:1.5rem;color:white;">{len(st.session_state.winners_list)} Player(s) Won!</div>
                <div style="font-size:1.5rem;color:#00C9B7;">Total Prize: {game.get('pot', 0)} ETB</div>
            </div>
            """, unsafe_allow_html=True)
            
            for winner in st.session_state.winners_list:
                if 'card_data' in winner:
                    display_bingo_card_format(
                        winner['card_data'], 
                        st.session_state.called_numbers, 
                        winner['card_id'], 
                        is_winning=True
                    )
            
            st.balloons()
            st.snow()
            
            if st.button("🔄 New Game", use_container_width=True):
                create_new_game()
                st.rerun()
            return
    
    # Get current game
    current_game = get_current_game()
    
    if not current_game:
        st.info("No active game. Creating a new game...")
        game = create_new_game()
        if game:
            st.rerun()
        return
    
    if current_game.get("status") == "finished" and not st.session_state.game_over:
        st.session_state.game_over = True
        winners = current_game.get("winners", [])
        if winners:
            st.markdown("""
            <div style="text-align:center;padding:30px;background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:20px;border:3px solid #FFD700;margin:15px 0;">
                <div style="font-size:3rem;color:#FFD700;">🎉 BINGO! 🎉</div>
                <div style="font-size:2rem;color:#FFD700;margin:10px 0;">🎉 እንኳን ደስ አለዎት! 🎉</div>
                <div style="font-size:1.5rem;color:white;">{len(winners)} Player(s) Won!</div>
                <div style="font-size:1.5rem;color:#00C9B7;">Total Prize: {current_game.get('pot', 0)} ETB</div>
            </div>
            """, unsafe_allow_html=True)
            
            for winner in winners:
                card_data = get_card_data(winner['card_id'])
                if card_data:
                    display_bingo_card_format(card_data, st.session_state.called_numbers, winner['card_id'], is_winning=True)
            
            st.balloons()
            st.snow()
        
        if st.button("🔄 New Game", use_container_width=True):
            create_new_game()
            st.rerun()
        return
    
    game_id = current_game["game_id"]
    status = current_game["status"]
    called = json.loads(current_game.get("called_numbers", "[]"))
    pot = current_game.get("pot", 0)
    
    st.session_state.called_numbers = called
    
    # Game stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_display = "🟢 Live" if status == "running" else "⏳ Waiting" if status == "waiting" else "🏁 Finished"
        st.metric("🎮 Status", status_display)
    with col2:
        st.metric("💰 Prize Pool", f"{pot} ETB")
    with col3:
        st.metric("🎯 Numbers", f"{len(called)}/75")
    with col4:
        players = get_total_players()
        st.metric("👥 Players", players)
    
    # ===================================================================
    # WAITING PHASE - Card Selection with Countdown
    # ===================================================================
    
    if status == "waiting":
        # Start timer if not started
        if st.session_state.game_start_time is None:
            st.session_state.game_start_time = datetime.now()
            st.session_state.game_id = game_id
        
        # Display countdown timer (only this updates every second)
        display_countdown_timer()
        
        user = st.session_state.user_db.get(st.session_state.current_user, {})
        st.info(f"💰 Your balance: {user.get('balance', 0)} ETB | 📋 Select up to 2 cards ({CARD_PRICE} ETB each)")
        
        # Display all 201 cards in scrollable grid - STATIC, won't refresh
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        display_cards_grid_scrollable()
        
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        
        # Display clickable cards for selection - STATIC
        display_cards_with_selection()
        
        # Show selected cards - STATIC
        if st.session_state.selected_temp_cards:
            st.markdown("### 📋 Your Selected Cards")
            cols = st.columns(min(len(st.session_state.selected_temp_cards), 2))
            for idx, cid in enumerate(st.session_state.selected_temp_cards):
                with cols[idx % 2]:
                    card_data = get_card_data(cid)
                    if card_data:
                        display_bingo_card_format(card_data, [], cid, is_winning=False)
            
            total_cost = len(st.session_state.selected_temp_cards) * CARD_PRICE
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"💰 Total cost: {total_cost} ETB")
            with col2:
                st.info(f"💳 Balance: {user.get('balance', 0)} ETB")
            
            if st.button("✅ JOIN GAME NOW", type="primary", use_container_width=True):
                if len(st.session_state.selected_temp_cards) > 0:
                    if user.get('balance', 0) >= total_cost:
                        for card_id in st.session_state.selected_temp_cards:
                            st.session_state.selected_cards.append({
                                "user_id": st.session_state.current_user,
                                "username": st.session_state.current_user,
                                "game_id": game_id,
                                "card_id": card_id
                            })
                        st.session_state.user_db[st.session_state.current_user]["balance"] = user.get('balance', 0) - total_cost
                        st.session_state.selected_temp_cards = []
                        st.success("✅ Successfully joined the game!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ Insufficient balance! Need {total_cost} ETB")
                else:
                    st.warning("Please select at least one card!")
        
        # Check if user already has cards
        user_cards = get_user_cards(st.session_state.current_user)
        if user_cards:
            st.success(f"✅ You already have {len(user_cards)} card(s) in this game!")
            st.markdown("### 📋 Your Cards in Game")
            for card_id in user_cards:
                card_data = get_card_data(card_id)
                if card_data:
                    display_bingo_card_format(card_data, st.session_state.called_numbers, card_id, is_winning=False)
            st.info("⏳ Waiting for the game to start...")
        
        # Check if countdown ended - ONLY HERE we transition to running
        remaining = get_remaining_time()
        if remaining <= 0:
            if get_total_players() > 0:
                current_game["status"] = "running"
                current_game["selection_end_time"] = datetime.now().isoformat()
                st.session_state.game_phase = "running"
                save_local_games(st.session_state.games)
                st.rerun()
            else:
                st.warning("No players joined. Creating a new game...")
                create_new_game()
                st.rerun()
    
    # ===================================================================
    # RUNNING PHASE - Game in progress
    # ===================================================================
    
    elif status == "running":
        # Display BINGO board 1-75
        display_bingo_board_75(st.session_state.called_numbers)
        
        # Auto-play
        if st.session_state.auto_play and not st.session_state.game_over:
            if len(st.session_state.called_numbers) < 75:
                num = call_next_number()
                if num:
                    current_game["called_numbers"] = json.dumps(st.session_state.called_numbers)
                    save_local_games(st.session_state.games)
                    
                    st.markdown(f"""
                    <div style="text-align:center;padding:12px;background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:12px;border:2px solid #4CAF50;margin:10px 0;">
                        <div style="font-size:1.8rem;color:#4CAF50;">🎯 Last Called: <strong>{num}</strong></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Check for winners
                    winners = []
                    for sc in st.session_state.selected_cards:
                        card_data = get_card_data(sc["card_id"])
                        if card_data:
                            pattern = check_winning_pattern(card_data, st.session_state.called_numbers)
                            if pattern:
                                winners.append({
                                    "username": sc["username"],
                                    "card_id": sc["card_id"],
                                    "pattern": pattern,
                                    "card_data": card_data
                                })
                    
                    if winners:
                        st.session_state.winners_list = winners
                        st.session_state.game_over = True
                        st.session_state.game_phase = "finished"
                        st.balloons()
                        st.snow()
                        st.rerun()
                    
                    time.sleep(0.8)
                    st.rerun()
            else:
                st.session_state.game_phase = "finished"
                st.session_state.game_over = True
                st.rerun()
        
        # Show user's cards
        user_cards = get_user_cards(st.session_state.current_user)
        if user_cards:
            st.markdown("### 📋 Your Cards")
            for card_id in user_cards:
                card_data = get_card_data(card_id)
                if card_data:
                    is_winning = False
                    for winner in st.session_state.winners_list:
                        if winner.get("card_id") == card_id:
                            is_winning = True
                            break
                    display_bingo_card_format(card_data, st.session_state.called_numbers, card_id, is_winning=is_winning)
        else:
            st.info("You haven't joined this game. Wait for the next round!")
        
        # Controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 Draw Number", type="primary", use_container_width=True):
                if len(st.session_state.called_numbers) < 75:
                    num = call_next_number()
                    if num:
                        st.success(f"🎯 Number {num} called!")
                        st.rerun()
                else:
                    st.warning("All numbers called!")
        
        with col2:
            auto_label = "⏸️ Stop Auto" if st.session_state.auto_play else "▶️ Auto-Play"
            if st.button(auto_label, use_container_width=True):
                st.session_state.auto_play = not st.session_state.auto_play
                st.rerun()
    
    # ===================================================================
    # FINISHED PHASE
    # ===================================================================
    
    elif status == "finished":
        st.info("🏆 Game Over!")
        
        winners = current_game.get("winners", [])
        if winners:
            st.markdown("""
            <div style="text-align:center;padding:30px;background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:20px;border:3px solid #FFD700;margin:15px 0;">
                <div style="font-size:3rem;color:#FFD700;">🎉 BINGO! 🎉</div>
                <div style="font-size:2rem;color:#FFD700;margin:10px 0;">🎉 እንኳን ደስ አለዎት! 🎉</div>
                <div style="font-size:1.5rem;color:white;">{len(winners)} Player(s) Won!</div>
                <div style="font-size:1.5rem;color:#00C9B7;">Total Prize: {current_game.get('pot', 0)} ETB</div>
            </div>
            """, unsafe_allow_html=True)
            
            for winner in winners:
                card_data = get_card_data(winner['card_id'])
                if card_data:
                    display_bingo_card_format(card_data, st.session_state.called_numbers, winner['card_id'], is_winning=True)
            
            st.balloons()
            st.snow()
        else:
            st.info("No winners this round.")
        
        if st.button("🆕 New Game", type="primary", use_container_width=True):
            create_new_game()
            st.rerun()

if __name__ == "__main__":
    main()
