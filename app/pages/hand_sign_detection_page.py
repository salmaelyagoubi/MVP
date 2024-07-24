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
# Initialize Hand Detectors
hd = HandDetector(maxHands=1)
hd2 = HandDetector(maxHands=1)

offset = 29

# Application class for handling sign language detection
class Application:

    def __init__(self):
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        relative_model_path=r'Sign-Language-To-Text-and-Speech-Conversion-master\cnn8grps_rad1_model.h5'
        self.model = load_model(relative_model_path)  # Update with the RELATIVE path to your model
        self.speak_engine = pyttsx3.init()
        self.speak_engine.setProperty("rate", 100)
        voices = self.speak_engine.getProperty("voices")
        self.speak_engine.setProperty("voice", voices[0].id)

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0
        self.space_flag = False
        self.next_flag = True
        self.prev_char = ""
        self.count = -1
        self.ten_prev_char = []
        for i in range(10):
            self.ten_prev_char.append(" ")

        for i in ascii_uppercase:
            self.ct[i] = 0

        print("Loaded model from disk")

        self.str = " "
        self.ccc = 0
        self.word = " "
        self.current_symbol = "C"
        self.photo = "Empty"

        self.word1 = " "
        self.word2 = " "
        self.word3 = " "
        self.word4 = " "

        self.video_loop()

    def video_loop(self):
        try:
            ok, frame = self.vs.read()
            if not ok:
                st.error("Failed to capture image from webcam")
                return

            cv2image = cv2.flip(frame, 1)
            hands, _ = hd.findHands(cv2image, draw=False, flipType=True)
            cv2image_copy = np.array(cv2image)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
            self.current_image = Image.fromarray(cv2image)

            if hands:
                hand = hands[0]
                if 'bbox' in hand:
                    bbox = hand['bbox']
                    x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
                    image = cv2image_copy[y - offset:y + h + offset, x - offset:x + w + offset]
                    white = np.ones((400, 400, 3), np.uint8) * 255

                    handz, _ = hd2.findHands(image, draw=False, flipType=True)
                    if handz:
                        hand = handz[0]
                        self.pts = hand['lmList']
                        os = ((400 - w) // 2) - 15
                        os1 = ((400 - h) // 2) - 15
                        for t in range(0, 4, 1):
                            cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                    (0, 255, 0), 3)
                        for t in range(5, 8, 1):
                            cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                    (0, 255, 0), 3)
                        for t in range(9, 12, 1):
                            cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                    (0, 255, 0), 3)
                        for t in range(13, 16, 1):
                            cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                    (0, 255, 0), 3)
                        for t in range(17, 20, 1):
                            cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                    (0, 255, 0), 3)
                        cv2.line(white, (self.pts[5][0] + os, self.pts[5][1] + os1), (self.pts[9][0] + os, self.pts[9][1] + os1), (0, 255, 0), 3)
                        cv2.line(white, (self.pts[9][0] + os, self.pts[9][1] + os1), (self.pts[13][0] + os, self.pts[13][1] + os1), (0, 255, 0), 3)
                        cv2.line(white, (self.pts[13][0] + os, self.pts[13][1] + os1), (self.pts[17][0] + os, self.pts[17][1] + os1), (0, 255, 0), 3)
                        cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), (self.pts[5][0] + os, self.pts[5][1] + os1), (0, 255, 0), 3)
                        cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), (self.pts[17][0] + os, self.pts[17][1] + os1), (0, 255, 0), 3)

                        for i in range(21):
                            cv2.circle(white, (self.pts[i][0] + os, self.pts[i][1] + os1), 2, (0, 0, 255), 1)

                        res = white
                        self.predict(res)

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            st.image(img_pil)
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            self.root.after(1, self.video_loop)

    def predict(self, test_image):
        white = test_image
        white = white.reshape(1, 400, 400, 3)
        prob = np.array(self.model.predict(white)[0], dtype='float32')
        ch1 = np.argmax(prob, axis=0)
        prob[ch1] = 0
        ch2 = np.argmax(prob, axis=0)
        prob[ch2] = 0
        ch3 = np.argmax(prob, axis=0)
        prob[ch3] = 0

        pl = [ch1, ch2]
        self.current_symbol = self.get_symbol_from_prediction(pl)

    def get_symbol_from_prediction(self, pl):
        ch1 = pl[0]
        if ch1 == 0:
            ch1 = 'S'
            if self.pts[4][0] < self.pts[6][0] and self.pts[4][0] < self.pts[10][0] and self.pts[4][0] < self.pts[14][0] and self.pts[4][0] < self.pts[18][0]:
                ch1 = 'A'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] < self.pts[10][0] and self.pts[4][0] < self.pts[14][0] and self.pts[4][0] < self.pts[18][0] and self.pts[4][1] < self.pts[14][1] and self.pts[4][1] < self.pts[18][1]:
                ch1 = 'T'
            if self.pts[4][1] > self.pts[8][1] and self.pts[4][1] > self.pts[12][1] and self.pts[4][1] > self.pts[16][1] and self.pts[4][1] > self.pts[20][1]:
                ch1 = 'E'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] > self.pts[10][0] and self.pts[4][0] > the.pts[14][0] and self.pts[4][1] < self.pts[18][1]:
                ch1 = 'M'
            if self.pts[4][0] > the.pts[6][0] and self.pts[4][0] > self.pts[10][0] and self.pts[4][1] < self.pts[18][1] and self.pts[4][1] < the.pts[14][1]:
                ch1 = 'N'

        if ch1 == 2:
            if self.distance(self.pts[12], self.pts[4]) > 42:
                ch1 = 'C'
            else:
                ch1 = 'O'

        if ch1 == 3:
            if (self.distance(self.pts[8], self.pts[12])) > 72:
                ch1 = 'G'
            else:
                ch1 = 'H'

        if ch1 == 7:
            if self.distance(self.pts[8], self.pts[4]) > 42:
                ch1 = 'Y'
            else:
                ch1 = 'J'

        if ch1 == 4:
            ch1 = 'L'

        if ch1 == 6:
            ch1 = 'X'

        if ch1 == 5:
            if self.pts[4][0] > self.pts[12][0] and self.pts[4][0] > self.pts[16][0] and self.pts[4][0] > self.pts[20][0]:
                if self.pts[8][1] < self.pts[5][1]:
                    ch1 = 'Z'
                else:
                    ch1 = 'Q'
            else:
                ch1 = 'P'

        if ch1 == 1:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > the.pts[20][1]):
                ch1 = 'B'
            if (self.pts[6][1] > the.pts[8][1] and self.pts[10][1] < the.pts[12][1] and self.pts[14][1] < the.pts[16][1] and self.pts[18][1] < the.pts[20][1]):
                ch1 = 'D'
            if (self.pts[6][1] < the.pts[8][1] and self.pts[10][1] > the.pts[12][1] and self.pts[14][1] > the.pts[16][1] and the.pts[18][1] > the.pts[20][1]):
                ch1 = 'F'
            if (self.pts[6][1] < the.pts[8][1] and the.pts[10][1] < the.pts[12][1] and the.pts[14][1] < the.pts[16][1] and the.pts[18][1] > the.pts[20][1]):
                ch1 = 'I'
            if (the.pts[6][1] > the.pts[8][1] and the.pts[10][1] > the.pts[12][1] and the.pts[14][1] > the.pts[16][1] and the.pts[18][1] < the.pts[20][1]):
                ch1 = 'W'
            if (the.pts[6][1] > the.pts[8][1] and the.pts[10][1] > the.pts[12][1] and the.pts[14][1] < the.pts[16][1] and the.pts[18][1] < the.pts[20][1]) and the.pts[4][1] < the.pts[9][1]:
                ch1 = 'K'
            if ((self.distance(the.pts[8], the.pts[12]) - self.distance(the.pts[6], the.pts[10])) < 8) and (
                    the.pts[6][1] > the.pts[8][1] and the.pts[10][1] > the.pts[12][1] and the.pts[14][1] < the.pts[16][1] and the.pts[18][1] <
                    the.pts[20][1]):
                ch1 = 'U'
            if ((self.distance(the.pts[8], the.pts[12]) - self.distance(the.pts[6], the.pts[10])) >= 8) and (
                    the.pts[6][1] > the.pts[8][1] and the.pts[10][1] > the.pts[12][1] and the.pts[14][1] < the.pts[16][1] and the.pts[18][1] <
                    the.pts[20][1]) and (the.pts[4][1] > the.pts[9][1]):
                ch1 = 'V'

            if (the.pts[8][0] > the.pts[12][0]) and (
                    the.pts[6][1] > the.pts[8][1] and the.pts[10][1] > the.pts[12][1] and the.pts[14][1] < the.pts[16][1] and the.pts[18][1] <
                    the.pts[20][1]):
                ch1 = 'R'

        if ch1 == 1 or ch1 == 'E' or ch1 == 'S' or ch1 == 'X' or ch1 == 'Y' or ch1 == 'B':
            if (the.pts[6][1] > the.pts[8][1] and the.pts[10][1] < the.pts[12][1] and the.pts[14][1] < the.pts[16][1] and the.pts[18][1] > the.pts[20][1]):
                ch1 = " "

        if ch1 == 'E' or ch1 == 'Y' or ch1 == 'B':
            if (the.pts[4][0] < the.pts[5][0]) and (the.pts[6][1] > the.pts[8][1] and the.pts[10][1] > the.pts[12][1] and the.pts[14][1] > the.pts[16][1] and the.pts[18][1] > the.pts[20][1]):
                ch1 = "next"

        if ch1 == 'Next' or 'B' or 'C' or 'H' or 'F' or 'X':
            if (the.pts[0][0] > the.pts[8][0] and the.pts[0][0] > the.pts[12][0] and the.pts[0][0] > the.pts[16][0] and the.pts[0][0] > the.pts[20][0]) and (the.pts[4][1] < the.pts[8][1] and the.pts[4][1] < the.pts[12][1] and the.pts[4][1] < the.pts[16][1] and the.pts[4][1] < the.pts[20][1]) and (the.pts[4][1] < the.pts[6][1] and the.pts[4][1] < the.pts[10][1] and the.pts[4][1] < the.pts[14][1] and the.pts[4][1] < the.pts[18][1]):
                ch1 = 'Backspace'

        return ch1
        
    def distance(self, x, y):
        return np.linalg.norm(np.array(x) - np.array(y))

    def speak_fun(self):
        self.speak_engine.say(self.str)
        self.speak_engine.runAndWait()

    def clear_fun(self):
        self.str = " "
        self.word1 = " "
        self.word2 = " "
        self.word3 = " "
        self.word4 = " "

    def destructor(self):
        print("Closing Application...")
        self.vs.release()
        cv2.destroyAllWindows()

def hand_sign_detection_page():
    st.title("Hand Sign Detection")
    app = Application()

if __name__ == "__main__":
    hand_sign_detection_page()
