import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import streamlit as st

# Global variable to stop recording
stop_recording = False

# Function to recognize speech from microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = recognizer.listen(source, timeout=10)  # Timeout set to 10 seconds
        text = recognizer.recognize_google(audio_data)
    return text

# Function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Function to convert speech to translation
def speech_to_translation(target_language):
    recognized_text = recognize_speech()
    translated_text = translate_text(recognized_text, target_language)
    return translated_text

# Streamlit UI
st.title("Consecutive Interpretation App")

# Language selection
input_language_auto = st.checkbox("Auto Detect Input Language")
input_language = st.selectbox("Select Input Language", ["en", "ru"]) if not input_language_auto else None
output_language = st.selectbox("Select Output Language", ["en", "ru"])

# Recognition and Translation
if st.button("Start Recording"):
    st.write("Recording... Speak now!")

    # Reset the global variable
    stop_recording = False

    while not stop_recording:
        recorded_text = recognize_speech()
        st.subheader("Recognized Text")
        st.write(recorded_text)

        translated_text = translate_text(recorded_text, output_language)
        st.subheader("Translated Text")
        st.write(translated_text)

        # Play the translated text
        tts = gTTS(translated_text, lang=output_language)
        tts.save('audio/translation.mp3')
        st.audio('audio/translation.mp3', format="audio/mp3")

        # Add button to stop recording
        stop_recording = st.button("Stop Recording")

# Stop recording if the loop exits
st.stop()
