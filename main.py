import pygame
from copy import deepcopy
import random
WIDTH, HEIGHT = 10, 20
TILE = 30
GAME_RES = WIDTH*TILE, HEIGHT*TILE
FPS = 60
RES = 1100, 756
pygame.init()
main_font = pygame.font.Font('fonts/Cheltenham-Normal.ttf', 65)
title = main_font.render('CATETRIS', True, pygame.Color('black'))
titleScore = main_font.render('score', True, pygame.Color('red'))
titleRecord = main_font.render('record', True, pygame.Color('green'))
get_color = lambda : (random.randrange(30, 256), random.randrange(30, 256), random.randrange(30, 256))
color = get_color()
count, speed, limit = 0, 60, 2000
p = [[0 for i in range(WIDTH)] for i1 in range(HEIGHT)]
screen = pygame.display.set_mode(RES)
gameScreen = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()
grid = [pygame.Rect(x*TILE, y*TILE, TILE, TILE) for x in range(WIDTH) for y in range(HEIGHT)]
figuresCoord = [
    [(0, 0), (0, -1), (0, 1), (-1, 0)],
    [(0, 0), (0, -1), (0, 1), (1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, -1)],
    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
    [(-1, 0), (-1, 1), (0, 0), (0, -1)],
    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
    [(-1, 0), (-2, 0), (0, 0), (1, 0)],
]
bg1 = pygame.image.load('images/1.jpg').convert()
bg2 = pygame.image.load('images/11.jpg').convert()
def borders():
    if figure[i].x < 0 or figure[i].x > WIDTH-1:
        return True
    elif figure[i].y > HEIGHT - 1 or p[figure[i].y][figure[i].x]:

        return True
    return False




def record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(rec, scor):
    rek = (max(int(rec), score))
    with open('record', 'w') as f:
        f.write(str(rek))


    


figures = [[pygame.Rect(x + WIDTH // 2, y + 1, 1, 1) for x, y in i] for i in figuresCoord]
rectfig = pygame.Rect(0, 0, TILE - 2, TILE - 2)
figure = deepcopy(random.choice(figures))
#score
score, line = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
while True:
    recordd = record()
    screen.blit(bg1, (0, 0))
    screen.blit(gameScreen, (45, 156))
    gameScreen.blit(bg2, (0, 0))

#delay
    for i in range(line):
        pygame.time.wait(200)
    xx, r = 0, False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit("exit")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xx = -1
            if event.key == pygame.K_RIGHT:
                xx = 1
            if event.key == pygame.K_DOWN:
                limit = 400
            if event.key == pygame.K_UP:
                r = True

    figure1 = deepcopy(figure)
    for i in range(4):
        figure[i].x += xx
        if borders():
            figure = deepcopy(figure1)
            break
    [pygame.draw.rect(gameScreen, (40, 40, 40), i, 1) for i in grid]
    for i in range(4):
        rectfig.x = figure[i].x * TILE
        rectfig.y = figure[i].y * TILE
        pygame.draw.rect(gameScreen, color, rectfig)

    count += speed
    if count > limit:
        count = 0
        figure1 = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if borders():
                for i in range(4):
                    p[figure1[i].y][figure1[i].x] = color
                color = get_color()
                figure = deepcopy(random.choice(figures))
                limit = 2000
                break
    for y, row in enumerate(p):
        for x, column in enumerate(row):
            if column:
                rectfig.x, rectfig.y = x * TILE, y * TILE
                pygame.draw.rect(gameScreen, column, rectfig)
    # ////// rotation mechanics
    centerOfRotation = figure[0]
    figure1 = deepcopy(figure)

    if (r):
        for i in range(4):
            x = figure[i].y - centerOfRotation.y
            y = figure[i].x - centerOfRotation.x
            figure[i].x = centerOfRotation.x - x
            figure[i].y = centerOfRotation.y - y
            if borders():
                figure = deepcopy(random.choice(figures))
                break

    # //////
    # delete full lines
    l_quantity, line = HEIGHT - 1, 0
    for row in range(HEIGHT-1, -1, -1):
        counter = 0
        for i in range(WIDTH):
            if p[row][i]:
                counter += 1
            p[l_quantity][i] = p[row][i]
        if counter < WIDTH:
            l_quantity -= 1
        else:
            speed += 3
            line += 1
    #scooore
    score += scores[line]
    # delete full lines

    #game over :(
    for i in range(WIDTH):
        if p[0][i]:
            set_record(recordd, score)
            p = [[0 for i in range(WIDTH)] for i1 in range(HEIGHT)]
            count, speed, limit = 0, 60, 2000
            score = 0
    # game over :(
    screen.blit(title, (350, 20))
    screen.blit(titleScore, (420, 90))
    screen.blit(main_font.render(str(score), True, pygame.Color('black')), (420, 170))
    screen.blit(titleRecord, (700, 90))
    screen.blit(main_font.render(str(recordd), True, pygame.Color('black')), (950, 90))
    pygame.display.flip()

clock.tick(FPS)

