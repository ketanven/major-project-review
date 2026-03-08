import fitz # PyMuPDF
import os
import json

HTML_DIR = "/Users/ketanpillai/Documents/Major_Project_3rd_review.html"
ASSETS_DIR = os.path.join(HTML_DIR, "assets")
HEADER_JSON = os.path.join(ASSETS_DIR, "header.json")

with open(HEADER_JSON, "r") as f:
    header = json.load(f)

slide_list = header["slideList"]
print(f"Found {len(slide_list)} slides.")

for i, slide_id in enumerate(slide_list):
    slide_dir = os.path.join(ASSETS_DIR, slide_id, "assets")
    pdf_path = os.path.join(slide_dir, f"{slide_id}.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"Could not find PDF for slide {i+1} ({slide_id})")
        continue
        
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # 2.0 scale for high res (retina)
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=True)
        img_path = os.path.join(slide_dir, f"layer_{page_num}.png")
        pix.save(img_path)
    print(f"Extracted slide {i+1} ({doc.page_count} layers)")
    
print("Extraction complete.")
