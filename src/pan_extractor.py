import pytesseract
import cv2
from utils import is_frame_stable, detect_pan_region
import numpy as np
import re

class PanExtractor:
    def __init__(self):
        self.last_pan_number = None
        self.angles = [0, 90, 180, 270]  # Angles to rotate the image

    def extract_pan_number(self, frame, stability_threshold=5):
        if self.is_frame_stable(frame, stability_threshold):
            pan_region = self.detect_pan_region(frame)
            if pan_region is None:
                return self.last_pan_number
            for angle in self.angles:
                rotated_region = self.rotate_image(pan_region, angle)
                processed_region = self.preprocess_region(rotated_region)
                pan_text = pytesseract.image_to_string(processed_region, config='--psm 6')
                pan_number = self.extract_pan_pattern(pan_text)
                

                # Update the last seen PAN number if a new one is detected
                if pan_number and pan_number != self.last_pan_number:
                    self.last_pan_number = pan_number
                    break  # Exit loop if PAN number is found
            return pan_number
        return None

    def preprocess_region(self, region):
        # Convert to grayscale
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        
        # Increase contrast and apply threshold
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
 
        cv2.imwrite("/home/drovco/Bhumika/CardDetectionAndClassification/preprocessed_pan_region.png", gray)

        return gray 

    def is_frame_stable(self, frame, stability_threshold):
        return True  # Assuming frame is stable for this example

    def detect_pan_region(self, frame):
        h, w = frame.shape[:2]
        pan_region = frame
        cv2.imwrite("/mnt/data/detected_pan_region.png", pan_region)
        
        return pan_region

    @staticmethod
    def extract_pan_pattern(text):
        pattern = r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'
        match = re.search(pattern, text)
        return match.group(0) if match else None

    @staticmethod
    def rotate_image(image, angle):
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_image = cv2.warpAffine(image, matrix, (w, h))
        return rotated_image