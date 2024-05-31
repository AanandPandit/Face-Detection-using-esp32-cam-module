import datetime
import tkinter as tk
from tkinter import filedialog
import cv2
import os
import urllib.request
import numpy as np

debug = True

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# create folder for output images
os.makedirs("output/cam_images", exist_ok=True)

# -------------------------from_camera-----------------------
def detect_faces_from_camera():
    url = 'http://192.168.137.149/cam-lo.jpg'

    while True:
        try:
            img_resp = urllib.request.urlopen(url)
            img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(img_arr, -1)
        except Exception as e:
            print(f"Error retrieving frame: {e}")
            break

        if frame is None:
            print("Error: Failed to decode frame.")
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.imshow('Face Detection from Camera', frame)

        key = cv2.waitKey(1)

        if key & 0xFF == ord('q'):
            print('Camera closed by user')
            break
        elif key & 0xFF == ord('c'):
            print('Camera captured the image')
            face = frame[y:y + h, x:x + w]
            cv2.imwrite(os.path.join(
                "output/cam_images", f"captured_face_{len(os.listdir('output/cam_images')) + 1}.jpg"), face)

    cv2.destroyAllWindows()
    if debug:
        print("Camera capture completed")

detect_faces_from_camera()
