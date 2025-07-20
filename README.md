# 🕉️ Vedic Sanskrit OCR – Ancient Manuscript Digitization

Welcome to the **Vedic Sanskrit OCR** project, a Streamlit-powered web application that allows users to upload images of ancient Sanskrit texts and extract editable, digitized text using Optical Character Recognition.

🌐 **Try the App Online**: [vedic-sanskrit-ocr.streamlit.app](https://vedic-sanskrit-ocr.streamlit.app/)

---

## 📌 Features

- Upload scanned manuscripts and Sanskrit documents.
- Preprocess images with filters for better OCR results.
- Extract Sanskrit text using state-of-the-art OCR techniques.
- Display extracted text and provide options for correction.
- Download results in plain text.

---

## 🛠️ Local Setup Instructions

### ✅ Prerequisites

Ensure you have the following installed:

- Python 3.8 or later
- `git` (to clone the repository)

---

## 💻 Setup on macOS / Windows (using virtual environment)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/vedic-sanskrit-ocr.git
cd vedic-sanskrit-ocr
2. Create a virtual environment
On macOS / Linux:
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
On Windows (Command Prompt):
cmd
Copy
Edit
python -m venv venv
venv\Scripts\activate
3. Install the dependencies
bash
Copy
Edit
pip install --upgrade pip
pip install -r requirements.txt
If requirements.txt is missing, install the essentials manually:

bash
Copy
Edit
pip install streamlit opencv-python pytesseract numpy
4. Run the app locally
bash
Copy
Edit
streamlit run sanskrit_ocr_streamlit.py
The app should now be running at http://localhost:8501

🔍 OCR Requirements
Make sure Tesseract OCR is installed and accessible:

On macOS (with Homebrew):
bash
Copy
Edit
brew install tesseract
On Windows:
Download the installer from Tesseract at UB Mannheim

Add the installation path (e.g., C:\Program Files\Tesseract-OCR) to your system environment variables.

🚀 Live App
Try it online with no setup:
👉 vedic-sanskrit-ocr.streamlit.app

🤝 Contribute
We’re actively looking for contributors to:

Improve OCR accuracy, especially for handwritten texts.

Enhance the user interface and add user-friendly tools.

Add language detection and post-processing corrections.

Feel free to fork the project, raise issues, or submit pull requests!

📜 License
This project is licensed under the MIT License. See LICENSE for more information.

🙏 Acknowledgements
Streamlit

Tesseract OCR

Open Source Sanskrit Datasets and Researchers

ॐ नमः शिवाय — Preserving ancient knowledge through modern intelligence.

yaml
Copy
Edit

---

Let me know if you want the filename changed or want a logo badge/banner added at the top.
