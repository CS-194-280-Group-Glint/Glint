from agent.text_to_audio import TextToAudio
import os

def main():
    """
    Example usage of the TextToAudio class.
    
    Make sure to set your OpenAI API key as an environment variable:
    export OPENAI_API_KEY=your_api_key_here
    """
    # Initialize the TextToAudio converter with default settings
    converter = TextToAudio()
    
    # Text to convert
    text = "Hello! This is an example of text-to-speech using OpenAI's TTS model. I can be an agent that can be used to generate audio from text."
    
    # Save to a file
    output_path = "example_output.mp3"
    print(f"Converting text to speech and saving to {output_path}...")
    
    file_path = converter.convert(
        text=text,
        output_path=output_path,
        # Optional parameters:
        # response_format="mp3",  # Options: "mp3", "opus", "aac", "flac"
        # speed=1.0,              # Speed between 0.25 and 4.0
    )
    
    print(f"File saved to: {file_path}")
    
    # You can also try different voices
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    for voice in voices:
        print(f"Converting with voice: {voice}")
        voice_file = f"example_{voice}.mp3"
        
        voice_converter = TextToAudio(voice=voice)
        voice_converter.convert(
            text=f"This is the {voice} voice from OpenAI's text to speech API.",
            output_path=voice_file,
        )
        
        print(f"Saved {voice} sample to: {voice_file}")
        
    print("\nAll done! Check the generated audio files.")

if __name__ == "__main__":
    main() 