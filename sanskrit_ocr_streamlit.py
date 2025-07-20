import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image
import io
import zipfile
from typing import List, Tuple
import pandas as pd
import time

# Configure page with Vedic theme
st.set_page_config(
    page_title="🕉️ Vedic Sanskrit OCR",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Vedic theme and animations
st.markdown("""
<style>
    /* Import Sanskrit/Vedic fonts */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');
    
    /* Root variables for Vedic color scheme */
    :root {
        --vedic-gold: #DAA520;
        --vedic-saffron: #FF9933;
        --vedic-maroon: #800000;
        --vedic-cream: #FFF8DC;
        --vedic-orange: #FF8C00;
        --sacred-red: #DC143C;
        --manuscript-brown: #8B4513;
        --lotus-pink: #FFB6C1;
    }
    
    /* Main background with subtle pattern */
    .main {
        background: linear-gradient(135deg, #FFF8DC 0%, #F5DEB3 50%, #DEB887 100%);
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(218, 165, 32, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(255, 153, 51, 0.1) 0%, transparent 50%);
    }
    
    /* Sidebar Vedic styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--vedic-maroon) 0%, var(--manuscript-brown) 100%);
        border-right: 3px solid var(--vedic-gold);
    }
    
    /* Headers with Sanskrit styling */
    .main h1 {
        color: var(--vedic-maroon);
        text-align: center;
        font-family: 'Noto Sans Devanagari', serif;
        font-size: 3rem !important;
        text-shadow: 2px 2px 4px rgba(218, 165, 32, 0.3);
        margin-bottom: 2rem;
        background: linear-gradient(45deg, var(--vedic-maroon), var(--vedic-gold));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main h2 {
        color: var(--vedic-maroon);
        font-family: 'Noto Sans Devanagari', serif;
        border-bottom: 2px solid var(--vedic-gold);
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    /* Sacred Om symbol animation */
    @keyframes om-pulse {
        0%, 100% { 
            transform: scale(1); 
            filter: drop-shadow(0 0 5px var(--vedic-gold));
        }
        50% { 
            transform: scale(1.1); 
            filter: drop-shadow(0 0 15px var(--vedic-saffron));
        }
    }
    
    .om-symbol {
        font-size: 2rem;
        color: var(--vedic-gold);
        animation: om-pulse 3s ease-in-out infinite;
        display: inline-block;
        margin: 0 10px;
    }
    
    /* Scanning animation */
    @keyframes scan-line {
        0% { transform: translateX(-100%); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px var(--vedic-gold); }
        50% { box-shadow: 0 0 20px var(--vedic-saffron), 0 0 30px var(--vedic-gold); }
    }
    
    .scanning-container {
        position: relative;
        overflow: hidden;
        border: 2px solid var(--vedic-gold);
        border-radius: 10px;
        animation: glow 2s ease-in-out infinite;
    }
    
    .scan-line {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            var(--vedic-saffron) 30%, 
            var(--vedic-gold) 50%, 
            var(--vedic-saffron) 70%, 
            transparent 100%);
        animation: scan-line 2s linear infinite;
        z-index: 10;
    }
    
    /* Progress bar Vedic styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--vedic-saffron), var(--vedic-gold)) !important;
        height: 8px !important;
        border-radius: 4px !important;
    }
    
    /* Buttons with Vedic styling */
    .stButton > button {
        background: linear-gradient(45deg, var(--vedic-maroon), var(--manuscript-brown));
        color: var(--vedic-cream);
        border: 2px solid var(--vedic-gold);
        border-radius: 25px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        font-family: 'Noto Sans Devanagari', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(218, 165, 32, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, var(--vedic-gold), var(--vedic-saffron));
        color: var(--vedic-maroon);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(218, 165, 32, 0.5);
    }
    
    /* Info/Success boxes with Vedic styling */
    .stAlert {
        border-left: 4px solid var(--vedic-gold) !important;
        background: rgba(255, 248, 220, 0.9) !important;
        border-radius: 0 10px 10px 0 !important;
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: rgba(255, 248, 220, 0.7);
        border: 2px dashed var(--vedic-gold);
        border-radius: 15px;
        padding: 2rem;
    }
    
    /* Expandable sections */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, var(--vedic-cream), rgba(218, 165, 32, 0.1));
        border: 1px solid var(--vedic-gold);
        border-radius: 10px;
        color: var(--vedic-maroon) !important;
        font-weight: 600;
    }
    
    /* Text areas for Sanskrit text */
    .stTextArea textarea {
        font-family: 'Noto Sans Devanagari', monospace;
        font-size: 16px;
        line-height: 1.6;
        background: rgba(255, 248, 220, 0.9);
        border: 2px solid var(--vedic-gold);
        border-radius: 10px;
    }
    
    /* Code blocks for Sanskrit */
    .stCodeBlock {
        background: rgba(139, 69, 19, 0.1) !important;
        border: 1px solid var(--vedic-gold) !important;
        border-radius: 10px !important;
    }
    
    .stCodeBlock code {
        font-family: 'Noto Sans Devanagari', monospace !important;
        color: var(--vedic-maroon) !important;
        font-size: 16px !important;
        line-height: 1.8 !important;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--vedic-maroon), var(--manuscript-brown));
        color: var(--vedic-cream);
    }
    
    /* Sanskrit text styling */
    .sanskrit-text {
        font-family: 'Noto Sans Devanagari', serif;
        font-size: 1.2rem;
        line-height: 1.8;
        color: var(--vedic-maroon);
        text-align: center;
        padding: 1rem;
        background: rgba(255, 248, 220, 0.8);
        border-radius: 10px;
        border: 1px solid var(--vedic-gold);
        margin: 1rem 0;
    }
    
    /* Confidence indicators */
    .confidence-high { color: #228B22; font-weight: bold; }
    .confidence-medium { color: #FF8C00; font-weight: bold; }
    .confidence-low { color: #DC143C; font-weight: bold; }
    
    /* Lotus decoration */
    .lotus-decoration {
        text-align: center;
        font-size: 1.5rem;
        color: var(--lotus-pink);
        margin: 1rem 0;
        opacity: 0.7;
    }
    
    /* Processing animation */
    @keyframes processing {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .processing-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid var(--vedic-gold);
        border-top: 2px solid var(--vedic-saffron);
        border-radius: 50%;
        animation: processing 1s linear infinite;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

class VedicSanskritOCR:
    """Vedic Sanskrit OCR processor class with specialized handling"""
    
    def __init__(self):
        self.supported_formats = ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp']
        # Vedic-specific accent marks and characters
        self.vedic_chars = {
            'udatta': '॒',  # Acute accent
            'anudatta': '॑',  # Grave accent  
            'svarita': '᳚',  # Circumflex accent
            'anusvara': 'ं',
            'visarga': 'ः',
            'jihvamuliya': 'ᳵ',
            'upadhmaniya': 'ᳶ'
        }
    
    def preprocess_image(self, image: np.ndarray, preprocessing_option: str = 'vedic_optimized') -> np.ndarray:
        """Apply preprocessing optimized for Vedic Sanskrit texts"""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        if preprocessing_option == 'vedic_optimized':
            # Multi-step preprocessing optimized for Vedic texts
            # 1. Denoise first to handle manuscript artifacts
            denoised = cv2.fastNlMeansDenoising(gray, h=10)
            
            # 2. Enhance contrast for faded manuscripts
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)
            
            # 3. Apply adaptive threshold for varying ink density
            processed = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 15, 4)
            
        elif preprocessing_option == 'manuscript':
            # For aged manuscript processing
            # Morphological operations to connect broken characters
            kernel = np.ones((2,2), np.uint8)
            denoised = cv2.fastNlMeansDenoising(gray, h=15)
            processed = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
            _, processed = cv2.threshold(processed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
        elif preprocessing_option == 'accent_preserve':
            # Gentle processing to preserve accent marks
            processed = cv2.bilateralFilter(gray, 9, 75, 75)
            _, processed = cv2.threshold(processed, 140, 255, cv2.THRESH_BINARY)
            
        elif preprocessing_option == 'threshold':
            # Apply binary thresholding
            _, processed = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        elif preprocessing_option == 'adaptive':
            # Apply adaptive thresholding
            processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 11, 2)
        elif preprocessing_option == 'denoise':
            # Apply denoising
            processed = cv2.fastNlMeansDenoising(gray)
        elif preprocessing_option == 'enhance':
            # Enhance contrast
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            processed = clahe.apply(gray)
        else:  # auto
            # Apply OTSU thresholding (usually works well)
            _, processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return processed
    
    def recognize_text(self, image: np.ndarray, preprocessing: str = 'vedic_optimized', 
                      custom_config: str = '', text_type: str = 'vedic') -> Tuple[str, float]:
        """Recognize Vedic Sanskrit text from image"""
        try:
            # Preprocess image
            processed_img = self.preprocess_image(image, preprocessing)
            
            # Vedic-specific Tesseract configurations
            vedic_configs = {
                'vedic': '--oem 3 --psm 6 -c preserve_interword_spaces=1 -c tessedit_char_whitelist=अआइईउऊऋॠऌॡएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह।॥ं॒॑᳚ः०१२३४५६७८९ ',
                'manuscript': '--oem 3 --psm 4 -c preserve_interword_spaces=1',
                'verse': '--oem 3 --psm 6 -c preserve_interword_spaces=1',
                'prose': '--oem 3 --psm 12 -c preserve_interword_spaces=1'
            }
            
            # Use custom config or predefined vedic config
            if custom_config:
                config = custom_config
            else:
                config = vedic_configs.get(text_type, vedic_configs['vedic'])
            
            # Perform OCR with Sanskrit language
            text = pytesseract.image_to_string(processed_img, lang='san', config=config)
            
            # Post-process for Vedic text
            text = self.post_process_vedic_text(text)
            
            # Get confidence score
            data = pytesseract.image_to_data(processed_img, lang='san', config=config, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return text.strip(), avg_confidence
            
        except Exception as e:
            return f"Error during OCR: {str(e)}", 0.0
    
    def post_process_vedic_text(self, text: str) -> str:
        """Post-process text to improve Vedic Sanskrit accuracy"""
        # Remove extra spaces and normalize
        text = ' '.join(text.split())
        
        # Common OCR corrections for Vedic text
        corrections = {
            # Common misreadings
            'ॐ': 'ओम्',  # Om symbol correction
            '।।': '॥',   # Double danda
            'र्': 'र्',    # Ensure proper ra-halanta
            'ज्ञ': 'ज्ञ',   # Correct jña
        }
        
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        
        # Preserve traditional spacing and punctuation
        text = text.replace(' । ', ' ।\n')  # Line break after single danda
        text = text.replace(' ॥ ', ' ॥\n\n')  # Double line break after double danda
        
        return text

def create_scanning_animation():
    """Create animated scanning effect"""
    return """
    <div class="scanning-container">
        <div class="scan-line"></div>
        <div style="padding: 20px; text-align: center; background: rgba(255,248,220,0.1);">
            <div class="processing-spinner"></div>
            <span style="color: var(--vedic-maroon); font-family: 'Noto Sans Devanagari', sans-serif;">
                प्रक्रिया चलित... (Processing in progress...)
            </span>
        </div>
    </div>
    """

def main():
    # Sacred header with Om symbols
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <span class="om-symbol">🕉️</span>
        <span style="font-family: 'Noto Sans Devanagari', serif; font-size: 3rem; 
               background: linear-gradient(45deg, #800000, #DAA520); 
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               text-shadow: 2px 2px 4px rgba(218, 165, 32, 0.3);">
            वैदिक संस्कृत OCR
        </span>
        <span class="om-symbol">🕉️</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; color: #800000; font-family: 'Noto Sans Devanagari', serif; 
               font-size: 1.2rem; margin-bottom: 2rem;">
        सत्यं ज्ञानमनन्तम् | Upload Vedic texts and manuscripts for sacred digitization
    </div>
    """, unsafe_allow_html=True)
    
    # Lotus decoration
    st.markdown('<div class="lotus-decoration">🪷 ॐ गं गणपतये नमः ॐ 🪷</div>', unsafe_allow_html=True)
    
    # Initialize OCR processor
    ocr_processor = VedicSanskritOCR()
    
    # Sidebar for configuration
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; color: #FFF8DC;">
        <span style="font-size: 2rem;">🕉️</span><br>
        <span style="font-family: 'Noto Sans Devanagari', serif; font-size: 1.5rem;">
            OCR सेटिंग्स
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Text type selection
    text_type = st.sidebar.selectbox(
        "📜 Text Type | ग्रन्थ प्रकार",
        ['vedic', 'manuscript', 'verse', 'prose'],
        help="Choose the type of Vedic text for optimized recognition"
    )
    
    # Preprocessing options for Vedic texts
    preprocessing_option = st.sidebar.selectbox(
        "⚙️ Preprocessing | पूर्व-प्रक्रिया",
        ['vedic_optimized', 'manuscript', 'accent_preserve', 'threshold', 'adaptive', 'denoise', 'enhance'],
        help="Choose preprocessing method optimized for different Vedic text conditions"
    )
    
    # Advanced Tesseract configuration
    with st.sidebar.expander("🔧 Advanced Settings | उन्नत सेटिंग्स"):
        custom_config = st.text_input(
            "Custom Tesseract Config",
            placeholder="--oem 3 --psm 6",
            help="Custom Tesseract configuration parameters"
        )
        
        show_preprocessed = st.checkbox("Show Preprocessed Images", value=False)
        show_confidence = st.checkbox("Show Confidence Scores", value=True)
        preserve_formatting = st.checkbox("Preserve Traditional Formatting", value=True)
    
    # Sacred divider
    st.markdown('<div class="lotus-decoration">🌸 ॐ 🌸</div>', unsafe_allow_html=True)
    
    # File upload section
    st.markdown("""
    <h2 style="text-align: center; color: #800000; font-family: 'Noto Sans Devanagari', serif;">
        📁 Upload Vedic Texts | वैदिक ग्रन्थ अपलोड करें
    </h2>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose Vedic Sanskrit text images or manuscript photos",
        type=ocr_processor.supported_formats,
        accept_multiple_files=True,
        help="Upload images of Vedic texts, manuscripts, or printed materials"
    )
    
    if uploaded_files:
        st.success(f"🎯 Uploaded {len(uploaded_files)} sacred text(s) | {len(uploaded_files)} पवित्र ग्रन्थ अपलोड किए गए")
        
        # Processing options
        col1, col2 = st.columns([1, 1])
        
        with col1:
            process_all = st.button("🚀 Process All Images | सभी चित्र संसाधित करें", type="primary")
        
        with col2:
            if len(uploaded_files) > 1:
                download_results = st.checkbox("📥 Prepare Download Package", value=True)
            else:
                download_results = False
        
        # Process images
        if process_all:
            # Show scanning animation
            scanning_placeholder = st.empty()
            scanning_placeholder.markdown(create_scanning_animation(), unsafe_allow_html=True)
            
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, uploaded_file in enumerate(uploaded_files):
                status_text.markdown(f"""
                <div style="text-align: center; color: #800000; font-family: 'Noto Sans Devanagari', sans-serif;">
                    <div class="processing-spinner"></div>
                    Processing {uploaded_file.name} | {uploaded_file.name} संसाधित किया जा रहा...
                </div>
                """, unsafe_allow_html=True)
                
                # Load image
                image = Image.open(uploaded_file)
                img_array = np.array(image)
                
                # Simulate processing time for animation effect
                time.sleep(0.5)
                
                # Perform OCR
                recognized_text, confidence = ocr_processor.recognize_text(
                    img_array, preprocessing_option, custom_config, text_type
                )
                
                results.append({
                    'filename': uploaded_file.name,
                    'text': recognized_text,
                    'confidence': confidence,
                    'image': img_array
                })
                
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            # Clear scanning animation
            scanning_placeholder.empty()
            
            status_text.markdown("""
            <div style="text-align: center; color: #228B22; font-family: 'Noto Sans Devanagari', sans-serif; font-size: 1.2rem;">
                ✅ Processing complete! | प्रक्रिया पूर्ण!
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="lotus-decoration">🪷 सर्वम् सिद्धम् 🪷</div>', unsafe_allow_html=True)
            
            # Display results
            st.markdown("""
            <h2 style="text-align: center; color: #800000; font-family: 'Noto Sans Devanagari', serif;">
                📊 Results | परिणाम
            </h2>
            """, unsafe_allow_html=True)
            
            for idx, result in enumerate(results):
                with st.expander(f"📄 {result['filename']}", expanded=len(results) == 1):
                    
                    col1, col2 = st.columns([1, 2] if show_preprocessed else [1, 3])
                    
                    with col1:
                        # Image display with sacred border
                        st.markdown("""
                        <div style="border: 3px solid #DAA520; border-radius: 10px; padding: 5px; background: rgba(255,248,220,0.3);">
                        """, unsafe_allow_html=True)
                        st.image(result['image'], caption="Original Sacred Text", use_column_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        if show_preprocessed:
                            preprocessed = ocr_processor.preprocess_image(result['image'], preprocessing_option)
                            st.markdown("""
                            <div style="border: 2px solid #FF9933; border-radius: 10px; padding: 5px; margin-top: 10px;">
                            """, unsafe_allow_html=True)
                            st.image(preprocessed, caption="Preprocessed", use_column_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col2:
                        if show_confidence:
                            if result['confidence'] > 70:
                                conf_class = "confidence-high"
                                conf_emoji = "🟢"
                            elif result['confidence'] > 40:
                                conf_class = "confidence-medium"
                                conf_emoji = "🟡"
                            else:
                                conf_class = "confidence-low"
                                conf_emoji = "🔴"
                            
                            st.markdown(f"""
                            <div style="text-align: center; margin: 1rem 0;">
                                <span class="{conf_class}">
                                    {conf_emoji} Confidence | विश्वसनीयता: {result['confidence']:.1f}%
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("""
                        <h3 style="color: #800000; font-family: 'Noto Sans Devanagari', serif; text-align: center;">
                            Recognized Vedic Sanskrit Text | पहचाना गया वैदिक संस्कृत पाठ:
                        </h3>
                        """, unsafe_allow_html=True)
                        
                        if result['text']:
                            # Display with proper formatting for Vedic texts
                            if preserve_formatting:
                                st.markdown(f"""
                                <div class="sanskrit-text">
                                    {result['text']}
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.text_area(
                                    f"Text from {result['filename']}",
                                    result['text'],
                                    height=200,
                                    key=f"text_{idx}"
                                )
                            
                            # Copy button (using code block for easy copying)
                            if st.button(f"📋 Show Copyable Text | प्रतिलिपि योग्य पाठ", key=f"copy_{idx}"):
                                st.code(result['text'], language=None)
                        else:
                            st.warning("No text detected. Try different preprocessing options. | कोई पाठ नहीं मिला। विभिन्न पूर्व-प्रक्रिया विकल्प आज़माएं।")
            
            # Download package
            if download_results and len(results) > 1:
                st.markdown("""
                <h2 style="color: #800000; font-family: 'Noto Sans Devanagari', serif;">
                    📥 Download Results | परिणाम डाउनलोड करें
                </h2>
                """, unsafe_allow_html=True)
                
                # Create results summary
                summary_data = []
                for result in results:
                    summary_data.append({
                        'Filename': result['filename'],
                        'Text Length': len(result['text']),
                        'Confidence': f"{result['confidence']:.1f}%",
                        'Status': '✅ Success' if result['text'] else '❌ No text detected'
                    })
                
                # Show summary table
                df = pd.DataFrame(summary_data)
                st.dataframe(df, use_container_width=True)
                
                # Create download package
                if st.button("📦 Generate Sacred Text Package | पवित्र ग्रन्थ पैकेज बनाएं"):
                    zip_buffer = io.BytesIO()
                    
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        # Add text files
                        for result in results:
                            if result['text']:
                                txt_filename = f"{result['filename'].rsplit('.', 1)[0]}.txt"
                                zip_file.writestr(txt_filename, result['text'])
                        
                        # Add summary CSV
                        csv_buffer = io.StringIO()
                        df.to_csv(csv_buffer, index=