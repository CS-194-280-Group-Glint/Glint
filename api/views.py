import datetime
from typing import Dict, Optional
from django.conf import settings
from agent.text_to_audio import TextToAudio
from agent.summary import SummaryAgent
from agent.analysis import AnalysisAgent
from agent.podcast import PodcastScriptAgent
from agent.news import get_top_news

from django.shortcuts import render
from django.http import JsonResponse
from pathlib import Path
import json
import logging
import uuid
import traceback
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@csrf_exempt
def podcast(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)
    category = data.get('category', [])
    style = data.get('style', 'casual')
    career = data.get('career', 'student')
    voice = data.get('voice', 'nova')
    speed = data.get('speed', 1.0)
    model = data.get('model', 'gpt-4o')
    news_api_key = data.get('newsapi') or settings.NEWS_API_KEY
    openai_api_key = data.get('modelapi') or settings.OPENAI_API_KEY

    audio = generate_podcast(category=category,
                             style=style,
                             career=career,
                             voice=voice,
                             speed=speed,
                             model=model,
                             news_api_key=news_api_key,
                             openai_api_key=openai_api_key)

    if not audio["result"]:
        return JsonResponse({'error': audio["error"]}, status=404)

    path = audio["data"]
    context = {'audio_file': path}

    return render(request, 'test.html', context)


def index(request):
    return render(request, 'index.html')


def generate_podcast(
        news_api_key: str,
        openai_api_key: str,
        category: list,
        style: str,
        career: str,
        voice: str = "nova",
        speed: float = 1.0,
        model: str = "gpt-4o",
) -> Dict:
    all_news = []
    for c in category:
        all_news.append(get_top_news(api_key=news_api_key, category=c, page_size=5))

    # Use the new classify_news function to split important and worth mentioning news
    news_classification = classify_news(api_key=openai_api_key, news_list=all_news, user_interests=category,
                                        user_career=career)

    if not news_classification["result"]:
        return {"result": False, "error": news_classification["error"]}

    classified_news = news_classification["data"]
    important_news = classified_news["important"]
    mention_news = classified_news["mention"]

    # Create a combined news summary with clearly marked sections
    combined_summary = f"Important News:\n{important_news}\n\nWorth Mentioning:\n{mention_news}"

    # Pass user interests and career for personalized analysis
    analysis = analyze_text(combined_summary, user_interests=category, user_career=career, api_key=openai_api_key)
    if not analysis["result"]:
        return {"result": False, "error": analysis["error"]}

    analysis = analysis["data"]

    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M")

    script = write_script(news_summary=combined_summary,
                          weather=time_str,
                          reflection=str(analysis),
                          user_style=style,
                          api_key=openai_api_key)
    if not script["result"]:
        return {"result": False, "error": script["error"]}

    script = script["data"]
    audio = text_to_speech(text=script,
                           speed=speed,
                           voice=voice,
                           api_key=openai_api_key)
    if not audio["result"]:
        return {"result": False, "error": audio["error"]}
    return {"result": True, "data": audio["data"]}


def text_to_speech(
        text: str,
        voice: str = "nova",
        model: str = "tts-1",
        speed: float = 1.0,
        output_dir: str = "static/audio",
        api_key: Optional[str] = None
) -> Dict:
    """
    Convert text to speech and return result dictionary

    Args:
        text: Input text to synthesize
        voice: Voice style (default: 'nova')
        model: TTS model version (default: 'tts-1')
        speed: Speech speed ratio (0.25-4.0)
        output_dir: Output directory path (default: 'tts_output')

    Returns:
        dict: {'result': True, 'path': str} or {'result': False, 'error': str}

    Example:
        text_to_speech("Hello world")
        {'result': True, 'path': 'tts_output/9f86d081.mp3'}
    """
    # Validate input parameters
    if not text.strip():
        return {"result": False, "error": "Text is required"}

    if not 0.25 <= speed <= 4.0:
        return {"result": False, "error": "Speed must be between 0.25 and 4.0"}

    try:
        # Create output directory
        output_path = Path(output_dir)

        # Generate unique filename
        file_name = f"{uuid.uuid4().hex[:8]}.mp3"
        rel_path = str(output_path / file_name)

        # Initialize and convert
        converter = TextToAudio(api_key=api_key, model=model, voice=voice)
        converter.convert(text=text, output_path=rel_path, speed=speed)

        return {"result": True, "data": rel_path}

    except Exception as e:
        return {"result": False, "error": f"Conversion failed: {str(e)}"}


def summarize_text(
        text: str,
        api_key: str,
        max_length: Optional[int] = None,
        with_key_points: bool = False,
        bullet_format: bool = False,
        num_bullets: int = 5,
        content_type: str = "general",
        user_interests: list = None,
        user_career: str = None,
        model: str = "gpt-4o"
) -> Dict:
    """
    Summarize text using the SummaryAgent

    Args:
        text: Text to summarize
        max_length: Optional max length in tokens
        with_key_points: Return key points as well
        bullet_format: Return summary as bullet points
        num_bullets: Number of bullet points (if bullet_format)
        content_type: Type of content being summarized
        user_interests: List of user's interest categories
        user_career: User's career or professional field
        model: Model to use

    Returns:
        Dictionary with results or error message
    """
    if not text.strip():
        return {"result": False, 'error': 'Text is required'}

    agent = SummaryAgent(api_key=api_key, model_name=model)

    try:
        if bullet_format:
            bullets = agent.bullet_summary(
                text,
                num_points=num_bullets,
                content_type=content_type,
                user_interests=user_interests,
                user_career=user_career
            )
            return {'result': True, 'data': bullets}
        else:
            result = agent.summarize(
                text=text,
                max_length=max_length,
                with_key_points=with_key_points,
                content_type=content_type,
                user_interests=user_interests,
                user_career=user_career
            )
            return {'result': True, 'data': result}
    except Exception as e:
        return {"result": False, 'error': str(e)}


