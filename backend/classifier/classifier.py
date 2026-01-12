"""
Rule-based comment classifier.

This is a simple implementation using banned words.
Can be replaced with:
- ML model (e.g., Hugging Face transformers)
- External API (e.g., OpenAI Moderation API, Perspective API)
- More sophisticated rule-based systems
"""

from typing import List

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


def classify_comment(text: str) -> bool:
    """
    Classify a comment to determine if it needs review.
    
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
