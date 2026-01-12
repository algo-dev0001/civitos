"""
Unit tests for the classifier module.
"""

from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from classifier import classify_comment, classify_comment_ai, classify_comment_rule_based


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


class AIClassifierTestCase(TestCase):
    """Test the AI-based classification with mocking."""
    
    @override_settings(USE_AI_CLASSIFIER=True, OPENAI_API_KEY='sk-test-key')
    @patch('openai.OpenAI')
    def test_ai_classification_flags_toxic_comment(self, mock_openai_class):
        """Test that AI correctly flags toxic comments."""
        # Mock the OpenAI API response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "true"
        mock_client.chat.completions.create.return_value = mock_response
        
        result = classify_comment_ai("You are a terrible person")
        
        self.assertTrue(result)
        mock_client.chat.completions.create.assert_called_once()
    
    @override_settings(USE_AI_CLASSIFIER=True, OPENAI_API_KEY='sk-test-key')
    @patch('openai.OpenAI')
    def test_ai_classification_allows_safe_comment(self, mock_openai_class):
        """Test that AI correctly allows safe comments."""
        # Mock the OpenAI API response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "false"
        mock_client.chat.completions.create.return_value = mock_response
        
        result = classify_comment_ai("Great article, thanks!")
        
        self.assertFalse(result)
        mock_client.chat.completions.create.assert_called_once()
    
    @override_settings(USE_AI_CLASSIFIER=True, OPENAI_API_KEY='sk-test-key')
    @patch('openai.OpenAI')
    def test_ai_classification_uses_correct_model(self, mock_openai_class):
        """Test that AI uses gpt-4o-mini model."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "false"
        mock_client.chat.completions.create.return_value = mock_response
        
        classify_comment_ai("Test comment")
        
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        self.assertEqual(call_kwargs['model'], 'gpt-4o-mini')
        self.assertEqual(call_kwargs['temperature'], 0)
        self.assertEqual(call_kwargs['max_tokens'], 10)
        self.assertEqual(call_kwargs['timeout'], 5.0)
    
    @override_settings(USE_AI_CLASSIFIER=True, OPENAI_API_KEY='')
    def test_ai_classification_fails_without_api_key(self):
        """Test that AI classification raises error without API key."""
        with self.assertRaises(ValueError) as context:
            classify_comment_ai("Test comment")
        
        self.assertIn("OPENAI_API_KEY not configured", str(context.exception))
    
    @override_settings(USE_AI_CLASSIFIER=True, OPENAI_API_KEY='sk-test-key')
    @patch('openai.OpenAI')
    def test_ai_classification_handles_unexpected_response(self, mock_openai_class):
        """Test that AI classification handles unexpected responses."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "maybe"
        mock_client.chat.completions.create.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            classify_comment_ai("Test comment")
        
        self.assertIn("Unexpected response from AI", str(context.exception))
    
    @override_settings(USE_AI_CLASSIFIER=True, OPENAI_API_KEY='sk-test-key')
    @patch('openai.OpenAI')
    def test_ai_classification_handles_api_error(self, mock_openai_class):
        """Test that AI classification handles API errors."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Simulate API error
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception):
            classify_comment_ai("Test comment")


class FallbackClassifierTestCase(TestCase):
    """Test the fallback mechanism between AI and rule-based classification."""
    
    @override_settings(USE_AI_CLASSIFIER=False, OPENAI_API_KEY='sk-test-key')
    def test_uses_rule_based_when_ai_disabled(self):
        """Test that rule-based is used when AI is disabled."""
        # Should flag based on rule-based (contains 'spam')
        result = classify_comment("This is spam")
        self.assertTrue(result)
        
        # Should not flag safe comment
        result = classify_comment("Great article!")
        self.assertFalse(result)
    
    @override_settings(USE_AI_CLASSIFIER=True, OPENAI_API_KEY='')
    def test_uses_rule_based_when_no_api_key(self):
        """Test that rule-based is used when API key is missing."""
        # Should flag based on rule-based
        result = classify_comment("This is spam")
        self.assertTrue(result)
    
    @override_settings(USE_AI_CLASSIFIER=True, OPENAI_API_KEY='sk-test-key')
    @patch('openai.OpenAI')
    def test_falls_back_to_rule_based_on_ai_error(self, mock_openai_class):
        """Test that system falls back to rule-based if AI fails."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Simulate API error
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        # Should fall back to rule-based and flag 'spam'
        result = classify_comment("This is spam")
        self.assertTrue(result)
        
        # Should fall back to rule-based and not flag safe comment
        result = classify_comment("Great article!")
        self.assertFalse(result)
    
    @override_settings(USE_AI_CLASSIFIER=True, OPENAI_API_KEY='sk-test-key')
    @patch('openai.OpenAI')
    def test_ai_classification_used_when_enabled(self, mock_openai_class):
        """Test that AI classification is used when properly configured."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "true"
        mock_client.chat.completions.create.return_value = mock_response
        
        result = classify_comment("Some comment")
        
        self.assertTrue(result)
        mock_client.chat.completions.create.assert_called_once()
    
    @override_settings(USE_AI_CLASSIFIER=True, OPENAI_API_KEY='sk-test-key')
    @patch('openai.OpenAI')
    def test_returns_boolean_always(self, mock_openai_class):
        """Test that classify_comment always returns a boolean."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Test with successful AI call
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "false"
        mock_client.chat.completions.create.return_value = mock_response
        
        result = classify_comment("Test")
        self.assertIsInstance(result, bool)
        
        # Test with AI error (should fall back)
        mock_client.chat.completions.create.side_effect = Exception("Error")
        
        result = classify_comment("Test")
        self.assertIsInstance(result, bool)


class RuleBasedClassifierTestCase(TestCase):
    """Test the rule-based classifier function directly."""
    
    def test_rule_based_flags_spam(self):
        """Test rule-based classifier flags spam."""
        self.assertTrue(classify_comment_rule_based("This is spam"))
    
    def test_rule_based_allows_safe_comment(self):
        """Test rule-based classifier allows safe comments."""
        self.assertFalse(classify_comment_rule_based("Great article!"))
    
    def test_rule_based_flags_caps(self):
        """Test rule-based classifier flags excessive caps."""
        self.assertTrue(classify_comment_rule_based("THIS IS ALL CAPS"))
    
    def test_rule_based_flags_punctuation(self):
        """Test rule-based classifier flags excessive punctuation."""
        self.assertTrue(classify_comment_rule_based("Amazing!!!!!!"))
