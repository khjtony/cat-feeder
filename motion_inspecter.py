import zmq
import time
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://192.168.88.235:5556")
socket.setsockopt_string(zmq.SUBSCRIBE, '/motion_detection')

def recv_array(socket, flags=0, copy=True, track=False):
    """recv a numpy array, including topic, dtype and shape"""
    topic = socket.recv_string()
    md = socket.recv_json(flags=flags)
    msg = socket.recv_string(flags=flags)
    return (md['topic'], msg)


while(True):
    topic, msg = recv_array(socket)
    print(topic + " : " + msg)
    time.sleep(0.1)