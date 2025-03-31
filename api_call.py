from dotenv import load_dotenv
import os
import re
import requests
import json

from googleapiclient.discovery import build

load_dotenv()
API_KEY=os.getenv("GOOGLE_API_KEY")

def get_place_id(google_maps_url):

    # Step 1: Expand short URL if needed
    response = requests.get(google_maps_url, allow_redirects=True)
    expanded_url = response.url  # Get the final redirected URL
    
    # Step 2: Extract Place ID using regex
    match = re.search(r"1s([A-Za-z0-9_-]+)", expanded_url)
    
    if match:
        return match.group(1)
    else:
        return "Place ID not found"


def get_google_reviews(input_url):
    """
    Returns a JSON file with google maps reviews of place specified by URL. 
    URL = 'https://www.google.com/maps/place/Coffee+Fellows/@52.5187619,13.390657,16.38z/data=!4m6!3m5!1s0x47a85112f53a95fd:0xfdf13d684a6ff07b!8m2!3d52.5199246!4d13.3888139!16s%2Fg%2F11fmfz6hg4?entry=ttu&g_ep=EgoyMDI1MDMyNS4xIKXMDSoASAFQAw%3D%3D'
    """
    link = "https://maps.app.goo.gl/X3zNLhkMrFF3m65MA"
    #PLACE_ID = get_place_id(input_url)
    PLACE_ID = "ChIJMRf7YNBRqEcR1mUQLhrJtss"

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
    
    return general_information

# run

if __name__ == "__main__":
    url = input("Enter a URL: ").strip()

    get_google_reviews(url)


#res = get_google_reviews(input_url='https://www.google.com/maps/place/Espresso+House/@52.5139521,13.3991998,14.69z/data=!3m1!5s0x47a84fdc2df7cc8b:0x7a8d8e897582900d!4m14!1m7!3m6!1s0x47a85112f53a95fd:0xfdf13d684a6ff07b!2sCoffee+Fellows!8m2!3d52.5199246!4d13.3888139!16s%2Fg%2F11fmfz6hg4!3m5!1s0x47a851ab89a4030f:0x68146642825a7b12!8m2!3d52.5197469!4d13.4036221!16s%2Fg%2F11j2vwx0l9?entry=ttu&g_ep=EgoyMDI1MDMyNS4xIKXMDSoASAFQAw%3D%3D')









