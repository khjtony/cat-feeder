# imageShowServer.py
import zmqimage
zmq = zmqimage.zmqImageShowServer(open_port="tcp://192.168.88.235:5555")
print("Starting zmqImageShow Server...")
print("  press Ctrl-C to stop")
while True:       # Until Ctrl-C is pressed, will repeatedly
    zmq.imshow()  # display images sent from the headless computer
