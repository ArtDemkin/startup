import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import streamlit as st

# Function to recognize speech
def recognize_speech(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

# Function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Function to convert speech to translation
def speech_to_translation(audio_file_path, target_language):
    recognized_text = recognize_speech(audio_file_path)
    translated_text = translate_text(recognized_text, target_language)
    return translated_text

# Streamlit UI
st.title("Consecutive Interpretation App")

# Upload audio file
uploaded_file = st.file_uploader("Upload an audio file (WAV format)", type=["wav"])
if uploaded_file:
    st.audio(uploaded_file, format="audio/wav")
    st.write("Translating...")

    # Process the uploaded audio file
    audio_file_path = "audio/file.wav"
    with open(audio_file_path, "wb") as f:
        f.write(uploaded_file.read())

    translated_text = speech_to_translation(audio_file_path, target_language='ru')

    # Display the translated text
    st.subheader("Translated Text")
    st.write(translated_text)

    # Play the translated text
    tts = gTTS(translated_text, lang='ru')
    tts.save('audio/translation.mp3')
    st.audio('audio/translation.mp3', format="audio/mp3")

st.write("Note: This app is for consecutive interpretation from English to Russian.")