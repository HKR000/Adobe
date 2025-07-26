# Approach Explanation – Round 1B: Persona-Driven Document Intelligence

## 🔍 Objective

The goal of Round 1B is to build an intelligent system that, given a collection of PDFs, a defined user persona, and a specific job-to-be-done, can identify the most relevant document sections and provide refined sub-section insights — all offline and CPU-only.

---

## 🧠 High-Level Strategy

The solution builds on our Round 1A outline extractor, which parses each PDF to identify structural elements like titles, H1/H2/H3 headings, and their page numbers. This outline forms the backbone for semantic analysis in Round 1B.

The core of the system is a pipeline that:

1. **Loads PDFs and extracts headings (1A)**
2. **Reads the persona + job intent from a structured JSON file**
3. **Embeds and compares semantic similarity between each section heading and the job-to-be-done**
4. **Ranks the most relevant sections using cosine similarity**
5. **Extracts and refines sub-sections under those ranked headings using lightweight heuristics**
6. **Outputs a final structured JSON response**

---

## 🧰 Technical Components

### 1. **PDF Heading Extraction**
- Reuses the `pdfminer.six`-based logic from Round 1A to extract bold headings and font sizes.
- Classifies headings into levels (H1, H2, H3) based on relative font size and boldness.

### 2. **Semantic Relevance Ranking**
- Uses the `sentence-transformers` library (`paraphrase-MiniLM-L6-v2` model, <90MB) to embed:
  - Each section heading text
  - A query string: "Persona needs to [job]"
- Applies cosine similarity to match headings with the persona’s intent.
- Ranks sections by similarity score and assigns `importance_rank`.

### 3. **Sub-section Text Extraction**
- Uses `PyMuPDF` to extract text from the same page as the relevant heading.
- If the heading is found in the text, extracts the paragraph(s) following it.
- Limits the summary to 2–3 sentences or 500 characters for clarity and performance.

---

## ⚙️ Offline + Docker Compliance

- The system is containerized using a slim Python base image.
- All models are downloaded during the Docker build process to ensure **offline inference**.
- No GPU is used; the system runs on CPU with <1GB model size and <60 seconds runtime for 3–5 PDFs.

---

## 📦 Output

The final output includes:
- Metadata (documents, persona, job, timestamp)
- Ranked section list with `importance_rank`
- Sub-section analysis text from relevant pages

---

## ✅ Why This Generalizes Well

By decoupling structure extraction (1A) from semantic matching (1B), the solution remains highly adaptable across:
- Domains (research, finance, education)
- Personas (students, analysts, researchers)
- Jobs (reviewing, summarizing, studying)

All logic is modular and extendable — ready to scale or plug into a future interactive document interface.

