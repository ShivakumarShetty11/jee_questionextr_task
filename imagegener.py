import cv2
import numpy as np
import easyocr
from pdf2image import convert_from_path
import os

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])  # English language

# Input PDF and output directory
pdf_path = r"C:\Users\SHIVA KUMAR\Documents\projects\jee_questionextr_task\2024_1_English.pdf"
  # Change this to your PDF file path
output_folder = "questions_images"
os.makedirs(output_folder, exist_ok=True)

# Set Poppler Path Manually (Change this based on your system)
poppler_path = r"C:\poppler-24.08.0\Library\bin"  # Update this path if necessary

# Convert PDF pages to images using Poppler
pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)

# Process each page
for page_num, page in enumerate(pages):
    img_path = f"{output_folder}/page_{page_num+1}.png"
    page.save(img_path, "PNG")

    # Load image
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use EasyOCR to detect text
    results = reader.readtext(gray)

    # Extract text and positions
    extracted_text = []
    question_positions = []

    for (bbox, text, prob) in results:
        extracted_text.append(text)
        if text.strip().startswith("Q.") or text.strip().startswith("Q "):  # Detect question numbers
            y_position = int(bbox[0][1])  # Get Y coordinate of top-left corner
            question_positions.append(y_position)

    # Crop and save each question
    for i in range(len(question_positions)):
        y1 = question_positions[i]
        y2 = question_positions[i+1] if i + 1 < len(question_positions) else img.shape[0]  # End of page for last question
        
        question_img = img[y1:y2, :]  # Crop the question
        q_img_path = f"{output_folder}/question_{page_num+1}_{i+1}.png"
        cv2.imwrite(q_img_path, question_img)

print("✅ Questions extracted and saved as separate images.")
