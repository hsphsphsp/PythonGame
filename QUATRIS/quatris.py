#Quatris (a Tetris clone)
# Originally By Al Sweigart al@inventwithpython.com
# Rearrange By Alegruz
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
# https://alegruz.imweb.me/blog
# version 1

import random, time, pygame, sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 1600
WINDOWHEIGHT = 990
BOXSIZE = 20
CENTERWIDTH = 5
CENTERHEIGHT = 5
BOARDWIDTH = CENTERWIDTH + 40
BOARDHEIGHT = CENTERHEIGHT + 40
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)
GREY        = ( 50,  50,  50)
LIGHTGREY   = ( 70,  70,  70)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW, GREY)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW, LIGHTGREY)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Quatris')
    pygame.joystick.init()

    global famicom, joystick

    joystick = False
    
    if pygame.joystick.get_count() >= 0:
        famicom = pygame.joystick.Joystick(0)
        if famicom.get_name() == 'BUFFALO BGC-FC801 USB Gamepad':
            famicom.init()
    
    global ct, channel1, channel2, pause, smb, tloz, line_clear_sound, bump, end, gameover, ab, tetris, gta_4, ff, tes_4_o, f_3, h, h_3, tes_5_s_d, tes_5_s_f, p_1, p_2, m, tw_3_wh

    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)

    pause = pygame.mixer.Sound('smb_pause.wav')
    line_clear_sound = pygame.mixer.Sound('smb_1-up.wav')
    bump = pygame.mixer.Sound('smb_bump.wav')
    end = pygame.mixer.Sound('smb_mariodie.wav')
    gameover = pygame.mixer.Sound('smb_gameover.wav')
    insertcoin = pygame.mixer.Sound('smb_coin.wav')

    ct = pygame.mixer.Sound('ct_main.wav')
    smb = pygame.mixer.Sound('smb_overworld.wav')
    tloz = pygame.mixer.Sound('tloz_intro.wav')
    ab = pygame.mixer.Sound('ab_main.wav')
    tetris = pygame.mixer.Sound('tetris.wav')
    gta_4 = pygame.mixer.Sound('gta4_soviet.wav')
    ff = pygame.mixer.Sound('ff_main.wav')
    tes_4_o = pygame.mixer.Sound('tes4o_main.wav')
    f_3 = pygame.mixer.Sound('f3_main.wav')
    h = pygame.mixer.Sound('h_onefinaleffort.wav')
    h_3 = pygame.mixer.Sound('h3_neverforget.wav')
    tes_5_s_f = pygame.mixer.Sound('tes5s_farhorizons.wav')
    tes_5_s_d = pygame.mixer.Sound('tes5s_dragonborn.wav')
    p_1 = pygame.mixer.Sound('p1_stillalive.wav')
    p_2 = pygame.mixer.Sound('p2_caramiaaddio.wav')
    m = pygame.mixer.Sound('m_sweden.wav')
    tw_3_wh = pygame.mixer.Sound('tw3wh_main.wav')

    life = 3
    showTextScreen('Quatris')
    while life >= 0: # game loop
        global music
        music = random.choice([ct, smb, tloz, ab, tetris, gta_4, ff, tes_4_o, f_3, h, h_3, tes_5_s_d, tes_5_s_f, p_1, p_2, m, tw_3_wh])
        channel1.play(music, loops = -1)
        runGame(life)
        channel1.stop()
        channel2.play(end, 0)
        showTextScreen('Game Over')
        life -= 1
    DISPLAYSURF.fill(BGCOLOR)
    channel2.play(gameover, 0)
    showTextScreen('Insert Coin')  # pause until a key press
    channel2.play(insertcoin, 0)

