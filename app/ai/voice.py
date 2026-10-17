from groq import Groq
from app.core.config import settings
import os

# Initialize the Groq client
client = Groq(api_key = settings.GROQ_API_KEY)

# Specify the path to the audio file

def audio_text(filename: str):
    # Open the audio file
    with open(filename, "rb") as file:

        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(

        file=file, # Required audio file
        model="whisper-large-v3-turbo", # Required model to use for transcription
        prompt="Specify context or spelling",  # Optional
        language="en",  # Optional
        temperature=1.0  # Optional

        )

        # To print only the transcription text, you'd use print(transcription.text) (here we're printing the entire transcription object to access timestamps)
        print(transcription.text)



