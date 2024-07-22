import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
import os
import requests
import pytube

def transcribe_audio_page():
    st.title("Audio/Video Transcription")

    url = st.text_input("Enter the URL of the video or audio file (optional):")
    uploaded_file = st.file_uploader("Or upload an audio file", type=["mp3", "wav", "mp4"])
    
    if st.button("Transcribe"):
        if url or uploaded_file:
            try:
                st.write("Processing the file, please wait...")
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
                        st.error("Failed to download the file. Check the URL and try again.")
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
                st.success("Transcription completed successfully!")
                st.text_area("Transcription:", text, height=200)
                
                # Cleanup
                os.remove(audio_file)
                if os.path.exists("video.mp4"):
                    os.remove("video.mp4")
                if os.path.exists("uploaded_file.mp4"):
                    os.remove("uploaded_file.mp4")
                if os.path.exists("audio.mp4"):
                    os.remove("audio.mp4")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a URL or upload a file.")
