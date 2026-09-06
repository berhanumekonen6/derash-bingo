import streamlit as st
import random
import time

st.set_page_config(
    page_title="ደራሽ ቢንጎ",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state for clicked numbers
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
if 'last_update_time' not in st.session_state:
    st.session_state.last_update_time = time.time()
if 'next_call_time' not in st.session_state:
    st.session_state.next_call_time = time.time() + 3.0
if 'call_interval' not in st.session_state:
    st.session_state.call_interval = 3.0
if 'last_auto_call_time' not in st.session_state:
    st.session_state.last_auto_call_time = time.time()

# ===================================================================
# ALL 201 BINGO CARDS - FULL LIST (shortened for brevity - keep your full list)
# ===================================================================

BINGO_CARDS = [
    {"id": 1, "cells": [['15', '16', '39', '59', '66'], ['11', '28', '40', '51', '68'], ['12', '20', 'F', '56', '67'], ['3', '30', '35', '60', '72'], ['10', '24', '37', '53', '64']]},
    {"id": 2, "cells": [['5', '21', '35', '46', '69'], ['15', '20', '42', '51', '70'], ['10', '28', 'F', '47', '67'], ['2', '26', '31', '49', '64'], ['6', '27', '33', '52', '65']]},
    # ... (keep all your BINGO_CARDS here)
]

def get_card(card_id):
    for card in BINGO_CARDS:
        if card["id"] == card_id:
            return card
    return None

def call_random_number():
    """Call a random number from 1-75 that hasn't been called yet"""
    available = [i for i in range(1, 76) if i not in st.session_state.called_numbers]
    if available:
        called_num = random.choice(available)
        st.session_state.called_numbers.add(called_num)
        st.session_state.last_called_number = called_num
        st.session_state.auto_called_count += 1
        st.session_state.last_auto_call_time = time.time()
        return True
    return False

def display_bingo_card(card_id):
    """Display a BINGO card with called numbers highlighted"""
    card = get_card(card_id)
    if not card:
        return
    
    cells = card["cells"]
    
    st.markdown(f"""
    <style>
        .bingo-card-wrapper {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin: 20px auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            max-width: 500px;
            border: 2px solid #2E7D32;
        }}
        .bingo-card-title {{
            text-align: center;
            color: #1B5E20;
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .bingo-table {{
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
        }}
        .bingo-table th {{
            background: #2E7D32;
            color: white;
            padding: 8px 6px;
            font-size: 0.9rem;
            font-weight: bold;
            text-align: center;
            border: 1px solid #1B5E20;
        }}
        .bingo-table td {{
            border: 1px solid #333;
            padding: 8px 4px;
            text-align: center;
            font-size: 0.9rem;
            font-weight: bold;
            min-width: 40px;
            height: 40px;
        }}
        .bingo-table .row-label {{
            background: #2E7D32 !important;
            color: white !important;
            font-weight: bold;
            font-size: 0.8rem;
            min-width: 30px;
        }}
        .bingo-table .free-space {{
            background: #FFEB3B;
            color: #E53935;
            font-size: 1.5rem;
        }}
        .bingo-table .number-cell {{
            color: #1A237E;
        }}
        .bingo-table .called-number {{
            background: #FF9800 !important;
            color: white !important;
            border-radius: 4px;
        }}
        .bingo-table .ticked-number {{
            background: #4CAF50 !important;
            color: white !important;
            border-radius: 4px;
        }}
        .bingo-footer {{
            text-align: center;
            color: #333;
            font-size: 0.8rem;
            font-weight: bold;
            margin-top: 8px;
            letter-spacing: 2px;
            font-family: Arial, sans-serif;
        }}
        @media (max-width: 600px) {{
            .bingo-table td {{
                padding: 4px 2px;
                font-size: 0.8rem;
                min-width: 30px;
                height: 30px;
            }}
            .bingo-table th {{
                padding: 4px 2px;
                font-size: 0.8rem;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Card wrapper
    html = f'<div class="bingo-card-wrapper">'
    html += f'<div class="bingo-card-title">Card #{card_id}</div>'
    
    # Table
    html += '<table class="bingo-table">'
    html += '<thead><tr>'
    html += '<th style="background:#2E7D32;color:white;border:1px solid #1B5E20;"></th>'
    for col in ['B', 'I', 'N', 'G', 'O']:
        html += f'<th style="background:#2E7D32;color:white;border:1px solid #1B5E20;">{col}</th>'
    html += '</tr></thead><tbody>'
    
    # Row labels - B, I, N, G, O
    row_labels = ['B', 'I', 'N', 'G', 'O']
    
    for row_idx in range(5):
        html += '<tr>'
        html += f'<td class="row-label" style="background:#2E7D32;color:white;font-weight:bold;text-align:center;border:1px solid #1B5E20;padding:8px 6px;">{row_labels[row_idx]}</td>'
        
        for col_idx in range(5):
            value = cells[row_idx][col_idx]
            
            if value == 'F':
                html += '<td class="free-space">★</td>'
            else:
                # Check if this number has been called
                num = int(value)
                is_called = num in st.session_state.called_numbers
                # Check if this number is on the selected card (ticked)
                is_ticked = num in st.session_state.clicked_numbers
                
                if is_ticked and is_called:
                    html += f'<td class="number-cell ticked-number">{value}</td>'
                elif is_called:
                    html += f'<td class="number-cell called-number">{value}</td>'
                else:
                    html += f'<td class="number-cell">{value}</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    html += '<div class="bingo-footer"></div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

def display_master_board():
    """Display the BINGO board with all letters and numbers in circles"""
    st.markdown("""
    <style>
        .master-board-container {
            max-width: 950px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .master-board-title {
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            color: #1B5E20;
            margin-bottom: 15px;
        }
        .master-table {
            width: 100%;
            border-collapse: collapse;
        }
        .master-table td {
            border: 1px solid #333;
            padding: 8px 6px;
            text-align: center;
            font-size: 0.95rem;
            font-weight: bold;
            min-width: 35px;
        }
        .master-table .row-label {
            background: #2E7D32;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
            min-width: 50px;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: auto;
        }
        .circle-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            background: #E8F5E9;
            color: #1A237E;
            font-weight: bold;
            font-size: 0.9rem;
            border: 2px solid #2E7D32;
            transition: all 0.3s ease;
        }
        .circle-number.called {
            background: #FF9800;
            color: white;
            border-color: #E65100;
            transform: scale(1.1);
        }
        .circle-number.last-called {
            background: #E53935;
            color: white;
            border-color: #B71C1C;
            transform: scale(1.2);
            animation: pulse 0.5s ease-in-out;
            box-shadow: 0 0 20px rgba(229, 57, 53, 0.5);
        }
        .circle-letter {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: #2E7D32;
            color: white;
            font-weight: bold;
            font-size: 1.5rem;
            border: 3px solid #1B5E20;
            margin: auto;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.3); }
            100% { transform: scale(1); }
        }
        @media (max-width: 600px) {
            .master-table td {
                padding: 4px 2px;
                font-size: 0.7rem;
                min-width: 20px;
            }
            .circle-number {
                width: 28px;
                height: 28px;
                font-size: 0.7rem;
            }
            .circle-letter {
                width: 35px;
                height: 35px;
                font-size: 1rem;
            }
            .master-table .row-label {
                width: 35px;
                height: 35px;
                font-size: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create master board data
    master_board = {
        'B': list(range(1, 16)),
        'I': list(range(16, 31)),
        'N': list(range(31, 46)),
        'G': list(range(46, 61)),
        'O': list(range(61, 76))
    }
    
    html = '<div class="master-board-container">'
    html += '<div class="master-board-title">🎯 BINGO Board</div>'
    
    # Show last called number if exists
    if st.session_state.last_called_number:
        html += f'<div style="text-align:center;font-size:1.5rem;font-weight:bold;color:#E53935;margin-bottom:10px;">🎯 Last Called: <span style="background:#E53935;color:white;padding:5px 15px;border-radius:20px;display:inline-block;">{st.session_state.last_called_number}</span></div>'
    
    html += '<table class="master-table">'
    
    for letter in ['B', 'I', 'N', 'G', 'O']:
        html += '<tr>'
        html += f'<td><div class="circle-letter">{letter}</div></td>'
        for num in master_board[letter]:
            is_called = num in st.session_state.called_numbers
            is_last = num == st.session_state.last_called_number
            
            if is_last:
                html += f'<td><div class="circle-number last-called">{num}</div></td>'
            elif is_called:
                html += f'<td><div class="circle-number called">{num}</div></td>'
            else:
                html += f'<td><div class="circle-number">{num}</div></td>'
        html += '</tr>'
    
    html += '</table>'
    
    # Show count of called numbers
    html += f'<div style="text-align:center;margin-top:15px;font-size:1rem;color:#333;padding:10px;background:#F5F5F5;border-radius:8px;">📊 Called: <strong>{len(st.session_state.called_numbers)}</strong> / 75 numbers</div>'
    
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ===================================================================
# MAIN APP
# ===================================================================

# Auto-call logic - runs continuously when enabled
if st.session_state.is_auto_calling:
    # Check if all numbers have been called
    if len(st.session_state.called_numbers) >= 75:
        st.session_state.is_auto_calling = False
        st.success("🎉 All numbers have been called! Auto-call stopped.")
    else:
        # Check if 3 seconds have passed since the last call
        current_time = time.time()
        if current_time - st.session_state.last_auto_call_time >= 3.0:
            # Call a number
            if call_random_number():
                # Update the time
                st.session_state.last_auto_call_time = current_time
                # Force a rerun to update the display
                st.rerun()
        else:
            # Still waiting for the next call - refresh to update the countdown
            time.sleep(0.1)
            st.rerun()

# Display Master Board at top
display_master_board()

# Call Number Section
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### 🎲 Number Calling")
    
    # Check if all numbers are called
    all_called = len(st.session_state.called_numbers) >= 75
    
    # Control buttons
    control_col1, control_col2, control_col3, control_col4 = st.columns(4)
    
    with control_col1:
        if not st.session_state.is_auto_calling and not all_called:
            if st.button("▶️ Start Auto-Call", use_container_width=True, type="primary"):
                st.session_state.is_auto_calling = True
                st.session_state.last_auto_call_time = time.time()
                # Call first number immediately
                call_random_number()
                st.rerun()
    
    with control_col2:
        if st.session_state.is_auto_calling:
            if st.button("⏹️ Stop Auto-Call", use_container_width=True):
                st.session_state.is_auto_calling = False
                st.rerun()
    
    with control_col3:
        if not st.session_state.is_auto_calling and not all_called:
            if st.button("🎯 Call One", use_container_width=True):
                call_random_number()
                st.rerun()
    
    with control_col4:
        if st.button("🔄 Reset Game", use_container_width=True):
            st.session_state.called_numbers = set()
            st.session_state.clicked_numbers = set()
            st.session_state.selected_card = None
            st.session_state.last_called_number = None
            st.session_state.is_auto_calling = False
            st.session_state.auto_called_count = 0
            st.session_state.last_auto_call_time = time.time()
            st.rerun()
    
    # Status display
    if st.session_state.is_auto_calling:
        # Calculate time until next call
        time_since_last = time.time() - st.session_state.last_auto_call_time
        time_until_next = max(0, 3.0 - time_since_last)
        
        st.info(f"⏳ Auto-calling in progress... ({len(st.session_state.called_numbers)}/75 called)")
        progress = len(st.session_state.called_numbers) / 75
        st.progress(progress)
        st.caption(f"⏱️ Next call in: {time_until_next:.1f} seconds")
        
        # Auto-refresh the page to update the countdown
        if time_until_next > 0:
            st.empty()
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
        # Check if number is clicked
        is_clicked = i in st.session_state.clicked_numbers
        
        # Create clickable button
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

# Footer with stats
st.markdown(f"""
<div style="text-align: center; color: #2d6a4f; padding: 20px; margin-top: 20px; border-top: 2px solid #2d6a4f;">
    Total: 201 Cards | Selected: {len(st.session_state.clicked_numbers)} cards | Called: {len(st.session_state.called_numbers)}/75 numbers
    {' | ⏳ Auto-calling active' if st.session_state.is_auto_calling else ''}
</div>
""", unsafe_allow_html=True)

# Display selected card
if st.session_state.selected_card:
    st.markdown("---")
    st.markdown("### 📋 Selected Card")
    display_bingo_card(st.session_state.selected_card)
