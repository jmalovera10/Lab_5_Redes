import socket
import sys

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', sys.argv[1])
    print >> sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)
    while True:
        print >> sys.stderr, '\nwaiting to receive message'
        data, address = sock.recvfrom(4096)

        print >> sys.stderr, 'received %s bytes from %s' % (len(data), address)
        print >> sys.stderr, data

        if data:
            data, client = sock.recvfrom(4096)
            print(client)
            print >> sys.stderr, 'sent %s bytes back to %s' % (sent, address)
            file=open
