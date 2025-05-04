from django.shortcuts import render
from django.http import JsonResponse
import json
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def podcast(request):
    return render(request, 'podcast.html')

def save_preferences(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            preferences = data.get('preferences', [])
            
            logger.info(f"Save Preferences: {preferences}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Preferences saved', 
                'preferences': preferences
            })
            
        except Exception as e:
            logger.error(f"Failed to save preferences: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Request failed. Please try again.: {str(e)}'
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST requests are allowed'
    }, status=405)