import requests
import json
import sys

def test_analysis_endpoint(summary, user_interests=None, user_career=None, model="gpt-4o"):
    """
    Test the analysis API endpoint by sending a POST request.
    
    Args:
        summary: The summarized news content to analyze
        user_interests: List of user's interest categories (optional)
        user_career: User's career or professional field (optional)
        model: LLM model to use (optional)
    """
    #API endpoint URL
    url = "http://localhost:8000/api/analyze-text/"
    
    #build request payload
    payload = {
        "summary": summary,
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
        #send POST request
        response = requests.post(url, json=payload, headers=headers)
        
        #check if request was successful
        if response.status_code == 200:
            result = response.json()
            
            #print the results
            print("\nAnalysis Results:")
            print("=" * 50)
            print("Impact Analysis:")
            print(result.get("impact_analysis", "No impact analysis generated."))
            
            print("\nCritical Analysis:")
            print(result.get("critical_analysis", "No critical analysis generated."))
            
            print("\nBackground Analysis:")
            print(result.get("background_analysis", "No background analysis generated."))
            
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
        summary = " ".join(sys.argv[1:])
    else:
        summary = """
        """
    
    # Example of user interests and career for testing
    user_interests = ["technology", "business"]
    user_career = "software engineer"
    
    #test the endpoint
    print("\nRunning Analysis Agent Test...")
    test_analysis_endpoint(summary, user_interests, user_career)
