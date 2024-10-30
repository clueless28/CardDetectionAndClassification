import pytesseract
import cv2
from utils import is_frame_stable, detect_pan_region

class PanExtractor:
    def __init__(self):
        self.last_pan_number = None

    def extract_pan_number(self, frame, stability_threshold=5):
        if is_frame_stable(frame, stability_threshold):
            pan_region = detect_pan_region(frame)
            if pan_region is None:
                return self.last_pan_number
            
            pan_text = pytesseract.image_to_string(pan_region, config='--psm 6')
            pan_number = self.extract_pan_pattern(pan_text)
            if pan_number and pan_number != self.last_pan_number:
                self.last_pan_number = pan_number
            return pan_number
        return None

    @staticmethod
    def extract_pan_pattern(text):
        import re
        pattern = r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'  # PAN format regex
        match = re.search(pattern, text)
        return match.group(0) if match else None
