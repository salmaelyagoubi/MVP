import streamlit as st
from st_pages import Page, show_pages

# Set the page configuration
st.set_page_config(page_title="Hand Sign Detection App", page_icon="✋")

# Display the navigation sidebar
show_pages(
    [
        Page("pages/welcome_page.py", "Welcome", "🏠"),
        Page("pages/hand_sign_detection_page.py", "Hand Sign Detection", "✋"),
        Page("pages/speech_to_text_translation_page.py", "Speech-to-Text and Translation", "🗣️"),
        Page("pages/customer_review_page.py", "Customer Reviews", "📝")
    ]
)

# Main app content can go here if any
if __name__ == "__main__":
    st.query_params = {"page": "pages.welcome_page"}
