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
