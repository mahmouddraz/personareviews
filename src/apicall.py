import json
import os
import random
import re
import googlemaps
import pandas as pd
import os
import random
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Initialize Google Maps Client
gmaps = googlemaps.Client(key=API_KEY)

# from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")


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


# def get_google_reviews(input_url):
#     """
#     Returns a JSON file with google maps reviews of place specified by URL.
#     URL = 'https://www.google.com/maps/place/Coffee+Fellows/@52.5187619,13.390657,16.38z/data=!4m6!3m5!1s0x47a85112f53a95fd:0xfdf13d684a6ff07b!8m2!3d52.5199246!4d13.3888139!16s%2Fg%2F11fmfz6hg4?entry=ttu&g_ep=EgoyMDI1MDMyNS4xIKXMDSoASAFQAw%3D%3D'
#     """

#     #PLACE_ID = get_place_id(input_url)
#     PLACE_ID = "ChIJMRf7YNBRqEcR1mUQLhrJtss"

#     url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&fields=name,rating,reviews&key={API_KEY}"

#     # Make the request using Google SDK's `build` function (alternative to requests)
#     service = build("customsearch", "v1", developerKey=API_KEY)  # This is just an example service

#     response = requests.get(url)
#     data = response.json()

#     # Extract information to dictionary
#     general_information = {}
#     reviews_dict = {}

#     if "result" in data:

#         general_information["restaurant_name"] = data["result"].get("name", "Unknown")
#         general_information['overall_rating'] = data["result"].get("rating", "No Rating")
#         reviews = data["result"].get("reviews", [])


#         # populate reviews
#         for review in reviews:
#             reviews_dict[review.get("author_name", "Anonymous")] = dict({
#                                     "rating": review.get("rating", "No Rating"),
#                                     "text": review.get("text", "No review text")})

#         general_information['reviews'] = reviews_dict

#         print(general_information)

#     else:
#          print("Error fetching reviews!")


#     # export JSON file
#     with open('result.json', 'w') as fp:
#         json.dump(general_information, fp)

#     return

# # run

# if __name__ == "__main__":
#     url = input("Enter a URL: ").strip()

#     get_google_reviews(url)


# res = get_google_reviews(input_url='https://www.google.com/maps/place/Espresso+House/@52.5139521,13.3991998,14.69z/data=!3m1!5s0x47a84fdc2df7cc8b:0x7a8d8e897582900d!4m14!1m7!3m6!1s0x47a85112f53a95fd:0xfdf13d684a6ff07b!2sCoffee+Fellows!8m2!3d52.5199246!4d13.3888139!16s%2Fg%2F11fmfz6hg4!3m5!1s0x47a851ab89a4030f:0x68146642825a7b12!8m2!3d52.5197469!4d13.4036221!16s%2Fg%2F11j2vwx0l9?entry=ttu&g_ep=EgoyMDI1MDMyNS4xIKXMDSoASAFQAw%3D%3D')


def get_places_details(
    coordinate: tuple = None,
    link: str = None,
    place_type=["restaurant", "cafe"],
    radius=1000,
):
    """Fetches place details either by coordinate (Nearby Search) or from a Google Maps link (Place ID)."""
    API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

    gmaps = googlemaps.Client(key=API_KEY)

    # Function to flatten nested JSON
    def flatten_dict(d, parent_key="", sep="_"):
        """Recursively flattens a nested dictionary."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                items.append((new_key, str(v)))  # Convert lists to string
            else:
                items.append((new_key, v))
        return dict(items)

    all_places = []

    if coordinate:
        # Perform Nearby Search
        places_result = gmaps.places_nearby(
            location=coordinate, radius=radius, type=place_type
        )

        for place in places_result.get("results", []):
            place_id = place.get("place_id")
            # Fetch place details
            place_details = gmaps.place(
                place_id=place_id,
                fields=[
                    "geometry/location/lat",
                    "plus_code",
                    "current_opening_hours",
                    "geometry/viewport/northeast/lng",
                    "website",
                    "reservable",
                    "curbside_pickup",
                    "address_component",
                    "price_level",
                    "geometry/viewport/northeast/lat",
                    "type",
                    "geometry/location/lng",
                    "photo",
                    "rating",
                    "serves_breakfast",
                    "serves_vegetarian_food",
                    "editorial_summary",
                    "secondary_opening_hours",
                    "serves_lunch",
                    "place_id",
                    "url",
                    "geometry/viewport/southwest/lat",
                    "utc_offset",
                    "permanently_closed",
                    "geometry/viewport/southwest",
                    "takeout",
                    "delivery",
                    "dine_in",
                    "opening_hours",
                    "wheelchair_accessible_entrance",
                    "name",
                    "review",
                    "adr_address",
                    "formatted_address",
                    "serves_beer",
                    "formatted_phone_number",
                    "international_phone_number",
                    "serves_brunch",
                    "geometry/location",
                    "geometry/viewport/southwest/lng",
                    "user_ratings_total",
                    "geometry/viewport",
                    "serves_wine",
                    "icon",
                    "vicinity",
                    "serves_dinner",
                    "reviews",
                    "geometry",
                    "business_status",
                    "geometry/viewport/northeast",
                ],
            )

            # Flatten and process data
            data = place_details.get("result", {})
            flat_data = flatten_dict(data)

            # Add random attributes
            flat_data["cardpayment"] = random.choice([True, False])
            flat_data["cashpayment"] = random.choice([True, False])
            flat_data["dog_friendly"] = random.choice([True, False])
            flat_data["laptop_friendly"] = random.choice([True, False])

            all_places.append(flat_data)

    elif link:
        # Extract Place ID from URL
        place_id = get_place_id(link)
        print(place_id)
        if place_id:
            # Fetch details using Place ID
            place_details = gmaps.place(
                place_id=place_id,
                fields=[
                    "geometry/location/lat",
                    "plus_code",
                    "current_opening_hours",
                    "geometry/viewport/northeast/lng",
                    "website",
                    "reservable",
                    "curbside_pickup",
                    "address_component",
                    "price_level",
                    "geometry/viewport/northeast/lat",
                    "type",
                    "geometry/location/lng",
                    "photo",
                    "rating",
                    "serves_breakfast",
                    "serves_vegetarian_food",
                    "editorial_summary",
                    "secondary_opening_hours",
                    "serves_lunch",
                    "place_id",
                    "url",
                    "geometry/viewport/southwest/lat",
                    "utc_offset",
                    "permanently_closed",
                    "geometry/viewport/southwest",
                    "takeout",
                    "delivery",
                    "dine_in",
                    "opening_hours",
                    "wheelchair_accessible_entrance",
                    "name",
                    "review",
                    "adr_address",
                    "formatted_address",
                    "serves_beer",
                    "formatted_phone_number",
                    "international_phone_number",
                    "serves_brunch",
                    "geometry/location",
                    "geometry/viewport/southwest/lng",
                    "user_ratings_total",
                    "geometry/viewport",
                    "serves_wine",
                    "icon",
                    "vicinity",
                    "serves_dinner",
                    "reviews",
                    "geometry",
                    "business_status",
                    "geometry/viewport/northeast",
                ],
            )

            # Flatten and process data
            data = place_details.get("result", {})
            flat_data = flatten_dict(data)

            # Add random attributes
            flat_data["cardpayment"] = random.choice([True, False])
            flat_data["cashpayment"] = random.choice([True, False])
            flat_data["dog_friendly"] = random.choice([True, False])
            flat_data["laptop_friendly"] = random.choice([True, False])

            all_places.append(flat_data)

    # Convert to DataFrame
    df_places = pd.DataFrame(all_places)
    return df_places