def runGame(life):
    # setup variables for the start of the game
    board = getBlankBoard()
    direction = 0
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0

    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece(0)
    nextPiece = getNewPiece(1)
    next_direction = 1

    JOYAXISDOWN = False
    JOYAXISUP = False

    while True: # game loop
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            movingDown = False
            movingRight = False
            movingLeft = False
            fallingPiece = nextPiece
            direction = next_direction
            next_direction = (direction + 1) % 4
            nextPiece = getNewPiece(next_direction)
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return # can't fit a new piece on the board, so game over
        if direction == 0:
            for y in range(BOARDHEIGHT):
                if board[BOARDWIDTH - 1][y] != BLANK:
                    return
        elif direction == 1:
            for x in range(BOARDWIDTH):
                if board[x][BOARDHEIGHT - 1] != BLANK:
                    return
        elif direction == 2:
            for y in range(BOARDHEIGHT):
                if board[0][y] != BLANK:
                    return
        else:
            for x in range(BOARDWIDTH):
                if board[x][0] != BLANK:
                    return

        checkForQuit()

        '''
        for event in pygame.event.get(): # event handling
            if event.type == (KEYUP or JOYBUTTONUP):
                if event.key == K_p or famicom.get_button(7):
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    channel1.pause()
                    channel2.play(pause)
                    showTextScreen('Paused') # pause until a key press
                    channel1.unpause()
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or famicom.get_axis(0) < 0):
                    if direction == 0 or direction == 2:
                        movingLeft = False
                    elif direction == 1:
                        movingDown = False
                elif (event.key == K_RIGHT or famicom.get_axis(0) > 0):
                    if direction == 0 or direction == 2:
                        movingRight = False
                    elif direction == 3:
                        movingDown = False
                elif (event.key == K_DOWN or famicom.get_axis(1) > 0):
                    if direction == 0:
                        movingDown = False
                    elif direction == 1 or direction == 3:
                        movingRight = False
                elif (event.key == K_UP or famicom.get_axis(1) < 0):
                    if direction == 1 or direction == 3:
                        movingLeft = False
                    elif direction == 2:
                        movingDown = False

            elif event.type == (KEYDOWN or JOYBUTTONDOWN):
                # moving the piece sideways
                if (event.key == K_r or famicom.get_button(1)):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(
                            PIECES[fallingPiece['shape']])

                elif (event.key == K_LEFT or famicom.get_axis(0) < 0):
                    if direction == 0 or direction == 2:
                        if isValidPosition(board, fallingPiece, adjX=-1):
                            fallingPiece['x'] -= 1
                            movingLeft = True
                            movingRight = False
                            lastMoveSidewaysTime = time.time()
                    elif direction == 1:
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjX=-1):
                            fallingPiece['x'] -= 1
                        lastMoveDownTime = time.time()
                    else:
                        movingDown = False
                        movingLeft = False
                        movingRight = False

                elif (event.key == K_RIGHT or famicom.get_axis(0) > 0):
                    if (direction == 0 or direction == 2):
                        if isValidPosition(board, fallingPiece, adjX=1):
                            fallingPiece['x'] += 1
                            movingRight = True
                            movingLeft = False
                            lastMoveSidewaysTime = time.time()
                    elif direction == 3:
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjX=+1):
                            fallingPiece['x'] += 1
                        lastMoveDownTime = time.time()
                    else:
                        movingDown = False
                        movingLeft = False
                        movingRight = False

                elif (event.key == K_DOWN or famicom.get_axis(1) > 0):
                    if direction == 0:
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjY=1):
                            fallingPiece['y'] += 1
                        lastMoveDownTime = time.time()
                    elif direction == 1 or direction == 3:
                        if isValidPosition(board, fallingPiece, adjY=1):
                            fallingPiece['y'] += 1
                            movingRight = True
                            movingLeft = False
                            lastMoveSidewaysTime = time.time()
                    else:
                        movingDown = False
                        movingLeft = False
                        movingRight = False

                elif (event.key == K_UP or famicom.get_axis(1) < 0):
                    if direction == 2:
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjY=-1):
                            fallingPiece['y'] -= 1
                        lastMoveDownTime = time.time()
                    elif (direction == 1 or direction == 3):
                        if isValidPosition(board, fallingPiece, adjY=-1):
                            fallingPiece['y'] -= 1
                            movingRight = False
                            movingLeft = True
                            lastMoveSidewaysTime = time.time()
                    else:
                        movingDown = False
                        movingLeft = False
                        movingRight = False

                # move the current piece all the way down
                elif event.key == K_SPACE or famicom.get_button(0):
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    if direction == 0:
                        for i in range(1, BOARDHEIGHT):
                            if not isValidPosition(board, fallingPiece, adjY=i):
                                break
                        fallingPiece['y'] += i - 1
                    elif direction == 1:
                        for i in range(1, BOARDWIDTH):
                            if not isValidPosition(board, fallingPiece, adjX=(-1) * i):
                                break
                        fallingPiece['x'] -= i - 1
                    elif direction == 2:
                        for i in range(1, BOARDHEIGHT):
                            if not isValidPosition(board, fallingPiece, adjY=(-1)*i):
                                break
                        fallingPiece['y'] -= i - 1
                    else:
                        for i in range(1, BOARDWIDTH):
                            if not isValidPosition(board, fallingPiece, adjX=i):
                                break
                        fallingPiece['x'] += i - 1
        '''

        '''
        if (famicom.get_axis(0) > 0.5 or famicom.get_axis(0) < -0.5) or (
                famicom.get_axis(1) > 0.5 or famicom.get_axis(1) < -0.5):
            if not JOYAXISDOWN and not JOYAXISUP and not button:
                JOYAXISDOWN = True
                JOYAXISUP = False
                button = True
            elif JOYAXISDOWN and button:
                JOYAXISDOWN = False
                JOYAXISUP = False
                button = True
            elif not JOYAXISDOWN and button:
                JOYAXISDOWN = False
                JOYAXISUP = False
                button = True
        else:
            if not JOYAXISDOWN and not JOYAXISUP and button:
                JOYAXISDOWN = False
                JOYAXISUP = True
                button = False
            elif not JOYAXISDOWN and JOYAXISUP and not button:
                JOYAXISDOWN = False
                JOYAXISUP = False
                button = False
            elif not JOYAXISDOWN and not JOYAXISUP and not button:
                JOYAXISDOWN = False
                JOYAXISUP = False
                button = False
        '''

        for event in pygame.event.get():  # event
            if event.type == JOYAXISMOTION:
                if event.value == -3.051850947599719e-05:
                    JOYAXISDOWN = False
                    JOYAXISUP = True
                else:
                    JOYAXISDOWN = True
                    JOYAXISUP = False
                    AXIS = event.axis
                    VALUE = event.value
            if event.type == JOYBUTTONUP:
                if event.button == 7:
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    channel1.pause()
                    channel2.play(pause)
                    showTextScreen('Paused')  # pause until a key press
                    channel1.unpause()
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()

            elif event.type == JOYBUTTONDOWN:
                # moving the piece sideways
                if event.button == 1:
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(
                        PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(
                            PIECES[fallingPiece['shape']])

                # move the current piece all the way down
                elif (event.button == 0):
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    if direction == 0:
                        for i in range(1, BOARDHEIGHT):
                            if not isValidPosition(board, fallingPiece, adjY=i):
                                break
                        fallingPiece['y'] += i - 1
                    elif direction == 1:
                        for i in range(1, BOARDWIDTH):
                            if not isValidPosition(board, fallingPiece, adjX=(-1) * i):
                                break
                        fallingPiece['x'] -= i - 1
                    elif direction == 2:
                        for i in range(1, BOARDHEIGHT):
                            if not isValidPosition(board, fallingPiece, adjY=(-1) * i):
                                break
                        fallingPiece['y'] -= i - 1
                    else:
                        for i in range(1, BOARDWIDTH):
                            if not isValidPosition(board, fallingPiece, adjX=i):
                                break
                        fallingPiece['x'] += i - 1

            if JOYAXISUP:
                if AXIS == 0 and VALUE < 0:
                    if direction == 0 or direction == 2:
                        movingLeft = False
                    elif direction == 1:
                        movingDown = False
                elif AXIS == 0 and VALUE > 0:
                    if direction == 0 or direction == 2:
                        movingRight = False
                    elif direction == 3:
                        movingDown = False
                elif AXIS == 1 and VALUE > 0:
                    if direction == 0:
                        movingDown = False
                    elif direction == 1 or direction == 3:
                        movingRight = False
                elif AXIS == 1 and VALUE < 0:
                    if direction == 1 or direction == 3:
                        movingLeft = False
                    elif direction == 2:
                        movingDown = False
            elif JOYAXISDOWN:
                if AXIS == 0 and VALUE < 0:
                    if direction == 0 or direction == 2:
                        if isValidPosition(board, fallingPiece, adjX=-1):
                            fallingPiece['x'] -= 1
                            movingLeft = True
                            movingRight = False
                            lastMoveSidewaysTime = time.time()
                    elif direction == 1:
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjX=-1):
                            fallingPiece['x'] -= 1
                        lastMoveDownTime = time.time()
                    else:
                        movingDown = False
                        movingLeft = False
                        movingRight = False

                elif AXIS == 0 and VALUE > 0:
                    if (direction == 0 or direction == 2):
                        if isValidPosition(board, fallingPiece, adjX=1):
                            fallingPiece['x'] += 1
                            movingRight = True
                            movingLeft = False
                            lastMoveSidewaysTime = time.time()
                    elif direction == 3:
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjX=+1):
                            fallingPiece['x'] += 1
                        lastMoveDownTime = time.time()
                    else:
                        movingDown = False
                        movingLeft = False
                        movingRight = False

                elif (AXIS == 1 and VALUE > 0):
                    if direction == 0:
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjY=1):
                            fallingPiece['y'] += 1
                        lastMoveDownTime = time.time()
                    elif direction == 1 or direction == 3:
                        if isValidPosition(board, fallingPiece, adjY=1):
                            fallingPiece['y'] += 1
                            movingRight = True
                            movingLeft = False
                            lastMoveSidewaysTime = time.time()
                    else:
                        movingDown = False
                        movingLeft = False
                        movingRight = False

                elif AXIS == 1 and VALUE < 0:
                    if direction == 2:
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjY=-1):
                            fallingPiece['y'] -= 1
                        lastMoveDownTime = time.time()
                    elif (direction == 1 or direction == 3):
                        if isValidPosition(board, fallingPiece, adjY=-1):
                            fallingPiece['y'] -= 1
                            movingRight = False
                            movingLeft = True
                            lastMoveSidewaysTime = time.time()
                    else:
                        movingDown = False
                        movingLeft = False
                        movingRight = False

        # handle moving the piece because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft:
                if direction == 0 or direction == 2:
                    if isValidPosition(board, fallingPiece, adjX=-1):
                        fallingPiece['x'] -= 1
                else:
                    if isValidPosition(board, fallingPiece, adjY=-1):
                        fallingPiece['y'] -= 1
            elif movingRight:
                if direction == 0 or direction == 2:
                    if isValidPosition(board, fallingPiece, adjX=1):
                        fallingPiece['x'] += 1
                else:
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ:
            if direction == 0:
                if isValidPosition(board, fallingPiece, adjY=1):
                    fallingPiece['y'] += 1
            elif direction == 1:
                if isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
            elif direction == 2:
                if isValidPosition(board, fallingPiece, adjY=-1):
                    fallingPiece['y'] -= 1
            else:
                if isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
            lastMoveDownTime = time.time()



        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if direction == 0:
                if not isValidPosition(board, fallingPiece, adjY=1):
                    # falling piece has landed, set it on the board
                    addToBoard(board, fallingPiece)
                    channel2.play(bump)
                    score += removeCompleteLines(board)
                    level, fallFreq = calculateLevelAndFallFreq(score)
                    fallingPiece = None
                else:
                    # piece did not land, just move the piece down
                    fallingPiece['y'] += 1
                    lastFallTime = time.time()
            elif direction == 1:
                if not isValidPosition(board, fallingPiece, adjX=-1):
                    # falling piece has landed, set it on the board
                    addToBoard(board, fallingPiece)
                    channel2.play(bump)
                    score += removeCompleteLines(board)
                    level, fallFreq = calculateLevelAndFallFreq(score)
                    fallingPiece = None
                else:
                    # piece did not land, just move the piece down
                    fallingPiece['x'] -= 1
                    lastFallTime = time.time()
            elif direction == 2:
                if not isValidPosition(board, fallingPiece, adjY=-1):
                    # falling piece has landed, set it on the board
                    addToBoard(board, fallingPiece)
                    channel2.play(bump)
                    score += removeCompleteLines(board)
                    level, fallFreq = calculateLevelAndFallFreq(score)
                    fallingPiece = None
                else:
                    # piece did not land, just move the piece down
                    fallingPiece['y'] -= 1
                    lastFallTime = time.time()
            else:
                if not isValidPosition(board, fallingPiece, adjX=1):
                    # falling piece has landed, set it on the board
                    addToBoard(board, fallingPiece)
                    channel2.play(bump)
                    score += removeCompleteLines(board)
                    level, fallFreq = calculateLevelAndFallFreq(score)
                    fallingPiece = None
                else:
                    # piece did not land, just move the piece down
                    fallingPiece['x'] += 1
                    lastFallTime = time.time()
        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level, life)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()

