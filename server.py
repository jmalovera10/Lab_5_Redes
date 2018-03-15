import socket
import sys
from datetime import datetime
import time
import ast

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', int(sys.argv[1]))
    print (sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)
    clients = {}
    while True:
        print (sys.stderr, '\nwaiting to receive message')
        data, client = sock.recvfrom(4096)

        print (sys.stderr, 'received %s bytes from %s' % (len(data), client))
        print (sys.stderr, data)

        if data:
            print(client)
            parsedData = ast.literal_eval(data);
            sendTime = int(
                time.mktime(datetime.strptime(parsedData["marcaTiempo"], "%Y-%m-%d %H:%M:%S.%f").timetuple()))
            now = int(time.mktime(datetime.utcnow().timetuple()))
            delay = now - sendTime
            print(str(delay) + " ms")
            file = open(str(client), "a")
            file.write(data + "  delay: " + str(delay) + " ms" + "\n")
            file.close()
