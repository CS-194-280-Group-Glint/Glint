def summarize_prompt(text: str, max_length: int = None, content_type: str = "general", user_interests: list = None, user_career: str = None) -> str:
    """
    Generate a prompt for text summarization with configurable parameters.
    
    Args:
        text: The text to summarize
        max_length: Optional maximum length for the summary (in words)
        content_type: Type of content being summarized (general, news, academic, technical)
        user_interests: List of user's interest categories
        user_career: User's career or professional field
    
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
    
    # Personalization
    personalization = ""
    if user_interests or user_career:
        personalization = "\n## Personalization Context:\n"
        if user_interests:
            personalization += f"- User's interests: {', '.join(user_interests)}\n"
        if user_career:
            personalization += f"- User's career: {user_career}\n"
        personalization += "\nWhen summarizing, emphasize aspects that relate to the user's interests and professional background when applicable.\n"
    
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
    {personalization}
    
    ## Text to Summarize:
    {text}
    
    ## Summary:
    """

def bullet_summary_prompt(text: str, num_points: int = 5, content_type: str = "general", user_interests: list = None, user_career: str = None) -> str:
    """
    Generate a prompt for bullet-point summarization.
    
    Args:
        text: The text to summarize
        num_points: Number of bullet points to generate
        content_type: Type of content being summarized
        user_interests: List of user's interest categories
        user_career: User's career or professional field
    
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
    
    # Personalization
    personalization = ""
    if user_interests or user_career:
        personalization = "\n## Personalization Context:\n"
        if user_interests:
            personalization += f"- User's interests: {', '.join(user_interests)}\n"
        if user_career:
            personalization += f"- User's career: {user_career}\n"
        personalization += "\nEnsure that some key points highlight aspects relevant to the user's interests and professional background when applicable.\n"
    
    return f"""
    # Bullet-Point Summarization Task
    
    ## Instructions
    Extract exactly {num_points} key points from the following text.
    {content_instructions.get(content_type, "")}
    
    - Ensure each point captures an essential piece of information
    - Make each point self-contained and understandable on its own
    - Use concise, clear language
    - Order points by importance
    {personalization}
    
    ## Text to Summarize:
    {text}
    
    ## Key Points:
    """

def key_points_extraction_prompt(text: str, summary: str, user_interests: list = None, user_career: str = None) -> str:
    """
    Generate a prompt for extracting key points from a text that has already been summarized.
    
    Args:
        text: The original text
        summary: The generated summary
        user_interests: List of user's interest categories
        user_career: User's career or professional field
    
    Returns:
        A formatted prompt string
    """
    # Personalization
    personalization = ""
    if user_interests or user_career:
        personalization = "\n## Personalization Context:\n"
        if user_interests:
            personalization += f"- User's interests: {', '.join(user_interests)}\n"
        if user_career:
            personalization += f"- User's career: {user_career}\n"
        personalization += "\nTry to include key points that relate to the user's interests and professional background when applicable.\n"
    
    return f"""
    # Key Points Extraction Task
    
    ## Instructions
    Extract 3-5 essential key points from the text below. These points should:
    - Represent the most important information
    - Be presented in order of significance
    - Be stated clearly and concisely
    - Complement the following summary
    {personalization}
    
    ## Original Text:
    {text}
    
    ## Summary Already Generated:
    {summary}
    
    ## Key Points:
    """

def impact_analysis_prompt(summary: str, user_interests: list = None, user_career: str = None) -> str:
    """
    Generate a prompt for analyzing the potential impact and future implications of the news.
    
    Args:
        summary: The summary of the news content.
        user_interests: List of user's interest categories.
        user_career: User's career or professional field.
    
    Returns:
        A formatted prompt string.
    """
    personalization = ""
    if user_interests or user_career:
        personalization = "## Personalization Context:\n"
        if user_interests:
            personalization += f"- User's interests: {', '.join(user_interests)}\n"
        if user_career:
            personalization += f"- User's career: {user_career}\n"
        personalization += "\nTailor your analysis to be particularly relevant to the user's interests and career when applicable.\n"
    
    return f"""
    # News Impact Analysis Task

    ## Instructions
    Analyze the following news summary and describe:
    - The possible impact of the event described
    - The potential future implications
    - Any affected stakeholders or sectors
    
    {personalization}
    ## News Summary:
    {summary}

    ## Impact Analysis:
    """


def critical_analysis_prompt(summary: str, user_interests: list = None, user_career: str = None) -> str:
    """
    Generate a prompt for critically analyzing the news content.
    
    Args:
        summary: The summary of the news content.
        user_interests: List of user's interest categories.
        user_career: User's career or professional field.
    
    Returns:
        A formatted prompt string.
    """
    personalization = ""
    if user_interests or user_career:
        personalization = "## Personalization Context:\n"
        if user_interests:
            personalization += f"- User's interests: {', '.join(user_interests)}\n"
        if user_career:
            personalization += f"- User's career: {user_career}\n"
        personalization += "\nTailor your critical analysis to highlight aspects that intersect with the user's interests and professional background when applicable.\n"
    
    return f"""
    # News Critical Analysis Task

    ## Instructions
    Critically analyze the following news summary. Provide:
    - Any potential biases or missing perspectives
    - Whether the summary is objective and factual
    - Any important details or viewpoints that might be omitted
    
    {personalization}
    ## News Summary:
    {summary}

    ## Critical Analysis:
    """


def background_analysis_prompt(summary: str, user_interests: list = None, user_career: str = None) -> str:
    """
    Generate a prompt for providing background context of the news.
    
    Args:
        summary: The summary of the news content.
        user_interests: List of user's interest categories.
        user_career: User's career or professional field.
    
    Returns:
        A formatted prompt string.
    """
    personalization = ""
    if user_interests or user_career:
        personalization = "## Personalization Context:\n"
        if user_interests:
            personalization += f"- User's interests: {', '.join(user_interests)}\n"
        if user_career:
            personalization += f"- User's career: {user_career}\n"
        personalization += "\nFocus on historical context and background that intersects with the user's interests and professional field when applicable.\n"
    
    return f"""
    # News Background Context Task

    ## Instructions
    Based on the following news summary, provide relevant background information and context, such as:
    - Related historical events
    - Underlying causes or preceding incidents
    - Broader socio-political or economic background
    
    {personalization}
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

