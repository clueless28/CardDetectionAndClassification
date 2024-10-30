import cv2
import pytesseract

class CardClassifier:
    def __init__(self):
        # Define keywords for PAN and Aadhaar cards
        self.pan_keywords = ["Permanent Account Number", "PAN"]
        self.aadhaar_keywords = ["Aadhaar Number", "Aadhaar"]

    def classify(self, frame):
        # Use OCR to extract text from the frame
        extracted_text = self.extract_text(frame)

        # Check if extracted text contains keywords for PAN or Aadhaar
        if self.is_pan_card(extracted_text):
            return 'PAN'
        elif self.is_aadhaar_card(extracted_text):
            return 'Aadhaar'
        
        return None

    def extract_text(self, frame):
        # Preprocess frame for better OCR results
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        _, binary_frame = cv2.threshold(blurred_frame, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Use Tesseract to perform OCR
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(binary_frame, config=custom_config)
        return text.strip()  # Clean up any leading/trailing whitespace

    def is_pan_card(self, text):
        # Check if any PAN keywords are in the extracted text
        return any(keyword in text for keyword in self.pan_keywords)

    def is_aadhaar_card(self, text):
        # Check if any Aadhaar keywords are in the extracted text
        return any(keyword in text for keyword in self.aadhaar_keywords)
