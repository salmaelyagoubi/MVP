import streamlit as st
import matplotlib.pyplot as plt
from twilio.rest import Client
from opencage.geocoder import OpenCageGeocode
from geopy.geocoders import Nominatim
import geocoder
import os


TWILIO_ACCOUNT_SID = 'add yours '
TWILIO_AUTH_TOKEN = 'add yours'

# Custom CSS for button styling
st.markdown(
    """
    <style>
    .centered-button {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .centered-button button {
        background-color: red !important;
        color: white !important;
        border-radius: 50px;
        font-size: 24px;
        padding: 20px 40px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Function to send SMS
def send_sms(location):
    account_sid =TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    if not account_sid or not auth_token:
        raise ValueError("Twilio credentials are not set in environment variables.")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"This person needs your help. Location: {location}",
        from_='+12513696511',
        to='+33619164400'
    )

    return message.sid

# Function to get detailed location dynamically
def get_location():
    g = geocoder.ip('me')
    if g.ok:
        latlng = g.latlng
        geolocator = Nominatim(user_agent="your_app_name")
        location = geolocator.reverse(latlng, exactly_one=True)
        if location:
            address = location.raw.get('address', {})
            street = address.get('road', 'N/A')
            neighborhood = address.get('neighbourhood', 'N/A')
            city = address.get('city', 'N/A')
            state = address.get('state', 'N/A')
            country = address.get('country', 'N/A')
            return f"{street}, {neighborhood}, {city}, {state}, {country}"
        else:
            return "Unknown location"
    else:
        return "Unknown location"

def welcome_page():
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

    labels = ['Emergency Calls Answered', 'Emergency Calls Missed']
    sizes = [70, 30]
    colors = ['#ff9999','#66b3ff']

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')

    # Remove the background
    fig1.patch.set_visible(False)
    ax1.axis('off')

    st.pyplot(fig1)


    st.markdown("""
        <div class="centered-button">
            <h2>Press the button to get instant help:</h2>
            
        """,
        unsafe_allow_html=True)
    if st.button('SOS', key='panic_button'):
        location = get_location()
        st.write(f"Location: {location}")
        try:
            message_sid = send_sms(location)
            st.success(f"Message sent successfully! SID: {message_sid} please wait for help in your location.")
        except Exception as e:
            st.error(f"Failed to send message: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    welcome_page()
