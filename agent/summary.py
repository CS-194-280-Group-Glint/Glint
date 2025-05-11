import dspy
from typing import Optional, List, Dict, Any
from .lm import LMFactory
from .signatures import SummarizeContent, KeyPointsExtraction, BulletPoints, NewsClassification
from .prompts import summarize_prompt, bullet_summary_prompt, key_points_extraction_prompt, news_classification_prompt

class SummaryAgent:
    """
    The Summary Agent condenses content, prioritizing key points.
    
    This agent uses DSPy to create summaries that maintain the core 
    message while reducing length.
    
    Summaries can be personalized based on user interests and career.
    """
    
    def __init__(
        self,
        provider: str = "openai",
        model_name: str = "gpt-4o",
    ):
        """
        Initialize the summary agent.
        
        Args:
            provider: The LLM provider (e.g., "openai")
            model_name: The model to use (e.g., "gpt-4o", "o1-mini")
        """
        # Get the language model but don't try to globally configure DSPy
        self.lm = LMFactory.get_model(provider, model_name)
        
    def generate(self, signature, prompt_text):
        """Internal method to generate content using DSPy with explicit LM."""
        generator = dspy.ChainOfThought(signature)
        # Set the specific language model for this prediction
        response = generator(user_instructions=prompt_text, lm=self.lm)
        return response
        
    def summarize(
        self, 
        text: str, 
        max_length: Optional[int] = None,
        with_key_points: bool = False,
        content_type: str = "general",
        user_interests: list = None,
        user_career: str = None
    ) -> Dict[str, Any]:
        """
        Summarize the provided text.
        
        Args:
            text: The text to summarize
            max_length: Optional maximum length for the summary
            with_key_points: If True, also extract key points separately
            content_type: Type of content being summarized (general, news, academic, technical)
            user_interests: List of user's interest categories
            user_career: User's career or professional field
            
        Returns:
            Dictionary containing the summary and optionally key points
        """
        if not text or not text.strip():
            return {"summary": "", "key_points": [] if with_key_points else None}
        
        # Create prompt using the prompt function
        prompt_text = summarize_prompt(text, max_length, content_type, user_interests, user_career)
        
        # Generate summary using our local generate method with explicit LM
        result = self.generate(SummarizeContent, prompt_text)
        
        if not with_key_points:
            return {"summary": result.summary}
        
        # If key points requested, extract them separately using key_points prompt
        key_points_text = key_points_extraction_prompt(text, result.summary, user_interests, user_career)
        
        key_points_result = self.generate(KeyPointsExtraction, key_points_text)
        
        return {
            "summary": result.summary,
            "key_points": key_points_result.key_points
        }
        
    def bullet_summary(
        self, 
        text: str, 
        num_points: int = 5,
        content_type: str = "general",
        user_interests: list = None,
        user_career: str = None
    ) -> List[str]:
        """
        Create a bullet-point summary of the key points.
        
        Args:
            text: The text to summarize
            num_points: Number of bullet points to generate
            content_type: Type of content being summarized
            user_interests: List of user's interest categories
            user_career: User's career or professional field
            
        Returns:
            List of bullet points
        """
        if not text or not text.strip():
            return []
        
        # Create prompt using bullet_summary_prompt function
        bullet_prompt_text = bullet_summary_prompt(text, num_points, content_type, user_interests, user_career)
        
        # Generate bullet points using our local generate method
        result = self.generate(BulletPoints, bullet_prompt_text)
        
        # Process the bullets to ensure they're in list format
        if isinstance(result.bullets, list):
            return result.bullets
        else:
            # If the model returned bullets as text, try to split them
            bullets_text = str(result.bullets)
            return [b.strip().lstrip('•-*').strip() for b in bullets_text.split('\n') if b.strip()]
            
    def classify_and_summarize_news(
        self,
        news_list: List[str],
        user_interests: list = None,
        user_career: str = None
    ) -> Dict[str, str]:
        """
        Classify news articles into 'important' and 'worth mentioning' categories and summarize them.
        
        Args:
            news_list: List of news articles to process
            user_interests: List of user's interest categories
            user_career: User's career or professional field
            
        Returns:
            Dictionary with keys 'important' and 'mention', each containing summarized news
        """
        if not news_list or len(news_list) == 0:
            return {"important": "", "mention": ""}
            
        # Create a single string with all news for classification
        all_news = "\n\n---\n\n".join([str(news) for news in news_list])
        
        # Generate prompt for classification
        prompt_text = news_classification_prompt(all_news, user_interests, user_career)
        
        # Generate classification using our local generate method
        result = self.generate(NewsClassification, prompt_text)
        
        return {
            "important": result.important_news,
            "mention": result.mention_news
        }