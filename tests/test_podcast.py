import requests
import json


def test_podcast_endpoint(
        category,
        style,
        voice,
        speed
):
    # API endpoint URL
    url = "http://localhost:8000/api/generate-podcast/"

    # Build request payload
    payload = {
        "category": category,
        "style": style,
        "voice": voice,
        "speed": speed
    }
    
    # Set headers to exempt from CSRF
    headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }

    print(f"Sending request to {url}...")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        # Send POST request
        response = requests.post(url, json=payload, headers=headers)

        # Check if request was successful
        if response.status_code == 200:
            result = response.content.decode('utf-8')

            # Print the results
            print("\nRequest Results:")
            print("=" * 50)
            print(result)

        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.ConnectionError:
        print("Connection error. Make sure the Django server is running.")
        print("Start the server with: python manage.py runserver")
        return None


if __name__ == "__main__":
    test_podcast_endpoint(["business", "technology"], "relaxed", "nova", 1.0)
