import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
import os
import requests
import pytube

LANGUAGES = {
    'en': 'English',
    'fr': 'French',
    'es': 'Spanish'
}

translations = {
    'title': {
        'en': 'Audio/Video Transcription',
        'fr': 'Transcription Audio/Vidéo',
        'es': 'Transcripción de Audio/Vídeo'
    },
    'url_input': {
        'en': 'Enter the URL of the video or audio file (optional):',
        'fr': "Entrez l'URL du fichier vidéo ou audio (facultatif) :",
        'es': 'Ingrese la URL del archivo de video o audio (opcional):'
    },
    'file_uploader': {
        'en': 'Or upload an audio file',
        'fr': 'Ou téléchargez un fichier audio',
        'es': 'O cargue un archivo de audio'
    },
    'transcribe_button': {
        'en': 'Transcribe',
        'fr': 'Transcrire',
        'es': 'Transcribir'
    },
    'processing_message': {
        'en': 'Processing the file, please wait...',
        'fr': 'Traitement du fichier, veuillez patienter...',
        'es': 'Procesando el archivo, por favor espere...'
    },
    'error_message': {
        'en': 'Failed to download the file. Check the URL and try again.',
        'fr': "Échec du téléchargement du fichier. Vérifiez l'URL et réessayez.",
        'es': 'No se pudo descargar el archivo. Verifique la URL y vuelva a intentarlo.'
    },
    'transcription_success': {
        'en': 'Transcription completed successfully!',
        'fr': 'Transcription terminée avec succès!',
        'es': '¡Transcripción completada con éxito!'
    },
    'transcription_label': {
        'en': 'Transcription:',
        'fr': 'Transcription :',
        'es': 'Transcripción:'
    },
    'error_occurred': {
        'en': 'An error occurred:',
        'fr': "Une erreur s'est produite :",
        'es': 'Ocurrió un error:'
    },
    'no_input_error': {
        'en': 'Please enter a URL or upload a file.',
        'fr': 'Veuillez entrer une URL ou télécharger un fichier.',
        'es': 'Por favor, ingrese una URL o cargue un archivo.'
    }
}

def transcribe_audio_page(selected_lang):
    st.title(translations['title'][selected_lang])

    url = st.text_input(translations['url_input'][selected_lang])
    uploaded_file = st.file_uploader(translations['file_uploader'][selected_lang], type=["mp3", "wav", "mp4"])
    
    if st.button(translations['transcribe_button'][selected_lang]):
        if url or uploaded_file:
            try:
                st.write(translations['processing_message'][selected_lang])
                audio_file = "audio.wav"

                if uploaded_file:
                    with open("uploaded_file.mp4", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    clip = mp.VideoFileClip("uploaded_file.mp4")
                    clip.audio.write_audiofile(audio_file)
                
                elif "youtube.com" in url or "youtu.be" in url:
                    yt = pytube.YouTube(url)
                    video = yt.streams.filter(only_audio=True).first()
                    downloaded_file = video.download(filename='audio.mp4')
                    clip = mp.AudioFileClip(downloaded_file)
                    clip.write_audiofile(audio_file)
                
                else:
                    response = requests.get(url)
                    if response.status_code != 200:
                        st.error(translations['error_message'][selected_lang])
                        return
                    with open("video.mp4", 'wb') as f:
                        f.write(response.content)
                    clip = mp.VideoFileClip("video.mp4")
                    clip.audio.write_audiofile(audio_file)

                # Transcribe audio
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                st.success(translations['transcription_success'][selected_lang])
                st.text_area(translations['transcription_label'][selected_lang], text, height=200)
                
                # Cleanup
                os.remove(audio_file)
                if os.path.exists("video.mp4"):
                    os.remove("video.mp4")
                if os.path.exists("uploaded_file.mp4"):
                    os.remove("uploaded_file.mp4")
                if os.path.exists("audio.mp4"):
                    os.remove("audio.mp4")
                
            except Exception as e:
                st.error(f"{translations['error_occurred'][selected_lang]} {e}")
        else:
            st.error(translations['no_input_error'][selected_lang])