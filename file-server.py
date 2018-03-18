import socket
import sys
from datetime import datetime
import time
import ast
import json


class UDP_Server:
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
        return str(average)+" ms"

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

                # Delay calculation
                sendTime = int(
                    time.mktime(datetime.strptime(parsedData["sentTime"], "%Y-%m-%d %H:%M:%S.%f").timetuple()))
                now = int(time.mktime(datetime.utcnow().timetuple()))
                delay = now - sendTime
                parsedData["delay"] = "" + str(delay) + " ms"
                print(str(delay) + " ms")

                # Store data in local variable
                if not str(client) in clients:
                    clients[str(client)] = {}
                    clients[str(client)]["data"] = [parsedData]
                else:
                    clients[str(client)]["data"].append(parsedData)

                # Loss calculation
                lost = calculateLoss(clients[str(client)])
                clients[str(client)]["lost"] = lost

                # Received calculation
                received = calculateReceived(clients[str(client)])
                clients[str(client)]["received"] = received

                # Average delay calculation
                average = averageDelay(clients[str(client)])
                clients[str(client)]["averageDelay"] = average

                # File writing
                file = open("./clientRecords/"+str(client), "w")
                file.write(json.dumps(clients[str(client)], indent=2))
                file.close()
