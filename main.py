from llm import compare_requirements_with_place_info, query_perplexity
from speach import generate, upload_to_gcs
import streamlit as st
import datetime
import os
from speach import clean_bucket
import time
from api_call_single import compare_requirements_with_place_info, parse_response_to_dict
from dotenv import load_dotenv

# Custom CSS to improve appearance
st.set_page_config(layout="wide", page_title="MAPME - Place Finder")

# # Apply custom styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         color: #1E88E5;
#         text-align: center;
#     }
#     .subheader {
#         font-size: 1.5rem;
#         color: #424242;
#         margin-bottom: 2rem;
#         text-align: center;
#     }
#     .card {
#         padding: 1.5rem;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#         margin-bottom: 1rem;
#         background-color: #f8f9fa;
#     }
#     .success-text {
#         color: #2E7D32;
#         font-weight: bold;
#     }
#     .stAudio {
#         margin: 1rem 0;
#     }
# </style>
# """, unsafe_allow_html=True)

# App header with improved styling
st.markdown("<h1 class='main-header'>MAPME 🗺️</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Share your preferences, and we'll find the perfect place for you! 🍽️ ☕️</p>", unsafe_allow_html=True)

# Create two columns for better layout
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Enter Place Information")
    link = st.text_input("Place link or Google Maps URL", placeholder="https://maps.google.com/...")    
    st.markdown("<h4>Record your preferences</h4>", unsafe_allow_html=True)
    st.markdown("Tell us what you're looking for in this place:")
    audio_value = st.audio_input("Record your voice")
    st.markdown("</div>", unsafe_allow_html=True)
    
    filename = None
    if audio_value is not None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recorded_audio_{timestamp}.mp3"
        
        with open(filename, "wb") as f:
            f.write(audio_value.getvalue())
        
        st.success("✅ Audio recorded successfully!")

    analyze_button = st.button("🔎 Analyze", type="primary", use_container_width=True)
    


if analyze_button and filename:
    with st.spinner('Processing your audio...'):
        progress_bar = st.progress(0)
        
        # Simulate progress for better UX
        for percent in range(50):
            time.sleep(0.02)
            progress_bar.progress(percent)
            
        requirements = generate(filename)
        col2.markdown("## Your Requirements:")
        col2.info(f"Your requirements: {requirements}")

    
        
        for percent in range(50, 75):
            time.sleep(0.01)
            progress_bar.progress(percent)
        
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)
        clean_bucket()
        
        # Load environment variables
        load_dotenv()
        api_key = os.environ.get("PERPLEXITY_API_KEY")
        
        for percent in range(75, 90):
            time.sleep(0.01)
            progress_bar.progress(percent)

        info = compare_requirements_with_place_info(requirements=requirements, place_url=link)
        final = parse_response_to_dict(info)

        cafe_name = final['cafe_name']

        # Generate recommendation
        prompt = f"""Find all relevant information about {cafe_name} in Berlin. I want to know if I should go there based on my requirements: {requirements}.
        Be concise and provide direct feedback in two lines maximum."""

        
        response = query_perplexity(prompt=prompt, api_key=api_key)
        recommendation = response['choices'][0]['message']['content']
        col2.markdown("### Recommendation:")
        col2.success(f"Recommendation: {recommendation}")
   

        personalise_rating = final['rating']



        # Display rating
        st.markdown("### Personalized Rating:")
        rating_stars = "⭐" * int(round(personalise_rating/2))  # Convert to 1-5 stars
        st.markdown(f"<h2 style='text-align: center;'>{personalise_rating}/5 {rating_stars}</h2>", unsafe_allow_html=True)
        progress_bar.progress(100)
        
    st.balloons()
