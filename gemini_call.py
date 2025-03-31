from google import genai
from google.genai import types
import base64
from openai import OpenAI
import requests


def compare_requirements_with_place_info(requirements=None, place_info=None):
  client = genai.Client(
    vertexai=True,
    project="bliss-hack25fra-9533",
    location="us-central1",
  )

  text1 = types.Part.from_text(text="""You are an expert Translator. You are tasked to translate documents from en to fr.Please provide an accurate translation of this document and return translation text only:""")

  model = "gemini-2.0-flash-lite-001"
  contents = [
    types.Content(
      role="user",
      parts=[
        text1
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
  return response.text


