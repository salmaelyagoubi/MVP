import streamlit as st
import matplotlib.pyplot as plt
from pages.hand_sign_detection_page import hand_sign_detection_page
from pages.transcribe_audio_page import transcribe_audio_page

def main():
    st.title("Welcome to the Hand Sign Detection App")
    st.write("""
        This application allows you to detect hand signs and translate them into letters.
        
        **How to use the app:**
        1. Navigate to the 'Hand Sign Detection' page.
        2. Allow access to your webcam.
        3. Adjust the confidence threshold using the slider if necessary.
        4. The detected letters will be displayed on the screen.
        5. Use the 'Reset Detected Letters' button to clear the detected letters.
        6. Use the 'Stop Webcam' button to stop the webcam feed.
        
        **Note:** Ensure you are in a well-lit area and that your hand is clearly visible to the camera.
    """)

    st.write("""
        ### Statistics on Emergency Calls for Deaf People
        
        According to various reports:
        - Approximately 1 million deaf and hard-of-hearing individuals reach out to emergency services each year.
        - Communication barriers can delay response times and affect the quality of assistance provided.
        - Innovations in technology, like this app, aim to bridge the communication gap and provide timely help to those in need.
    """)

    # Sample data for statistics
    labels = ['Emergency Calls Answered', 'Emergency Calls Missed']
    sizes = [70, 30]  # Example data
    colors = ['#ff9999','#66b3ff']
    explode = (0.1, 0)  # explode 1st slice

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)

    # Navigation buttons
    if st.button('Go to Hand Sign Detection'):
        hand_sign_detection_page()
    if st.button('Go to Audio/Video Transcription'):
        transcribe_audio_page()

if __name__ == "__main__":
    main()
