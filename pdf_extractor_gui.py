import fitz
import pdfplumber
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import platform
import subprocess

# ---------------- LANGUAGE SUPPORT ---------------- #

LANGUAGES = {
    "en": {
        "title": "PDF Extractor by Shamll Tech",
        "select_pdf": "📄 PDF File Path:",
        "browse": "Browse",
        "select_output": "📁 Output Folder (optional):",
        "start": "🚀 Start Extraction",
        "success": "✅ Extraction completed!",
        "images": "📸 Images extracted",
        "texts": "📝 Text pages extracted",
        "saved": "📁 Saved in",
        "developed": "Developed by Shamll Tech",
        "error": "Error",
        "invalid_path": "PDF file path is invalid.",
        "open_folder": "📂 Open Folder",
        "menu_language": "Language",
        "lang_en": "English",
        "lang_ar": "Arabic"
    },
    "ar": {
        "title": "أداة استخراج PDF - شامل للتقنية",
        "select_pdf": "📄 مسار ملف PDF:",
        "browse": "استعراض",
        "select_output": "📁 مجلد الإخراج (اختياري):",
        "start": "🚀 بدء الاستخراج",
        "success": "✅ تم الاستخراج بنجاح!",
        "images": "📸 عدد الصور المستخرجة",
        "texts": "📝 عدد الصفحات النصية",
        "saved": "📁 تم الحفظ في",
        "developed": "تم التطوير بواسطة شامل للتقنية",
        "error": "خطأ",
        "invalid_path": "مسار ملف PDF غير صالح.",
        "open_folder": "📂 فتح المجلد",
        "menu_language": "اللغة",
        "lang_en": "الإنجليزية",
        "lang_ar": "العربية"
    }
}

current_lang = "en"

def tr(key):
    return LANGUAGES[current_lang][key]

# ---------------- CORE FUNCTIONALITY ---------------- #

def extract_images(pdf_path, images_dir):
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

def extract_text(pdf_path, texts_dir):
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            text_filename = os.path.join(texts_dir, f"text_page_{i+1}.txt")
            with open(text_filename, "w", encoding="utf-8") as f:
                f.write(text or "")
    return len(pdf.pages)

def create_output_dirs(base_dir="output"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_dir = os.path.join(base_dir, f"extract_{timestamp}")
    images_dir = os.path.join(main_dir, "images")
    texts_dir = os.path.join(main_dir, "texts")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(texts_dir, exist_ok=True)
    return main_dir, images_dir, texts_dir

def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

# ---------------- GUI ---------------- #

def browse_pdf():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        pdf_path_var.set(filepath)

def browse_output_folder():
    folderpath = filedialog.askdirectory()
    if folderpath:
        output_folder_var.set(folderpath)

def start_extraction():
    pdf_path = pdf_path_var.get().strip()
    output_base = output_folder_var.get().strip() or "output"

    if not os.path.isfile(pdf_path):
        messagebox.showerror(tr("error"), tr("invalid_path"))
        return

    try:
        main_dir, images_dir, texts_dir = create_output_dirs(output_base)
        image_count = extract_images(pdf_path, images_dir)
        text_count = extract_text(pdf_path, texts_dir)

        result = (
            f"{tr('success')}\n\n"
            f"{tr('images')}: {image_count}\n"
            f"{tr('texts')}: {text_count}\n\n"
            f"{tr('saved')}: {main_dir}"
        )
        messagebox.showinfo(tr("success"), result)

        open_folder_btn.config(state=tk.NORMAL)
        open_folder_btn.path = main_dir

    except Exception as e:
        messagebox.showerror(tr("error"), str(e))

def switch_language(lang):
    global current_lang
    current_lang = lang
    rebuild_ui()

def rebuild_ui():
    root.title(tr("title"))
    label_pdf.config(text=tr("select_pdf"))
    label_out.config(text=tr("select_output"))
    btn_pdf.config(text=tr("browse"))
    btn_out.config(text=tr("browse"))
    extract_btn.config(text=tr("start"))
    open_folder_btn.config(text=tr("open_folder"))
    footer_label.config(text=tr("developed"))

# ---------------- RUN ---------------- #

root = tk.Tk()
root.geometry("520x320")
root.resizable(False, False)

# Menu
menubar = tk.Menu(root)
lang_menu = tk.Menu(menubar, tearoff=0)
lang_menu.add_command(label=LANGUAGES["en"]["lang_en"], command=lambda: switch_language("en"))
lang_menu.add_command(label=LANGUAGES["ar"]["lang_ar"], command=lambda: switch_language("ar"))
menubar.add_cascade(label=tr("menu_language"), menu=lang_menu)
root.config(menu=menubar)

# Variables
pdf_path_var = tk.StringVar()
output_folder_var = tk.StringVar()

# UI
label_pdf = tk.Label(root, text="", font=("Arial", 12))
label_pdf.pack(pady=5)
tk.Entry(root, textvariable=pdf_path_var, width=60).pack()
btn_pdf = tk.Button(root, text="", command=browse_pdf)
btn_pdf.pack(pady=2)

label_out = tk.Label(root, text="", font=("Arial", 12))
label_out.pack(pady=10)
tk.Entry(root, textvariable=output_folder_var, width=60).pack()
btn_out = tk.Button(root, text="", command=browse_output_folder)
btn_out.pack(pady=2)

extract_btn = tk.Button(root, text="", command=start_extraction, bg="#4CAF50", fg="white", font=("Arial", 12))
extract_btn.pack(pady=15)

open_folder_btn = tk.Button(root, text="", state=tk.DISABLED, command=lambda: open_folder(open_folder_btn.path), bg="#2196F3", fg="white")
open_folder_btn.pack()

footer_label = tk.Label(root, text="", fg="gray")
footer_label.pack(side="bottom", pady=5)

# Initialize UI text
rebuild_ui()

root.mainloop()
