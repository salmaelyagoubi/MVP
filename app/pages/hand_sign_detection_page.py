import math
import cv2
import streamlit as st
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from keras.models import load_model
import traceback

model_path = r'C:\Users\salma elyagoubi\Downloads\MVP\MVP\Sign-Language-To-Text-and-Speech-Conversion-master\cnn8grps_rad1_model.h5'
model = load_model(model_path)
white = np.ones((400, 400), np.uint8) * 255
cv2.imwrite("white.jpg", white)

# Initialize hand detectors
hd = HandDetector(maxHands=1)
hd2 = HandDetector(maxHands=1)

# Constants
offset = 29
step = 1
flag = False
suv = 0

# Utility functions
def distance(x, y):
    return math.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))

def distance_3d(x, y):
    return math.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2) + ((x[2] - y[2]) ** 2))

def hand_sign_detection_page():
    st.title("Hand Sign Detection")

    # Streamlit UI elements
    st.sidebar.header("Settings")
    confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)
    stop_button = st.sidebar.button("Stop Webcam")
    reset_button = st.sidebar.button("Reset Detected Letters")

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    # Streamlit placeholder for video feed
    stframe = st.empty()
    
    # Streamlit placeholder for detected word
    word_placeholder = st.empty()

    detected_letters = []

    while cap.isOpened():
        try:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to grab frame from webcam.")
                break

            frame = cv2.flip(frame, 1)
            hands, _ = hd.findHands(frame, draw=False, flipType=True)
            if hands:
                hand = hands[0]
                if 'bbox' in hand:
                    x, y, w, h = hand['bbox']
                    image = frame[y - offset:y + h + offset, x - offset:x + w + offset]
                    white = cv2.imread("white.jpg")
                    handz, _ = hd2.findHands(image, draw=False, flipType=True)
                    if handz:
                        hand = handz[0]
                        pts = hand['lmList']
                        os = ((400 - w) // 2) - 15
                        os1 = ((400 - h) // 2) - 15
                        for t in range(0, 4, 1):
                            cv2.line(white, (pts[t][0] + os, pts[t][1] + os1), (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)
                        for t in range(5, 8, 1):
                            cv2.line(white, (pts[t][0] + os, pts[t][1] + os1), (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)
                        for t in range(9, 12, 1):
                            cv2.line(white, (pts[t][0] + os, pts[t][1] + os1), (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)
                        for t in range(13, 16, 1):
                            cv2.line(white, (pts[t][0] + os, pts[t][1] + os1), (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)
                        for t in range(17, 20, 1):
                            cv2.line(white, (pts[t][0] + os, pts[t][1] + os1), (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)
                        cv2.line(white, (pts[5][0] + os, pts[5][1] + os1), (pts[9][0] + os, pts[9][1] + os1), (0, 255, 0), 3)
                        cv2.line(white, (pts[9][0] + os, pts[9][1] + os1), (pts[13][0] + os, pts[13][1] + os1), (0, 255, 0), 3)
                        cv2.line(white, (pts[13][0] + os, pts[13][1] + os1), (pts[17][0] + os, pts[17][1] + os1), (0, 255, 0), 3)
                        cv2.line(white, (pts[0][0] + os, pts[0][1] + os1), (pts[5][0] + os, pts[5][1] + os1), (0, 255, 0), 3)
                        cv2.line(white, (pts[0][0] + os, pts[0][1] + os1), (pts[17][0] + os, pts[17][1] + os1), (0, 255, 0), 3)
                        for i in range(21):
                            cv2.circle(white, (pts[i][0] + os, pts[i][1] + os1), 2, (0, 0, 255), 1)
                        cv2.imshow("2", white)
                        white = white.reshape(1, 400, 400, 3)
                        prob = np.array(model.predict(white)[0], dtype='float32')
                        ch1 = np.argmax(prob, axis=0)
                        prob[ch1] = 0
                        ch2 = np.argmax(prob, axis=0)
                        prob[ch2] = 0
                        ch3 = np.argmax(prob, axis=0)
                        prob[ch3] = 0

                        pl = [ch1, ch2]

                        # Condition checks and classification logic here...
                        # Add your custom conditions and logic based on the pts array and ch1, ch2, ch3 values

                        detected_letter = ch1  # Replace with actual detected letter
                        detected_letters.append(detected_letter)
                        
                        frame = cv2.putText(frame, "Predicted " + str(detected_letter), (30, 80),
                                            cv2.FONT_HERSHEY_SIMPLEX,
                                            3, (0, 0, 255), 2, cv2.LINE_AA)

            # Convert color space from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Display the frame
            stframe.image(frame_rgb, channels="RGB")
            
            # Display the detected word
            detected_word = ''.join(detected_letters[-10:])  # Show last 10 detected letters
            word_placeholder.text(f"Detected Word: {detected_word}")

            # Check for stop button
            if stop_button:
                break

            # Check for reset button
            if reset_button:
                detected_letters.clear()

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.text(traceback.format_exc())

    cap.release()
    st.write("Webcam stopped.")
