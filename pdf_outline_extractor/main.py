# main.py

import os
import sys
import json
from datetime import datetime

from persona_engine.job_parser import load_persona_job
from persona_engine.ranker import SectionRanker
from persona_engine.summarizer import SectionSummarizer

# 👇 Import your existing process_pdf function
from extract_outline import process_pdf

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def run_round_1a():
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            print(f"Processing {filename}...")
            process_pdf(filename)
    print("✅ Round 1A complete.")

def run_round_1b():
    print("🔍 Loading persona and job...")
    persona, job = load_persona_job(INPUT_DIR)

    print("📑 Running outline extraction from Round 1A...")
    sections = []
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]

    for pdf_file in pdf_files:
        # First call process_pdf() to generate outline json
        process_pdf(pdf_file)

        json_path = os.path.join(OUTPUT_DIR, pdf_file.replace(".pdf", ".json"))
        if not os.path.exists(json_path):
            print(f"⚠️ Skipping {pdf_file}, outline JSON not found.")
            continue

        with open(json_path, "r", encoding="utf-8") as f:
            outline_data = json.load(f)

        for entry in outline_data.get("outline", []):
            sections.append({
                "document": pdf_file,
                "page_number": entry["page"],
                "text": entry["text"],
                "level": entry["level"]
            })

    print(f"📊 Ranking {len(sections)} sections...")
    ranker = SectionRanker()
    ranked_sections = ranker.rank_sections(sections, persona, job)

    print("✂️ Summarizing top-ranked sections...")
    summarizer = SectionSummarizer()
    refined_analysis = []
    for sec in ranked_sections:
        summary = summarizer.extract_text_from_section(
            pdf_path=os.path.join(INPUT_DIR, sec["document"]),
            page_number=sec["page_number"],
            section_title=sec["text"]
        )
        refined_analysis.append({
            "document": sec["document"],
            "page_number": sec["page_number"],
            "refined_text": summary
        })

    output_data = {
        "metadata": {
            "documents": pdf_files,
            "persona": persona,
            "job_to_be_done": job,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "extracted_sections": [
            {
                "document": sec["document"],
                "page_number": sec["page_number"],
                "section_title": sec["text"],
                "importance_rank": sec["importance_rank"]
            }
            for sec in ranked_sections
        ],
        "sub_section_analysis": refined_analysis
    }

    summary_path = os.path.join(OUTPUT_DIR, "summary_output.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print("✅ Round 1B complete. Output written to summary_output.json")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "1a"

    if mode == "1a":
        run_round_1a()
    elif mode == "1b":
        run_round_1b()
    else:
        print("❌ Invalid mode. Use '1a' or '1b'")

