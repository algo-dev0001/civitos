"""
Comment classification module.

This module provides classification logic for user-generated comments.
Supports both AI-based and rule-based classification with automatic fallback.
"""

from .classifier import classify_comment, classify_comment_ai, classify_comment_rule_based

__all__ = ['classify_comment', 'classify_comment_ai', 'classify_comment_rule_based']
