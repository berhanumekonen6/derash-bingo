import streamlit as st

st.set_page_config(
    page_title="ደራሽ ቢንጎ",
    page_icon="🎯",
    layout="wide"
)

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

# Exactly as in your image - "Fork" header
st.markdown("# Fork")
st.markdown("## Cards 1 - 201")

# Create grid of numbered boxes
st.markdown('<div class="bingo-grid">', unsafe_allow_html=True)

for i in range(1, 202):
    st.markdown(f'<div class="number-box">{i}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
