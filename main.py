from llm import compare_requirements_with_place_info, query_perplexity
from speach import generate, upload_to_gcs
import streamlit as st
import datetime
import os
from speach import clean_bucket
import time
from api_call_single import  parse_response_to_dict
from dotenv import load_dotenv
from google import genai
from google.genai import types
import base64
from openai import OpenAI
import requests
import json
import pandas as pd
from src.apicall import get_places_details,compare_requirements_with_place_info

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
import streamlit as st
import streamlit.components.v1 as components




with col1:
    st.markdown("Detecting your current location")
    html_code = """
        <script>
        navigator.geolocation.getCurrentPosition((position) => {
            const coords = position.coords;
            document.getElementById("data").innerText = 
                `Your current position: Latitude: ${coords.latitude}, Longitude: ${coords.longitude}`;
            // Store in local storage
            localStorage.setItem("latitude", coords.latitude);
            localStorage.setItem("longitude", coords.longitude);
        });
        </script>
        <div id="data" style="margin: 0; padding: 0;">Fetching location...</div>
    """

    # Inject the HTML
    # st.components.v1.html(html_code, height=50) 
    from streamlit_js_eval import streamlit_js_eval

    # Get coordinates from local storage
    latitude = streamlit_js_eval(js_expressions="localStorage.getItem('latitude')", key="lat")
    longitude = streamlit_js_eval(js_expressions="localStorage.getItem('longitude')", key="lng")

    # st.write(f"Latitude: {latitude}, Longitude: {longitude}")

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
        place_details=get_places_details(coordinate=(latitude, longitude),radius=1000,place_type="cafe")

        json_input=place_details[[
                "current_opening_hours_open_now",
                "reservable",
                "curbside_pickup",
                "price_level",
                "rating",
                "serves_breakfast",
                "serves_vegetarian_food",
                "editorial_summary_overview",
                "serves_lunch",
                "utc_offset",
                "takeout",
                "delivery",
                "dine_in",
                "wheelchair_accessible_entrance",
                "name",
                "serves_beer",
                "serves_brunch",
                "user_ratings_total",
                "serves_wine",
                'cashpayment','cardpayment',
        'dog_friendly', 'laptop_friendly',
                "serves_dinner",
                "reviews",
                "business_status"]]
        
        llm_input=json_input.to_json()

        info = compare_requirements_with_place_info(requirements=requirements, place_details=llm_input)
        recommendations = parse_response_to_dict(info)

        
        # response = query_perplexity(prompt=prompt, api_key=api_key)
        # recommendation = response['choices'][0]['message']['content']
        col2.markdown("### Recommendation:")
        for i, place in enumerate(recommendations, start=1):
            name = place["name"]
            rating = place["rating"]
            col2.success(f"{i}. Place: {name} (Rating: {rating}/5)")
        # col2.success(f"Recommendation: {recommendation}")
   

        # personalise_rating = final['rating']



        # Display rating
        first_place = recommendations[0]  # Get the first place
        
        st.subheader("🏆 Your Personalized Top Recommended Café:")
 
        st.subheader(f"**{first_place['name']} ({first_place['rating']})**")          # rating_stars = "⭐" * int(round(personalise_rating/2))  # Convert to 1-5 stars
        # st.markdown(f"<h2 style='text-align: center;'>{personalise_rating}/5 {rating_stars}</h2>", unsafe_allow_html=True)
        st.markdown(f"**{first_place['reasoning']}**")          # rating_stars = "⭐" * int(round(personalise_rating/2))  # Convert to 1-5 stars

        progress_bar.progress(100)
        
    st.balloons()
