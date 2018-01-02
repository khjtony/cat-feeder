import numpy as np
import cv2
import zmqimage
import time
import os,signal
print("Connecting to zmqShowImage Server ... ")
zmq = zmqimage.zmqConnect(connect_to='tcp://*:5555')
print("connected to zmqServer")

cap = cv2.VideoCapture(0)

def ctrlc(sig, err):
    cap.release()
    os.kill(os.getpid(), signal.SIGKILL)
signal.signal(signal.SIGINT, ctrlc)

ret, frame = cap.read()
while True:
    ret, frame = cap.read()
    if(ret):
        zmq.imshow("test", frame)
        print(frame.shape)
        #k = cv20.waitKey(1)

    print(ret)
    time.sleep(0.1)


