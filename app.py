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
            else:
                st.session_state.clicked_numbers.add(i)
            st.rerun()
