import streamlit as st
import whisper
from googletrans import Translator
import tempfile
import os

# Load the Whisper model
@st.cache_resource
def load_model():
    return whisper.load_model("medium")

model = load_model()
translator = Translator()

def transcribe_audio(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name

    audio = whisper.load_audio(temp_file_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    os.remove(temp_file_path)  # Clean up the temporary file
    return result.text

def translate_text(text, target_language):
    translation = translator.translate(text, dest=target_language)
    return translation.text

def app():
    st.title("Speech-to-Text and Translation 🗣️")

    uploaded_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav"])

    if uploaded_file is not None:
        with st.spinner("Transcribing..."):
            transcription = transcribe_audio(uploaded_file)
            st.success("Transcription completed!")
            st.text_area("Transcription:", value=transcription, height=200)
        
        target_language = st.selectbox("Select target language for translation:", ["es", "fr", "de", "zh", "ja", "hi"])
        
        if st.button("Translate"):
            with st.spinner("Translating..."):
                translated_text = translate_text(transcription, target_language)
                st.success("Translation completed!")
                st.text_area("Translation:", value=translated_text, height=200)

if __name__ == "__main__":
    app()
