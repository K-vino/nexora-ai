from typing import List
from utils.logging import Logger
import numpy as np

class TextSummarizer:
    """
    Simple Extractive Summarizer based on keyword frequency.
    (Non-GenAI, purely statistical).
    """
    def __init__(self):
        self.logger = Logger.get_logger("TextSummarizer")
        
    def summarize(self, text: str, top_n=1) -> str:
        """
        Extracts top_n sentences based on length/complexity (Proxi-Summarization).
        Real imp would use PageRank/TextRank.
        Here we just pick the longest sentence as a heuristic for 'most informative'
        in short real estate blurbs.
        """
        if not text: return ""
        
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if not sentences: return text
        
        # Heuristic: Score by word count
        scores = [len(s.split()) for s in sentences]
        top_idx = np.argmax(scores)
        
        return sentences[top_idx] + "."
