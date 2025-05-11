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

logger = logging.getLogger(__name__)


def podcast(request):
    # if request.method != 'POST':
    #     return JsonResponse({'error': 'Method not allowed'}, status=405)
    # data = json.loads(request.body)
    # category = data.get('category')
    # style = data.get('style')
    # career = data.get('career')
    # voice = data.get('voice', "nova")
    # speed = data.get('speed', 1.0)
    # audio = generate_podcast(category=category, style=style, career=career, voice=voice, speed=speed)
    # if not audio["result"]:
    #     return JsonResponse({'error': audio["error"]}, status=404)
    # path = audio["data"].replace("static/", "")
    # context = {
    #     'audio_file': path
    # }
    # return render(request, 'test.html', context)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)
    category = data.get('category', [])
    style = data.get('style', 'casual')
    career = data.get('career', 'student')
    voice = data.get('voice', 'nova')
    speed = data.get('speed', 1.0)

    audio = generate_podcast(category=category, style=style, career=career, voice=voice, speed=speed)

    if not audio["result"]:
        return JsonResponse({'error': audio["error"]}, status=404)
    
    path = audio["data"]
    context = {'audio_file': path}

    return render(request, 'test.html', context)

def index(request):
    return render(request, 'index.html')


def generate_podcast(
        category: list,
        style: str,
        career: str,
        voice: str = "nova",
        speed: float = 1.0
) -> Dict:
    all_news = []
    for c in category:
        all_news.append(get_top_news(api_key=settings.NEWS_API_KEY, category=c, page_size=5))
    summary = summarize_text(str(all_news))
    if not summary["result"]:
        return {"result": False, "error": summary["error"]}
    summary = str(summary["data"])
    analysis = analyze_text(summary)
    if not analysis["result"]:
        return {"result": False, "error": analysis["error"]}
    analysis = analysis["data"]

    # 要加一个获取当前时间+天气 连成字符串的function call

    script = write_script(news_summary=summary,
                          weather="",
                          reflection=str(analysis),
                          user_style=style)
    if not script["result"]:
        return {"result": False, "error": script["error"]}
    script = script["data"]
    audio = text_to_speech(text=script,
                           speed=speed,
                           voice=voice)
    if not audio["result"]:
        return {"result": False, "error": audio["error"]}
    return {"result": True, "data": audio["data"]}


def text_to_speech(
        text: str,
        voice: str = "nova",
        model: str = "tts-1",
        speed: float = 1.0,
        output_dir: str = "static/audio"
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
        converter = TextToAudio(api_key=settings.OPENAI_API_KEY, model=model, voice=voice)
        converter.convert(text=text, output_path=rel_path, speed=speed)

        return {"result": True, "data": rel_path}

    except Exception as e:
        return {"result": False, "error": f"Conversion failed: {str(e)}"}


def summarize_text(
        text: str,
        max_length: Optional[int] = None,
        with_key_points: bool = False,
        bullet_format: bool = False,
        num_bullets: int = 5,
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
        model: Model to use

    Returns:
        Dictionary with results or error message
    """
    if not text.strip():
        return {"result": False, 'error': 'Text is required'}

    agent = SummaryAgent(model_name=model)

    try:
        if bullet_format:
            bullets = agent.bullet_summary(text, num_points=num_bullets)
            return {'bullet_summary': bullets}
        else:
            result = agent.summarize(
                text=text,
                max_length=max_length,
                with_key_points=with_key_points
            )
            return {'result': True, 'data': result}
    except Exception as e:
        return {"result": False, 'error': str(e)}


def analyze_text(
        summary: str,
        model: str = "gpt-4o"
) -> Dict:
    """
    Analyze news using the AnalysisAgent

    Args:
        summary: The summarized news content
        model: Model to use

    Returns:
        Dictionary with analysis results or error message
    """
    if not summary.strip():
        return {"result": False, 'error': 'Summary is required'}

    agent = AnalysisAgent(model_name=model)

    try:
        result = agent.analyze_all(summary)
        return {'result': True, 'data': result}
    except Exception as e:
        return {"result": False, 'error': str(e)}


def write_script(
        news_summary: str,
        weather: str,
        reflection: str,
        user_style: Optional[str] = None,
        length_minutes: int = 10
) -> Dict:
    agent = PodcastScriptAgent()

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
