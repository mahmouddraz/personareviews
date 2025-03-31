import os
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel

def download_gcs_file(bucket_name, source_blob_name, destination_file_name):
    """Downloads a file from Google Cloud Storage."""
    storage_client = storage.Client(project="bliss-hack25fra-9533")
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)
    
    blob.download_to_filename(destination_file_name)

    print(f"File {source_blob_name} downloaded to {destination_file_name}.")


if __name__ == "__main__":
    # Initialize Vertex AI
    vertexai.init(project="bliss-hack25fra-9533", location="us-central1")
    
    # Parse the GCS URI
    gcs_uri = "gs://cloud-samples-data/generative-ai/audio/pixel.mp3"
    bucket_name = gcs_uri.split('/')[2]
    source_blob_name = '/'.join(gcs_uri.split('/')[3:])
    
    # Set the local destination for the file
    destination_file_name = "pixel.mp3"
    
    # Download the file
    download_gcs_file(bucket_name, source_blob_name, destination_file_name)