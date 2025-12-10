
---

📄 **AI PDF Semantic Search Engine**
Developed by **Rehan Shafique**

---

## 📌 Overview

`pdf_ai_search` is a fully local, offline PDF semantic search engine that extracts, indexes, and searches aviation incident reports using semantic embeddings.

The system uses:

* PyMuPDF → PDF text extraction
* SentenceTransformers (MiniLM-L6-v2) → Embeddings
* FAISS → High-performance vector indexing
* Streamlit → Graphical interface
* Snippet Generator → Most relevant sentence extraction
* Threshold Filtering → Prevents irrelevant matches

This project is optimized for speed, accuracy, and offline usage.

---

## 🚀 Key Features

* ✓ Extracts text from aviation PDFs
* ✓ Builds a local FAISS vector index
* ✓ Semantic search (query → relevant pages)
* ✓ Automatic snippet generation
* ✓ Threshold filtering for accuracy
* ✓ Full CLI tool
* ✓ Full GUI (Streamlit)
* ✓ Download PDF buttons
* ✓ Export results to JSON
* ✓ Persistent results (session state)

---

## 🏗 Project Structure

```
pdf_ai_search/
│
├── data/
│   ├── extracted/         # JSON extracted PDFs
│   └── index/             # FAISS index + metadata
│
├── dataset/               # Raw PDF files
│
├── embedder.py
├── extractor.py
├── vector_store.py
├── search_engine.py
├── build_index.py
├── search_cli.py
├── streamlit_app.py
│
├── requirements.txt
└── README.md
```

---

## 🧠 System Architecture

```
┌──────────────────┐
│   Raw PDFs       │
│   (dataset/)     │
└───────┬──────────┘
        │ Extract
        ▼
┌──────────────────┐
│ JSON Text Pages  │
│ (extracted/)     │
└───────┬──────────┘
        │ Embed
        ▼
┌──────────────────┐
│ Embeddings +     │
│ FAISS Index      │
└───────┬──────────┘
        │ Search
        ▼
┌──────────────────────────────────────┐
│ Semantic Search Engine + Snippets    │
└───────┬──────────────────────────────┘
        │ Display
        ▼
┌──────────────────────────────────────┐
│ Streamlit GUI / CLI Output           │
└──────────────────────────────────────┘
```

---

## 🔧 Installation

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd pdf_ai_search
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

Activate:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If PyTorch fails on Python 3.13:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

---

## 📥 Preparing the Dataset

Place all aviation PDFs in:

```
dataset/
```

---

## 🏗 Step 1 – Extract Text

```bash
python extractor.py
```

Output saved to:

```
data/extracted/
```

---

## 🏗 Step 2 – Build FAISS Index

```bash
python build_index.py
```

Creates:

```
data/index/faiss.index
data/index/metadata.json
```

---

## 🖥 CLI Usage

```bash
python search_cli.py
```

Example:

```
Enter query: weather conditions
```

Example output:

```
File: 20080102X00002.pdf
Page: 3
Score: 0.83
Snippet: "The **weather** conditions during the approach..."
```

---

## 📊 GUI Usage

Start Streamlit:

```bash
streamlit run streamlit_app.py
```

Opens at:

```
http://localhost:8501/
```

GUI Features:

* Adjustable Top K results
* Adjustable relevance threshold
* Snippet preview
* PDF download
* JSON export
* Persistent results

---

## 🖼 Screenshot Placeholders

Home Screen:

```
docs/home_screenshot.png
```

Search Results:

```
docs/search_screenshot.png
```

---

## 🧪 Example Queries

* weather conditions
* engine failure
* runway excursion
* icing
* crosswind landing
* stall warning
* pilot visibility

---

## 👨‍💻 Author

**Rehan Shafique**
Data Scientist


---

## 📜 Requirements

See `requirements.txt`.

---

## 📝 Final Notes

This project demonstrates:

* Clean modular architecture
* High-performance FAISS search
* Accurate semantic retrieval
* Professional engineering practices

Now ready for review and deployment.
