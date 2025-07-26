# main.py

import os
import json
import sys
from datetime import datetime

from persona_engine.job_parser import load_persona_job
from persona_engine.ranker import SectionRanker
from persona_engine.summarizer import SectionSummarizer

# Import your 1A extractor
from extract_outline import extract_outline_from_pdf  # assuming your 1A function looks like this

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def run_round_1a():
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".pdf"):
            input_path = os.path.join(INPUT_DIR, file)
            output_path = os.path.join(OUTPUT_DIR, file.replace(".pdf", ".json"))
            outline = extract_outline_from_pdf(input_path)
            with open(output_path, "w") as f:
                json.dump(outline, f, indent=2)
            print(f"✅ Outline extracted for {file}")

def run_round_1b():
    persona, job = load_persona_job(INPUT_DIR)

    # Step 1: Extract outlines from all PDFs
    sections = []
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        outline = extract_outline_from_pdf(pdf_path)
        for entry in outline.get("outline", []):
            sections.append({
                "document": pdf_file,
                "page_number": entry["page"],
                "text": entry["text"],
                "level": entry["level"]
            })

    # Step 2: Rank relevant sections
    ranker = SectionRanker()
    ranked_sections = ranker.rank_sections(sections, persona, job)

    # Step 3: Summarize top sections
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

    # Step 4: Final Output
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

    with open(os.path.join(OUTPUT_DIR, "summary_output.json"), "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print("✅ Round 1B processing complete. Output written to summary_output.json")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "1a"

    if mode == "1a":
        run_round_1a()
    elif mode == "1b":
        run_round_1b()
    else:
        print("❌ Invalid mode. Use '1a' or '1b'")
