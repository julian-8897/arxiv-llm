import sys
from pathlib import Path
from typing import Dict, List, Tuple

import streamlit as st
import yaml

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.arxiv_client import ArxivClient
from src.embeddings import TextEmbedder
from src.vector_store import VectorStore

# Initialize session state
if "store" not in st.session_state:
    st.session_state.store = None
if "embedder" not in st.session_state:
    st.session_state.embedder = None
if "loaded_categories" not in st.session_state:
    st.session_state.loaded_categories = []


@st.cache_data
def load_categories_config() -> Tuple[Dict[str, str], Dict[str, Dict[str, str]]]:
    """
    Load categories from config/categories.yaml.
    Returns:
      - flat_map: {"cs.AI": "Computer Science - Artificial Intelligence", ...}
      - domains: {"cs": {"cs.AI": "...", ...}, "astro-ph": {...}, ...}
    """
    cfg_path = project_root / "config" / "categories.yaml"
    flat_map: Dict[str, str] = {}
    domains: Dict[str, Dict[str, str]] = {}

    if cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)

        for domain_key, domain_info in cfg.get("domains", {}).items():
            domain_name = domain_info.get("name", domain_key)
            subcats = domain_info.get("categories", {})
            domains[domain_key] = {}
            for cat_key, cat_desc in subcats.items():
                full = f"{domain_key}.{cat_key}"
                desc = f"{domain_name} - {cat_desc}"
                flat_map[full] = desc
                domains[domain_key][full] = desc

    return flat_map, domains


def select_categories_ui() -> List[str]:
    flat_map, domains = load_categories_config()

    st.subheader("🌍 Select any arXiv categories")
    if not flat_map:
        st.warning(
            "No categories config found. Create config/categories.yaml or type category codes manually."
        )

    # Quick search
    query = st.text_input(
        "Search categories", placeholder="e.g., machine learning, galaxy, optics, cs.AI"
    )
    search_results = {}
    if query:
        q = query.lower()
        for k, v in flat_map.items():
            if q in k.lower() or q in v.lower():
                search_results[k] = v

    selected_from_search = st.multiselect(
        "Results" if query else "All categories",
        options=sorted((search_results or flat_map).keys()),
        format_func=lambda k: (search_results or flat_map)[k],
        default=[],
    )

    # Domain tabs (optional, shown if config present)
    selected_from_domains: List[str] = []
    if domains:
        st.write("Or browse by domain:")
        tabs = st.tabs([f"{d.upper()} ({len(cats)})" for d, cats in domains.items()])
        for tab, (domain, cat_map) in zip(tabs, domains.items()):
            with tab:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(
                        f"Select all {domain.upper()}", key=f"sel_all_{domain}"
                    ):
                        st.session_state[f"sel_{domain}"] = list(cat_map.keys())
                with c2:
                    if st.button(f"Clear {domain.upper()}", key=f"clr_{domain}"):
                        st.session_state[f"sel_{domain}"] = []

                chosen = st.multiselect(
                    f"{domain.upper()} categories",
                    options=sorted(cat_map.keys()),
                    default=st.session_state.get(f"sel_{domain}", []),
                    format_func=lambda k: cat_map[k].split(" - ")[-1],
                    key=f"multi_{domain}",
                )
                selected_from_domains.extend(chosen)

    # Manual codes
    with st.expander("Advanced: enter category codes manually"):
        manual = st.text_input(
            "Comma-separated category IDs",
            placeholder="e.g., cs.AI, cs.IR, astro-ph.GA",
        )
        manual_list = (
            [c.strip() for c in manual.split(",") if c.strip()] if manual else []
        )

    # Combine and de-duplicate
    final = list(
        dict.fromkeys(selected_from_search + selected_from_domains + manual_list)
    )
    if final:
        st.info(f"Selected {len(final)} categories")
    return final


