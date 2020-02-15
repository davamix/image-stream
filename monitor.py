import cv2
import socket
import pickle
import struct
import json

class Monitor():
    def __init__(self):
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = b""
        self.payload_size = struct.calcsize(">L")

        self.configuration = self.load_configuration("config.json")

        self.setup_input_connections()

    def load_configuration(self, file):
        with open(file) as json_data:
            return json.load(json_data)

    def setup_input_connections(self):
        host = self.configuration["monitor"]["input"]["host"]
        port = self.configuration["monitor"]["input"]["port"]

        self.input_socket.bind((host, port))
        print(f"Listening: {host}: {port}")

        self.input_socket.listen(10)

    def connect(self):        
        conn, addr = self.input_socket.accept()
        return conn, addr

    def receive_data(self, connection):
        while len(self.data) < self.payload_size:
            self.data += connection.recv(4096)

        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        while(len(self.data) < msg_size):
            self.data += connection.recv(4096)

        predictions = self.data[:msg_size]
        self.data = self.data[msg_size:]

        return predictions

def main():
    print("## MONITOR ##")
    monitor = Monitor()
    connection, _ = monitor.connect()

    while True:
        data = monitor.receive_data(connection)

        prediction = pickle.loads(data, fix_imports=True, encoding="bytes")
        #print(prediction)
        
        # TODO: Decode prediction
        #print(prediction)
        cv2.imshow('Prediction', prediction)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()