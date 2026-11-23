import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .embeddings import DenseSemanticEmbedder
from .synonyms import SynonymExpander

class HybridSemanticSearcher:
    """
    Hybrid Retrieval Engine combining:
    1. Dense Semantic Vector Search (dense embeddings in 256-D space)
    2. Query Expansion (clinical synonym thesaurus)
    3. Sparse Lexical Match (TF-IDF sublinear scoring)
    4. Entity-Aware Clinical Alignment
    """
    def __init__(self, dense_weight: float = 0.60, lexical_weight: float = 0.25, entity_weight: float = 0.15):
        self.dense_weight = dense_weight
        self.lexical_weight = lexical_weight
        self.entity_weight = entity_weight

        self.dense_embedder = DenseSemanticEmbedder()
        self.synonym_expander = SynonymExpander()
        self.tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)

        self.records = []
        self.dense_matrix = None
        self.tfidf_matrix = None
        self.corpus_docs = []
        self._is_indexed = False

    def index_knowledge_base(self, records: list[dict]):
        """Indexes knowledge base records for hybrid dense & sparse retrieval."""
        self.records = records
        self.corpus_docs = []

        for rec in records:
            topic = rec.get('topic', '')
            cat = rec.get('category', '')
            keywords = rec.get('keywords', '')
            symptoms = rec.get('symptoms', [])
            symptoms_str = " ".join(symptoms) if isinstance(symptoms, list) else str(symptoms)
            desc = rec.get('description', '')
            causes = rec.get('causes', '')
            prevention = rec.get('prevention', '')

            # Create rich representation document
            doc_text = f"{topic} {cat} {keywords} {symptoms_str} {desc} {causes} {prevention}".lower()
            self.corpus_docs.append(doc_text)

        if self.corpus_docs:
            # 1. Compute Dense Semantic Embeddings Matrix
            self.dense_matrix = self.dense_embedder.embed_corpus(self.corpus_docs)
            # 2. Fit and compute Sparse Lexical TF-IDF Matrix
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.corpus_docs)
            self._is_indexed = True

    def search(self, raw_query: str, entities: dict | None = None, top_k: int = 3) -> list[dict]:
        """
        Executes hybrid dense-sparse search for a user query.
        Returns sorted list of match dicts:
        [{'record': ..., 'score': float, 'dense_score': float, 'lexical_score': float}]
        """
        if not self._is_indexed or not self.records or not raw_query:
            return []

        # Step 1: Semantic Query Expansion
        expanded_query = self.synonym_expander.expand_query(raw_query)

        # Step 2: Dense Semantic Embedding of Query
        query_dense_vec = self.dense_embedder.embed_text(expanded_query)
        # Cosine similarity between query vector and all document vectors
        dense_scores = np.dot(self.dense_matrix, query_dense_vec)
        # Clip to [0, 1]
        dense_scores = np.clip(dense_scores, 0.0, 1.0)

        # Step 3: Sparse Lexical TF-IDF Similarity
        query_tfidf = self.tfidf_vectorizer.transform([expanded_query])
        lexical_scores = cosine_similarity(query_tfidf, self.tfidf_matrix)[0]

        # Step 4: Medical Entity Alignment Scoring
        entity_scores = np.zeros(len(self.records), dtype=np.float32)
        if entities:
            found_symptoms = [s.lower() for s in entities.get('symptoms', [])]
            found_conditions = [c.lower() for c in entities.get('conditions', [])]
            found_body_parts = [b.lower() for b in entities.get('body_parts', [])]

            for idx, rec in enumerate(self.records):
                score = 0.0
                topic_lower = rec.get('topic', '').lower()
                cat_lower = rec.get('category', '').lower()
                rec_symptoms = [s.lower() for s in rec.get('symptoms', [])] if isinstance(rec.get('symptoms'), list) else []
                keywords_lower = rec.get('keywords', '').lower()

                # Condition direct match
                for cond in found_conditions:
                    if cond in topic_lower or cond in keywords_lower:
                        score += 0.5

                # Symptom overlap
                for sym in found_symptoms:
                    if any(sym in rs or rs in sym for rs in rec_symptoms) or sym in keywords_lower:
                        score += 0.3

                # Body part alignment
                for bp in found_body_parts:
                    if bp in topic_lower or bp in keywords_lower or bp in cat_lower:
                        score += 0.2

                entity_scores[idx] = min(1.0, score)

        # Step 5: Composite Hybrid Score
        hybrid_scores = (
            self.dense_weight * dense_scores +
            self.lexical_weight * lexical_scores +
            self.entity_weight * entity_scores
        )

        ranked_indices = hybrid_scores.argsort()[::-1][:top_k]
        results = []
        for idx in ranked_indices:
            results.append({
                "record": self.records[idx],
                "score": round(float(hybrid_scores[idx]), 4),
                "dense_score": round(float(dense_scores[idx]), 4),
                "lexical_score": round(float(lexical_scores[idx]), 4),
                "entity_score": round(float(entity_scores[idx]), 4)
            })

        return results

