# tts_services.py

from gtts import gTTS
import boto3
import os
import requests

def google_tts(text, output_path):
    tts = gTTS(text, lang="en")
    tts.save(output_path)

def amazon_polly_tts(text, output_path):
    polly_client = boto3.client('polly', region_name='us-east-1')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Matthew'
    )
    with open(output_path, 'wb') as file:
        file.write(response['AudioStream'].read())

def elevenlabs_tts(text, output_path):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = "your-voice-id"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {"text": text, "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"ElevenLabs API Error: {response.text}")

    with open(output_path, 'wb') as file:
        file.write(response.content)