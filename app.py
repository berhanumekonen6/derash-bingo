import streamlit as st
import random
import time

st.set_page_config(
    page_title="ደራሽ ቢንጎ",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if 'clicked_numbers' not in st.session_state:
    st.session_state.clicked_numbers = set()
if 'selected_card' not in st.session_state:
    st.session_state.selected_card = None
if 'called_numbers' not in st.session_state:
    st.session_state.called_numbers = set()
if 'last_called_number' not in st.session_state:
    st.session_state.last_called_number = None
if 'is_auto_calling' not in st.session_state:
    st.session_state.is_auto_calling = False
if 'auto_called_count' not in st.session_state:
    st.session_state.auto_called_count = 0
if 'last_call_time' not in st.session_state:
    st.session_state.last_call_time = time.time()

# Check if we need to auto-call
if st.session_state.is_auto_calling:
    if len(st.session_state.called_numbers) < 75:
        current_time = time.time()
        if current_time - st.session_state.last_call_time >= 3.0:
            available = [i for i in range(1, 76) if i not in st.session_state.called_numbers]
            if available:
                called_num = random.choice(available)
                st.session_state.called_numbers.add(called_num)
                st.session_state.last_called_number = called_num
                st.session_state.auto_called_count += 1
                st.session_state.last_call_time = current_time
                st.rerun()
    else:
        st.session_state.is_auto_calling = False

# ===================================================================
# ENHANCED CSS STYLES - MOBILE FIRST
# ===================================================================

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    /* Mobile-first responsive design */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 10px;
    }
    
    /* BINGO Board Container - Mobile First */
    .master-board-container {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 15px;
        padding: 15px;
        margin: 10px auto;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        border: 2px solid #2E7D32;
        position: relative;
        overflow: hidden;
        max-width: 100%;
    }
    
    .master-board-title {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 900;
        color: #1B5E20;
        margin-bottom: 12px;
        letter-spacing: 3px;
    }
    
    /* Circle Numbers - Mobile Optimized */
    .circle-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(145deg, #E8F5E9, #C8E6C9);
        color: #1A237E;
        font-weight: 900;
        font-size: 0.7rem;
        border: 2px solid #2E7D32;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        font-family: 'Orbitron', sans-serif;
        cursor: pointer;
    }
    
    .circle-number.called {
        background: linear-gradient(145deg, #FF9800, #F57C00);
        color: white;
        border-color: #E65100;
        transform: scale(1.1);
        animation: pop 0.3s ease-out;
        box-shadow: 0 0 20px rgba(255,152,0,0.5);
    }
    
    .circle-number.last-called {
        background: linear-gradient(145deg, #E53935, #C62828);
        color: white;
        border-color: #B71C1C;
        transform: scale(1.2);
        animation: pulse-glow 1s ease-in-out infinite;
        box-shadow: 0 0 30px rgba(229,57,53,0.6);
    }
    
    @keyframes pop {
        0% { transform: scale(0.5); opacity: 0; }
        50% { transform: scale(1.3); }
        100% { transform: scale(1.1); opacity: 1; }
    }
    
    @keyframes pulse-glow {
        0%, 100% { 
            transform: scale(1.2);
            box-shadow: 0 0 30px rgba(229,57,53,0.6);
        }
        50% { 
            transform: scale(1.3);
            box-shadow: 0 0 50px rgba(229,57,53,0.8);
        }
    }
    
    .circle-letter {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: linear-gradient(145deg, #2E7D32, #1B5E20);
        color: white;
        font-weight: 900;
        font-size: 1.2rem;
        border: 3px solid #F9A825;
        margin: auto;
        font-family: 'Orbitron', sans-serif;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Selected Card - Mobile Optimized */
    .selected-card-container {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        max-width: 100%;
        border: 2px solid #2E7D32;
        transition: all 0.3s;
    }
    
    .selected-card-title {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        color: #1B5E20;
        font-size: 1.1rem;
        font-weight: 900;
        margin-bottom: 10px;
        letter-spacing: 2px;
    }
    
    .selected-circle {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: linear-gradient(145deg, #E8F5E9, #C8E6C9);
        color: #1A237E;
        font-weight: 900;
        font-size: 0.8rem;
        border: 2px solid #2E7D32;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        font-family: 'Orbitron', sans-serif;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    .selected-circle.called {
        background: linear-gradient(145deg, #FF9800, #F57C00);
        color: white;
        border-color: #E65100;
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(255,152,0,0.4);
        animation: pop 0.3s ease-out;
    }
    
    .selected-circle.ticked {
        background: linear-gradient(145deg, #4CAF50, #388E3C);
        color: white;
        border-color: #1B5E20;
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(76,175,80,0.3);
    }
    
    .selected-circle.ticked-and-called {
        background: linear-gradient(145deg, #4CAF50, #388E3C);
        color: white;
        border-color: #E65100;
        transform: scale(1.15);
        box-shadow: 0 0 25px rgba(76,175,80,0.5), inset 0 0 15px rgba(255,152,0,0.3);
        animation: pulse-glow-green 1s ease-in-out infinite;
    }
    
    @keyframes pulse-glow-green {
        0%, 100% { 
            transform: scale(1.15);
            box-shadow: 0 0 25px rgba(76,175,80,0.5);
        }
        50% { 
            transform: scale(1.2);
            box-shadow: 0 0 35px rgba(76,175,80,0.7);
        }
    }
    
    .selected-circle.free {
        background: linear-gradient(145deg, #FFEB3B, #FDD835);
        color: #E53935;
        font-size: 1.2rem;
        border-color: #F57F17;
        animation: blink-star 1s ease-in-out infinite;
    }
    
    @keyframes blink-star {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }
    
    /* Buttons - Mobile Friendly */
    .stButton > button {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 0.8rem !important;
        padding: 8px 12px !important;
        min-height: 40px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.95);
    }
    
    /* Number Cards - Mobile Grid */
    .stButton > button[data-testid="baseButton-secondary"] {
        background: linear-gradient(145deg, #e8f5e9, #c8e6c9) !important;
        border: 2px solid #2E7D32 !important;
        color: #1A237E !important;
        font-weight: 700 !important;
        font-size: 0.7rem !important;
        min-height: 35px !important;
        padding: 4px 2px !important;
    }
    
    .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(145deg, #FF9800, #F57C00) !important;
        border: 2px solid #E65100 !important;
        color: white !important;
        font-weight: 700 !important;
        box-shadow: 0 3px 10px rgba(255,152,0,0.3) !important;
        font-size: 0.7rem !important;
        min-height: 35px !important;
        padding: 4px 2px !important;
    }
    
    /* Info Box */
    .stAlert {
        border-radius: 12px !important;
        border-left: 4px solid #2E7D32 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 10px !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #2E7D32, #4CAF50, #8BC34A) !important;
        border-radius: 8px !important;
        height: 6px !important;
    }
    
    /* Footer */
    .footer-stats {
        background: linear-gradient(145deg, #1B5E20, #2E7D32);
        color: white;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 0.7rem;
        letter-spacing: 1px;
        margin-top: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        border: 2px solid #F9A825;
    }
    
    /* Tablet and Desktop */
    @media (min-width: 768px) {
        .master-board-container {
            padding: 25px;
            margin: 20px auto;
            border-radius: 20px;
        }
        
        .master-board-title {
            font-size: 2.2rem;
            letter-spacing: 5px;
        }
        
        .circle-number {
            width: 40px;
            height: 40px;
            font-size: 0.9rem;
            border-width: 3px;
        }
        
        .circle-letter {
            width: 50px;
            height: 50px;
            font-size: 1.5rem;
            border-width: 4px;
        }
        
        .selected-circle {
            width: 45px;
            height: 45px;
            font-size: 0.95rem;
            border-width: 3px;
        }
        
        .selected-card-container {
            padding: 20px;
            border-radius: 20px;
        }
        
        .selected-card-title {
            font-size: 1.3rem;
        }
        
        .stButton > button {
            font-size: 1rem !important;
            padding: 10px 20px !important;
            min-height: 45px !important;
        }
        
        .stButton > button[data-testid="baseButton-secondary"],
        .stButton > button[data-testid="baseButton-primary"] {
            font-size: 0.9rem !important;
            min-height: 40px !important;
            padding: 6px 4px !important;
        }
        
        .footer-stats {
            font-size: 1rem;
            padding: 15px;
        }
    }
    
    @media (min-width: 1024px) {
        .master-board-container {
            padding: 30px;
            max-width: 950px;
        }
        
        .circle-number {
            width: 45px;
            height: 45px;
            font-size: 1rem;
        }
        
        .circle-letter {
            width: 55px;
            height: 55px;
            font-size: 1.8rem;
        }
    }
    
    /* Fix for small screens */
    @media (max-width: 480px) {
        .circle-number {
            width: 28px;
            height: 28px;
            font-size: 0.6rem;
            border-width: 1.5px;
        }
        
        .circle-letter {
            width: 30px;
            height: 30px;
            font-size: 1rem;
            border-width: 2px;
        }
        
        .selected-circle {
            width: 32px;
            height: 32px;
            font-size: 0.7rem;
            border-width: 1.5px;
        }
        
        .stButton > button[data-testid="baseButton-secondary"],
        .stButton > button[data-testid="baseButton-primary"] {
            font-size: 0.6rem !important;
            min-height: 30px !important;
            padding: 2px 1px !important;
        }
        
        .master-board-title {
            font-size: 1.2rem;
        }
        
        .selected-card-title {
            font-size: 0.9rem;
        }
        
        .footer-stats {
            font-size: 0.6rem;
            padding: 8px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# ALL 201 BINGO CARDS - FULL LIST (same as before)
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
    # ... (add all remaining cards here - same as your original code)
]

# For complete implementation, you would add all 201 cards here
# I'm showing the first 10 for brevity

def get_card(card_id):
    for card in BINGO_CARDS:
        if card["id"] == card_id:
            return card
    return None

def display_selected_card(card_id):
    """Display a BINGO card with enhanced styling - mobile optimized"""
    card = get_card(card_id)
    if not card:
        return
    
    cells = card["cells"]
    
    html = f'<div class="selected-card-container">'
    html += f'<div class="selected-card-title">🎯 Card #{card_id}</div>'
    
    html += '<table style="width:100%;border-collapse:collapse;margin:0 auto;">'
    html += '<tr style="text-align:center;">'
    for label in ['B', 'I', 'N', 'G', 'O']:
        html += f'<td style="padding:3px;font-family:Orbitron,sans-serif;font-weight:900;color:#1B5E20;font-size:0.8rem;">{label}</td>'
    html += '</tr>'
    
    for row_idx in range(5):
        html += '<tr style="text-align:center;">'
        for col_idx in range(5):
            value = cells[row_idx][col_idx]
            
            if value == 'F':
                html += f'<td style="padding:3px;"><div class="selected-circle free">★</div></td>'
            else:
                num = int(value)
                is_called = num in st.session_state.called_numbers
                is_ticked = num in st.session_state.clicked_numbers
                
                circle_class = "selected-circle"
                if is_ticked and is_called:
                    circle_class += " ticked-and-called"
                elif is_called:
                    circle_class += " called"
                elif is_ticked:
                    circle_class += " ticked"
                
                html += f'<td style="padding:3px;"><div class="{circle_class}">{value}</div></td>'
        html += '</tr>'
    
    html += '</table>'
    
    # Stats
    total_called_on_card = 0
    total_ticked = 0
    for row in cells:
        for val in row:
            if val != 'F':
                num = int(val)
                if num in st.session_state.called_numbers:
                    total_called_on_card += 1
                if num in st.session_state.clicked_numbers:
                    total_ticked += 1
    
    html += f'<div style="text-align:center;margin-top:10px;font-family:Orbitron,sans-serif;font-size:0.7rem;color:#333;background:#f5f5f5;padding:6px;border-radius:8px;">✅ {total_called_on_card}/24 called | ⭐ {total_ticked} ticked</div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

def display_master_board():
    """Display the BINGO board with enhanced styling - mobile optimized"""
    master_board = {
        'B': list(range(1, 16)),
        'I': list(range(16, 31)),
        'N': list(range(31, 46)),
        'G': list(range(46, 61)),
        'O': list(range(61, 76))
    }
    
    html = '<div class="master-board-container">'
    html += '<div class="master-board-title">🎯 BINGO Board</div>'
    
    # Last called number display
    if st.session_state.last_called_number:
        html += f'''
        <div style="text-align:center;font-size:1.2rem;font-weight:900;font-family:Orbitron,sans-serif;color:#E53935;margin-bottom:12px;">
            🎯 Last Called: 
            <span style="background:linear-gradient(145deg,#E53935,#C62828);color:white;padding:5px 18px;border-radius:25px;display:inline-block;box-shadow:0 3px 15px rgba(229,57,53,0.4);border:2px solid #F9A825;font-size:1.1rem;">
                {st.session_state.last_called_number}
            </span>
        </div>
        '''
    
    html += '<table style="width:100%;border-collapse:collapse;position:relative;z-index:1;">'
    
    for letter in ['B', 'I', 'N', 'G', 'O']:
        html += '<tr>'
        html += f'<td style="padding:3px;text-align:center;"><div class="circle-letter">{letter}</div></td>'
        for num in master_board[letter]:
            is_called = num in st.session_state.called_numbers
            is_last = num == st.session_state.last_called_number
            
            circle_class = "circle-number"
            if is_last:
                circle_class += " last-called"
            elif is_called:
                circle_class += " called"
            
            html += f'<td style="padding:3px;text-align:center;"><div class="{circle_class}">{num}</div></td>'
        html += '</tr>'
    
    html += '</table>'
    
    # Stats
    html += f'''
    <div style="text-align:center;margin-top:15px;font-family:Orbitron,sans-serif;font-size:0.9rem;color:#333;padding:10px;background:linear-gradient(145deg,#f5f5f5,#e8e8e8);border-radius:10px;position:relative;z-index:1;">
        📊 Called: <strong style="color:#2E7D32;font-size:1.1rem;">{len(st.session_state.called_numbers)}</strong> / 75 numbers
        <div style="margin-top:3px;font-size:0.7rem;color:#666;">
            {f"{len(st.session_state.called_numbers)/75*100:.1f}% complete" if len(st.session_state.called_numbers) > 0 else "Game not started"}
        </div>
    </div>
    '''
    
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ===================================================================
# MAIN APP - MOBILE FIRST LAYOUT
# ===================================================================

# Header
st.markdown("""
<div style="text-align:center;padding:15px 10px;margin-bottom:10px;">
    <h1 style="font-family:'Orbitron',sans-serif;font-weight:900;font-size:2rem;color:#1B5E20;text-shadow:2px 2px 4px rgba(0,0,0,0.1);letter-spacing:5px;margin:0;">
        🎯 ደራሽ ቢንጎ
    </h1>
    <p style="font-family:'Orbitron',sans-serif;color:#555;font-weight:400;letter-spacing:2px;font-size:0.8rem;margin:5px 0;">
        Derash BINGO - 201 Cards
    </p>
</div>
""", unsafe_allow_html=True)

# SINGLE COLUMN LAYOUT - Mobile First
# Display Master Board
display_master_board()

# Display Selected Card right after the board
if st.session_state.selected_card:
    display_selected_card(st.session_state.selected_card)
else:
    st.markdown("""
    <div style="background:linear-gradient(145deg,#f8f9fa,#e8e8e8);border-radius:15px;padding:25px 15px;text-align:center;border:2px dashed #2E7D32;margin:10px 0;">
        <div style="font-size:2.5rem;margin-bottom:8px;">👆</div>
        <div style="font-family:'Orbitron',sans-serif;font-weight:700;color:#555;font-size:0.9rem;">
            Click a card number below to select it
        </div>
    </div>
    """, unsafe_allow_html=True)

# Call Number Section
st.markdown("---")
st.markdown("### 🎲 Number Calling")

all_called = len(st.session_state.called_numbers) >= 75

# Control buttons - Mobile friendly grid
control_col1, control_col2 = st.columns(2)

with control_col1:
    if not st.session_state.is_auto_calling and not all_called:
        if st.button("▶️ Start Auto", use_container_width=True, type="primary"):
            st.session_state.is_auto_calling = True
            st.session_state.last_call_time = time.time()
            available = [i for i in range(1, 76) if i not in st.session_state.called_numbers]
            if available:
                called_num = random.choice(available)
                st.session_state.called_numbers.add(called_num)
                st.session_state.last_called_number = called_num
                st.session_state.auto_called_count += 1
                st.session_state.last_call_time = time.time()
            st.rerun()
    else:
        st.button("⏹️ Stop", use_container_width=True, disabled=True)

with control_col2:
    if st.session_state.is_auto_calling:
        if st.button("⏹️ Stop", use_container_width=True):
            st.session_state.is_auto_calling = False
            st.rerun()
    elif not all_called:
        if st.button("🎯 Call One", use_container_width=True):
            available = [i for i in range(1, 76) if i not in st.session_state.called_numbers]
            if available:
                called_num = random.choice(available)
                st.session_state.called_numbers.add(called_num)
                st.session_state.last_called_number = called_num
                st.session_state.auto_called_count += 1
            st.rerun()
    else:
        st.button("🔄 Reset", use_container_width=True)

# Reset button
if st.button("🔄 Reset Game", use_container_width=True):
    st.session_state.called_numbers = set()
    st.session_state.clicked_numbers = set()
    st.session_state.selected_card = None
    st.session_state.last_called_number = None
    st.session_state.is_auto_calling = False
    st.session_state.auto_called_count = 0
    st.session_state.last_call_time = time.time()
    st.rerun()

# Status display
if st.session_state.is_auto_calling:
    time_since_last = time.time() - st.session_state.last_call_time
    time_until_next = max(0, 3.0 - time_since_last)
    
    st.info(f"⏳ Auto-calling... ({len(st.session_state.called_numbers)}/75)")
    progress = len(st.session_state.called_numbers) / 75
    st.progress(progress)
    
    countdown_percent = (time_since_last / 3.0) * 100
    st.caption(f"⏱️ Next call in: {time_until_next:.1f}s")
    
    st.markdown(f"""
    <div style="width:100%; background:#e0e0e0; border-radius:8px; height:8px; margin-top:5px;">
        <div style="width:{min(countdown_percent, 100)}%; background:linear-gradient(90deg,#FF9800,#F57C00); border-radius:8px; height:8px; transition: width 0.1s;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    import time as timer
    timer.sleep(0.5)
    st.rerun()
    
elif all_called:
    st.success("🎉 All 75 numbers have been called!")
    st.progress(1.0)
elif st.session_state.last_called_number:
    st.success(f"✅ Last called: **{st.session_state.last_called_number}**")
    progress = len(st.session_state.called_numbers) / 75
    st.progress(progress)

# Cards selection section
st.markdown("---")
st.markdown("## Select Cards (1 - 201)")

# Numbers in a grid - Mobile optimized
cols = st.columns(8)  # 8 columns for better mobile fit
for i in range(1, 202):
    col_idx = (i - 1) % 8
    with cols[col_idx]:
        is_clicked = i in st.session_state.clicked_numbers
        
        # Smaller buttons for mobile
        if st.button(
            str(i),
            key=f"num_{i}",
            use_container_width=True,
            type="secondary" if is_clicked else "primary"
        ):
            if i in st.session_state.clicked_numbers:
                st.session_state.clicked_numbers.remove(i)
                st.session_state.selected_card = None
            else:
                st.session_state.clicked_numbers.add(i)
                st.session_state.selected_card = i
            st.rerun()

# Enhanced Footer
st.markdown(f"""
<div class="footer-stats">
    🎯 {len(st.session_state.called_numbers)}/75 Called | 
    📌 {len(st.session_state.clicked_numbers)} Selected
    {' | ⏳ Auto' if st.session_state.is_auto_calling else ''}
</div>
""", unsafe_allow_html=True)
