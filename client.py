import socket
import sys
import datetime

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (sys.argv[0], sys.argv[1])
    object_amount = sys.argv[2]
    try:
        # Send data
        for i in range(object_amount):

            message = {
                "numeroSecuencia": i,
                "marcaTiempo": datetime.datetime.now
            }

            print >> sys.stderr, 'sending "%s"' % message
            sent = sock.sendto(message, server_address)

            # Receive response
            print >> sys.stderr, 'waiting to receive'
            data, server = sock.recvfrom(4096)
            print >> sys.stderr, 'received "%s"' % data

    finally:
        print >> sys.stderr, 'closing socket'
        sock.close()

