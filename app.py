import streamlit as st

st.set_page_config(
    page_title="ደራሽ ቢንጎ",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for green bingo theme
st.markdown("""
<style>
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1a472a, #2d6a4f);
        border-radius: 10px;
        margin-bottom: 20px;
        color: white;
    }
    .header h1 {
        color: #ffd700;
        margin: 0;
        font-size: 2.5em;
    }
    .header p {
        color: #a8d5ba;
        margin: 5px 0 0 0;
        font-size: 1.2em;
    }
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
    .footer {
        text-align: center;
        color: #2d6a4f;
        padding: 20px;
        margin-top: 20px;
        border-top: 2px solid #2d6a4f;
        font-weight: bold;
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

# Header
st.markdown("""
<div class="header">
    <h1>🎯 ደራሽ ቢንጎ</h1>
    <p>Cards 1 - 201</p>
</div>
""", unsafe_allow_html=True)

# Create grid of numbered boxes
st.markdown('<div class="bingo-grid">', unsafe_allow_html=True)

for i in range(1, 202):
    st.markdown(f'<div class="number-box">{i}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Total: 201 Cards | ደራሽ ቢንጎ
</div>
""", unsafe_allow_html=True)
