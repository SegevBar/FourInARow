import socket
from _thread import *
import pickle
from game import Game

server = "localhost" #server IP
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket connecting

try:
    s.bind((server, port))   #bind the socket to address=(host, port)
except socket.error as e:
    str(e)

s.listen(1)    #listen for connections made to the socket
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))  #send player's number to thair client

    while True:
        try:
            data = conn.recv(4096).decode()  #recv = receive data from the client in bits, decode- from bit to relevent data

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:  #checking the data recieved from client
                    if data == "reset":
                        game.resetBoard()
                    elif data != "get":  #if the data is a player move
                        print("Player=", game.currentPlayer)
                        if game.currentPlayer == p:
                            game.doMove(p, int(data))
                            game.winning(4)

                    conn.sendall(pickle.dumps(game))  #sending the updated game to client
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]  #delete the game if connection to one of the client is lost, or problem with data
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()   #close the socket



while True:
    conn, addr = s.accept()   #accept a connection. conn is a new socket object usable to send and receive data on the connection, and address is the address bound to the socket on the other end of the connection.
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:    #if new player joined and dosent have an open game to join tp- create a new game
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True  #2 players connected to the game- ready to start the game
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))