'''
Code from:
https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b
'''

import sys
import cv2
import socket
import pickle
import struct
import json

class Client():
    def __init__(self):
        # self.host = "127.0.0.1"
        # self.port = 6666

        self.configuration = self.load_configuration("config.json")

        self.vcapture = cv2.VideoCapture(0)
        self.vcapture.set(3, 320)
        self.vcapture.set(4, 240)
        self.encode_param = [int(cv2.IMWRITE_WEBP_QUALITY), 90]

        self.isCapturing = True

        self.output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isConnected = False

    def load_configuration(self, file):
        with open(file) as json_data:
            return json.load(json_data)

    def connect(self):
        host = self.configuration["client"]["output"]["host"]
        port = self.configuration["client"]["output"]["port"]

        try:
            self.output_socket.connect((host, port))
            self.isConnected = True
        except ConnectionRefusedError:
            print(f"Cannot connect to the server: {host}: {port}")

    def disconnect(self):
        try:
            h, p = self.output_socket.getpeername()
            print(f"Closing connection to: {h}: {p}")
        except:
            print("Client was not connected.")
        finally:
            self.output_socket.close()
            self.isConnected = False

    def capture(self):
        if not self.vcapture.isOpened():
            print("Webcam cannot be opened")
            return
        
        _, frame = self.vcapture.read()

        return frame
    
    def get_prediction(self, frame):
        _, frame = cv2.imencode('.jpg', frame, self.encode_param)

        data = pickle.dumps(frame, 0)
        size = len(data)

        self.output_socket.sendall(struct.pack(">L", size) + data)

def main():
    print("## CLIENT ##")
    client = Client()
    client.connect()
    
    if client.isConnected:
        while True:
            frame = client.capture()

            client.get_prediction(frame)

    client.disconnect()

if __name__ == '__main__':
    main()