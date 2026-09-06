import streamlit as st

st.set_page_config(
    page_title="ደራሽ ቢንጎ - Cards 1-201",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for exact image replication
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background: #ffffff;
        min-height: 100vh;
    }
    
    .card-grid {
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        gap: 2px;
        background: #ffffff;
        padding: 10px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
    }
    
    .card-item {
        background: #f8f9fa;
        padding: 6px 4px;
        text-align: center;
        border: 1px solid #dee2e6;
        border-radius: 3px;
        font-weight: 500;
        color: #1a1a2e;
        transition: all 0.2s;
        cursor: pointer;
        font-size: 13px;
    }
    
    .card-item:hover {
        background: #ffd700;
        transform: scale(1.05);
        z-index: 10;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* Special styling for numbers that run together in the image */
    .card-item.merged {
        font-size: 11px;
        letter-spacing: -0.5px;
    }
    
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 10px;
        margin-bottom: 20px;
        color: white;
    }
    
    .header h1 {
        color: #ffd700;
        font-size: 2.2em;
        margin: 0;
    }
    
    .header p {
        color: #aaa;
        margin: 5px 0 0 0;
    }
    
    @media (max-width: 768px) {
        .card-grid {
            grid-template-columns: repeat(5, 1fr);
            font-size: 12px;
        }
        .card-item {
            font-size: 11px;
            padding: 4px 2px;
        }
    }
    
    @media (max-width: 480px) {
        .card-grid {
            grid-template-columns: repeat(3, 1fr);
            font-size: 10px;
        }
        .card-item {
            font-size: 10px;
            padding: 3px 2px;
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

# Create the grid display
st.markdown('<div class="card-grid">', unsafe_allow_html=True)

# Generate numbers 1-201
for i in range(1, 202):
    # Special handling for the merged numbers in the image
    # 101-120 are shown as "101102103...120" in the image
    if 101 <= i <= 120:
        if i == 101:
            # Show the merged string for 101-120
            merged = ''.join(str(x) for x in range(101, 121))
            st.markdown(f'<div class="card-item merged" title="101-120">{merged}</div>', unsafe_allow_html=True)
        # Skip individual numbers 102-120 since they're merged
        if 102 <= i <= 120:
            continue
    # 121-140 are merged
    elif 121 <= i <= 140:
        if i == 121:
            merged = ''.join(str(x) for x in range(121, 141))
            st.markdown(f'<div class="card-item merged" title="121-140">{merged}</div>', unsafe_allow_html=True)
        if 122 <= i <= 140:
            continue
    # 141-160 are merged
    elif 141 <= i <= 160:
        if i == 141:
            merged = ''.join(str(x) for x in range(141, 161))
            st.markdown(f'<div class="card-item merged" title="141-160">{merged}</div>', unsafe_allow_html=True)
        if 142 <= i <= 160:
            continue
    # 161-180 are merged
    elif 161 <= i <= 180:
        if i == 161:
            merged = ''.join(str(x) for x in range(161, 181))
            st.markdown(f'<div class="card-item merged" title="161-180">{merged}</div>', unsafe_allow_html=True)
        if 162 <= i <= 180:
            continue
    # 181-200 are merged
    elif 181 <= i <= 200:
        if i == 181:
            merged = ''.join(str(x) for x in range(181, 201))
            st.markdown(f'<div class="card-item merged" title="181-200">{merged}</div>', unsafe_allow_html=True)
        if 182 <= i <= 200:
            continue
    else:
        # Regular individual numbers
        st.markdown(f'<div class="card-item">{i}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: #888; padding: 20px; margin-top: 20px; border-top: 2px solid #eee;">
    Total: 201 Cards | 1 - 201
</div>
""", unsafe_allow_html=True)
