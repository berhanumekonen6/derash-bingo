import streamlit as st

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

# ===================================================================
# ALL 201 BINGO CARDS - FULL LIST
# ===================================================================

BINGO_CARDS = [
    {"id": 1, "cells": [['15', '16', '39', '59', '66'], ['11', '28', '40', '51', '68'], ['12', '20', 'F', '56', '67'], ['3', '30', '35', '60', '72'], ['10', '24', '37', '53', '64']]},
    {"id": 2, "cells": [['5', '21', '35', '46', '69'], ['15', '20', '42', '51', '70'], ['10', '28', 'F', '47', '67'], ['2', '26', '31', '49', '64'], ['6', '27', '33', '52', '65']]},
    # ... (all your 201 cards here)
    {"id": 201, "cells": [['5', '20', '38', '58', '61'], ['10', '22', '41', '52', '64'], ['2', '19', 'F', '57', '62'], ['12', '23', '36', '51', '63'], ['3', '26', '31', '53', '74']]},
]

def get_card(card_id):
    for card in BINGO_CARDS:
        if card["id"] == card_id:
            return card
    return None

def display_bingo_card(card_id):
    """Display a BINGO card with B, I, N, G, O on both axes"""
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
        .bingo-table .free-space {{
            background: #FFEB3B;
            color: #E53935;
            font-size: 1.5rem;
        }}
        .bingo-table .number-cell {{
            color: #1A237E;
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
                html += f'<td class="number-cell">{value}</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    html += '<div class="bingo-footer"></div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ===================================================================
# DISPLAY BINGO BOARD 1-75
# ===================================================================

def display_bingo_board():
    """Display BINGO board 1-75 with B, I, N, G, O columns"""
    
    st.markdown("""
    <style>
        .bingo-board-container {
            background: linear-gradient(135deg, #0a1a0a, #1a3a1a);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0 20px 0;
            border: 3px solid #2E7D32;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .bingo-board-title {
            text-align: center;
            color: #FFD700;
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 15px;
            letter-spacing: 8px;
            font-family: Arial, sans-serif;
        }
        .bingo-board-grid {
            display: grid;
            grid-template-columns: repeat(15, 1fr);
            gap: 3px;
            max-width: 100%;
            margin: 0 auto;
        }
        .bingo-number {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 4px;
            padding: 6px 0;
            text-align: center;
            font-size: 0.7rem;
            font-weight: 600;
            color: #88ff88;
            transition: all 0.3s;
        }
        .bingo-number:hover {
            transform: scale(1.05);
            background: rgba(46,125,50,0.3);
            border-color: #FFD700;
        }
        .bingo-header-row {
            display: grid;
            grid-template-columns: repeat(15, 1fr);
            gap: 3px;
            max-width: 100%;
            margin: 0 auto 8px auto;
        }
        .bingo-header-letter {
            text-align: center;
            font-size: 1rem;
            font-weight: 900;
            font-family: Arial, sans-serif;
            color: #FFD700;
            letter-spacing: 2px;
        }
        .bingo-board-stats {
            text-align: center;
            color: #88ff88;
            font-size: 0.9rem;
            margin-top: 12px;
            padding: 8px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .bingo-board-stats span {
            color: #FFD700;
            font-weight: bold;
        }
        .bingo-column-label {
            text-align: center;
            color: #FFD700;
            font-size: 0.65rem;
            font-weight: bold;
            margin-top: 2px;
            opacity: 0.7;
        }
        @media (max-width: 768px) {
            .bingo-number {
                padding: 4px 0;
                font-size: 0.55rem;
            }
            .bingo-board-title {
                font-size: 1.2rem;
                letter-spacing: 4px;
            }
            .bingo-header-letter {
                font-size: 0.8rem;
            }
        }
        @media (max-width: 480px) {
            .bingo-number {
                padding: 3px 0;
                font-size: 0.45rem;
            }
            .bingo-board-grid {
                gap: 2px;
            }
            .bingo-header-row {
                gap: 2px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Column ranges
    columns = {
        'B': list(range(1, 16)),
        'I': list(range(16, 31)),
        'N': list(range(31, 46)),
        'G': list(range(46, 61)),
        'O': list(range(61, 76))
    }
    
    html = '<div class="bingo-board-container">'
    html += '<div class="bingo-board-title">🎯 B I N G O</div>'
    
    # Header row with letters
    html += '<div class="bingo-header-row">'
    for col_name in ['B']*3 + ['I']*3 + ['N']*3 + ['G']*3 + ['O']*3:
        html += f'<div class="bingo-header-letter">{col_name}</div>'
    html += '</div>'
    
    # Numbers grid
    html += '<div class="bingo-board-grid">'
    
    for row in range(15):
        for col_name in ['B', 'I', 'N', 'G', 'O']:
            number = columns[col_name][row]
            html += f'<div class="bingo-number">{number}</div>'
    
    html += '</div>'
    
    # Column labels
    html += '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:3px;margin-top:5px;">'
    for col_name in ['B (1-15)', 'I (16-30)', 'N (31-45)', 'G (46-60)', 'O (61-75)']:
        html += f'<div class="bingo-column-label">{col_name}</div>'
    html += '</div>'
    
    html += f'''
    <div class="bingo-board-stats">
        📊 Total: <span>75</span> numbers | 
        B: <span>1-15</span> | 
        I: <span>16-30</span> | 
        N: <span>31-45</span> | 
        G: <span>46-60</span> | 
        O: <span>61-75</span>
    </div>
    '''
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ===================================================================
# MAIN DISPLAY
# ===================================================================

st.markdown("""
<style>
    .header-title {
        text-align: center;
        color: #2E7D32;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 5px;
        font-family: Arial, sans-serif;
    }
    .header-subtitle {
        text-align: center;
        color: #555;
        font-size: 1.2rem;
        margin-bottom: 20px;
        font-family: Arial, sans-serif;
    }
    .bingo-grid {
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        gap: 6px;
        padding: 10px;
        max-width: 1200px;
        margin: 0 auto;
    }
    .number-box {
        background: #2d6a4f;
        border: 2px solid #40916c;
        border-radius: 8px;
        padding: 12px 5px;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        color: white;
        transition: all 0.2s;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .number-box:hover {
        background: #40916c;
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        border-color: #ffd700;
    }
    .number-box.selected {
        background: #ffd700;
        color: #1a1a2e;
        border-color: #ffd700;
    }
    .footer-stats {
        text-align: center;
        color: #2d6a4f;
        padding: 20px;
        margin-top: 20px;
        border-top: 2px solid #2d6a4f;
        font-weight: bold;
        font-family: Arial, sans-serif;
    }
    @media (max-width: 768px) {
        .bingo-grid {
            grid-template-columns: repeat(5, 1fr);
        }
        .number-box {
            font-size: 14px;
            padding: 10px 3px;
        }
        .header-title {
            font-size: 1.8rem;
        }
    }
    @media (max-width: 480px) {
        .bingo-grid {
            grid-template-columns: repeat(4, 1fr);
        }
        .number-box {
            font-size: 12px;
            padding: 8px 2px;
        }
        .header-title {
            font-size: 1.5rem;
        }
        .header-subtitle {
            font-size: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">Fork</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">BINGO Board & Cards 1 - 201</div>', unsafe_allow_html=True)

# Display BINGO Board 1-75
display_bingo_board()

# Divider
st.markdown("---")

# Numbers in a grid (Cards 1-201)
st.markdown('<div class="bingo-grid">', unsafe_allow_html=True)

for i in range(1, 202):
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

st.markdown('</div>', unsafe_allow_html=True)

# Footer with stats
st.markdown(f"""
<div class="footer-stats">
    Total: 201 Cards | Selected: {len(st.session_state.clicked_numbers)} cards
</div>
""", unsafe_allow_html=True)

# Display selected card
if st.session_state.selected_card:
    st.markdown("---")
    display_bingo_card(st.session_state.selected_card)
