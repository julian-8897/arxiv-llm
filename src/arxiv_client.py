from datetime import datetime, timedelta
from typing import Dict, List

import arxiv
import pandas as pd


class ArxivClient:
    def __init__(self):
        self.client = arxiv.Client()

    def search_papers(
        self,
        query: str = "cat:astro-ph.GA",
        max_results: int = 100,
        sort_by: arxiv.SortCriterion = arxiv.SortCriterion.SubmittedDate,
    ) -> List[Dict]:
        search = arxiv.Search(query=query, max_results=max_results, sort_by=sort_by)

        papers = []
        for result in self.client.results(search):
            paper_id = result.entry_id.split("/")[-1]
            paper = {
                "id": paper_id,
                "title": result.title,
                "summary": result.summary,
                "authors": [author.name for author in result.authors],
                "published": result.published,
                "updated": result.updated,
                "categories": result.categories,
                "primary_category": result.primary_category,
                "pdf_url": result.pdf_url,
                "arxiv_url": f"https://arxiv.org/abs/{paper_id}",
                "links": [link.href for link in result.links],
            }
            papers.append(paper)

        return papers

    def get_recent_papers(self, category: str = "cs.AI", days: int = 7) -> List[Dict]:
        """Get recent papers from a specific category"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        query = f"cat:{category} AND submittedDate:[{start_date.strftime('%Y%m%d')}* TO {end_date.strftime('%Y%m%d')}*]"
        return self.search_papers(query=query, max_results=50)

    def papers_to_dataframe(self, papers: List[Dict]) -> pd.DataFrame:
        """Convert papers list to pandas DataFrame"""
        return pd.DataFrame(papers)


def main():
    client = ArxivClient()
    papers = client.search_papers()
    df = client.papers_to_dataframe(papers)
    print(df.head())


if __name__ == "__main__":
    main()
