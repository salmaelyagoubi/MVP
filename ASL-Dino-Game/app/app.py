import streamlit as st

# Set the title of the app
st.title("Chrome Dino Game")

# Add some styling
st.markdown("""
<style>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    text-align: center;
}
.button-container {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}
.button-container button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border: none;
    border-radius: 5px;
    color: #fff;
    background-color: #007bff;
}
.button-container button:hover {
    background-color: #0056b3;
}
.iframe-container {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}
iframe {
    border: none;
    width: 800px;
    height: 600px;
}
</style>
""", unsafe_allow_html=True)

# Create a container for the game and buttons
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Play"):
            st.markdown("""
                <div class="iframe-container">
                    <iframe src="https://chromedino.com/" title="Chrome Dino Game"></iframe>
                </div>
            """, unsafe_allow_html=True)
    with col2:
        if st.button("Score"):
            st.write("Your current score: 0")  # This is a placeholder. You can integrate score logic here.
    with col3:
        if st.button("Exit"):
            st.write("Exiting the game. Goodbye!")
            st.stop()

