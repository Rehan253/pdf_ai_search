import fitz  # PyMuPDF
import os
import json


def extract_text_from_pdf(pdf_path):
    """
    Extract text from each page of a PDF.
    Returns a dictionary with filename and pages.
    """

    print(f"[INFO] Opening PDF: {pdf_path}")

    try:
        pdf = fitz.open(pdf_path)
    except Exception as e:
        print(f"[ERROR] Could not open PDF: {e}")
        return None

    extracted_pages = []

    for page_number in range(len(pdf)):
        page = pdf[page_number]
        text = page.get_text()

        # Clean text
        text = text.strip().replace("\n", " ")

        extracted_pages.append({
            "page": page_number + 1,
            "text": text
        })

    pdf.close()

    return {
        "filename": os.path.basename(pdf_path),
        "pages": extracted_pages
    }


def save_extracted_json(data, output_path):
    """Save extracted PDF content as a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"[INFO] JSON saved to {output_path}")


def save_extracted_text(data, output_path):
    """Save extracted PDF content as a plain .txt file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for page in data["pages"]:
            f.write(f"--- Page {page['page']} ---\n")
            f.write(page["text"] + "\n\n")
    print(f"[INFO] Text file saved to {output_path}")
