# Comment Classifier Module

## Overview

This module provides comment classification to identify content that needs human review. The current implementation uses a simple rule-based approach that can easily be replaced with more sophisticated solutions.

## Current Implementation

**Rule-Based Classifier** (`classifier.py`):
- Checks for banned words (case-insensitive)
- Detects excessive capitalization (>50% uppercase)
- Flags excessive punctuation (>5 exclamation or question marks)
- Returns `True` if comment needs review, `False` otherwise

## Usage

```python
from classifier import classify_comment

# Check a comment
needs_review = classify_comment("This is spam!")
# Returns: True

needs_review = classify_comment("Great article, thanks!")
# Returns: False
```

## Future Enhancements

This module is designed to be easily replaceable with:

### 1. Machine Learning Model
```python
from transformers import pipeline

classifier = pipeline("text-classification", 
                     model="unitary/toxic-bert")

def classify_comment(text: str) -> bool:
    result = classifier(text)[0]
    return result['label'] == 'toxic' and result['score'] > 0.7
```

### 2. External API (OpenAI Moderation)
```python
import openai

def classify_comment(text: str) -> bool:
    response = openai.Moderation.create(input=text)
    return response["results"][0]["flagged"]
```

### 3. External API (Perspective API)
```python
from googleapiclient import discovery

def classify_comment(text: str) -> bool:
    client = discovery.build("commentanalyzer", "v1alpha1",
                            developerKey=API_KEY)
    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = client.comments().analyze(body=analyze_request).execute()
    return response['attributeScores']['TOXICITY']['summaryScore']['value'] > 0.7
```

## Testing

Run the test suite:
```bash
python classifier/test_classifier.py
```

## Configuration

Banned words can be updated in `BANNED_WORDS` list in `classifier.py`.
