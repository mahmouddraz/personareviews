import streamlit as st
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def transcribe_audio(audio_bytes):
    """Mock function that pretends to transcribe audio to text"""
    # In a real app, this would send the audio to a speech-to-text API
    time.sleep(1)  # Simulate API call delay
    
    # Return one of several fake transcriptions
    transcriptions = [
        "I want a place with free WiFi, laptop friendly space, and good cappuccino.",
        "Looking for a quiet spot that's not too crowded with strong espresso.",
        "Need somewhere with comfortable seating and not so noisy where I can work.",
        "A place with power outlets and peaceful ambiance for studying would be great.",
        "I'm looking for a cafe that's not crowded on weekends with good pastries."
    ]
    return random.choice(transcriptions)

def analyze_requirements(text):
    """Analyze the user's requirements from the transcribed text"""
    time.sleep(1)  # Simulate processing delay
    
    # Extract key requirements
    requirement_keywords = {
        "wifi": ["wifi", "internet", "connection", "online"],
        "quiet": ["quiet", "peaceful", "not noisy", "silence", "not loud"],
        "uncrowded": ["not crowded", "spacious", "empty", "not busy", "uncrowded"],
        "coffee": ["coffee", "cappuccino", "espresso", "latte"],
        "seating": ["seating", "comfortable", "chairs", "couch", "seats"],
        "laptop_friendly": ["laptop", "work", "outlet", "power", "study"]
    }
    
    found_requirements = {}
    text_lower = text.lower()
    
    for category, keywords in requirement_keywords.items():
        found_requirements[category] = any(keyword in text_lower for keyword in keywords)
    
    # Convert to list of requirements
    requirements_list = [req for req, found in found_requirements.items() if found]
    
    return requirements_list

def fetch_place_reviews(maps_link):
    """Mock function to get reviews from Google Maps"""
    # In a real app, this would use Google Places API
    time.sleep(1.5)  # Simulate API call
    
    sample_reviews = [
        {"rating": 5, "text": "Great WiFi and the cappuccino is amazing! Never too crowded in the mornings.", "date": "2 weeks ago"},
        {"rating": 4, "text": "Comfortable seating and laptop friendly. The coffee is good but a bit pricey.", "date": "1 month ago"},
        {"rating": 2, "text": "Always packed during lunch hours. Could barely find a seat.", "date": "3 weeks ago"},
        {"rating": 3, "text": "Decent wifi but it gets slow when the place is full. The espresso is excellent though.", "date": "1 week ago"},
        {"rating": 5, "text": "Perfect spot for working! Plenty of outlets and the staff doesn't mind if you stay for hours.", "date": "1 month ago"},
        {"rating": 1, "text": "Too noisy to concentrate. Avoid if you need to get work done.", "date": "2 months ago"},
        {"rating": 4, "text": "Great atmosphere and comfy chairs. The wifi password changes weekly which is annoying.", "date": "3 weeks ago"},
        {"rating": 2, "text": "Coffee is good but the place is tiny and always full.", "date": "1 month ago"}
    ]
    
    return {
        "average_rating": 3.25,
        "review_count": len(sample_reviews),
        "reviews": sample_reviews
    }

def extract_location_info(maps_link):
    """Mock function to extract information from a Google Maps link"""
    # In a real app, this would parse the link and fetch location details
    sample_locations = [
        {"name": "Central Park Cafe", "address": "123 Main St, New York, NY", "type": "Cafe", 
         "hours": "7AM - 10PM", "features": ["WiFi", "Outdoor Seating"]},
        {"name": "Oceanview Coffee", "address": "456 Beach Rd, Miami, FL", "type": "Coffee Shop",
         "hours": "6AM - 8PM", "features": ["Free WiFi", "Breakfast"]},
        {"name": "Mountain Study Lounge", "address": "789 Pine St, Denver, CO", "type": "Cafe",
         "hours": "8AM - 11PM", "features": ["Power Outlets", "Study Space"]},
        {"name": "City Library Cafe", "address": "101 Culture Ave, Chicago, IL", "type": "Cafe",
         "hours": "9AM - 7PM", "features": ["Quiet Space", "Free WiFi"]},
        {"name": "Sunset Reading Room", "address": "202 Literary Ln, San Francisco, CA", "type": "Bookstore Cafe",
         "hours": "10AM - 9PM", "features": ["Book Selection", "Coffee Bar"]}
    ]
    return random.choice(sample_locations)

