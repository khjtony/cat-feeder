import zmq
import cv2
import time
import numpy as np
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.88.235:5555")
while(True):
    socket.send_string("LALALLA")
    msg = socket.recv()
    A = np.frombuffer(msg, dtype=np.uint8)
    # A = A.reshape((240, 320, 3))
    A = cv2.imdecode(A, 1)
    cv2.imshow("haha", A)
    k = cv2.waitKey(1)