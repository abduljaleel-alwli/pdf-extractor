import os
import fitz  # PyMuPDF
import pdfplumber
import argparse
from datetime import datetime


def extract_images(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    image_count = 0

    for page_index in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(page_index)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = os.path.join(
                output_dir, f"image_p{page_index+1}_{img_index+1}.{image_ext}"
            )
            with open(image_filename, "wb") as f:
                f.write(image_bytes)
            image_count += 1

    return image_count


def extract_texts(pdf_path, output_dir):
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            text_filename = os.path.join(output_dir, f"text_page_{i+1}.txt")
            with open(text_filename, "w", encoding="utf-8") as f:
                f.write(text or "")
    return len(pdf.pages)


def make_output_dir(base_dir="output"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(base_dir, f"run_{timestamp}")
    os.makedirs(output_path, exist_ok=True)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="PDF Product Extractor by Shamll Tech")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output directory (optional)", default="output")
    args = parser.parse_args()

    pdf_path = args.pdf
    output_base = args.output

    if not os.path.isfile(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return

    output_dir = make_output_dir(output_base)
    print(f"📁 Output will be saved to: {output_dir}\n")

    print("📤 Extracting images...")
    image_count = extract_images(pdf_path, output_dir)
    print(f"✅ Extracted {image_count} images.")

    print("📤 Extracting text...")
    page_count = extract_texts(pdf_path, output_dir)
    print(f"✅ Extracted text from {page_count} pages.")

    print("\n🎉 Extraction completed successfully!")


if __name__ == "__main__":
    main()
