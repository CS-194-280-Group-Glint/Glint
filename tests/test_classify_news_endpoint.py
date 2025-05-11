import requests
import json
import sys

def test_classify_news_endpoint(
    news_list,
    user_interests=None,
    user_career=None,
    model="gpt-4o"
):
    """
    Test the news classification API endpoint by sending a POST request.
    
    Args:
        news_list: List of news articles to process
        user_interests: List of user's interest categories (optional)
        user_career: User's career or professional field (optional)
        model: LLM model to use (optional)
    """
    # API endpoint URL
    url = "http://localhost:8000/api/classify-news/"
    
    # Build request payload
    payload = {
        "news_list": news_list,
        "model": model
    }
    
    # Add personalization parameters if provided
    if user_interests:
        payload["user_interests"] = user_interests
    if user_career:
        payload["user_career"] = user_career
    
    # Set headers to exempt from CSRF
    headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    print(f"\nSending request to {url}...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Send POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            
            # Print the results
            print("\nNews Classification Results:")
            print("=" * 50)
            
            print("Important News:")
            print(result.get("important", "No important news generated."))
            
            print("\nWorth Mentioning:")
            print(result.get("mention", "No worth mentioning news generated."))
            
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
    # Sample news for testing
    sample_news = [
        "Tesla has announced a major breakthrough in artificial intelligence for self-driving cars. The new AI system, which will be rolled out in the next software update, uses advanced neural networks to better recognize pedestrians, cyclists, and other vehicles in complex urban environments. The company claims this will reduce accident rates by up to 30% compared to previous systems.",
        
        "Apple's quarterly earnings report showed a 15% increase in revenue, driven primarily by strong iPhone sales in emerging markets. The company also announced plans to increase its stock buyback program.",
        
        "A minor earthquake measuring 3.2 on the Richter scale was detected near San Francisco. No damage or injuries were reported.",
        
        "Scientists have discovered a new species of deep-sea fish that can survive at extreme depths. The fish has unique adaptations that allow it to withstand incredible pressure and cold temperatures.",
        
        "Local weather forecasts predict scattered showers throughout the weekend, with temperatures remaining in the mid-70s."
    ]
    
    # Example of user interests and career for testing
    user_interests = ["technology", "science"]
    user_career = "software engineer"
    
    # Test with personalization
    print("\nRunning News Classification Test with personalization...")
    test_classify_news_endpoint(sample_news, user_interests, user_career) 