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
# ENHANCED CSS STYLES
# ===================================================================

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    /* Global styles */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* BINGO Board Container */
    .master-board-container {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 20px;
        padding: 25px;
        margin: 20px auto;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3), 0 5px 15px rgba(0,0,0,0.1);
        border: 3px solid #2E7D32;
        position: relative;
        overflow: hidden;
    }
    
    .master-board-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(46,125,50,0.05) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .master-board-title {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 900;
        color: #1B5E20;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        letter-spacing: 5px;
        position: relative;
        z-index: 1;
    }
    
    /* Circle Numbers - Enhanced */
    .circle-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(145deg, #E8F5E9, #C8E6C9);
        color: #1A237E;
        font-weight: 900;
        font-size: 0.95rem;
        border: 3px solid #2E7D32;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-family: 'Orbitron', sans-serif;
    }
    
    .circle-number:hover {
        transform: scale(1.15) rotate(5deg);
        box-shadow: 0 4px 15px rgba(46,125,50,0.3);
    }
    
    .circle-number.called {
        background: linear-gradient(145deg, #FF9800, #F57C00);
        color: white;
        border-color: #E65100;
        transform: scale(1.15);
        animation: pop 0.3s ease-out;
        box-shadow: 0 0 25px rgba(255,152,0,0.6);
    }
    
    .circle-number.last-called {
        background: linear-gradient(145deg, #E53935, #C62828);
        color: white;
        border-color: #B71C1C;
        transform: scale(1.25);
        animation: pulse-glow 1s ease-in-out infinite;
        box-shadow: 0 0 40px rgba(229,57,53,0.7);
    }
    
    @keyframes pop {
        0% { transform: scale(0.5); opacity: 0; }
        50% { transform: scale(1.3); }
        100% { transform: scale(1.15); opacity: 1; }
    }
    
    @keyframes pulse-glow {
        0%, 100% { 
            transform: scale(1.25);
            box-shadow: 0 0 40px rgba(229,57,53,0.7);
        }
        50% { 
            transform: scale(1.35);
            box-shadow: 0 0 60px rgba(229,57,53,0.9);
        }
    }
    
    .circle-letter {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 55px;
        height: 55px;
        border-radius: 50%;
        background: linear-gradient(145deg, #2E7D32, #1B5E20);
        color: white;
        font-weight: 900;
        font-size: 1.8rem;
        border: 4px solid #F9A825;
        margin: auto;
        font-family: 'Orbitron', sans-serif;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        transition: transform 0.3s;
    }
    
    .circle-letter:hover {
        transform: rotate(10deg) scale(1.05);
    }
    
    /* Selected Card - Enhanced */
    .selected-card-container {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 20px;
        padding: 20px;
        margin: 10px auto;
        box-shadow: 0 15px 35px rgba(0,0,0,0.25);
        max-width: 400px;
        border: 3px solid #2E7D32;
        position: relative;
        transition: all 0.3s;
    }
    
    .selected-card-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 45px rgba(0,0,0,0.3);
    }
    
    .selected-card-title {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        color: #1B5E20;
        font-size: 1.3rem;
        font-weight: 900;
        margin-bottom: 15px;
        letter-spacing: 2px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .selected-circle {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: linear-gradient(145deg, #E8F5E9, #C8E6C9);
        color: #1A237E;
        font-weight: 900;
        font-size: 1rem;
        border: 3px solid #2E7D32;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        font-family: 'Orbitron', sans-serif;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .selected-circle.called {
        background: linear-gradient(145deg, #FF9800, #F57C00);
        color: white;
        border-color: #E65100;
        transform: scale(1.15);
        box-shadow: 0 0 25px rgba(255,152,0,0.4);
        animation: pop 0.3s ease-out;
    }
    
    .selected-circle.ticked {
        background: linear-gradient(145deg, #4CAF50, #388E3C);
        color: white;
        border-color: #1B5E20;
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(76,175,80,0.3);
    }
    
    .selected-circle.ticked-and-called {
        background: linear-gradient(145deg, #4CAF50, #388E3C);
        color: white;
        border-color: #E65100;
        transform: scale(1.2);
        box-shadow: 0 0 30px rgba(76,175,80,0.5), inset 0 0 20px rgba(255,152,0,0.3);
        animation: pulse-glow-green 1s ease-in-out infinite;
    }
    
    @keyframes pulse-glow-green {
        0%, 100% { 
            transform: scale(1.2);
            box-shadow: 0 0 30px rgba(76,175,80,0.5);
        }
        50% { 
            transform: scale(1.25);
            box-shadow: 0 0 45px rgba(76,175,80,0.7);
        }
    }
    
    .selected-circle.free {
        background: linear-gradient(145deg, #FFEB3B, #FDD835);
        color: #E53935;
        font-size: 1.5rem;
        border-color: #F57F17;
        animation: blink-star 1s ease-in-out infinite;
    }
    
    @keyframes blink-star {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }
    
    /* Buttons - Enhanced */
    .stButton > button {
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        border-radius: 12px !important;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.95);
    }
    
    /* Number Cards - Grid Enhancement */
    .stButton > button[data-testid="baseButton-secondary"] {
        background: linear-gradient(145deg, #e8f5e9, #c8e6c9) !important;
        border: 2px solid #2E7D32 !important;
        color: #1A237E !important;
        font-weight: 700 !important;
    }
    
    .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(145deg, #FF9800, #F57C00) !important;
        border: 2px solid #E65100 !important;
        color: white !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(255,152,0,0.3) !important;
    }
    
    /* Info Box */
    .stAlert {
        border-radius: 15px !important;
        border-left: 5px solid #2E7D32 !important;
        font-weight: 500 !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #2E7D32, #4CAF50, #8BC34A) !important;
        border-radius: 10px !important;
        height: 8px !important;
    }
    
    /* Footer */
    .footer-stats {
        background: linear-gradient(145deg, #1B5E20, #2E7D32);
        color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 2px solid #F9A825;
    }
    
    /* Responsive */
    @media (max-width: 600px) {
        .circle-number {
            width: 30px;
            height: 30px;
            font-size: 0.7rem;
        }
        .circle-letter {
            width: 40px;
            height: 40px;
            font-size: 1.2rem;
        }
        .selected-circle {
            width: 35px;
            height: 35px;
            font-size: 0.8rem;
        }
        .master-board-title {
            font-size: 1.8rem;
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
    # ... (add all other cards here, same as before)
]

# For brevity, I'm including just the first two cards here
# You would include all 201 cards from your original code

def get_card(card_id):
    for card in BINGO_CARDS:
        if card["id"] == card_id:
            return card
    return None

def display_selected_card(card_id):
    """Display a BINGO card with enhanced styling"""
    card = get_card(card_id)
    if not card:
        return
    
    cells = card["cells"]
    
    html = f'<div class="selected-card-container">'
    html += f'<div class="selected-card-title">🎯 Card #{card_id}</div>'
    
    html += '<table style="width:100%;border-collapse:collapse;margin:0 auto;">'
    html += '<tr style="text-align:center;">'
    for label in ['B', 'I', 'N', 'G', 'O']:
        html += f'<td style="padding:5px;font-family:Orbitron,sans-serif;font-weight:900;color:#1B5E20;font-size:1rem;">{label}</td>'
    html += '</tr>'
    
    for row_idx in range(5):
        html += '<tr style="text-align:center;">'
        for col_idx in range(5):
            value = cells[row_idx][col_idx]
            
            if value == 'F':
                html += f'<td style="padding:4px;"><div class="selected-circle free">★</div></td>'
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
                
                html += f'<td style="padding:4px;"><div class="{circle_class}">{value}</div></td>'
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
    
    html += f'<div style="text-align:center;margin-top:12px;font-family:Orbitron,sans-serif;font-size:0.8rem;color:#333;background:#f5f5f5;padding:8px;border-radius:10px;">✅ {total_called_on_card}/24 called | ⭐ {total_ticked} ticked</div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

def display_master_board():
    """Display the BINGO board with enhanced styling"""
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
        <div style="text-align:center;font-size:1.8rem;font-weight:900;font-family:Orbitron,sans-serif;color:#E53935;margin-bottom:15px;">
            🎯 Last Called: 
            <span style="background:linear-gradient(145deg,#E53935,#C62828);color:white;padding:8px 25px;border-radius:30px;display:inline-block;box-shadow:0 4px 20px rgba(229,57,53,0.4);border:2px solid #F9A825;">
                {st.session_state.last_called_number}
            </span>
        </div>
        '''
    
    html += '<table style="width:100%;border-collapse:collapse;position:relative;z-index:1;">'
    
    for letter in ['B', 'I', 'N', 'G', 'O']:
        html += '<tr>'
        html += f'<td style="padding:4px;text-align:center;"><div class="circle-letter">{letter}</div></td>'
        for num in master_board[letter]:
            is_called = num in st.session_state.called_numbers
            is_last = num == st.session_state.last_called_number
            
            circle_class = "circle-number"
            if is_last:
                circle_class += " last-called"
            elif is_called:
                circle_class += " called"
            
            html += f'<td style="padding:4px;text-align:center;"><div class="{circle_class}">{num}</div></td>'
        html += '</tr>'
    
    html += '</table>'
    
    # Stats
    html += f'''
    <div style="text-align:center;margin-top:20px;font-family:Orbitron,sans-serif;font-size:1.1rem;color:#333;padding:12px;background:linear-gradient(145deg,#f5f5f5,#e8e8e8);border-radius:12px;position:relative;z-index:1;">
        📊 Called: <strong style="color:#2E7D32;font-size:1.3rem;">{len(st.session_state.called_numbers)}</strong> / 75 numbers
        <div style="margin-top:5px;font-size:0.8rem;color:#666;">
            {f"{len(st.session_state.called_numbers)/75*100:.1f}% complete" if len(st.session_state.called_numbers) > 0 else "Game not started"}
        </div>
    </div>
    '''
    
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ===================================================================
# MAIN APP - Enhanced Layout
# ===================================================================

# Header with animated title
st.markdown("""
<div style="text-align:center;padding:20px;margin-bottom:20px;">
    <h1 style="font-family:'Orbitron',sans-serif;font-weight:900;font-size:3rem;color:#1B5E20;text-shadow:3px 3px 6px rgba(0,0,0,0.1);letter-spacing:8px;">
        🎯 ደራሽ ቢንጎ
    </h1>
    <p style="font-family:'Orbitron',sans-serif;color:#555;font-weight:400;letter-spacing:2px;">
        Derash BINGO - 201 Cards
    </p>
</div>
""", unsafe_allow_html=True)

# Create two columns for BINGO Board and Selected Card
board_col, card_col = st.columns([2, 1])

with board_col:
    display_master_board()

with card_col:
    if st.session_state.selected_card:
        display_selected_card(st.session_state.selected_card)
    else:
        st.markdown("""
        <div style="background:linear-gradient(145deg,#f8f9fa,#e8e8e8);border-radius:20px;padding:40px 20px;text-align:center;border:3px dashed #2E7D32;margin:10px 0;">
            <div style="font-size:3rem;margin-bottom:10px;">👆</div>
            <div style="font-family:'Orbitron',sans-serif;font-weight:700;color:#555;font-size:1rem;">
                Click a card number below to select it
            </div>
        </div>
        """, unsafe_allow_html=True)

# Call Number Section
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### 🎲 Number Calling")
    
    all_called = len(st.session_state.called_numbers) >= 75
    
    control_col1, control_col2, control_col3, control_col4 = st.columns(4)
    
    with control_col1:
        if not st.session_state.is_auto_calling and not all_called:
            if st.button("▶️ Start Auto-Call", use_container_width=True, type="primary"):
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
    
    with control_col2:
        if st.session_state.is_auto_calling:
            if st.button("⏹️ Stop Auto-Call", use_container_width=True):
                st.session_state.is_auto_calling = False
                st.rerun()
    
    with control_col3:
        if not st.session_state.is_auto_calling and not all_called:
            if st.button("🎯 Call One", use_container_width=True):
                available = [i for i in range(1, 76) if i not in st.session_state.called_numbers]
                if available:
                    called_num = random.choice(available)
                    st.session_state.called_numbers.add(called_num)
                    st.session_state.last_called_number = called_num
                    st.session_state.auto_called_count += 1
                st.rerun()
    
    with control_col4:
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
        
        st.info(f"⏳ Auto-calling in progress... ({len(st.session_state.called_numbers)}/75 called)")
        progress = len(st.session_state.called_numbers) / 75
        st.progress(progress)
        
        countdown_percent = (time_since_last / 3.0) * 100
        st.caption(f"⏱️ Next call in: {time_until_next:.1f} seconds")
        
        st.markdown(f"""
        <div style="width:100%; background:#e0e0e0; border-radius:10px; height:10px; margin-top:5px;">
            <div style="width:{min(countdown_percent, 100)}%; background:linear-gradient(90deg,#FF9800,#F57C00); border-radius:10px; height:10px; transition: width 0.1s;"></div>
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

# Numbers in a grid
cols = st.columns(10)
for i in range(1, 202):
    col_idx = (i - 1) % 10
    with cols[col_idx]:
        is_clicked = i in st.session_state.clicked_numbers
        
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
    🎯 Total: 201 Cards | 
    📌 Selected: {len(st.session_state.clicked_numbers)} cards | 
    📊 Called: {len(st.session_state.called_numbers)}/75 numbers
    {' | ⏳ Auto-calling active' if st.session_state.is_auto_calling else ''}
</div>
""", unsafe_allow_html=True)
