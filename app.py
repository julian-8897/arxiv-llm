import sys
from pathlib import Path

import streamlit as st

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.arxiv_client import ArxivClient
from src.embeddings import TextEmbedder
from src.vector_store import VectorStore

# Simple category options
CATEGORIES = {
    "cs.AI": "Computer Science - Artificial Intelligence",
    "cs.LG": "Computer Science - Machine Learning",
    "cs.CL": "Computer Science - Natural Language Processing",
    "cs.CV": "Computer Science - Computer Vision",
    "astro-ph.GA": "Astrophysics - Galaxies",
    "astro-ph.CO": "Astrophysics - Cosmology",
    "astro-ph.SR": "Astrophysics - Solar and Stellar",
}

# Initialize session state
if "store" not in st.session_state:
    st.session_state.store = None
if "embedder" not in st.session_state:
    st.session_state.embedder = None


def load_papers(category, max_papers):
    """Load papers and build vector store"""
    client = ArxivClient()
    embedder = TextEmbedder()

    papers = client.search_papers(f"cat:{category}", max_results=max_papers)

    embeddings = embedder.encode_papers(papers, field="title_summary")

    store = VectorStore(embeddings.shape[1])
    store.add_papers(papers, embeddings)

    return store, embedder


def main():
    st.title("🔬 ArXiv Paper Search")
    st.write("Discover papers through AI-enabled semantic search")

    with st.sidebar:
        st.header("📚 Available Categories")

        st.write("**💻 Computer Science:**")
        cs_cats = {k: v for k, v in CATEGORIES.items() if k.startswith("cs")}
        for cat, desc in cs_cats.items():
            st.write(f"• {desc}")

        st.write("**🌌 Astrophysics:**")
        astro_cats = {k: v for k, v in CATEGORIES.items() if k.startswith("astro")}
        for cat, desc in astro_cats.items():
            st.write(f"• {desc}")

        st.divider()

    # Simple configuration
    col1, col2 = st.columns(2)

    with col1:
        selected_category = st.selectbox(
            "Choose category:",
            options=list(CATEGORIES.keys()),
            format_func=lambda x: CATEGORIES[x],
        )

    with col2:
        max_papers = st.selectbox(
            "Number of papers:", options=[100, 200, 300, 500], index=1
        )

    # Load data
    if st.button("Load Papers"):
        with st.spinner(
            f"Loading {max_papers} papers from {CATEGORIES[selected_category]}..."
        ):
            try:
                store, embedder = load_papers(selected_category, max_papers)
                st.session_state.store = store
                st.session_state.embedder = embedder
                st.success(f"Loaded {len(store)} papers!")
            except Exception as e:
                st.error(f"Error: {e}")

    # Search interface
    if st.session_state.store is not None:
        st.header("🔍 Search Papers")

        query = st.text_input(
            "Enter search query:",
            placeholder="e.g., 'neural networks', 'black holes', 'galaxy formation'",
        )
        num_results = st.slider("Number of results", 1, 15, 5)

        if st.button("Search") and query:
            query_embedding = st.session_state.embedder.encode_texts([query])
            results = st.session_state.store.search(query_embedding[0], k=num_results)

            st.subheader(f"Found {len(results)} similar papers:")

            for i, (paper, score) in enumerate(results, 1):
                emoji = "💻" if paper["primary_category"].startswith("cs") else "🌌"

                with st.expander(
                    f"{emoji} {i}. {paper['title'][:70]}... (Score: {score:.3f})"
                ):
                    st.write(f"**Authors:** {', '.join(paper['authors'][:3])}")
                    st.write(
                        f"**Published:** {paper['published'].strftime('%Y-%m-%d')}"
                    )
                    st.write(f"**Category:** {paper['primary_category']}")
                    st.write(f"**Abstract:** {paper['summary'][:400]}...")
                    st.write(f"**ArXiv ID:** {paper['id']}")

                    # Add both links
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**[📄 PDF]({paper['pdf_url']})**")
                    with col2:
                        st.write(f"**[🔗 ArXiv Page]({paper['arxiv_url']})**")

    else:
        st.info("👆 Choose a category and click 'Load Papers' to get started")


if __name__ == "__main__":
    main()
