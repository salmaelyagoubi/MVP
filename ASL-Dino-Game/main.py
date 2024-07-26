import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

space_pressed=0x39

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

if __name__ == '__main__':
    PressKey(0x39)
    time.sleep(1)
    ReleaseKey(0x39)
    time.sleep(1)

import cv2
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey , ReleaseKey
from directkeys import space_pressed
import time

detector = HandDetector(detectionCon=0.8 , maxHands=1)

space_key_pressed=space_pressed

time.sleep(2.0)
current_key_pressed = set()
video = cv2.VideoCapture(0)

while True:
    ret , frame = video.read()
    keyPressed = False
    spacePressed = False
    key_count = 0
    key_pressed = 0
    hands , img = detector.findHands(frame)
    cv2.rectangle(img, (0, 500), (300, 425), (50, 50, 255), -2)
    cv2.rectangle(img, (640, 480), (400, 425), (50, 50, 255), -2)
    if hands:
        lmlist  =hands[0]
        fingerup = detector.fingersUp(lmlist)
        print(fingerup)
        if fingerup == [0,0,0,0,0]:
            cv2.putText(frame , 'Finger Count : 0', (20 , 460) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255,255 , 255),1 , cv2.LINE_AA)
            cv2.putText(frame,  'Jumping', (440, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,     cv2.LINE_AA)
            PressKey(space_key_pressed)
            spacePressed = True
            current_key_pressed.add(space_key_pressed)
            key_pressed = space_key_pressed
            keyPressed = True
            key_count = key_count + 1
        if fingerup == [0,1,0,0,0]:
            cv2.putText(frame , 'Finger Count : 1', (20 , 460) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255,255 , 255),1 , cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        if fingerup == [0,1,1,0,0]:
            cv2.putText(frame , 'Finger Count : 2', (20 , 460) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255,255 , 255),1 , cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        if fingerup == [0,1,1,1,0]:
            cv2.putText(frame , 'Finger Count : 3', (20 , 460) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255,255 , 255),1 , cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        if fingerup == [0,1,1,1,1]:
            cv2.putText(frame , 'Finger Count : 4', (20 , 460) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255,255 , 255),1 , cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        if fingerup == [1,1,1,1,1]:
            cv2.putText(frame , 'Finger Count : 5`', (20 , 460) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255,255 , 255),1 , cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            if not keyPressed and len(current_key_pressed) != 0:
                for key in current_key_pressed:
                    ReleaseKey(key)
                current_key_pressed = set()
            elif key_count == 1 and len(current_key_pressed) == 2:
                for key in current_key_pressed:
                    if key_pressed != key:
                        ReleaseKey(key)
                current_key_pressed = set()
                for key in current_key_pressed:
                    ReleaseKey(key)
                current_key_pressed = set()
    cv2.imshow("Frame",frame)
    k = cv2.waitKey(1)
    if k==ord('q'):
        break

video.release()
cv2.destroyAllWindows()
