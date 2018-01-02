import zmq
import cv2
import os, signal, time
from picamera.array import PiRGBArray
from picamera import PiCamera

context = zmq.Context()
cap = cv2.VideoCapture(0)
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 16
rawCapture = PiRGBArray(camera, size=camera.resolution)

time.sleep(0.1)

def ctrlc(sig, err):
    os.kill(os.getpid(), signal.SIGKILL)
    cap.release()
signal.signal(signal.SIGINT, ctrlc)

def send_iamge(socket, arrayname, array):
    '''send image to display on remote server'''
    if array.flags['C_CONTIGUOUS']:
        # if array is already contiguous in memory just send it
        return socket.send(array)
    else:
        # else make it contiguous before sending
        array = np.ascontiguousarray(array)
        return socket.send(array)

    
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    result, image = cv2.imencode('.jpg', image, encode_param)
 
    # show the frame
    req = socket.recv()
    send_iamge(socket, 'haha', image)
    print("Sent image")
    time.sleep(0.1)
 
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
 