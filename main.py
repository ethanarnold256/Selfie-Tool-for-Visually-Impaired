# dependencies:
# pip install opencv-python
#             pyside6
#             pyaudio
#             SpeechRecognition

import os
import threading
import speech_recognition as sr
import cv2
#from PySide6 import QtCore, QtWidgets, QtGui

#    _                          _           
#   | |                        | |          
#   | |__   ___ _   _      __ _| | _____  __
#   | '_ \ / _ \ | | |    / _` | |/ _ \ \/ /
#   | | | |  __/ |_| |   | (_| | |  __/>  < 
#   |_| |_|\___|\__, |    \__,_|_|\___/_/\_\ ...
#                __/ |                      
#               |___/                       
#
# please put QT class/code here

# declarations
# these are put up here because some functions (below) use them

r = sr.Recognizer()
m = sr.Microphone()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# photographs user
def photograph():
    print("*SNAP* Implement me!")

# terminates program
def terminate():
    print("Exiting... Goodbye!")
    os._exit(0)

# handles speech input
def handle(input):
    match input:
        # terminate
        case "exit":
            terminate()
        case "quit":
            terminate()
        case "leave":
            terminate()
        case "leaf": # near homophone; may save some people
            terminate()
        case "close":
            terminate()
        case "clothes": # near homophone; may save some people
            terminate()
        
        # photograph
        case "cheese":
            photograph()
        case "snap":
            photograph()

# listens for user input
# https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__main__.py
def listen():
    try:
        print("Please remain quiet as the program adjusts ambiance levels.")
        with m as source: r.adjust_for_ambient_noise(source)
        while True:
            print("You may now speak.")
            with m as source: audio = r.listen(source)
            print("Please wait while we process what was said.")
            try:
                value = r.recognize_google(audio)
                print("What we think you said:\n\n\t{}\n".format(value))
                handle(value)
            except sr.UnknownValueError:
                print("What you said was unintelligable")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service.")
    except KeyboardInterrupt:
        print("\nGoodbye.")
        pass

# detects faces through webcam
# https://github.com/adarsh1021/facedetection
def look():
    while True:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # cv2.imshow('img', img) # (un)comment this to toggle OpenCV's video output
        k = cv2.waitKey(30) & 0xff
        if k==27:
            break
    cap.release()
    terminate()

# main "function"

# multithreading 'look' and 'listen'
t1 = threading.Thread(target=listen)
t2 = threading.Thread(target=look)
t1.start()
t2.start()
t1.join()
t2.join()