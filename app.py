import streamlit as st

st.set_page_config(
    page_title="BINGO Board - Vertical",
    page_icon="🎯",
    layout="centered"
)

def create_bingo_board():
    """Create BINGO board with vertical rows (B, I, N, G, O)"""
    board = {
        'B': list(range(1, 16)),      # 1-15
        'I': list(range(16, 31)),     # 16-30
        'N': list(range(31, 46)),     # 31-45
        'G': list(range(46, 61)),     # 46-60
        'O': list(range(61, 76))      # 61-75
    }
    return board

def display_bingo_board(board, called_numbers=None):
    """Display BINGO board with vertical rows (B, I, N, G, O)"""
    
    if called_numbers is None:
        called_numbers = set()
    
    st.markdown("""
    <style>
        .bingo-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }
        .bingo-title {
            text-align: center;
            font-size: 2rem;
            font-weight: 900;
            letter-spacing: 10px;
            color: #1B5E20;
            margin-bottom: 20px;
            font-family: 'Arial Black', sans-serif;
        }
        .bingo-table {
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
        }
        .bingo-table th {
            background: #2E7D32;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
            padding: 10px;
            border: 2px solid #1B5E20;
            text-align: center;
            width: 20%;
        }
        .bingo-table td {
            border: 2px solid #1B5E20;
            padding: 6px 4px;
            text-align: center;
            font-size: 0.9rem;
            font-weight: bold;
            background: #F5F5F5;
            min-width: 30px;
        }
        .bingo-table .row-label {
            background: #2E7D32;
            color: white;
            font-size: 1rem;
            font-weight: bold;
            min-width: 40px;
        }
        .bingo-table .called {
            background: #FFD700;
            color: #D32F2F;
            text-decoration: line-through;
        }
        .bingo-table .free {
            background: #FFD700;
            color: #D32F2F;
            font-weight: 900;
            font-size: 0.8rem;
        }
        .bingo-table td:not(.called):not(.free):not(.row-label) {
            color: #1A237E;
        }
        .bingo-footer {
            text-align: center;
            margin-top: 15px;
            font-size: 0.9rem;
            color: #666;
        }
        .stButton button {
            background: #2E7D32 !important;
            color: white !important;
            font-weight: bold !important;
        }
        .stButton button:hover {
            background: #1B5E20 !important;
            transform: scale(1.02);
        }
        @media (max-width: 600px) {
            .bingo-table td {
                padding: 4px 2px;
                font-size: 0.7rem;
                min-width: 20px;
            }
            .bingo-table th {
                font-size: 1.2rem;
                padding: 6px;
            }
            .bingo-table .row-label {
                font-size: 0.8rem;
                min-width: 30px;
            }
            .bingo-title {
                font-size: 1.5rem;
                letter-spacing: 5px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Build HTML table
    html = '<div class="bingo-container">'
    html += '<div class="bingo-title">🎯 BINGO BOARD 🎯</div>'
    html += '<table class="bingo-table">'
    
    # Header row (B, I, N, G, O)
    html += '<thead><tr>'
    html += '<th style="background:#2E7D32;color:white;">#</th>'
    for letter in ['B', 'I', 'N', 'G', 'O']:
        html += f'<th style="background:#2E7D32;color:white;">{letter}</th>'
    html += '</tr></thead>'
    
    # Body rows - each row shows positions 1-15 down
    html += '<tbody>'
    
    # For each number position (1-15)
    for pos in range(15):
        html += '<tr>'
        # Row label (position number 1-15)
        html += f'<td class="row-label" style="background:#2E7D32;color:white;border:2px solid #1B5E20;text-align:center;font-weight:bold;">{pos + 1}</td>'
        
        # B, I, N, G, O columns
        for letter in ['B', 'I', 'N', 'G', 'O']:
            num = board[letter][pos]
            
            # Check if number is called
            is_called = num in called_numbers
            
            # Special: Free space in center of N column (position 8, index 7)
            if letter == 'N' and pos == 7:
                html += '<td class="free">⭐ FREE</td>'
            elif is_called:
                html += f'<td class="called">✅ {num}</td>'
            else:
                html += f'<td>{num}</td>'
        html += '</tr>'
    
    html += '</tbody>'
    html += '</table>'
    html += '<div class="bingo-footer">🎯 Click numbers below to mark them as called 🎯</div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = create_bingo_board()
if 'called_numbers' not in st.session_state:
    st.session_state.called_numbers = set()

# Main UI
st.title("🎲 BINGO Caller")

# Display the board
display_bingo_board(st.session_state.board, st.session_state.called_numbers)

# Controls for marking numbers
st.markdown("---")
st.subheader("📢 Mark Called Numbers")

# Create a grid of numbers 1-75 for marking
cols = st.columns(15)
for i in range(1, 76):
    col_idx = (i - 1) % 15
    with cols[col_idx]:
        is_called = i in st.session_state.called_numbers
        label = f"✅ {i}" if is_called else str(i)
        if st.button(
            label,
            key=f"call_{i}",
            use_container_width=True,
            type="primary" if is_called else "secondary"
        ):
            if i in st.session_state.called_numbers:
                st.session_state.called_numbers.remove(i)
            else:
                st.session_state.called_numbers.add(i)
            st.rerun()

# Stats and Controls
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📞 Called", len(st.session_state.called_numbers))
with col2:
    remaining = 75 - len(st.session_state.called_numbers)
    st.metric("📭 Remaining", remaining)
with col3:
    percentage = (len(st.session_state.called_numbers) / 75) * 100
    st.metric("📊 Progress", f"{percentage:.1f}%")
with col4:
    if st.button("🗑️ Reset All", use_container_width=True):
        st.session_state.called_numbers = set()
        st.rerun()

# Quick call buttons for each letter range
st.markdown("---")
st.subheader("⚡ Quick Call by Range")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("B (1-15)", use_container_width=True):
        for num in range(1, 16):
            if num not in st.session_state.called_numbers:
                st.session_state.called_numbers.add(num)
        st.rerun()

with col2:
    if st.button("I (16-30)", use_container_width=True):
        for num in range(16, 31):
            if num not in st.session_state.called_numbers:
                st.session_state.called_numbers.add(num)
        st.rerun()

with col3:
    if st.button("N (31-45)", use_container_width=True):
        for num in range(31, 46):
            if num not in st.session_state.called_numbers:
                st.session_state.called_numbers.add(num)
        st.rerun()

with col4:
    if st.button("G (46-60)", use_container_width=True):
        for num in range(46, 61):
            if num not in st.session_state.called_numbers:
                st.session_state.called_numbers.add(num)
        st.rerun()

with col5:
    if st.button("O (61-75)", use_container_width=True):
        for num in range(61, 76):
            if num not in st.session_state.called_numbers:
                st.session_state.called_numbers.add(num)
        st.rerun()

# Footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px; margin-top: 20px; border-top: 1px solid #ddd;">
    <p>🎯 BINGO Board</p>
    <p style="font-size: 0.8rem;">B: 1-15 • I: 16-30 • N: 31-45 • G: 46-60 • O: 61-75</p>
</div>
""", unsafe_allow_html=True)
