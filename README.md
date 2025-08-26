# ArXiv LLM

An AI-powered semantic search tool for arXiv papers using sentence transformers and vector similarity search.

## Features

- Search papers by meaning, not just keywords
- Filter by Computer Science and Astrophysics categories
- Fast similarity search using FAISS
- Simple web interface built with Streamlit

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/arxiv-llm.git
cd arxiv-llm

# Install dependencies
pip install -e .
```

### Run the Web App

```bash
streamlit run app.py
```

### Command Line Usage

```bash
python scripts/run_arxiv_search.py
```

## How It Works

1. **Load Papers** - Fetch papers from arXiv by category
2. **Generate Embeddings** - Create semantic embeddings using sentence transformers
3. **Vector Search** - Use FAISS to find similar papers based on your query
4. **Browse Results** - View ranked results with abstracts and links

## Currently Supported Categories

**Computer Science:**

- Artificial Intelligence (cs.AI)
- Machine Learning (cs.LG)
- Natural Language Processing (cs.CL)
- Computer Vision (cs.CV)

**Astrophysics:**

- Galaxies (astro-ph.GA)
- Cosmology (astro-ph.CO)
- Solar and Stellar (astro-ph.SR)

## Project Structure

```text
arxiv-llm/
├── app.py                 # Streamlit web interface
├── pyproject.toml         # Project configuration
├── scripts/
│   └── run_arxiv_search.py # CLI example
└── src/
    ├── arxiv_client.py    # arXiv API client
    ├── embeddings.py      # Text embedding models
    └── vector_store.py    # Vector similarity search
```
