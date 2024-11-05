import cv2
import pytesseract
import numpy as np
import re

class CardClassifier:
    def __init__(self):
        self.pan_keywords = ["Permanent Account Number Card", "PAN"]
        self.aadhaar_keywords = ["Aadhaar Number", "Aadhaar", "Government of India"]
        self.previous_frame = None

    def classify(self, frame):
        # Orient the image so the text appears top-down
        oriented_frame = self.orient_text_top_down(frame)

        if self.has_significant_change(oriented_frame):
            extracted_text = self.extract_text(oriented_frame)
            print("Extracted Text:", extracted_text)
            self.previous_frame = cv2.cvtColor(oriented_frame, cv2.COLOR_BGR2GRAY)
        else:
            print("Skipping OCR as there is no significant change.")
            extracted_text = ""

        if extracted_text and self.is_pan_card(extracted_text):
            return 'PAN'
        elif extracted_text and self.is_aadhaar_card(extracted_text):
            return 'Aadhaar'
        return None

    def orient_text_top_down(self, frame):
        try:
            # Set a manual DPI and run OSD
            frame_with_dpi = cv2.imencode('.png', frame)[1]
            image = cv2.imdecode(np.frombuffer(frame_with_dpi, np.uint8), cv2.IMREAD_COLOR)
            cv2.imwrite("temp_image_with_dpi.png", image)
            osd = pytesseract.image_to_osd("temp_image_with_dpi.png")
            rotation = int(re.search(r'Rotate: (\d+)', osd).group(1))
            print(f"Detected rotation angle: {rotation}")
            
            if rotation != 0:
                # Rotate the image to correct the orientation
                (h, w) = frame.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, -rotation, 1.0)
                oriented_frame = cv2.warpAffine(frame, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                return oriented_frame
        except pytesseract.TesseractError as e:
            rotated = self.rotate_image(frame, -90)
            extracted_text = self.extract_text(frame)
            if len(extracted_text) > 10: 
                return rotated
        return frame

    def rotate_image(self, image, angle):
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    def extract_text(self, frame):
        roi = self.detect_text_region(frame)
        if roi is None:
            return ""

        resized_roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        gray_frame = cv2.cvtColor(resized_roi, cv2.COLOR_BGR2GRAY)
        _, binary_frame = cv2.threshold(gray_frame, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        cv2.imwrite("optimized_aadhaar_region.png", binary_frame)
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(binary_frame, config=custom_config)
        return text.strip()

    def detect_text_region(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                roi = frame
                return roi
        return None

    def has_significant_change(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.previous_frame is None:
            return True
        diff = cv2.absdiff(gray_frame, self.previous_frame)
        non_zero_count = np.count_nonzero(diff)
        return non_zero_count > 10000

    def is_pan_card(self, text):
        return any(keyword in text for keyword in self.pan_keywords)

    def is_aadhaar_card(self, text):
        return any(keyword in text for keyword in self.aadhaar_keywords)
