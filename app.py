import streamlit as st

st.set_page_config(
    page_title="BINGO Board",
    page_icon="🎯",
    layout="centered"
)

def create_bingo_board():
    board = {
        'B': list(range(1, 16)),
        'I': list(range(16, 31)),
        'N': list(range(31, 46)),
        'G': list(range(46, 61)),
        'O': list(range(61, 76))
    }
    return board

def display_bingo_board(board):
    st.markdown("""
    <style>
        .bingo-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .bingo-table {
            width: 100%;
            border-collapse: collapse;
            font-family: monospace;
        }
        .bingo-table td {
            border: 1px solid #333;
            padding: 8px 6px;
            text-align: center;
            font-size: 0.95rem;
            font-weight: bold;
            min-width: 35px;
        }
        .bingo-table .row-label {
            background: #2E7D32;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
            min-width: 50px;
        }
        .bingo-table .header {
            background: #2E7D32;
            color: white;
            font-weight: bold;
            font-size: 0.9rem;
        }
        .bingo-table td:not(.row-label):not(.header) {
            color: #1A237E;
            background: #FAFAFA;
        }
        @media (max-width: 600px) {
            .bingo-table td {
                padding: 4px 2px;
                font-size: 0.7rem;
                min-width: 20px;
            }
            .bingo-table .row-label {
                font-size: 1rem;
                min-width: 30px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    html = '<div class="bingo-container">'
    html += '<table class="bingo-table">'
    
    # Header row
    html += '<tr>'
    html += '<td class="header">#</td>'
    for num in range(1, 16):
        html += f'<td class="header">{num}</td>'
    html += '</tr>'
    
    # Data rows
    for letter in ['B', 'I', 'N', 'G', 'O']:
        html += '<tr>'
        html += f'<td class="row-label">{letter}</td>'
        for num in board[letter]:
            html += f'<td>{num}</td>'
        html += '</tr>'
    
    html += '</table>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# Initialize
if 'board' not in st.session_state:
    st.session_state.board = create_bingo_board()

# Display
st.title("🎯 BINGO Board")
display_bingo_board(st.session_state.board)
