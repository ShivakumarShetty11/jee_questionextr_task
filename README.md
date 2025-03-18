# Question Extraction from PDF to JSON

## 📌 Overview
This project extracts questions from a **PDF document**, detects their type (**MCQ, Fill in the Blanks, Open-ended**), and saves them in a **structured JSON format**. It uses **OCR (EasyOCR)** and **Image Processing (OpenCV)** to recognize and process text.

## 🚀 Features
- Extracts **questions** from a PDF document
- Identifies **MCQs, Fill in the Blanks, and Open-ended** questions
- Saves extracted questions as **JSON**
- Handles OCR failures by saving unreadable images
- Uses **EasyOCR** for text recognition
- Uses **pdf2image** for PDF conversion

---

## 📂 Project Structure
```
📁 question_extraction_project
│-- 📁 questions_images          # Extracted question images
│-- 📁 failed_extractions        # Images where OCR failed
│-- 📄 main.py                   # Main script for processing
│-- 📄 requirements.txt          # Python dependencies
│-- 📄 README.md                 # Documentation (this file)
│-- 📄 questions_data.json       # Extracted questions in JSON
```

---

## 🛠️ Installation
### 1️⃣ Install Python (if not installed)
Make sure you have **Python 3.8+** installed.

### 2️⃣ Install Required Dependencies
```sh
pip install -r requirements.txt
```

#### `requirements.txt` includes:
```
numpy
opencv-python
easyocr
pdf2image
Pillow
```

### 3️⃣ Install Poppler (For PDF to Image Conversion)
#### 🔹 Windows
- Download from: [https://github.com/oschwartz10612/poppler-windows/releases](https://github.com/oschwartz10612/poppler-windows/releases)
- Extract and add the **bin** folder to your system PATH

#### 🔹 macOS (via Homebrew)
```sh
brew install poppler
```

#### 🔹 Linux (Ubuntu/Debian)
```sh
sudo apt install poppler-utils
```

---

## 📜 How It Works
### 📝 Step 1: Convert PDF to Images
- The script **converts each PDF page into an image** using `pdf2image`
- Saves images in `questions_images/`

### 🔍 Step 2: Detect Questions using OCR
- Uses `EasyOCR` to **detect and extract text** from each image
- Finds **question numbers** (`Q.1`, `Q 2`, etc.)
- Identifies **answer choices** (A, B, C, D)

### 🧠 Step 3: Classify Question Type
- **MCQ**: If it contains choices `(A)`, `(B)`, `(C)`, `(D)`
- **Fill in the Blanks**: If it contains underscores (`_____`) or "fill in the blank"
- **Open-ended**: If it doesn't match the above two

### 📊 Step 4: Save Extracted Data to JSON
- Extracted questions are saved in `questions_data.json`
- If OCR fails, the image is saved in `failed_extractions/`

---

## 🏃 Running the Script
```sh
python main.py
```

### ✅ Example JSON Output
```json
{
    "questions": [
        {
            "question_id": "1",
            "question_type": "MCQ",
            "question_text": "Which of the following is correct?",
            "answer_choices": {
                "A": "Option 1",
                "B": "Option 2",
                "C": "Option 3",
                "D": "Option 4"
            },
            "correct_answer": null,
            "image": "question_1.png"
        },
        {
            "question_id": "5",
            "question_type": "Fill in the Blanks",
            "question_text": "The value of x is _____ when y is 5.",
            "answer_choices": null,
            "correct_answer": null,
            "image": "question_5.png"
        },
        {
            "question_id": "8",
            "question_type": "Open-ended",
            "question_text": "Explain the process of nuclear fission.",
            "answer_choices": null,
            "correct_answer": null,
            "image": "question_8.png"
        }
    ]
}
```

---

## 📌 Next Steps / Improvements 
✅ Implement answer key matching (if provided)  

