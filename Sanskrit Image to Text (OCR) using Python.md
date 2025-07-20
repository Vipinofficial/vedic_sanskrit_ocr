## Sanskrit Image to Text (OCR) using Python

This project provides a Python-based solution for performing Optical Character Recognition (OCR) on images containing Sanskrit text, specifically in the Devanagari script.

### Prerequisites

Before running the application, ensure you have the following installed:

-   **Tesseract OCR Engine**: This is the core OCR engine. You can install it using your system's package manager.
    For Debian/Ubuntu:
    ```bash
    sudo apt update
    sudo apt install -y tesseract-ocr
    sudo apt install -y tesseract-ocr-san
    ```

-   **Python 3**: Make sure you have Python 3 installed.

-   **Python Libraries**: Install the required Python libraries using pip:
    ```bash
    pip install pytesseract opencv-python
    ```

### How to Use

1.  **Save the Python script**: Save the provided `sanskrit_ocr.py` file to your local machine.

2.  **Prepare your image**: Place the image file containing Sanskrit text (e.g., `sanskrit_test.png`) in the same directory as the `sanskrit_ocr.py` script, or update the `image_path` variable in the script to point to your image.

3.  **Run the script**: Open a terminal or command prompt, navigate to the directory where you saved the files, and run the script using Python:
    ```bash
    python3 sanskrit_ocr.py
    ```

    The script will output the recognized Sanskrit text to the console.

### `sanskrit_ocr.py` Code

```python
import cv2
import pytesseract

def recognize_sanskrit_text(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(thresh, lang=\'san\')
    return text

if __name__ == \'__main__\':
    recognized_text = recognize_sanskrit_text(\'sanskrit_test.png\')
    print(f"Recognized Sanskrit Text:\n{recognized_text}")

```

### Example

If you use the `sanskrit_test.png` image (which contains the text "नमस्ते"), the output will be:

```
Recognized Sanskrit Text:
नमस्ते
```


