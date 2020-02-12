#!/usr/bin/python3
'''
Code from:
https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b
'''

import cv2
import socket
import struct
import pickle

from model import Model


class Server():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = b""
        self.payload_size = struct.calcsize(">L")

    def connect(self, host, port):
        self.sock.bind((host, port))
        self.sock.listen(10)
        conn, addr = self.sock.accept()

        return conn, addr

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

    def send_data(self, data):
        # TODO: Implement send predictions back to the client
        print(f"Sending data... {data}")


def main():
    model = Model()
    host = "0.0.0.0"
    port = 6666

    server = Server()
    connection, _ = server.connect(host, port)

    while True:
        frame_data = server.receive_data(connection)

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        classes, scores = model.detect(frame)

        for c,s in zip(classes, scores):
            print(f"Class {model.classes[c]}, {s * 100:.2f}%")
        
        server.send_data(zip(classes, scores))


if __name__ == '__main__':
    main()