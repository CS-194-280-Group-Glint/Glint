import dspy
from typing import List

class SummarizeContent(dspy.Signature):
    """Signature for summarizing content."""
    user_instructions: str = dspy.InputField()
    summary: str = dspy.OutputField(desc="A concise summary that captures the key points")

class KeyPointsExtraction(dspy.Signature):
    """Signature for extracting key points from content."""
    user_instructions: str = dspy.InputField()
    key_points: List[str] = dspy.OutputField(desc="A list of 3-5 key points from the text")

class BulletPoints(dspy.Signature):
    """Signature for creating bullet points from content."""
    user_instructions: str = dspy.InputField()
    bullets: List[str] = dspy.OutputField(desc="A list of 3-5 bullet points")

class ImpactAnalysis(dspy.Signature):
    """Signature for analyzing the potential impact and future implications of the news."""
    user_instructions: str = dspy.InputField()
    impact_analysis: str = dspy.OutputField(desc="An analysis of the possible impact and future implications of the news")


class CriticalAnalysis(dspy.Signature):
    """Signature for critically analyzing the news content."""
    user_instructions: str = dspy.InputField()
    critical_analysis: str = dspy.OutputField(desc="A critical analysis of the news content, identifying biases or missing perspectives")


class BackgroundAnalysis(dspy.Signature):
    """Signature for providing background context of the news."""
    user_instructions: str = dspy.InputField()
    background_analysis: str = dspy.OutputField(desc="Relevant background information and context about the news")
