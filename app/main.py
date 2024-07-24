import streamlit as st
from st_pages import Page, show_pages

# Set the page configuration
st.set_page_config(page_title="Hand Sign Detection App", page_icon="✋")

# Display the navigation sidebar
show_pages(
    [
        #"pages/welcome_page.py"
        Page("app/pages/welcome_page.py", "Welcome", "🏠"),
        #pages/hand_sign_detection_page.py
        Page("app/pages/hand_sign_detection_page.py", "Hand Sign Detection", "✋"),
        # Add a customer reviews page
        Page("app/pages/customer_review_page.py", "Customer Reviews", "💬"),
        Page("app/pages/transcribe_audio_page.py", "Transcribe Audio Page", "🔊")
    ]
)

# Language selection
lang = st.sidebar.selectbox("Select Language / Sélectionnez la langue / Seleccione el idioma", ["English", "Français", "Español"])

if __name__ == "__main__":
    st.session_state["selected_lang"] = lang
    st.query_params = {"page": "welcome_page"}
    # Main app content can go here if any