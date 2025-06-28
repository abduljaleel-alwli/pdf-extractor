## 🛠️ Project Overview

This repository contains [brief project name or purpose – e.g., "Product PDF Extractor"], a tool designed to:

- Extract product images and data from PDF catalogs
- Save content in organized formats (images, text, or CSV)
- Automate tedious manual processes for faster results

> ✅ Ideal for digital stores, content managers, and product catalog digitization.

---

## 🚀 Features

- Extract all embedded images from PDFs
- Parse product names and descriptions
- Auto-save outputs in structured folders
- CLI-based user interaction (easy to use)
- Built with Python (fitz, pdfplumber, Pillow)

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/abduljaleel-alwli/pdf-extractor.git
cd product-extractor
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the script:

```bash
python main.py
```

## 📁 Output Structure

After running the script, you'll find an output/ folder containing:

```bash
output/
├── image_1_1.jpg
├── image_1_2.png
├── text_page_1.txt
└── ...
```
