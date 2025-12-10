import os
import json
import streamlit as st
import re
from search_engine import SearchEngine


# ============================
# IMPROVED SNIPPET FUNCTION
# ============================
def generate_snippet(text, query, max_length=250):
    """
    Extract the most relevant sentence(s) based on the query.
    Highlights the query words.
    """

    if not text or not text.strip():
        return "[No text available]"

    # 1. Split text into sentences based on punctuation
    sentences = re.split(r'(?<=[.!?]) +', text)

    query_words = [w.lower() for w in query.split()]

    # 2. Score each sentence by presence of query words
    best_sentence = None
    best_score = 0

    for sentence in sentences:
        sent_lower = sentence.lower()
        score = sum(1 for w in query_words if w in sent_lower)

        if score > best_score:
            best_score = score
            best_sentence = sentence

    # 3. Fallback if no matching sentence found
    if not best_sentence:
        best_sentence = text[:max_length]

    # 4. Trim if needed
    if len(best_sentence) > max_length:
        best_sentence = best_sentence[:max_length] + "..."

    # 5. Highlight matched words
    snippet = best_sentence
    for w in query_words:
        snippet = re.sub(
            rf"\b({re.escape(w)})\b",
            r"**\1**",
            snippet,
            flags=re.IGNORECASE
        )

    return snippet


# ==================================
# Streamlit cache for performance
# ==================================
@st.cache_resource
def load_engine():
    return SearchEngine()


# ============================
# MAIN STREAMLIT INTERFACE
# ============================
def main():
    st.set_page_config(page_title="AI PDF Semantic Search", layout="wide")

    st.title("📄 AI PDF Semantic Search Engine")
    st.write(
        "Search through indexed aviation PDF reports using **semantic search**. "
        "This system runs fully **offline** using embeddings + FAISS."
    )

    # ------------------------------
    # Initialize session state
    # ------------------------------
    if "last_query" not in st.session_state:
        st.session_state.last_query = ""

    if "last_results" not in st.session_state:
        st.session_state.last_results = []

    # Load search engine
    try:
        engine = load_engine()
    except Exception as e:
        st.error("❌ Failed to initialize search engine. Run `build_index.py` first.")
        st.code(str(e))
        return

    # Sidebar
    st.sidebar.header("⚙️ Search Options")
    top_k = st.sidebar.slider("Number of results", 1, 10, 5)

    threshold = st.sidebar.slider(
        "Relevance threshold (lower = stricter filtering)",
        min_value=0.5,
        max_value=2.5,
        value=1.2,
        step=0.1
    )


    # Search input
    query = st.text_input(
        "🔎 Enter your question:",
        placeholder="e.g. weather conditions, visibility issues, crosswind on takeoff",
        value=st.session_state.last_query  # KEEP QUERY AFTER REFRESH
    )

    # Handle Search Button
    search_clicked = st.button("Search")

    if search_clicked:
        if not query.strip():
            st.warning("⚠️ Please enter a query before searching.")
            return

        with st.spinner("Searching the indexed documents..."):
            results = engine.search(query, k=top_k, threshold=threshold)


        # Save results in session state
        st.session_state.last_query = query
        st.session_state.last_results = results

    # ====================================
    # DISPLAY RESULTS (FROM SESSION STATE)
    # ====================================
    results = st.session_state.last_results

    if results:
        st.subheader(f"🔍 Results for: **{st.session_state.last_query}**")

        for i, res in enumerate(results, start=1):
            filename = res["metadata"]["filename"]
            page = res["metadata"]["page"]
            score = res["distance"]
            snippet = res.get("snippet", "[Snippet unavailable]")

            pdf_file_path = f"./dataset/{filename}"

            with st.container():
                st.markdown(f"### {i}. 📄 {filename} — Page {page}")
                st.markdown(f"**Relevance Score:** `{score:.4f}`")

                # Snippet
                st.markdown(f"> {snippet}")

                # PDF download button
                try:
                    with open(pdf_file_path, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()

                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        key=f"download_{i}"
                    )
                except Exception as e:
                    st.warning(f"Could not load PDF for download: {e}")

                st.markdown("---")

        # ==========================
        # EXPORT ALL RESULTS (JSON)
        # ==========================
        export_data = {
            "query": st.session_state.last_query,
            "results": [
                {
                    "score": r["distance"],
                    "filename": r["metadata"]["filename"],
                    "page": r["metadata"]["page"],
                    "snippet": r.get("snippet", "[Snippet unavailable]"),
                }
                for r in results
            ],
        }


        export_json = json.dumps(export_data, indent=4)

        st.download_button(
            label="📥 Download All Results (JSON)",
            data=export_json,
            file_name="search_results.json",
            mime="application/json"
        )

    else:
        st.info("No relevant results found for this query. Try different keywords.")

# ==================
# Launch App
# ==================
if __name__ == "__main__":
    main()
