"""
Comment classification module.

This module provides classification logic for user-generated comments.
The implementation can be swapped out for ML models or external APIs.
"""

from .classifier import classify_comment

__all__ = ['classify_comment']
