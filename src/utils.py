import cv2
import numpy as np

def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return blurred

def is_frame_stable(frame, threshold=5):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if hasattr(is_frame_stable, 'last_frame'):
        diff = cv2.absdiff(gray, is_frame_stable.last_frame)
        non_zero_count = np.count_nonzero(diff)
        if non_zero_count < threshold:
            return True
    is_frame_stable.last_frame = gray
    return False

def detect_pan_region(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 30, 150)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # Adjust area threshold as needed
            x, y, w, h = cv2.boundingRect(contour)
            roi = frame[y:y+h, x:x+w]
            return roi  # Return the region of interest for OCR
    return None
