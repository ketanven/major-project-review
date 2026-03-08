import fitz
import os
import json

HTML_DIR = "/Users/ketanpillai/Documents/Major_Project_3rd_review.html"
ASSETS_DIR = os.path.join(HTML_DIR, "assets")
HEADER_JSON = os.path.join(ASSETS_DIR, "header.json")

with open(HEADER_JSON, "r") as f:
    header = json.load(f)

slide_list = header["slideList"]

print(f"Total slides: {len(slide_list)}")

for i, slide_id in enumerate(slide_list[:5]): # Check first 5 slides
    pdf_path = os.path.join(ASSETS_DIR, slide_id, "assets", f"{slide_id}.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"Slide {i} PDF not found at {pdf_path}")
        continue
        
    doc = fitz.open(pdf_path)
    print(f"\n--- Slide {i} ({slide_id}) ---")
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        images = page.get_images()
        print(f"Page {page_num} Text: {repr(text[:100])}...")
        print(f"Page {page_num} Images: {images}")
