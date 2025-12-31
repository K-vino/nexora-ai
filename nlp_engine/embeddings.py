from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from utils.logging import Logger

class EmbeddingEngine:
    """
    Generates TF-IDF (Interpretability) and Mean-Vector (Semantics) embeddings.
    """
    def __init__(self):
        self.logger = Logger.get_logger("EmbeddingEngine")
        self.tfidf = TfidfVectorizer(max_features=1000)
        self.vocab = None
        
    def compute_tfidf(self, corpus: List[str]) -> Tuple[Any, List[str]]:
        """
        Computes TF-IDF matrix and returns (matrix, feature_names).
        """
        self.logger.info(f"Computing TF-IDF for {len(corpus)} documents.")
        tfidf_matrix = self.tfidf.fit_transform(corpus)
        feature_names = self.tfidf.get_feature_names_out()
        self.vocab = feature_names
        return tfidf_matrix, feature_names
        
    def get_top_keywords(self, tfidf_matrix, feature_names, top_n=5) -> List[List[str]]:
        """
        Extracts top keywords per document based on TF-IDF score.
        """
        keywords = []
        dense = tfidf_matrix.todense()
        
        for i in range(dense.shape[0]):
            row = np.array(dense[i]).flatten()
            top_indices = row.argsort()[-top_n:][::-1]
            doc_keywords = [feature_names[idx] for idx in top_indices if row[idx] > 0]
            keywords.append(doc_keywords)
            
        return keywords
