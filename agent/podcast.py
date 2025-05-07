import dspy
from typing import Dict, Optional
from .lm import LMFactory
from .signatures import PodcastScriptGeneration
from .prompts import podcast_prompt_template


class PodcastScriptAgent:
    """
    Personalized podcast script generator combining news, weather, and analysis.

    Creates listener-adapted content with style-specific narration elements.
    """

    def __init__(
            self,
            provider: str = "openai",
            model_name: str = "gpt-4o",
    ):
        """
        Initialize podcast script agent.

        Args:
            provider: LLM service provider
            model_name: Model version/name
        """
        self.lm = LMFactory.get_model(provider, model_name)

    def _generate(self, signature, prompt_text: str) -> str:
        """Internal generation workflow"""
        generator = dspy.ChainOfThought(signature)
        response = generator(user_instructions=prompt_text, lm=self.lm)
        return response

    def generate_script(
            self,
            news_summary: str,
            weather: str,
            reflection: str,
            user_style: Optional[str] = None,
            length_minutes: int = 10
    ) -> str:
        """
        Generate personalized podcast script.

        Args:
            news_summary: Condensed news content
            weather: Formatted weather report
            reflection: Analytical commentary
            user_style: Preferred tone/style descriptors
            length_minutes: Target duration

        Returns:
            complete script
        """
        # Validate core content
        if not any([news_summary, reflection]):
            raise ValueError("Require at least news or analysis content")

        # Build generation prompt
        prompt_text = podcast_prompt_template(
            news_summary=news_summary,
            weather=weather,
            reflection=reflection,
            user_style=user_style
        )

        # Generate with DSPy components
        result = self._generate(PodcastScriptGeneration, prompt_text)

        # Post-processing
        # formatted_script = self._add_audio_cues(result.script)

        return result.script

    def _add_audio_cues(self, script: str) -> str:
        """Enhance raw script with production elements"""
        cues = [
            "\n[BACKGROUND MUSIC FADES IN]",
            "[PAUSE FOR EFFECT]",
            "[SOUND EFFECT: PAPER RUSTLING]"
        ]
        # Simple implementation - add cues at paragraph breaks
        for i, cue in enumerate(cues, 1):
            script = script.replace(f"\n\n", f"{cue}\n\n", i)
        return script