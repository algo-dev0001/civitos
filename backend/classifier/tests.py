"""
Unit tests for the classifier module.
"""

from django.test import TestCase
from classifier import classify_comment


class ClassifierTestCase(TestCase):
    """Test the comment classification logic."""
    
    def test_safe_comment(self):
        """Test that safe comments are not flagged."""
        safe_comments = [
            "This is a great article!",
            "Thanks for sharing.",
            "I learned a lot from this post.",
            "Very helpful information.",
            "Looking forward to more content.",
        ]
        
        for comment in safe_comments:
            with self.subTest(comment=comment):
                self.assertFalse(
                    classify_comment(comment),
                    f"Safe comment should not be flagged: {comment}"
                )
    
    def test_banned_word_spam(self):
        """Test that comments with 'spam' are flagged."""
        self.assertTrue(classify_comment("This is spam!"))
        self.assertTrue(classify_comment("SPAM message here"))
        self.assertTrue(classify_comment("spam"))
    
    def test_banned_word_scam(self):
        """Test that comments with 'scam' are flagged."""
        self.assertTrue(classify_comment("This is a scam"))
        self.assertTrue(classify_comment("Total scam!"))
    
    def test_banned_word_hate(self):
        """Test that comments with 'hate' are flagged."""
        self.assertTrue(classify_comment("I hate this"))
        self.assertTrue(classify_comment("HATE"))
    
    def test_banned_phrase_buy_now(self):
        """Test that 'buy now' phrase is flagged."""
        self.assertTrue(classify_comment("Buy now for best price!"))
        self.assertTrue(classify_comment("BUY NOW limited offer"))
    
    def test_excessive_caps(self):
        """Test that excessive capitalization is flagged."""
        # More than 50% uppercase in text longer than 10 chars
        self.assertTrue(classify_comment("THIS IS ALL CAPS MESSAGE"))
        self.assertTrue(classify_comment("HELLO EVERYONE"))
        
        # Normal caps should be fine
        self.assertFalse(classify_comment("Hello Everyone"))
        self.assertFalse(classify_comment("This Is A Title"))
    
    def test_excessive_punctuation_exclamation(self):
        """Test that excessive exclamation marks are flagged."""
        self.assertTrue(classify_comment("Amazing!!!!!!"))
        self.assertTrue(classify_comment("Wow!!!!!!!!"))
        
        # Normal punctuation is fine
        self.assertFalse(classify_comment("Great!"))
        self.assertFalse(classify_comment("Wow! That's cool!"))
    
    def test_excessive_punctuation_question(self):
        """Test that excessive question marks are flagged."""
        self.assertTrue(classify_comment("What??????"))
        self.assertTrue(classify_comment("Really?????????"))
        
        # Normal punctuation is fine
        self.assertFalse(classify_comment("What?"))
        self.assertFalse(classify_comment("What? Why?"))
    
    def test_case_insensitive_matching(self):
        """Test that banned words are matched case-insensitively."""
        self.assertTrue(classify_comment("SPAM"))
        self.assertTrue(classify_comment("Spam"))
        self.assertTrue(classify_comment("sPaM"))
        self.assertTrue(classify_comment("spam"))
    
    def test_empty_and_whitespace(self):
        """Test that empty or whitespace-only comments are not flagged."""
        self.assertFalse(classify_comment(""))
        self.assertFalse(classify_comment("   "))
        self.assertFalse(classify_comment("\n\t"))
    
    def test_short_text_with_caps(self):
        """Test that short text with caps is not flagged."""
        # Text must be longer than 10 chars to trigger caps check
        self.assertFalse(classify_comment("HELLO"))
        self.assertFalse(classify_comment("OK"))
    
    def test_multiple_violations(self):
        """Test comments with multiple violations are flagged."""
        self.assertTrue(classify_comment("THIS IS SPAM!!!!!!"))
        self.assertTrue(classify_comment("BUY NOW!!!!!!!!"))
        self.assertTrue(classify_comment("I HATE THIS SCAM!!!!"))
    
    def test_banned_word_in_sentence(self):
        """Test that banned words within sentences are caught."""
        self.assertTrue(classify_comment("I think this might be spam content"))
        self.assertTrue(classify_comment("You are an idiot for believing this"))
