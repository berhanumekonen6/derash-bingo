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
            max-width: 950px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .bingo-table {
            width: 100%;
            border-collapse: collapse;
        }
        .bingo-table td {
            border: 1px solid #333;
            padding: 6px 4px;
            text-align: center;
            min-width: 35px;
        }
        .bingo-table .circle {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            border-radius: 50%;
            font-size: 0.9rem;
            font-weight: bold;
            font-family: Arial, sans-serif;
            background: #FAFAFA;
            color: #1A237E;
            border: 2px solid #2E7D32;
        }
        .bingo-table .row-label .circle {
            width: 45px;
            height: 45px;
            font-size: 1.3rem;
            background: #2E7D32;
            color: white;
            border: 2px solid #1B5E20;
            font-weight: 900;
        }
        .bingo-table td:not(.row-label) .circle:hover {
            transform: scale(1.05);
            box-shadow: 0 2px 8px rgba(46, 125, 50, 0.2);
        }
        @media (max-width: 600px) {
            .bingo-table td {
                padding: 3px 2px;
                min-width: 22px;
            }
            .bingo-table .circle {
                width: 26px;
                height: 26px;
                font-size: 0.65rem;
                border-width: 1.5px;
            }
            .bingo-table .row-label .circle {
                width: 30px;
                height: 30px;
                font-size: 0.9rem;
            }
        }
        @media (max-width: 400px) {
            .bingo-table .circle {
                width: 20px;
                height: 20px;
                font-size: 0.5rem;
                border-width: 1px;
            }
            .bingo-table .row-label .circle {
                width: 24px;
                height: 24px;
                font-size: 0.7rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    html = '<div class="bingo-container">'
    html += '<table class="bingo-table">'
    
    for letter in ['B', 'I', 'N', 'G', 'O']:
        html += '<tr>'
        html += f'<td class="row-label"><div class="circle">{letter}</div></td>'
        for num in board[letter]:
            html += f'<td><div class="circle">{num}</div></td>'
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
