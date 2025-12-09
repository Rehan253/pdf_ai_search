from pdf_processor import extract_text_from_pdf, save_extracted_text, save_extracted_json
import os

input_folder = "dataset"             # <-- using your dataset folder directly
output_folder = "data/extracted"     # <-- extracted files go here

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_folder, filename)

        print(f"\n[PROCESSING] {filename}")

        data = extract_text_from_pdf(pdf_path)

        if data:
            txt_out = os.path.join(output_folder, filename.replace(".pdf", ".txt"))
            json_out = os.path.join(output_folder, filename.replace(".pdf", ".json"))

            save_extracted_text(data, txt_out)
            save_extracted_json(data, json_out)
