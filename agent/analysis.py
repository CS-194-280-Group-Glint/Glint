import dspy
from .lm import LMFactory
from .signatures import ImpactAnalysis, CriticalAnalysis, BackgroundAnalysis
from .prompts import (
    impact_analysis_prompt,
    critical_analysis_prompt,
    background_analysis_prompt,
)


class AnalysisAgent:
    """
    The Analysis Agent performs deeper analysis on summarized news content.

    It provides:
    - Impact analysis
    - Critical analysis
    - Background/context analysis

    Analysis can be personalized based on user interests and career.
    """

    def __init__(
        self,
        api_key: str,
        provider: str = "openai",
        model_name: str = "gpt-4o"
    ):
        """
        Initialize the analysis agent.

        Args:
            provider: The LLM provider (default: "openai")
            model_name: The model to use (default: "gpt-4o")
        """
        self.lm = LMFactory.get_model(provider, model_name, api_key=api_key)

    def generate(self, signature, prompt_text):
        """Internal method to generate analysis content using DSPy."""
        generator = dspy.ChainOfThought(signature)
        response = generator(user_instructions=prompt_text, lm=self.lm)
        return response

    def analyze_impact(self, summary: str, user_interests: list = None, user_career: str = None) -> str:
        """
        Analyze the impact and future implications of the news.

        Args:
            summary: The summarized news content.
            user_interests: List of user's interest categories.
            user_career: User's career or professional field.
        Returns:
            Impact analysis text.
        """
        if not summary or not summary.strip():
            return ""

        prompt_text = impact_analysis_prompt(summary, user_interests, user_career)
        result = self.generate(ImpactAnalysis, prompt_text)
        return result.impact_analysis

    def analyze_critical(self, summary: str, user_interests: list = None, user_career: str = None) -> str:
        """
        Critically analyze the news content.

        Args:
            summary: The summarized news content.
            user_interests: List of user's interest categories.
            user_career: User's career or professional field.

        Returns:
            Critical analysis text.
        """
        if not summary or not summary.strip():
            return ""

        prompt_text = critical_analysis_prompt(summary, user_interests, user_career)
        result = self.generate(CriticalAnalysis, prompt_text)
        return result.critical_analysis

    def analyze_background(self, summary: str, user_interests: list = None, user_career: str = None) -> str:
        """
        Provide background/context analysis of the news.

        Args:
            summary: The summarized news content.
            user_interests: List of user's interest categories.
            user_career: User's career or professional field.

        Returns:
            Background analysis text.
        """
        if not summary or not summary.strip():
            return ""

        prompt_text = background_analysis_prompt(summary, user_interests, user_career)
        result = self.generate(BackgroundAnalysis, prompt_text)
        return result.background_analysis

    def analyze_all(self, summary: str, user_interests: list = None, user_career: str = None) -> dict:
        """
        Perform all analysis tasks at once.

        Args:
            summary: The summarized news content.
            user_interests: List of user's interest categories.
            user_career: User's career or professional field.

        Returns:
            A dictionary containing three types of analysis.
        """
        return {
            "impact_analysis": self.analyze_impact(summary, user_interests, user_career),
            "critical_analysis": self.analyze_critical(summary, user_interests, user_career),
            "background_analysis": self.analyze_background(summary, user_interests, user_career),
        }
