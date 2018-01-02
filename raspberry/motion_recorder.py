"""
    This motion recorder script will save images that labeled as "motion" into NAS
"""

#!/usr/bin/env python

"""
Found on
http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
"""
import zmq
import cv2
import numpy as np
import time
import signal, os
import glob

image_path = "/mnt/nas_photo/cat_feeder/front_camera"

context = zmq.Context()
motion_socket = context.socket(zmq.SUB)
motion_socket.connect("tcp://127.0.0.1:5556")
motion_socket.setsockopt_string(zmq.SUBSCRIBE, '/motion_detection')

image_socket = context.socket(zmq.SUB)
image_socket.connect("tcp://127.0.0.1:5555")
image_socket.setsockopt_string(zmq.SUBSCRIBE, '/front_camera/raw')

time.sleep(0.1)

def ctrlc(sig, err):
    os.kill(os.getpid(), signal.SIGKILL)
signal.signal(signal.SIGINT, ctrlc)

def recv_motion(socket, flags=0, copy=True, track=False):
    """recv a numpy array, including topic, dtype and shape"""
    topic = socket.recv_string()
    md = socket.recv_json(flags=flags)
    msg = socket.recv_string(flags=flags)
    return (md['topic'], msg)


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

# find lastest file
if not os.path.isdir(image_path):
    try:
        os.makedirs(image_path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(image_path):
            pass
        else:
            raise
file_list = glob.glob(image_path + '/*.png')
counter = 0
timestamp = time.time()
if len(file_list) > 0:
    print("Last file is: " + file_list[-1])
    counter = int(file_list[-1].split('.')[-2].split('/')[-1]) + 1
print("new counter is: " + str(counter))


while True:
    motion = recv_motion(motion_socket)[1]
    image = recv_image(image_socket)[1]

    if(time.time() >= timestamp and motion == '1'):
        cv2.imwrite(image_path + '/' + str(counter) + '.png',image)
        print("save image at: " + image_path + '/' + str(counter) + '.png')
        counter += 1
        timestamp = time.time() + 2.5

    time.sleep(0.001)


 


