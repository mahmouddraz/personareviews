# Voice Review App

A Streamlit application that lets users record voice reviews for locations and displays analysis of their review.

## Features

- Input Google Maps links to specify locations
- Record voice reviews directly in the browser
- View automatic rating and keyword extraction from your review
- Simple and intuitive interface

## Setup and Running

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```
   streamlit run voice_review_app.py
   ```

3. Open your browser and go to the URL displayed in the terminal (typically http://localhost:8501)

## Notes

This is currently a mockup with simulated API calls. In a production version, this would:
- Use a real speech-to-text API (like Google Speech API)
- Use NLP for sentiment analysis (like NLTK or spaCy)
- Parse and validate Google Maps links properly
- Store reviews in a database