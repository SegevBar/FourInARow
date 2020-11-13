class Game:
    def __init__(self, id):
        self.row = 7
        self.colomn = 6
        self.board = [[-1]*self.colomn for i in range(self.row)]
        self.id = id
        self.currentPlayer = 0
        self.ready = False
        self.winner = -2

    def __repr__(self):
        board = ""
        for i in range(self.row):
            for j in range(self.colomn):
                board += " " + str(self.board[i][j]) + " "
            board += "\n"
        return board

    def connected(self):
        return self.ready

    def doMove(self, player, pos):
        if pos < 0 or pos >= self.colomn:
            return False
        elif self.board[0][pos] != -1:
            return False

        for j in range(self.row-1, -1, -1):
            if self.board[j][pos] == -1:
                self.board[j][pos] = player
                self.currentPlayer = (self.currentPlayer + 1) % 2
                return True
        return False

    def getBoard(self):
        return self.board

    def winning(self, k):
        counter = 1
        #check rows
        for j in range(self.row):
            for i in range(self.colomn-k+1):
                cur = self.board[j][i]
                if cur != -1:
                    for d in range(i + 1, i + k):
                        if counter == k:
                            self.winner = cur
                            return self.winner
                        elif self.board[j][d] == cur:
                            counter += 1
                        else:
                            counter = 1
                    if counter == k:
                        self.winner = cur
                        return self.winner

        #check colomns
        for i in range(self.colomn):
            for j in range(self.row-k+1):
                cur = self.board[j][i]
                if cur != -1:
                    for d in range(j + 1, j + k):
                        if counter == k:
                            self.winner = cur
                            return self.winner
                        elif self.board[d][i] == cur:
                            counter += 1
                        else:
                            counter = 1
                    if counter == k:
                        self.winner = cur
                        return self.winner

        #check diag top right bottom left
        for j in range(self.row-1, k-1, -1):
            for i in range(self.colomn-k+1):
                cur = self.board[j][i]
                if cur != -1:
                    for d in range(i + 1, i + k):
                        if counter == k:
                            self.winner = cur
                            return self.winner
                        elif self.board[j-d][d] == cur:
                            counter += 1
                        else:
                            counter = 1
                    if counter == k:
                        self.winner = cur
                        return self.winner

        #check diag top left bottom right
        for j in range(self.row-k+1):
            for i in range(self.colomn-k+1):
                cur = self.board[j][i]
                if cur != -1:
                    for d in range(i + 1, i + k):
                        if counter == k:
                            self.winner = cur
                            return self.winner
                        elif self.board[j+d][i+d] == cur:
                            counter += 1
                        else:
                            counter = 1
                    if counter == k:
                        self.winner = cur
                        return self.winner

        #checking if the board is full and no winner
        for i in range(self.colomn):
            for j in range(self.row):
                if self.board[j][i] == -1:
                    return self.winner
                elif i < self.colomn-2:
                    continue
                else:
                    self.winner = 2
                    return self.winner


    def resetBoard(self):
        self.board = [[-1] * self.colomn for i in range(self.row)]
        self.currentPlayer = 0
        self.id = id
        self.ready = False
        self.winner = -2
