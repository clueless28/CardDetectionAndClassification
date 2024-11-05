# CardDetectionAndClassification
A Python application to detect and classify cards (PAN and Aadhaar) in video frames, with OCR-optimized PAN extraction.

## Objective
The goal of this project is to develop a Computer Vision model capable of:
1. Detecting the presence of a card in an image or video.
2. Classifying the detected card as either a PAN card or an Aadhaar card.
3. Extracting the PAN number from the PAN card while minimizing the number of OCR (Optical Character Recognition) calls.

### Key Consideration while developing the solution, 
1. Variability in card appearance, including slight obstructions and tilts.
2. Different lighting conditions affect the image quality.
3. The requirement to extract text accurately from potentially low-quality images, specifically for PAN cards.
4. Minimizing the number of OCR calls to improve efficiency and reduce processing time.

## Functional Requirements
1. The system should be able to process a video input of up to 30 seconds (minimum 720p resolution).
2. It should detect the presence of a card in video frames.
3. It should classify the card as either a PAN card or an Aadhaar card.
4. If a PAN card is detected, the system should extract the PAN number and display it.

## Non-Functional Requirements
1. The model must handle various orientations and partial obstructions.
2. It should operate efficiently in real-time.
3. The solution should maintain high accuracy in detection and classification.

## Architecture
The solution consists of several components:
1. Video Processing Module: Captures frames from the input video.
2. Card Classifier: Classifies detected cards as PAN or Aadhaar.
3. PAN Extractor: Extracts PAN numbers from detected PAN cards.
4. User Interface: Utilizes Gradio to provide an interactive interface for video upload and results display.

<img width="715" alt="Screenshot 2024-11-05 at 2 27 54 PM" src="https://github.com/user-attachments/assets/b3813437-6a61-4050-9cae-a79d3e92e39b">




