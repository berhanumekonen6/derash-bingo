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
    {"id": 3, "cells": [['14', '23', '40', '58', '62'], ['13', '25', '32', '46', '65'], ['3', '28', 'F', '50', '63'], ['6', '30', '44', '54', '66'], ['10', '16', '37', '53', '74']]},
    {"id": 4, "cells": [['1', '19', '41', '49', '72'], ['5', '26', '36', '50', '69'], ['6', '29', 'F', '60', '61'], ['14', '25', '42', '47', '71'], ['2', '24', '45', '54', '65']]},
    {"id": 5, "cells": [['2', '16', '43', '47', '70'], ['4', '23', '32', '58', '73'], ['9', '17', 'F', '51', '74'], ['1', '26', '34', '59', '75'], ['14', '20', '31', '57', '72']]},
    {"id": 6, "cells": [['3', '28', '42', '46', '70'], ['15', '18', '36', '53', '64'], ['14', '20', 'F', '55', '67'], ['6', '21', '45', '57', '73'], ['11', '30', '41', '60', '62']]},
    {"id": 7, "cells": [['15', '28', '39', '58', '65'], ['10', '19', '34', '54', '68'], ['3', '17', 'F', '59', '71'], ['9', '16', '45', '51', '66'], ['14', '24', '36', '49', '64']]},
    {"id": 8, "cells": [['7', '20', '32', '47', '61'], ['13', '19', '36', '53', '67'], ['9', '21', 'F', '57', '66'], ['4', '18', '38', '59', '68'], ['2', '27', '45', '51', '69']]},
    {"id": 9, "cells": [['5', '26', '33', '56', '75'], ['2', '18', '39', '54', '62'], ['1', '29', 'F', '58', '72'], ['9', '22', '44', '57', '68'], ['13', '17', '42', '55', '67']]},
    {"id": 10, "cells": [['1', '20', '34', '58', '75'], ['13', '18', '40', '59', '69'], ['6', '27', 'F', '52', '67'], ['7', '23', '37', '48', '70'], ['2', '29', '44', '57', '73']]},
    # ... (add all cards 11-200 from your file)
    {"id": 201, "cells": [['5', '20', '38', '58', '61'], ['10', '22', '41', '52', '64'], ['2', '19', 'F', '57', '62'], ['12', '23', '36', '51', '63'], ['3', '26', '31', '53', '74']]},
]

def get_card(card_id):
    for card in BINGO_CARDS:
        if card["id"] == card_id:
            return card
    return None

def display_bingo_card(card_id):
    """Display a BINGO card EXACTLY like the image format"""
    card = get_card(card_id)
    if not card:
        return
    
    cells = card["cells"]
    
    # EXACT format from the image - simple table with BINGO headers
    st.markdown(f"""
    <style>
        .bingo-card-exact {{
            max-width: 500px;
            margin: 20px auto;
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            border: 2px solid #2E7D32;
        }}
        .bingo-card-exact .card-title {{
            text-align: center;
            font-size: 1.1rem;
            font-weight: bold;
            color: #1B5E20;
            margin-bottom: 10px;
            font-family: Arial, sans-serif;
        }}
        .bingo-card-exact table {{
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
        }}
        .bingo-card-exact th {{
            background: #2E7D32;
            color: white;
            padding: 10px 8px;
            font-size: 1rem;
            font-weight: bold;
            text-align: center;
            border: 2px solid #1B5E20;
            font-family: Arial, sans-serif;
        }}
        .bingo-card-exact td {{
            border: 2px solid #333;
            padding: 10px 6px;
            text-align: center;
            font-size: 1rem;
            font-weight: bold;
            background: white;
            color: #1A237E;
            min-width: 50px;
            height: 42px;
            font-family: Arial, sans-serif;
        }}
        .bingo-card-exact .free-star {{
            background: #FFD700;
            color: #D32F2F;
            font-size: 1.8rem;
            font-weight: bold;
        }}
        .bingo-card-exact .footer-text {{
            text-align: center;
            color: #333;
            font-size: 0.75rem;
            font-weight: bold;
            margin-top: 10px;
            letter-spacing: 2px;
            font-family: Arial, sans-serif;
        }}
        @media (max-width: 600px) {{
            .bingo-card-exact td {{
                padding: 6px 3px;
                font-size: 0.8rem;
                min-width: 35px;
                height: 35px;
            }}
            .bingo-card-exact th {{
                padding: 6px 4px;
                font-size: 0.85rem;
            }}
            .bingo-card-exact .free-star {{
                font-size: 1.3rem;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Build the exact card
    html = f'<div class="bingo-card-exact">'
    html += f'<div class="card-title">Card #{card_id}</div>'
    
    html += '<table>'
    html += '<thead><tr>'
    for col in ['B', 'I', 'N', 'G', 'O']:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    
    for row_idx in range(5):
        html += '<tr>'
        for col_idx in range(5):
            value = cells[row_idx][col_idx]
            if value == 'F':
                html += '<td class="free-star">★</td>'
            else:
                html += f'<td>{value}</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    html += '<div class="footer-text">ЧСТА ФТС:4</div>'
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
st.markdown('<div class="header-subtitle">Cards 1 - 201</div>', unsafe_allow_html=True)

# Numbers in a grid
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
