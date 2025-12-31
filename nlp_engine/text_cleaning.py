import re
from typing import List, Tuple
from utils.logging import Logger

class TextCleaner:
    """
    Cleans and normalizes text for NLP tasks.
    Uses Regex and a built-in stopword list to avoid NLTK dependency/hangs.
    """
    def __init__(self):
        self.logger = Logger.get_logger("TextCleaner")
        # Minimal stopword list for real estate context
        self.stop_words = {
            "the", "and", "is", "in", "to", "of", "a", "with", "for", "on", 
            "it", "this", "that", "are", "was", "be", "at", "as", "by", "an",
            "from", "or", "but", "not", "has", "have", "had", "will", "would"
        }
        
    def clean_text(self, text: str) -> Tuple[str, List[str]]:
        """
        Returns (lowercased_cleaned_text, list_of_tokens).
        """
        if not isinstance(text, str):
            return "", []
            
        # 1. Lowercase
        text = text.lower()
        
        # 2. Remove punctuation/numbers (keep alpha and spaces)
        text = re.sub(r'[^a-z\s]', '', text)
        
        # 3. Tokenize (split by space)
        tokens = text.split()
        
        # 4. Remove stopwords
        cleaned_tokens = [
            word for word in tokens 
            if word not in self.stop_words and len(word) > 2
        ]
        
        cleaned_text = " ".join(cleaned_tokens)
        
        return cleaned_text, cleaned_tokens
