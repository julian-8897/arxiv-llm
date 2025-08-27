# ArXiv Universal Semantic Search

An AI-powered semantic search tool that lets you search across **any arXiv categories** using sentence transformers and vector similarity search.

**🚀 [Try the Live Demo](https://arxiv-llm.streamlit.app/)**

## ✨ Key Features

- **🌍 Universal Category Support** - Search across ALL arXiv domains (CS, Physics, Math, Biology, Economics, etc.)
- **🔍 Semantic Search** - Find papers by meaning, not just keywords
- **📊 Multi-Category Selection** - Load and search multiple categories simultaneously
- **🎯 Smart Category Discovery** - Search categories by name or browse by domain
- **⚡ Fast Vector Search** - Powered by FAISS for efficient similarity matching
- **🌐 Clean Web Interface** - Intuitive Streamlit UI with tabbed browsing

## 🚀 Quick Start

### Try Online

Visit the live demo: **https://arxiv-llm.streamlit.app/**

### Run Locally

```bash
# Clone the repository
git clone https://github.com/julian-8897/arxiv-llm.git
cd arxiv-llm

# Install dependencies
pip install -e .

# Run the app
streamlit run app.py
```

## 🎯 How It Works

1. **Select Categories** - Choose from any arXiv categories using search, domain tabs, or manual entry
2. **Load Papers** - Fetch papers from selected categories (25-200 papers per category)
3. **Generate Embeddings** - Create semantic embeddings using sentence transformers
4. **Vector Search** - Use FAISS to find similar papers across all loaded categories
5. **Browse Results** - View ranked results with abstracts, authors, and direct links

## 🌍 Supported Domains

The app supports **all arXiv categories** across domains including:

**💻 Computer Science**

- Artificial Intelligence, Machine Learning, Computer Vision
- Natural Language Processing, Robotics, Software Engineering
- Databases, Cryptography, Human-Computer Interaction

**🌌 Astrophysics**

- Cosmology, Galaxy Formation, Solar Physics
- High Energy Phenomena, Instrumentation

**⚛️ Physics**

- Computational Physics, Optics, Plasma Physics
- Applied Physics, Biological Physics

**🔢 Mathematics**

- Combinatorics, Number Theory, Algebraic Geometry
- Mathematical Physics, Probability, Statistics

**🧬 Quantitative Biology**

- Genomics, Neuroscience, Molecular Networks

**💰 Economics & 📡 Engineering**

- Econometrics, Signal Processing, Systems Control

## 🏗️ Project Structure

```text
arxiv-llm/
├── app.py                 # Main Streamlit application
├── pyproject.toml         # Project configuration and dependencies
├── config/
│   └── categories.yaml    # ArXiv category definitions
├── scripts/
│   └── run_arxiv_search.py # CLI example
└── src/
    ├── arxiv_client.py    # arXiv API client
    ├── embeddings.py      # Text embedding models
    └── vector_store.py    # Vector similarity search
```

## ⚙️ Configuration

### Category Configuration

Create `config/categories.yaml` to define available categories:

```yaml
domains:
  cs:
    name: "Computer Science"
    categories:
      AI: "Artificial Intelligence"
      LG: "Machine Learning"
      CV: "Computer Vision"
  astro-ph:
    name: "Astrophysics"
    categories:
      GA: "Astrophysics of Galaxies"
      CO: "Cosmology"
```

### Advanced Usage

**Multi-Category Search:**

- Select categories from different domains to find interdisciplinary connections
- Use the search box to quickly find specific categories
- Enter category codes manually for precise control

**Search Tips:**

- Use descriptive queries: "transformer models for astronomical data"
- Try cross-domain searches: "machine learning in cosmology"
- Filter results by specific categories if needed

## 🛠️ Tech Stack

- **Frontend:** Streamlit for interactive web interface
- **Embeddings:** Sentence Transformers for semantic understanding
- **Vector Search:** FAISS for fast similarity search
- **Data Source:** arXiv API for paper metadata
- **Deployment:** Streamlit Community Cloud

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License
