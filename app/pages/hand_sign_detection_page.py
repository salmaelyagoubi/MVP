import streamlit as st
import cv2
import numpy as np
from keras.models import load_model
from cvzone.HandTrackingModule import HandDetector
from PIL import Image
import pyttsx3
from string import ascii_uppercase
import enchant

# Initialize enchant dictionary
ddd = enchant.Dict("en-US")
# Initialize Hand Detector
hd = HandDetector(maxHands=1)

offset = 29

# Load the model
relative_model_path = r'Sign-Language-To-Text-and-Speech-Conversion-master/cnn8grps_rad1_model.h5'
model = load_model(relative_model_path)

# Application class for handling sign language detection
class Application:
    def __init__(self):
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.speak_engine = pyttsx3.init()
        self.speak_engine.setProperty("rate", 100)
        voices = self.speak_engine.getProperty("voices")
        self.speak_engine.setProperty("voice", voices[0].id)

        self.ct = {letter: 0 for letter in ascii_uppercase}
        self.ct['blank'] = 0
        self.str = " "

    def predict(self, test_image):
        white = test_image.reshape(1, 400, 400, 3)
        prob = np.array(model.predict(white)[0], dtype='float32')
        ch = ascii_uppercase[np.argmax(prob)]
        return ch

    def video_loop(self):
        ok, frame = self.vs.read()
        if not ok:
            st.error("Failed to capture image from webcam")
            return None

        cv2image = cv2.flip(frame, 1)
        hands, _ = hd.findHands(cv2image, draw=False, flipType=True)
        cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
        if hands:
            hand = hands[0]
            if 'bbox' in hand:
                bbox = hand['bbox']
                x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
                if y - offset < 0 or x - offset < 0 or y + h + offset > cv2image.shape[0] or x + w + offset > cv2image.shape[1]:
                    return cv2image  # Skip if the bounding box is out of frame

                image = cv2image[y - offset:y + h + offset, x - offset:x + w + offset]
                if image.size == 0:
                    return cv2image  # Skip if the image slice is empty

                white = np.ones((400, 400, 3), np.uint8) * 255

                handz, _ = hd.findHands(image, draw=False, flipType=True)
                if handz:
                    hand = handz[0]
                    self.pts = hand['lmList']
                    os = ((400 - w) // 2) - 15
                    os1 = ((400 - h) // 2) - 15
                    for t in range(0, 4, 1):
                        cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), 
                                 (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1), 
                                 (0, 255, 0), 3)
                    for t in range(5, 8, 1):
                        cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), 
                                 (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1), 
                                 (0, 255, 0), 3)
                    for t in range(9, 12, 1):
                        cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), 
                                 (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1), 
                                 (0, 255, 0), 3)
                    for t in range(13, 16, 1):
                        cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), 
                                 (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1), 
                                 (0, 255, 0), 3)
                    for t in range(17, 20, 1):
                        cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), 
                                 (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1), 
                                 (0, 255, 0), 3)
                    cv2.line(white, (self.pts[5][0] + os, self.pts[5][1] + os1), 
                             (self.pts[9][0] + os, self.pts[9][1] + os1), (0, 255, 0), 3)
                    cv2.line(white, (self.pts[9][0] + os, self.pts[9][1] + os1), 
                             (self.pts[13][0] + os, self.pts[13][1] + os1), (0, 255, 0), 3)
                    cv2.line(white, (self.pts[13][0] + os, self.pts[13][1] + os1), 
                             (self.pts[17][0] + os, self.pts[17][1] + os1), (0, 255, 0), 3)
                    cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), 
                             (self.pts[5][0] + os, self.pts[5][1] + os1), (0, 255, 0), 3)
                    cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), 
                             (self.pts[17][0] + os, self.pts[17][1] + os1), (0, 255, 0), 3)

                    for i in range(21):
                        cv2.circle(white, (self.pts[i][0] + os, self.pts[i][1] + os1), 2, (0, 0, 255), 1)

                    res = white
                    symbol = self.predict(res)
                    cv2.rectangle(cv2image, (x - offset, y - offset), 
                                  (x + w + offset, y + h + offset), (255, 0, 0), 2)
                    cv2.putText(cv2image, symbol, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (255, 0, 0), 2, cv2.LINE_AA)

        return cv2image

    def destructor(self):
        print("Closing Application...")
        self.vs.release()
        cv2.destroyAllWindows()

def hand_sign_detection_page():
    st.title("Hand Sign Detection")
    app = Application()

    frame_placeholder = st.empty()

    while True:
        frame = app.video_loop()
        if frame is not None:
            frame_placeholder.image(frame)
        else:
            break

if __name__ == "__main__":
    hand_sign_detection_page()
