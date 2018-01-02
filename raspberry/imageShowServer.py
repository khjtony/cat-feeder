# imageShowServer.py
import zmqimage
import time
zmq = zmqimage.zmqImageShowServer(open_port="tcp://127.0.0.1:5555")
print("Starting zmqImageShow Server...")
print("  press Ctrl-C to stop")
while True:       # Until Ctrl-C is pressed, will repeatedly
    image = zmq.read()  # display images sent from the headless computer
    time.sleep(0.01)
    print(image.shape)
