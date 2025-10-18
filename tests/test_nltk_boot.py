"""
Test NLTK bootstrap initialization.
Ensures NLTK data (wordnet, stopwords, etc.) is available at startup.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def test_ensure_nltk_data():
    """Test that NLTK data bootstrap function works without errors."""
    from api_analyse.startup_nltk import ensure_nltk_data
    
    # Call the bootstrap function - should not raise any exceptions
    ensure_nltk_data()
    
    # Verify corpora are actually available by importing and using them
    import nltk
    from nltk.corpus import wordnet, stopwords
    from nltk.tokenize import punkt
    
    # Simple sanity checks
    assert wordnet is not None, "WordNet corpus should be available"
    assert stopwords is not None, "Stopwords corpus should be available"
    
    # Try accessing stopwords for a common language
    english_stopwords = stopwords.words('english')
    assert len(english_stopwords) > 0, "English stopwords list should not be empty"
    
    # Try using wordnet
    synsets = wordnet.synsets('dog')
    assert len(synsets) > 0, "WordNet should return synsets for common words"
    
    print("✅ NLTK bootstrap test passed - all corpora available")


if __name__ == "__main__":
    test_ensure_nltk_data()
