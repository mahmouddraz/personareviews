from google import genai
import base64
from google.cloud import storage

def upload_to_gcs(local_file_path, bucket_name="bliss-hack25fra-9533"):
  """Upload a local file to Google Cloud Storage and return the gs:// URI."""
  storage_client = storage.Client(project=bucket_name)
  
  # Create the bucket if it doesn't exist
  bucket = storage_client.bucket(bucket_name)
  if not bucket.exists():
    bucket.create()
  
  # Extract just the filename from the path
  blob_name = local_file_path.split('/')[-1]
  blob = bucket.blob(f"audio/{blob_name}")
  
  # Upload the file
  blob.upload_from_filename(local_file_path)
  
  # Return the gs:// URI
  return f"gs://{bucket_name}/audio/{blob_name}"

def clean_bucket(bucket_name="bliss-hack25fra-9533", prefix="audio/"):
  """Delete all objects in a GCS bucket with the given prefix."""
  storage_client = storage.Client(project=bucket_name)
  bucket = storage_client.bucket(bucket_name)
  
  # Check if bucket exists first
  if not bucket.exists():
    print(f"Bucket {bucket_name} does not exist.")
    return
  
  blobs = bucket.list_blobs(prefix=prefix)
  deleted_count = 0
  
  for blob in blobs:
    blob.delete()
    deleted_count += 1
  
  print(f"Deleted {deleted_count} files from {bucket_name}/{prefix}")

def generate(local_audio_path):
  # Upload the local audio file to GCS

  file_uri = upload_to_gcs(local_audio_path)
  print(f"Uploaded to: {file_uri}")
  
  client = genai.Client(
    vertexai=True,
    project="bliss-hack25fra-9533",
    location="us-central1",
  )

  audio1 = genai.types.Part.from_uri(
    file_uri=file_uri,
    mime_type="audio/mpeg",
  )

  model = "gemini-2.0-flash-001"
  contents = [
    genai.types.Content(
    role="user",
    parts=[
      genai.types.Part.from_text(text="""Please analyze this audio file and summarize the contents of the audio as bullet points."""),
      audio1
    ]
    )
  ]
  generate_content_config = genai.types.GenerateContentConfig(
    temperature = 0.2,
    max_output_tokens = 8192,
    response_modalities = ["TEXT"],
    safety_settings = [genai.types.SafetySetting(
    category="HARM_CATEGORY_HATE_SPEECH",
    threshold="OFF"
    ),genai.types.SafetySetting(
    category="HARM_CATEGORY_DANGEROUS_CONTENT",
    threshold="OFF"
    ),genai.types.SafetySetting(
    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
    threshold="OFF"
    ),genai.types.SafetySetting(
    category="HARM_CATEGORY_HARASSMENT",
    threshold="OFF"
    )],
  )
  text = ""
  for chunk in client.models.generate_content_stream(
    model = model,
    contents = contents,
    config = generate_content_config,
    ):
    text = text + chunk.text
  return text
# local_audio_path = "/Users/davidzumaquero/GitHub/mody/audio/short-audio-sample-10s.mp3"
# generate(local_audio_path)
