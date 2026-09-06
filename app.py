def display_bingo_card(card_id):
    """Display a BINGO card with B, I, N, G, O on the left side"""
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
            background: #2E7D32;
            color: white;
            font-weight: bold;
            font-size: 0.9rem;
            min-width: 30px;
            border: 1px solid #1B5E20;
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
    
    # Row labels: B, I, N, G, O instead of 1, 2, 3, 4, 5
    row_labels = ['B', 'I', 'N', 'G', 'O']
    
    for row_idx in range(5):
        html += '<tr>'
        html += f'<td class="row-label">{row_labels[row_idx]}</td>'
        
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
