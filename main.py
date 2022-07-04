import pygame
from copy import deepcopy
import random
import time
import ctypes

ctypes.windll.user32.SetProcessDPIAware()
WIDTH, HEIGHT = 10, 20
TILE = 30
GAME_RES = WIDTH * TILE, HEIGHT * TILE
FPS = 60
RES = 1100, 753
pygame.init()
instr_button_visible= True
main_font = pygame.font.Font('freesansbold.ttf', 65)
small_font= pygame.font.Font('freesansbold.ttf', 20)
title = main_font.render('CATETRIS', True, pygame.Color('black'))
titleScore = main_font.render('score', True, pygame.Color('red'))
titleRecord = main_font.render('record', True, pygame.Color('green'))
get_color = lambda: (random.randrange(30, 256), random.randrange(30, 256), random.randrange(30, 256))
color = get_color()
count, speed, limit = 0, 60, 2000
p = [[0 for i in range(WIDTH)] for i1 in range(HEIGHT)]
pygame.display.set_caption('Catetris')
screen = pygame.display.set_mode(RES)
gameScreen = pygame.Surface(GAME_RES)
menuscreen = pygame.Surface(GAME_RES)
restartscreen = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(WIDTH) for y in range(HEIGHT)]
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
bg3 = pygame.image.load('images/2.jpg').convert()


def borders():
    if figure[i].x < 0 or figure[i].x > WIDTH - 1:
        return True
    elif figure[i].y > HEIGHT - 1 or p[figure[i].y][figure[i].x]:

        return True
    return False

def initrestart():
    screen.blit(restartscreen, (45, 156))
    restartscreen.blit(bg3, (0, 0))
    restartscreen.blit(main_font.render('GAME', True, pygame.Color('red')), (53, 140))
    restartscreen.blit(main_font.render('OVER', True, pygame.Color('red')), (60, 190))
    restartscreen.blit(small_font.render('to quit press q', True, pygame.Color('black')), (80, 280))
    restartscreen.blit(small_font.render('or press any other  ', True, pygame.Color('black')), (60, 320))
    restartscreen.blit(small_font.render('button to play again', True, pygame.Color('black')), (50, 360))
    pygame.display.flip()

def restart():
    initrestart()

    ext= False
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit("exit")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 600 <= mouse[0] <= 736 and 500 <= mouse[1] <= 534:
                    instr_button_visible = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit("exit")
                    ext = True
                if event.key != pygame.K_q and event.key != pygame.K_LEFT and event.key != pygame.K_RIGHT and event.key != pygame.K_UP and event.key != pygame.K_DOWN:
                    ext= True
        if ext:
            break



def menuinit():
    if (not instr_button_visible):
        s = "welcome to CATETRIS\nthis game is a subversion of popular game called tetris\nto start playing follow the instructions written on the gamescreen\nkey buttons:\n1) press \"right\" and \"left\" arrows to move the falling brick.\n2) press \"up\" arrow to rotate the falling brick\n3) press \"down\" arrow to make your falling brick fall faster\nyou earn score points when you complete 1 or more horizontal lines\nif you complete:1 line at a time - 100 points\n2 lines at a time  - 300 points\n3 lines at a time  - 700 points\n4 lines at a time - 1500 points\nWe wish you luck and hope you will enjoy playing our CATETRIS game\n Press [space] to hide"
        guide = small_font.render(s, True, pygame.Color('black'))
        pygame.draw.rect(screen, pygame.Color('grey'), pygame.Rect(380, 380, 730, 310))
        blit_text(screen, s, (400, 400), small_font)
    if (instr_button_visible):
        instr_button = pygame.Rect(600, 500, 136, 34)
        pygame.draw.rect(screen, pygame.Color("grey"), instr_button)
        instr_text = small_font.render('Instructions', True, pygame.Color('black'))
        screen.blit(instr_text, (607, 507))

    screen.blit(menuscreen, (45, 156))
    menuscreen.blit(bg3, (0, 0))
    menuscreen.blit(small_font.render('Choose difficulty, 1-5', True, pygame.Color('black')), (55, 210))
    menuscreen.blit(small_font.render('Press number 1-5 on', True, pygame.Color('black')), (60, 240))
    menuscreen.blit(small_font.render('keyboard to choose it', True, pygame.Color('black')), (55, 270))
    menuscreen.blit(small_font.render('and start a game', True, pygame.Color('black')), (70, 300))
    pygame.display.flip()



def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split('\n') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def menu():
    menuinit()
    global instr_button_visible
    ext= False
    global speed
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit("exit")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 600 <= mouse[0] <= 736 and 500 <= mouse[1] <= 534:
                    instr_button_visible = False
                    render_texts()
                    menuinit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    instr_button_visible = True
                    render_texts()
                    menuinit()
                if event.key == pygame.K_q:
                    exit("exit")
                if event.key == pygame.K_1:
                    speed = 10
                    ext=True
                if event.key == pygame.K_2:
                    speed = 40
                    ext = True
                if event.key == pygame.K_3:
                    speed = 80
                    ext = True
                if event.key == pygame.K_4:
                    speed = 100
                    ext = True
                if event.key == pygame.K_5:
                    speed = 130
                    ext = True

        if ext:
            break


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
# score
score, line = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
firstLaunch = True


def render_texts():
    global recordd
    recordd = record()
    screen.blit(bg1, (0, 0))
    screen.blit(title, (350, 20))
    screen.blit(titleScore, (420, 90))
    screen.blit(main_font.render(str(score), True, pygame.Color('black')), (420, 170))
    screen.blit(titleRecord, (700, 90))
    screen.blit(main_font.render(str(recordd), True, pygame.Color('black')), (950, 90))

while True:
    render_texts()

    if firstLaunch:
        menuinit()
        menu()
        firstLaunch = False

    screen.blit(gameScreen, (45, 156))
    gameScreen.blit(bg2, (0, 0))

    # delay
    for i in range(line):
        pygame.time.wait(200)
    xx, r = 0, False
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit("exit")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 600 <= mouse[0] <= 736 and 500 <= mouse[1] <= 534:
                instr_button_visible = False
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
    for row in range(HEIGHT - 1, -1, -1):
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
    # scooore
    score += scores[line]
    # delete full lines

    # game over :(
    for i in range(WIDTH):
        if p[0][i]:
            set_record(recordd, score)
            p = [[0 for i in range(WIDTH)] for i1 in range(HEIGHT)]
            count, speed, limit = 0, 60, 2000
            score = 0
            initrestart()
            restart()
            menu()

    pygame.display.flip()

clock.tick(FPS)

