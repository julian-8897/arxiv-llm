# ArXiv LLM Semantic Search

LLM-enabled Semantic search across arXiv papers using AI embeddings. Search by meaning instead of just keywords, and explore papers from multiple research domains simultaneously.

**[🚀 Try it live](https://arxiv-llm.streamlit.app/)**

## What it does

This tool lets you search arXiv papers semantically - find papers by describing what you're looking for rather than guessing the right keywords. You can load papers from any arXiv categories and search across all of them at once.

## Features

- **Semantic search** - "machine learning for astronomy" finds relevant papers even without exact keyword matches
- **Multi-category support** - Load papers from computer science, physics, math, biology, economics, etc.
- **Cross-domain discovery** - Find connections between different research areas
- **Fast vector search** using FAISS

## Quick start

```bash
git clone https://github.com/julian-8897/arxiv-llm.git
cd arxiv-llm
pip install -e .
streamlit run app.py
```

Or just use the [live demo](https://arxiv-llm.streamlit.app/).

## How to use

1. Select arXiv categories you're interested in (search by name or browse by domain)
2. Choose how many papers to load per category (50-100 works well)
3. Wait for papers to load and embeddings to generate
4. Search with natural language queries
5. Browse results with abstracts and links to full papers

## Example searches

- "transformers for time series prediction"
- "dark matter simulation techniques"
- "graph neural networks in biology"
- "quantum algorithms for optimization"

## Project structure

```
arxiv-llm/
├── app.py              # Main web app
├── config/
│   └── categories.yaml # Available arXiv categories
└── src/
    ├── arxiv_client.py # arXiv API client
    ├── embeddings.py   # Text embedding models
    └── vector_store.py # Vector search
```

## Configuration

Edit `config/categories.yaml` to add more arXiv categories, or just type category codes directly in the app (like `cs.AI` or `astro-ph.GA`).

The app falls back to a basic set of categories if the config file is missing.

##
