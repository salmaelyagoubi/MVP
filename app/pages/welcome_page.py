import streamlit as st
import matplotlib.pyplot as plt
from twilio.rest import Client
from geopy.geocoders import Nominatim
import geocoder

# Translation dictionaries
translations = {
    "title": {
        "English": "Welcome to the Hand Sign Detection App",
        "Français": "Bienvenue dans l'application de détection des signes de la main",
        "Español": "Bienvenido a la aplicación de detección de signos de la mano"
    },
    "how_to_use": {
        "English": """
            This application allows you to detect hand signs and translate them into letters.
            
            **How to use the app:**
            1. Navigate to the 'Hand Sign Detection' page.
            2. Allow access to your webcam.
            3. Adjust the confidence threshold using the slider if necessary.
            4. The detected letters will be displayed on the screen.
            5. Use the 'Reset Detected Letters' button to clear the detected letters.
            6. Use the 'Stop Webcam' button to stop the webcam feed.
            
            **Note:** Ensure you are in a well-lit area and that your hand is clearly visible to the camera.
        """,
        "Français": """
            Cette application vous permet de détecter les signes de la main et de les traduire en lettres.
            
            **Comment utiliser l'application :**
            1. Allez à la page 'Détection des signes de la main'.
            2. Autorisez l'accès à votre webcam.
            3. Ajustez le seuil de confiance à l'aide du curseur si nécessaire.
            4. Les lettres détectées s'afficheront à l'écran.
            5. Utilisez le bouton 'Réinitialiser les lettres détectées' pour effacer les lettres détectées.
            6. Utilisez le bouton 'Arrêter la webcam' pour arrêter le flux de la webcam.
            
            **Remarque :** Assurez-vous d'être dans un endroit bien éclairé et que votre main soit bien visible par la caméra.
        """,
        "Español": """
            Esta aplicación te permite detectar signos de la mano y traducirlos en letras.
            
            **Cómo usar la aplicación:**
            1. Navega a la página 'Detección de Signos de la Mano'.
            2. Permite el acceso a tu cámara web.
            3. Ajusta el umbral de confianza usando el deslizador si es necesario.
            4. Las letras detectadas se mostrarán en la pantalla.
            5. Usa el botón 'Restablecer Letras Detectadas' para borrar las letras detectadas.
            6. Usa el botón 'Detener Cámara Web' para detener el feed de la cámara web.
            
            **Nota:** Asegúrate de estar en un área bien iluminada y que tu mano sea claramente visible para la cámara.
        """
    }
}

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
    lang = st.session_state.get("selected_lang", "English")
    
    st.title(translations["title"][lang])
    st.write(translations["how_to_use"][lang])

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
            st.success(f"Message sent successfully! SID: {message_sid} please wait for help in ")
        except Exception as e:
            st.error(f"Failed to send message: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    welcome_page()
