import pygame
from network import Network
pygame.font.init()

width = 1000
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Four In A Row")

#players:
color0 = (174, 85, 141)
color1 = (85, 114, 174)

#board:
boardWidth = 600
boardHeight = 700
boardColor = (250,250,250)
leftBorder = (width-boardWidth)//2
rightBorder = leftBorder + boardWidth
topBorder = (height-boardHeight)//2
bottomBorder = topBorder + boardHeight
sizeBtwn = 100

class Disc:
    def __init__(self, p, mid):
        self.mid = mid
        self.radius = 30
        if p == 0:
            self.color = color0
        elif p == 1:
            self.color = color1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.mid, self.radius)


def redrawWindow(win, game, player):
    pygame.display.init()
    win.fill((255,255,255))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 0, (85,174,162))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        #draw player number
        pygame.draw.rect(win, (100,100,100), (0, 0, 50, 50))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(str(player+1), 1, (255, 255, 255))
        win.blit(text, (round(50 / 2) - round(text.get_width() / 2),
                        round(50 / 2) - round(text.get_height() / 2)))

        #draw board grid
        pygame.draw.rect(win, (100, 100, 100), (leftBorder, topBorder, boardWidth, boardHeight), 2)

        x = leftBorder
        for i in range(6):
            x = x + sizeBtwn
            pygame.draw.line(win, (100, 100, 100), (x, topBorder), (x, bottomBorder), 2)
        y = topBorder
        for j in range(7):
            y = y + sizeBtwn
            pygame.draw.line(win, (100, 100, 100), (leftBorder, y), (rightBorder, y), 2)

        #draw discs
        board = game.getBoard()
        for j in range(game.row):
            for i in range(game.colomn):
                if board[j][i] != -1:
                    mid = (leftBorder + i*100 + 50, topBorder + j*100 + 50)
                    disc = Disc(board[j][i], mid)
                    disc.draw(win)

        # draw reset botton
        pygame.draw.rect(win, (124, 200, 150), (width-150, height-90, 130, 60))
        font = pygame.font.SysFont("comicsans", 36)
        text = font.render("Restart", 1, (255, 255, 255))
        win.blit(text, (width-150 + round(130 / 2) - round(text.get_width() / 2),
                        height-90 + round(60 / 2) - round(text.get_height() / 2)))
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:  #main game loop
        clock.tick(60)   #compute how many milliseconds have passed since the previous call.
        try:
            game = n.send("get")  #asking the server to send the game
        except:
            run = False
            print("Lost connection with other player")
            break

        redrawWindow(win, game, player)

        font = pygame.font.SysFont("comicsans", 90)
        if game.winner != -2:
            if game.winner == player:
                text = font.render("You Won!", 1, (150, 150, 150))
            elif game.winner == 2:
                text = font.render("No winner this time...", 1, (150, 150, 150))
            else:
                text = font.render("You Lost...", 1, (150, 150, 150))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i in range(game.colomn):
                    if (leftBorder + i*sizeBtwn) < x < (leftBorder + (i+1)*sizeBtwn) and (topBorder) < y < (bottomBorder) and game.connected():
                        n.send(str(i))

                if width-150 < x < width-20 and height-90 < y < height-30:
                    try:
                        game = n.send("reset")
                    except:
                        run = False
                        print("Couldn't get game")


            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                pygame.display.quit()
                break

main()

