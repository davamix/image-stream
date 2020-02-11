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


model = Model()

host = "0.0.0.0"
port = 6666

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print(f"Listening: {host}:{port}")

s.listen(10)
conn, addr = s.accept()

data = b""
payload_size = struct.calcsize(">L")

while True:
    while len(data) < payload_size:
        #print(f"Recv: {len(data)}")
        data += conn.recv(4096)

    #print(f"Done recv: {len(data)}")

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    #print(f"msg_size: {msg_size}")

    while(len(data) < msg_size):
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # cv2.imshow('Window', frame)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    model.detect(frame)

cv2.destroyAllWindows()