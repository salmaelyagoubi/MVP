# Hand Gesture Controlled Keyboard Input

This repository contains a Python project that uses OpenCV and the cvzone library to control keyboard inputs based on hand gestures detected via a webcam. This project is particularly aimed at controlling the space key to simulate a jumping action in games or other applications.

# Demo of The Game 
Just as gamers have mastered the WASD keys, it's now time to embrace AB in sign language , AB is set to become the new standard for future gamers

![Dino_Game-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/5889d07d-5925-4176-9ca5-51d54c7433da)


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Demo](#demo)
- [Dataset](#dataset)
- [Code Explanation](#code-explanation)
- [License](#license)

## Introduction

This project demonstrates how to capture hand gestures using a webcam and translate those gestures into keyboard inputs. Specifically, it uses OpenCV for video capture and the cvzone library for hand detection and gesture recognition.

"Like how gamers are familiar with WASD on keyboard, it's time to get familiar with AB on sign language. AB is the new WASD version for future gamers."

## Features

- Detects hand gestures using a webcam.
- Maps specific hand gestures to keyboard inputs.
- Simulates pressing and releasing the space key based on detected gestures.

## Installation

To run this project, you need to have Python installed on your machine along with the following libraries:

- OpenCV
- cvzone
- numpy


main.py
This script captures video from the webcam, detects hand gestures, and maps them to keyboard inputs.

HandDetector: Initializes the hand detector from cvzone.
Video Capture: Starts capturing video from the webcam.
Gesture Detection: Analyzes each frame to detect hand gestures.
Key Press Simulation: Simulates pressing or releasing the space key based on detected gestures.
