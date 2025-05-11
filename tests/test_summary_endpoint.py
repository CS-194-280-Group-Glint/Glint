import requests
import json
import sys

def test_summary_endpoint(
    text, 
    max_length=None, 
    with_key_points=False, 
    bullet_format=False, 
    num_bullets=5,
    content_type="general",
    user_interests=None,
    user_career=None,
    model="gpt-4o"
):
    """
    Test the summary API endpoint by sending a POST request.
    
    Args:
        text: Text to summarize
        max_length: Maximum length of summary (optional)
        with_key_points: Whether to include key points (optional)
        bullet_format: Whether to return summary as bullets (optional)
        num_bullets: Number of bullet points (optional)
        content_type: Type of content being summarized (optional)
        user_interests: List of user's interest categories (optional)
        user_career: User's career or professional field (optional)
        model: LLM model to use (optional)
    """
    # API endpoint URL
    url = "http://localhost:8000/api/summarize-text/"
    
    # Build request payload
    payload = {
        "text": text,
        "with_key_points": with_key_points,
        "bullet_format": bullet_format,
        "content_type": content_type,
        "model": model
    }
    
    # Add optional parameters if provided
    if max_length:
        payload["max_length"] = max_length
    if bullet_format:
        payload["num_bullets"] = num_bullets
    if user_interests:
        payload["user_interests"] = user_interests
    if user_career:
        payload["user_career"] = user_career
    
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
            result = response.json()
            
            # Print the results
            print("\nSummary Results:")
            print("=" * 50)
            
            if bullet_format:
                print("Bullet Summary:")
                bullets = result if isinstance(result, list) else []
                for i, bullet in enumerate(bullets, 1):
                    print(f"{i}. {bullet}")
            else:
                print("Summary:")
                summary = result.get("summary", "No summary generated")
                print(summary)
                
                if with_key_points and "key_points" in result:
                    print("\nKey Points:")
                    for point in result["key_points"]:
                        print(f"- {point}")
            
            return result
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.ConnectionError:
        print("Connection error. Make sure the Django server is running.")
        print("Start the server with: python manage.py runserver")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = """
        Tesla has announced a major breakthrough in artificial intelligence for self-driving cars. 
        The new AI system, which will be rolled out in the next software update, uses advanced 
        neural networks to better recognize pedestrians, cyclists, and other vehicles in complex 
        urban environments. The company claims this will reduce accident rates by up to 30% compared 
        to previous systems. Industry analysts predict this could accelerate the adoption of 
        self-driving technology across the automotive sector. Tesla stock rose 10% on the announcement.
        """
    
    # Example of user interests and career for testing
    user_interests = ["technology", "automotive"]
    user_career = "software engineer"
    
    # Test with personalization
    print("\nRunning Summary Agent Test with personalization...")
    test_summary_endpoint(text, user_interests=user_interests, user_career=user_career) 