import streamlit as st

st.set_page_config(
    page_title="ደራሽ ቢንጎ",
    page_icon="🎯",
    layout="wide"
)

st.markdown("# Fork")
st.markdown("## Cards 1 - 201")

# Numbers in a grid
cols = st.columns(10)
for i in range(1, 202):
    col_idx = (i - 1) % 10
    with cols[col_idx]:
        st.markdown(f"""
        <div style="
            border: 2px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            text-align: center;
            margin: 2px;
            font-weight: bold;
        ">
            {i}
        </div>
        """, unsafe_allow_html=True)
