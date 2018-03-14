import socket
import sys
import datetime

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (sys.argv[1], int(sys.argv[2]))
    object_amount = int(sys.argv[3])
    try:
        # Send data
        for i in range(object_amount):
            message = {
                "numeroSecuencia": i,
                "marcaTiempo": str(datetime.datetime.now)
            }

            print(str(datetime.datetime.now))

            print(sys.stderr, 'sending "%s"' % message)
            sent = sock.sendto(str(message).encode('utf-8'), server_address)

            # Receive response
            #print(sys.stderr, 'waiting to receive')
            # data, server = sock.recvfrom(4096)
            #print(sys.stderr, 'received "%s"' % data)

    finally:
        print(sys.stderr, 'closing socket')
        sock.close()
