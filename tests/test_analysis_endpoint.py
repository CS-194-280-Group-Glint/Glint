import requests
import json
import sys

def test_analysis_endpoint(summary, model="gpt-4o"):
    """
    Test the analysis API endpoint by sending a POST request.
    
    Args:
        summary: The summarized news content to analyze
        model: LLM model to use (optional)
    """
    #API endpoint URL
    url = "http://localhost:8000/api/analyze-text/"
    
    #build request payload
    payload = {
        "summary": summary,
        "model": model
    }
    
    print(f"\nSending request to {url}...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        #send POST request
        response = requests.post(url, json=payload)
        
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
    
    #test the endpoint
    print("\nRunning Analysis Agent Test...")
    test_analysis_endpoint(summary)
