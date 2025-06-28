import fitz  # PyMuPDF
import pdfplumber
import os
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Dummy:
        def __getattr__(self, _): return ''
    Fore = Style = Dummy()


def extract_images(pdf_path: str, images_dir: str) -> int:
    """
    Extracts all images from the PDF and saves them to the images directory.
    """
    doc = fitz.open(pdf_path)
    image_count = 0

    for page_index in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(page_index)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = os.path.join(images_dir, f"image_p{page_index+1}_{img_index+1}.{image_ext}")
            with open(image_filename, "wb") as f:
                f.write(image_bytes)
            image_count += 1

    return image_count


def extract_text(pdf_path: str, texts_dir: str) -> int:
    """
    Extracts text from each page in the PDF and saves it as .txt files in texts_dir.
    """
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            text_filename = os.path.join(texts_dir, f"text_page_{i+1}.txt")
            with open(text_filename, "w", encoding="utf-8") as f:
                f.write(text or "")
    return len(pdf.pages)


def create_output_structure(base_name: str = "output") -> tuple:
    """
    Creates a structured output directory with images/ and texts/ subfolders.
    Returns the full paths of (main_dir, images_dir, texts_dir).
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_dir = os.path.join(base_name, f"extract_{timestamp}")
    images_dir = os.path.join(main_dir, "images")
    texts_dir = os.path.join(main_dir, "texts")

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(texts_dir, exist_ok=True)

    return main_dir, images_dir, texts_dir


def main():
    print(Fore.CYAN + "\n📄 PDF Image & Text Extractor - By Shamll Tech\n" + Style.RESET_ALL)

    pdf_path = input("🔍 Enter the full path to your PDF file: ").strip()

    if not os.path.isfile(pdf_path):
        print(Fore.RED + "❌ Error: File does not exist or path is incorrect.\n")
        return

    output_dir, images_dir, texts_dir = create_output_structure()

    print(Fore.YELLOW + "\n🖼️ Extracting images...")
    image_count = extract_images(pdf_path, images_dir)
    print(Fore.GREEN + f"✅ {image_count} images extracted and saved to: {images_dir}")

    print(Fore.YELLOW + "\n📝 Extracting text...")
    text_count = extract_text(pdf_path, texts_dir)
    print(Fore.GREEN + f"✅ Text extracted from {text_count} pages and saved to: {texts_dir}")

    print(Fore.CYAN + f"\n📁 All results are organized under: {output_dir}\n")


if __name__ == "__main__":
    main()
