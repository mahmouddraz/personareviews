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
    # Save audio as MP3 if recorded
    if audio_bytes:
        # Create a unique filename using current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recorded_audio_{timestamp}.mp3"
        
        # Convert audio bytes to MP3 format
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
            
            # Save the audio to a file
            audio.export(filename, format="mp3")
            
            st.success(f"Audio saved as {filename}")
        except Exception as e:
            st.error(f"Error saving audio: {str(e)}")
    
    if audio_bytes:
       st.write(generate(filename))

if __name__ == "__main__":
    main()