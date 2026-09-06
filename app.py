import streamlit as st

st.set_page_config(
    page_title="ደራሽ ቢንጎ",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state for clicked numbers
if 'clicked_numbers' not in st.session_state:
    st.session_state.clicked_numbers = set()

st.markdown("# Fork")
st.markdown("## Cards 1 - 201")

# Custom CSS for green bingo theme
st.markdown("""
<style>
    .bingo-grid {
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        gap: 5px;
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
    @media (max-width: 768px) {
        .bingo-grid {
            grid-template-columns: repeat(5, 1fr);
        }
        .number-box {
            font-size: 14px;
            padding: 10px 3px;
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
    }
</style>
""", unsafe_allow_html=True)

# Display all cards 1-201
st.markdown('<div class="bingo-grid">', unsafe_allow_html=True)

for i in range(1, 202):
    # Check if number is clicked
    is_clicked = i in st.session_state.clicked_numbers
    selected_class = "selected" if is_clicked else ""
    
    # Create clickable div with onclick using Streamlit button
    if st.button(
        str(i),
        key=f"card_{i}",
        use_container_width=True,
        type="secondary" if is_clicked else "primary"
    ):
        if i in st.session_state.clicked_numbers:
            st.session_state.clicked_numbers.remove(i)
        else:
            st.session_state.clicked_numbers.add(i)
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer with stats
st.markdown(f"""
<div style="text-align: center; color: #2d6a4f; padding: 20px; margin-top: 20px; border-top: 2px solid #2d6a4f;">
    Total: 201 Cards | Selected: {len(st.session_state.clicked_numbers)} cards
</div>
""", unsafe_allow_html=True)