def news_classification_prompt(news_text: str, user_interests: list = None, user_career: str = None) -> str:
    """
    Generate a prompt for classifying and summarizing news articles into important and worth mentioning categories.
    
    Args:
        news_text: The text containing multiple news articles
        user_interests: List of user's interest categories
        user_career: User's career or professional field
    
    Returns:
        A formatted prompt string
    """
    # Personalization
    personalization = ""
    if user_interests or user_career:
        personalization = "\n## Personalization Context:\n"
        if user_interests:
            personalization += f"- User's interests: {', '.join(user_interests)}\n"
        if user_career:
            personalization += f"- User's career: {user_career}\n"
        personalization += "\nWhen evaluating importance, prioritize news that aligns with the user's interests and professional background.\n"
    
    return f"""
    # News Classification and Summarization Task
    
    ## Instructions
    You are presented with multiple news articles. Your task is to:
    
    1. Classify the news into two categories:
       - IMPORTANT: News that has significant impact, relevance, or importance
       - WORTH MENTIONING: News that is interesting but less critical
       
    2. For each category, provide a comprehensive summary that combines the relevant news
       - Important news should be detailed and thorough
       - News worth mentioning should be briefly summarized
    
    3. Format your response as two distinct sections:
       - First section: Important news summary
       - Second section: News worth mentioning summary
    {personalization}
    
    ## News Articles:
    {news_text}
    
    ## Important News Summary:
    """

