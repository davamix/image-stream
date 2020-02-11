'''
Code from:
https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b
'''

'''
Run this code on Raspberry
'''
import sys
import cv2
import socket
import pickle
import struct

host = "127.0.0.1"
#host = "172.17.0.1"
#host = "192.168.2.101"
port = 6666

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((host, port))
except ConnectionRefusedError:
    print(f"Cannot connect to the server: {host}:{port}")
    sys.exit()

capture = cv2.VideoCapture(0)
capture.set(3, 320)
capture.set(4, 240)

encode_param = [int(cv2.IMWRITE_WEBP_QUALITY), 90]

if capture.isOpened():
    try:

        while True:
            _, frame = capture.read()

            encode, frame = cv2.imencode('.jpg', frame, encode_param)

            data = pickle.dumps(frame, 0)
            size = len(data)
            print(print(f"length: {size}"))

            s.sendall(struct.pack(">L", size) + data)
    
    except BrokenPipeError:
        print("The connection with the server has been closed.")
    finally:
        capture.release()
else:
    print("Webcam cannot be opened")

s.close()