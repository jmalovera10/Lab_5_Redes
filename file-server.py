from __future__ import print_function
import threading
import socket
import sys
from datetime import datetime
import ast
import hashlib


class UDPWorker(threading.Thread):

    def __init__(self, buffer_size, client, sock, file_name):
        super(UDPWorker, self).__init__()
        self.buffer_size = buffer_size
        self.client = client
        self.sock = sock
        self.file_name = file_name

    def run(self):
        file_len = {
            "size": 0
        }
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.buffer_size)
        file = open("./files-served/" + self.file_name, "rb")
        i = 1
        for piece in self.read_in_chunks(file, file_len, chunk_size=10240):
            print("")
        file = open("./files-served/" + self.file_name, "rb")
        dummy = {"size": 0}
        for piece in self.read_in_chunks(file, dummy, chunk_size=10240):
            message = {
                "sequence": i,
                "sequenceLength": file_len["size"],
                "data": piece,
                "sentTime": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            }
            hashm = hashlib.sha224(str(message).encode('utf-8')).hexdigest()
            message["hash"] = hashm
            #print(str(message))
            self.sock.sendto(str(message).encode('utf-8'), self.client)
            i += 1

        file.close()

    def read_in_chunks(self, file_object, size, chunk_size=None):
        while True:
            data = file_object.read(chunk_size)
            size["size"] += 1
            if not data:
                break
            yield data


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', int(sys.argv[1]))
    print(sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)
    buffer_size = int(sys.argv[2])
    clients = {}
    while True:
        print(sys.stderr, '\nwaiting to receive message')
        data, client = sock.recvfrom(buffer_size)

        print(sys.stderr, 'received %s bytes from %s' % (len(data), client))
        print(sys.stderr, data)

        if data:
            print(client)
            parsedData = ast.literal_eval(data)

            # Gets the requested file
            request = parsedData["request"]
            worker = UDPWorker(buffer_size, client, sock, request)
            worker.start()
