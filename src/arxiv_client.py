"""
arxiv_client.py

Provides ArxivClient for searching and retrieving papers from arXiv.
"""

from datetime import datetime, timedelta
from typing import Dict, List

import arxiv
import pandas as pd


class ArxivClient:
    """
    Client for fetching and processing arXiv papers.
    """

    def __init__(self):
        self.client = arxiv.Client()

    def search_papers(
        self,
        query: str = "cat:astro-ph.GA",
        max_results: int = 100,
        sort_by: arxiv.SortCriterion = arxiv.SortCriterion.SubmittedDate,
    ) -> List[Dict]:
        """
        Search arXiv for papers matching a query.

        Args:
            query (str): arXiv search query string (e.g., "cat:cs.AI").
            max_results (int): Maximum number of papers to fetch.
            sort_by (arxiv.SortCriterion): Sort criterion (e.g., by date).

        Returns:
            List[Dict]: List of paper metadata dictionaries.
        """
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
        """
        Get recent papers from a specific category.

        Args:
            category (str): arXiv category code (e.g., "cs.AI").
            days (int): Number of days back to include.

        Returns:
            List[Dict]: List of recent paper metadata dictionaries.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        query = f"cat:{category} AND submittedDate:[{start_date.strftime('%Y%m%d')}* TO {end_date.strftime('%Y%m%d')}*]"
        return self.search_papers(query=query, max_results=50)

    def papers_to_dataframe(self, papers: List[Dict]) -> pd.DataFrame:
        """
        Convert papers list to pandas DataFrame.

        Args:
            papers (List[Dict]): List of paper metadata dictionaries.

        Returns:
            pd.DataFrame: DataFrame containing paper data.
        """
        return pd.DataFrame(papers)
