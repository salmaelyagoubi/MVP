# Hand Gesture Recognition

This project implements real-time hand gesture recognition using computer vision and machine learning techniques. It can identify hand gestures corresponding to the letters 'A', 'B', and 'L' using a webcam feed.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- Real-time hand gesture recognition
- Utilizes MediaPipe for accurate hand landmark detection
- Implements a machine learning model for gesture classification
- Provides visual feedback with bounding box and predicted letter overlay
- Supports multiple hand detection

## Requirements

- Python 3.7+
- OpenCV (cv2)
- MediaPipe
- NumPy
- scikit-learn (for the pre-trained model)
- Webcam or video input device

## Installation

1. Clone this repository:https://github.com/salmaelyagoubi/MVP.git
2. Create and activate a virtual environment (optional but recommended):

   python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

3. Install the required packages:

   pip install opencv-python mediapipe numpy scikit-learn

4. Ensure you have the pre-trained model file `model.p` in the project directory.

## Usage

To run the hand gesture recognition system:
python gesture_recognition.py
Copy
- The webcam feed will open in a new window.
- Position your hand in front of the camera.
- The system will detect your hand, draw landmarks, and predict the gesture.
- The predicted letter (A, B, or L) will be displayed on the screen.
- Press 'Q' to quit the application.

## How It Works

1. Video Capture: The script captures video frames from the default webcam.
2. Hand Detection: Each frame is converted to RGB and processed by MediaPipe's hand detection model.
3. Landmark Extraction: If hands are detected, the system extracts 21 landmark points for each hand.
4. Data Preprocessing: The landmark coordinates are normalized and prepared for the machine learning model.
5. Gesture Prediction: The preprocessed data is fed into a pre-trained machine learning model to predict the gesture.
6. Visualization: The frame is annotated with hand landmarks, a bounding box, and the predicted letter.

## Project Structure
hand-gesture-recognition/
│

├── gesture_recognition.py
                            # Main script
├── model.p
                            # Pre-trained machine learning model
├── README.md
                            # Project documentation
└── requirements.txt
                            # List of Python dependencies
Copy
## Customization

- To add more gestures:
  1. Collect training data for new gestures
  2. Retrain the machine learning model
  3. Update the `labels_dict` in the script with new gesture labels

- To adjust detection sensitivity:
  - Modify the `min_detection_confidence` parameter in the `mp_hands.Hands()` initialization

## Troubleshooting

- If the webcam doesn't open, ensure no other application is using it.
- For performance issues, try reducing the frame resolution in the `cv2.VideoCapture()` call.
- If gestures are not recognized accurately, you may need to retrain the model with more diverse data.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for the hand landmark detection
- [OpenCV](https://opencv.org/) for image processing and computer vision utilities
- [scikit-learn](https://scikit-learn.org/) for machine learning tools