def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    '''
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
        if event.type == KEYUP:
            if event.key == K_r:
                break
    '''
    for event in pygame.event.get([JOYBUTTONDOWN, JOYBUTTONUP]):
        if event.type == JOYBUTTONDOWN:
            continue
        return event.button
        if event.type == JOYBUTTONUP:
            if event.button == 3:
                break

    return None

def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to continue.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

    channel2.stop()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    '''
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back
    '''
    for event in pygame.event.get(JOYBUTTONDOWN):
        if famicom.get_button(2):
            terminate()
        pygame.event.post(event)

def calculateLevelAndFallFreq(score):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(score / 4) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getNewPiece(direction):
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': 0,
                'y': 0,
                'color': random.randint(0, len(COLORS)-2)}
    if direction == 0:
        newPiece['x'] = int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2)
        newPiece['y'] = 0 # start it above the board (i.e. less than 0)
    elif direction == 1:
        newPiece['x'] = BOARDWIDTH - 4
        newPiece['y'] = int(BOARDHEIGHT / 2) - int(TEMPLATEHEIGHT / 2)
    elif direction == 2:
        newPiece['x'] = int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2)
        newPiece['y'] = BOARDHEIGHT - 4 # start it above the board (i.e. less than 0)
    else:
        newPiece['x'] = 0
        newPiece['y'] = int(BOARDHEIGHT / 2) - int(TEMPLATEHEIGHT / 2)
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    for i in range(5):
        for j in range(5):
            board[20 + i][20 + j] = len(COLORS)-1
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, i):
    # Return True if the line filled with boxes with no gaps.
    for x in range(0, BOARDWIDTH - 2 * i):
        for y in range(0, BOARDHEIGHT - 2 * i):
            if x * (x - BOARDWIDTH + 2 * i + 1) == 0 or y * (y - BOARDHEIGHT + 2 * i + 1) == 0:
                if board[x + i][y + i] == BLANK:
                    return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    i = int((BOARDHEIGHT - CENTERHEIGHT) / 2) - 1 # start y at the bottom of the board
    while i >= 0:
        if isCompleteLine(board, i):
            # Remove the line and pull boxes down by one line.
            channel2.play(line_clear_sound, 0)
            for pullDown in range(i, 0, -1):
                for x in range(0, BOARDWIDTH - 2 * pullDown - 2):
                    board[x + pullDown + 1][pullDown] = board[x + pullDown + 1][pullDown-1]
                    board[x + pullDown + 1][BOARDHEIGHT - 1 - pullDown] = board[x + pullDown + 1][BOARDHEIGHT - pullDown]
                for y in range(0, BOARDWIDTH - 2 * pullDown - 2):
                    board[pullDown][y + pullDown + 1] = board[pullDown - 1][y + pullDown + 1]
                    board[BOARDWIDTH - 1 - pullDown][y + pullDown + 1] = board[BOARDHEIGHT - pullDown][y + pullDown + 1]
                board[pullDown][pullDown] = board[pullDown - 1][pullDown - 1]
                board[pullDown][BOARDHEIGHT - 1 - pullDown] = board[pullDown - 1][BOARDHEIGHT - pullDown]
                board[BOARDWIDTH - 1 - pullDown][pullDown] = board[BOARDWIDTH - pullDown][pullDown - 1]
                board[BOARDWIDTH - 1 - pullDown][BOARDHEIGHT - 1 - pullDown] = board[BOARDWIDTH - pullDown][BOARDHEIGHT - pullDown]

            for l in range(BOARDWIDTH):
                board[l][0] = BLANK
                board[l][BOARDHEIGHT - 1] = BLANK
                board[0][l] = BLANK
                board[BOARDWIDTH - 1][l] = BLANK

            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            i -= 1 # move on to check next row up
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each quatris piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])


