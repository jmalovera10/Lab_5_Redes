import socket
import sys
import ast
import json
from datetime import datetime
import hashlib

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (sys.argv[1], int(sys.argv[2]))
    buffer_size = int(sys.argv[3])
    file_request = sys.argv[4]
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
        while data != "":
            print(sys.stderr, 'waiting to receive')
            data, server = sock.recvfrom(buffer_size)
            parsedData = ast.literal_eval(data);
            hashm = parsedData["hash"]
            del parsedData["hash"]
            verify = hashlib.sha224(str(parsedData).encode('utf-8')).hexdigest()
            if hashm == verify:
                print(parsedData)
                conver = unicode(parsedData["data"], errors='replace')
                print(conver)
                file = open("./files-received/" + file_request, "a")
                file.write(ord(conver), indent=0)
                file.close()
                print(sys.stderr, 'received "%s"' % parsedData)
            else:
                print("Message " + str(parsedData["sequence"]) + " was corrupted")

    finally:
        print(sys.stderr, 'closing socket')
        sock.close()
