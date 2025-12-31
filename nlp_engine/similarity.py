from sklearn.metrics.pairwise import cosine_similarity # type: ignore
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from utils.logging import Logger

class SimilarityEngine:
    """
    Computes similarity between documents.
    """
    def __init__(self):
        self.logger = Logger.get_logger("SimilarityEngine")
        
    def find_similar_documents(self, tfidf_matrix, doc_ids: List[Any], top_n=3) -> Dict[Any, List[Dict[str, Any]]]:
        """
        Returns top_n similar docs for each doc.
        """
        self.logger.info("Computing cosine similarity matrix.")
        sim_matrix = cosine_similarity(tfidf_matrix)
        
        results = {}
        
        for i, doc_id in enumerate(doc_ids):
            # Get similarity scores for doc i
            scores = sim_matrix[i]
            
            # Sort indices (descending), exclude self
            sorted_indices = scores.argsort()[::-1]
            top_matches = []
            
            for idx in sorted_indices:
                if idx == i: continue # Skip self
                if len(top_matches) >= top_n: break
                
                match_id = doc_ids[idx]
                score = scores[idx]
                
                # Only include meaningful matches
                if score > 0.1:
                    top_matches.append({
                        "match_doc_id": match_id,
                        "score": round(float(score), 4)
                    })
            
            results[doc_id] = top_matches
            
        return results