def drawStatus(score, level, life):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)

    lifeSurf = BASICFONT.render('Life: %s' % life, True, TEXTCOLOR)
    lifeRect = lifeSurf.get_rect()
    lifeRect.topleft = (WINDOWWIDTH - 150, 200)
    DISPLAYSURF.blit(lifeSurf, lifeRect)

    if music == ct:
        musicTitle = 'Chrono Trigger'
    elif music == ab:
        musicTitle = 'Angry Birds'
    elif music == tetris:
        musicTitle = 'Tetris'
    elif music == tloz:
        musicTitle = 'The Legend of Zelda'
    elif music == gta_4:
        musicTitle = 'Grand Theft Auto 4'
    elif music == ff:
        musicTitle = 'Final Fantasy'
    elif music == tes_4_o:
        musicTitle = 'The Elder Scrolls IV Oblivion'
    elif music == f_3:
        musicTitle = 'Fallout 3'
    elif music == h:
        musicTitle = 'Halo'
    elif music == h_3:
        musicTitle = 'Halo 3'
    elif music == tes_5_s_f:
        musicTitle = 'The Elder Scrolls V Skyrim : Far Horizons'
    elif music == tes_5_s_d:
        musicTitle = 'The Elder Scrolls V Skyrim : Dragonborn'
    elif music == p_1:
        musicTitle = 'Portal'
    elif music == p_2:
        musicTitle = 'Portal 2'
    elif music == m:
        musicTitle = 'Minecraft'
    elif music == tw_3_wh:
        musicTitle = 'The Witcher 3 Wild Hunt'
    else:
        musicTitle = 'Super Mario Bros.'
    musicSurf = BASICFONT.render('BGM: %s' % musicTitle, True, TEXTCOLOR)
    musicRect = musicSurf.get_rect()
    DISPLAYSURF.blit(musicSurf, musicRect)


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)


if __name__ == '__main__':
    main()
