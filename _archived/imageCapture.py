import numpy as np
import cv2
import zmqimage
print("Connecting to zmqShowImage Server ... ")
zmq = zmqimage.zmqConnect(connect_to='tcp://localhost:5555')
print("connected to zmqServer")

cap = cv2.VideoCapture('sample.avi')
ret, frame = cap.read()
while(ret):
    ret, frame = cap.read()
    zmq.imshow("test", frame)
    k = cv2.waitKey(1)


