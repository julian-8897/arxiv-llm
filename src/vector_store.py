from typing import Dict, List

import faiss
import numpy as np


class VectorStore:
    def __init__(self, embedding_dimension: int):
        self.embedding_dimension = embedding_dimension
        self.index = faiss.IndexFlatIP(self.embedding_dimension)
        self.papers = []
        self.embeddings = None

    def add_papers(self, papers: List[Dict], embeddings: np.ndarray):
        """
        Add papers and their embeddings to the store

        Args:
            papers: List of paper dictionaries
            embeddings: Corresponding embeddings
        """
        faiss.normalize_L2(embeddings)

        # Add to FAISS index
        self.index.add(embeddings.astype("float32"))

        # Store papers and embeddings
        self.papers.extend(papers)
        if self.embeddings is None:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])

    def search(self, query_embedding: np.ndarray, k: int = 5):
        if not self.papers:
            return []

        query_embedding = query_embedding.reshape(1, -1).astype("float32")
        faiss.normalize_L2(query_embedding)

        similarities, indices = self.index.search(query_embedding, k)

        results = []
        for similarity, idx in zip(similarities[0], indices[0]):
            if idx < len(self.papers):
                paper = self.papers[idx]
                results.append((paper, float(similarity)))

        return results

    def __len__(self):
        """Return number of papers in store"""
        return len(self.papers)
