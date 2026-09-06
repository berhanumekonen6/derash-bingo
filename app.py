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
# ALL 201 BINGO CARDS - FULL LIST (Copy all from your file)
# ===================================================================

BINGO_CARDS = [
    {"id": 4, "cells": [['1', '19', '41', '49', '72'], ['5', '26', '36', '50', '69'], ['6', '29', 'F', '60', '61'], ['14', '25', '42', '47', '71'], ['2', '24', '45', '54', '65']]},
    # ... Add all other cards here ...
]

def get_card(card_id):
    for card in BINGO_CARDS:
        if card["id"] == card_id:
            return card
    return None

def display_bingo_card(card_id):
    """Display a BINGO card in the exact format shown in the image"""
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
            background: #E8F5E9;
            color: #333;
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
    
    for row_idx in range(5):
        html += '<tr>'
        html += f'<td class="row-label">{row_idx + 1}</td>'
        
        for col_idx in range(5):
            value = cells[row_idx][col_idx]
            
            if value == 'F':
                html += '<td class="free-space">★</td>'
            else:
                html += f'<td class="number-cell">{value}</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    html += '<div class="bingo-footer">ЧСТА ФТС:4</div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

st.markdown("# Fork")
st.markdown("## Cards 1 - 201")

# Numbers in a grid
cols = st.columns(10)
for i in range(1, 202):
    col_idx = (i - 1) % 10
    with cols[col_idx]:
        # Check if number is clicked
        is_clicked = i in st.session_state.clicked_numbers
        bg_color = "#ffd700" if is_clicked else "#2d6a4f"
        text_color = "#1a1a2e" if is_clicked else "white"
        border_color = "#ffd700" if is_clicked else "#2d6a4f"
        
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
    Total: 201 Cards | Selected: {len(st.session_state.clicked_numbers)} cards
</div>
""", unsafe_allow_html=True)

# Display selected card
if st.session_state.selected_card:
    st.markdown("---")
    display_bingo_card(st.session_state.selected_card)
