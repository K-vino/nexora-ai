from sklearn.decomposition import LatentDirichletAllocation # type: ignore
import numpy as np
from typing import List, Dict, Any
from utils.logging import Logger

class TopicModeler:
    """
    Discovers latent topics in text using LDA.
    """
    def __init__(self, n_topics=3):
        self.logger = Logger.get_logger("TopicModeler")
        self.n_topics = n_topics
        self.lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        
    def discover_topics(self, tfidf_matrix, feature_names) -> List[Dict[str, Any]]:
        """
        Fits LDA and returns topics with top words.
        """
        self.logger.info(f"Discovering {self.n_topics} latent topics...")
        self.lda.fit(tfidf_matrix)
        
        topics = []
        for index, topic in enumerate(self.lda.components_):
            # top 5 words per topic
            top_indices = topic.argsort()[-5:][::-1]
            top_words = [feature_names[i] for i in top_indices]
            topics.append({
                "topic_id": index,
                "terms": top_words
            })
            
        return topics