def analyze_compatibility(requirements, reviews_data, location_info):
    """Analyze how well the place matches user requirements"""
    # Define keywords related to each requirement
    requirement_review_keywords = {
        "wifi": ["wifi", "internet", "connection", "online"],
        "quiet": ["quiet", "peaceful", "silence", "not loud"],
        "uncrowded": ["not crowded", "spacious", "empty", "not busy"],
        "coffee": ["coffee", "cappuccino", "espresso", "latte"],
        "seating": ["seating", "comfortable", "chairs", "couch", "seats"],
        "laptop_friendly": ["laptop", "work", "outlet", "power", "study"]
    }
    
    # Also consider opposite keywords (negative mentions)
    negative_keywords = {
        "wifi": ["poor wifi", "slow internet", "bad connection", "wifi doesn't work"],
        "quiet": ["noisy", "loud", "busy", "crowded"],
        "uncrowded": ["packed", "crowded", "busy", "full", "long wait"],
        "coffee": ["bad coffee", "terrible espresso", "poor quality", "overpriced"],
        "seating": ["uncomfortable", "hard chairs", "no seating", "limited seats"],
        "laptop_friendly": ["no outlets", "not for working", "no wifi", "not laptop friendly"]
    }
    
    # Analyze each requirement
    compatibility = {}
    highlighted_reviews = {
        "positive": [],
        "negative": []
    }
    
    for req in requirements:
        if req not in requirement_review_keywords:
            continue
            
        pos_count = 0
        neg_count = 0
        total_relevant = 0
        
        for review in reviews_data["reviews"]:
            text = review["text"].lower()
            
            # Check for positive mentions
            has_positive = any(keyword in text for keyword in requirement_review_keywords[req])
            # Check for negative mentions
            has_negative = any(keyword in text for keyword in negative_keywords.get(req, []))
            
            if has_positive or has_negative:
                total_relevant += 1
                
                if has_positive and not has_negative:
                    pos_count += 1
                    # Add to highlighted if it's a high rating
                    if review["rating"] >= 4 and req in text:
                        highlighted_reviews["positive"].append((req, review))
                        
                if has_negative:
                    neg_count += 1
                    # Add to highlighted if it's a low rating
                    if review["rating"] <= 2:
                        highlighted_reviews["negative"].append((req, review))
        
        # Calculate score (0-100)
        if total_relevant > 0:
            score = int((pos_count / total_relevant) * 100)
        else:
            # If no relevant reviews, check the location features
            if req in [feature.lower() for feature in location_info.get("features", [])]:
                score = 80  # Assume good if mentioned in features
            else:
                score = 50  # Neutral if no information
                
        compatibility[req] = score
    
    # Overall compatibility score
    if compatibility:
        overall_score = sum(compatibility.values()) / len(compatibility)
    else:
        overall_score = 50
        
    return {
        "requirement_scores": compatibility,
        "overall_score": overall_score,
        "highlighted_reviews": highlighted_reviews
    }

def display_compatibility(compatibility_data):
    """Display compatibility metrics"""
    st.subheader("Compatibility with Your Requirements")
    
    # Overall score gauge
    overall_score = compatibility_data["overall_score"]
    fig, ax = plt.subplots(figsize=(10, 3))
    
    # Create gauge chart for overall score
    colors = ['#ff9999', '#ffcc99', '#ffff99', '#99ff99', '#99cc99']
    ax.barh(["Overall"], [overall_score], color=colors[min(4, int(overall_score/20))], height=0.6)
    ax.barh(["Overall"], [100-overall_score], left=[overall_score], color='#f0f0f0', height=0.6)
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.get_yaxis().set_visible(False)
    
    # Add a vertical line for the overall score
    ax.axvline(x=overall_score, color='#444444', linestyle='-', alpha=0.7)
    
    # Add text with the score
    ax.text(overall_score, 0, f"{int(overall_score)}%", 
            ha='center', va='center', color='black', 
            fontweight='bold', fontsize=12)
    
    st.pyplot(fig)
    
    # Individual requirement scores
    if compatibility_data["requirement_scores"]:
        st.markdown("#### Individual Requirements")
        
        fig, ax = plt.subplots(figsize=(10, 4))
        requirements = list(compatibility_data["requirement_scores"].keys())
        scores = list(compatibility_data["requirement_scores"].values())
        
        # Sort by score (descending)
        sorted_data = sorted(zip(requirements, scores), key=lambda x: x[1], reverse=True)
        requirements = [item[0].replace('_', ' ').title() for item in sorted_data]
        scores = [item[1] for item in sorted_data]
        
        # Create horizontal bar chart
        colors = [colors[min(4, int(score/20))] for score in scores]
        ax.barh(requirements, scores, color=colors)
        ax.set_xlim(0, 100)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlabel('Match Score (%)')
        
        # Add score text at the end of each bar
        for i, score in enumerate(scores):
            ax.text(max(score + 2, 10), i, f"{int(score)}%", va='center')
        
        st.pyplot(fig)

