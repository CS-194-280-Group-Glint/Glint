import requests
import json
import sys

def test_summary_endpoint(
    text, 
    max_length=None, 
    with_key_points=False, 
    bullet_format=False, 
    num_bullets=5,
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
        model: LLM model to use (optional)
    """
    # API endpoint URL
    url = "http://localhost:8000/api/summarize-text/"
    
    # Build request payload
    payload = {
        "text": text,
        "with_key_points": with_key_points,
        "bullet_format": bullet_format,
        "model": model
    }
    
    # Add optional parameters if provided
    if max_length:
        payload["max_length"] = max_length
    if bullet_format:
        payload["num_bullets"] = num_bullets
    
    print(f"Sending request to {url}...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Send POST request
        response = requests.post(url, json=payload)
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            
            # Print the results
            print("\nSummary Results:")
            print("=" * 50)
            
            if bullet_format:
                print("Bullet Summary:")
                for i, bullet in enumerate(result.get("bullet_summary", []), 1):
                    print(f"{i}. {bullet}")
            else:
                print("Summary:")
                print(result.get("summary", "No summary generated"))
                
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
    # Get text from command line argument or use sample text
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = """
        Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural 
        intelligence displayed by animals and humans. AI research has been defined as the field of study of 
        intelligent agents, which refers to any system that perceives its environment and takes actions that 
        maximize its chance of achieving its goals.

        The term "artificial intelligence" had previously been used to describe machines that mimic and display 
        "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". 
        This definition has since been rejected by major AI researchers who now describe AI in terms of rationality 
        and acting rationally, which does not limit how intelligence can be articulated.
        
        AI applications include advanced web search engines (e.g., Google), recommendation systems (used by YouTube, 
        Amazon, and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), 
        generative or creative tools (ChatGPT and AI art), automated decision-making, and competing at the highest 
        level in strategic game systems (such as chess and Go).
        """
    
    # Test the endpoint
    print("\n1. Standard summary:")
    test_summary_endpoint(text)
    
    print("\n2. Summary with key points:")
    test_summary_endpoint(text, with_key_points=True)
    
    print("\n3. Bullet point summary:")
    test_summary_endpoint(text, bullet_format=True, num_bullets=3) 