# dependencies:
# pip install opencv-python
#             pyside6
#             pyaudio
#             SpeechRecognition
# sudo apt install espeak

import os
import threading
import speech_recognition as sr
import cv2
import pyttsx3

# declarations
# these are put up here because some functions (below) use them

desired_quadrant = (0, 0)
r = sr.Recognizer()
m = sr.Microphone()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
engine = pyttsx3.init()

# photographs user
def photograph():
    global cap
    engine.say('cheese')
    engine.runAndWait()
    result, image = cap.read()
    cv2.imwrite("Shot.png", image)
    

# terminates program
def terminate():
    print("Exiting... Goodbye!")
    os._exit(0)

def say(current_quadrant):
    vertical = ""
    horizontal = ""
    if(current_quadrant[0] < desired_quadrant[0]):
        horizontal = "left"
    elif(current_quadrant[0] > desired_quadrant[0]):
        horizontal = "right"
    else:
        horizontal = ""
    
    if(current_quadrant[1] < desired_quadrant[1]):
        vertical = "up"
    elif(current_quadrant[1] > desired_quadrant[1]):
        vertical = "down"
    else:
        vertical = ""

    if(horizontal == vertical): # "" == ""
        engine.say('keep head still')
        engine.runAndWait()
        return

    engine.say('move head ' + horizontal + ' ' + vertical)
    engine.runAndWait()

# handles speech input
def handle(input):
    global desired_quadrant
    
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
        
        # quadrant
        case "bottom left":
            desired_quadrant = (0, 0)
        case "bottom right":
            desired_quadrant = (1, 0)
        case "top left":
            desired_quadrant = (0, 1)
        case "top right":
            desired_quadrant = (1, 1)

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

    quad = (0, 0)
    prev_quad = quad
    prev_in_frame = True

    while True:
        _, img = cap.read()
        CAMERA_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        CAMERA_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 6)
        if(len(faces) != 0):
            for (x, y, w, h) in faces:

                x_center = x+(w/2)
                y_center = y+(h/2)

                if x_center > CAMERA_WIDTH/2:
                    if y_center > CAMERA_HEIGHT/2:
                        # TOP RIGHT
                        quad = (1, 0)
                        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    else:
                        # BOTTOM RIGHT
                        quad = (1, 1)
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                else:
                    if y_center > CAMERA_HEIGHT/2:
                        # TOP LEFT
                        quad = (0, 0)
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    else:
                        # BOTTOM LEFT
                        quad = (0, 1)
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)
                
                if(prev_quad != quad):
                    say(quad)

                prev_quad = quad
                prev_in_frame = True
        else:
            if prev_in_frame:
                engine.say('move around until you appear')
                engine.runAndWait()
            prev_in_frame = False
        
        cv2.imshow('img', img) # (un)comment this to toggle OpenCV's video output
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