import zmq
import cv2
import time
import numpy as np
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://192.168.88.235:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, '/front_camera/compressed')

def recv_image(socket):
    md, A = recv_array(socket)
    if md['topic'].split('/')[-1] == 'compressed':
        return (md['topic'], cv2.imdecode(A, 1))
    elif md['topic'].split('/')[-1] == 'raw':
        return (md['topic'], A.reshape(md['shape']))

def recv_array(socket, flags=0, copy=True, track=False):
    """recv a numpy array, including topic, dtype and shape"""
    topic = socket.recv_string()
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    A = np.frombuffer(msg, dtype=md['dtype'])
    return (md, A.reshape(md['shape']))


while(True):
    topic, A = recv_image(socket)
    cv2.imshow(topic, A)
    print(topic)
    k = cv2.waitKey(1)