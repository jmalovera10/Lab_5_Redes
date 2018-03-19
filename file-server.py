from __future__ import print_function
import threading
import socket
import sys
from datetime import datetime
import time
import ast
import hashlib


class UDPServer:
    def calculateLoss(client):
        data = client["data"]
        total = data[0]["sequenceLength"]
        total -= len(data)
        return total

    def calculateReceived(client):
        return len(client["data"])

    def averageDelay(client):
        data = client["data"]
        average = 0
        for d in data:
            average += int(d["delay"].split(" ")[0])
        average /= len(data)
        return str(average) + " ms"


class UDPWorker(threading.Thread):

    def __init__(self, buffer_size, client, sock, file_name):
        super(UDPWorker, self).__init__()
        self.buffer_size = buffer_size
        self.client = client
        self.sock = sock
        self.file_name = file_name

    def run(self):
        file = open("./files-served/" + self.file_name, "r")
        print(len(data))
        i = 1
        for line in file:
            message = {
                "sequence": i,
                "data": line,
                "sentTime": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            }
            hashm = hashlib.sha224(str(message).encode('utf-8')).hexdigest()
            message["hash"] = hashm
            print(str(message))
            self.sock.sendto(str(message).encode('utf-8'), self.client)
            i += 1

        file.close()


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
            parsedData = ast.literal_eval(data);

            # Delay calculation
            sendTime = int(
                time.mktime(datetime.strptime(parsedData["sentTime"], "%Y-%m-%d %H:%M:%S.%f").timetuple()))
            now = int(time.mktime(datetime.utcnow().timetuple()))
            delay = now - sendTime
            parsedData["delay"] = "" + str(delay) + " ms"
            print(str(delay) + " ms")

            # Gets the requested file
            request = parsedData["request"]
            worker = UDPWorker(buffer_size, client, sock, request)
            worker.start()
