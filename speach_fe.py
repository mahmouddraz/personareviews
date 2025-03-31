from speach import generate
import streamlit as st
import os
from datetime import datetime
from pydub import AudioSegment
import io

def main():
    st.title("Audio Recorder")
    st.write("Record your audio and save it as MP3")
    
    # Record audio using audio_recorder
    audio_bytes = st.audio_input("1")
    
    if audio_bytes:
       st.write(generate(audio_bytes))

if __name__ == "__main__":
    main()