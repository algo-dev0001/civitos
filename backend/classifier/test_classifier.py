"""
Tests for the comment classifier module.
"""

from classifier import classify_comment


def test_classify_comment():
    """Test the classify_comment function with various inputs."""
    
    # Test cases that should be flagged
    assert classify_comment("This is spam!") == True
    assert classify_comment("You are stupid") == True
    assert classify_comment("BUY NOW LIMITED OFFER") == True
    assert classify_comment("HELLO THIS IS ALL CAPS") == True
    assert classify_comment("What?????????") == True
    assert classify_comment("Amazing!!!!!!!!") == True
    
    # Test cases that should NOT be flagged
    assert classify_comment("This is a great article!") == False
    assert classify_comment("I really enjoyed reading this.") == False
    assert classify_comment("Thanks for sharing your thoughts.") == False
    assert classify_comment("") == False
    assert classify_comment("   ") == False
    
    print("✓ All classifier tests passed!")


if __name__ == "__main__":
    test_classify_comment()