def main():
    st.set_page_config(page_title="Place Matcher", page_icon="🗺️", layout="wide")
    
    st.title("🗺️ Place Requirement Matcher")
    st.markdown("Check if a place matches your requirements based on reviews!")
    
    # Two columns layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Step 1: Enter Location")
        maps_link = st.text_input("Paste Google Maps Link", 
                                 value="https://maps.google.com/example",
                                 placeholder="https://maps.google.com/...")
        
        if maps_link:
            location_info = extract_location_info(maps_link)
            
            st.success("Location found!")
            st.markdown(f"### {location_info['name']}")
            st.markdown(f"**Address:** {location_info['address']}")
            st.markdown(f"**Type:** {location_info['type']}")
            st.markdown(f"**Hours:** {location_info['hours']}")
            st.markdown("**Features:** " + ", ".join(location_info['features']))
            
        st.subheader("Step 2: Record Your Requirements")
        audio_bytes = st.audio_input(label = 'Record your requirements (e.g., "I need WiFi and quiet space")')
        
        if st.button("Check Compatibility") and maps_link:
            if audio_bytes:
                with st.spinner("Analyzing requirements and reviews..."):
                    # Mock the transcription and analysis process
                    transcription = transcribe_audio(audio_bytes)
                    requirements = analyze_requirements(transcription)
                    reviews_data = fetch_place_reviews(maps_link)
                    compatibility = analyze_compatibility(requirements, reviews_data, location_info)
                    
                    # Store in session state to display in the other column
                    st.session_state.analysis_submitted = True
                    st.session_state.transcription = transcription
                    st.session_state.requirements = requirements
                    st.session_state.reviews_data = reviews_data
                    st.session_state.compatibility = compatibility
                    st.session_state.location = location_info
                    
                    st.success("Analysis complete!")
            else:
                st.error("Please record your requirements before checking compatibility")
    
    with col2:
        st.subheader("Compatibility Analysis")
        
        if 'analysis_submitted' in st.session_state and st.session_state.analysis_submitted:
            st.markdown(f"### {st.session_state.location['name']}")
            
            st.markdown("#### Your Requirements:")
            st.info(st.session_state.transcription)
            
            if st.session_state.requirements:
                st.markdown("**We identified these key requirements:**")
                for req in st.session_state.requirements:
                    st.markdown(f"• {req.replace('_', ' ').title()}")
            else:
                st.warning("No specific requirements were identified. Please be more specific.")
            
            if st.session_state.requirements:
                # Display compatibility metrics
                display_compatibility(st.session_state.compatibility)
                
                # Show highlighted reviews
                st.markdown("### Key Reviews")
                
                # Positive highlights
                positive_highlights = st.session_state.compatibility["highlighted_reviews"]["positive"]
                if positive_highlights:
                    st.markdown("#### Positive Mentions")
                    for req, review in positive_highlights[:3]:  # Limit to top 3
                        st.markdown(f"**{req.replace('_', ' ').title()}** ⭐{review['rating']}")
                        st.markdown(f"> {review['text']}")
                        st.markdown(f"*{review['date']}*")
                        st.markdown("---")
                
                # Negative highlights - focus on these
                negative_highlights = st.session_state.compatibility["highlighted_reviews"]["negative"]
                if negative_highlights:
                    st.markdown("#### Negative Mentions")
                    for req, review in negative_highlights:
                        st.markdown(f"**{req.replace('_', ' ').title()}** ⭐{review['rating']}")
                        st.markdown(f"> {review['text']}")
                        st.markdown(f"*{review['date']}*")
                        st.markdown("---")
                
                # Overall rating from reviews
                st.markdown(f"**Average Rating:** {st.session_state.reviews_data['average_rating']}/5 ({st.session_state.reviews_data['review_count']} reviews)")
        else:
            st.info("Enter a location and record your requirements to see if it's a good match for you")

if __name__ == "__main__":
    main()
