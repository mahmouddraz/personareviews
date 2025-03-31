from dotenv import load_dotenv
import os
import re
import requests
import json

from googleapiclient.discovery import build

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


def get_google_reviews(input_url):
    """
    Returns a JSON file with google maps reviews of place specified by URL. 
    URL = 'https://www.google.com/maps/place/Coffee+Fellows/@52.5187619,13.390657,16.38z/data=!4m6!3m5!1s0x47a85112f53a95fd:0xfdf13d684a6ff07b!8m2!3d52.5199246!4d13.3888139!16s%2Fg%2F11fmfz6hg4?entry=ttu&g_ep=EgoyMDI1MDMyNS4xIKXMDSoASAFQAw%3D%3D'
    """
    
    PLACE_ID = get_place_id(input_url)
    #PLACE_ID = "ChIJMRf7YNBRqEcR1mUQLhrJtss"

    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&fields=name,rating,reviews&key={API_KEY}"

    # Make the request using Google SDK's `build` function (alternative to requests)
    service = build("customsearch", "v1", developerKey=API_KEY)  # This is just an example service

    response = requests.get(url)
    data = response.json()

    # Extract information to dictionary 
    general_information = {}
    reviews_dict = {}

    if "result" in data: 

        general_information["restaurant_name"] = data["result"].get("name", "Unknown")
        general_information['overall_rating'] = data["result"].get("rating", "No Rating")
        reviews = data["result"].get("reviews", [])


        # populate reviews
        for review in reviews:
            reviews_dict[review.get("author_name", "Anonymous")] = dict({
                                    "rating": review.get("rating", "No Rating"),
                                    "text": review.get("text", "No review text")})
            
        general_information['reviews'] = reviews_dict

        print(general_information)
    
    else:
         print("Error fetching reviews!")

 
    # export JSON file 
    with open('result.json', 'w') as fp:
        json.dump(general_information, fp)
    
    return

# run

if __name__ == "__main__":
    url = 'https://www.google.com/maps/place/Espresso+House/@52.5139521,13.3991998,14.69z/data=!3m1!5s0x47a84fdc2df7cc8b:0x7a8d8e897582900d!4m14!1m7!3m6!1s0x47a85112f53a95fd:0xfdf13d684a6ff07b!2sCoffee+Fellows!8m2!3d52.5199246!4d13.3888139!16s%2Fg%2F11fmfz6hg4!3m5!1s0x47a851ab89a4030f:0x68146642825a7b12!8m2!3d52.5197469!4d13.4036221!16s%2Fg%2F11j2vwx0l9?entry=ttu&g_ep=EgoyMDI1MDMyNS4xIKXMDSoASAFQAw%3D%3D'
    url = 'https://www.google.com/maps/place/Caf%C3%A9+Anna+Blume/@52.5371817,13.4207449,17.41z/data=!3m1!5s0x47a84e0108a0f505:0xa0ba322584220387!4m6!3m5!1s0x47a84e01061fde95:0xf6b1fa04e27f04d6!8m2!3d52.5380566!4d13.4195398!16s%2Fg%2F1ts3k78q?entry=ttu&g_ep=EgoyMDI1MDMyNS4xIKXMDSoASAFQAw%3D%3D'
    #input("Enter a URL: ").strip()

    get_google_reviews(url)