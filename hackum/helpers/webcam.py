import numpy as np
import cv2
import time
import base64
#from clarifai_helper import *
from clarifai.client import ClarifaiApi

cap = cv2.VideoCapture(0)

while(True):
    time.sleep(0.2)
    frame = cap.read()[1]
    cv2.imshow('frame',frame)
    cnt = cv2.imencode('.png',frame)[1]
    print(base64.b64encode(cnt))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
