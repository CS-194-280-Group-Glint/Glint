def summarize_prompt(text: str, max_length: int = None, content_type: str = "general") -> str:
    """
    Generate a prompt for text summarization with configurable parameters.
    
    Args:
        text: The text to summarize
        max_length: Optional maximum length for the summary (in words)
        content_type: Type of content being summarized (general, news, academic, technical)
    
    Returns:
        A formatted prompt string
    """
    # Content-specific instructions
    content_instructions = {
        "general": "",
        "news": "Focus on key events, people involved, and significant outcomes.",
        "academic": "Preserve key theoretical concepts and important findings.",
        "technical": "Maintain technical accuracy while making complex concepts accessible."
    }
    
    # Length constraint
    length_constraint = f"Limit the summary to approximately {max_length} words." if max_length else "Create a concise summary."
    
    # Build the prompt
    return f"""
    # Text Summarization Task
    
    ## Instructions
    Summarize the following text in a clear, concise manner that captures the essential information.
    {content_instructions.get(content_type, "")}
    {length_constraint}
    
    - Maintain objectivity and accuracy
    - Preserve the original meaning and important context
    - Prioritize key points over peripheral details
    - Use clear, direct language
    
    ## Text to Summarize:
    {text}
    
    ## Summary:
    """

def bullet_summary_prompt(text: str, num_points: int = 5, content_type: str = "general") -> str:
    """
    Generate a prompt for bullet-point summarization.
    
    Args:
        text: The text to summarize
        num_points: Number of bullet points to generate
        content_type: Type of content being summarized
    
    Returns:
        A formatted prompt string
    """
    # Content-specific instructions
    content_instructions = {
        "general": "",
        "news": "Focus on key events, people involved, and significant outcomes.",
        "academic": "Identify key theoretical concepts and important findings.",
        "technical": "Highlight the most important technical information."
    }
    
    return f"""
    # Bullet-Point Summarization Task
    
    ## Instructions
    Extract exactly {num_points} key points from the following text.
    {content_instructions.get(content_type, "")}
    
    - Ensure each point captures an essential piece of information
    - Make each point self-contained and understandable on its own
    - Use concise, clear language
    - Order points by importance
    
    ## Text to Summarize:
    {text}
    
    ## Key Points:
    """

def key_points_extraction_prompt(text: str, summary: str) -> str:
    """
    Generate a prompt for extracting key points from a text that has already been summarized.
    
    Args:
        text: The original text
        summary: The generated summary
    
    Returns:
        A formatted prompt string
    """
    return f"""
    # Key Points Extraction Task
    
    ## Instructions
    Extract 3-5 essential key points from the text below. These points should:
    - Represent the most important information
    - Be presented in order of significance
    - Be stated clearly and concisely
    - Complement the following summary
    
    ## Original Text:
    {text}
    
    ## Summary Already Generated:
    {summary}
    
    ## Key Points:
    """

def impact_analysis_prompt(summary: str) -> str:
    """
    Generate a prompt for analyzing the potential impact and future implications of the news.
    
    Args:
        summary: The summary of the news content.
    
    Returns:
        A formatted prompt string.
    """
    return f"""
    # News Impact Analysis Task

    ## Instructions
    Analyze the following news summary and describe:
    - The possible impact of the event described
    - The potential future implications
    - Any affected stakeholders or sectors

    ## News Summary:
    {summary}

    ## Impact Analysis:
    """


def critical_analysis_prompt(summary: str) -> str:
    """
    Generate a prompt for critically analyzing the news content.
    
    Args:
        summary: The summary of the news content.
    
    Returns:
        A formatted prompt string.
    """
    return f"""
    # News Critical Analysis Task

    ## Instructions
    Critically analyze the following news summary. Provide:
    - Any potential biases or missing perspectives
    - Whether the summary is objective and factual
    - Any important details or viewpoints that might be omitted

    ## News Summary:
    {summary}

    ## Critical Analysis:
    """


def background_analysis_prompt(summary: str) -> str:
    """
    Generate a prompt for providing background context of the news.
    
    Args:
        summary: The summary of the news content.
    
    Returns:
        A formatted prompt string.
    """
    return f"""
    # News Background Context Task

    ## Instructions
    Based on the following news summary, provide relevant background information and context, such as:
    - Related historical events
    - Underlying causes or preceding incidents
    - Broader socio-political or economic background

    ## News Summary:
    {summary}

    ## Background Analysis:
    """


def podcast_prompt_template(
        news_summary: str,
        weather: str,
        reflection: str,
        user_style: str
) -> str:
    """Construct structured prompt for podcast script generation."""
    return f"""
    **Task**: Create a 10-minute engaging podcast script combining these elements:

    **News Summary**:
    {news_summary}

    **Current Time and Weather**:
    {weather}

    **Analytical Reflection**:
    {reflection}

    **Style Requirements**:
    {user_style if user_style else "Standard engaging podcast format"}

    **Structure Guidance**:
    1. Open with weather and time related greeting, if no context open with general greeting
    2. Introduce news topic naturally
    3. Blend analysis with real-world connections
    4. Maintain {user_style} tone throughout
    5. Close with memorable remark
    6. Script should have at most 4096 characters

    Include verbal cues like [BACKGROUND MUSIC] and [PAUSE] where appropriate.
    """

