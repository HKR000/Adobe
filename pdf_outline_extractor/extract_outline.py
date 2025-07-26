import os
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def is_bold(fontname):
    bold_keywords = ["Bold", "bold", "BD", "Bd"]
    return any(keyword in fontname for keyword in bold_keywords)

def extract_fonts_and_text(pdf_path):
    headings = []
    font_sizes = []

    for page_number, page_layout in enumerate(extract_pages(pdf_path), start=1):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    line_text = text_line.get_text().strip()
                    if not line_text:
                        continue

                    sizes = []
                    font_names = []
                    for char in text_line:
                        if isinstance(char, LTChar):
                            sizes.append(char.size)
                            font_names.append(char.fontname)

                    if not sizes:
                        continue

                    avg_size = sum(sizes) / len(sizes)
                    font_sizes.append(avg_size)

                    bold = any(is_bold(f) for f in font_names)

                    headings.append((line_text, avg_size, page_number, bold))

    return headings, font_sizes

def classify_headings(headings, font_sizes):
    unique_sizes = sorted(set(font_sizes), reverse=True)
    size_to_level = {size: f"H{i+1}" for i, size in enumerate(unique_sizes[:3])}

    outline = []
    title = headings[0][0] if headings else "Untitled Document"

    for text, size, page, bold in headings:
        level = size_to_level.get(size)
        if level and bold:
            outline.append({"level": level, "text": text, "page": page})

    return title, outline

def process_pdf(pdf_filename):
    pdf_path = os.path.join(INPUT_DIR, pdf_filename)
    headings, font_sizes = extract_fonts_and_text(pdf_path)
    title, outline = classify_headings(headings, font_sizes)

    result = {
        "title": title,
        "outline": outline
    }

    output_path = os.path.join(OUTPUT_DIR, pdf_filename.replace(".pdf", ".json"))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

def main():
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            print(f"Processing {filename}...")
            process_pdf(filename)

if __name__ == "__main__":
    main()
