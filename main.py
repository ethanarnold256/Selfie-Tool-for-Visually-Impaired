import threading
import speech_recognition as sr
import cv2

# This function listens for user input.
# https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__main__.py
def listen():
    r = sr.Recognizer()
    m = sr.Microphone()
    try:
        print("Please remain quiet as the program adjusts ambiance levels.")
        with m as source: r.adjust_for_ambient_noise(source)
        while True:
            print("You may now speak.")
            with m as source: audio = r.listen(source)
            print("Please wait while we process what was said.")
            try:
                value = r.recognize_google(audio)
                print("What we think you said:\n{}".format(value))
            except sr.UnknownValueError:
                print("What you said was unintelligable")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service.")
    except KeyboardInterrupt:
        print("\nGoodbye.")
        pass

# This function detects faces through webcam.
# https://github.com/adarsh1021/facedetection
def look():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    while True:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k==27:
            break
    cap.release()