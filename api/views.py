from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from agent.text_to_audio import TextToAudio
from agent.summary import SummaryAgent

# Create your views here.

@api_view(['POST'])
def text_to_speech(request):
    """
    Convert text to speech using OpenAI's TTS service.
    
    Expected payload:
    {
        "text": "Text to convert to speech",
        "voice": "nova",  # Optional
        "model": "tts-1",  # Optional
        "format": "mp3",   # Optional
        "speed": 1.0       # Optional
    }
    """
    # Get parameters from request
    text = request.data.get('text')
    if not text:
        return Response({'error': 'Text is required'}, status=400)
    
    voice = request.data.get('voice', 'nova')
    model = request.data.get('model', 'tts-1')
    format = request.data.get('format', 'mp3')
    speed = float(request.data.get('speed', 1.0))
    
    # Initialize TTS converter
    converter = TextToAudio(
        model=model,
        voice=voice,
    )
    
    # Convert text to speech
    try:
        output_file = converter.convert_to_temp_file(
            text=text,
            response_format=format,
            speed=speed,
        )
        
        # Return the audio file
        response = FileResponse(
            open(output_file, 'rb'),
            content_type=f'audio/{format}',
            as_attachment=True,
            filename=f'speech.{format}'
        )
        
        # Set header to delete the temp file after it's sent
        response['X-Accel-Buffering'] = 'no'
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    finally:
        # Clean up temp file
        if 'output_file' in locals() and os.path.exists(output_file):
            os.unlink(output_file)

@api_view(['POST'])
def summarize_text(request):
    """
    Summarize text using the SummaryAgent.
    
    Expected payload:
    {
        "text": "Text to summarize",
        "max_length": 200,          # Optional - max length in tokens
        "with_key_points": false,   # Optional - return key points as well
        "bullet_format": false,     # Optional - return summary as bullet points
        "num_bullets": 5,           # Optional - number of bullet points (if bullet_format is true)
        "model": "gpt-4o"           # Optional - model to use
    }
    """
    # Get parameters from request
    text = request.data.get('text')
    if not text:
        return Response({'error': 'Text is required'}, status=400)
    
    max_length = request.data.get('max_length')
    with_key_points = request.data.get('with_key_points', False)
    bullet_format = request.data.get('bullet_format', False)
    num_bullets = int(request.data.get('num_bullets', 5))
    model = request.data.get('model', 'gpt-4o')
    
    # Initialize summary agent
    agent = SummaryAgent(model_name=model)
    
    try:
        # Handle different summary formats
        if bullet_format:
            bullets = agent.bullet_summary(text, num_points=num_bullets)
            return Response({
                'bullet_summary': bullets
            })
        else:
            # Generate standard summary
            result = agent.summarize(
                text=text, 
                max_length=max_length,
                with_key_points=with_key_points
            )
            return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=500)