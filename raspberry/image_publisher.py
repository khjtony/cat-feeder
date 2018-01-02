import zmq
import cv2
import os, signal, time
from picamera.array import PiRGBArray
from picamera import PiCamera

"""
    This is image publisher node that will publish the raw image and compressed image.
"""

context = zmq.Context()
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=camera.resolution)

time.sleep(0.1)

def ctrlc(sig, err):
    os.kill(os.getpid(), signal.SIGKILL)
signal.signal(signal.SIGINT, ctrlc)

def publish_image(socket, A, topic="NoName", flags=0, copy=True, track=False):
    """send a numpy array with metadata and array name"""
    md = dict(
        topic=topic,
        dtype=str(A.dtype),
        shape=A.shape,
    )
    socket.send_string(topic, flags | zmq.SNDMORE)
    socket.send_json(md, flags | zmq.SNDMORE)
    if A.flags['C_CONTIGUOUS']:
        # if array is already contiguous in memory just send it
        return socket.send(A, flags, copy=copy, track=track)
    else:
        # else make it contiguous before sending
        A = np.ascontiguousarray(array)
        return socket.send(A, flags, copy=copy, track=track)

def recv_array(socket, flags=0, copy=True, track=False):
    """recv a numpy array, including topic, dtype and shape"""
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    A = np.frombuffer(msg, dtype=md['dtype'])
    return (md['topic'], A.reshape(md['shape']))




socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")
counter = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    publish_image(socket, image, '/front_camera/raw')

    # compress the image
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    result, image = cv2.imencode('.jpg', image, encode_param)
 
    # show the frame
    publish_image(socket, image, '/front_camera/compressed')
    time.sleep(0.001)
 
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
 