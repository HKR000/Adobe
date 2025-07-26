# persona_engine/summarizer.py
import fitz  # PyMuPDF

class SectionSummarizer:
    def __init__(self):
        pass

    def extract_text_from_section(self, pdf_path, page_number, section_title=None, max_chars=500):
        doc = fitz.open(pdf_path)
        page = doc[page_number - 1]  # PyMuPDF is 0-indexed

        full_text = page.get_text()

        if section_title:
            # Try to find and return the paragraph after the heading
            lines = full_text.split('\n')
            section_index = None
            for i, line in enumerate(lines):
                if section_title.lower() in line.lower():
                    section_index = i
                    break

            if section_index is not None and section_index + 1 < len(lines):
                # Return 2–3 lines below heading as crude summary
                summary = " ".join(lines[section_index + 1 : section_index + 4])
                return summary[:max_chars]

        # fallback: return first 500 chars
        return full_text[:max_chars]
