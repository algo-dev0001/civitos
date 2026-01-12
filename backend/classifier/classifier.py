"""
Comment classifier with AI and rule-based fallback.

This module provides two classification approaches:
1. AI-based: Uses OpenAI API for nuanced content moderation
2. Rule-based: Simple pattern matching for banned words and heuristics

The AI classifier is optional and falls back to rule-based if:
- USE_AI_CLASSIFIER setting is False
- OpenAI API key is not configured
- API call fails or times out
"""

import logging
from typing import List

logger = logging.getLogger(__name__)

# Banned words that trigger review
# Keep this list simple and focused on obvious problematic content
BANNED_WORDS: List[str] = [
    # Profanity
    'spam',
    'scam',
    'phishing',
    # Aggressive language
    'stupid',
    'idiot',
    'hate',
    'kill',
    # Commercial spam indicators
    'buy now',
    'click here',
    'limited offer',
    'free money',
    # Add more as needed
]


def classify_comment_rule_based(text: str) -> bool:
    """
    Rule-based comment classification (original implementation).
    
    Args:
        text: The comment text to classify
        
    Returns:
        True if the comment should be flagged for review, False otherwise
    """
    if not text or not text.strip():
        return False
    
    # Normalize text for comparison
    normalized_text = text.lower().strip()
    
    # Check for banned words
    for banned_word in BANNED_WORDS:
        if banned_word.lower() in normalized_text:
            return True
    
    # Additional heuristics can be added here:
    # - Excessive punctuation (!!!!!!)
    # - All caps text
    # - URLs or email addresses
    # - Very long comments
    
    # Check for excessive caps (more than 50% uppercase)
    if len(text) > 10:
        uppercase_ratio = sum(1 for c in text if c.isupper()) / len(text)
        if uppercase_ratio > 0.5:
            return True
    
    # Check for excessive punctuation
    if text.count('!') > 5 or text.count('?') > 5:
        return True
    
    return False


def classify_comment_ai(text: str) -> bool:
    """
    AI-based comment classification using OpenAI API.
    
    Uses a small, efficient model (gpt-4o-mini) to classify comments.
    Returns a boolean indicating if the comment needs review.
    
    Args:
        text: The comment text to classify
        
    Returns:
        True if the comment should be flagged for review, False otherwise
        
    Raises:
        Exception: If API call fails (caller should handle gracefully)
    """
    from django.conf import settings
    from openai import OpenAI
    
    # Validate API key is configured
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not configured")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    # System prompt for the moderation task
    system_prompt = """You are a comment moderation system for a blog platform.
Analyze the given comment and determine if it needs human review.

Flag comments that contain:
- Hate speech, harassment, or personal attacks
- Spam, scams, or commercial promotions
- Profanity or inappropriate language
- Threats or violent content
- Off-topic or nonsensical content

Respond with ONLY "true" if the comment needs review, or "false" if it's safe.
Do not include any explanation, just the boolean value."""

    try:
        # Call OpenAI API with minimal parameters for cost efficiency
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Small, fast, cost-efficient model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Comment: {text}"}
            ],
            temperature=0,  # Deterministic output
            max_tokens=10,  # We only need "true" or "false"
            timeout=5.0,  # 5 second timeout
        )
        
        # Parse the response
        result = response.choices[0].message.content.strip().lower()
        
        # Convert to boolean
        if result == "true":
            return True
        elif result == "false":
            return False
        else:
            # Unexpected response, log and raise
            logger.warning(f"Unexpected AI response: {result}")
            raise ValueError(f"Unexpected response from AI: {result}")
            
    except Exception as e:
        # Log the error and re-raise so caller can handle fallback
        logger.error(f"AI classification failed: {str(e)}")
        raise


def classify_comment(text: str) -> bool:
    """
    Main comment classification function with AI and rule-based fallback.
    
    Process:
    1. If USE_AI_CLASSIFIER is enabled and API key is configured, try AI classification
    2. If AI fails or is disabled, fall back to rule-based classification
    3. Always returns a boolean (never fails)
    
    Args:
        text: The comment text to classify
        
    Returns:
        True if the comment should be flagged for review, False otherwise
    """
    from django.conf import settings
    
    # Try AI classification if enabled
    if settings.USE_AI_CLASSIFIER and settings.OPENAI_API_KEY:
        try:
            result = classify_comment_ai(text)
            logger.info(f"AI classification successful: {result}")
            return result
        except Exception as e:
            # Log the error and fall through to rule-based
            logger.warning(f"AI classification failed, falling back to rule-based: {str(e)}")
    
    # Fall back to rule-based classification
    result = classify_comment_rule_based(text)
    logger.info(f"Rule-based classification: {result}")
    return result
