# 🕉️ Vedic Sanskrit OCR

A Streamlit-based web application for Optical Character Recognition (OCR) of Vedic Sanskrit texts. This project helps digitize ancient manuscripts, allowing easy access and preservation of our cultural heritage.

🌐 **Try it online**: [https://vedic-sanskrit-ocr.streamlit.app](https://vedic-sanskrit-ocr.streamlit.app)

---

## ✨ Features

- Upload scanned images of Vedic Sanskrit manuscripts.
- Perform image preprocessing (grayscale, thresholding, noise removal, etc.).
- OCR using trained models.
- View extracted text and download results.
- Simple and responsive web UI built with Streamlit.

---

## 🛠️ Setup Instructions

You can run this project on both **macOS** and **Windows** using Python and virtual environments.

---

### 💻 Prerequisites

- Python ≥ 3.8
- Git
- pip (Python package manager)
- Virtualenv (recommended)

---

### 🧪 Setup on macOS / Linux

```bash
# Clone the repository
git clone https://github.com/yourusername/vedic-sanskrit-ocr.git
cd vedic-sanskrit-ocr

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run sanskrit_ocr_streamlit.py

```
### Setup on Windows
```bash
# Clone the repository
git clone https://github.com/yourusername/vedic-sanskrit-ocr.git
cd vedic-sanskrit-ocr

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run sanskrit_ocr_streamlit.py
```

vedic-sanskrit-ocr/
│
├── sanskrit_ocr_streamlit.py   # Main Streamlit app
├── requirements.txt            # Python dependencies
├── model/                      # Saved ML models
├── utils/                      # Preprocessing scripts
├── assets/                     # Sample images and icons
└── README.md                   # Project documentation
