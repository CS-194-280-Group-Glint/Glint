import requests
import os
import sys
import json
from pathlib import Path

def test_tts_endpoint(text, output_file="api_response.mp3", voice="nova", model="tts-1", format="mp3", speed=1.0):
    """
    Test the text-to-speech API endpoint by sending a POST request.
    
    Args:
        text: Text to convert to speech
        output_file: Path to save the audio file
        voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        model: Model to use (tts-1, tts-1-hd)
        format: Audio format (mp3, opus, aac, flac)
        speed: Speed of the audio (0.25 to 4.0)
    """
    # API endpoint URL
    url = "http://localhost:8000/api/text-to-speech/"
    
    # Request payload
    payload = {
        "text": text,
        "voice": voice,
        "model": model,
        "format": format,
        "speed": speed
    }
    
    print(f"Sending request to {url}...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Send POST request
        response = requests.post(url, json=payload)
        
        # Check if request was successful
        if response.status_code == 200:
            # Save the audio file
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            print(f"Audio file saved to: {output_file}")
            return True
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return False
    except requests.exceptions.ConnectionError:
        print("Connection error. Make sure the Django server is running.")
        print("Start the server with: python manage.py runserver")
        return False

if __name__ == "__main__":
    # Get text from command line argument or use default
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "This is a test of the text to speech API endpoint."
    
    # Test the endpoint
    test_tts_endpoint(text) 