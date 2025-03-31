from dotenv import load_dotenv
import os
import re
import requests
import json
from google import genai
from google.genai import types
import base64
from openai import OpenAI
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
    Returns a python dict with google maps reviews of place specified by URL. 
    URL = 'https://www.google.com/maps/place/Coffee+Fellows/@52.5187619,13.390657,16.38z/data=!4m6!3m5!1s0x47a85112f53a95fd:0xfdf13d684a6ff07b!8m2!3d52.5199246!4d13.3888139!16s%2Fg%2F11fmfz6hg4?entry=ttu&g_ep=EgoyMDI1MDMyNS4xIKXMDSoASAFQAw%3D%3D'
    """
    
    PLACE_ID = get_place_id(input_url)
    
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
    
    else:
         print("Error fetching reviews!")

 
    # export JSON file 
    with open('result.json', 'w') as fp:
        json.dump(general_information, fp)
    
    return general_information


def convert_place_info(place_dict):
  """
  Input `place_dict`
  Output: text
  """
  return "\n".join(f"{key}: {value}" for key, value in place_dict.items())  



def compare_requirements_with_place_info(requirements=None, place_url=None):
  client = genai.Client(
    vertexai=True,
    project="bliss-hack25fra-9533",
    location="us-central1",
  )

  text1 = types.Part.from_text(text=
                               """You are an expert travel advisor, and you love to make personalized recommendations for users.
                               You have a favorite cafe for which you have a set of reviews {place_info}.
                               A user gives you his requirements for the perfect cafe {requirements}.

                               Your task is to give the user a rating between 0 and 5 starts of how well does your favorite cafe match his requirements.

                               You must return: 
                               - The name of your favorite cafe. 
                               - The personalized rating that you would give for that cafe. 
                               - An example from the {place_info} that explains why you would give that rating.

                               """)

  
  text2 = types.Part.from_text(text=requirements)

  place_info = get_google_reviews(place_url)

  place_info = convert_place_info(place_info)

  text3 = types.Part.from_text(text=place_info)



  model = "gemini-2.0-flash-lite-001"
  contents = [
    types.Content(
      role="user",
      parts=[
        text1,
        text2,
        text3
      ]
    )
  ]
  generate_content_config = types.GenerateContentConfig(
    temperature = 0,
    top_k = 1,
    candidate_count = 1,
    max_output_tokens = 8192,
  )

  response = client.models.generate_content(
    model = model,
    contents = contents,
    config = generate_content_config,
  )

  print(response.text)

  return response.text


# gemini call outputs python dict 


# run
if __name__ == "__main__":
    compare_requirements_with_place_info(requirements="dog-friendly, laptop friendly, cheap, serves a cappuccino", 
                                       place_url='https://www.google.com/maps/place/Caf%C3%A9+Anna+Blume/@52.5371817,13.4207449,17.41z/data=!3m1!5s0x47a84e0108a0f505:0xa0ba322584220387!4m6!3m5!1s0x47a84e01061fde95:0xf6b1fa04e27f04d6!8m2!3d52.5380566!4d13.4195398!16s%2Fg%2F1ts3k78q?entry=ttu&g_ep=EgoyMDI1MDMyNS4xIKXMDSoASAFQAw%3D%3D')