import os
import pandas as pd
from nlp_engine.problem_definition import NLPProblemDefiner
from nlp_engine.text_cleaning import TextCleaner
from nlp_engine.embeddings import EmbeddingEngine
from nlp_engine.similarity import SimilarityEngine
from nlp_engine.topic_modeling import TopicModeler
from utils.logging import Logger

# Mock Data Loading
print("Starting Phase-4 Verification...")
TEXT_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "real_estate_descriptions.csv")
print(f"Loading data from {TEXT_DATA_PATH}")
df = pd.read_csv(TEXT_DATA_PATH)
print(f"Loaded {len(df)} documents.")

# 13. Text Cleaning
print("\n[STEP 13] TEXT CLEANING & NORMALIZATION")
cleaner = TextCleaner()
original_texts = df["text_content"].tolist()
doc_ids = df["doc_id"].tolist()
cleaned_corpus = [cleaner.clean_text(t)[0] for t in original_texts]
print(f"   Cleaned {len(cleaned_corpus)} documents.")
print(f"   Sample: {cleaned_corpus[0][:50]}...")

# 14. Embeddings (TF-IDF)
print("\n[STEP 14] TF-IDF & KEYWORD EXTRACTION")
embedder = EmbeddingEngine()
tfidf_matrix, features = embedder.compute_tfidf(cleaned_corpus)
keywords = embedder.get_top_keywords(tfidf_matrix, features)
print(f"   Vocabulary Size: {len(features)}")
print(f"   Doc 101 Keywords: {keywords[0]}")

# 15. Similarity Matching
print("\n[STEP 15] SIMILARITY & MATCHING")
matcher = SimilarityEngine()
similarities = matcher.find_similar_documents(tfidf_matrix, doc_ids)
# Show matches for first doc
matches_101 = similarities[doc_ids[0]]
if matches_101:
    print(f"   Matches for Doc {doc_ids[0]}: {matches_101[0]['match_doc_id']} (Score: {matches_101[0]['score']})")
else:
        print(f"   Matches for Doc {doc_ids[0]}: None (Unique)")

# 16. Topic Modeling
print("\n[STEP 16] TOPIC MODELING (LDA)")
topic_modeler = TopicModeler(n_topics=3)
topics = topic_modeler.discover_topics(tfidf_matrix, features)
for t in topics:
    print(f"   Topic {t['topic_id']}: {', '.join(t['terms'])}")

print("\nPHASE-4 VERIFICATION COMPLETE.")