def analyze_text(
        summary: str,
        api_key: str,
        user_interests: list = None,
        user_career: str = None,
        model: str = "gpt-4o"
) -> Dict:
    """
    Analyze news using the AnalysisAgent

    Args:
        summary: The summarized news content
        user_interests: List of user's interest categories
        user_career: User's career or professional field
        model: Model to use

    Returns:
        Dictionary with analysis results or error message
    """
    if not summary.strip():
        return {"result": False, 'error': 'Summary is required'}

    agent = AnalysisAgent(api_key=api_key, model_name=model)

    try:
        result = agent.analyze_all(summary, user_interests, user_career)
        return {'result': True, 'data': result}
    except Exception as e:
        return {"result": False, 'error': str(e)}


def write_script(
        api_key: str,
        news_summary: str,
        weather: str,
        reflection: str,
        user_style: Optional[str] = None,
        length_minutes: int = 10
) -> Dict:
    agent = PodcastScriptAgent(api_key=api_key)

    try:
        script = agent.generate_script(
            news_summary=news_summary,
            weather=weather,
            reflection=reflection,
            user_style=user_style,
            length_minutes=length_minutes
        )
        return {'result': True, 'data': script}
    except Exception as e:
        return {"result": False, 'error': str(e)}


@csrf_exempt
def analyze_text_endpoint(request):
    """
    API endpoint for text analysis.
    Accepts POST requests with JSON data.
    
    Expected JSON format:
    {
        "summary": "Text to analyze",
        "user_interests": ["category1", "category2", ...], (optional)
        "user_career": "user's profession", (optional)
        "model": "gpt-4o" (optional)
    }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        summary = data.get('summary', '')
        user_interests = data.get('user_interests', None)
        user_career = data.get('user_career', None)
        model = data.get('model', 'gpt-4o')

        if not summary:
            return JsonResponse({'error': 'Summary text is required'}, status=400)

        result = analyze_text(
            summary=summary,
            user_interests=user_interests,
            user_career=user_career,
            model=model
        )

        if result['result']:
            return JsonResponse(result['data'], status=200)
        else:
            return JsonResponse({'error': result['error']}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def summarize_text_endpoint(request):
    """
    API endpoint for text summarization.
    Accepts POST requests with JSON data.
    
    Expected JSON format:
    {
        "text": "Text to summarize",
        "max_length": 150, (optional)
        "with_key_points": false, (optional)
        "bullet_format": false, (optional)
        "num_bullets": 5, (optional)
        "content_type": "general", (optional)
        "user_interests": ["category1", "category2", ...], (optional)
        "user_career": "user's profession", (optional)
        "model": "gpt-4o" (optional)
    }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        max_length = data.get('max_length')
        with_key_points = data.get('with_key_points', False)
        bullet_format = data.get('bullet_format', False)
        num_bullets = data.get('num_bullets', 5)
        content_type = data.get('content_type', 'general')
        user_interests = data.get('user_interests')
        user_career = data.get('user_career')
        model = data.get('model', 'gpt-4o')
        openai_api_key = data.get('modelapi') or settings.OPENAI_API_KEY

        if not text:
            return JsonResponse({'error': 'Text is required'}, status=400)

        result = summarize_text(
            text=text,
            max_length=max_length,
            with_key_points=with_key_points,
            bullet_format=bullet_format,
            num_bullets=num_bullets,
            content_type=content_type,
            user_interests=user_interests,
            user_career=user_career,
            model=model,
            api_key=openai_api_key
        )

        if result['result']:
            return JsonResponse(result['data'], status=200)
        else:
            return JsonResponse({'error': result['error']}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def classify_news(
        api_key: str,
        news_list: list,
        user_interests: list = None,
        user_career: str = None,
        model: str = "gpt-4o"
) -> Dict:
    """
    Classify and summarize a list of news articles into important and worth mentioning categories.

    Args:
        news_list: List of news articles to process
        user_interests: List of user's interest categories
        user_career: User's career or professional field
        model: Model to use

    Returns:
        Dictionary with classification results or error message
    """
    if not news_list or len(news_list) == 0:
        return {"result": False, 'error': 'News list is empty'}

    agent = SummaryAgent(model_name=model, api_key=api_key)

    try:
        result = agent.classify_and_summarize_news(
            news_list=news_list,
            user_interests=user_interests,
            user_career=user_career
        )
        return {'result': True, 'data': result}
    except Exception as e:
        return {"result": False, 'error': str(e)}


@csrf_exempt
def classify_news_endpoint(request):
    """
    API endpoint for news classification and summarization.
    Accepts POST requests with JSON data.
    
    Expected JSON format:
    {
        "news_list": ["news1", "news2", ...],
        "user_interests": ["category1", "category2", ...], (optional)
        "user_career": "user's profession", (optional)
        "model": "gpt-4o" (optional)
    }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        news_list = data.get('news_list', [])
        user_interests = data.get('user_interests')
        user_career = data.get('user_career')
        model = data.get('model', 'gpt-4o')

        if not news_list:
            return JsonResponse({'error': 'News list is required'}, status=400)

        result = classify_news(
            news_list=news_list,
            user_interests=user_interests,
            user_career=user_career,
            model=model
        )

        if result['result']:
            return JsonResponse(result['data'], status=200)
        else:
            return JsonResponse({'error': result['error']}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
