import streamlit as st
import matplotlib.pyplot as plt
from transcribe_audio_page import transcribe_audio_page
from customer_review_page import customer_reviews_page

# Define supported languages and translations
LANGUAGES = {
    'en': 'English',
    'fr': 'French',
    'es': 'Spanish'
}

translations = {
    'title': {
        'en': 'Welcome to the Hand Sign Detection App',
        'fr': "Bienvenue dans l'application de détection des signes de la main",
        'es': 'Bienvenido a la aplicación de detección de signos de la mano'
    },
    'instructions': {
        'en': """
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
        'fr': """
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
        'es': """
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
    },
    'statistics': {
        'en': """
            ### Statistics on Emergency Calls for Deaf People
            
            According to various reports:
            - Approximately 1 million deaf and hard-of-hearing individuals reach out to emergency services each year.
            - Communication barriers can delay response times and affect the quality of assistance provided.
            - Innovations in technology, like this app, aim to bridge the communication gap and provide timely help to those in need.
        """,
        'fr': """
            ### Statistiques sur les appels d'urgence pour les personnes sourdes
            
            Selon divers rapports :
            - Environ 1 million de personnes sourdes et malentendantes contactent les services d'urgence chaque année.
            - Les barrières de communication peuvent retarder les temps de réponse et affecter la qualité de l'aide fournie.
            - Les innovations technologiques, comme cette application, visent à combler le fossé de communication et à fournir une aide rapide à ceux qui en ont besoin.
        """,
        'es': """
            ### Estadísticas sobre las llamadas de emergencia para personas sordas
            
            Según varios informes:
            - Aproximadamente 1 millón de personas sordas y con problemas de audición se comunican con los servicios de emergencia cada año.
            - Las barreras de comunicación pueden retrasar los tiempos de respuesta y afectar la calidad de la asistencia proporcionada.
            - Las innovaciones en tecnología, como esta aplicación, tienen como objetivo cerrar la brecha de comunicación y proporcionar ayuda oportuna a quienes la necesitan.
        """
    },
    'buttons': {
        'hand_sign': {
            'en': 'Go to Hand Sign Detection',
            'fr': 'Aller à la détection des signes de la main',
            'es': 'Ir a la detección de signos de la mano'
        },
        'transcription': {
            'en': 'Go to Audio/Video Transcription',
            'fr': "Aller à la transcription audio/vidéo",
            'es': 'Ir a la transcripción de audio/vídeo'
        },
        'reviews': {
            'en': 'Customer Reviews',
            'fr': 'Avis des clients',
            'es': 'Opiniones de los clientes'
        }
    }
}

def main():
    # Language selection
    selected_lang = st.sidebar.selectbox('Select Language / Sélectionnez la langue / Seleccione el idioma', options=list(LANGUAGES.keys()), format_func=lambda lang: LANGUAGES[lang])

    # Translate and display content
    st.title(translations['title'][selected_lang])
    st.write(translations['instructions'][selected_lang])
    st.write(translations['statistics'][selected_lang])

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
    if st.button(translations['buttons']['hand_sign'][selected_lang]):
        hand_sign_detection_page(selected_lang)  # Ensure this function accepts the language argument
    if st.button(translations['buttons']['transcription'][selected_lang]):
        transcribe_audio_page(selected_lang)
    if st.button(translations['buttons']['reviews'][selected_lang]):
        customer_reviews_page(selected_lang)

if __name__ == "__main__":
    main()
