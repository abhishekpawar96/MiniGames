import pickle
import socket
from _thread import *
import sys

from Network.colors import RED, BLUE
from Network.player import Player

server = "10.52.99.220"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server started...")

players = [Player(0, 0, 50, 50, RED), Player(100, 100, 50, 50, BLUE)]


def threaded_client(c, p):
    c.send(pickle.dumps(players[p]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[p] = data
            if not data:
                print("Disconnected")
                break
            else:
                if p == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)
            c.sendall(pickle.dumps(reply))

        except:
            break

    print("Lost Connection")
    c.close()


currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1


