import google.genai as genai

def generate(audio_bytes):
    client = genai.Client(
        vertexai=True,
        project="bliss-hack25fra-9533",
        location="us-central1",
    )

    # Create a Part object from the audio bytes
    audio_part = genai.types.Part.from_bytes(
        data=audio_bytes,
        mime_type="audio/mpeg",
    )

    model = "gemini-2.0-flash-001"
    contents = [
        genai.types.Content(
            role="user",
            parts=[
                genai.types.Part.from_text(
                    text="Please analyze this audio file and summarize the contents of the audio as bullet points."
                ),
                audio_part,
            ],
        )
    ]
    generate_content_config = genai.types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        safety_settings=[
            genai.types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ),
            genai.types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ),
            genai.types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ),
            genai.types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            ),
        ],
    )

    text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")
    
        text += chunk.text
    return text
