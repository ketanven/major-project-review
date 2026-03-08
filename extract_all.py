import fitz
import os
import json

HTML_DIR = "/Users/ketanpillai/Documents/Major_Project_3rd_review.html"
ASSETS_DIR = os.path.join(HTML_DIR, "assets")
HEADER_JSON = os.path.join(ASSETS_DIR, "header.json")
EXTRACTED_DIR = os.path.join(HTML_DIR, "extracted_assets")

if not os.path.exists(EXTRACTED_DIR):
    os.makedirs(EXTRACTED_DIR)

with open(HEADER_JSON, "r") as f:
    header = json.load(f)

slide_list = header["slideList"]
content_data = []

image_counter = 0

for i, slide_id in enumerate(slide_list):
    pdf_path = os.path.join(ASSETS_DIR, slide_id, "assets", f"{slide_id}.pdf")
    if not os.path.exists(pdf_path):
        continue
        
    doc = fitz.open(pdf_path)
    # We'll take the text from the LAST page of the slide, which usually contains all bullets built-in
    last_page = doc.load_page(doc.page_count - 1)
    text = last_page.get_text()
    
    # Extract images from all pages of this slide to be safe, but avoid duplicates
    slide_images = []
    seen_xrefs = set()
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for img in page.get_images():
            xref = img[0]
            if xref not in seen_xrefs:
                seen_xrefs.add(xref)
                try:
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    img_ext = base_image["ext"]
                    # filter out very small background UI elements if any?
                    if len(image_bytes) > 5000: # only images > 5KB
                        img_filename = f"img_{i}_{xref}.{img_ext}"
                        with open(os.path.join(EXTRACTED_DIR, img_filename), "wb") as img_file:
                            img_file.write(image_bytes)
                        slide_images.append(img_filename)
                except Exception as e:
                    pass
                    
    content_data.append({
        "slide_index": i,
        "text": text.strip(),
        "images": slide_images
    })

with open(os.path.join(HTML_DIR, "extracted_content.json"), "w") as f:
    json.dump(content_data, f, indent=2)

print(f"Extracted content for {len(content_data)} slides.")
