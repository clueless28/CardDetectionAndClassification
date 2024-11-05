import gradio as gr
import cv2
import os
from card_classifier import CardClassifier
from pan_extractor import PanExtractor

class CardDetectionApp:
    def __init__(self):
        self.classifier = CardClassifier()
        self.pan_extractor = PanExtractor()
        self.default_videos = [
           ("pan_normal", "signal-2024-10-30-170812_002.mp4"),
           ("pan_blurred", "pan_blur.mp4"),
           ("aadhar", "aadhar.mp4")

        ]
        self.default_video_names = [name for name, _ in self.default_videos]

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        processed_frames = []  # List to hold frames with PAN numbers
        frame_count = 0 
        print("here", video_path)
        while cap.isOpened() and frame_count < 10:
            ret, frame = cap.read()
            if not ret:
                break
            card_type = self.classifier.classify(frame)
            if card_type == 'PAN':
                pan_number = self.pan_extractor.extract_pan_number(frame)
                if pan_number:
                    cv2.putText(frame, f"PAN: {pan_number}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif card_type == 'Aadhaar':
                cv2.putText(frame, "Aadhaar Card", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Convert the frame to RGB format for Gradio
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_frames.append(frame_rgb)
            
            frame_count += 1

        cap.release()
        print(f"Processed {len(processed_frames)} frames.") 
        return processed_frames  # Return the list of processed frames

    def process_uploaded_video(self, video_file):
        return self.process_video(video_file)

    def process_selected_video(self, selected_video):
        # Get the full path of the selected video
        video_path = next((path for name, path in self.default_videos if name == selected_video), None)
        if video_path:
            return self.process_video(video_path)
        else:
            print(f"Video not found for selection: {selected_video}")
            return []

app = CardDetectionApp()

def process_selection(uploaded_video, selected_video):
    if uploaded_video:
        return app.process_uploaded_video(uploaded_video)
    elif selected_video:
        return app.process_selected_video(selected_video)
    else:
        return []

with gr.Blocks() as demo:
    gr.Markdown("### Card Detection App")
    gr.Markdown("Upload a video (max 30 seconds) to detect PAN or Aadhaar cards.")
    
    upload_button = gr.File(label="Upload a Video", type="filepath")
    video_dropdown = gr.Dropdown(choices=app.default_video_names, label="Select a Default Video")
    output_gallery = gr.Gallery(label="Processed Frames with Card Detection", height=200, scale=2)

    process_button = gr.Button("Process Video")
    process_button.click(
        fn=process_selection,
        inputs=[upload_button, video_dropdown],
        outputs=output_gallery,
        show_progress=True  # Enable progress to see real-time updates
    )

demo.launch(share=True)
