import socket
import sys

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', int(sys.argv[1]))
    print ( sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)
    while True:
        print ( sys.stderr, '\nwaiting to receive message')
        data, client = sock.recvfrom(4096)

        print ( sys.stderr, 'received %s bytes from %s' % (len(data), client))
        print ( sys.stderr, data)

        if data:
            print(client)
            file=open(str(client),"a")
            file.write(str(data))
            file.close()



