# Four In A Row
The popular board game in which two players choose a color and then take turns dropping colored discs into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the lowest available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs.

Written with pygame module.

Code Structure- A server-client model:

Server- has 3 parts:
- Intiate sockets
- Threading- connecting to clients and creating a new game
- While loop- getting moves from players and updating the game for all clients. Resets game when finished.

Client- runs for each player locally, responsible for:
- Uses Network class to recieve game board from server and to send players moves to server
- redrawWindow - using pygame to draw the game window and board
- main - defining the while loop of the game


Network- responsible for the connection between client and server. This class has 4 methods:
- init - initiates server IP and calls "connect" method, stores connect's output as the player ID
- connect - connects to server and returns server's response
- send(data) - recieves string data and send it to server, returns server's response
- getP- get the player ID

Game- definnig the game mechanism. The game board is stored as an 2d array of 6x7. This class has the following methods:
- init - initiates an empty gameboard
- doMove(player, position) - returns True if move is legal, updates the game board. If move is illegal returns False
- getBoard - returns the current game board
- winning - checks if a player has four in a row. If so, return the player number, else returns -1. If the board is full and no winner, returns -2
- resetBoard - resets the board for a new game
