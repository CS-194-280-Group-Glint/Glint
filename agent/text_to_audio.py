import tempfile
from pathlib import Path
from openai import OpenAI
from typing import Optional, Literal, Union


class TextToAudio:
    """A class that converts text to audio using OpenAI's TTS models."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Literal["tts-1", "tts-1-hd"] = "tts-1",
        voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = "nova",
    ):
        """
        Initialize the TextToAudio converter.
        
        Args:
            api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
            model: The TTS model to use. Options are "tts-1" (faster, standard quality) 
                  or "tts-1-hd" (higher quality).
            voice: The voice to use. Options are "alloy", "echo", "fable", "onyx", 
                  "nova", or "shimmer".
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.voice = voice
    
    def convert(
        self,
        text: str,
        output_path: Optional[Union[str, Path]] = None,
        response_format: Literal["mp3", "opus", "aac", "flac"] = "mp3",
        speed: float = 1.0,
    ) -> Union[str, bytes]:
        """
        Convert text to audio.
        
        Args:
            text: The text to convert to audio
            output_path: Path to save the audio file. If None, returns the audio as bytes.
            response_format: Audio format. Options are "mp3", "opus", "aac", or "flac".
            speed: Speed of the audio. Must be between 0.25 and 4.0.
            
        Returns:
            If output_path is provided, returns the path to the saved file.
            Otherwise, returns the audio data as bytes.
        """
        if not 0.25 <= speed <= 4.0:
            raise ValueError("Speed must be between 0.25 and 4.0")
        
        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text,
            response_format=response_format,
            speed=speed,
        )
        
        if output_path:
            output_path = Path(output_path)
            
            # Make sure the extension matches the response format
            if output_path.suffix[1:] != response_format:
                output_path = output_path.with_suffix(f".{response_format}")
                
            # Create directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save to file
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            return str(output_path)
        
        return response.content
    
    def convert_to_temp_file(
        self,
        text: str,
        response_format: Literal["mp3", "opus", "aac", "flac"] = "mp3",
        speed: float = 1.0,
    ) -> str:
        """
        Convert text to audio and save to a temporary file.
        
        Args:
            text: The text to convert to audio
            response_format: Audio format. Options are "mp3", "opus", "aac", or "flac".
            speed: Speed of the audio. Must be between 0.25 and 4.0.
            
        Returns:
            Path to the temporary file.
        """
        # Create a temporary file with the appropriate extension
        temp_file = tempfile.NamedTemporaryFile(
            suffix=f".{response_format}", delete=False
        )
        temp_file.close()
        
        # Convert and save
        return self.convert(
            text=text,
            output_path=temp_file.name,
            response_format=response_format,
            speed=speed,
        )
