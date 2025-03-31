import streamlit as st
import datetime

audio_value = st.audio_input("Record a voice message")

# Check if audio was recorded
if audio_value is not None:
    # Create a unique filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recorded_audio_{timestamp}.mp3"
    
    # Save the audio bytes to a file
    with open(filename, "wb") as f:
        f.write(audio_value.getvalue())
    