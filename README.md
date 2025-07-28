📌 Challenge Overview


Round 1B focuses on intelligent content extraction from multiple PDFs. The solution must identify the most relevant sections and subsections based on:

A given persona (e.g., Researcher, Analyst, Student)

A job-to-be-done (e.g., summarize reports, literature review)

🚀 Solution Approach

Uses Round 1A’s outline extractor to structure each document.

Embeds document sections using sentence transformers (≤ 1GB model).

Uses a relevance ranking algorithm to score each section based on persona and job description.

Extracts top-ranked sections and subsections for each document.

Generates final output in the required JSON format.

🛠️ Technologies and Libraries

Language: Python 3

Libraries:


sentence-transformers – for semantic embeddings

pdfminer.six / PyMuPDF – for text extraction

numpy, scikit-learn – for ranking relevance

json – for output formatting

Environment: Docker (linux/amd64), CPU-only

🏗️ Project Structure


├── Dockerfile
├── main.py
├── requirements.txt
├── README.md  (this file)
└── modules/
    ├── outline_extractor.py
    ├── persona_ranker.py
    └── subsection_analyzer.py
    
⚡ Building the Docker Image


docker build --platform linux/amd64 -t persona-doc-analyzer:latest .

▶️ Running the Container


Prepare input:

/input/docs/ → 3–10 PDF files

/input/persona.json → Persona definition

/input/job.txt → Job-to-be-done

Run:



docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  persona-doc-analyzer:latest
The processed JSON will be saved in output/.

✅ Features

Multi-document processing (3–10 PDFs).

Persona and job-aware section ranking.

Subsection-level refined text extraction.

Fast execution (≤ 60s).

Fully offline, CPU-only, model size ≤ 1GB.

📊 Example Output


{
  "metadata": {
    "documents": ["report1.pdf", "report2.pdf"],
    "persona": "Investment Analyst",
    "job_to_be_done": "Analyze revenue trends and R&D investments",
    "timestamp": "2025-07-28T10:00:00Z"
  },
  "extracted_sections": [
    {
      "document": "report1.pdf",
      "page": 12,
      "section_title": "Revenue Growth",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "report1.pdf",
      "page": 12,
      "refined_text": "In 2024, revenue increased by 20% due to product diversification..."
    }
  ]
}
