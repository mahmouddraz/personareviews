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


# print(compare_requirements_with_place_info())

def query_perplexity(prompt, model="sonar", max_tokens=1024, temperature=0.0, api_key=None):
    """
    Function to send a query to the Perplexity AI API.
    
    Args:
        prompt (str): The query to send to the API
        model (str): The model to use for the query
        max_tokens (int): Maximum number of tokens to generate
        temperature (float): Controls randomness in the response
        api_key (str): Perplexity API key. If None, must be set in environment variables
    
    Returns:
        dict: The JSON response from the API
    """  # Replace with env var in production
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": model,
        "stream": False,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": "Be precise and concise in your responses."},
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post("https://api.perplexity.ai/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    
def test_perplexity_api():
    api_key = "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"
    prompt = ""
    
    try:
        response = query_perplexity(prompt=prompt, api_key=api_key)
        print("API Response:")
        print(f"Status: Success")
        if "choices" in response and len(response["choices"]) > 0:
            print(f"Response text: {response['choices'][0]['message']['content']}")
            return response['choices'][0]['message']['content']
        else:
            print(f"Full response: {response}")
            return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error occurred: {e}")
    

print(test_perplexity_api())