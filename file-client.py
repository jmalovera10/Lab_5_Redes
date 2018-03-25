from __future__ import print_function
import socket
import sys
import ast
import time
from datetime import datetime
import hashlib


def calculateLoss(client):
    data = client["data"]
    total = data[0]["sequenceLength"]
    total -= len(data)
    return total


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (sys.argv[1], int(sys.argv[2]))
    buffer_size = int(sys.argv[3])
    file_request = sys.argv[4]
    packet_amount = None
    corrupted = 0
    received = {
        "data": []
    }
    sendTime = 0
    try:
        # Send request
        message = {
            "request": file_request,
            "sentTime": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        }

        print(str(message))

        print(sys.stderr, 'sending "%s"' % message)
        sent = sock.sendto(str(message).encode('utf-8'), server_address)

        # Receive response
        data = 1
        sendTime = int(time.mktime(datetime.utcnow().timetuple()))
        while data != "":
            sock.settimeout(1)
            # print(sys.stderr, 'waiting to receive')
            data, server = sock.recvfrom(buffer_size)
            parsedData = ast.literal_eval(data);
            hashm = parsedData["hash"]
            del parsedData["hash"]
            verify = hashlib.sha224(str(parsedData).encode('utf-8')).hexdigest()
            if hashm == verify:
                # print(parsedData)
                parsedData["integrity"] = "ACK"
                if not packet_amount:
                    packet_amount = parsedData["sequenceLength"]
            else:
                # print("Message " + str(parsedData["sequence"]) + " was corrupted")
                parsedData["integrity"] = "NACK"
                corrupted += 1
            received["data"].append(parsedData)
    except socket.timeout:
        print("Connection timed out")
    finally:
        now = int(time.mktime(datetime.utcnow().timetuple()))
        timelapse = (now - sendTime)
        print(sys.stderr, 'closing socket')
        print("Time elapsed: " + str(timelapse) + " s")
        print("Corrupted packages: " + str(corrupted))
        print("Lost packages: " + str(calculateLoss(received)))
        sock.close()
