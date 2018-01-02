#!/usr/bin/env python

"""
Found on
http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
"""
import zmq
import cv2
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://192.168.88.235:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, 'front_camera/compressed')

def recv_image(socket):
    topic, A = recv_array(socket)
    return (topic, cv2.imdecode(np.frombuffer(A, dtype=np.uint8), 1))

def recv_array(socket, flags=0, copy=True, track=False):
    """recv a numpy array, including topic, dtype and shape"""
    topic = socket.recv_string()
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    A = np.frombuffer(msg, dtype=md['dtype'])
    return (md['topic'], A.reshape(md['shape']))


def diffImg(t0, t1, t2):
    kernel = np.ones((5,5),np.uint8)
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.dilate(cv2.bitwise_and(d1, d2), kernel, iterations=3)

def is_motion(img, threshold_gray, threshold_sum):
    # use threshold to find motion in diffImg
    ret,result = cv2.threshold(img,threshold_gray,255,cv2.THRESH_BINARY)
    if np.sum(result) >= threshold_sum:
        return True
    else:
        return False
 

# Read three images first:
t_minus = recv_image(socket)[1]
t_minus = cv2.cvtColor(t_minus, cv2.COLOR_RGB2GRAY)
t = recv_image(socket)[1]
t = cv2.cvtColor(t, cv2.COLOR_RGB2GRAY)
t_plus = recv_image(socket)[1]
t_plus = cv2.cvtColor(t_plus, cv2.COLOR_RGB2GRAY)
 
while True:
    diff = diffImg(t_minus, t, t_plus)
    print(is_motion(diff, 60, 50))

    # Read next image
    t_minus = t
    t = t_plus
    t_plus = recv_image(socket)[1]
    t_plus = cv2.cvtColor(t_plus, cv2.COLOR_RGB2GRAY)

    key = cv2.waitKey(1)

 
