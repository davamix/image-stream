#!/usr/bin/python3
'''
Code from:
https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b
'''

import cv2
import socket
import struct
import pickle
import json
import time
import time

from model import Model


class Server():
    def __init__(self):
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.data = b""
        self.payload_size = struct.calcsize(">L")

        self.configuration = self.load_configuration("config.json")
        self.isOutputConnected = False

        self.setup_input_connections()
        self.setup_output_connections()

        # FPS
        self.time_start = None
        self.time_end = None
        self.frames = 0

    def load_configuration(self, file):
        with open(file) as json_data:
            return json.load(json_data)

    '''
    Configure and bind the input socket connection
    '''
    def setup_input_connections(self):
        host = self.configuration["server"]["input"]["host"]
        port = self.configuration["server"]["input"]["port"]
        
        self.input_socket.bind((host, port))
        print(f"Listening: {host}: {port}")

        self.input_socket.listen(10)
    
    '''
    Configure the output socket connection
    '''
    def setup_output_connections(self):
        host = self.configuration["server"]["output"]["host"]
        port = self.configuration["server"]["output"]["port"]

        try:
            self.output_socket.connect((host, port))
            self.isOutputConnected = True
        except ConnectionRefusedError:
            print(f"Cannot connect to: {host}: {port}")

    def connect(self):
        conn, addr = self.input_socket.accept()
        return conn, addr

    '''
    Close the output socket connection
    '''
    def disconnect(self):
        try:
            h, p = self.output_socket.getpeername()
            print(f"Closing connection to: {h}: {p}")
        except:
            print("The output connection was not available.")
        finally:
            self.output_socket.close()
            self.isOutputConnected = False

    def receive_data(self, connection):
        while len(self.data) < self.payload_size:
            self.data += connection.recv(4096)

        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        while(len(self.data) < msg_size):
            self.data += connection.recv(4096)

        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]

        return frame_data

    def send_data(self, original_image, predicted_image):
        #print(f"Sending data: {data}")

        # data = pickle.dumps(data, 0)
        data = pickle.dumps((original_image, predicted_image))
        size = len(data)

        # TODO: Try to connect if the output socket is not connected
        if self.isOutputConnected:
            self.output_socket.sendall(struct.pack(">L", size) + data)


def main():
    print("## SERVER ##")
    model = Model()

    server = Server()
    connection, _ = server.connect()

    start_time = time.time()
    counter = 0

    while True:
        frame_data = server.receive_data(connection)

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        if model.isPredicting: continue

        # classes, scores = model.detect(frame)

        # for c,s in zip(classes, scores):
        #     #print(f"Class {model.classes[c]}, {s * 100:.2f}%")
        #     msg = f"Class {model.classes[c]}, {s * 100:.2f}%"
        #     server.send_data(msg)
        
        #server.send_data(zip(classes, scores))

        # detection_time = time.time()
        
        final_image = model.detect(frame)
        # print(f"Detection in {int(round((time.time() - detection_time) * 1000))} ms")
        
        server.send_data(frame, final_image)

        counter+=1
        # Display FPS every 1s
        if (time.time() - start_time) > 1 :
            print("FPS: ", counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()

if __name__ == '__main__':
    main()