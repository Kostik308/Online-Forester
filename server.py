import socket
import pickle
from _thread import *
from player import Player

server = '192.168.1.250'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print('\033[33m{}\033[0m'.format('Waiting for connection, Server started.'))

players = [Player(0, 0, 50, 50, (255, 0, 128)), Player(100, 100, 50, 50, (128, 128, 0))]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("\033[31m{}\033[0m".format('Disconnected'))
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                
                print("\033[36m{}".format('Received:'), data, "\033[0m")
                print("\033[36m{}".format(' Sending:'), reply, "\033[0m")
            
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("\033[31m{}\033[0m".format('Connection lost'))
    conn.close()

currPlayer = 0

while True:
    conn, addr = s.accept()
    print("\033[32m{}".format('Connected to'), addr[0], 'with port', addr[1], "\033[0m")

    start_new_thread(threaded_client, (conn, currPlayer))
    currPlayer += 1