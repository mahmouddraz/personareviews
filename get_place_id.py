import re
import requests
from dotenv import load_dotenv
import os
import random
from dotenv import load_dotenv

load_dotenv()
API_KEY=os.getenv("GOOGLE_API_KEY")


def get_place_id(google_maps_url, api_key=API_KEY):
    """
    Extracts the Place ID from a Google Maps URL using Google Places API.
    
    Args:
        google_maps_url (str): The Google Maps URL.
        api_key (str): Your Google Places API Key.
    
    Returns:
        str: The Place ID if found, else an error message.
    """
    # Extract the place identifier from the URL
    match = re.search(r'place/([^/]+)', google_maps_url)
    if not match:
        return "Invalid Google Maps URL"
    
    place_name = match.group(1).replace('+', ' ')  # Convert + to space if needed
    
    # Construct the API request
    endpoint = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": place_name,
        "inputtype": "textquery",
        "fields": "place_id",
        "key": api_key
    }
    
    # Make the request
    response = requests.get(endpoint, params=params)
    data = response.json()
    
    # Parse the response
    if "candidates" in data and len(data["candidates"]) > 0:
        return data["candidates"][0]["place_id"]
    else:
        return "Place ID not found"

# Example Usage
google_maps_url = "https://www.google.com/maps/place/Empire+State+Building/@40.748817,-73.985428,17z/"
api_key = API_KEY  # Replace with your actual API key
place_id = get_place_id(google_maps_url, api_key)
print("Place ID:", place_id)



