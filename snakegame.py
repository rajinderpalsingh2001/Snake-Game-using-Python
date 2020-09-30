import pygame, sys, random
from pygame.locals import *
from pymysql import *

pygame.init()
FPS = 15
OLDSCORE=0
FPSLIST = [3, 6, 9, 12, 15, 18, 21, 24]
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

SCORE = 0
OLDSCORE=0


def main():
    global DISPLAYSURFACE, FPSCLOCK, BASICFONT,OLDSCORE
    DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH+200, WINDOWHEIGHT))
    FPSCLOCK = pygame.time.Clock()
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    startscreen()
    while True:
        playgame()
        insertscore(SCORE)
        endscreen()

def startscreen():
    flag=0
    while True:
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                flag=1
            elif event.type==QUIT:
                terminate()
        if flag==1:
            break
        Snaketext = pygame.font.Font('freesansbold.ttf', 58)

        text = Snaketext.render("Snake Game", True, GREEN)
        print(text.get_width())
        DISPLAYSURFACE.blit(text, (270,200))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def playgame():
    global FPS, SCORE,OLDSCORE
    SCORE = 0
    fetchlastscore()
    xcord = random.randint(5, CELLWIDTH - 6)
    ycord = random.randint(5, CELLHEIGHT - 6)
    snakecord = [
        {'x': xcord, 'y': ycord},
        {'x': xcord - 1, 'y': ycord},
        {'x': xcord - 2, 'y': ycord},
    ]
    # print(snakecord)
    apples = randomfr()
    direction = 1
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif (event.key == K_UP or event.key == K_w) and direction != 3:
                    direction = 4
                elif (event.key == K_DOWN or event.key == K_s) and direction != 4:
                    direction = 3
                elif (event.key == K_LEFT or event.key == K_a) and direction != 1:
                    direction = 2
                elif (event.key == K_RIGHT or event.key == K_d) and direction != 2:
                    direction = 1

        DISPLAYSURFACE.fill(BGCOLOR)
        for row in snakecord[1:]:
            # print(row)
            if row['x'] == snakecord[0]['x'] and row['y'] == snakecord[0]['y']:
                terminate()
        if direction == 1:
            newcord = {'x': snakecord[0]['x'] + 1, 'y': snakecord[0]['y']}
        elif direction == 2:
            newcord = {'x': snakecord[0]['x'] - 1, 'y': snakecord[0]['y']}
        elif direction == 3:
            newcord = {'x': snakecord[0]['x'], 'y': snakecord[0]['y'] + 1}
        elif direction == 4:
            newcord = {'x': snakecord[0]['x'], 'y': snakecord[0]['y'] - 1}
        snakecord.insert(0, newcord)

        if snakecord[0]['x'] == apples['x'] and snakecord[0]['y'] == apples['y']:
            apples = randomfr()
            SCORE += 1
            if SCORE in FPSLIST:
                FPS = FPS + 2
                print(FPS)
            print(SCORE)
        else:
            del snakecord[-1]
        Snaketext = pygame.font.Font('freesansbold.ttf', 28)
        text=Snaketext.render("Snake Game",True,GREEN)
        DISPLAYSURFACE.blit(text,(650,30))
        Snaketext = pygame.font.Font('freesansbold.ttf', 24)
        text=Snaketext.render(f"Score: {SCORE}",True,GREEN)
        DISPLAYSURFACE.blit(text,(650,60))
        if SCORE>OLDSCORE:
            OLDSCORE=SCORE
        text = Snaketext.render(f"MAX SCORE: {OLDSCORE}", True, GREEN)
        DISPLAYSURFACE.blit(text, (650, 90))
        # print(snakecord)

        if snakecord[0]['x'] == -1 or snakecord[0]['x'] == CELLWIDTH or snakecord[0]['y'] == -1 or snakecord[0][
            'y'] == CELLHEIGHT:
            break
            # terminate()
        makeapple(apples)
        makegrid()
        makesnake(snakecord)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def fetchlastscore():
    global OLDSCORE
    con = connect('127.0.0.1', 'root', '', 'snakegame')
    cr = con.cursor()
    query2 = "SELECT max(score) FROM `scoreboard`"
    cr.execute(query2)
    result = cr.fetchone()
    OLDSCORE=result[0]


def insertscore(SCORE):
    print(SCORE)
    con = connect('127.0.0.1', 'root', '123456', 'snakegame')
    query = f"insert into `scoreboard` (`score`) VALUES ('{SCORE}')"
    cr = con.cursor()
    cr.execute(query)
    con.commit()


def randomfr():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def makeapple(fcords):
    xc = fcords['x'] * CELLSIZE
    yc = fcords['y'] * CELLSIZE
    snakerect = pygame.Rect(xc, yc, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURFACE, WHITE, snakerect)


def makesnake(snakecord):
    for row in snakecord:
        xc = row['x'] * CELLSIZE
        yc = row['y'] * CELLSIZE
        snakerect = pygame.Rect(xc, yc, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURFACE, GREEN, snakerect)


def makegrid():
    for x in range(0, WINDOWWIDTH+20, CELLSIZE):
        pygame.draw.line(DISPLAYSURFACE, RED, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURFACE, RED, (0, y), (WINDOWWIDTH, y))

def endscreen():
    flag=0
    while True:
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                flag=1
            elif event.type==QUIT:
                terminate()
        if flag==1:
            break
        Snaketext = pygame.font.Font('freesansbold.ttf', 68)
        text = Snaketext.render("Game Over", True, RED)
        print(text.get_width())
        DISPLAYSURFACE.blit(text, (270,200))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def terminate():
    pygame.quit()
    sys.exit()


print(__name__)
if __name__ == '__main__':
    main()