def load_multiple_categories(
    categories: List[str], max_papers_per_category: int
) -> bool:
    progress = st.progress(0)
    status = st.empty()

    client = ArxivClient()
    embedder = TextEmbedder()

    flat_map, _ = load_categories_config()

    all_papers: List[Dict] = []
    for i, cat in enumerate(categories):
        status.text(f"Loading {flat_map.get(cat, cat)} ({cat})")
        try:
            papers = client.search_papers(
                f"cat:{cat}", max_results=max_papers_per_category
            )
            for p in papers:
                p["loaded_category"] = cat
                p["category_name"] = flat_map.get(cat, cat)
            all_papers.extend(papers)
        except Exception as e:
            st.warning(f"Failed to load {cat}: {e}")
        progress.progress((i + 1) / max(1, len(categories)))

    if not all_papers:
        status.empty()
        progress.empty()
        st.error("No papers loaded.")
        return False

    status.text("Generating embeddings...")
    embeddings = embedder.encode_papers(all_papers, field="title_summary")

    store = VectorStore(embeddings.shape[1])
    store.add_papers(all_papers, embeddings)

    st.session_state.store = store
    st.session_state.embedder = embedder
    st.session_state.loaded_categories = categories

    status.empty()
    progress.empty()
    st.success(f"Loaded {len(all_papers)} papers from {len(categories)} categories.")
    return True


def search_ui():
    st.header("🔍 Semantic search")
    query = st.text_input(
        "Query",
        placeholder="e.g., diffusion models for cosmology, black hole accretion, retrieval-augmented generation",
    )
    num_results = st.slider("Results", 1, 30, 5)

    # Optional filters if multiple categories loaded
    filter_cats = []
    if (
        st.session_state.loaded_categories
        and len(st.session_state.loaded_categories) > 1
    ):
        with st.expander("Filters"):
            filter_cats = st.multiselect(
                "Filter by loaded categories",
                options=st.session_state.loaded_categories,
                default=[],
            )

    if st.button("Search") and query:
        q_emb = st.session_state.embedder.encode_texts([query])
        raw = st.session_state.store.search(
            q_emb[0], k=min(50, max(10, num_results * 3))
        )

        results: List[Tuple[Dict, float]] = []
        for paper, score in raw:
            if filter_cats and paper.get("loaded_category") not in filter_cats:
                continue
            results.append((paper, score))
            if len(results) >= num_results:
                break

        if not results:
            st.warning("No results matched your filters.")
            return

        st.subheader(f"Found {len(results)} papers")
        for i, (p, s) in enumerate(results, 1):
            cat = p.get("loaded_category", p.get("primary_category", ""))
            emoji = (
                "💻"
                if str(cat).startswith("cs")
                else ("🌌" if str(cat).startswith("astro") else "📄")
            )
            with st.expander(
                f"{emoji} {i}. {p['title']}... (Similarity score: {s:.3f}) [{cat}]"
            ):
                st.write(f"**Authors:** {', '.join(p['authors'][:3])}")
                st.write(f"**Published:** {p['published'].strftime('%Y-%m-%d')}")
                st.write(f"**Category:** {p.get('primary_category', cat)}")
                st.write(f"**Abstract:** {p['summary']}...")
                st.write(f"**ArXiv ID:** {p['id']}")
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**[📄 PDF]({p['pdf_url']})**")
                with c2:
                    st.write(f"**[🔗 ArXiv Page]({p['arxiv_url']})**")


def main():
    st.title("🔬 ArXiv Universal Semantic Search")
    st.set_page_config(layout="wide")

    # Category selection
    cats = select_categories_ui()

    # Config + loader
    c1, c2 = st.columns(2)
    with c1:
        max_ppc = st.selectbox("Papers per category", [25, 50, 100, 150, 200], index=1)
    with c2:
        if cats:
            st.metric("Estimated total", f"~{len(cats) * max_ppc}")

    if st.button("🚀 Load Selected Categories", disabled=not bool(cats)):
        with st.spinner("Loading and indexing..."):
            if load_multiple_categories(cats, max_ppc):
                st.rerun()

    # Search section
    if st.session_state.store is not None:
        search_ui()
    else:
        st.info("Select one or more categories and load to begin.")


if __name__ == "__main__":
    main()
