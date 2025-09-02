from typing import Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer


class TextEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/allenai-specter"):
        self.model_name = model_name
        self.model = SentenceTransformer(self.model_name)

    def encode_texts(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        embeddings = self.model.encode(
            texts, batch_size=batch_size, show_progress_bar=True, convert_to_numpy=True
        )

        return embeddings

    def encode_papers(self, papers: List[Dict], field: str = "title"):
        if field == "title":
            texts = [paper["title"] for paper in papers]
        elif field == "summary":
            texts = [paper["summary"] for paper in papers]
        elif field == "title_summary":
            # Structured concatenation
            texts = [
                f"Title: {paper['title']}\nAbstract: {paper['summary']}"
                for paper in papers
            ]
        else:
            raise ValueError("field must be 'title', 'summary', or 'title_summary'")

        return self.encode_texts(texts)
