import cv2
from card_classifier import CardClassifier
from pan_extractor import PanExtractor

class CardDetectionApp:
    def __init__(self, video_path):
        self.video_path = video_path
        self.classifier = CardClassifier()
        self.pan_extractor = PanExtractor()
    
    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            card_type = self.classifier.classify(frame)
            if card_type == 'PAN':
                pan_number = self.pan_extractor.extract_pan_number(frame)
                print(f"PAN Card Detected - PAN Number: {pan_number}")
                cv2.putText(frame, f"PAN: {pan_number}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif card_type == 'Aadhaar':
                print("Aadhaar Card Detected")
                cv2.putText(frame, "Aadhaar Card", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow('Card Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = CardDetectionApp("data/sample_video.mp4")
    app.run()
