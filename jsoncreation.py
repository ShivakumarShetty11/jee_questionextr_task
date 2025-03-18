import os
import easyocr
import json
import re
import cv2
import numpy as np

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Input and output directories
input_folder = "questions_images"
output_folder = "failed_extractions"  
output_json = "questions_data.json"
os.makedirs(output_folder, exist_ok=True)

# Function to process each question image
def process_question_image(image_path):
    results = reader.readtext(image_path)
    extracted_text = " ".join([text for (_, text, _) in results]) if results else ""

    # Extract question ID (supports multiple formats)
    question_id_match = re.search(r'(?:Q[.\s]?|^)(\d+)', extracted_text)
    question_id = question_id_match.group(1) if question_id_match else None

    # Detect answer choices
    options_start = re.search(r'\(A\)|\(B\)|\(C\)|\(D\)', extracted_text)
    question_text = extracted_text[:options_start.start()].strip() if options_start else extracted_text.strip()
    question_text = question_text if question_text else None  

    # Extract answer choices
    options = {}
    options_matches = re.findall(r'[(]?([A-D1-4])[).]\s(.*?)(?=\s[(]?[A-D1-4][).]|$)', extracted_text)
    for option in options_matches:
        options[option[0]] = option[1].strip()

    answer_choices = options if options else None  

    # 🔥 Classify Question Type  
    if answer_choices:
        question_type = "MCQ"
    elif re.search(r'_{2,}|\bfill\s?in\s?the\s?blank\b', extracted_text):  # Matches "____" or "fill in the blank"
        question_type = "Fill in the Blanks"
    else:
        question_type = "Open-ended"  

    # Save image if OCR fails
    if not question_text or len(question_text) < 10:
        failed_image_path = os.path.join(output_folder, os.path.basename(image_path))
        save_failed_image(image_path, failed_image_path)
        return {
            "question_id": question_id,
            "question_type": None,
            "question_text": None,
            "answer_choices": None,
            "correct_answer": None,
            "image": failed_image_path  
        }

    # Return structured question data
    return {
        "question_id": question_id,
        "question_type": question_type,  # Now includes MCQ, Fill in the Blanks, or Open-ended
        "question_text": question_text,
        "answer_choices": answer_choices,
        "correct_answer": None,  
        "image": os.path.basename(image_path) if image_path else None
    }

# Function to save images where OCR failed
def save_failed_image(original_path, failed_path):
    image = cv2.imread(original_path)
    if image is not None:
        cv2.imwrite(failed_path, image)
        print(f"❌ OCR Failed: Saved {failed_path}")

# Process all images
questions_data = []
for image_file in sorted(os.listdir(input_folder)):
    if image_file.endswith(".png") or image_file.endswith(".jpg"):
        image_path = os.path.join(input_folder, image_file)
        question_data = process_question_image(image_path)
        questions_data.append(question_data)

# Save JSON output
with open(output_json, "w", encoding="utf-8") as json_file:
    json.dump({"questions": questions_data}, json_file, indent=4)

print(f"✅ Extracted data saved to {output_json}")
