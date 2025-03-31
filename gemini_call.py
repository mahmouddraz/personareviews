from google import genai
from google.genai import types
import base64
from openai import OpenAI
import requests
import json


def convert_place_info(place_json):
  """
  Input `place_json`: a JSON file with place information + reviews
  Output: text
  """
  
  with open(place_json, 'r', encoding='utf-8') as file:
    data = json.load(file)  # Load JSON data into a Python object
  
  text_output = json.dumps(data, indent=4)
  
  return text_output


def compare_requirements_with_place_info(requirements=None, place_info=None):
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
  #return response.text


compare_requirements_with_place_info(requirements="dog-friendly, laptop friendly, cheap, serves a cappuccino", 
                                       place_info='result.json')


# gemini call outputs python dict 
# fix the hard coded place ID